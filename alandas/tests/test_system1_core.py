"""Tests for pure Alandas System 1 lead logic."""

from __future__ import annotations

import asyncio
import unittest

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


class System1CoreTests(unittest.TestCase):
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

    def test_discovery_request_is_bounded_to_target_cities(self) -> None:
        self.assertEqual(validate_discovery_request("Berlin", ["specialty cafe"], 10), [])
        self.assertIn(
            "city must be one of Berlin, Hamburg, or Munich",
            validate_discovery_request("Paris", ["cafe"], 10),
        )
        self.assertIn(
            "limit must be between 1 and 50",
            validate_discovery_request("Berlin", ["cafe"], 51),
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
