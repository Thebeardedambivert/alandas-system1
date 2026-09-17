# Alandas System 1 — Current Project State

**Last updated:** 2026-09-17 (discovery-trial deployment and SDK validation)
**Use this file first when resuming work in a new session.**

## One-sentence purpose

Build a reliable B2B lead-to-follow-up system for Alandas Tea Berlin: it finds
and qualifies suitable German cafes, prepares safe outreach for Sidy's approval,
and later connects to the tools Sidy already uses.

The business target is 100 active wholesale cafe accounts. System 1's immediate
target is a clean first batch of qualified leads for the EUR 19 discovery tasting
box.

## Confirmed business facts

- Sidy is the founder of Alandas Tea Berlin.
- The EUR 19 discovery tasting box is the current B2B offer used in System 1
  drafts. It includes a teapot, tray, spoon, and samples, and is intended to be
  credited against the EUR 249 starter crate.
- Sidy has an existing Dolibarr CRM/ERP for accounts, stock, and invoices.
- Sidy calls his existing email/WhatsApp agent **Hermes**. He reports that it
  sends email and WhatsApp and keeps leads in the CRM, but this has not yet been
  independently verified.
- Sidy has separate B2B and B2C Instagram accounts. B2B is the future inbound
  lead channel.
- Sidy does not want an AI making unreviewed claims to customers. He is willing
  to manage roughly 10–20 customer conversations per day himself.
- Payment for the current work has been received.

## Live, verified System 1 foundation

The Git-backed Docker Compose stack is deployed through Coolify. The following
services are running:

- Postgres
- Temporal Postgres
- Temporal server
- Temporal admin tools
- Temporal UI, kept private behind a Caddy gateway
- System 1 worker

The Temporal UI gateway login has been verified. No passwords, hashes, or other
secrets belong in this repository or this document.

### Workflow behavior verified live

The deployed workflow is:

```text
lead starts
-> validate
-> enrich research notes
-> draft outreach
-> wait for Sidy approval
-> wait for a real send record
-> wait 4 days
-> mark follow-up due
```

The following was tested on the live worker:

1. A sample lead workflow started successfully.
2. `record-sent` was rejected before approval.
3. Sidy approval changed the workflow to `approved`.
4. A recorded send changed the workflow correctly.
5. Retrying one audit write twice created exactly one Postgres `audit_events`
   row and one JSONL audit record.

The retry-safe audit rule uses the stable key:

```text
<workflow_id>:<event_name>
```

## System boundaries

| Component | Owns | Current state |
| --- | --- | --- |
| Alandas System 1 / Temporal | Lead workflow state, drafts, approval, timers, audit trail | Live |
| Postgres | System 1 lead rows and queryable audit history | Live |
| Dolibarr | CRM, customer/prospect records, stock, invoices | Not connected |
| Hermes | Existing email/WhatsApp delivery and future order parsing | Not connected or verified |
| OpenReply | Future B2B Instagram inbound comment-to-DM flow | Not connected |
| Sidy | Customer-message approval and handling ambiguous cases | Required human gate |

System 1 does not currently write to Dolibarr, Hermes, Shopify, Meta,
WhatsApp, or Instagram. It must not claim those connections are live.

## Discovery trial — current verified state

The seven-day Germany-wide raw-lead discovery trial is now implemented and
deployed, but remains **disabled**. It is a discovery and qualification input,
not an outreach or CRM automation.

Trial design:

- Apify: 50 raw Google Maps candidates/day: cafes (20), brunch venues (10),
  specialty coffee venues (10), and boutique hotels (10).
- Outscraper: 50 raw Google Maps cafe candidates/day.
- Maximum raw intake: 100 candidates/day, 700 over seven days.
- No paid enrichment, reviews, email validation, or phone lookups during this
  trial.
- The existing public-site/Impressum research remains the next enrichment
  step after raw intake.
- No outreach, CRM write, Hermes delivery, or Instagram message can occur in
  this trial.

Safety controls already implemented:

- `SYSTEM1_DISCOVERY_ENABLED=false` is the default and blocks provider calls.
- Apify and Outscraper have separate daily cost caps: USD 1.40 and USD 0.60.
- A provider submission is reserved before the request. A network timeout with
  an unknown result must be reconciled, not resubmitted.
- Daily workflow IDs and audit event keys are stable, preventing duplicates.
- The intended schedule is 09:00 Europe/Berlin and ends before day eight.

### Latest deployment and live checks

- GitHub/Coolify deployment `83f2ae5` succeeded on 2026-09-17.
- In the deployed worker, `python -m system_1.discovery_status today` showed:
  `not_started`, discovery disabled, and neither provider configured.
- The deployed Temporal SDK accepted `ScheduleSpec` with
  `time_zone_name='Europe/Berlin'` and the intended end date.

### Current blocker — do not enable discovery yet

The next no-spend, in-memory schedule-object test exposed one remaining SDK
compatibility mismatch:

```text
ScheduleActionStartWorkflow.__init__() takes one workflow argument payload,
not two separate positional workflow arguments.
```

No Temporal schedule, lead-provider request, or paid action was created by that
test. A local regression test has been added but the correction is not yet
committed or deployed. The next session must inspect the deployed signature
before changing the schedule action. Use this safe command in the
`system1-worker` Coolify terminal:

```sh
python -c "from temporalio.client import ScheduleActionStartWorkflow; import inspect; print(inspect.signature(ScheduleActionStartWorkflow))"
```

Then update `system_1/discovery_scheduler.py`, add/adjust a regression test,
run the full test suite, commit, push only with Cyril's approval, redeploy
while disabled, and repeat the full in-memory schedule-object check.

For the detailed resume sequence, read `SESSION_HANDOFF_2026-09-17.md`.

## Agreed lead generation and qualification waterfall

```text
Google Maps / Instagram raw lead
-> normalize venue data
-> duplicate check
-> budget and rate-limit check
-> Stage 0: public website / §5 TMG Impressum
-> Stage 1: GitLeads or Apollo
-> Stage 2: Origami or Prospeo
-> MillionVerifier email validation
-> Stage 3: LeadMagic mobile lookup, only when justified
-> Gemini Flash ICP qualification (score >= 70)
-> Claude personalized draft
-> Sidy approval
-> future Hermes delivery receipt + Dolibarr handoff
```

### Waterfall policy

- Use the cheapest reliable source first.
- Start with free public sources: website, German Impressum/contact page,
  Instagram profile, and Google profile.
- Paid providers are fallbacks, not the default path.
- No paid tools have been connected or used.
- Do not spend without explicit approval. Until Sidy approves a change, use the
  stricter planning limit: EUR 15/day and EUR 60 total.
- Do not buy personal mobile data or use a paid lookup merely because a phone
  field is empty.

### Fit rule

Prioritise cafes, brunch venues, boutique hotels, and specialty coffee venues
across Germany. Look for likely seating above 30, visible quality in food or
drinks, and a credible loose-leaf tea fit. Exclude low-margin kiosks and random
snack shops. The proposed AI qualification threshold is an ICP score of 70 or
more; lower-scoring leads go to low-priority nurture.

## Safety rules

- AI drafts; Sidy approves before customer outreach.
- Never claim every tea is organic, guarantee profit, or promise stock that Sidy
  has not confirmed.
- Do not auto-send outreach, create invoices, run Meta ads, or alter Dolibarr
  records without separate approved implementation and the needed access.
- Opt-outs must block future messages when delivery integration is built.
- Do not paste secrets into chat, source code, commits, screenshots, or docs.

## Integration contracts and access gaps

The Hermes-to-Dolibarr contract is documented in
`HERMES_DOLIBARR_HANDOFF_CONTRACT.md`.

Before building the actual connector, obtain through Sidy's normal login screens
or a secure channel:

1. Dolibarr login URL and a safe test account or test record.
2. Confirmation of the Dolibarr prospect/customer fields he actually uses.
3. Hermes login URL or normal dashboard view.
4. Hermes delivery-status or webhook information, if it exists.
5. The email and WhatsApp provider behind Hermes.
6. Backup location/status for Dolibarr and Hermes before production writes.

Sidy is not technical. Ask for normal login links or screenshots, not API jargon
or passwords. He should enter sensitive credentials himself if needed.

## Priority order from here

1. Test one $0 discovery-provider run only after its displayed estimate is
   reviewed. Apify remains the first available provider because Cyril has free
   account credit. Outscraper is now an optional webhook intake path; see
   `OUTSCRAPER_WEBHOOK_CONTRACT.md`. Neither provider is live until its feature
   flag, secret, domain, and one-run verification are complete.
2. Confirm current commercial facts with Sidy before real outreach: discovery-box
   price, credit policy, available stock, and shipping threshold.
3. Inspect Sidy's normal Dolibarr and Hermes screens; build a read-only Dolibarr
   capability check.
4. Add paid enrichment providers only after their current prices and the budget
   are approved.
5. Add deterministic Gemini qualification and Claude personalization.
6. Add idempotent Dolibarr prospect upsert.
7. Add Hermes delivery receipts behind the existing Sidy approval gate.
8. Add OpenReply to the B2B Instagram account for inbound comment-to-DM flows.
9. Consider Shopify and Meta ads only as separate, approved workstreams.

## Known conflicts to resolve before outreach

Older site-audit materials show inconsistent commercial information:

- free shipping is listed as both EUR 40 and EUR 59;
- the discovery-box price is listed as both EUR 19 and EUR 9.90 netto in
  different places;
- the Teebar may appear out of stock.

Do not use unverified numbers or availability in a customer message. Confirm the
current offer directly with Sidy first.

## Important files

- `LOCKED_SCOPE.md` — Layer 1 inclusions/exclusions.
- `LEAD_SCHEMA.md` — lead fields and validation.
- `TEMPORAL_WORKFLOW.md` — deployed state machine and operator commands.
- `HERMES_DOLIBARR_HANDOFF_CONTRACT.md` — future integration boundaries.
- `APIFY_DISCOVERY_CONTRACT.md` — proposed raw-candidate contract; no live Apify connection.
- `OUTSCRAPER_WEBHOOK_CONTRACT.md` — optional callback contract; disabled by default.
- `ACCESS_CHECKLIST.md` — access discovery requirements.
- `GO_LIVE_CHECKLIST.md` — deployment reference; some entries are now historical
  because the live checks above are complete.
- `project_resources/diagrams/waterfall_enrichment_engine.svg` — enrichment
  waterfall design.
- `project_resources/diagrams/tier1_essential_automation_flowchart.svg` — Tier
  1 end-to-end flow.
- `project_resources/strategy_docs/SIDY_TECH_STACK_INTEGRATION_PLAN.md` —
  longer-term commercial architecture.

## Resume prompt for a new session

> Read `alandas/system_1/CURRENT_PROJECT_STATE.md` first. Treat it as the latest
> verified handover. Then inspect the named source files before changing code or
> connecting any external service. Do not claim an unconnected provider is live,
> do not spend money without approval, and keep Sidy approval ahead of every
> customer-facing action.
