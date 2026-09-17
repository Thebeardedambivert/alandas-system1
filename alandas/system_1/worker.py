"""Run the Alandas System 1 Temporal worker."""

from __future__ import annotations

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from system_1.db import ensure_schema
from system_1.activities import (
    append_audit_event_activity,
    draft_outreach_activity,
    enrich_lead_activity,
    find_internal_duplicates_activity,
    normalize_lead_activity,
    research_public_lead_activity,
    update_lead_status_activity,
    upsert_lead_activity,
    validate_intake_activity,
    validate_lead_activity,
)
from system_1.workflows import CafeLeadWorkflow
from system_1.discovery_activities import (
    create_daily_discovery_run_activity,
    submit_daily_discovery_providers_activity,
)
from system_1.discovery_temporal_workflow import DailyDiscoveryWorkflow


logger = logging.getLogger(__name__)


async def connect_temporal_with_retry(
    address: str,
    namespace: str,
    *,
    attempts: int = 60,
    delay_seconds: int = 5,
) -> Client:
    """Connect to Temporal, waiting for the service to become ready."""

    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            logger.info(
                "Connecting to Temporal at %s in namespace %s, attempt %s/%s",
                address,
                namespace,
                attempt,
                attempts,
            )
            return await Client.connect(address, namespace=namespace)
        except Exception as error:
            last_error = error
            logger.warning(
                "Temporal is not ready yet, retrying in %s seconds: %s",
                delay_seconds,
                error,
            )
            await asyncio.sleep(delay_seconds)

    raise RuntimeError("Temporal connection failed after retries") from last_error


async def main() -> None:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "info").upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    address = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
    namespace = os.environ.get("TEMPORAL_NAMESPACE", "default")
    task_queue = os.environ.get("TEMPORAL_TASK_QUEUE", "alandas-system1")

    ensure_schema()
    client = await connect_temporal_with_retry(address, namespace)
    with ThreadPoolExecutor(max_workers=8) as activity_executor:
        worker = Worker(
            client,
            task_queue=task_queue,
            workflows=[CafeLeadWorkflow, DailyDiscoveryWorkflow],
            activities=[
                create_daily_discovery_run_activity,
                submit_daily_discovery_providers_activity,
                validate_lead_activity,
                validate_intake_activity,
                normalize_lead_activity,
                find_internal_duplicates_activity,
                research_public_lead_activity,
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
