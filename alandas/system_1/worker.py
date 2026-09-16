"""Run the Alandas System 1 Temporal worker."""

from __future__ import annotations

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from system_1.activities import (
    append_audit_event_activity,
    draft_outreach_activity,
    enrich_lead_activity,
    update_lead_status_activity,
    upsert_lead_activity,
    validate_lead_activity,
)
from system_1.workflows import CafeLeadWorkflow


async def main() -> None:
    address = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
    namespace = os.environ.get("TEMPORAL_NAMESPACE", "default")
    task_queue = os.environ.get("TEMPORAL_TASK_QUEUE", "alandas-system1")

    client = await Client.connect(address, namespace=namespace)
    with ThreadPoolExecutor(max_workers=8) as activity_executor:
        worker = Worker(
            client,
            task_queue=task_queue,
            workflows=[CafeLeadWorkflow],
            activities=[
                validate_lead_activity,
                enrich_lead_activity,
                draft_outreach_activity,
                append_audit_event_activity,
                upsert_lead_activity,
                update_lead_status_activity,
            ],
            activity_executor=activity_executor,
        )
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
