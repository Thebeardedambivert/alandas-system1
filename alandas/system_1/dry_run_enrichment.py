"""Local-only dry-run executor for Alandas System 1 discovery lead enrichment.

Evaluates which planned enrichment steps would run, which are blocked, and why,
without executing any enrichment or calling any network providers.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import sys
from typing import Any, Sequence

from system_1 import db

LOCAL_STEPS = {"system1_duplicate_check", "phone_validation"}


@dataclass(frozen=True)
class DryRunSummary:
    leads_inspected: int
    total_steps: int
    would_run: int
    blocked_missing_approval: int
    blocked_provider_not_connected: int
    blocked_paid_step: int
    skipped_local_only: int


def evaluate_step_decision(
    step: dict[str, Any],
    approval: dict[str, Any] | None,
) -> tuple[str, str]:
    """Evaluate decision status and human-readable explanation for a planned step."""
    name = str(step.get("name") or "")
    requires_external = bool(step.get("requires_external_call"))
    may_cost_money = bool(step.get("may_cost_money"))

    # 1. Local-only checks
    if name in LOCAL_STEPS or not requires_external:
        return "skipped_local_only", "Local-only check; skipped during external enrichment execution"

    # 2. Paid enrichment steps
    # Current production fact: Paid enrichment providers are not connected yet.
    if may_cost_money:
        return (
            "blocked_provider_not_connected",
            "Paid enrichment provider is not connected yet (Apollo, GitLeads, Prospeo, etc.)",
        )

    # 3. External free steps
    if approval is None:
        return "blocked_missing_approval", "Requires human approval before external execution"

    return "would_run", f"Approved by {approval.get('approved_by')}"


def format_lead_dry_run(
    plan: dict[str, Any],
    approvals: dict[tuple[str, str], dict[str, Any]],
) -> tuple[str, list[str]]:
    """Format dry-run evaluation for a single lead."""
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
        "Step Decisions:",
    ]

    steps = plan.get("steps") or []
    step_decisions: list[str] = []
    if not steps:
        lines.append("  (none)")
    else:
        for idx, step in enumerate(steps, start=1):
            name = str(step.get("name") or "unnamed_step")
            approval = approvals.get((workflow_id, name))
            decision, explanation = evaluate_step_decision(step, approval)
            step_decisions.append(decision)
            lines.append(f"  {idx}. {name}: {decision}")
            lines.append(f"     - Reason: {explanation}")

    return "\n".join(lines), step_decisions


def format_dry_run_summary(summary: DryRunSummary) -> str:
    """Format the overall dry run summary block."""
    lines = [
        "=== Dry-Run Enrichment Summary ===",
        f"Leads Inspected:                 {summary.leads_inspected}",
        f"Total Steps:                     {summary.total_steps}",
        f"Would Run:                       {summary.would_run}",
        f"Blocked Missing Approval:        {summary.blocked_missing_approval}",
        f"Blocked Provider Not Connected:  {summary.blocked_provider_not_connected}",
        f"Blocked Paid Step:               {summary.blocked_paid_step}",
        f"Skipped Local Only:              {summary.skipped_local_only}",
    ]
    return "\n".join(lines)


def render_dry_run_report(
    plans: Sequence[dict[str, Any]],
    approvals: dict[tuple[str, str], dict[str, Any]],
) -> tuple[str, DryRunSummary]:
    """Render full dry-run report and aggregate summary counts."""
    leads_inspected = len(plans)
    total_steps = 0
    would_run = 0
    blocked_missing_approval = 0
    blocked_provider_not_connected = 0
    blocked_paid_step = 0
    skipped_local_only = 0

    lead_blocks: list[str] = []

    for plan in plans:
        block_text, decisions = format_lead_dry_run(plan, approvals)
        lead_blocks.append(block_text)
        for d in decisions:
            total_steps += 1
            if d == "would_run":
                would_run += 1
            elif d == "blocked_missing_approval":
                blocked_missing_approval += 1
            elif d == "blocked_provider_not_connected":
                blocked_provider_not_connected += 1
            elif d == "blocked_paid_step":
                blocked_paid_step += 1
            elif d == "skipped_local_only":
                skipped_local_only += 1

    summary = DryRunSummary(
        leads_inspected=leads_inspected,
        total_steps=total_steps,
        would_run=would_run,
        blocked_missing_approval=blocked_missing_approval,
        blocked_provider_not_connected=blocked_provider_not_connected,
        blocked_paid_step=blocked_paid_step,
        skipped_local_only=skipped_local_only,
    )

    full_output = "\n\n".join(lead_blocks)
    if full_output:
        full_output += "\n\n"
    full_output += format_dry_run_summary(summary)

    return full_output, summary


def dry_run_enrichment(
    statuses: Sequence[str] = ("qualified", "needs_review"),
    limit: int = 50,
) -> DryRunSummary:
    """Fetch plans and approvals from Postgres and display dry-run report."""
    db.ensure_schema()
    plans = db.fetch_enrichment_plans(statuses=statuses, limit=limit)
    workflow_ids = [str(p["workflow_id"]) for p in plans if p.get("workflow_id")]
    approvals = db.fetch_enrichment_step_approvals(workflow_ids)

    report_text, summary = render_dry_run_report(plans, approvals)
    print(report_text)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run executor previewing discovery lead enrichment decisions."
    )
    parser.add_argument(
        "--statuses",
        nargs="+",
        default=["qualified", "needs_review"],
        help="Qualification statuses to inspect (default: qualified needs_review)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of leads to inspect (default: 50)",
    )
    args = parser.parse_args()

    try:
        dry_run_enrichment(statuses=args.statuses, limit=args.limit)
        return 0
    except Exception as error:
        print(f"Dry run failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
