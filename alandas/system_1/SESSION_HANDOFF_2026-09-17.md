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
at commit `75f2782`. The latest Coolify deployment succeeded.

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

## Schedule SDK blocker — resolved and deployed

The deployed `temporalio==1.16.0` requires scheduled workflow inputs in
`args=[...]` and also requires an `id=`. Two focused test-first fixes were
made, verified, committed, pushed, and deployed:

- `65b3dc7 fix: pass discovery schedule inputs via args`
- `75f2782 fix: set discovery schedule workflow id`

The deployed `system1-worker` completed the full in-memory schedule-object
check with this output:

```text
schedule_id: alandas-discovery-trial-v1
workflow_id_base: alandas-discovery-trial-v1
workflow_args: ['trial-v1', '2026-09-17']
task_queue: alandas-system1
timezone: Europe/Berlin
```

That check used a memory-only client. It created no Temporal schedule, sent no
provider request, enabled no provider, and spent no money.

## First next action — configuration only, still no spend

Have Cyril enter the provider credentials and public callback base URL directly
in Coolify. Keep `SYSTEM1_DISCOVERY_ENABLED=false`; do not start the schedule
or a manual run. Do not put credentials or token-bearing URLs in chat, source
code, Git, screenshots, or these notes.

After the settings are present while disabled, open each provider dashboard and
record its displayed estimate. Ask Cyril to approve the exact amount before a
single paid manual run. The caps remain USD 1.40/day for Apify and USD 0.60/day
for Outscraper.

## Key source files

- `system_1/discovery_scheduler.py` — manual/scheduled discovery controls;
  deployed schedule SDK compatibility is now verified.
- `system_1/discovery_temporal_workflow.py` — one durable daily workflow.
- `system_1/discovery_activities.py` — provider calls, disabled unless the
  feature flag is explicitly true.
- `system_1/discovery_controls.py` — fail-closed environment and cap checks.
- `system_1/discovery_policy.py` — daily volume and seven-day limit.
- `system_1/discovery_runs.py` and `system_1/db.py` — reservation and
  duplicate-prevention records.
- `system_1/AUTOMATED_DISCOVERY_RUNBOOK.md` — operator steps and recovery.
- `system_1/CURRENT_PROJECT_STATE.md` — broader business/system state.

## Working-tree state when this handoff was updated

GitHub `master` and Coolify are at deployed commit `75f2782`. The two schedule
SDK fixes are committed and pushed. No provider configuration, Temporal
schedule, or paid discovery run has been created in this session.

There are also existing untracked local items that must not be staged or
deleted: `.tmp/`, `_skill_staging/`, and `alandas-slice1-skills.zip`.

## Hard safety rules

- Never paste credentials, tokens, hashes, or URLs containing tokens into chat,
  source code, Git, screenshots, or this handoff.
- No auto-send. Sidy approves every customer-facing message.
- A timeout with unknown provider outcome is reconcile-only; do not resubmit.
- Never turn `SYSTEM1_DISCOVERY_ENABLED` on simply to test code.
- Do not push or redeploy without Cyril's explicit request.
