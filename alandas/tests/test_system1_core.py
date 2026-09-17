"""Tests for pure Alandas System 1 lead logic."""

from __future__ import annotations

import asyncio
import unittest
from datetime import date
import json
from decimal import Decimal

from system_1.core import (
    apply_research_evidence,
    audit_event_key,
    can_approve_outreach,
    can_record_send,
    draft_outreach,
    enrich_lead,
    lead_workflow_id,
    normalize_lead,
    slug,
    validate_intake,
    validate_lead,
    website_domain,
)
from system_1.models import LeadInput, LeadWorkflowState, ResearchEvidence
from system_1.apify_google_maps import (
    candidate_to_lead,
    map_apify_dataset,
    map_apify_place,
    validate_discovery_request,
)
from system_1.public_research import (
    candidate_urls,
    research_public_pages,
    validate_public_url,
)
from system_1.outscraper_google_maps import candidate_to_lead as outscraper_candidate_to_lead
from system_1.outscraper_google_maps import map_outscraper_callback
from system_1.outscraper_webhook import receive_outscraper_callback, validate_webhook_token
from system_1.discovery_policy import TrialPolicy
from system_1.discovery_runs import InMemoryDiscoveryStore, retry_decision
from system_1.apify_provider import ApifyProvider, CostLimitExceeded
from system_1.outscraper_provider import OutscraperProvider
from system_1.provider_http import HttpResponse
from system_1.discovery_scheduler import schedule_action
from system_1.discovery_workflows import final_daily_status


class FakeTransport:
    def __init__(self, response_json: dict[str, object], status_code: int = 201) -> None:
        self.response_json = response_json
        self.status_code = status_code
        self.requests: list[object] = []

    def request(self, method: str, url: str, headers: dict[str, str], body: bytes | None, timeout_seconds: int) -> HttpResponse:
        self.requests.append(
            type(
                "Request",
                (),
                {"method": method, "url": url, "headers": headers, "body": body},
            )()
        )
        return HttpResponse(self.status_code, self.response_json)


class FakeUrlResponse:
    def __init__(self, status_code: int, payload: bytes) -> None:
        self.status = status_code
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self) -> "FakeUrlResponse":
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> bool:
        return False


class System1CoreTests(unittest.TestCase):
    def test_daily_status_is_degraded_when_one_provider_fails(self) -> None:
        self.assertEqual(
            final_daily_status({"apify": "succeeded", "outscraper": "needs_attention"}),
            "degraded",
        )

    def test_day_eight_pauses_without_submission(self) -> None:
        policy = TrialPolicy.default(date(2026, 9, 17))

        self.assertEqual(schedule_action(policy, date(2026, 9, 24)), "pause")

    def test_apify_refuses_cost_above_policy_cap(self) -> None:
        provider = ApifyProvider(token="secret", transport=FakeTransport({}))

        with self.assertRaises(CostLimitExceeded):
            provider.submit(
                TrialPolicy.default(date(2026, 9, 17)),
                "discovery:trial-v1:2026-09-17",
                Decimal("1.41"),
            )

    def test_outscraper_request_has_no_paid_enrichment_parameters(self) -> None:
        transport = FakeTransport({"id": "request-123", "status": "Pending"})
        provider = OutscraperProvider(token="secret", transport=transport)

        provider.submit(
            TrialPolicy.default(date(2026, 9, 17)),
            "discovery:trial-v1:2026-09-17",
            "https://receiver.example/callback?token=hidden",
            Decimal("0.60"),
        )

        request = transport.requests[0]
        self.assertIn("limit=50", request.url)
        self.assertNotIn("contacts_n_leads", request.url)
        self.assertNotIn("emails_validator_service", request.url)
        self.assertNotIn("secret", request.url)

    def test_apify_allocation_has_its_own_result_and_cost_cap(self) -> None:
        transport = FakeTransport({"data": {"id": "run-cafe"}})
        provider = ApifyProvider(token="secret", transport=transport)

        provider.submit_allocation(
            TrialPolicy.default(date(2026, 9, 17)),
            "discovery:trial-v1:2026-09-17",
            "cafe",
            20,
            Decimal("0.56"),
        )

        request = transport.requests[0]
        payload = json.loads(request.body)
        self.assertEqual(payload["searchStringsArray"], ["cafe"])
        self.assertEqual(payload["locationQuery"], "Germany")
        self.assertEqual(payload["maxCrawledPlacesPerSearch"], 20)
        self.assertIn("maxTotalChargeUsd=0.56", request.url)

    def test_outscraper_reconciliation_uses_saved_request_id(self) -> None:
        transport = FakeTransport({"status": "Success", "data": []}, status_code=200)
        provider = OutscraperProvider(token="secret", transport=transport)

        provider.reconcile("request-123")

        request = transport.requests[0]
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.url, "https://api.outscraper.com/requests/request-123")
        self.assertNotIn("secret", request.url)

    def test_http_transport_decodes_provider_json_without_logging_credentials(self) -> None:
        from system_1.provider_http import UrllibHttpTransport

        captured: list[object] = []

        def fake_open(request: object, timeout: int) -> FakeUrlResponse:
            captured.append(request)
            self.assertEqual(timeout, 30)
            return FakeUrlResponse(202, b'{"id":"request-123"}')

        response = UrllibHttpTransport(open_request=fake_open).request(
            "GET",
            "https://api.example/requests",
            {"X-API-KEY": "secret"},
            None,
            30,
        )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json_body, {"id": "request-123"})
        self.assertEqual(len(captured), 1)
    def test_provider_submission_is_idempotent(self) -> None:
        store = InMemoryDiscoveryStore()

        first = store.record_submission(
            "discovery:trial-v1:2026-09-17", "apify", "run-a", Decimal("1.40")
        )
        second = store.record_submission(
            "discovery:trial-v1:2026-09-17", "apify", "run-a", Decimal("1.40")
        )

        self.assertEqual(first, second)

    def test_unknown_charge_outcome_requires_reconciliation(self) -> None:
        decision = retry_decision(status_code=None, outcome_known=False, attempt_number=1)

        self.assertEqual(decision.action, "reconcile")

    def test_first_transient_failure_waits_thirty_seconds(self) -> None:
        decision = retry_decision(status_code=503, outcome_known=True, attempt_number=1)

        self.assertEqual(decision.action, "retry")
        self.assertEqual(decision.delay_seconds, 30)

    def test_third_transient_failure_waits_ten_minutes(self) -> None:
        decision = retry_decision(status_code=503, outcome_known=True, attempt_number=3)

        self.assertEqual(decision.action, "retry")
        self.assertEqual(decision.delay_seconds, 600)
    def test_trial_policy_has_approved_allocations(self) -> None:
        policy = TrialPolicy.default(date(2026, 9, 17))

        self.assertEqual(
            policy.apify_allocations,
            {
                "cafe": 20,
                "brunch venue": 10,
                "specialty coffee venue": 10,
                "boutique hotel": 10,
            },
        )
        self.assertEqual(policy.outscraper_limit, 50)
        self.assertTrue(policy.for_date(date(2026, 9, 23)))
        self.assertFalse(policy.for_date(date(2026, 9, 24)))

    def test_outscraper_callback_maps_only_basic_business_fields(self) -> None:
        candidates, notes = map_outscraper_callback(
            {
                "id": "request-123",
                "status": "Success",
                "data": [[{
                    "place_id": "place-123",
                    "name": "Example Cafe",
                    "city": "Cologne",
                    "type": "Cafe",
                    "country_code": "DE",
                    "site": "https://example.de",
                    "phone": "+4930123456",
                    "full_address": "Example Street 1, Cologne",
                    "location_link": "https://www.google.com/maps/place/example",
                    "email": "ignore@example.de",
                    "reviews_data": [{"text": "ignore"}],
                }]],
            }
        )

        self.assertEqual(notes, [])
        self.assertEqual(len(candidates), 1)
        lead = outscraper_candidate_to_lead(candidates[0])
        self.assertEqual(lead.website, "https://example.de")
        self.assertEqual(lead.email, "")

    def test_outscraper_callback_rejects_more_than_fifty_rows(self) -> None:
        record = {
            "place_id": "place-123",
            "name": "Example Cafe",
            "city": "Berlin",
            "type": "Cafe",
            "country_code": "DE",
            "location_link": "https://www.google.com/maps/place/example",
        }
        with self.assertRaises(ValueError):
            map_outscraper_callback({"status": "Success", "data": [[record] * 51]})

    def test_outscraper_webhook_token_requires_long_exact_value(self) -> None:
        with self.assertRaises(RuntimeError):
            validate_webhook_token("anything", "too-short")
        with self.assertRaises(PermissionError):
            validate_webhook_token("wrong", "x" * 32)
        validate_webhook_token("x" * 32, "x" * 32)

    def test_outscraper_callback_starts_once_and_audits_summary(self) -> None:
        payload = {
            "id": "request-123",
            "status": "Success",
            "data": [[{
                "place_id": "place-123",
                "name": "Example Cafe",
                "city": "Berlin",
                "type": "Cafe",
                "country_code": "DE",
                "location_link": "https://www.google.com/maps/place/example",
            }]],
        }
        started: list[LeadInput] = []

        async def fake_start(lead: LeadInput) -> str:
            started.append(lead)
            return "started"

        audit_calls: list[dict[str, object]] = []

        def fake_audit(**kwargs: object) -> bool:
            audit_calls.append(kwargs)
            return True

        result = asyncio.run(
            receive_outscraper_callback(
                payload,
                provided_token="x" * 32,
                expected_token="x" * 32,
                start_workflow=fake_start,
                audit_writer=fake_audit,
            )
        )

        self.assertEqual(result["started"], 1)
        self.assertEqual(len(started), 1)
        self.assertEqual(len(audit_calls), 1)
    def test_apify_place_maps_to_a_raw_lead_without_paid_enrichment_fields(self) -> None:
        candidate = map_apify_place(
            {
                "placeId": "place-123",
                "url": "https://www.google.com/maps/place/example",
                "title": "Example Cafe",
                "city": "Berlin",
                "categoryName": "Cafe",
                "countryCode": "DE",
                "website": "https://www.example.de/",
                "phoneUnformatted": "+4930123456",
                "address": "Example Street 1",
                "email": "do-not-import@example.de",
            }
        )

        self.assertIsNotNone(candidate)
        lead = candidate_to_lead(candidate)
        self.assertEqual(lead.website, "https://www.example.de")
        self.assertEqual(lead.phone, "+4930123456")
        self.assertEqual(lead.email, "")

    def test_apify_dataset_skips_closed_and_duplicate_places(self) -> None:
        record = {
            "placeId": "place-123",
            "url": "https://www.google.com/maps/place/example",
            "title": "Example Cafe",
            "city": "Berlin",
            "categoryName": "Cafe",
            "countryCode": "DE",
        }
        closed = {**record, "placeId": "place-closed", "permanentlyClosed": True}

        candidates, notes = map_apify_dataset([record, record, closed])

        self.assertEqual(len(candidates), 1)
        self.assertEqual(len(notes), 2)

    def test_discovery_request_is_bounded_to_germany_wide_scope(self) -> None:
        self.assertEqual(validate_discovery_request("Germany", ["specialty cafe"], 10), [])
        self.assertIn(
            "search scope is required",
            validate_discovery_request(" ", ["cafe"], 10),
        )
        self.assertIn(
            "limit must be between 1 and 50",
            validate_discovery_request("Germany", ["cafe"], 51),
        )
    def test_valid_lead_passes(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
            fit_score=4,
        )

        self.assertEqual(validate_lead(lead), [])

    def test_missing_contact_route_fails(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
        )

        self.assertIn("at least one contact route is required", validate_lead(lead))
        self.assertEqual(validate_intake(lead), [])

    def test_normalization_makes_stable_identity_values(self) -> None:
        lead = LeadInput(
            venue_name="  Example Cafe ",
            city=" Berlin ",
            venue_type=" cafe ",
            source_url="https://maps.example/cafe",
            website="https://www.example.de/menu?day=today",
            instagram="https://instagram.com/example_cafe/",
        )

        normalized = normalize_lead(lead)

        self.assertEqual(normalized.venue_name, "Example Cafe")
        self.assertEqual(normalized.website, "https://www.example.de/menu?day=today")
        self.assertEqual(website_domain(normalized.website), "example.de")

    def test_research_evidence_fills_only_empty_contact_fields(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://maps.example/cafe",
            email="owner@example.de",
        )
        evidence = [
            ResearchEvidence("email", "new@example.de", "https://example.de/impressum", "email"),
            ResearchEvidence("phone", "+49 30 123456", "https://example.de/impressum", "tel"),
        ]

        enriched = apply_research_evidence(lead, evidence)

        self.assertEqual(enriched.email, "owner@example.de")
        self.assertEqual(enriched.phone, "+49 30 123456")

    def test_public_research_uses_bounded_candidate_pages_and_extracts_evidence(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://maps.example/cafe",
            website="https://example.de",
        )

        def fake_fetch(url: str) -> str:
            if url.endswith("/impressum"):
                return (
                    '<a href="mailto:hello@example.de">Email</a>'
                    '<a href="tel:+4930123456">Call</a>'
                    '<a href="https://instagram.com/example_cafe/">Instagram</a>'
                )
            return "<html><body>No contact yet</body></html>"

        evidence, notes = research_public_pages(lead, fetcher=fake_fetch)

        self.assertLessEqual(len(candidate_urls(lead)), 6)
        self.assertEqual({item.field for item in evidence}, {"email", "phone", "instagram", "impressum_url"})
        self.assertFalse(notes)

    def test_public_research_rejects_private_network_targets(self) -> None:
        def private_resolver(*_args: object, **_kwargs: object) -> list[tuple]:
            return [(2, 1, 6, "", ("127.0.0.1", 0))]

        with self.assertRaises(ValueError):
            validate_public_url("http://internal.example", resolver=private_resolver)

    def test_fit_score_range_is_checked(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
            fit_score=6,
        )

        self.assertIn("fit_score must be between 1 and 5", validate_lead(lead))

    def test_enrichment_lists_missing_research(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
        )

        notes = enrich_lead(lead)

        self.assertIn("Find public Impressum or contact page", notes)
        self.assertIn("Find email from website, Impressum, or approved tool", notes)

    def test_draft_requires_sidy_approval(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
        )

        draft = draft_outreach(lead)

        self.assertFalse(draft.allowed_to_send)
        self.assertIn("EUR 19 discovery box", draft.body)

    def test_lead_workflow_id_is_stable(self) -> None:
        lead = LeadInput(
            venue_name="Cafe Beispiel Mitte",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
        )

        self.assertEqual(lead_workflow_id(lead), "alandas-lead-berlin-cafe-beispiel-mitte")

    def test_slug_handles_empty_values(self) -> None:
        self.assertEqual(slug("   "), "lead")

    def test_audit_event_key_is_stable_for_retries(self) -> None:
        first_attempt = audit_event_key("alandas-lead-123", "outreach_approved")
        retry_attempt = audit_event_key("alandas-lead-123", "outreach_approved")

        self.assertEqual(first_attempt, retry_attempt)
        self.assertNotEqual(
            first_attempt,
            audit_event_key("alandas-lead-123", "send_recorded"),
        )

    def test_audit_event_key_requires_both_parts(self) -> None:
        with self.assertRaises(ValueError):
            audit_event_key("", "send_recorded")
        with self.assertRaises(ValueError):
            audit_event_key("alandas-lead-123", "")

    def test_send_record_is_rejected_before_approval(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
        )
        state = LeadWorkflowState(
            lead=lead,
            status="drafted",
            outreach_draft=draft_outreach(lead),
        )

        self.assertFalse(can_record_send(state))

    def test_approval_and_send_require_the_right_state(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
        )
        state = LeadWorkflowState(
            lead=lead,
            status="drafted",
            outreach_draft=draft_outreach(lead),
        )

        self.assertTrue(can_approve_outreach(state))
        self.assertFalse(can_record_send(state))

        state.sidy_approved = True
        state.outreach_draft.allowed_to_send = True
        state.status = "approved"

        self.assertTrue(can_record_send(state))


if __name__ == "__main__":
    unittest.main()
