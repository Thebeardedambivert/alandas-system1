"""Local-only viewer and export command for Alandas System 1 lead enrichment plans.

Reads planned enrichment steps from PostgreSQL and formats an operator report.
Never makes network calls, never accesses CRM or live providers, and never spends money.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import sys
from typing import Any, Sequence

from system_1 import db


@dataclass(frozen=True)
class DisplaySummary:
    leads_shown: int
    total_steps: int
    external_steps_pending_approval: int
    paid_steps_pending_approval: int


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def format_lead_plan(plan: dict[str, Any]) -> str:
    """Format one lead's enrichment plan for terminal display."""
    workflow_id = str(plan.get("workflow_id") or "")
    venue_name = str(plan.get("venue_name") or "(unknown venue)")
    city = str(plan.get("city") or "")
    qualification_status = str(plan.get("qualification_status") or "")
    score = plan.get("qualification_score")
    score_display = str(score) if score is not None else "n/a"

    lines = [
        f"=== Lead: {workflow_id} ===",
        f"Venue:                {venue_name} ({city})",
        f"Qualification Status: {qualification_status} (Score: {score_display})",
        "Planned Steps:",
    ]

    steps = plan.get("steps") or []
    if not steps:
        lines.append("  (none)")
    else:
        for idx, step in enumerate(steps, start=1):
            name = str(step.get("name") or "unnamed_step")
            ext = bool(step.get("requires_external_call"))
            paid = bool(step.get("may_cost_money"))
            approval = bool(step.get("requires_human_approval"))
            reason = str(step.get("reason") or "")

            lines.append(f"  {idx}. {name}")
            lines.append(f"     - External call required:  {_yes_no(ext)}")
            lines.append(f"     - May cost money:          {_yes_no(paid)}")
            lines.append(f"     - Human approval required: {_yes_no(approval)}")
            if reason:
                lines.append(f"     - Reason:                  {reason}")

    return "\n".join(lines)


def format_plans_summary(summary: DisplaySummary) -> str:
    """Format the overall summary block for the displayed plans."""
    lines = [
        "=== Enrichment Plans Summary ===",
        f"Leads Shown:                     {summary.leads_shown}",
        f"Total Steps:                     {summary.total_steps}",
        f"External Steps Pending Approval: {summary.external_steps_pending_approval}",
        f"Paid Steps Pending Approval:     {summary.paid_steps_pending_approval}",
    ]
    return "\n".join(lines)


def render_enrichment_plans_report(plans: Sequence[dict[str, Any]]) -> tuple[str, DisplaySummary]:
    """Render all plans and compute summary metrics."""
    leads_shown = len(plans)
    total_steps = 0
    external_pending = 0
    paid_pending = 0

    plan_blocks: list[str] = []

    for plan in plans:
        plan_blocks.append(format_lead_plan(plan))
        steps = plan.get("steps") or []
        for step in steps:
            total_steps += 1
            if step.get("requires_external_call") and step.get("requires_human_approval"):
                external_pending += 1
            if step.get("may_cost_money") and step.get("requires_human_approval"):
                paid_pending += 1

    summary = DisplaySummary(
        leads_shown=leads_shown,
        total_steps=total_steps,
        external_steps_pending_approval=external_pending,
        paid_steps_pending_approval=paid_pending,
    )

    full_output = "\n\n".join(plan_blocks)
    if full_output:
        full_output += "\n\n"
    full_output += format_plans_summary(summary)

    return full_output, summary


def show_enrichment_plans(
    statuses: Sequence[str] = ("qualified", "needs_review"),
    limit: int = 50,
) -> DisplaySummary:
    """Fetch plans from PostgreSQL and print formatted report to stdout."""
    db.ensure_schema()
    plans = db.fetch_enrichment_plans(statuses=statuses, limit=limit)
    report_text, summary = render_enrichment_plans_report(plans)
    print(report_text)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="View planned discovery lead enrichment steps from local Postgres."
    )
    parser.add_argument(
        "--statuses",
        nargs="+",
        default=["qualified", "needs_review"],
        help="Qualification statuses to display plans for (default: qualified needs_review)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of plans to display (default: 50)",
    )
    args = parser.parse_args()

    try:
        show_enrichment_plans(statuses=args.statuses, limit=args.limit)
        return 0
    except Exception as error:
        print(f"Error displaying enrichment plans: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
