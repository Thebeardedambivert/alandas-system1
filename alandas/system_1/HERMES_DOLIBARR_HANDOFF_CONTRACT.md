# Hermes-to-Dolibarr Handoff Contract

## Purpose

This document defines how Alandas System 1, Hermes, and Dolibarr work together.

The goal is simple: a qualified cafe appears once in Dolibarr, outreach is never
sent twice by accident, and the system can show what actually happened.

This is a contract, not a live integration. No credentials or external writes are
enabled by this document.

## System roles

| System | Owns | Must not do |
| --- | --- | --- |
| Alandas System 1 / Temporal | Lead research state, draft, Sidy's approval, follow-up timing, and audit trail | Send a message, create an invoice, or replace the CRM |
| Hermes | WhatsApp and email delivery facts; WhatsApp order-photo and voice-note parsing when restored | Invent product details, create final invoices without validation, or silently retry sends |
| Dolibarr | Customer/prospect records, stock, invoices, and commercial record | Decide whether an AI draft is approved |
| Sidy | Approval of external outreach and resolution of ambiguous orders or failed handoffs | Manually reconcile routine successful handoffs |

Dolibarr is the CRM and accounting system of record. Temporal is the durable
process tracker. Hermes is a channel adapter, not a second CRM.

## Vocabulary

| Term | Meaning |
| --- | --- |
| `workflow_id` | Stable Alandas ID for one lead workflow |
| `handoff_key` | Stable idempotency key for one external action: `<workflow_id>:<event_name>` |
| `dolibarr_thirdparty_id` | ID returned by Dolibarr for the prospect/customer record |
| `message_id` | ID returned by Hermes or the email/WhatsApp provider after delivery is accepted |
| delivery fact | A confirmed result from Hermes, such as accepted, delivered, failed, or opted out |

## Lead handoff: Alandas to Dolibarr

### Trigger

The first safe version hands a lead to Dolibarr only after it passes lead
validation. It does **not** send outreach. This lets Sidy see qualified leads in
his existing CRM before any channel action.

### Request payload

```json
{
  "handoff_key": "alandas-lead-berlin-example-cafe:dolibarr_lead_upsert",
  "workflow_id": "alandas-lead-berlin-example-cafe",
  "source": "alandas-system-1",
  "lead": {
    "venue_name": "Example Cafe",
    "city": "Berlin",
    "venue_type": "cafe",
    "website": "https://example.de",
    "instagram": "https://instagram.com/example",
    "email": "hello@example.de",
    "phone": "+49301234567",
    "impressum_url": "https://example.de/impressum",
    "decision_maker": "",
    "seat_estimate": 40,
    "fit_score": 4,
    "fit_reason": "premium brunch cafe with visible drinks service",
    "source_url": "https://example.de"
  }
}
```

Only public business-contact data that is needed for the sales process belongs in
the handoff. Do not send prompts, model notes, secrets, or raw scraped page text.

### Deterministic duplicate check

Before creating a record, the Dolibarr adapter searches in this order:

1. Existing stored `dolibarr_thirdparty_id` for the `workflow_id`.
2. Exact normalized business email, if present.
3. Exact normalized phone number, if present.
4. Exact normalized website domain plus city.
5. Exact normalized venue name plus city.

If one clear match is found, update only the Alandas-owned lead metadata and
return that record's ID. If multiple possible matches are found, do not choose;
mark the handoff `needs_review` for Sidy. A weak name-only match across cities is
not enough.

### Success response

```json
{
  "handoff_key": "alandas-lead-berlin-example-cafe:dolibarr_lead_upsert",
  "status": "created",
  "dolibarr_thirdparty_id": "123",
  "occurred_at": "2026-09-17T12:00:00Z"
}
```

Allowed values for `status` are `created`, `updated`, `duplicate_matched`,
`needs_review`, and `failed`.

The adapter records the returned ID and response status in the Alandas audit
trail. Repeating the same `handoff_key` must return the earlier result or make no
second CRM change.

## Message delivery handoff: Hermes to Alandas

Hermes may report a delivery fact only after Sidy has approved the exact outreach
draft in the corresponding workflow.

```json
{
  "handoff_key": "alandas-lead-berlin-example-cafe:message_sent:hermes-abc123",
  "workflow_id": "alandas-lead-berlin-example-cafe",
  "channel": "whatsapp",
  "message_id": "hermes-abc123",
  "status": "accepted",
  "occurred_at": "2026-09-17T12:05:00Z"
}
```

Allowed delivery states are `accepted`, `delivered`, `failed`, and `opted_out`.

- `accepted` may move an approved workflow to `contacted`.
- `delivered` adds evidence only; it does not send a follow-up early.
- `failed` keeps the workflow out of `contacted` and creates a review task.
- `opted_out` blocks future outreach for that contact and is sent to Dolibarr as
  a suppression marker.

Hermes must not accept a request without a `workflow_id`, `handoff_key`, and
Sidy-approved status supplied by Alandas. Alandas must not mark a send as real
from a browser click or a draft alone; it needs Hermes' `message_id`.

## State transitions

```text
validated
  -> crm_synced | crm_review_required | crm_sync_failed
crm_synced
  -> drafted
drafted
  -> approved | rejected
approved
  -> delivery_pending
delivery_pending
  -> contacted | delivery_failed | opted_out
contacted
  -> follow_up_due
```

The current deployed workflow already enforces `drafted -> approved -> contacted`
through a recorded send. The Hermes connector will replace the manual
`record-sent` operation only after its delivery receipt is verified.

## Failure and recovery rules

| Situation | Required result |
| --- | --- |
| Temporary Dolibarr or Hermes network failure | Retry with bounded backoff and the same `handoff_key` |
| Invalid credentials, permission failure, or invalid data | Do not retry blindly; alert Cyril/Sidy and keep the item for review |
| Timeout after sending request | Query the provider by `handoff_key` or provider reference before retrying |
| Ambiguous CRM duplicate | Do not merge or overwrite; request Sidy's choice |
| Hermes reports failure | Do not set the lead to contacted; retain the error without secret values |
| Opt-out or do-not-contact request | Record immediately in Dolibarr and Alandas; block future sends |
| Hermes or Dolibarr outage | Keep Temporal state and audit records; resume reconciliation after recovery |

## Required access before implementation

1. Dolibarr base URL, REST API version, and a least-privilege API key.
2. Confirmation of the Dolibarr entity/module and fields Sidy uses for prospects.
3. A non-production Dolibarr record or test environment.
4. Hermes endpoint or webhook documentation, authentication method, and its
   message-status payload examples.
5. Confirmation of the actual email and WhatsApp delivery provider behind Hermes.
6. A named owner for failed/ambiguous cases and a way to notify them.

Do not paste credentials into chat or commit them. They belong in Coolify's
runtime environment variables after the connector exists.

## Acceptance checks for the first connector slice

1. A test lead creates one Dolibarr prospect record and returns its ID.
2. Repeating the identical handoff creates no second prospect record.
3. A matching existing Dolibarr prospect is linked, not duplicated.
4. An ambiguous duplicate becomes `needs_review` and writes nothing.
5. An unapproved workflow cannot call Hermes to send a message.
6. A repeated Hermes delivery webhook changes no state twice.
7. A failed delivery never becomes `contacted`.
8. An opt-out blocks future delivery attempts and is visible in Dolibarr.

## Next implementation sequence

1. Confirm the six access facts above with Sidy.
2. Build a read-only Dolibarr capability check: authenticate and search one test
   lead, with no create/update action.
3. Build and test the idempotent prospect upsert using a test record.
4. Add Hermes delivery receipts behind the existing Sidy approval gate.
5. Only then replace the manual `record-sent` command in normal operations.
