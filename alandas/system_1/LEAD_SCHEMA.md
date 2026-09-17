# System 1 Lead Schema

Every raw candidate must fit the intake schema. It needs a fuller record before
outreach can be drafted.

## Fields

| Field | Meaning | Example |
| --- | --- | --- |
| `venue_name` | Name of the cafe or venue | Cafe Beispiel |
| `city` | Target city | Berlin |
| `venue_type` | Cafe, brunch, restaurant, hotel, bakery | cafe |
| `website` | Main website URL if found | https://example.de |
| `instagram` | Instagram URL or handle if found | https://instagram.com/example |
| `email` | Best contact email if found | hello@example.de |
| `phone` | Best phone or WhatsApp number if found | +49 30 123456 |
| `impressum_url` | Impressum or contact page source | https://example.de/impressum |
| `decision_maker` | Owner or manager name if public | Maria Beispiel |
| `seat_estimate` | Estimated seating count | 40 |
| `fit_score` | 1 to 5 | 4 |
| `fit_reason` | Plain reason this venue fits | brunch cafe with premium drinks |
| `source_url` | Page where the lead was found | https://maps.google.com/... |
| `status` | Current workflow state | new |
| `next_action` | What happens next | draft outreach |

## Status values

Use one of these:

- `new`
- `researching`
- `duplicate_review`
- `needs_research`
- `qualified`
- `drafted`
- `sent_to_sidy`
- `approved`
- `contacted`
- `rejected`

## Validation rules

- Intake requires `venue_name`, `city`, `venue_type`, and `source_url`. This is
  enough to accept a raw Google Maps or Instagram candidate.
- Outreach requires the intake fields plus one contact route: `email`, `phone`,
  `instagram`, or `website`.
- `fit_score` must be a number from 1 to 5.
- `status` must match the allowed list.
- URLs should start with `http://` or `https://` when present.

## Research and duplicate rules

- The system normalizes website domains, Instagram handles, and venue-plus-city
  names before comparing leads.
- A possible existing match becomes `duplicate_review`. It never overwrites the
  existing record automatically.
- Public-site research can fill blank contact fields only. Each value keeps the
  source page where it was found.
- Public fetching is disabled by default. It is read-only when enabled: no login,
  form submission, direct message, or paid enrichment tool is part of this slice.

## Human approval rule

A lead can move from `drafted` to `contacted` only after Sidy approves the text.
