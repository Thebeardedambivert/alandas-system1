"""Tests for pure Alandas System 1 lead logic."""

from __future__ import annotations

import asyncio
import json
import os
import unittest
from datetime import date, datetime, timezone
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

from system_1 import db
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
from system_1.show_enrichment_plans import (
    DisplaySummary,
    format_lead_plan,
    format_plans_summary,
    render_enrichment_plans_report,
    show_enrichment_plans,
)
from system_1.approve_enrichment_step import (
    StepApprovalSummary,
    approve_enrichment_step,
    format_step_approval_summary,
)
from system_1.dry_run_enrichment import (
    DryRunSummary,
    dry_run_enrichment,
    evaluate_step_decision,
    format_dry_run_summary,
    format_lead_dry_run,
    render_dry_run_report,
)
from system_1.record_manual_enrichment_evidence import (
    ManualEvidenceSummary,
    format_manual_evidence_summary,
    record_manual_enrichment_evidence,
)
from system_1.social_enrichment_provider import (
    ApifyEnrichmentAdapter,
    ApifyEnrichmentConfig,
    FirecrawlAdapter,
    FirecrawlConfig,
    PlannedEnrichmentAction,
    ProviderPlanningSummary,
    format_provider_planning_summary,
    plan_lead_provider_routing,
    plan_provider_enrichment,
    render_provider_planning_report,
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
        steps_by_name = {s.name: s for s in steps_custom}
        self.assertIn("website_review", steps_by_name)
        self.assertIn("email_lookup", steps_by_name)
        self.assertIn("phone_validation", steps_by_name)
        self.assertIn("system1_duplicate_check", steps_by_name)
        self.assertIn("menu_or_product_signal_check", steps_by_name)
        self.assertNotIn("dolibarr_duplicate_check", steps_by_name)

        # REV-02: system1_duplicate_check is strictly local and un-gated
        dup_step = steps_by_name["system1_duplicate_check"]
        self.assertFalse(dup_step.requires_external_call)
        self.assertFalse(dup_step.may_cost_money)
        self.assertFalse(dup_step.requires_human_approval)
        self.assertIn("System 1 database", dup_step.reason)

        # REV-01: website_review requires external call and human approval
        web_step = steps_by_name["website_review"]
        self.assertTrue(web_step.requires_external_call)
        self.assertFalse(web_step.may_cost_money)
        self.assertTrue(web_step.requires_human_approval)

        # REV-01: menu_or_product_signal_check requires external call and human approval
        menu_step = steps_by_name["menu_or_product_signal_check"]
        self.assertTrue(menu_step.requires_external_call)
        self.assertFalse(menu_step.may_cost_money)
        self.assertTrue(menu_step.requires_human_approval)

        # email_lookup requires external call, may cost money, and requires human approval
        email_step = steps_by_name["email_lookup"]
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
        social_by_name = {s.name: s for s in steps_social}
        self.assertIn("instagram_review", social_by_name)
        self.assertNotIn("website_review", social_by_name)

        # REV-01: instagram_review requires external call and human approval
        insta_step = social_by_name["instagram_review"]
        self.assertTrue(insta_step.requires_external_call)
        self.assertFalse(insta_step.may_cost_money)
        self.assertTrue(insta_step.requires_human_approval)

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
        no_web_by_name = {s.name: s for s in steps_no_web}
        self.assertIn("phone_validation", no_web_by_name)
        self.assertIn("website_discovery", no_web_by_name)

        # REV-01: website_discovery requires external call and human approval
        disc_step = no_web_by_name["website_discovery"]
        self.assertTrue(disc_step.requires_external_call)
        self.assertFalse(disc_step.may_cost_money)
        self.assertTrue(disc_step.requires_human_approval)

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
        # lead-q1: website_review, email_lookup, menu_or_product_signal_check (3)
        # lead-nr1: instagram_review, menu_or_product_signal_check (2)
        # total external steps pending approval = 5
        self.assertEqual(summary1.external_steps_pending_approval, 5)
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
        self.assertIn("External Steps Pending Approval: 5", summary_text)
        self.assertIn("Paid Steps Pending Approval:     1", summary_text)

    def test_show_enrichment_plans_formatting_and_summary(self) -> None:
        plans = [
            {
                "workflow_id": "lead-mitte-1",
                "venue_name": "Kaffeehaus Mitte",
                "city": "Berlin",
                "qualification_status": "qualified",
                "qualification_score": 82,
                "steps": [
                    {
                        "name": "system1_duplicate_check",
                        "requires_external_call": False,
                        "may_cost_money": False,
                        "requires_human_approval": False,
                        "reason": "Check System 1 database for existing lead or duplicate venue records",
                    },
                    {
                        "name": "website_review",
                        "requires_external_call": True,
                        "may_cost_money": False,
                        "requires_human_approval": True,
                        "reason": "Inspect homepage and impressum",
                    },
                    {
                        "name": "email_lookup",
                        "requires_external_call": True,
                        "may_cost_money": True,
                        "requires_human_approval": True,
                        "reason": "Find business contact email via paid waterfall",
                    },
                ],
            },
            {
                "workflow_id": "lead-neukolln-2",
                "venue_name": "Social Brunch Bar",
                "city": "Berlin",
                "qualification_status": "needs_review",
                "qualification_score": 55,
                "steps": [
                    {
                        "name": "system1_duplicate_check",
                        "requires_external_call": False,
                        "may_cost_money": False,
                        "requires_human_approval": False,
                        "reason": "Check System 1 database",
                    },
                    {
                        "name": "instagram_review",
                        "requires_external_call": True,
                        "may_cost_money": False,
                        "requires_human_approval": True,
                        "reason": "Review social profile",
                    },
                ],
            },
        ]

        report_text, summary = render_enrichment_plans_report(plans)

        # Summary assertions
        self.assertEqual(summary.leads_shown, 2)
        self.assertEqual(summary.total_steps, 5)
        self.assertEqual(summary.external_steps_pending_approval, 3)  # website_review, email_lookup, instagram_review
        self.assertEqual(summary.paid_steps_pending_approval, 1)      # email_lookup

        # Formatting assertions for lead details
        self.assertIn("=== Lead: lead-mitte-1 ===", report_text)
        self.assertIn("Venue:                Kaffeehaus Mitte (Berlin)", report_text)
        self.assertIn("Qualification Status: qualified (Score: 82)", report_text)
        self.assertIn("1. system1_duplicate_check", report_text)
        self.assertIn("External call required:  no", report_text)
        self.assertIn("May cost money:          no", report_text)
        self.assertIn("Human approval required: no", report_text)
        self.assertIn("2. website_review", report_text)
        self.assertIn("External call required:  yes", report_text)
        self.assertIn("3. email_lookup", report_text)
        self.assertIn("May cost money:          yes", report_text)
        self.assertIn("Human approval required: yes", report_text)

        # Formatting assertions for summary block
        self.assertIn("=== Enrichment Plans Summary ===", report_text)
        self.assertIn("Leads Shown:                     2", report_text)
        self.assertIn("Total Steps:                     5", report_text)
        self.assertIn("External Steps Pending Approval: 3", report_text)
        self.assertIn("Paid Steps Pending Approval:     1", report_text)

    def test_fetch_enrichment_plans_db_read_and_cli_execution(self) -> None:
        db_rows = [
            (
                "lead-mitte-1",
                "Kaffeehaus Mitte",
                "Berlin",
                "qualified",
                82,
                [
                    {
                        "name": "system1_duplicate_check",
                        "requires_external_call": False,
                        "may_cost_money": False,
                        "requires_human_approval": False,
                    }
                ],
            )
        ]

        class FakePlansDbConn:
            def __init__(self) -> None:
                self.queries = []

            def execute(self, sql: str, params: tuple = ()) -> "FakePlansDbConn":
                self.queries.append((sql, params))
                return self

            def fetchall(self) -> list:
                return db_rows

            def __enter__(self) -> "FakePlansDbConn":
                return self

            def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                return False

        with patch("system_1.db.connect", return_value=FakePlansDbConn()):
            plans = db.fetch_enrichment_plans(statuses=["qualified"], limit=10)

        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]["workflow_id"], "lead-mitte-1")
        self.assertEqual(plans[0]["venue_name"], "Kaffeehaus Mitte")
        self.assertEqual(plans[0]["city"], "Berlin")
        self.assertEqual(plans[0]["qualification_status"], "qualified")
        self.assertEqual(plans[0]["qualification_score"], 82)
        self.assertEqual(len(plans[0]["steps"]), 1)

        # Verify show_enrichment_plans calls db.fetch_enrichment_plans without external calls
        with patch("system_1.show_enrichment_plans.db.ensure_schema"), \
             patch("system_1.show_enrichment_plans.db.fetch_enrichment_plans", return_value=plans):
            summary = show_enrichment_plans(statuses=["qualified"], limit=10)

        self.assertEqual(summary.leads_shown, 1)
        self.assertEqual(summary.total_steps, 1)
        self.assertEqual(summary.external_steps_pending_approval, 0)
        self.assertEqual(summary.paid_steps_pending_approval, 0)

    def test_approve_enrichment_step_lifecycle_and_validation(self) -> None:
        mock_plan = {
            "workflow_id": "lead-mitte-1",
            "qualification_status": "qualified",
            "steps": [
                {
                    "name": "system1_duplicate_check",
                    "requires_external_call": False,
                    "may_cost_money": False,
                    "requires_human_approval": False,
                },
                {
                    "name": "website_review",
                    "requires_external_call": True,
                    "may_cost_money": False,
                    "requires_human_approval": True,
                },
                {
                    "name": "email_lookup",
                    "requires_external_call": True,
                    "may_cost_money": True,
                    "requires_human_approval": True,
                },
            ],
        }

        approvals_store: dict[tuple[str, str], dict] = {}

        def fake_fetch_plan(wid: str) -> dict | None:
            if wid == "lead-mitte-1":
                return mock_plan
            return None

        def fake_record_approval(
            workflow_id: str,
            step_name: str,
            approved_by: str,
            max_cost_usd: Decimal,
        ) -> tuple[dict, bool]:
            key = (workflow_id, step_name)
            if key in approvals_store:
                return approvals_store[key], False
            rec = {
                "workflow_id": workflow_id,
                "step_name": step_name,
                "approved_by": approved_by,
                "max_cost_usd": max_cost_usd,
            }
            approvals_store[key] = rec
            return rec, True

        with patch("system_1.approve_enrichment_step.db.ensure_schema"), \
             patch("system_1.approve_enrichment_step.db.fetch_enrichment_plan", side_effect=fake_fetch_plan), \
             patch("system_1.approve_enrichment_step.db.record_enrichment_step_approval", side_effect=fake_record_approval):

            # 1. Approving an existing free/local step works
            res1 = approve_enrichment_step("lead-mitte-1", "system1_duplicate_check", "Cyril")
            self.assertEqual(res1.workflow_id, "lead-mitte-1")
            self.assertEqual(res1.step_name, "system1_duplicate_check")
            self.assertEqual(res1.approved_by, "Cyril")
            self.assertEqual(res1.max_cost_usd, "0.00")
            self.assertEqual(res1.status, "created")

            # 2. Approving an existing external/free step works with max_cost_usd 0.00
            res2 = approve_enrichment_step("lead-mitte-1", "website_review", "Cyril", Decimal("0.00"))
            self.assertEqual(res2.step_name, "website_review")
            self.assertEqual(res2.max_cost_usd, "0.00")
            self.assertEqual(res2.status, "created")

            # 3. Approving a paid step requires max_cost_usd >= 0.00
            with self.assertRaisesRegex(ValueError, "paid step 'email_lookup' requires --max-cost-usd"):
                approve_enrichment_step("lead-mitte-1", "email_lookup", "Cyril", None)

            with self.assertRaisesRegex(ValueError, "paid step 'email_lookup' requires --max-cost-usd"):
                approve_enrichment_step("lead-mitte-1", "email_lookup", "Cyril", Decimal("-0.50"))

            res3 = approve_enrichment_step("lead-mitte-1", "email_lookup", "Cyril", Decimal("0.10"))
            self.assertEqual(res3.step_name, "email_lookup")
            self.assertEqual(res3.max_cost_usd, "0.10")
            self.assertEqual(res3.status, "created")

            # 4. Re-approving the same step is idempotent
            res3_rerun = approve_enrichment_step("lead-mitte-1", "email_lookup", "Cyril", Decimal("0.10"))
            self.assertEqual(res3_rerun.status, "already_exists")
            self.assertEqual(res3_rerun.max_cost_usd, "0.10")

            # 5. Unknown workflow_id fails
            with self.assertRaisesRegex(ValueError, "no enrichment plan found"):
                approve_enrichment_step("unknown-lead", "website_review", "Cyril")

            # 6. Unknown step_name fails
            with self.assertRaisesRegex(ValueError, "step 'unknown_step' not found"):
                approve_enrichment_step("lead-mitte-1", "unknown_step", "Cyril")

            # 7. Summary formatting check
            text = format_step_approval_summary(res3)
            self.assertIn("Workflow ID:  lead-mitte-1", text)
            self.assertIn("Step Name:    email_lookup", text)
            self.assertIn("Approved By:  Cyril", text)
            self.assertIn("Max Cost USD: 0.10", text)
            self.assertIn("Status:       created", text)

    def test_record_enrichment_step_approval_db_sql(self) -> None:
        db_store: dict[tuple[str, str], tuple] = {}

        class FakeApprovalDbConn:
            def __init__(self) -> None:
                self.queries = []

            def execute(self, sql: str, params: tuple = ()) -> "FakeApprovalDbConn":
                self.queries.append((sql, params))
                if "INSERT INTO lead_enrichment_step_approvals" in sql:
                    wid, step, approver, max_cost = params
                    db_store[(wid, step)] = (wid, step, approver, Decimal(str(max_cost)), "2026-09-19T05:00:00Z")
                return self

            def fetchone(self) -> tuple | None:
                last_sql, last_params = self.queries[-1]
                if "SELECT workflow_id, step_name" in last_sql:
                    wid, step = last_params
                    return db_store.get((wid, step))
                return None

            def __enter__(self) -> "FakeApprovalDbConn":
                return self

            def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                return False

        with patch("system_1.db.connect", return_value=FakeApprovalDbConn()):
            rec, is_new = db.record_enrichment_step_approval("lead-1", "website_review", "Cyril", Decimal("0.00"))
            self.assertTrue(is_new)
            self.assertEqual(rec["workflow_id"], "lead-1")
            self.assertEqual(rec["step_name"], "website_review")
            self.assertEqual(rec["approved_by"], "Cyril")
            self.assertEqual(rec["max_cost_usd"], Decimal("0.00"))

            # Second call retrieves existing
            rec2, is_new2 = db.record_enrichment_step_approval("lead-1", "website_review", "Cyril", Decimal("0.00"))
            self.assertFalse(is_new2)
            self.assertEqual(rec2["workflow_id"], "lead-1")

    def test_dry_run_enrichment_decisions(self) -> None:
        # 1. Approved website_review becomes operator_review_needed
        step_web = {
            "name": "website_review",
            "requires_external_call": True,
            "may_cost_money": False,
            "requires_human_approval": True,
        }
        approval_web = {"approved_by": "Cyril", "max_cost_usd": Decimal("0.00")}
        dec_web_app, _ = evaluate_step_decision(step_web, approval_web)
        self.assertEqual(dec_web_app, "operator_review_needed")

        # 2. Approved menu_or_product_signal_check becomes operator_review_needed
        step_menu = {
            "name": "menu_or_product_signal_check",
            "requires_external_call": True,
            "may_cost_money": False,
            "requires_human_approval": True,
        }
        approval_menu = {"approved_by": "Cyril", "max_cost_usd": Decimal("0.00")}
        dec_menu_app, _ = evaluate_step_decision(step_menu, approval_menu)
        self.assertEqual(dec_menu_app, "operator_review_needed")

        # 3. Unapproved website_review becomes blocked_missing_approval
        dec_web_unapp, _ = evaluate_step_decision(step_web, None)
        self.assertEqual(dec_web_unapp, "blocked_missing_approval")

        # 4. email_lookup becomes blocked_provider_not_connected
        step_email = {
            "name": "email_lookup",
            "requires_external_call": True,
            "may_cost_money": True,
            "requires_human_approval": True,
        }
        dec_email_no_app, _ = evaluate_step_decision(step_email, None)
        self.assertEqual(dec_email_no_app, "blocked_provider_not_connected")

        # 5. email_lookup remains blocked_provider_not_connected even if an approval exists
        approval_email = {"approved_by": "Cyril", "max_cost_usd": Decimal("0.10")}
        dec_email_app, _ = evaluate_step_decision(step_email, approval_email)
        self.assertEqual(dec_email_app, "blocked_provider_not_connected")

        # 6. system1_duplicate_check becomes skipped_local_only
        step_dup = {
            "name": "system1_duplicate_check",
            "requires_external_call": False,
            "may_cost_money": False,
            "requires_human_approval": False,
        }
        dec_dup, _ = evaluate_step_decision(step_dup, None)
        self.assertEqual(dec_dup, "skipped_local_only")

        # 7. phone_validation becomes skipped_local_only
        step_phone = {
            "name": "phone_validation",
            "requires_external_call": False,
            "may_cost_money": False,
            "requires_human_approval": False,
        }
        dec_phone, _ = evaluate_step_decision(step_phone, None)
        self.assertEqual(dec_phone, "skipped_local_only")

    def test_dry_run_enrichment_report_and_db_flow(self) -> None:
        plans = [
            {
                "workflow_id": "lead-101",
                "venue_name": "Matcha Bar Mitte",
                "city": "Berlin",
                "qualification_status": "qualified",
                "qualification_score": 85,
                "steps": [
                    {
                        "name": "system1_duplicate_check",
                        "requires_external_call": False,
                        "may_cost_money": False,
                        "requires_human_approval": False,
                    },
                    {
                        "name": "website_review",
                        "requires_external_call": True,
                        "may_cost_money": False,
                        "requires_human_approval": True,
                    },
                    {
                        "name": "email_lookup",
                        "requires_external_call": True,
                        "may_cost_money": True,
                        "requires_human_approval": True,
                    },
                ],
            },
            {
                "workflow_id": "lead-102",
                "venue_name": "Cafe Neukolln",
                "city": "Berlin",
                "qualification_status": "needs_review",
                "qualification_score": 60,
                "steps": [
                    {
                        "name": "phone_validation",
                        "requires_external_call": False,
                        "may_cost_money": False,
                        "requires_human_approval": False,
                    },
                    {
                        "name": "instagram_review",
                        "requires_external_call": True,
                        "may_cost_money": False,
                        "requires_human_approval": True,
                    },
                ],
            },
        ]

        # Approvals: lead-101 website_review approved, lead-101 email_lookup approved
        approvals = {
            ("lead-101", "website_review"): {"approved_by": "Cyril", "max_cost_usd": Decimal("0.00")},
            ("lead-101", "email_lookup"): {"approved_by": "Cyril", "max_cost_usd": Decimal("0.20")},
        }

        report_text, summary = render_dry_run_report(plans, approvals)

        self.assertEqual(summary.leads_inspected, 2)
        self.assertEqual(summary.total_steps, 5)
        self.assertEqual(summary.operator_review_needed, 1)  # lead-101 website_review
        self.assertEqual(summary.blocked_missing_approval, 1)  # lead-102 instagram_review
        self.assertEqual(summary.blocked_provider_not_connected, 1)  # lead-101 email_lookup
        self.assertEqual(summary.blocked_paid_step, 0)
        self.assertEqual(summary.skipped_local_only, 2)  # system1_duplicate_check, phone_validation

        # Output formatting assertions
        self.assertIn("=== Lead: lead-101 ===", report_text)
        self.assertIn("1. system1_duplicate_check: skipped_local_only", report_text)
        self.assertIn("2. website_review: operator_review_needed", report_text)
        self.assertIn("3. email_lookup: blocked_provider_not_connected", report_text)
        self.assertIn("=== Lead: lead-102 ===", report_text)
        self.assertIn("1. phone_validation: skipped_local_only", report_text)
        self.assertIn("2. instagram_review: blocked_missing_approval", report_text)

        self.assertIn("=== Dry-Run Enrichment Summary ===", report_text)
        self.assertIn("Leads Inspected:                 2", report_text)
        self.assertIn("Total Steps:                     5", report_text)
        self.assertIn("Operator Review Needed:          1", report_text)
        self.assertIn("Blocked Missing Approval:        1", report_text)
        self.assertIn("Blocked Provider Not Connected:  1", report_text)
        self.assertIn("Blocked Paid Step:               0", report_text)
        self.assertIn("Skipped Local Only:              2", report_text)

        # Verify command execution through DB mocks without external/network calls
        with patch("system_1.dry_run_enrichment.db.ensure_schema"), \
             patch("system_1.dry_run_enrichment.db.fetch_enrichment_plans", return_value=plans), \
             patch("system_1.dry_run_enrichment.db.fetch_enrichment_step_approvals", return_value=approvals):
            run_summary = dry_run_enrichment(statuses=["qualified", "needs_review"], limit=50)

        self.assertEqual(run_summary.leads_inspected, 2)
        self.assertEqual(run_summary.operator_review_needed, 1)

    def test_record_manual_enrichment_evidence_validation_and_lifecycle(self) -> None:
        mock_plan = {
            "workflow_id": "lead-mitte-1",
            "qualification_status": "qualified",
            "steps": [
                {
                    "name": "system1_duplicate_check",
                    "requires_external_call": False,
                    "may_cost_money": False,
                    "requires_human_approval": False,
                },
                {
                    "name": "website_review",
                    "requires_external_call": True,
                    "may_cost_money": False,
                    "requires_human_approval": True,
                },
                {
                    "name": "menu_or_product_signal_check",
                    "requires_external_call": True,
                    "may_cost_money": False,
                    "requires_human_approval": True,
                },
                {
                    "name": "email_lookup",
                    "requires_external_call": True,
                    "may_cost_money": True,
                    "requires_human_approval": True,
                },
            ],
        }

        # Approvals: website_review and menu_or_product_signal_check are approved
        approvals = {
            ("lead-mitte-1", "website_review"): {"approved_by": "Cyril", "max_cost_usd": Decimal("0.00")},
            ("lead-mitte-1", "menu_or_product_signal_check"): {"approved_by": "Cyril", "max_cost_usd": Decimal("0.00")},
            ("lead-mitte-1", "email_lookup"): {"approved_by": "Cyril", "max_cost_usd": Decimal("0.10")},
        }

        evidence_store: dict[tuple[str, str, str], dict] = {}

        def fake_fetch_plan(wid: str) -> dict | None:
            if wid == "lead-mitte-1":
                return mock_plan
            return None

        def fake_fetch_approvals(wids: list[str]) -> dict:
            return {k: v for k, v in approvals.items() if k[0] in wids}

        def fake_record_evidence(
            workflow_id: str,
            step_name: str,
            field: str,
            value: str,
            source_url: str,
            recorded_by: str,
        ) -> tuple[dict, str]:
            key = (workflow_id, step_name, field)
            if key in evidence_store:
                existing = evidence_store[key]
                if (
                    existing["value"] == value
                    and existing["source_url"] == source_url
                    and existing["recorded_by"] == recorded_by
                ):
                    return existing, "already_exists"
                existing["value"] = value
                existing["source_url"] = source_url
                existing["recorded_by"] = recorded_by
                return existing, "updated"
            rec = {
                "workflow_id": workflow_id,
                "step_name": step_name,
                "field": field,
                "value": value,
                "source_url": source_url,
                "recorded_by": recorded_by,
            }
            evidence_store[key] = rec
            return rec, "created"

        with patch("system_1.record_manual_enrichment_evidence.db.ensure_schema"), \
             patch("system_1.record_manual_enrichment_evidence.db.fetch_enrichment_plan", side_effect=fake_fetch_plan), \
             patch("system_1.record_manual_enrichment_evidence.db.fetch_enrichment_step_approvals", side_effect=fake_fetch_approvals), \
             patch("system_1.record_manual_enrichment_evidence.db.record_manual_enrichment_evidence", side_effect=fake_record_evidence):

            # 1. Approved website_review accepts evidence
            res1 = record_manual_enrichment_evidence(
                workflow_id="lead-mitte-1",
                step_name="website_review",
                field="decision_maker_name",
                value="Anna Becker",
                source_url="https://kaffee-mitte.de/impressum",
                recorded_by="Cyril",
            )
            self.assertEqual(res1.workflow_id, "lead-mitte-1")
            self.assertEqual(res1.step_name, "website_review")
            self.assertEqual(res1.field, "decision_maker_name")
            self.assertEqual(res1.value, "Anna Becker")
            self.assertEqual(res1.source_url, "https://kaffee-mitte.de/impressum")
            self.assertEqual(res1.recorded_by, "Cyril")
            self.assertEqual(res1.status, "created")

            # 2. Approved menu_or_product_signal_check accepts evidence
            res2 = record_manual_enrichment_evidence(
                workflow_id="lead-mitte-1",
                step_name="menu_or_product_signal_check",
                field="matcha_served",
                value="yes, ceremonial grade iced matcha latte on drink menu",
                source_url="https://kaffee-mitte.de/menu",
                recorded_by="Cyril",
            )
            self.assertEqual(res2.step_name, "menu_or_product_signal_check")
            self.assertEqual(res2.status, "created")

            # 3. Unapproved step is rejected
            del approvals[("lead-mitte-1", "website_review")]
            with self.assertRaisesRegex(ValueError, "step 'website_review' has not been approved"):
                record_manual_enrichment_evidence(
                    workflow_id="lead-mitte-1",
                    step_name="website_review",
                    field="instagram",
                    value="@kaffeemitte",
                    source_url="https://kaffee-mitte.de",
                    recorded_by="Cyril",
                )

            # 4. Unknown workflow is rejected
            with self.assertRaisesRegex(ValueError, "no enrichment plan found"):
                record_manual_enrichment_evidence(
                    workflow_id="unknown-lead",
                    step_name="website_review",
                    field="instagram",
                    value="@unknown",
                    source_url="https://unknown.de",
                    recorded_by="Cyril",
                )

            # 5. Unknown step is rejected
            with self.assertRaisesRegex(ValueError, "step 'unplanned_step' not found"):
                record_manual_enrichment_evidence(
                    workflow_id="lead-mitte-1",
                    step_name="unplanned_step",
                    field="instagram",
                    value="@test",
                    source_url="https://test.de",
                    recorded_by="Cyril",
                )

            # 6. email_lookup is rejected because provider is not connected
            with self.assertRaisesRegex(ValueError, "paid/provider-only step; provider is not connected"):
                record_manual_enrichment_evidence(
                    workflow_id="lead-mitte-1",
                    step_name="email_lookup",
                    field="contact_email",
                    value="owner@kaffee-mitte.de",
                    source_url="https://apollo.io",
                    recorded_by="Cyril",
                )

            # 7. Duplicate evidence does not create messy duplicates (is idempotent)
            res2_duplicate = record_manual_enrichment_evidence(
                workflow_id="lead-mitte-1",
                step_name="menu_or_product_signal_check",
                field="matcha_served",
                value="yes, ceremonial grade iced matcha latte on drink menu",
                source_url="https://kaffee-mitte.de/menu",
                recorded_by="Cyril",
            )
            self.assertEqual(res2_duplicate.status, "already_exists")

            # 7b. Existing evidence with changed value returns updated
            res2_val_updated = record_manual_enrichment_evidence(
                workflow_id="lead-mitte-1",
                step_name="menu_or_product_signal_check",
                field="matcha_served",
                value="yes, ceremonial grade iced matcha latte from Kyoto",
                source_url="https://kaffee-mitte.de/menu",
                recorded_by="Cyril",
            )
            self.assertEqual(res2_val_updated.status, "updated")
            self.assertEqual(res2_val_updated.value, "yes, ceremonial grade iced matcha latte from Kyoto")

            # 7c. Existing evidence with changed source_url returns updated
            res2_url_updated = record_manual_enrichment_evidence(
                workflow_id="lead-mitte-1",
                step_name="menu_or_product_signal_check",
                field="matcha_served",
                value="yes, ceremonial grade iced matcha latte from Kyoto",
                source_url="https://kaffee-mitte.de/drinks-menu-2026",
                recorded_by="Cyril",
            )
            self.assertEqual(res2_url_updated.status, "updated")
            self.assertEqual(res2_url_updated.source_url, "https://kaffee-mitte.de/drinks-menu-2026")

            # 7d. Existing evidence with changed recorded_by returns updated
            res2_rec_updated = record_manual_enrichment_evidence(
                workflow_id="lead-mitte-1",
                step_name="menu_or_product_signal_check",
                field="matcha_served",
                value="yes, ceremonial grade iced matcha latte from Kyoto",
                source_url="https://kaffee-mitte.de/drinks-menu-2026",
                recorded_by="Operator2",
            )
            self.assertEqual(res2_rec_updated.status, "updated")
            self.assertEqual(res2_rec_updated.recorded_by, "Operator2")

            # 7e. Re-submitting identical values returns already_exists again
            res2_same_again = record_manual_enrichment_evidence(
                workflow_id="lead-mitte-1",
                step_name="menu_or_product_signal_check",
                field="matcha_served",
                value="yes, ceremonial grade iced matcha latte from Kyoto",
                source_url="https://kaffee-mitte.de/drinks-menu-2026",
                recorded_by="Operator2",
            )
            self.assertEqual(res2_same_again.status, "already_exists")

            # 7f. Verify store maintains exactly one record per workflow_id + step_name + field
            target_keys = [k for k in evidence_store if k == ("lead-mitte-1", "menu_or_product_signal_check", "matcha_served")]
            self.assertEqual(len(target_keys), 1)

            # 8. Summary formatting check
            summary_text = format_manual_evidence_summary(res1)
            self.assertIn("=== Manual Enrichment Evidence Summary ===", summary_text)
            self.assertIn("Workflow ID:  lead-mitte-1", summary_text)
            self.assertIn("Step Name:    website_review", summary_text)
            self.assertIn("Field:        decision_maker_name", summary_text)
            self.assertIn("Value:        Anna Becker", summary_text)
            self.assertIn("Source URL:   https://kaffee-mitte.de/impressum", summary_text)
            self.assertIn("Recorded By:  Cyril", summary_text)
            self.assertIn("Status:       created", summary_text)

    def test_record_manual_enrichment_evidence_db_sql(self) -> None:
        db_store: dict[tuple[str, str, str], tuple] = {}

        class FakeEvidenceDbConn:
            def __init__(self) -> None:
                self.queries = []

            def execute(self, sql: str, params: tuple = ()) -> "FakeEvidenceDbConn":
                self.queries.append((sql, params))
                if "INSERT INTO lead_manual_enrichment_evidence" in sql:
                    wid, step, fld, val, src, rec_by = params
                    db_store[(wid, step, fld)] = (wid, step, fld, val, src, rec_by, "2026-09-19T06:00:00Z")
                elif "UPDATE lead_manual_enrichment_evidence" in sql:
                    val, src, rec_by, wid, step, fld = params
                    db_store[(wid, step, fld)] = (wid, step, fld, val, src, rec_by, "2026-09-19T06:01:00Z")
                return self

            def fetchone(self) -> tuple | None:
                last_sql, last_params = self.queries[-1]
                if "SELECT workflow_id, step_name, field" in last_sql:
                    wid, step, fld = last_params
                    return db_store.get((wid, step, fld))
                return None

            def __enter__(self) -> "FakeEvidenceDbConn":
                return self

            def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
                return False

        with patch("system_1.db.connect", return_value=FakeEvidenceDbConn()):
            # 1. New insertion returns created
            rec, status1 = db.record_manual_enrichment_evidence(
                workflow_id="lead-1",
                step_name="website_review",
                field="owner_name",
                value="John Doe",
                source_url="https://example.com",
                recorded_by="Cyril",
            )
            self.assertEqual(status1, "created")
            self.assertEqual(rec["workflow_id"], "lead-1")
            self.assertEqual(rec["field"], "owner_name")
            self.assertEqual(rec["value"], "John Doe")

            # 2. Duplicate call with identical values returns already_exists
            rec2, status2 = db.record_manual_enrichment_evidence(
                workflow_id="lead-1",
                step_name="website_review",
                field="owner_name",
                value="John Doe",
                source_url="https://example.com",
                recorded_by="Cyril",
            )
            self.assertEqual(status2, "already_exists")
            self.assertEqual(rec2["workflow_id"], "lead-1")

            # 3. Update call with changed value returns updated
            rec3, status3 = db.record_manual_enrichment_evidence(
                workflow_id="lead-1",
                step_name="website_review",
                field="owner_name",
                value="Jane Doe",
                source_url="https://example.com",
                recorded_by="Cyril",
            )
            self.assertEqual(status3, "updated")
            self.assertEqual(rec3["value"], "Jane Doe")

            # 4. Update call with changed source_url returns updated
            rec4, status4 = db.record_manual_enrichment_evidence(
                workflow_id="lead-1",
                step_name="website_review",
                field="owner_name",
                value="Jane Doe",
                source_url="https://example.com/team",
                recorded_by="Cyril",
            )
            self.assertEqual(status4, "updated")
            self.assertEqual(rec4["source_url"], "https://example.com/team")

            # 5. Update call with changed recorded_by returns updated
            rec5, status5 = db.record_manual_enrichment_evidence(
                workflow_id="lead-1",
                step_name="website_review",
                field="owner_name",
                value="Jane Doe",
                source_url="https://example.com/team",
                recorded_by="Operator2",
            )
            self.assertEqual(status5, "updated")
            self.assertEqual(rec5["recorded_by"], "Operator2")

            # 6. Verify single record per workflow_id + step_name + field in DB store
            self.assertEqual(len(db_store), 1)
            self.assertIn(("lead-1", "website_review", "owner_name"), db_store)

    def test_social_enrichment_provider_configs_and_actor_registry(self) -> None:
        # 1. Defaults are disabled
        with patch.dict(os.environ, {}, clear=True):
            fc = FirecrawlConfig.from_env()
            self.assertFalse(fc.enabled)
            self.assertEqual(fc.api_key, "")
            self.assertEqual(fc.max_credits_per_run, 50)
            self.assertEqual(fc.max_pages_per_lead, 5)

            ap = ApifyEnrichmentConfig.from_env()
            self.assertFalse(ap.enabled)
            self.assertEqual(ap.api_token, "")
            self.assertEqual(ap.max_cost_usd, Decimal("1.00"))
            self.assertEqual(ap.max_results_per_actor, 10)
            self.assertEqual(ap.instagram_profile_actors, ())
            self.assertEqual(ap.facebook_page_actors, ())
            self.assertEqual(ap.people_fallback_actors, ())

        # 2. Actor registry parsing and grouping
        custom_env = {
            "SYSTEM1_FIRECRAWL_ENABLED": "true",
            "FIRECRAWL_API_KEY": "fc-test-key",
            "SYSTEM1_FIRECRAWL_MAX_CREDITS_PER_RUN": "100",
            "SYSTEM1_FIRECRAWL_MAX_PAGES_PER_LEAD": "10",
            "SYSTEM1_APIFY_ENRICHMENT_ENABLED": "1",
            "APIFY_API_TOKEN": "apify-test-token",
            "SYSTEM1_APIFY_ENRICHMENT_MAX_COST_USD": "2.50",
            "SYSTEM1_APIFY_ENRICHMENT_MAX_RESULTS_PER_ACTOR": "20",
            "SYSTEM1_APIFY_INSTAGRAM_PROFILE_ACTORS": "apify/instagram-profile-scraper, user/insta-tool",
            "SYSTEM1_APIFY_FACEBOOK_PAGE_ACTORS": "apify/facebook-pages-scraper",
            "SYSTEM1_APIFY_PEOPLE_FALLBACK_ACTORS": "actor/people-finder, actor/phone-finder",
        }
        with patch.dict(os.environ, custom_env, clear=True):
            fc2 = FirecrawlConfig.from_env()
            self.assertTrue(fc2.enabled)
            self.assertEqual(fc2.api_key, "fc-test-key")
            self.assertEqual(fc2.max_credits_per_run, 100)
            self.assertEqual(fc2.max_pages_per_lead, 10)

            ap2 = ApifyEnrichmentConfig.from_env()
            self.assertTrue(ap2.enabled)
            self.assertEqual(ap2.api_token, "apify-test-token")
            self.assertEqual(ap2.max_cost_usd, Decimal("2.50"))
            self.assertEqual(ap2.max_results_per_actor, 20)
            self.assertEqual(
                ap2.instagram_profile_actors,
                ("apify/instagram-profile-scraper", "user/insta-tool"),
            )
            self.assertEqual(ap2.facebook_page_actors, ("apify/facebook-pages-scraper",))
            self.assertEqual(
                ap2.people_fallback_actors,
                ("actor/people-finder", "actor/phone-finder"),
            )

    def test_social_enrichment_adapters_fail_closed_and_enforce_caps(self) -> None:
        transport = FakeTransport({"success": True})

        # 1. Disabled Firecrawl makes zero network calls and raises
        disabled_fc = FirecrawlConfig(api_key="key", enabled=False)
        fc_adapter = FirecrawlAdapter(disabled_fc, transport=transport)
        with self.assertRaisesRegex(RuntimeError, "Firecrawl enrichment is disabled"):
            fc_adapter.scrape_url("https://example.com")
        self.assertEqual(len(transport.requests), 0)

        # 2. Enabled Firecrawl missing key fails closed
        missing_key_fc = FirecrawlConfig(api_key="", enabled=True)
        fc_adapter_no_key = FirecrawlAdapter(missing_key_fc, transport=transport)
        with self.assertRaisesRegex(ValueError, "FIRECRAWL_API_KEY is missing"):
            fc_adapter_no_key.scrape_url("https://example.com")
        self.assertEqual(len(transport.requests), 0)

        # 3. Firecrawl caps enforced before network call
        enabled_fc = FirecrawlConfig(api_key="key", enabled=True, max_pages_per_lead=3)
        fc_adapter_valid = FirecrawlAdapter(enabled_fc, transport=transport)
        with self.assertRaisesRegex(ValueError, "exceeds configured max pages"):
            fc_adapter_valid.scrape_url("https://example.com", pages_limit=5)
        self.assertEqual(len(transport.requests), 0)

        # Valid call executes with auth header
        res_fc = fc_adapter_valid.scrape_url("https://example.com", pages_limit=2)
        self.assertEqual(res_fc.status_code, 201)
        self.assertEqual(len(transport.requests), 1)

        # 4. Disabled Apify makes zero network calls and raises
        disabled_ap = ApifyEnrichmentConfig(api_token="token", enabled=False)
        ap_adapter = ApifyEnrichmentAdapter(disabled_ap, transport=transport)
        with self.assertRaisesRegex(RuntimeError, "Apify enrichment is disabled"):
            ap_adapter.run_actor("actor-1", "instagram", {}, Decimal("0.50"))
        self.assertEqual(len(transport.requests), 1)  # unchanged from previous call

        # 5. Enabled Apify missing key fails closed
        no_key_ap = ApifyEnrichmentConfig(api_token="", enabled=True)
        ap_adapter_no_key = ApifyEnrichmentAdapter(no_key_ap, transport=transport)
        with self.assertRaisesRegex(ValueError, "APIFY_API_TOKEN is missing"):
            ap_adapter_no_key.run_actor("actor-1", "instagram", {}, Decimal("0.50"))
        self.assertEqual(len(transport.requests), 1)

        # 6. Apify cost cap enforced before network call
        enabled_ap = ApifyEnrichmentConfig(api_token="token", enabled=True, max_cost_usd=Decimal("0.80"))
        ap_adapter_valid = ApifyEnrichmentAdapter(enabled_ap, transport=transport)
        with self.assertRaisesRegex(ValueError, "exceeds configured max cost"):
            ap_adapter_valid.run_actor("actor-1", "instagram", {}, Decimal("1.20"))
        self.assertEqual(len(transport.requests), 1)

        # 7. People fallback actors blocked by default unless explicitly approved
        with self.assertRaisesRegex(ValueError, "People fallback actors are blocked by default"):
            ap_adapter_valid.run_actor("actor-people", "people_fallback", {}, Decimal("0.50"))
        self.assertEqual(len(transport.requests), 1)

        # Approved people fallback executes
        res_ap = ap_adapter_valid.run_actor("actor-people", "people_fallback", {}, Decimal("0.50"), approved_by="Cyril")
        self.assertEqual(res_ap.status_code, 201)
        self.assertEqual(len(transport.requests), 2)

    def test_provider_enrichment_dry_run_routing_logic(self) -> None:
        fc_cfg = FirecrawlConfig(api_key="", enabled=False)
        ap_cfg = ApifyEnrichmentConfig(
            api_token="",
            enabled=False,
            instagram_profile_actors=("apify/instagram-profile-scraper",),
            facebook_page_actors=("apify/facebook-pages-scraper",),
            people_fallback_actors=("apify/people-finder",),
        )

        # Lead 1: Custom website -> Firecrawl step
        lead_web = {
            "workflow_id": "lead-web-1",
            "venue_name": "Specialty Coffee",
            "city": "Berlin",
            "website": "https://specialtycoffee.de",
            "instagram": "",
            "source_url": "https://maps.google.com/?cid=1",
        }
        routes_web = plan_lead_provider_routing(lead_web, fc_cfg, ap_cfg)
        fc_routes = [r for r in routes_web if r.provider == "firecrawl"]
        self.assertEqual(len(fc_routes), 1)
        self.assertEqual(fc_routes[0].target_type, "website_pages")
        self.assertEqual(fc_routes[0].target_value, "https://specialtycoffee.de")

        # Lead 2: Instagram URL -> Instagram actor group
        lead_insta = {
            "workflow_id": "lead-insta-2",
            "venue_name": "Insta Brunch",
            "city": "Berlin",
            "website": "",
            "instagram": "https://instagram.com/instabrunch",
            "source_url": "https://maps.google.com/?cid=2",
        }
        routes_insta = plan_lead_provider_routing(lead_insta, fc_cfg, ap_cfg)
        ig_routes = [r for r in routes_insta if r.provider == "apify_instagram"]
        self.assertEqual(len(ig_routes), 1)
        self.assertEqual(ig_routes[0].actor_id, "apify/instagram-profile-scraper")
        self.assertEqual(ig_routes[0].target_value, "https://instagram.com/instabrunch")

        # Lead 3: Facebook URL -> Facebook actor group
        lead_fb = {
            "workflow_id": "lead-fb-3",
            "venue_name": "Facebook Cafe",
            "city": "Berlin",
            "website": "https://facebook.com/fbcafeberlin",
            "instagram": "",
            "source_url": "https://maps.google.com/?cid=3",
        }
        routes_fb = plan_lead_provider_routing(lead_fb, fc_cfg, ap_cfg)
        fb_routes = [r for r in routes_fb if r.provider == "apify_facebook"]
        self.assertEqual(len(fb_routes), 1)
        self.assertEqual(fb_routes[0].actor_id, "apify/facebook-pages-scraper")
        self.assertEqual(fb_routes[0].target_value, "https://facebook.com/fbcafeberlin")

        # Lead 4: No custom website, no social URL -> needs_operator_review
        lead_none = {
            "workflow_id": "lead-none-4",
            "venue_name": "Offline Corner",
            "city": "Berlin",
            "website": "",
            "instagram": "",
            "source_url": "https://maps.google.com/?cid=4",
        }
        routes_none = plan_lead_provider_routing(lead_none, fc_cfg, ap_cfg)
        review_routes = [r for r in routes_none if r.status == "needs_operator_review"]
        self.assertEqual(len(review_routes), 1)
        self.assertIn("requires operator review", review_routes[0].reason)

        # People fallback is always tagged blocked_by_default
        fallback_routes = [r for r in routes_web if r.provider == "apify_people_fallback"]
        self.assertEqual(len(fallback_routes), 1)
        self.assertEqual(fallback_routes[0].status, "blocked_by_default")

        # End-to-end dry-run report rendering
        report_text, summary = render_provider_planning_report([lead_web, lead_insta, lead_fb, lead_none], fc_cfg, ap_cfg)
        self.assertEqual(summary.leads_inspected, 4)
        self.assertEqual(summary.firecrawl_routes, 1)
        self.assertEqual(summary.instagram_routes, 1)
        self.assertEqual(summary.facebook_routes, 1)
        self.assertEqual(summary.people_fallback_blocked, 4)
        self.assertEqual(summary.needs_operator_review, 1)

        self.assertIn("=== Provider Enrichment Planning Summary ===", report_text)
        self.assertIn("Firecrawl Website Routes:  1", report_text)
        self.assertIn("Instagram Actor Routes:    1", report_text)
        self.assertIn("Facebook Actor Routes:     1", report_text)
        self.assertIn("People Fallback Blocked:   4", report_text)
        self.assertIn("Needs Operator Review:     1", report_text)

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
