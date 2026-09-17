"""Temporal workflows for Alandas System 1."""

from __future__ import annotations

from datetime import timedelta

from temporalio import workflow

from system_1.core import audit_event_key, can_approve_outreach, can_record_send
from system_1.models import LeadInput, LeadWorkflowState

with workflow.unsafe.imports_passed_through():
    from system_1.activities import (
        append_audit_event_activity,
        draft_outreach_activity,
        enrich_lead_activity,
        update_lead_status_activity,
        upsert_lead_activity,
        validate_lead_activity,
    )


@workflow.defn
class CafeLeadWorkflow:
    """Track one cafe lead through Layer 1."""

    def __init__(self) -> None:
        self.state: LeadWorkflowState | None = None

    @workflow.run
    async def run(self, lead: LeadInput) -> LeadWorkflowState:
        self.state = LeadWorkflowState(lead=lead)
        await self._persist_lead()
        await self._audit("lead_started", {"venue_name": lead.venue_name})

        errors = await workflow.execute_activity(
            validate_lead_activity,
            lead,
            start_to_close_timeout=timedelta(seconds=30),
        )
        if errors:
            self.state.status = "needs_research"
            await self._persist_status()
            await self._audit("lead_validation_failed", {"errors": errors})
            return self.state

        self.state.status = "qualified"
        await self._persist_status()
        self.state.enrichment_notes = await workflow.execute_activity(
            enrich_lead_activity,
            lead,
            start_to_close_timeout=timedelta(minutes=2),
        )
        await self._audit("lead_enriched", {"notes": self.state.enrichment_notes})

        self.state.outreach_draft = await workflow.execute_activity(
            draft_outreach_activity,
            lead,
            start_to_close_timeout=timedelta(minutes=2),
        )
        self.state.status = "drafted"
        await self._persist_status()
        await self._audit("outreach_drafted", {"channel": self.state.outreach_draft.channel})

        await workflow.wait_condition(
            lambda: self.state is not None
            and (self.state.sidy_approved or bool(self.state.rejection_reason))
        )

        if self.state.rejection_reason:
            self.state.status = "rejected"
            await self._persist_status()
            await self._audit("lead_rejected", {"reason": self.state.rejection_reason})
            return self.state

        self.state.status = "approved"
        await self._persist_status()
        await self._audit("outreach_approved", {"venue_name": lead.venue_name})

        await workflow.wait_condition(lambda: self.state is not None and self.state.sent_recorded)
        self.state.status = "contacted"
        await self._persist_status()
        await self._audit("send_recorded", {"venue_name": lead.venue_name})

        await workflow.sleep(timedelta(days=4))
        self.state.follow_up_due = True
        self.state.status = "follow_up_due"
        await self._persist_status()
        await self._audit("follow_up_due", {"venue_name": lead.venue_name})
        return self.state

    @workflow.signal
    async def approve_by_sidy(self) -> None:
        if self.state is not None and can_approve_outreach(self.state):
            # A send record is valid only for the draft Sidy has just approved.
            self.state.sidy_approved = True
            self.state.outreach_draft.allowed_to_send = True

    @workflow.signal
    async def reject_by_sidy(self, reason: str) -> None:
        if self.state is not None:
            self.state.rejection_reason = reason

    @workflow.signal
    async def record_sent(self) -> None:
        if self.state is not None and can_record_send(self.state):
            self.state.sent_recorded = True

    @workflow.query
    def current_state(self) -> LeadWorkflowState | None:
        return self.state

    async def _audit(self, name: str, details: dict[str, object]) -> None:
        if self.state is None:
            return
        await workflow.execute_activity(
            append_audit_event_activity,
            {
                "event": name,
                "event_key": audit_event_key(workflow.info().workflow_id, name),
                "workflow_id": workflow.info().workflow_id,
                "status": self.state.status,
                "details": details,
            },
            start_to_close_timeout=timedelta(seconds=30),
        )

    async def _persist_lead(self) -> None:
        if self.state is None:
            return
        await workflow.execute_activity(
            upsert_lead_activity,
            {
                "workflow_id": workflow.info().workflow_id,
                "lead": self.state.lead,
                "status": self.state.status,
            },
            start_to_close_timeout=timedelta(seconds=30),
        )

    async def _persist_status(self) -> None:
        if self.state is None:
            return
        await workflow.execute_activity(
            update_lead_status_activity,
            {
                "workflow_id": workflow.info().workflow_id,
                "status": self.state.status,
            },
            start_to_close_timeout=timedelta(seconds=30),
        )
