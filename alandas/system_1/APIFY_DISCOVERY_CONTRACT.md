# Apify Google Maps Discovery Contract

## Purpose

Apify's `compass/crawler-google-places` actor is the proposed raw-candidate
source. It finds businesses. It does not decide whether a business is suitable,
and it does not send messages.

This contract is intentionally offline. No token, API call, paid actor run, or
schedule is configured in System 1 yet.

## One small run

A future run must be deliberately created with:

- Germany-wide search scope;
- four category allocations that total 50 results: 20 cafes, 10 brunch venues,
  10 specialty coffee venues, and 10 boutique hotels;
- no reviews, reviewer data, images, business-lead enrichment, social-profile
  enrichment, competitor-analysis add-on, or email-verification add-on.

The actor advertises usage pricing. A run is a paid external action. The operator
must state the current estimated cost and obtain Cyril's approval before it runs.
For the seven-day source-quality trial, paid enrichment is disabled. This is a
temporary policy: later approved enrichment remains part of Alandas' waterfall,
not an actor-side shortcut.

## Accepted actor fields

The mapper accepts only the documented standard place fields:

| Actor field | System 1 field | Reason |
| --- | --- | --- |
| `placeId` | `source_record_id` | Stable source-level duplicate key |
| `url` | `source_url` | Evidence of where the candidate came from |
| `title` | `venue_name` | Candidate name |
| `city` | `city` | German-market context; country code is the deterministic guard |
| `categoryName` | `venue_type` | Initial category; final fit is decided later |
| `countryCode` | `country_code` | Germany-only guard |
| `website` | `website` | Starts the public website/Impressum waterfall |
| `phoneUnformatted` or `phone` | `phone` | Public business phone only |
| `address` | `address` | Human review context only |

Rows that are advertisements, marked closed, incomplete, non-German, or a
duplicate Google Place ID are skipped and recorded as notes. The mapper does not
read email, reviews, reviewer information, contact-enrichment results, or social
profile enrichment from the actor output.

## Handoff

```text
Apify exported dataset
-> offline mapper and review notes
-> raw LeadInput
-> existing intake validation and internal duplicate review
-> website + Impressum evidence waterfall
```

The `placeId` is source provenance, not a permission to skip public-source
verification. A website or Impressum finding must still retain its own source
evidence.

## Security and operations

- Keep any future `APIFY_TOKEN` only in Coolify environment variables.
- Do not put a token in this repository, a CSV, a log, or chat.
- Do not run more than the reviewed result limit.
- Store the future run ID, search terms, city, result count, and estimated/actual
  cost in the audit trail.
- A failed or duplicate import must not start duplicate outreach workflows.
