# System 1 Temporal Workflow

## Why Temporal is included

Layer 1 needs memory across days.

A normal script can find a lead and draft a message. But it does not naturally remember:

- Sidy still needs to approve this lead
- the message was sent
- a follow-up is due in 4 days
- a refill reminder may be due later
- the server restarted halfway through

Temporal stores that process state. It is like parcel tracking. If the driver changes, the parcel status is still known.

## Workflow

Workflow name: `CafeLeadWorkflow`

Task queue: `alandas-system1`

One workflow tracks one cafe lead.

```text
lead_started
-> validate_lead
-> enrich_lead
-> draft_outreach
-> wait for Sidy approval
-> wait for send record
-> sleep 4 days
-> mark follow_up_due
```

## Signals

Signals are how a human action moves the workflow.

| Signal | Meaning |
| --- | --- |
| `approve_by_sidy` | Sidy approved the outreach draft; only accepted while it is `drafted` |
| `reject_by_sidy` | Sidy rejected the lead or message |
| `record_sent` | Sidy or Cyril recorded that the message was sent; only accepted after approval |

## Query

| Query | Meaning |
| --- | --- |
| `current_state` | Returns the current lead state |

## Operator scripts

| Script | Job |
| --- | --- |
| `python -m system_1.import_leads <csv>` | Starts one workflow per valid CSV row |
| `python -m system_1.workflow_cli state <workflow-id>` | Shows current state |
| `python -m system_1.workflow_cli approve <workflow-id>` | Records Sidy's approval |
| `python -m system_1.workflow_cli reject <workflow-id> <reason>` | Records Sidy's rejection |
| `python -m system_1.workflow_cli record-sent <workflow-id>` | Records that Sidy sent the message |

## Activities

Activities do the work that may touch files, APIs, or services.

| Activity | Job |
| --- | --- |
| `validate_lead_activity` | Checks required lead fields |
| `enrich_lead_activity` | Records missing research steps |
| `draft_outreach_activity` | Creates the first Sidy-approved draft |
| `append_audit_event_activity` | Writes an audit event |
| `upsert_lead_activity` | Stores the lead in Postgres |
| `update_lead_status_activity` | Stores status changes in Postgres |

## Human approval rule

The workflow can draft. It cannot send.

The lead cannot become `contacted` until:

1. Sidy approves the draft.
2. A send event is recorded.

An approval signal received before a draft exists, or a send record received before
the lead reaches `approved`, is ignored. This prevents an early or duplicated
operator action from unlocking a later send.

## Retry and duplicate rule

Each audit transition has the stable key `<workflow_id>:<event_name>`. Postgres
accepts that key once. If Temporal retries the same activity after a timeout or
restart, the duplicate audit write is ignored. Future Hermes-to-Dolibarr handoffs
must use the same transition key as their idempotency key.

## Current boundary

This first setup does not write to Shopify, Meta, WhatsApp, or Dolibarr.

Those are host side effects. They need credentials, backup checks, and a separate approved action before production writes.
