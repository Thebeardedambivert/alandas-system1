"""Local-only discovery enrichment planning engine for System 1.

Prepares an operator-readable, deterministic enrichment plan for qualified and
review-needed leads before any enrichment execution occurs. Never makes network
calls, never writes to CRM, and never spends credits or money.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import logging
import sys
from typing import Any, Sequence
from urllib.parse import urlparse

from system_1 import db

logger = logging.getLogger(__name__)

HOSTED_OR_SOCIAL_DOMAINS = {
    "canva.site",
    "canva.com",
    "sumup.link",
    "sumup.store",
    "metro.rest",
    "metro.biz",
    "facebook.com",
    "fb.com",
    "instagram.com",
    "linktr.ee",
    "wixsite.com",
    "business.site",
}


@dataclass(frozen=True)
class PlannedStep:
    name: str
    requires_external_call: bool
    may_cost_money: bool
    requires_human_approval: bool
    reason: str


@dataclass(frozen=True)
class LeadEnrichmentPlan:
    workflow_id: str
    qualification_status: str
    steps: list[PlannedStep]


@dataclass(frozen=True)
class EnrichmentPlanSummary:
    leads_inspected: int
    plans_created: int
    plans_updated: int
    rejected_skipped: int
    external_steps_pending_approval: int
    paid_steps_pending_approval: int
    failed: int


def _clean_domain(domain_or_url: str) -> str:
    val = domain_or_url.strip().lower()
    if not val:
        return ""
    if "://" in val:
        parsed = urlparse(val)
        val = parsed.netloc or parsed.path
    if ":" in val:
        val = val.split(":")[0]
    if val.startswith("www."):
        val = val[4:]
    return val


def plan_lead_enrichment_steps(lead: dict[str, Any]) -> list[PlannedStep]:
    """Determine necessary enrichment steps based on lead data and status.

    Pure function, zero external or network side effects.
    """
    website = str(lead.get("website") or "").strip()
    phone = str(lead.get("phone") or "").strip()
    email = str(lead.get("email") or "").strip()
    instagram = str(lead.get("instagram") or "").strip()
    raw_domain = str(lead.get("website_domain") or "") or website
    domain = _clean_domain(raw_domain)

    is_hosted = any(domain == h or domain.endswith("." + h) for h in HOSTED_OR_SOCIAL_DOMAINS)
    has_custom_website = bool(website) and not is_hosted

    steps: list[PlannedStep] = []

    # 1. System 1 internal duplicate check (always performed locally first)
    steps.append(
        PlannedStep(
            name="system1_duplicate_check",
            requires_external_call=False,
            may_cost_money=False,
            requires_human_approval=False,
            reason="Check System 1 database for existing lead or duplicate venue records",
        )
    )

    # 2. Website / Social Surface Analysis
    if is_hosted or (not website and bool(instagram)):
        steps.append(
            PlannedStep(
                name="instagram_review",
                requires_external_call=True,
                may_cost_money=False,
                requires_human_approval=True,
                reason="Review social/hosted profile for business details and active presence",
            )
        )
    elif has_custom_website:
        steps.append(
            PlannedStep(
                name="website_review",
                requires_external_call=True,
                may_cost_money=False,
                requires_human_approval=True,
                reason="Inspect homepage and impressum for decision maker and business details",
            )
        )
        if not email:
            steps.append(
                PlannedStep(
                    name="email_lookup",
                    requires_external_call=True,
                    may_cost_money=True,
                    requires_human_approval=True,
                    reason="Find business or owner contact email via paid enrichment waterfall",
                )
            )
    else:
        # Missing website entirely
        steps.append(
            PlannedStep(
                name="website_discovery",
                requires_external_call=True,
                may_cost_money=False,
                requires_human_approval=True,
                reason="Search for official website using venue name and city",
            )
        )

    # 3. Phone Validation
    if phone:
        steps.append(
            PlannedStep(
                name="phone_validation",
                requires_external_call=False,
                may_cost_money=False,
                requires_human_approval=False,
                reason="Format and validate phone number against E.164 dial plan",
            )
        )

    # 4. Product / Menu Suitability
    steps.append(
        PlannedStep(
            name="menu_or_product_signal_check",
            requires_external_call=True,
            may_cost_money=False,
            requires_human_approval=True,
            reason="Verify matcha and specialty beverage suitability from menu",
        )
    )

    return steps


def plan_enrichment_batch(
    statuses: Sequence[str] = ("qualified", "needs_review"),
    limit: int = 50,
) -> EnrichmentPlanSummary:
    """Read leads in requested qualification statuses, plan steps, and persist idempotently."""
    db.ensure_schema()
    leads = db.fetch_leads_for_enrichment_planning(statuses=statuses, limit=limit)

    leads_inspected = 0
    plans_created = 0
    plans_updated = 0
    rejected_skipped = 0
    external_pending_approval = 0
    paid_pending_approval = 0
    failed = 0

    for lead in leads:
        q_status = str(lead.get("qualification_status") or "").strip().lower()
        if q_status == "rejected":
            rejected_skipped += 1
            continue

        workflow_id = str(lead.get("workflow_id") or "").strip()
        if not workflow_id:
            continue

        leads_inspected += 1
        try:
            steps = plan_lead_enrichment_steps(lead)
            for s in steps:
                if s.requires_external_call and s.requires_human_approval:
                    external_pending_approval += 1
                if s.may_cost_money and s.requires_human_approval:
                    paid_pending_approval += 1

            steps_dicts = [asdict(s) for s in steps]
            is_created = db.upsert_enrichment_plan(
                workflow_id=workflow_id,
                qualification_status=q_status,
                steps=steps_dicts,
            )
            if is_created:
                plans_created += 1
            else:
                plans_updated += 1
        except Exception as error:
            logger.error("Failed to plan enrichment for lead %s: %s", workflow_id, error, exc_info=True)
            failed += 1

    return EnrichmentPlanSummary(
        leads_inspected=leads_inspected,
        plans_created=plans_created,
        plans_updated=plans_updated,
        rejected_skipped=rejected_skipped,
        external_steps_pending_approval=external_pending_approval,
        paid_steps_pending_approval=paid_pending_approval,
        failed=failed,
    )


def format_plan_summary(summary: EnrichmentPlanSummary) -> str:
    """Format clean, secret-free summary for operators."""
    lines = [
        "=== Discovery Enrichment Planning Summary ===",
        f"Leads Inspected:                 {summary.leads_inspected}",
        f"Plans Created:                   {summary.plans_created}",
        f"Plans Updated:                   {summary.plans_updated}",
        f"Rejected Skipped:                {summary.rejected_skipped}",
        f"External Steps Pending Approval: {summary.external_steps_pending_approval}",
        f"Paid Steps Pending Approval:     {summary.paid_steps_pending_approval}",
        f"Failed:                          {summary.failed}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plan safe discovery lead enrichment steps without external side effects."
    )
    parser.add_argument(
        "--statuses",
        nargs="+",
        default=["qualified", "needs_review"],
        help="Qualification statuses to plan enrichment for (default: qualified needs_review)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of leads to inspect (default: 50)",
    )
    args = parser.parse_args()

    try:
        summary = plan_enrichment_batch(statuses=args.statuses, limit=args.limit)
        print(format_plan_summary(summary))
        return 0 if summary.failed == 0 else 1
    except Exception as error:
        print(f"Enrichment planning failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
