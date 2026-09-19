"""Record human approval for planned discovery lead enrichment steps.

Local-only database mutation. Never makes network calls, never accesses CRM or
live providers, and never spends money.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal
import logging
import sys
from typing import Any

from system_1 import db

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StepApprovalSummary:
    workflow_id: str
    step_name: str
    approved_by: str
    max_cost_usd: str
    status: str  # "created" | "already_exists"


def approve_enrichment_step(
    workflow_id: str,
    step_name: str,
    approved_by: str,
    max_cost_usd: Decimal | None = None,
) -> StepApprovalSummary:
    """Validate that the step exists in the lead's enrichment plan and record approval."""
    clean_wid = workflow_id.strip()
    clean_step = step_name.strip()
    clean_approver = approved_by.strip()

    if not clean_wid:
        raise ValueError("workflow-id is required")
    if not clean_step:
        raise ValueError("step-name is required")
    if not clean_approver:
        raise ValueError("approved-by is required")

    db.ensure_schema()
    plan = db.fetch_enrichment_plan(clean_wid)
    if plan is None:
        raise ValueError(f"no enrichment plan found for lead '{clean_wid}'")

    steps = plan.get("steps") or []
    target_step = next((s for s in steps if s.get("name") == clean_step), None)
    if target_step is None:
        raise ValueError(f"step '{clean_step}' not found in enrichment plan for lead '{clean_wid}'")

    is_paid_step = bool(target_step.get("may_cost_money"))
    if is_paid_step:
        if max_cost_usd is None or max_cost_usd < Decimal("0.00"):
            raise ValueError(
                f"paid step '{clean_step}' requires --max-cost-usd greater than or equal to 0.00"
            )
        cost_to_record = max_cost_usd
    else:
        if max_cost_usd is None:
            cost_to_record = Decimal("0.00")
        elif max_cost_usd < Decimal("0.00"):
            raise ValueError("max-cost-usd cannot be negative")
        else:
            cost_to_record = max_cost_usd

    approval, is_new = db.record_enrichment_step_approval(
        workflow_id=clean_wid,
        step_name=clean_step,
        approved_by=clean_approver,
        max_cost_usd=cost_to_record,
    )

    return StepApprovalSummary(
        workflow_id=clean_wid,
        step_name=clean_step,
        approved_by=clean_approver,
        max_cost_usd=f"{Decimal(str(approval['max_cost_usd'])):.2f}",
        status="created" if is_new else "already_exists",
    )


def format_step_approval_summary(summary: StepApprovalSummary) -> str:
    """Format clean summary for terminal output."""
    lines = [
        "=== Enrichment Step Approval Summary ===",
        f"Workflow ID:  {summary.workflow_id}",
        f"Step Name:    {summary.step_name}",
        f"Approved By:  {summary.approved_by}",
        f"Max Cost USD: {summary.max_cost_usd}",
        f"Status:       {summary.status}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Record human approval for a planned discovery lead enrichment step."
    )
    parser.add_argument("--workflow-id", required=True, help="Workflow ID of the lead")
    parser.add_argument("--step-name", required=True, help="Planned step name to approve")
    parser.add_argument("--approved-by", required=True, help="Operator approving the step")
    parser.add_argument(
        "--max-cost-usd",
        type=Decimal,
        default=None,
        help="Maximum spend authorized for this step in USD",
    )

    args = parser.parse_args()

    try:
        summary = approve_enrichment_step(
            workflow_id=args.workflow_id,
            step_name=args.step_name,
            approved_by=args.approved_by,
            max_cost_usd=args.max_cost_usd,
        )
        print(format_step_approval_summary(summary))
        return 0
    except Exception as error:
        print(f"Approval failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
