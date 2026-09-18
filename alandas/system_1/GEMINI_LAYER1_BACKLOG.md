# Gemini Layer 1 Backlog — Alandas System 1

This backlog defines the strict, ordered Layer 1 implementation tasks for Gemini builder execution in Alandas System 1. Every task requires an approved task card written by Codex before work begins.

Discovery remains **disabled** (`SYSTEM1_DISCOVERY_ENABLED=false`). No task in this backlog authorizes provider calls, paid API usage, temporal schedule registrations, production writes, deployments, or customer-facing actions.

---

## Ordered Layer 1 Tasks

| ID | Task | Owner | Preconditions | Gemini role | Required skills | Stop condition | Done evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **L1-01** | Provider configuration readiness | Cyril | Coolify access available; builder governance committed | None (Cyril enters Coolify settings directly); Gemini has no secret access; discovery stays disabled | `ai-security-governance`, `platform-operations` | Any request to handle credentials, tokens, or enable discovery | Settings verified present in Coolify while `SYSTEM1_DISCOVERY_ENABLED=false` remains set |
| **L1-02** | Dashboard estimate and approval record | Cyril | L1-01 complete; provider dashboards accessible | None (Cyril records exact displayed amounts and approves them); Gemini does not infer a price or trigger a run | `model-operations`, `ai-security-governance` | Any attempt to estimate without dashboard evidence or trigger a run | Written approval record with exact dashboard estimates within USD 1.40 (Apify) and USD 0.60 (Outscraper) daily caps |
| **L1-03** | Manual discovery-run audit | Gemini (audit) / Cyril (run) | L1-02 approved; Cyril executes single manual test run | Inspect supplied run records, reservation keys, and error logs; make only scoped test-first fixes for parsing or duplicate prevention | `durable-systems-engineering`, `systematic-debugging`, `ai-security-governance`, `test-driven-development` | Provider failure requiring resubmission, live API calls, or schedule creation | Local tests pass; audit report confirms idempotent run keys and duplicate handling without data loss |
| **L1-04** | Commercial-fact record and draft safeguards | Gemini (code/docs) / Sidy (facts) | Sidy confirms tasting-box price, credit policy, available stock, and shipping threshold | Implement deterministic claim safeguards in outreach templates/prompting; add unit tests against forbidden claims | `copywriting`, `compliance-handling`, `test-driven-development`, `verification-before-completion` | Unconfirmed commercial claims or attempt to send outreach | Unit tests verify all commercial invariants; forbidden claims (e.g. organic guarantee, profit guarantee) rejected |
| **L1-05** | Dolibarr/Hermes access-gap and repair-plan documentation | Gemini | Normal-screen screenshots or safe test access provided by Sidy | Document field contracts, webhook capabilities, and recovery steps; no production writes | `ai-security-governance`, `platform-operations` | Production credentials exposed or direct write access attempted | `HERMES_DOLIBARR_REPAIR_PLAN.md` completed with field mapping and backup verification prerequisites |
| **L1-06** | Read-only Dolibarr capability check | Gemini | L1-05 complete; safe test account and isolated test instance available | Build isolated read-only connector test suite verifying schema compatibility; no writes to prospects, stock, invoices, or CRM | `platform-operations`, `ai-security-governance`, `test-driven-development`, `systematic-debugging` | Any attempt to perform HTTP POST/PUT/DELETE or write production records | Read-only test suite passes against mock/test endpoint with zero mutation operations |

---

## Out of scope

The following areas are strictly excluded from Layer 1 work and must not be implemented, scaffolded, or scheduled by Gemini:

1. **Production Dolibarr Writes:** Creating prospects, modifying stock records, altering invoices, or updating production ERP tables.
2. **Hermes Delivery Integration:** Automating outbound emails, WhatsApp message delivery, or live customer order ingestion.
3. **OpenReply / Instagram Automation:** Configuring DM bots, comment-to-DM automation, or automated social messaging.
4. **Shopify Production Changes:** Modifying live storefront themes, products, apps, or checkout settings.
5. **Meta Ad Spend:** Creating ad accounts, setting up ad campaigns, or incurring paid marketing expenditure.
6. **Autonomous Customer Messaging:** Sending unreviewed emails, WhatsApp messages, DMs, or outreach of any kind.
7. **Unapproved Spend:** Incurring any provider costs or credit consumption without Cyril's explicit written approval.
