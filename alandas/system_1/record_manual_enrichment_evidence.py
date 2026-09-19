"""Record manual enrichment evidence for an approved discovery lead enrichment step.

Local-only database mutation. Never makes network calls, never accesses CRM or
live providers, and never spends money.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import logging
import sys
from typing import Any

from system_1 import db

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ManualEvidenceSummary:
    workflow_id: str
    step_name: str
    field: str
    value: str
    source_url: str
    recorded_by: str
    status: str  # "created" | "already_exists" | "updated"


def record_manual_enrichment_evidence(
    workflow_id: str,
    step_name: str,
    field: str,
    value: str,
    source_url: str,
    recorded_by: str,
) -> ManualEvidenceSummary:
    """Validate that the step is planned and approved, then record manual evidence."""
    clean_wid = workflow_id.strip()
    clean_step = step_name.strip()
    clean_field = field.strip()
    clean_val = value.strip()
    clean_url = source_url.strip()
    clean_rec = recorded_by.strip()

    if not clean_wid:
        raise ValueError("workflow-id is required")
    if not clean_step:
        raise ValueError("step-name is required")
    if not clean_field:
        raise ValueError("field is required")
    if not clean_val:
        raise ValueError("value is required")
    if not clean_url:
        raise ValueError("source-url is required")
    if not clean_rec:
        raise ValueError("recorded-by is required")

    db.ensure_schema()

    # 1. Confirm enrichment plan exists
    plan = db.fetch_enrichment_plan(clean_wid)
    if plan is None:
        raise ValueError(f"no enrichment plan found for lead '{clean_wid}'")

    # 2. Confirm step exists in plan
    steps = plan.get("steps") or []
    target_step = next((s for s in steps if s.get("name") == clean_step), None)
    if target_step is None:
        raise ValueError(f"step '{clean_step}' not found in enrichment plan for lead '{clean_wid}'")

    # 3. Refuse paid/provider-only steps while providers are not connected
    if target_step.get("may_cost_money"):
        raise ValueError(
            f"step '{clean_step}' is a paid/provider-only step; provider is not connected"
        )

    # 4. Confirm step has an approval record before accepting evidence
    approvals = db.fetch_enrichment_step_approvals([clean_wid])
    if (clean_wid, clean_step) not in approvals:
        raise ValueError(
            f"step '{clean_step}' has not been approved; human approval is required before recording evidence"
        )

    # 5. Store evidence in dedicated table
    evidence, status = db.record_manual_enrichment_evidence(
        workflow_id=clean_wid,
        step_name=clean_step,
        field=clean_field,
        value=clean_val,
        source_url=clean_url,
        recorded_by=clean_rec,
    )

    return ManualEvidenceSummary(
        workflow_id=clean_wid,
        step_name=clean_step,
        field=clean_field,
        value=clean_val,
        source_url=clean_url,
        recorded_by=clean_rec,
        status=status,
    )


def format_manual_evidence_summary(summary: ManualEvidenceSummary) -> str:
    """Format clean summary for terminal output."""
    lines = [
        "=== Manual Enrichment Evidence Summary ===",
        f"Workflow ID:  {summary.workflow_id}",
        f"Step Name:    {summary.step_name}",
        f"Field:        {summary.field}",
        f"Value:        {summary.value}",
        f"Source URL:   {summary.source_url}",
        f"Recorded By:  {summary.recorded_by}",
        f"Status:       {summary.status}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Record manual enrichment evidence for an approved lead enrichment step."
    )
    parser.add_argument("--workflow-id", required=True, help="Workflow ID of the lead")
    parser.add_argument("--step-name", required=True, help="Approved step name (e.g. website_review)")
    parser.add_argument("--field", required=True, help="Evidence field name (e.g. decision_maker_name)")
    parser.add_argument("--value", required=True, help="Evidence value discovered")
    parser.add_argument("--source-url", required=True, help="Source URL where evidence was found")
    parser.add_argument("--recorded-by", required=True, help="Operator recording the evidence")

    args = parser.parse_args()

    try:
        summary = record_manual_enrichment_evidence(
            workflow_id=args.workflow_id,
            step_name=args.step_name,
            field=args.field,
            value=args.value,
            source_url=args.source_url,
            recorded_by=args.recorded_by,
        )
        print(format_manual_evidence_summary(summary))
        return 0
    except Exception as error:
        print(f"Evidence recording failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
