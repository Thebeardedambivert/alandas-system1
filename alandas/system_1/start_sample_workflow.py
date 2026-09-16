"""Start one sample Alandas System 1 workflow."""

from __future__ import annotations

import asyncio
import os
from uuid import uuid4

from temporalio.client import Client

from system_1.models import LeadInput
from system_1.workflows import CafeLeadWorkflow


async def main() -> None:
    address = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
    namespace = os.environ.get("TEMPORAL_NAMESPACE", "default")
    task_queue = os.environ.get("TEMPORAL_TASK_QUEUE", "alandas-system1")

    client = await Client.connect(address, namespace=namespace)
    lead = LeadInput(
        venue_name="Example Cafe",
        city="Berlin",
        venue_type="cafe",
        website="https://example.de",
        email="hello@example.de",
        source_url="https://example.de",
        seat_estimate=40,
        fit_score=4,
        fit_reason="premium brunch cafe with visible drinks service",
    )
    workflow_id = f"alandas-lead-{uuid4()}"
    handle = await client.start_workflow(
        CafeLeadWorkflow.run,
        lead,
        id=workflow_id,
        task_queue=task_queue,
    )
    print(f"Started workflow: {handle.id}")


if __name__ == "__main__":
    asyncio.run(main())
