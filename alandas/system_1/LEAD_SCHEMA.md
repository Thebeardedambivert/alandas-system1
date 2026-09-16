# System 1 Lead Schema

Every lead must fit this schema before outreach.

## Required fields

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
- `needs_research`
- `qualified`
- `drafted`
- `sent_to_sidy`
- `approved`
- `contacted`
- `rejected`

## Validation rules

- `venue_name`, `city`, `venue_type`, `fit_score`, `fit_reason`, `source_url`, `status`, and `next_action` cannot be blank.
- `fit_score` must be a number from 1 to 5.
- at least one contact route must exist: `email`, `phone`, `instagram`, or `website`.
- `status` must match the allowed list.
- URLs should start with `http://` or `https://` when present.

## Human approval rule

A lead can move from `drafted` to `contacted` only after Sidy approves the text.
