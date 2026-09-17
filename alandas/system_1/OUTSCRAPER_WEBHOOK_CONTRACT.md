# Outscraper Google Maps Webhook Contract

## Purpose

Outscraper is an optional discovery provider alongside Apify. Neither provider
replaces the Alandas enrichment waterfall. They only return raw business
candidates.

```text
Apify dataset OR Outscraper callback
-> provider-specific mapper
-> raw LeadInput
-> the same duplicate check and research waterfall
-> draft only
-> Sidy approval before any customer message
```

The public callback is deliberately disabled by default. It cannot spend money,
send a message, write to Dolibarr, or call Hermes.

## Receiver

Coolify must give **only** `system1-webhook` a public HTTPS domain. Do not expose
Postgres, Temporal, the worker, or the Temporal UI for this integration.

The callback endpoint is:

```text
POST /webhooks/outscraper/google-maps?token=<OUTSCRAPER_WEBHOOK_TOKEN>
```

`OUTSCRAPER_WEBHOOK_TOKEN` must be a unique random value of at least 32
characters. It is a secret: enter it directly in Coolify and Outscraper; never
put it in Git, chat, logs, or screenshots. The receiver does not log callback
URLs or bodies.

Outscraper documents a callback URL parameter, but its public API reference does
not document a request-signature header. This token is the compatibility guard
for the first run. Before larger recurring runs, confirm Outscraper's current
signature-verification documentation and add its signed-header validation if
available.

## Accepted request

The receiver accepts a JSON object only when all of these are true:

- `id` is Outscraper's non-empty request ID;
- `status` is `Success`;
- `data` is the documented flat or nested Maps result list;
- the entire callback contains at most 50 result rows;
- each accepted row has `place_id`, `name`, `city`, `type` or `category`,
  `country_code=DE`, and a Google Maps location link;
- city is in Germany; `country_code=DE` is the deterministic intake guard.

The mapper keeps only `place_id`, name, city, category, country code, basic
website, public phone, address, and Google Maps source URL. It ignores reviews,
photos, social data, email/contact enrichment, and every paid add-on.

## Duplicate and failure behavior

- Each cafe gets the existing stable Alandas workflow ID. A retry of the same
  callback cannot create a second outreach workflow for that cafe.
- Outscraper's request ID is audited once as `outscraper_callback_received`.
- A malformed, oversized, disabled, or unauthorized request is rejected before
  it can create a workflow.
- A transient failure returns HTTP 500, so Outscraper may retry. A retry is safe
  because Temporal rejects a second start for the same workflow ID.

## Operator sequence for the first run

1. Set `OUTSCRAPER_WEBHOOK_TOKEN` in Coolify and leave the enabled flag false.
2. Deploy and confirm `GET /healthz` returns `{"status":"ok"}`.
3. Assign the service's HTTPS domain in Coolify.
4. Set the full callback URL in Outscraper's task or integration settings.
5. Create one Maps search: `Cafes, Germany`, limit 50, no enrichments.
6. Check that Outscraper displays **$0.00** before starting.
7. Enable `SYSTEM1_OUTSCRAPER_WEBHOOK_ENABLED=true`, redeploy, and perform the
   one approved test.
8. Check the webhook response, Coolify logs, Temporal, and the audit table.

Do not enable a recurring schedule until this one-run check has passed.
