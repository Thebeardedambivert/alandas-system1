# Alandas System 1 — Configurable Enrichment Approval Policy Design

**Status:** Draft Design Note (Planning Only — No Implementation Yet)
**Date:** 2026-09-19
**Target Module:** `alandas/system_1/enrichment_policy.py`
**Governing Skills:** `agent-boundaries`, `durable-systems-engineering`, `ai-security-governance`, `production-readiness`, `writing-plans`, `requesting-code-review`

---

## 1. Executive Summary & Context

System 1 currently supports step-by-step human approval and manual evidence entry for planned discovery enrichment steps (`website_review`, `menu_or_product_signal_check`, `instagram_review`, `email_lookup`).

While this establishes an air-gapped security boundary, **approving individual enrichment steps lead-by-lead will overwhelm operators and Sidy at production scale (hundreds/thousands of leads).**

### Agent & Human Boundaries (`agent-boundaries`)
To scale sustainably without compromising safety, we define three strict responsibility layers:
1. **System 1 (Deterministic Orchestration):** Evaluates enrichment plans against a versioned policy rulebook, enforces spend caps, routes work between automated execution and queues, and records audit logs.
2. **Operator (Cyril):** Handles operational enrichment queues: manual website reviews, impressum checks, menu validation, and data entry. Manages provider configurations and cost controls.
3. **Business Owner (Sidy):** Retains exclusive authority over **commercial claims, customer-facing outreach message approval, brand positioning, and unusual high-risk lead escalations.** Sidy is never spammed with routine operational enrichment steps.

---

## 2. Policy Fields Needed

The policy must be represented as a frozen, strongly-typed configuration structure (`EnrichmentPolicy`):

```python
from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping

@dataclass(frozen=True)
class StepRule:
    mode: str  # "automatic" | "manual" | "blocked"
    requires_approval: bool = False
    max_step_cost_usd: Decimal = Decimal("0.00")

@dataclass(frozen=True)
class EnrichmentPolicy:
    policy_version: str                                  # e.g., "enrichment-v1"
    step_rules: Mapping[str, StepRule]                  # Rules per step name
    paid_enrichment_enabled: bool = False               # Global kill switch for paid APIs
    max_cost_per_lead_usd: Decimal = Decimal("0.20")    # Hard ceiling per venue
    max_daily_spend_usd: Decimal = Decimal("5.00")       # Hard ceiling per calendar day
    escalate_unclear_leads: bool = True                 # Route ambiguous scores to operator queue

    # Invariant Business Gates (Non-Overridable)
    require_evidence_for_outreach_draft: bool = True     # Never draft without stored evidence
    require_sidy_approval_for_outreach_send: bool = True # Never send without Sidy's signoff
    require_sidy_approval_for_commercial_claims: bool = True # Pricing / wholesale discount signoff
```

### Initial Baseline Rule Set:
* `website_review`: `mode = "manual"` (future: `"automatic"` once local headless browser worker is built).
* `menu_or_product_signal_check`: `mode = "manual"` (future: `"automatic"` with menu parser).
* `instagram_review`: `mode = "manual"` (or `"blocked"` if social review is deprioritized).
* `email_lookup`: `mode = "blocked"` (current truth: providers not connected. Future: `"manual"` or `"automatic"` under strict `max_step_cost_usd`).

---

## 3. Human-Facing Control Surface (Sidy & Operator Experience)

To ensure Sidy is empowered without needing to edit code, JSON files, or database rows, System 1 provides a clean, plain-language control surface.

### A. What Sidy Can Safely Change Himself
* **Step Automation Toggles:** Decide which enrichment steps run automatically vs. wait in Cyril's review queue vs. are completely blocked.
* **Budget Allocations:** Set and adjust maximum allowable spend per lead and maximum allowable daily spend across all providers.
* **Risk Escalation Thresholds:** Adjust qualification score thresholds for flagging high-value or ambiguous venues for business owner review.
* **IMMUTABLE BOUNDARY (What Sidy CANNOT Change):**
  * Sidy cannot disable `require_sidy_approval_for_outreach_send`.
  * Sidy cannot disable `require_sidy_approval_for_commercial_claims`.
  * Sidy cannot disable `require_evidence_for_outreach_draft`.
  * These safety invariants are hardcoded in application logic and cannot be turned off by any policy setting.

### B. What Cyril / Operator Controls
* Technical infrastructure: PostgreSQL schemas, Coolify deployments, Docker containers, Temporal worker health.
* Provider credential management and secret isolation (`OUTSCRAPER_API_KEY`, `APIFY_API_TOKEN`).
* Execution of reconciliation commands (`discovery_reconcile`) and provider batch imports (`import_apify_dataset`).
* Processing the operational enrichment queue (`operator_review_needed`) and recording manual evidence.

### C. Control Mechanism (How Sidy Interacts)
* **Phase 1 (Immediate / Operational): Operator-Assisted Policy Form:**
  * Sidy receives a structured plain-language summary or checklist (via message or internal form).
  * Sidy indicates desired policy adjustments in plain language.
  * Cyril runs an operator command to stage and validate the change:
    `python -m system_1.apply_enrichment_policy --policy-file <file> --approved-by Sidy`
* **Phase 2 (Target Web GUI): Plain-Language Admin Dashboard:**
  * Simple settings screen displaying toggle switches and bounded numeric inputs with zero technical jargon.

### D. Plain-Language Settings Display (What Sidy Sees)
```text
=== Alandas Enrichment & Outreach Policy Settings ===

Enrichment Automation Rules:
  1. Website Review:            [ Automatic | Operator Review | Blocked ]  -> Set to: Operator Review
  2. Menu & Matcha Signal Check: [ Automatic | Operator Review | Blocked ]  -> Set to: Operator Review
  3. Instagram Social Review:   [ Operator Review | Blocked ]             -> Set to: Operator Review
  4. Paid Email Lookup:         [ Blocked | Ask Sidy First | Auto-Cap ]   -> Set to: Blocked

Financial Spending Caps:
  - Paid Enrichment Allowed:    [ NO ]
  - Maximum Cost Per Lead:      [ €0.20 ]
  - Maximum Daily Budget:       [ €5.00 ]

Business & Safety Gates (Locked Invariants):
  [LOCKED] Outreach Drafts:      Allowed only with recorded evidence in database
  [LOCKED] Outreach Sending:     Always requires Sidy's explicit signoff before sending
  [LOCKED] Commercial Claims:    Wholesale prices and shipping claims require Sidy approval
```

### E. How Policy Changes Are Previewed Before Activation
Before any policy change becomes active, System 1 generates a **Dry-Run Policy Impact Preview**:
```powershell
python -m system_1.preview_policy_change --new-policy <policy_version> --sample 50
```
**Preview Output:**
* Shows side-by-side comparison on currently pending leads:
  * Current Policy: 11 leads in operator review queue, 0 automatic, 0 paid calls.
  * Proposed Policy: 8 leads automatic, 3 leads in operator review, estimated cost: $0.00.
* Alerts operator and Sidy if the proposed policy would cause unexpected spend or queue surges.

### F. How Policy Changes Are Audited and Rolled Back
* **Immutable Audit Trail:**
  * Every policy activation is written to PostgreSQL table `lead_enrichment_policies` with `activated_by`, `activated_at`, `rules JSONB`, and `change_reason`.
  * Past policies are never deleted; they are preserved with `is_active = FALSE`.
* **Instant One-Command Rollback:**
  * If a new policy generates unintended queue spikes or operator friction, Cyril or Sidy can immediately restore the prior safe policy:
    ```powershell
    python -m system_1.rollback_enrichment_policy --to-version <previous_policy_version>
    ```
  * Reverts the active pointer immediately and logs the rollback event in the audit trail.

---

## 4. Policy Location & Storage

1. **Code Defaults (`system_1/enrichment_policy.py`):**
   * Built-in `EnrichmentPolicy.default()` provides a secure, fail-closed configuration in source control.
   * Safety invariants (`require_sidy_approval_for_outreach_send = True`) are hardcoded and cannot be disabled by configuration.
2. **Postgres Storage (`lead_enrichment_policies` table):**
   ```sql
   CREATE TABLE IF NOT EXISTS lead_enrichment_policies (
       policy_version TEXT PRIMARY KEY,
       rules JSONB NOT NULL,
       is_active BOOLEAN NOT NULL DEFAULT FALSE,
       created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
   );
   ```
3. **Operator CLI:**
   * `python -m system_1.show_enrichment_policy`: Displays the active policy, cost caps, and step modes.
   * `python -m system_1.update_enrichment_policy`: Allows Cyril/Sidy to activate a new versioned policy.

---

## 5. Impact on Dry-Run Enrichment (`dry_run_enrichment`)

The dry-run executor transitions from hardcoded step conditionals to evaluating `(step, approval, policy, daily_spend_to_date)`.

### Decision Matrix:
| Step Type | Policy Rule | Approval Exists? | Provider Connected? | Under Spend Cap? | Dry-Run Decision Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Local check (`system1_duplicate_check`) | Any | N/A | N/A | N/A | `skipped_local_only` |
| Free external (`website_review`) | `manual` | Yes | N/A | N/A | `operator_review_needed` |
| Free external (`website_review`) | `manual` | No | N/A | N/A | `blocked_missing_approval` |
| Free external (`website_review`) | `automatic` | N/A | Yes (tool ready) | N/A | `would_run_automatic` |
| Free external (`instagram_review`) | `blocked` | N/A | N/A | N/A | `blocked_policy_rule` |
| Paid step (`email_lookup`) | Any | Any | **No (current)** | N/A | `blocked_provider_not_connected` |
| Paid step (`email_lookup`) | `automatic` | N/A | Yes | **No (exceeded)** | `blocked_budget_exceeded` |
| Paid step (`email_lookup`) | `automatic` | N/A | Yes | Yes | `would_run_automatic` |

*Note: High-risk leads (e.g. enterprise chains or ambiguous venue types) are tagged `escalated_to_sidy`.*

---

## 6. Impact on Manual Evidence Entry (`record_manual_enrichment_evidence`)

1. **Policy Enforcement on Write:**
   * If a step is `mode = "blocked"` under the active policy, `record_manual_enrichment_evidence` rejects the entry immediately (`ValueError: step '{step_name}' is blocked by active enrichment policy`).
   * If a step is `mode = "manual"`, it verifies whether the policy requires explicit human approval before evidence entry.
2. **Evidence Schema Consistency:**
   * Stored evidence continues to use `lead_manual_enrichment_evidence` with primary key `(workflow_id, step_name, field)`.
   * Retains accurate lifecycle status: `created`, `already_exists`, or `updated`.

---

## 7. What Stays Hard-Blocked For Now

Under current project facts, the following boundaries remain absolute:
1. **Live Paid Provider APIs:** GitLeads, Apollo, Prospeo, MillionVerifier, LeadMagic remain disconnected. No paid API requests will be executed.
2. **CRM Integration:** Zero writes to Dolibarr.
3. **Outreach Execution:** Zero emails, WhatsApp messages, or Instagram DMs sent.
4. **Temporal Schedules:** No automated discovery/enrichment schedules created.
5. **Commercial Commitments:** No automated wholesale pricing or stock guarantees.

---

## 8. What Can Later Become Automatic

Once reliable tools and sandboxes are built and verified:
1. **Automated Website Review:** Headless browser extraction of impressum / decision maker names from custom domains.
2. **Automated Menu Signal Check:** Ingestion and OCR/text extraction of menus to find matcha, specialty tea, and beverage signals.
3. **Automated Website Discovery:** Querying official business registries or search results for unlinked venues.
4. **Cost-Capped Email Waterfall:** Controlled paid lookup when authorized by Cyril with strict USD caps per lead and per day.

---

## 9. Failure Modes & Recovery Plan (`production-readiness`, `durable-systems-engineering`)

| Failure Mode | Impact | Recovery / System Behavior |
| :--- | :--- | :--- |
| **Missing or malformed policy in DB** | CLI or pipeline cannot determine step rules | **Fail-closed:** Fall back immediately to hardcoded `EnrichmentPolicy.default()`, which blocks all paid steps and flags all external steps as manual/approval-required. Log warning. |
| **Daily spend cap reached mid-batch** | Subsequent paid steps attempt to execute | **Atomic gate:** Evaluate spend atomically against DB ledger before each paid call; transition status to `blocked_budget_exceeded`. Zero overrun. |
| **Provider API failure / timeout** | Provider is down or returns error | **Isolation:** Mark step failed in plan; do not retry infinitely. Queue for operator review. |
| **Operator review queue backlog** | Unenriched leads accumulate | **No data loss:** Items remain safely in Postgres queue (`operator_review_needed`). Operator summary shows queue depth without timeout. |
| **Untrusted scraped text injection** | Scraped website contains prompt injection attempts | **AI Security Governance:** Untrusted content is stored as inert evidence strings. Policy gates and execution rules are written in deterministic Python, not driven by LLM prompts. |

---

## 10. Test Strategy Before Implementation (`test-driven-development`)

Before any implementation code is written, the following tests must be specified and run RED:
1. **Policy Immutability & Defaults:** Verify `EnrichmentPolicy.default()` enforces zero paid spend, blocks unconfigured steps, and immutably enforces Sidy approval for outreach sends.
2. **Policy Parser & Validation:** Verify negative cost caps, unknown step names, and missing versions raise descriptive errors.
3. **Dry-Run Matrix Verification:** Verify that modifying policy rules (`manual` vs `automatic` vs `blocked`) dynamically alters dry-run step decisions and summary counts.
4. **Budget Limit Enforcement:** Verify that simulated spend exceeding `max_cost_per_lead_usd` or `max_daily_spend_usd` trips `blocked_budget_exceeded`.
5. **Manual Evidence Policy Gate:** Verify that attempting to record evidence for a policy-blocked step is rejected.
6. **Zero Provider / Zero Side Effect Guarantee:** Assert that policy evaluation makes zero network calls and incurs $0.00 spend.
