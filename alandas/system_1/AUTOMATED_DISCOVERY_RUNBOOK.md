# Automated discovery trial runbook

This runbook is for the seven-day, Germany-wide raw-lead trial. It does not
authorize outreach, CRM writes, paid enrichment, email verification, or phone
lookups.

## Before the first test

1. In Coolify, keep `SYSTEM1_DISCOVERY_ENABLED=false`.
2. Enter `APIFY_API_TOKEN`, `OUTSCRAPER_API_KEY`, and a random
   `OUTSCRAPER_WEBHOOK_TOKEN` of at least 32 characters directly in Coolify.
   Do not place their values in Git, chat, screenshots, or this file.
3. Keep the two caps at USD 1.40 (Apify) and USD 0.60 (Outscraper).
4. Deploy while disabled. Confirm existing Temporal, Postgres, worker, and UI
   services remain healthy.
5. Run `python -m system_1.discovery_status today`. It must show discovery as
   `no` and must not print any secret value.

## One manual, capped test

Only after the provider dashboards show estimates at or below the two caps:

1. State the exact displayed total to Cyril and obtain a separate confirmation.
2. Enable discovery for that one manual run only.
3. Check the provider request IDs, Postgres audit/run rows, Temporal workflow,
   accepted-candidate count, and duplicate handling.
4. Switch discovery off again if any result is `needs_attention` or costs are
   unclear. Reconcile the saved provider request; never submit a replacement
   merely because a network call timed out.

## Recovery rules

- 401, invalid input, or a missing secret: stop and correct configuration.
- 429 or 5xx: retry after 30 seconds, 2 minutes, then 10 minutes.
- A timeout with an unknown provider outcome: do not retry automatically;
  reconcile the original request ID or mark it for attention.
- A single provider failure makes the day `degraded`, not successful.
- Day eight pauses the trial. Do not extend it without a new reviewed policy.
