# Alandas System 1 — Session Handoff (2026-09-17)

Read this file and `CURRENT_PROJECT_STATE.md` before changing code or asking
Cyril to do anything.

## Where the project is

The durable Layer 1 lead workflow is live in Coolify and previously verified:

```text
lead -> validate -> public research notes -> draft -> Sidy approval
-> recorded real send -> four-day timer -> follow-up due
```

The system has no live Dolibarr, Hermes, Instagram, WhatsApp, email, Shopify,
or Meta connection. Do not describe any of those as connected.

The automated discovery trial code is deployed on GitHub `master` and Coolify
at commit `83f2ae5`. The latest Coolify deployment succeeded.

## Trial agreed with Cyril

For one seven-day, Germany-wide test:

| Provider | Raw lead volume | Scope | Maximum daily cost |
| --- | ---: | --- | ---: |
| Apify Maps actor | 50 | cafe 20, brunch 10, specialty coffee 10, boutique hotel 10 | USD 1.40 |
| Outscraper Maps | 50 | cafes | USD 0.60 |

No paid enrichment, reviews, email verification, or phone lookup during this
trial. This limit is temporary. Do not submit any paid run until the provider
dashboard displays the actual estimate and Cyril separately approves that
exact amount.

## What is live and safe right now

In the deployed `system1-worker`, this command was run:

```sh
python -m system_1.discovery_status today
```

Output showed:

```text
Daily run: discovery:trial-v1:2026-09-17
Status: not_started
Discovery enabled: no
Apify configured: no
Outscraper configured: no
```

Therefore no external provider was contacted and no credit has been spent.

The deployed SDK also accepted this exact schedule specification:

```text
cron_expressions=['0 9 * * *']
time_zone_name='Europe/Berlin'
end_at=2026-09-24T00:00:00 Europe/Berlin
```

## Current blocker

The next in-memory schedule-object test failed without creating a schedule:

```text
TypeError: ScheduleActionStartWorkflow.__init__() takes from 2 to 3
positional arguments but 4 positional arguments (and 1 keyword-only argument)
were given
```

Cause: the code in `system_1/discovery_scheduler.py` gives
`ScheduleActionStartWorkflow` two positional workflow arguments:

```python
ScheduleActionStartWorkflow(
    DailyDiscoveryWorkflow.run,
    policy.policy_version,
    policy.starts_on.isoformat(),
    task_queue=task_queue,
)
```

The installed `temporalio==1.16.0` expects one payload argument (probably a
single list/tuple/dataclass), but do not guess its required form.

## First next action — no spend, no state change

Ask Cyril to run exactly this inside Coolify's `system1-worker` terminal and
paste the output:

```sh
python -c "from temporalio.client import ScheduleActionStartWorkflow; import inspect; print(inspect.signature(ScheduleActionStartWorkflow))"
```

This only prints a Python signature. It does not contact providers, create a
Temporal schedule, or spend money.

## Then follow this order

1. Use the signature output to update only
   `system_1/discovery_scheduler.py`.
2. Add a focused regression test in `tests/test_system1_core.py`. The test must
   fail before the code change and pass after it.
3. Run the full suite:

   ```powershell
   python -m unittest tests.test_system1_core
   ```

   Local Windows needs the `tzdata` package because it lacks system time-zone
   data; the worker image already includes `tzdata==2025.2`.
4. Compile the changed files and run:

   ```powershell
   docker compose -f docker-compose.system1.coolify.yml config --quiet
   ```

   A local warning about denied access to Docker's desktop `config.json` is
   known and did not prevent Compose validation.
5. Commit locally. Do not push unless Cyril explicitly says `push`.
6. After a successful Coolify deployment, while discovery remains disabled,
   repeat the complete in-memory schedule object check.
7. Only after that is green: have Cyril enter provider keys directly in
   Coolify, set the public callback base URL, and keep discovery disabled.
8. Before the single paid manual run, state the exact dashboard estimates and
   ask Cyril for a separate approval. Never infer spending approval.

## Key source files

- `system_1/discovery_scheduler.py` — manual/scheduled discovery controls;
  current SDK-action compatibility issue is here.
- `system_1/discovery_temporal_workflow.py` — one durable daily workflow.
- `system_1/discovery_activities.py` — provider calls, disabled unless the
  feature flag is explicitly true.
- `system_1/discovery_controls.py` — fail-closed environment and cap checks.
- `system_1/discovery_policy.py` — daily volume and seven-day limit.
- `system_1/discovery_runs.py` and `system_1/db.py` — reservation and
  duplicate-prevention records.
- `system_1/AUTOMATED_DISCOVERY_RUNBOOK.md` — operator steps and recovery.
- `system_1/CURRENT_PROJECT_STATE.md` — broader business/system state.

## Working-tree state when this handoff was written

The local `master` branch contains deployed commit `83f2ae5`.

The incorrect multi-argument `ScheduleActionStartWorkflow` call remains in the
currently deployed commit. It has not yet been edited locally. There is one
intentional, uncommitted test change from this debugging session:

- `tests/test_system1_core.py` — a regression test for the previously fixed
  `time_zone_name` keyword.

There are also existing untracked local items that must not be staged or
deleted: `.tmp/`, `_skill_staging/`, and `alandas-slice1-skills.zip`.

## Hard safety rules

- Never paste credentials, tokens, hashes, or URLs containing tokens into chat,
  source code, Git, screenshots, or this handoff.
- No auto-send. Sidy approves every customer-facing message.
- A timeout with unknown provider outcome is reconcile-only; do not resubmit.
- Never turn `SYSTEM1_DISCOVERY_ENABLED` on simply to test code.
- Do not push or redeploy without Cyril's explicit request.
