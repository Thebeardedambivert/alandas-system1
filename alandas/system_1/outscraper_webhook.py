"""Receive one Outscraper Maps completion callback safely.

The public HTTP server delegates here.  Keeping validation and side effects in
separate functions makes duplicate and malformed deliveries testable without a
network server.
"""

from __future__ import annotations

import hmac
from collections.abc import Awaitable, Callable, Mapping
from typing import TYPE_CHECKING

from system_1.core import lead_workflow_id
from system_1.models import LeadInput
from system_1.outscraper_google_maps import candidate_to_lead, map_outscraper_callback

if TYPE_CHECKING:
    from temporalio.client import Client


WorkflowStarter = Callable[[LeadInput], Awaitable[str]]
AuditWriter = Callable[[str, str, str, str, dict[str, object]], bool]


def validate_webhook_token(provided: str, expected: str) -> None:
    """Require a configured, high-entropy shared callback token."""

    if len(expected) < 32:
        raise RuntimeError("OUTSCRAPER_WEBHOOK_TOKEN must be at least 32 characters")
    if not hmac.compare_digest(provided, expected):
        raise PermissionError("invalid webhook token")


async def receive_outscraper_callback(
    payload: Mapping[str, Any],
    *,
    provided_token: str,
    expected_token: str,
    start_workflow: WorkflowStarter,
    audit_writer: AuditWriter | None = None,
) -> dict[str, object]:
    """Validate, start idempotent lead workflows, then audit one callback.

    The stable workflow ID makes a vendor retry harmless: Temporal rejects a
    second start for the same cafe instead of creating a second outreach path.
    """

    validate_webhook_token(provided_token, expected_token)
    request_id = payload.get("id")
    if not isinstance(request_id, str) or not request_id.strip():
        raise ValueError("Outscraper callback id is required")

    candidates, notes = map_outscraper_callback(payload)
    started = 0
    already_started = 0
    for candidate in candidates:
        result = await start_workflow(candidate_to_lead(candidate))
        if result == "started":
            started += 1
        elif result == "already_started":
            already_started += 1
        else:
            raise RuntimeError(f"unexpected workflow start result: {result}")

    if audit_writer is None:
        from system_1 import db

        audit_writer = db.insert_audit_event
    audit_writer(
        workflow_id=f"outscraper-delivery-{request_id}",
        event_key=f"outscraper:{request_id}:received",
        event_name="outscraper_callback_received",
        status="accepted",
        details={
            "source": "outscraper_google_maps",
            "candidate_count": len(candidates),
            "started": started,
            "already_started": already_started,
            "skipped": len(notes),
        },
    )
    return {
        "request_id": request_id,
        "accepted": len(candidates),
        "started": started,
        "already_started": already_started,
        "skipped": len(notes),
    }


def temporal_workflow_starter(client: "Client", task_queue: str) -> WorkflowStarter:
    """Build a callback-safe Temporal starter for the ingress service."""

    from system_1.workflows import CafeLeadWorkflow

    async def start(lead: LeadInput) -> str:
        try:
            await client.start_workflow(
                CafeLeadWorkflow.run,
                lead,
                id=lead_workflow_id(lead),
                task_queue=task_queue,
            )
            return "started"
        except Exception as error:
            # Temporal's exact exception import has changed across SDK versions.
            # Only the documented duplicate-start case is treated as harmless.
            if error.__class__.__name__ == "WorkflowAlreadyStartedError":
                return "already_started"
            raise

    return start
