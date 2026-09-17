# Automated Discovery Trial — Design

**Status:** proposed and approved for specification; implementation requires this
document's review

## Outcome and boundary

For seven days, Alandas System 1 will automatically request up to 50 raw German
cafe candidates per day from Apify and up to 50 from Outscraper.  The system
will pass safe, unique candidates into the existing lead workflow.  It will
measure whether the sources produce useful leads before the paid enrichment
waterfall is enabled.

This is a discovery trial, not outreach automation.  It does not send a
message, create a CRM record, use Hermes, or charge a customer.  Sidy approval
remains required before every customer-facing message.

"No paid enrichment" is a temporary trial policy.  The policy becomes
configurable after the trial; it does not remove the planned paid enrichment
waterfall.

## Trial policy

| Setting | Trial value | Why |
| --- | --- | --- |
| Duration | 7 calendar days | Enough samples to compare sources without open-ended spend |
| Geography | Germany | The market is Germany, not only Berlin, Hamburg, or Munich |
| Apify categories | 20 cafes; 10 brunch venues; 10 specialty coffee venues; 10 boutique hotels | Tests the full agreed ideal-customer mix while retaining enough volume per category |
| Outscraper category | Cafes, 50 source rows/day | Creates a focused comparison lane for raw Maps discovery |
| Apify cap | 50 source rows/day | Bounds one actor run across the four category allocations |
| Outscraper cap | 50 source rows/day | Bounds one focused vendor request |
| Combined cap | 100 source rows/day; 700/week | Makes the maximum exposure known before a run |
| Provider extras | Disabled | The trial measures raw discovery quality first |
| Paid waterfall stages | Disabled for this trial | Avoids mixing discovery-source quality with enrichment value |
| Outreach | Disabled | Existing Sidy approval rule is unchanged |

The system treats 50 as a maximum, not a promise.  A provider can return fewer
rows and the duplicate guard can accept fewer still.

## Cost guard

The system stores an estimated maximum for every provider request before it
submits it.  It refuses a request when that estimate exceeds the trial policy.
It records the provider-reported actual cost when available.

Public pricing checked on 2026-09-17 gives a conservative trial ceiling of
about USD 2 for 350 rows from each provider:

- Apify: use USD 4 per 1,000 as the conservative account-specific rate Cyril
  previously saw, giving a maximum of USD 1.40.  Existing Apify credit may
  cover this, but the system does not assume that credit exists.
- Outscraper: first 500 Maps places are free per 30-day tier; the remaining
  maximum 200 at USD 3 per 1,000 give USD 0.60.

The displayed provider estimate is authoritative.  A difference from the
configured rate stops that provider before a charge.  No enrichment add-on is
included in these figures.

## Components and ownership

| Component | Responsibility | Durable record |
| --- | --- | --- |
| Discovery policy | Trial dates, caps, geography, provider settings, cost ceilings | Postgres policy/run tables |
| Temporal schedule | Starts one daily discovery cycle in Europe/Berlin time | Temporal schedule and workflow history |
| Daily discovery workflow | Allocates per-provider work and decides whether the daily run is complete, degraded, or needs attention | Workflow state plus audit events |
| Apify adapter | Starts one actor run and obtains only raw Maps fields | Provider run ID and result/audit reference |
| Outscraper adapter | Starts one Maps request with the callback endpoint | Provider request ID and callback audit reference |
| Webhook ingress | Authenticates Outscraper completion data and starts the existing lead workflows | Existing audit_events row keyed by request ID |
| Existing CafeLeadWorkflow | Validates, researches later, drafts, and waits for Sidy | Existing lead and audit records |

Provider transport code stays behind adapters.  A provider can be paused or
replaced without changing the lead, approval, or CRM boundaries.

## Data flow

```text
Temporal daily schedule (Europe/Berlin)
  -> discovery run: YYYY-MM-DD + policy version
  -> budget/cap/duration check
  -> start Apify with the four category allocations and Outscraper for cafes
  -> provider run/request ID saved before waiting
  -> retrieve result or accept callback
  -> provider mapper: only raw Maps business fields
  -> Germany guard + row cap + source-place deduplication
  -> existing stable CafeLeadWorkflow ID
  -> audit summary and daily outcome
```

The daily run ID is stable: `discovery:<policy-version>:<Europe/Berlin-date>`.
Each provider attempt uses
`<daily-run-id>:<provider>`.  The same ID is used for audit writes and external
provider idempotency where that provider supports a request key.  A retry never
creates a second daily allocation or a second lead workflow.

## Failure policy

| Situation | System action | Human action |
| --- | --- | --- |
| Network timeout / 429 / 5xx | Retry the same request at 30 seconds, 2 minutes, then 10 minutes; honour `Retry-After` if supplied | None unless retries are exhausted |
| Timeout after submission | Query the saved provider run/request ID before doing anything else | None if the provider confirms outcome |
| Unknown charge/outcome | Mark provider run `needs_attention`; do not submit another paid request | Cyril checks the provider dashboard / run ID |
| Bad token, forbidden request, invalid settings | No retry; mark `needs_attention` | Cyril replaces credential or corrects policy |
| Malformed or too-large callback | Reject before workflow creation and record a safe failure event | Check provider configuration if repeated |
| Duplicate callback/result | Return the existing result; do not create duplicate lead workflows | None |
| Three provider failures in one day | Open that provider's circuit for the day and mark daily run degraded | Investigate before the next run |
| One provider fails, the other succeeds | Complete as `degraded`; retain the healthy provider's results | Review the daily summary |
| Scheduler restart | Temporal resumes the durable daily workflow | None |

No LLM decides retries, charges, credentials, or external delivery.  Those are
deterministic rules.

## Observability and operator controls

Every daily and provider run records:

- daily run ID, provider, policy version, Europe/Berlin start time;
- provider request/run ID; request cap; estimated and actual cost;
- row count received, valid candidates, duplicates, skipped rows, workflows
  started, and workflows already present;
- retry count, error class, final status, and reason.

The service exposes a health check and a read-only status command that shows
today's outcome and any `needs_attention` runs.  Logs never contain API tokens,
webhook query tokens, or full callback bodies.

Operational controls are explicit:

- pause the schedule;
- disable either provider independently;
- end the seven-day policy early;
- change post-trial limits only by creating a new policy version;
- replay a completed callback safely, but never blindly resubmit an unknown
  paid provider request.

## Post-trial state

On day eight, the trial policy ends automatically and the scheduler pauses.
Nothing silently moves to paid enrichment.  The review compares provider cost,
unique valid candidates, qualification yield, and duplicate rate.

After Cyril approves the results, a new policy version may enable a limited,
priced stage of the existing enrichment waterfall.  It starts with the
cheapest stage that improves qualification evidence.  The discovery providers
remain raw-candidate sources; their optional paid enrichments do not bypass the
waterfall.

## Evidence required before a live claim

1. Unit tests prove caps, Germany guard, duplicate suppression, backoff
   decisions, retry exhaustion, cost refusal, and disabled trial completion.
2. A no-charge adapter simulation proves the complete daily state path.
3. Coolify deploys the scheduler and webhook service successfully; health and
   a read-only status command are checked.
4. One manually approved, displayed-cost provider run proves the real provider
   callback/result contract before the schedule is enabled.
5. The first scheduled day is checked in Temporal, Postgres audit history, and
   provider dashboards.

## Known limits and decisions still pending

- The exact provider API token permissions, request schema, run-status lookup,
  and callback configuration will be verified from the providers' current
  official documentation before live credentials are added.
- Apify and Outscraper may return overlapping or geographically uneven Maps
  results.  The trial evaluates accepted unique leads, not provider row count.
- There is no notification channel connected to Alandas yet.  Until one is
  separately approved, `needs_attention` is visible in audit/status output and
  Coolify/Temporal logs rather than sent through Slack, email, or WhatsApp.
- The active commercial offer still needs Sidy's confirmation before real
  outreach.
