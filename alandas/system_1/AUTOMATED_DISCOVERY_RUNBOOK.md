# Automated discovery trial runbook

This runbook is for the seven-day, Germany-wide raw-lead trial. It does not
authorize outreach, CRM writes, paid enrichment, email verification, or phone
lookups.

## Before the first test

1. In Coolify, keep `SYSTEM1_DISCOVERY_ENABLED=false`.
2. Enter `APIFY_API_TOKEN` directly in Coolify. Outscraper is excluded until separately approved; `OUTSCRAPER_API_KEY`, `OUTSCRAPER_WEBHOOK_TOKEN`, and `SYSTEM1_DISCOVERY_OUTSCRAPER_CALLBACK_BASE_URL` are not required for Apify-only mode. Do not place secret values in Git, chat, screenshots, or this file.
3. Keep the Apify cap at USD 1.40 (Outscraper cap USD 0.60 applies only if Outscraper is separately approved and configured).
4. Deploy while disabled. Confirm existing Temporal, Postgres, worker, and UI services remain healthy.
5. Run `python -m system_1.discovery_status today`. It must show discovery as `no` and must not print any secret value.

## One manual, capped test

Only after the provider dashboard (Apify) shows an estimate at or below the USD 1.40 cap:

1. State the exact displayed total to Cyril and obtain a separate confirmation.
2. Enable discovery for that one manual run only.
3. In the Coolify terminal for `system1-worker`, run
   `python -m system_1.discovery_scheduler start-manual`.
4. Check the provider request IDs, Postgres audit/run rows, Temporal workflow,
   accepted-candidate count, and duplicate handling.
5. Switch discovery off again if any result is `needs_attention` or costs are
   unclear. Reconcile the saved provider request; never submit a replacement
   merely because a network call timed out.

## Recovery rules

- 401, invalid input, or a missing secret: stop and correct configuration.
- 429 or 5xx: retry after 30 seconds, 2 minutes, then 10 minutes.
- A timeout with an unknown provider outcome: do not retry automatically;
  reconcile the original request ID or mark it for attention.
- A single provider failure makes the day `degraded`, not successful.
- Day eight pauses the trial. Do not extend it without a new reviewed policy.

## Start and stop the seven-day schedule

After the one manual check is accepted, run
`python -m system_1.discovery_scheduler start-trial` once in the worker
terminal. It schedules a 09:00 Europe/Berlin run and has an end date before
day eight. To stop early, run `python -m system_1.discovery_scheduler
pause-trial`.
