# Automated Discovery Trial Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run a seven-day Germany-wide discovery trial: up to 50 raw leads daily from Apify and 50 from Outscraper, without daily clicks, duplicate workflows, uncontrolled spend, or unreviewed outreach.

**Architecture:** A Temporal schedule starts one durable run per Europe/Berlin day. Apify receives four category allocations totalling 50; Outscraper receives one 50-café request. Separate provider adapters submit, reconcile, and map raw Maps data through the existing stable lead workflow IDs. Postgres owns run, retry, cost, and operator status.

**Tech Stack:** Python 3.14, Temporal Python SDK 1.16, psycopg 3.2/Postgres, stdlib `urllib`, Docker Compose/Coolify, unittest.

**Spec:** `docs/superpowers/specs/2026-09-17-automated-discovery-trial-design.md`

## Global Constraints

- Trial lasts exactly seven calendar days and pauses on day eight.
- Market is Germany. Provider rows must retain `country_code=DE` / `countryCode=DE`.
- Apify allocations: 20 cafes, 10 brunch venues, 10 specialty coffee venues, 10 boutique hotels. Outscraper: 50 cafes.
- Daily maximum: 50 rows per provider, 100 combined; whole trial maximum: 700 rows.
- Paid enrichments, reviews, email validation, and phone lookup are disabled for the trial. This is policy, not permanent code removal.
- No provider can send a message, write Dolibarr, call Hermes, or bypass Sidy approval.
- No submission happens over its configured estimate. Tokens and full provider payloads are not logged.
- Retry waits are 30 seconds, 2 minutes, and 10 minutes. Authentication, validation, and unknown-charge outcomes do not submit a replacement job.

---

### Task 1: Add the Germany-wide, category-aware trial policy

**Files:**
- Create: `alandas/system_1/discovery_policy.py`
- Modify: `alandas/system_1/apify_google_maps.py`
- Modify: `alandas/system_1/outscraper_google_maps.py`
- Modify: `alandas/tests/test_system1_core.py`
- Modify: `alandas/system_1/APIFY_DISCOVERY_CONTRACT.md`
- Modify: `alandas/system_1/OUTSCRAPER_WEBHOOK_CONTRACT.md`

**Interfaces:**
- `TrialPolicy.default(starts_on: date) -> TrialPolicy`
- `TrialPolicy.for_date(day: date) -> bool`
- `TrialPolicy.daily_run_id(day: date) -> str`
- `validate_discovery_request(search_scope: str, search_terms: Sequence[str], limit: int) -> list[str]`

- [ ] **Step 1: Write failing policy tests**

```python
def test_trial_policy_has_approved_allocations(self) -> None:
    policy = TrialPolicy.default(date(2026, 9, 17))
    self.assertEqual(policy.apify_allocations, {
        "cafe": 20, "brunch venue": 10,
        "specialty coffee venue": 10, "boutique hotel": 10,
    })
    self.assertEqual(policy.outscraper_limit, 50)
    self.assertTrue(policy.for_date(date(2026, 9, 23)))
    self.assertFalse(policy.for_date(date(2026, 9, 24)))

def test_germany_scope_replaces_city_allow_list(self) -> None:
    self.assertEqual(validate_discovery_request("Germany", ["cafe"], 50), [])
    self.assertIn("search scope is required",
                  validate_discovery_request(" ", ["cafe"], 50))
```

- [ ] **Step 2: Verify RED**

Run: `python -m unittest alandas.tests.test_system1_core.System1CoreTests.test_trial_policy_has_approved_allocations alandas.tests.test_system1_core.System1CoreTests.test_germany_scope_replaces_city_allow_list`

Expected: FAIL because the policy and Germany-wide validation do not exist.

- [ ] **Step 3: Implement the smallest policy boundary**

```python
@dataclass(frozen=True)
class TrialPolicy:
    policy_version: str
    starts_on: date
    duration_days: int = 7
    timezone: str = "Europe/Berlin"
    apify_allocations: Mapping[str, int] = field(default_factory=lambda: {
        "cafe": 20, "brunch venue": 10,
        "specialty coffee venue": 10, "boutique hotel": 10,
    })
    outscraper_limit: int = 50
    daily_total_limit: int = 100
    paid_enrichment_enabled: bool = False

    def for_date(self, day: date) -> bool:
        return self.starts_on <= day < self.starts_on + timedelta(days=self.duration_days)
```

Remove only the Berlin/Hamburg/Munich rule. Keep both DE country guards and 50-row source caps. Update contracts with the exact temporary trial policy.

- [ ] **Step 4: Verify GREEN**

Run: `python -m unittest alandas.tests.test_system1_core`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add alandas/system_1/discovery_policy.py alandas/system_1/apify_google_maps.py alandas/system_1/outscraper_google_maps.py alandas/system_1/APIFY_DISCOVERY_CONTRACT.md alandas/system_1/OUTSCRAPER_WEBHOOK_CONTRACT.md alandas/tests/test_system1_core.py
git commit -m "feat(discovery): add Germany-wide trial policy"
```

### Task 2: Persist daily/provider runs and retry decisions

**Files:**
- Create: `alandas/system_1/discovery_runs.py`
- Modify: `alandas/system_1/models.py`
- Modify: `alandas/system_1/db.py`
- Modify: `alandas/tests/test_system1_core.py`

**Interfaces:**
- Statuses: `pending`, `submitted`, `running`, `succeeded`, `degraded`, `needs_attention`, `blocked`.
- `create_or_get_daily_run(policy: TrialPolicy, day: date) -> DiscoveryRun`
- `record_provider_submission(daily_run_id: str, provider: str, external_id: str, estimate_usd: Decimal) -> ProviderRun`
- `record_provider_outcome(..., status: str, actual_cost_usd: Decimal | None, details: Mapping[str, object]) -> ProviderRun`
- `retry_decision(status_code: int | None, outcome_known: bool, attempt_number: int) -> RetryDecision`

- [ ] **Step 1: Write failing idempotency and unknown-outcome tests**

```python
def test_provider_submission_is_idempotent(self) -> None:
    store = InMemoryDiscoveryStore()
    first = store.record_submission("discovery:v1:2026-09-17", "apify", "run-a", Decimal("1.40"))
    second = store.record_submission("discovery:v1:2026-09-17", "apify", "run-a", Decimal("1.40"))
    self.assertEqual(first, second)

def test_unknown_charge_outcome_requires_reconciliation(self) -> None:
    decision = retry_decision(status_code=None, outcome_known=False, attempt_number=1)
    self.assertEqual(decision.action, "reconcile")
```

- [ ] **Step 2: Verify RED**

Run: `python -m unittest alandas.tests.test_system1_core.System1CoreTests.test_provider_submission_is_idempotent alandas.tests.test_system1_core.System1CoreTests.test_unknown_charge_outcome_requires_reconciliation`

Expected: FAIL because the repository and decision rule do not exist.

- [ ] **Step 3: Add schema and repositories**

In `ensure_schema()`, add:
- `discovery_runs` primary-keyed by `daily_run_id`;
- `discovery_provider_runs` uniquely keyed by `(daily_run_id, provider)`;
- `discovery_attempts` uniquely keyed by `(daily_run_id, provider, attempt_number)`.

Use `INSERT ... ON CONFLICT ... RETURNING`. Persist only IDs, counters, safe error class, costs, and small JSON summaries. Never persist credentials or full response bodies.

```python
def retry_decision(*, status_code: int | None, outcome_known: bool, attempt_number: int) -> RetryDecision:
    if not outcome_known:
        return RetryDecision("reconcile", None)
    if status_code in {429, 500, 502, 503, 504} and attempt_number < 3:
        return RetryDecision("retry", (30, 120, 600)[attempt_number])
    return RetryDecision("needs_attention", None)
```

- [ ] **Step 4: Verify GREEN**

Run: `python -m unittest alandas.tests.test_system1_core`

Expected: PASS. Then run `ensure_schema()` inside the deployed worker before enabling anything.

- [ ] **Step 5: Commit**

```bash
git add alandas/system_1/discovery_runs.py alandas/system_1/models.py alandas/system_1/db.py alandas/tests/test_system1_core.py
git commit -m "feat(discovery): persist provider run state"
```

### Task 3: Build provider adapters with cost and reconciliation guards

**Files:**
- Create: `alandas/system_1/provider_http.py`
- Create: `alandas/system_1/apify_provider.py`
- Create: `alandas/system_1/outscraper_provider.py`
- Modify: `alandas/system_1/outscraper_webhook.py`
- Modify: `alandas/tests/test_system1_core.py`

**Interfaces:**
- `HttpTransport.request(method, url, headers, body, timeout_seconds) -> HttpResponse`
- `ApifyProvider.submit(policy, daily_run_id, estimated_cost_usd) -> ProviderSubmission`
- `ApifyProvider.reconcile(external_id) -> ProviderOutcome`
- `OutscraperProvider.submit(policy, daily_run_id, callback_url, estimated_cost_usd) -> ProviderSubmission`
- `OutscraperProvider.reconcile(external_id) -> ProviderOutcome`

- [ ] **Step 1: Write failing cost and raw-only request tests**

```python
def test_apify_refuses_cost_above_policy_cap(self) -> None:
    provider = ApifyProvider(token="secret", transport=FakeTransport())
    with self.assertRaises(CostLimitExceeded):
        provider.submit(policy_with_apify_cap(Decimal("1.40")), "daily-1", Decimal("1.41"))

def test_outscraper_request_has_no_paid_enrichment_parameters(self) -> None:
    transport = FakeTransport(response_json={"id": "request-123", "status": "Pending"})
    OutscraperProvider(token="secret", transport=transport).submit(policy(), "daily-1", "https://receiver.example/callback?token=hidden", Decimal("0.60"))
    request = transport.requests[0]
    self.assertIn("limit=50", request.url)
    self.assertNotIn("contacts_n_leads", request.url)
    self.assertNotIn("emails_validator_service", request.url)
```

- [ ] **Step 2: Verify RED**

Run: `python -m unittest alandas.tests.test_system1_core.System1CoreTests.test_apify_refuses_cost_above_policy_cap alandas.tests.test_system1_core.System1CoreTests.test_outscraper_request_has_no_paid_enrichment_parameters`

Expected: FAIL because adapters do not exist.

- [ ] **Step 3: Implement current provider contracts**

Use `Authorization: Bearer <APIFY_API_TOKEN>` for Apify and `X-API-KEY: <OUTSCRAPER_API_KEY>` for Outscraper; never use query-string tokens.

- Apify: `POST https://api.apify.com/v2/acts/compass~crawler-google-places/runs`; persist the run ID; reconcile using `GET /v2/actor-runs/{runId}`, then fetch its `defaultDatasetId` only after terminal success. Submit four category requests whose limits total 50, set `maxItems=50`, and use `maxTotalChargeUsd` equal to the policy cap.
- Outscraper: asynchronous `GET https://api.outscraper.cloud/google-maps-search` with a Germany café query, `limit=50`, `async=true`, and the callback URL. Do not send any enrichment parameter. Persist returned ID before waiting. Reconcile the saved request ID before any replacement submission.

The HTTP wrapper redacts authorization and callback query values, logging only provider, method, response status, duration, and external ID.

- [ ] **Step 4: Verify GREEN**

```bash
python -m unittest alandas.tests.test_system1_core
python -m py_compile alandas/system_1/provider_http.py alandas/system_1/apify_provider.py alandas/system_1/outscraper_provider.py
rg -n "APIFY_API_TOKEN=|OUTSCRAPER_API_KEY=|token=[A-Za-z0-9]" alandas/system_1 alandas/tests
```

Expected: tests/compile pass; no actual secret value is found.

- [ ] **Step 5: Commit**

```bash
git add alandas/system_1/provider_http.py alandas/system_1/apify_provider.py alandas/system_1/outscraper_provider.py alandas/system_1/outscraper_webhook.py alandas/tests/test_system1_core.py
git commit -m "feat(discovery): add bounded provider adapters"
```

### Task 4: Add the daily workflow and controlled schedule

**Files:**
- Create: `alandas/system_1/discovery_activities.py`
- Create: `alandas/system_1/discovery_workflows.py`
- Create: `alandas/system_1/discovery_scheduler.py`
- Modify: `alandas/system_1/worker.py`
- Modify: `alandas/tests/test_system1_core.py`

**Interfaces:**
- `DailyDiscoveryWorkflow.run(policy_version: str, scheduled_for: str) -> DailyDiscoveryResult`
- `final_daily_status(provider_statuses: Mapping[str, str]) -> str`
- `schedule_action(policy: TrialPolicy, day: date) -> Literal["run", "pause"]`
- `start_trial_schedule(client, policy) -> str`; `pause_trial_schedule(client, schedule_id) -> None`

- [ ] **Step 1: Write failing partial-failure and day-eight tests**

```python
def test_daily_status_is_degraded_when_one_provider_fails(self) -> None:
    self.assertEqual(final_daily_status({"apify": "succeeded", "outscraper": "needs_attention"}), "degraded")

def test_day_eight_pauses_without_submission(self) -> None:
    policy = TrialPolicy.default(date(2026, 9, 17))
    self.assertEqual(schedule_action(policy, date(2026, 9, 24)), "pause")
```

- [ ] **Step 2: Verify RED**

Run: `python -m unittest alandas.tests.test_system1_core.System1CoreTests.test_daily_status_is_degraded_when_one_provider_fails alandas.tests.test_system1_core.System1CoreTests.test_day_eight_pauses_without_submission`

Expected: FAIL because these decisions do not exist.

- [ ] **Step 3: Implement durable orchestration**

The workflow creates the stable daily run before provider work. It starts providers independently, applies Task 2 retry rules, and opens only the failing provider's circuit after its third failure. It finalizes `succeeded`, `degraded`, or `needs_attention` with an idempotent audit event.

Register this workflow and activities in `worker.py`. The separate scheduler CLI creates/updates exactly one Temporal schedule in `Europe/Berlin`; worker boot must never create schedules. Day eight calls pause, preserving history.

- [ ] **Step 4: Verify GREEN**

```bash
python -m unittest alandas.tests.test_system1_core
python -m py_compile alandas/system_1/discovery_activities.py alandas/system_1/discovery_workflows.py alandas/system_1/discovery_scheduler.py alandas/system_1/worker.py
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add alandas/system_1/discovery_activities.py alandas/system_1/discovery_workflows.py alandas/system_1/discovery_scheduler.py alandas/system_1/worker.py alandas/tests/test_system1_core.py
git commit -m "feat(discovery): schedule durable trial runs"
```

### Task 5: Add Coolify controls, status output, and runbook

**Files:**
- Modify: `alandas/docker-compose.system1.coolify.yml`
- Modify: `alandas/.env.system1.example`
- Modify: `alandas/system_1/webhook_server.py`
- Create: `alandas/system_1/discovery_status.py`
- Create: `alandas/system_1/AUTOMATED_DISCOVERY_RUNBOOK.md`
- Modify: `alandas/system_1/CURRENT_PROJECT_STATE.md`
- Modify: `alandas/tests/test_system1_core.py`

**Interfaces:**
- Feature flag: `SYSTEM1_DISCOVERY_ENABLED=false`.
- Secrets: `APIFY_API_TOKEN`, `OUTSCRAPER_API_KEY`, `OUTSCRAPER_WEBHOOK_TOKEN`.
- Cost caps: `SYSTEM1_DISCOVERY_MAX_APIFY_USD=1.40`, `SYSTEM1_DISCOVERY_MAX_OUTSCRAPER_USD=0.60`.
- `python -m system_1.discovery_status today`.
- `python -m system_1.discovery_scheduler start-trial` and `pause-trial`.

- [ ] **Step 1: Write failing operator-control tests**

```python
def test_start_refuses_when_feature_flag_is_off(self) -> None:
    with self.assertRaisesRegex(RuntimeError, "SYSTEM1_DISCOVERY_ENABLED"):
        validate_scheduler_environment({"SYSTEM1_DISCOVERY_ENABLED": "false"})

def test_status_output_redacts_tokens(self) -> None:
    self.assertNotIn("secret", format_daily_status(sample_run(), {"APIFY_API_TOKEN": "secret"}))
```

- [ ] **Step 2: Verify RED**

Run: `python -m unittest alandas.tests.test_system1_core.System1CoreTests.test_start_refuses_when_feature_flag_is_off alandas.tests.test_system1_core.System1CoreTests.test_status_output_redacts_tokens`

Expected: FAIL because controls do not exist.

- [ ] **Step 3: Add disabled-by-default operations**

Add a non-public `system1-scheduler` Compose service. It receives the same internal Temporal/Postgres access as the worker. Let the webhook service boot while disabled, but reject enabled callbacks without a configured 32-character secret.

Write the runbook in this exact order: secrets entered directly in Coolify; deploy disabled; health/status checks; only webhook receives a public HTTPS domain; one manually approved displayed-cost run; verify provider ID, audit row, workflow, and dedupe; then enable the seven-day schedule. Explain pause command and `needs_attention` recovery. Do not add Slack, email, WhatsApp, CRM, enrichment, or outreach actions.

- [ ] **Step 4: Verify GREEN**

```bash
docker compose -f alandas/docker-compose.system1.coolify.yml config
python -m unittest alandas.tests.test_system1_core
```

Expected: Compose resolves with discovery disabled and tests pass.

- [ ] **Step 5: Commit**

```bash
git add alandas/docker-compose.system1.coolify.yml alandas/.env.system1.example alandas/system_1/webhook_server.py alandas/system_1/discovery_status.py alandas/system_1/AUTOMATED_DISCOVERY_RUNBOOK.md alandas/system_1/CURRENT_PROJECT_STATE.md alandas/tests/test_system1_core.py
git commit -m "feat(discovery): add controlled trial operations"
```

### Task 6: Verify before live enablement

**Files:**
- Modify: `alandas/system_1/STATUS_AUDIT.md`
- Modify: `alandas/system_1/CURRENT_PROJECT_STATE.md`

- [ ] **Step 1: Run local evidence checks**

```bash
python -m unittest alandas.tests.test_system1_core
python -m py_compile alandas/system_1/*.py
git diff --check
git status --short
```

Expected: tests and compilation pass, no whitespace errors, and no accidental staging of `_skill_staging/` or `alandas/alandas-slice1-skills.zip`.

- [ ] **Step 2: Push only with Cyril's explicit instruction**

After Cyril says push, push reviewed commits and confirm Coolify keeps the original services healthy.

- [ ] **Step 3: Prove disabled state**

Deploy with `SYSTEM1_DISCOVERY_ENABLED=false`. Verify no provider request is created and status is `not_started` or `paused`.

- [ ] **Step 4: Perform one manual live contract check**

Before scheduling, inspect both displayed estimates, tell Cyril the exact total, and obtain a separate live-run confirmation. Run the capped request, verify provider ID, audit row, Temporal workflows, accepted candidate count, and duplicate suppression. If the estimate exceeds the caps, stop before submission.

- [ ] **Step 5: Enable the week and prove the stop**

Enable the schedule only after the manual check. Verify the first scheduled run in Temporal/Postgres/provider dashboards. On day eight verify it paused and paid enrichment remained disabled. Record mechanism, failure prediction, verification, and boundary defence in `STATUS_AUDIT.md`.

## Plan self-review

- **Spec coverage:** Task 1 covers scope and trial policy. Task 2 adds durable run state. Task 3 isolates vendor calls, costs, reconciliation, and redaction. Task 4 covers scheduling and partial failure. Task 5 adds controls and operational recovery. Task 6 requires local and live proof.
- **Placeholder scan:** No `TODO`, `TBD`, or unspecified error handling is used.
- **Type consistency:** `TrialPolicy` feeds durable run storage; storage feeds providers; providers feed workflow activities; operations call the named scheduler/status interfaces.

