"""Tests for pure Alandas System 1 lead logic."""

from __future__ import annotations

import asyncio
import unittest
from datetime import date, datetime, timezone
import json
from decimal import Decimal
from pathlib import Path
import sys
from types import ModuleType
from unittest.mock import patch

if "temporalio" not in sys.modules:
    _temporalio = ModuleType("temporalio")
    _temporalio.__path__ = []
    _client = ModuleType("temporalio.client")
    class _ClientStub:
        @classmethod
        async def connect(cls, *args, **kwargs):
            return cls()
    _client.Client = _ClientStub
    _temporalio.client = _client
    _worker = ModuleType("temporalio.worker")
    _worker.Worker = type("Worker", (), {})
    _temporalio.worker = _worker
    _activity = ModuleType("temporalio.activity")
    _activity.defn = lambda fn=None, **kwargs: (lambda f: f) if fn is None else fn
    _temporalio.activity = _activity
    _workflow = ModuleType("temporalio.workflow")
    _workflow.defn = lambda cls=None, **kwargs: (lambda c: c) if cls is None else cls
    _workflow.run = lambda fn=None, **kwargs: (lambda f: f) if fn is None else fn
    _workflow.signal = lambda fn=None, **kwargs: (lambda f: f) if fn is None else fn
    _workflow.query = lambda fn=None, **kwargs: (lambda f: f) if fn is None else fn
    _workflow.now = lambda: datetime.now(timezone.utc)
    _workflow.execute_activity = lambda *args, **kwargs: None
    _unsafe = ModuleType("temporalio.workflow.unsafe")
    from contextlib import contextmanager
    @contextmanager
    def _imports_passed_through():
        yield
    _unsafe.imports_passed_through = _imports_passed_through
    _workflow.unsafe = _unsafe
    _temporalio.workflow = _workflow
    sys.modules["temporalio"] = _temporalio
    sys.modules["temporalio.client"] = _client
    sys.modules["temporalio.worker"] = _worker
    sys.modules["temporalio.activity"] = _activity
    sys.modules["temporalio.workflow"] = _workflow
    sys.modules["temporalio.workflow.unsafe"] = _unsafe

if "psycopg" not in sys.modules:
    _psycopg = ModuleType("psycopg")
    _psycopg.Connection = object
    sys.modules["psycopg"] = _psycopg

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
from system_1.discovery_scheduler import (
    daily_workflow_id,
    policy_for_trial_start,
    schedule_action,
    scheduled_day_in_berlin,
    start_manual_daily_run,
    start_trial_schedule,
    trial_schedule_definition,
)
from system_1.discovery_workflows import final_daily_status
from system_1.discovery_controls import format_daily_status, validate_scheduler_environment
from system_1.worker_health import (
    format_worker_health,
    parse_host_port,
)
from system_1.discovery_reconcile import (
    fetch_apify_run_details,
    format_reconciliation_report,
    reconcile_daily_discovery_run,
)
from system_1.import_apify_dataset import (
    execute_apify_import,
    fetch_apify_dataset_items,
    format_import_summary,
    get_provider_run_external_id,
    import_apify_candidates,
)
from system_1.qualify_discovery_leads import (
    evaluate_lead_qualification,
    format_qualification_summary,
    qualify_leads_batch,
)
from system_1.plan_discovery_enrichment import (
    format_plan_summary,
    plan_enrichment_batch,
    plan_lead_enrichment_steps,
)
from system_1.discovery_activities import submit_daily_discovery_providers_activity


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
    def test_start_refuses_when_feature_flag_is_off(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "SYSTEM1_DISCOVERY_ENABLED"):
            validate_scheduler_environment({"SYSTEM1_DISCOVERY_ENABLED": "false"})

    def test_status_output_redacts_tokens(self) -> None:
        output = format_daily_status(
            {"daily_run_id": "discovery:trial-v1:2026-09-17", "status": "not_started"},
            {"APIFY_API_TOKEN": "secret", "OUTSCRAPER_API_KEY": "another-secret"},
        )

        self.assertNotIn("secret", output)
        self.assertIn("Apify configured: yes", output)

    def test_enabled_discovery_requires_a_callback_base_url(self) -> None:
        environment = {
            "SYSTEM1_DISCOVERY_ENABLED": "true",
            "APIFY_API_TOKEN": "apify-token",
            "OUTSCRAPER_API_KEY": "outscraper-token",
            "OUTSCRAPER_WEBHOOK_TOKEN": "12345678901234567890123456789012",
        }

        with self.assertRaisesRegex(RuntimeError, "CALLBACK_BASE_URL"):
            validate_scheduler_environment(environment)

    def test_apify_only_environment_validates_without_outscraper(self) -> None:
        environment = {
            "SYSTEM1_DISCOVERY_ENABLED": "true",
            "APIFY_API_TOKEN": "valid-token",
            "SYSTEM1_DISCOVERY_MAX_APIFY_USD": "1.40",
        }
        # Must validate cleanly without Outscraper credentials or webhook settings
        validate_scheduler_environment(environment)

    def test_missing_apify_token_fails_in_apify_only_mode(self) -> None:
        environment = {
            "SYSTEM1_DISCOVERY_ENABLED": "true",
        }
        with self.assertRaisesRegex(RuntimeError, "APIFY_API_TOKEN"):
            validate_scheduler_environment(environment)

    def test_outscraper_only_mode_rejected_and_requires_apify_token(self) -> None:
        environment = {
            "SYSTEM1_DISCOVERY_ENABLED": "true",
            "SYSTEM1_DISCOVERY_PROVIDERS": "outscraper",
            "OUTSCRAPER_API_KEY": "outscraper-test-key",
            "OUTSCRAPER_WEBHOOK_TOKEN": "12345678901234567890123456789012",
            "SYSTEM1_DISCOVERY_OUTSCRAPER_CALLBACK_BASE_URL": "https://callback.example.com",
        }
        with self.assertRaisesRegex(RuntimeError, "APIFY_API_TOKEN|Apify is required"):
            validate_scheduler_environment(environment)

    def test_invalid_or_over_cap_apify_amount_fails(self) -> None:
        over_cap_env = {
            "SYSTEM1_DISCOVERY_ENABLED": "true",
            "APIFY_API_TOKEN": "valid-token",
            "SYSTEM1_DISCOVERY_MAX_APIFY_USD": "1.50",
        }
        with self.assertRaisesRegex(RuntimeError, "SYSTEM1_DISCOVERY_MAX_APIFY_USD"):
            validate_scheduler_environment(over_cap_env)

        invalid_decimal_env = {
            "SYSTEM1_DISCOVERY_ENABLED": "true",
            "APIFY_API_TOKEN": "valid-token",
            "SYSTEM1_DISCOVERY_MAX_APIFY_USD": "not-a-number",
        }
        with self.assertRaisesRegex(RuntimeError, "must be a decimal amount"):
            validate_scheduler_environment(invalid_decimal_env)

    def test_safe_status_output_apify_only_redacts_and_shows_configured(self) -> None:
        output = format_daily_status(
            {"daily_run_id": "discovery:trial-v1:2026-09-17", "status": "not_started"},
            {"APIFY_API_TOKEN": "super-secret-token"},
        )
        self.assertNotIn("super-secret-token", output)
        self.assertIn("Apify configured: yes", output)
        self.assertIn("Outscraper configured: no", output)

    @patch("system_1.discovery_activities.OutscraperProvider")
    @patch("system_1.discovery_activities.ApifyProvider")
    @patch("system_1.discovery_activities.db")
    @patch.dict(
        "os.environ",
        {
            "SYSTEM1_DISCOVERY_ENABLED": "true",
            "APIFY_API_TOKEN": "test-apify-token",
            "SYSTEM1_DISCOVERY_MAX_APIFY_USD": "1.40",
        },
        clear=True,
    )
    def test_provider_submission_skips_outscraper_when_not_configured(
        self, mock_db, mock_apify, mock_outscraper
    ) -> None:
        mock_db.reserve_discovery_provider_submission.return_value = (1, "ext-1", "reserved", True)
        mock_apify_instance = mock_apify.return_value
        mock_apify_instance.submit_allocation.return_value = type("Sub", (), {"external_id": "ext-1"})()

        statuses = submit_daily_discovery_providers_activity(
            {"daily_run_id": "test-run", "trial_starts_on": "2026-09-17"}
        )

        self.assertNotIn("outscraper", statuses)
        mock_outscraper.assert_not_called()
        reserved_providers = [call.args[1] for call in mock_db.reserve_discovery_provider_submission.call_args_list]
        self.assertNotIn("outscraper", reserved_providers)

    @patch.dict(
        "os.environ",
        {"SYSTEM1_DISCOVERY_ENABLED": "false", "APIFY_API_TOKEN": "test-apify-token"},
        clear=True,
    )
    def test_provider_submission_returns_disabled_when_flag_is_off(self) -> None:
        statuses = submit_daily_discovery_providers_activity(
            {"daily_run_id": "test-run", "trial_starts_on": "2026-09-17"}
        )
        self.assertEqual(statuses, {"status": "disabled"})
    def test_daily_status_is_degraded_when_one_provider_fails(self) -> None:
        self.assertEqual(
            final_daily_status({"apify": "succeeded", "outscraper": "needs_attention"}),
            "degraded",
        )

    def test_day_eight_pauses_without_submission(self) -> None:
        policy = TrialPolicy.default(date(2026, 9, 17))

        self.assertEqual(schedule_action(policy, date(2026, 9, 24)), "pause")

    def test_daily_workflow_id_is_stable_for_retries(self) -> None:
        policy = TrialPolicy.default(date(2026, 9, 17))

        self.assertEqual(
            daily_workflow_id(policy, date(2026, 9, 17)),
            "alandas-discovery-trial-v1-2026-09-17",
        )

    def test_trial_start_date_controls_the_day_eight_stop(self) -> None:
        policy = policy_for_trial_start("2026-09-17")

        self.assertEqual(schedule_action(policy, date(2026, 9, 24)), "pause")

    def test_scheduler_uses_the_berlin_calendar_day(self) -> None:
        instant = datetime(2026, 9, 17, 22, 30, tzinfo=timezone.utc)

        self.assertEqual(scheduled_day_in_berlin(instant), date(2026, 9, 18))

    def test_trial_schedule_has_a_berlin_clock_and_day_eight_end(self) -> None:
        definition = trial_schedule_definition(TrialPolicy.default(date(2026, 9, 17)))

        self.assertEqual(definition["schedule_id"], "alandas-discovery-trial-v1")
        self.assertEqual(definition["cron"], "0 9 * * *")
        self.assertEqual(definition["timezone"], "Europe/Berlin")
        self.assertEqual(definition["ends_on"], "2026-09-24")

    def test_trial_schedule_uses_the_deployed_temporal_timezone_keyword(self) -> None:
        scheduler_source = Path("system_1/discovery_scheduler.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("time_zone_name=definition[\"timezone\"]", scheduler_source)

    def test_trial_schedule_passes_workflow_inputs_via_temporal_args(self) -> None:
        """Protect the SDK boundary that only accepts one positional workflow input."""

        unset = object()

        class FakeScheduleActionStartWorkflow:
            def __init__(
                self,
                workflow: object,
                arg: object = unset,
                *,
                args: list[object] | None = None,
                id: str | None = None,
                task_queue: str | None = None,
            ) -> None:
                self.workflow = workflow
                self.arg = arg
                self.args = args
                self.id = id
                self.task_queue = task_queue

        class FakeSchedule:
            def __init__(self, *, action: object, spec: object, state: object) -> None:
                self.action = action
                self.spec = spec
                self.state = state

        class FakeScheduleSpec:
            def __init__(self, **values: object) -> None:
                self.values = values

        class FakeScheduleState:
            def __init__(self, **values: object) -> None:
                self.values = values

        class FakeClient:
            def __init__(self) -> None:
                self.created: list[tuple[str, object]] = []

            async def create_schedule(self, schedule_id: str, schedule: object) -> None:
                self.created.append((schedule_id, schedule))

        async def workflow_run(*_args: object) -> None:
            return None

        temporalio_module = ModuleType("temporalio")
        temporalio_client_module = ModuleType("temporalio.client")
        temporalio_client_module.Schedule = FakeSchedule
        temporalio_client_module.ScheduleActionStartWorkflow = FakeScheduleActionStartWorkflow
        temporalio_client_module.ScheduleSpec = FakeScheduleSpec
        temporalio_client_module.ScheduleState = FakeScheduleState
        temporalio_module.client = temporalio_client_module
        workflow_module = ModuleType("system_1.discovery_temporal_workflow")
        workflow_module.DailyDiscoveryWorkflow = type(
            "DailyDiscoveryWorkflow", (), {"run": workflow_run}
        )
        client = FakeClient()

        with patch.dict(
            sys.modules,
            {
                "temporalio": temporalio_module,
                "temporalio.client": temporalio_client_module,
                "system_1.discovery_temporal_workflow": workflow_module,
            },
        ), patch("system_1.discovery_scheduler.ZoneInfo", return_value=timezone.utc):
            schedule_id = asyncio.run(
                start_trial_schedule(
                    client,
                    TrialPolicy.default(date(2026, 9, 17)),
                    "alandas-system1",
                )
            )

        self.assertEqual(schedule_id, "alandas-discovery-trial-v1")
        self.assertEqual(len(client.created), 1)
        created_schedule = client.created[0][1]
        self.assertIs(created_schedule.action.workflow, workflow_run)
        self.assertIs(created_schedule.action.arg, unset)
        self.assertEqual(
            created_schedule.action.args,
            ["trial-v1", "2026-09-17"],
        )
        self.assertEqual(created_schedule.action.id, "alandas-discovery-trial-v1")
        self.assertEqual(created_schedule.action.task_queue, "alandas-system1")

    def test_start_manual_daily_run_passes_inputs_via_args(self) -> None:
        class FakeTemporalClient:
            def __init__(self) -> None:
                self.calls: list[dict[str, object]] = []

            async def start_workflow(
                self,
                workflow: object,
                *pos_args: object,
                id: str | None = None,
                task_queue: str | None = None,
                args: list[object] | None = None,
                **kwargs: object,
            ) -> object:
                if len(pos_args) > 1:
                    raise TypeError(
                        f"Client.start_workflow() takes from 2 to 3 positional arguments but {len(pos_args) + 1} positional arguments were given"
                    )
                self.calls.append(
                    {
                        "workflow": workflow,
                        "pos_args": pos_args,
                        "id": id,
                        "task_queue": task_queue,
                        "args": args,
                    }
                )
                return type("Handle", (), {"id": id})()

        async def workflow_run(*_args: object) -> None:
            return None

        workflow_module = ModuleType("system_1.discovery_temporal_workflow")
        workflow_module.DailyDiscoveryWorkflow = type(
            "DailyDiscoveryWorkflow", (), {"run": workflow_run}
        )
        fake_client = FakeTemporalClient()

        with patch.dict(
            sys.modules,
            {"system_1.discovery_temporal_workflow": workflow_module},
        ), patch("system_1.discovery_scheduler.scheduled_day_in_berlin", return_value=date(2026, 9, 17)):
            workflow_id = asyncio.run(
                start_manual_daily_run(
                    fake_client,
                    TrialPolicy.default(date(2026, 9, 17)),
                    "alandas-system1",
                )
            )

        self.assertEqual(len(fake_client.calls), 1)
        call = fake_client.calls[0]
        self.assertEqual(call["workflow"], workflow_run)
        self.assertEqual(call["pos_args"], ())
        self.assertEqual(call["args"], ["trial-v1", "2026-09-17", "2026-09-17"])
        self.assertEqual(call["id"], workflow_id)
        self.assertEqual(call["task_queue"], "alandas-system1")

    def test_daily_discovery_workflow_runs_with_restricted_proxy_datetime(self) -> None:
        from system_1.discovery_temporal_workflow import DailyDiscoveryWorkflow

        class FakeRestrictedProxyDatetime:
            def __init__(self, dt: datetime) -> None:
                self._dt = dt

            def __getattr__(self, name: str) -> object:
                return getattr(self._dt, name)

            def astimezone(self, tz: object = None) -> object:
                # Simulates Temporal sandbox TypeError: tzinfo argument must be None or of a tzinfo subclass, not type '_RestrictedProxy'
                raise TypeError("tzinfo argument must be None or of a tzinfo subclass, not type '_RestrictedProxy'")

        class FakeWorkflowRuntime:
            def __init__(self, now_dt: datetime) -> None:
                self._now = FakeRestrictedProxyDatetime(now_dt)

            def now(self) -> object:
                return self._now

            async def execute_activity(self, activity_fn: object, args: dict[str, object], **kwargs: object) -> dict[str, object]:
                if "daily_run_id" in args and "scheduled_for" in args:
                    return {"daily_run_id": args["daily_run_id"], "status": "created"}
                return {"status": "disabled"}

        wf = DailyDiscoveryWorkflow()
        now_dt = datetime(2026, 9, 17, 9, 0, tzinfo=timezone.utc)
        fake_runtime = FakeWorkflowRuntime(now_dt)

        with patch("system_1.discovery_temporal_workflow.workflow.now", side_effect=fake_runtime.now), \
             patch("system_1.discovery_temporal_workflow.workflow.execute_activity", side_effect=fake_runtime.execute_activity):
            result = asyncio.run(wf.run("trial-v1", "2026-09-17"))

        self.assertEqual(result["status"], "disabled")
        self.assertEqual(result["daily_run_id"], "discovery:trial-v1:2026-09-17")

    def test_worker_connect_logs_success_and_run_logs_start(self) -> None:
        from system_1.worker import connect_temporal_with_retry

        class FakeTemporalClient:
            @classmethod
            async def connect(cls, address: str, namespace: str = "default") -> "FakeTemporalClient":
                return cls()

        with patch("system_1.worker.Client.connect", side_effect=FakeTemporalClient.connect):
            with self.assertLogs("system_1.worker", level="INFO") as log_cm:
                client = asyncio.run(connect_temporal_with_retry("temporal:7233", "default", attempts=1))
                self.assertIsNotNone(client)
                self.assertTrue(
                    any("Successfully connected to Temporal" in message for message in log_cm.output)
                )

    def test_worker_health_formatting_and_host_port_parsing(self) -> None:
        self.assertEqual(parse_host_port("temporal:7233"), ("temporal", 7233))
        self.assertEqual(parse_host_port("localhost"), ("localhost", 7233))
        self.assertEqual(parse_host_port("myhost:notaport"), ("myhost", 7233))

        env = {
            "TEMPORAL_ADDRESS": "temporal:7233",
            "TEMPORAL_NAMESPACE": "default",
            "TEMPORAL_TASK_QUEUE": "alandas-system1",
            "SYSTEM1_DISCOVERY_ENABLED": "false",
            "APIFY_API_TOKEN": "secret-token-value",
        }
        report = format_worker_health(
            env,
            db_status=(True, "connected"),
            temporal_socket_status=(True, "connected"),
            temporal_client_status=(True, "connected"),
        )
        self.assertNotIn("secret-token-value", report)
        self.assertIn("Database connectivity: ok", report)
        self.assertIn("Temporal address: temporal:7233", report)
        self.assertIn("Temporal socket connectivity: ok", report)
        self.assertIn("Temporal client connectivity: ok", report)
        self.assertIn("Discovery enabled: no", report)
        self.assertIn("Apify configured: yes", report)
        self.assertIn("Outscraper configured: no", report)
        self.assertIn("Overall status: healthy", report)

        degraded_report = format_worker_health(
            env,
            db_status=(False, "connection refused"),
            temporal_socket_status=(True, "connected"),
            temporal_client_status=(False, "connection refused"),
        )
        self.assertIn("Database connectivity: failed", degraded_report)
        self.assertIn("Overall status: degraded", degraded_report)

    def test_reconcile_daily_discovery_run_apify_and_unsubmitted_categories(self) -> None:
        fake_db_rows = [
            ("apify:cafe", "act-run-123", Decimal("0.56"), None, "submitted", {}),
            ("apify:brunch", "", Decimal("0.28"), None, "pending_submission", {}),
            ("apify:specialty_coffee", "", Decimal("0.28"), None, "pending_submission", {}),
            ("apify:boutique_hotel", "", Decimal("0.28"), None, "pending_submission", {}),
        ]

        class FakeDbConn:
            def __init__(self) -> None:
                self.updated_rows: list[tuple[object, ...]] = []

            def execute(self, sql: str, params: tuple[object, ...] = ()) -> "FakeDbConn":
                if "UPDATE discovery_provider_runs" in sql:
                    self.updated_rows.append(params)
                return self

            def fetchall(self) -> list[tuple[object, ...]]:
                return fake_db_rows

            def __enter__(self) -> "FakeDbConn":
                return self

            def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                return False

        apify_response_payload = {
            "data": {
                "id": "act-run-123",
                "status": "SUCCEEDED",
                "usageTotalUsd": 0.42,
            }
        }
        transport = FakeTransport(apify_response_payload, status_code=200)

        with patch("system_1.discovery_reconcile.db.connect", return_value=FakeDbConn()):
            report = reconcile_daily_discovery_run(
                "discovery:trial-v1:2026-09-17",
                {"APIFY_API_TOKEN": "valid-apify-token"},
                transport,
            )

        self.assertEqual(report["daily_run_id"], "discovery:trial-v1:2026-09-17")
        self.assertEqual(report["status"], "reconciled")
        runs = {r["provider"]: r for r in report["provider_runs"]}

        # Submitted Apify run was queried and reconciled
        self.assertEqual(runs["apify:cafe"]["status"], "succeeded")
        self.assertEqual(runs["apify:cafe"]["external_id"], "act-run-123")
        self.assertEqual(runs["apify:cafe"]["actual_cost_usd"], "0.42")
        self.assertTrue(runs["apify:cafe"]["reconciled"])

        # The other 3 categories were reserved but never submitted
        for cat in ("apify:brunch", "apify:specialty_coffee", "apify:boutique_hotel"):
            self.assertEqual(runs[cat]["status"], "reserved_not_submitted")
            self.assertEqual(runs[cat]["external_id"], "")
            self.assertEqual(runs[cat]["actual_cost_usd"], "0.00")
            self.assertFalse(runs[cat]["reconciled"])
            self.assertIn("Reserved but never submitted", runs[cat]["note"])

        # Verify transport only made GET requests to actor-runs, never POST
        for req in transport.requests:
            self.assertEqual(req.method, "GET")
            self.assertIn("/actor-runs/act-run-123", req.url)

        # Verify report string formatting
        text_report = format_reconciliation_report(report)
        self.assertIn("Daily Run ID: discovery:trial-v1:2026-09-17", text_report)
        self.assertIn("Provider: apify:cafe", text_report)
        self.assertIn("Actual USD: 0.42", text_report)
        self.assertIn("Provider: apify:brunch", text_report)
        self.assertIn("Reserved but never submitted to provider", text_report)

    def test_apify_dataset_import_end_to_end_and_duplicate_safety(self) -> None:
        valid_place = {
            "placeId": "ChIJN1t_tDeuEmsRUsoyG83frY4",
            "url": "https://maps.google.com/?cid=12345",
            "title": "Cafe Test Berlin",
            "city": "Berlin",
            "categoryName": "Cafe",
            "countryCode": "DE",
            "website": "https://cafe-test.de",
            "phone": "+49 30 1234567",
        }
        invalid_place = {
            "placeId": "ChIJ_invalid",
            "title": "Incomplete Venue",
            # missing required fields city, countryCode, url
        }
        advertisement_place = {
            **valid_place,
            "placeId": "ChIJ_ad",
            "isAdvertisement": True,
        }

        # Stored state for DB mock
        inserted_leads = {}
        audit_events = []

        class FakeImportDbConn:
            def execute(self, sql: str, params: tuple[object, ...] = ()) -> "FakeImportDbConn":
                self._last_sql = sql
                self._last_params = params
                return self

            def fetchone(self) -> tuple[object, ...] | None:
                if "SELECT external_id, status FROM discovery_provider_runs" in self._last_sql:
                    daily_run_id, provider = self._last_params
                    if daily_run_id == "discovery:trial-v1:2026-09-18" and provider == "apify:cafe":
                        return ("ZdjGOvrXoAfUYIQZA", "succeeded")
                    return None
                if "SELECT workflow_id, status FROM leads" in self._last_sql:
                    wid = self._last_params[0]
                    if wid in inserted_leads:
                        return (wid, "new")
                    return None
                return None

            def fetchall(self) -> list[tuple[object, ...]]:
                return []

            def __enter__(self) -> "FakeImportDbConn":
                return self

            def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                return False

        def fake_upsert_lead(wid: str, lead: object, status: str) -> None:
            inserted_leads[wid] = lead

        def fake_insert_audit_event(
            workflow_id: str,
            event_key: str,
            event_name: str,
            status: str,
            details: dict,
        ) -> bool:
            audit_events.append({
                "workflow_id": workflow_id,
                "event_key": event_key,
                "event_name": event_name,
                "status": status,
                "details": details,
            })
            return True

        class MultiUrlFakeTransport:
            def __init__(self) -> None:
                self.requests = []

            def request(self, method: str, url: str, headers: dict[str, str], body: bytes | None, timeout_seconds: int) -> HttpResponse:
                self.requests.append(type("Req", (), {"method": method, "url": url, "headers": headers, "body": body})())
                if "/actor-runs/ZdjGOvrXoAfUYIQZA" in url:
                    return HttpResponse(200, {"data": {"id": "ZdjGOvrXoAfUYIQZA", "defaultDatasetId": "dataset-xyz-123"}})
                if "/datasets/dataset-xyz-123/items" in url:
                    return HttpResponse(200, [valid_place, invalid_place, advertisement_place])
                return HttpResponse(404, {"error": "Not Found"})

        transport = MultiUrlFakeTransport()

        with patch("system_1.import_apify_dataset.db.connect", return_value=FakeImportDbConn()), \
             patch("system_1.import_apify_dataset.db.upsert_lead", side_effect=fake_upsert_lead), \
             patch("system_1.import_apify_dataset.db.insert_audit_event", side_effect=fake_insert_audit_event), \
             patch("system_1.import_apify_dataset.db.find_internal_duplicates", return_value=[]):
            summary = execute_apify_import(
                "discovery:trial-v1:2026-09-18",
                "apify:cafe",
                {"APIFY_API_TOKEN": "secret-token-to-redact"},
                transport,
            )

        self.assertEqual(summary.fetched, 3)
        self.assertEqual(summary.mapped, 1)
        self.assertEqual(summary.inserted, 1)
        self.assertEqual(summary.invalid_skipped, 2)
        self.assertEqual(summary.duplicate_skipped, 0)
        self.assertEqual(summary.failed, 0)
        self.assertEqual(len(inserted_leads), 1)
        self.assertEqual(len(audit_events), 1)
        self.assertEqual(audit_events[0]["event_name"], "discovery_lead_imported")
        self.assertEqual(
            audit_events[0]["event_key"],
            audit_event_key(audit_events[0]["workflow_id"], "discovery_lead_imported"),
        )

        # Verify all transport calls were GET and token was used in Authorization header
        for req in transport.requests:
            self.assertEqual(req.method, "GET")
            self.assertEqual(req.headers.get("Authorization"), "Bearer secret-token-to-redact")

        # RERUN TEST: Run again with the lead now existing in inserted_leads -> duplicate safe
        transport_rerun = MultiUrlFakeTransport()
        with patch("system_1.import_apify_dataset.db.connect", return_value=FakeImportDbConn()), \
             patch("system_1.import_apify_dataset.db.upsert_lead", side_effect=fake_upsert_lead), \
             patch("system_1.import_apify_dataset.db.insert_audit_event", side_effect=fake_insert_audit_event), \
             patch("system_1.import_apify_dataset.db.find_internal_duplicates", return_value=[]):

            rerun_summary = execute_apify_import(
                "discovery:trial-v1:2026-09-18",
                "apify:cafe",
                {"APIFY_API_TOKEN": "secret-token-to-redact"},
                transport_rerun,
            )

        self.assertEqual(rerun_summary.fetched, 3)
        self.assertEqual(rerun_summary.inserted, 0)
        self.assertEqual(rerun_summary.duplicate_skipped, 1)
        self.assertEqual(rerun_summary.invalid_skipped, 2)
        self.assertEqual(len(audit_events), 2)
        duplicate_event = audit_events[1]
        self.assertEqual(duplicate_event["event_name"], "discovery_import_duplicate_skipped")
        self.assertEqual(
            duplicate_event["event_key"],
            audit_event_key(duplicate_event["workflow_id"], "discovery_import_duplicate_skipped"),
        )

        # Output formatting test and token redaction check
        formatted = format_import_summary(summary)
        self.assertNotIn("secret-token-to-redact", formatted)
        self.assertIn("Daily Run ID:      discovery:trial-v1:2026-09-18", formatted)
        self.assertIn("Provider:          apify:cafe", formatted)
        self.assertIn("Inserted Leads:    1", formatted)

    def test_import_skips_duplicate_place_id_and_rejects_dataset_over_max_limit(self) -> None:
        base_place = {
            "placeId": "ChIJ_dup_place",
            "url": "https://maps.google.com/?cid=111",
            "title": "Dup Cafe Berlin",
            "city": "Berlin",
            "categoryName": "Cafe",
            "countryCode": "DE",
            "website": "https://dup-cafe.de",
        }
        duplicate_place = {
            **base_place,
            "url": "https://maps.google.com/?cid=222",
            "title": "Dup Cafe Berlin Duplicate Row",
        }
        items = [base_place, duplicate_place]

        class SimpleDbConn:
            def execute(self, sql: str, params: tuple[object, ...] = ()) -> "SimpleDbConn":
                return self
            def fetchone(self) -> tuple[object, ...] | None:
                return None
            def fetchall(self) -> list[tuple[object, ...]]:
                return []
            def __enter__(self) -> "SimpleDbConn":
                return self
            def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                return False

        with patch("system_1.import_apify_dataset.db.connect", return_value=SimpleDbConn()), \
             patch("system_1.import_apify_dataset.db.upsert_lead") as mock_upsert, \
             patch("system_1.import_apify_dataset.db.insert_audit_event") as mock_audit, \
             patch("system_1.import_apify_dataset.db.find_internal_duplicates", return_value=[]):

            summary = import_apify_candidates(
                "discovery:trial-v1:2026-09-18",
                "apify:cafe",
                items,
                dataset_id="ds-dup",
                run_id="run-dup",
            )

        self.assertEqual(summary.fetched, 2)
        self.assertEqual(summary.mapped, 1)
        self.assertEqual(summary.inserted, 1)
        self.assertEqual(summary.duplicate_skipped, 1)
        self.assertEqual(summary.invalid_skipped, 0)
        self.assertEqual(mock_upsert.call_count, 1)

        # Datasets exceeding MAX_RESULTS_PER_RUN (50) must fail cleanly via map_apify_dataset
        oversized_items = [base_place] * 51
        with self.assertRaisesRegex(ValueError, "review limit"):
            import_apify_candidates(
                "discovery:trial-v1:2026-09-18",
                "apify:cafe",
                oversized_items,
                dataset_id="ds-oversized",
                run_id="run-oversized",
            )

    def test_import_fails_cleanly_on_missing_or_incomplete_provider_row(self) -> None:
        class EmptyProviderDbConn:
            def execute(self, sql: str, params: tuple[object, ...] = ()) -> "EmptyProviderDbConn":
                return self
            def fetchone(self) -> tuple[object, ...] | None:
                return None
            def __enter__(self) -> "EmptyProviderDbConn":
                return self
            def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                return False

        with patch("system_1.import_apify_dataset.db.connect", return_value=EmptyProviderDbConn()):
            with self.assertRaisesRegex(RuntimeError, "no provider run found"):
                get_provider_run_external_id("discovery:trial-v1:2026-09-18", "apify:unknown")

        class MissingExternalIdDbConn:
            def execute(self, sql: str, params: tuple[object, ...] = ()) -> "MissingExternalIdDbConn":
                return self
            def fetchone(self) -> tuple[object, ...] | None:
                return ("", "pending_submission")
            def __enter__(self) -> "MissingExternalIdDbConn":
                return self
            def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                return False

        with patch("system_1.import_apify_dataset.db.connect", return_value=MissingExternalIdDbConn()):
            with self.assertRaisesRegex(RuntimeError, "has no external_id"):
                get_provider_run_external_id("discovery:trial-v1:2026-09-18", "apify:cafe")

    def test_import_fails_cleanly_on_apify_api_error(self) -> None:
        transport = FakeTransport({"error": "Unauthorized"}, status_code=401)
        with self.assertRaisesRegex(RuntimeError, "Apify API returned HTTP 401"):
            fetch_apify_dataset_items("invalid-token", transport, "some-run-id")

    def test_qualify_obvious_cafe_with_website_and_phone(self) -> None:
        lead = {
            "workflow_id": "lead-1",
            "venue_name": "Kaffeehaus Mitte",
            "venue_type": "Cafe",
            "city": "Berlin",
            "website": "https://kaffeehaus-mitte.de",
            "website_domain": "kaffeehaus-mitte.de",
            "phone": "+49 30 12345678",
        }
        res = evaluate_lead_qualification(lead)
        self.assertEqual(res.status, "qualified")
        self.assertEqual(res.score, 82)
        self.assertIn("category_hospitality", res.reasons)
        self.assertIn("custom_domain_website", res.reasons)
        self.assertIn("phone_present", res.reasons)
        self.assertTrue(res.evidence["has_website"])
        self.assertTrue(res.evidence["has_phone"])
        self.assertFalse(res.evidence["is_hosted_or_social_domain"])

    def test_qualify_electrical_repair_shop_with_cafe_name_needs_review(self) -> None:
        lead = {
            "workflow_id": "lead-2",
            "venue_name": "Cafe Espresso Electro Reparatur",
            "venue_type": "Electrical repair shop",
            "city": "Berlin",
            "website": "https://electro-reparatur.de",
            "website_domain": "electro-reparatur.de",
            "phone": "+49 30 87654321",
        }
        res = evaluate_lead_qualification(lead)
        self.assertEqual(res.status, "needs_review")
        self.assertEqual(res.score, 55)
        self.assertTrue(any("conflicting_signal" in r for r in res.reasons))

    def test_qualify_wholesaler_rejected(self) -> None:
        lead = {
            "workflow_id": "lead-3",
            "venue_name": "Gastro Großhandel Süd",
            "venue_type": "Wholesaler",
            "city": "Munich",
            "website": "https://gastro-grosshandel.de",
            "phone": "+49 89 11223344",
        }
        res = evaluate_lead_qualification(lead)
        self.assertEqual(res.status, "rejected")
        self.assertEqual(res.score, 12)
        self.assertTrue(any("non_target_category" in r for r in res.reasons))

    def test_qualify_cafe_with_hosted_or_social_domain_needs_review(self) -> None:
        domains = [
            "https://mycafe.canva.site",
            "https://mycafe.sumup.link",
            "https://mycafe.metro.rest",
            "https://instagram.com/mycafe",
            "https://facebook.com/mycafe",
        ]
        for url in domains:
            lead = {
                "workflow_id": f"lead-social-{url}",
                "venue_name": "Sunshine Cafe",
                "venue_type": "Cafe",
                "city": "Hamburg",
                "website": url,
                "phone": "+49 40 998877",
            }
            res = evaluate_lead_qualification(lead)
            self.assertEqual(res.status, "needs_review", f"Failed for domain {url}")
            self.assertEqual(res.score, 65)
            self.assertTrue(any("hosted_or_social_domain" in r for r in res.reasons))
            self.assertTrue(res.evidence["is_hosted_or_social_domain"])

    def test_qualify_batch_idempotency_and_summary_output(self) -> None:
        leads_fixture = [
            {
                "workflow_id": "lead-101",
                "venue_name": "Artisan Coffee Roasters",
                "venue_type": "Coffee roastery",
                "city": "Frankfurt",
                "website": "https://artisan-coffee.de",
                "phone": "+49 69 12345",
            },
            {
                "workflow_id": "lead-102",
                "venue_name": "Auto & Cafe Repair",
                "venue_type": "Car repair",
                "city": "Frankfurt",
                "website": "https://autorepair.de",
                "phone": "+49 69 54321",
            },
            {
                "workflow_id": "lead-103",
                "venue_name": "Elektro Handel GmbH",
                "venue_type": "Wholesaler",
                "city": "Frankfurt",
                "website": "https://elektro-handel.de",
                "phone": "+49 69 99999",
            },
            {
                "workflow_id": "lead-104",
                "venue_name": "Little Bakery Cafe",
                "venue_type": "Bakery",
                "city": "Frankfurt",
                "website": "https://littlebakery.sumup.store",
                "phone": "",
            },
        ]

        updated_leads: dict[str, dict] = {}

        def fake_update(
            workflow_id: str,
            qualification_status: str,
            qualification_score: int,
            qualification_reasons: list,
            qualification_evidence: dict,
        ) -> None:
            updated_leads[workflow_id] = {
                "status": qualification_status,
                "score": qualification_score,
                "reasons": qualification_reasons,
                "evidence": qualification_evidence,
            }

        with patch("system_1.qualify_discovery_leads.db.ensure_schema"), \
             patch("system_1.qualify_discovery_leads.db.fetch_leads_by_status", return_value=leads_fixture), \
             patch("system_1.qualify_discovery_leads.db.update_lead_qualification", side_effect=fake_update):

            summary1 = qualify_leads_batch(status="new", limit=50)

        self.assertEqual(summary1.total_inspected, 4)
        self.assertEqual(summary1.qualified, 1)
        self.assertEqual(summary1.rejected, 1)
        self.assertEqual(summary1.needs_review, 2)
        self.assertEqual(summary1.failed, 0)
        self.assertEqual(len(updated_leads), 4)

        # Verify idempotency: running again on same records updates same keys in place
        with patch("system_1.qualify_discovery_leads.db.ensure_schema"), \
             patch("system_1.qualify_discovery_leads.db.fetch_leads_by_status", return_value=leads_fixture), \
             patch("system_1.qualify_discovery_leads.db.update_lead_qualification", side_effect=fake_update):

            summary2 = qualify_leads_batch(status="new", limit=50)

        self.assertEqual(summary2.total_inspected, 4)
        self.assertEqual(summary2.qualified, 1)
        self.assertEqual(summary2.rejected, 1)
        self.assertEqual(summary2.needs_review, 2)
        self.assertEqual(len(updated_leads), 4)

        # Verify summary formatting
        summary_text = format_qualification_summary(summary1)
        self.assertIn("Total Inspected: 4", summary_text)
        self.assertIn("Qualified:       1", summary_text)
        self.assertIn("Rejected:        1", summary_text)
        self.assertIn("Needs Review:    2", summary_text)
        self.assertIn("Failed:          0", summary_text)

    def test_plan_discovery_enrichment_steps_and_attributes(self) -> None:
        # 1. Qualified lead with custom website
        lead_custom = {
            "workflow_id": "lead-custom",
            "qualification_status": "qualified",
            "venue_name": "Specialty Coffee Berlin",
            "website": "https://specialty-coffee.de",
            "website_domain": "specialty-coffee.de",
            "phone": "+49 30 11111",
            "email": "",
        }
        steps_custom = plan_lead_enrichment_steps(lead_custom)
        step_names = [s.name for s in steps_custom]
        self.assertIn("website_review", step_names)
        self.assertIn("email_lookup", step_names)
        self.assertIn("phone_validation", step_names)
        self.assertIn("dolibarr_duplicate_check", step_names)
        self.assertIn("menu_or_product_signal_check", step_names)

        # email_lookup requires external call, may cost money, and requires human approval
        email_step = next(s for s in steps_custom if s.name == "email_lookup")
        self.assertTrue(email_step.requires_external_call)
        self.assertTrue(email_step.may_cost_money)
        self.assertTrue(email_step.requires_human_approval)

        # 2. Needs_review social-only lead (e.g. Canva / Instagram)
        lead_social = {
            "workflow_id": "lead-social",
            "qualification_status": "needs_review",
            "venue_name": "Social Cafe",
            "website": "https://socialcafe.canva.site",
            "website_domain": "socialcafe.canva.site",
            "phone": "",
            "email": "",
        }
        steps_social = plan_lead_enrichment_steps(lead_social)
        social_step_names = [s.name for s in steps_social]
        self.assertIn("instagram_review", social_step_names)
        self.assertNotIn("website_review", social_step_names)

        # 3. Missing website + phone
        lead_no_web = {
            "workflow_id": "lead-no-web",
            "qualification_status": "needs_review",
            "venue_name": "Phone Only Cafe",
            "website": "",
            "phone": "+49 30 22222",
            "email": "",
        }
        steps_no_web = plan_lead_enrichment_steps(lead_no_web)
        no_web_step_names = [s.name for s in steps_no_web]
        self.assertIn("phone_validation", no_web_step_names)
        self.assertIn("website_discovery", no_web_step_names)

    def test_plan_enrichment_batch_skips_rejected_and_is_idempotent(self) -> None:
        leads_fixture = [
            {
                "workflow_id": "lead-q1",
                "qualification_status": "qualified",
                "venue_name": "Cafe Alpha",
                "website": "https://cafe-alpha.de",
                "phone": "+49 30 11",
                "email": "",
            },
            {
                "workflow_id": "lead-r1",
                "qualification_status": "rejected",
                "venue_name": "Wholesale Beta",
                "website": "https://beta-wholesale.de",
                "phone": "+49 30 22",
                "email": "",
            },
            {
                "workflow_id": "lead-nr1",
                "qualification_status": "needs_review",
                "venue_name": "Instagram Cafe",
                "website": "https://instagram.com/instacafe",
                "phone": "+49 30 33",
                "email": "",
            },
        ]

        plans_store: dict[str, dict] = {}

        def fake_upsert(workflow_id: str, qualification_status: str, steps: list) -> bool:
            is_new = workflow_id not in plans_store
            plans_store[workflow_id] = {
                "qualification_status": qualification_status,
                "steps": steps,
            }
            return is_new

        with patch("system_1.plan_discovery_enrichment.db.ensure_schema"), \
             patch("system_1.plan_discovery_enrichment.db.fetch_leads_for_enrichment_planning", return_value=leads_fixture), \
             patch("system_1.plan_discovery_enrichment.db.upsert_enrichment_plan", side_effect=fake_upsert):

            summary1 = plan_enrichment_batch(statuses=("qualified", "needs_review"), limit=50)

        self.assertEqual(summary1.leads_inspected, 2)
        self.assertEqual(summary1.plans_created, 2)
        self.assertEqual(summary1.plans_updated, 0)
        self.assertEqual(summary1.rejected_skipped, 1)
        self.assertEqual(summary1.paid_steps_pending_approval, 1)  # lead-q1 email_lookup
        self.assertEqual(summary1.external_steps_pending_approval, 1)
        self.assertEqual(summary1.failed, 0)
        self.assertIn("lead-q1", plans_store)
        self.assertIn("lead-nr1", plans_store)
        self.assertNotIn("lead-r1", plans_store)

        # Rerun to test idempotency
        with patch("system_1.plan_discovery_enrichment.db.ensure_schema"), \
             patch("system_1.plan_discovery_enrichment.db.fetch_leads_for_enrichment_planning", return_value=leads_fixture), \
             patch("system_1.plan_discovery_enrichment.db.upsert_enrichment_plan", side_effect=fake_upsert):

            summary2 = plan_enrichment_batch(statuses=("qualified", "needs_review"), limit=50)

        self.assertEqual(summary2.leads_inspected, 2)
        self.assertEqual(summary2.plans_created, 0)
        self.assertEqual(summary2.plans_updated, 2)
        self.assertEqual(summary2.rejected_skipped, 1)

        summary_text = format_plan_summary(summary1)
        self.assertIn("Leads Inspected:                 2", summary_text)
        self.assertIn("Plans Created:                   2", summary_text)
        self.assertIn("Rejected Skipped:                1", summary_text)
        self.assertIn("Paid Steps Pending Approval:     1", summary_text)

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

    def test_http_transport_allows_provider_json_arrays(self) -> None:
        from system_1.provider_http import UrllibHttpTransport

        def fake_open(request: object, timeout: int) -> FakeUrlResponse:
            return FakeUrlResponse(200, b'[{"title":"Cafe One"}]')

        response = UrllibHttpTransport(open_request=fake_open).request(
            "GET",
            "https://api.example/datasets/dataset-123/items?clean=true",
            {"Authorization": "Bearer secret"},
            None,
            60,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body, [{"title": "Cafe One"}])

    def test_provider_submission_is_idempotent(self) -> None:
        store = InMemoryDiscoveryStore()

        first = store.record_submission(
            "discovery:trial-v1:2026-09-17", "apify", "run-a", Decimal("1.40")
        )
        second = store.record_submission(
            "discovery:trial-v1:2026-09-17", "apify", "run-a", Decimal("1.40")
        )

        self.assertEqual(first, second)

    def test_reserved_provider_submission_is_not_resubmitted_after_timeout(self) -> None:
        store = InMemoryDiscoveryStore()

        first = store.reserve_submission(
            "discovery:trial-v1:2026-09-17", "outscraper", Decimal("0.60")
        )
        second = store.reserve_submission(
            "discovery:trial-v1:2026-09-17", "outscraper", Decimal("0.60")
        )

        self.assertEqual(first, second)
        self.assertEqual(first.status, "pending_submission")

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
