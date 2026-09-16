"""Import a lead CSV and start one Temporal workflow per lead."""

from __future__ import annotations

import asyncio
import csv
import os
import sys
from pathlib import Path

from temporalio.client import Client

from system_1.core import lead_workflow_id, validate_lead
from system_1.models import LeadInput
from system_1.workflows import CafeLeadWorkflow


def row_to_lead(row: dict[str, str]) -> LeadInput:
    """Convert one CSV row to a lead input."""

    seat_estimate_raw = row.get("seat_estimate", "").strip()
    fit_score_raw = row.get("fit_score", "").strip()
    return LeadInput(
        venue_name=row.get("venue_name", "").strip(),
        city=row.get("city", "").strip(),
        venue_type=row.get("venue_type", "").strip(),
        website=row.get("website", "").strip(),
        instagram=row.get("instagram", "").strip(),
        email=row.get("email", "").strip(),
        phone=row.get("phone", "").strip(),
        impressum_url=row.get("impressum_url", "").strip(),
        decision_maker=row.get("decision_maker", "").strip(),
        seat_estimate=int(seat_estimate_raw) if seat_estimate_raw else None,
        fit_score=int(fit_score_raw) if fit_score_raw else None,
        fit_reason=row.get("fit_reason", "").strip(),
        source_url=row.get("source_url", "").strip(),
    )


async def import_csv(path: Path) -> int:
    """Start workflows for every valid lead in a CSV file."""

    address = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
    namespace = os.environ.get("TEMPORAL_NAMESPACE", "default")
    task_queue = os.environ.get("TEMPORAL_TASK_QUEUE", "alandas-system1")
    client = await Client.connect(address, namespace=namespace)

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            print("CSV has no header row")
            return 1

        started = 0
        failed = 0
        for row_number, row in enumerate(reader, start=2):
            try:
                lead = row_to_lead(row)
            except ValueError as error:
                print(f"row {row_number}: invalid number field: {error}")
                failed += 1
                continue

            errors = validate_lead(lead)
            if errors:
                print(f"row {row_number}: skipped: {'; '.join(errors)}")
                failed += 1
                continue

            workflow_id = lead_workflow_id(lead)
            try:
                await client.start_workflow(
                    CafeLeadWorkflow.run,
                    lead,
                    id=workflow_id,
                    task_queue=task_queue,
                )
            except Exception as error:
                print(f"row {row_number}: failed to start {workflow_id}: {error}")
                failed += 1
                continue

            print(f"started {workflow_id}")
            started += 1

    print(f"import complete: started={started}, failed={failed}")
    return 0 if failed == 0 else 1


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m system_1.import_leads path/to/leads.csv")
        return 2

    return asyncio.run(import_csv(Path(sys.argv[1])))


if __name__ == "__main__":
    raise SystemExit(main())
