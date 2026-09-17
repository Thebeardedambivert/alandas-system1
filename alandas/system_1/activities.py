"""Temporal activities for Alandas System 1.

Activities are allowed to touch files, APIs, and services. The workflow calls
them in small steps so each result can be retried or audited.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from temporalio import activity

from system_1.core import (
    apply_research_evidence,
    audit_event_key,
    draft_outreach,
    enrich_lead,
    normalize_lead,
    validate_intake,
    validate_lead,
)
from system_1 import db
from system_1.models import LeadInput, OutreachDraft, ResearchEvidence
from system_1.public_research import research_public_pages


def _audit_path() -> str:
    return os.environ.get("SYSTEM1_AUDIT_PATH", "/app/runtime/audit/system1_audit.jsonl")


@activity.defn
def validate_lead_activity(lead: LeadInput) -> list[str]:
    """Check the minimum lead fields before drafting starts."""

    return validate_lead(lead)


@activity.defn
def normalize_lead_activity(lead: LeadInput) -> LeadInput:
    """Make stable comparison keys from a raw lead before it is stored."""

    return normalize_lead(lead)


@activity.defn
def validate_intake_activity(lead: LeadInput) -> list[str]:
    """Check fields needed to accept a raw candidate into the waterfall."""

    return validate_intake(lead)


@activity.defn
def find_internal_duplicates_activity(input_data: dict) -> list[dict[str, str]]:
    """Return possible existing records without changing either record."""

    lead = input_data["lead"]
    if isinstance(lead, dict):
        lead = LeadInput(**lead)
    elif not isinstance(lead, LeadInput):
        raise TypeError("lead must be a LeadInput or lead dict")
    return db.find_internal_duplicates(str(input_data["workflow_id"]), lead)


@activity.defn
def research_public_lead_activity(input_data: dict) -> dict:
    """Optionally read bounded public pages and persist source evidence.

    Public fetching is deliberately off unless the deployment explicitly enables
    it. This lets the workflow structure ship and be tested without silently
    starting web traffic from production.
    """

    lead = input_data["lead"]
    if isinstance(lead, dict):
        lead = LeadInput(**lead)
    elif not isinstance(lead, LeadInput):
        raise TypeError("lead must be a LeadInput or lead dict")

    if os.environ.get("SYSTEM1_PUBLIC_RESEARCH_ENABLED", "false").lower() != "true":
        return {
            "lead": lead,
            "evidence": [],
            "notes": ["Public research disabled; no external pages were fetched"],
        }

    evidence, notes = research_public_pages(lead)
    for item in evidence:
        db.insert_research_evidence(str(input_data["workflow_id"]), item)
    return {
        "lead": apply_research_evidence(lead, evidence),
        "evidence": evidence,
        "notes": notes,
    }


@activity.defn
def enrich_lead_activity(lead: LeadInput) -> list[str]:
    """Record known lead data and missing research steps."""

    return enrich_lead(lead)


@activity.defn
def draft_outreach_activity(lead: LeadInput) -> OutreachDraft:
    """Create a first-contact draft for Sidy's approval."""

    return draft_outreach(lead)


@activity.defn
def append_audit_event_activity(event: dict) -> None:
    """Append one transition audit event once, even when Temporal retries it."""

    path = _audit_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    inserted = db.insert_audit_event(
        workflow_id=str(payload["workflow_id"]),
        event_key=audit_event_key(
            str(payload["workflow_id"]), str(payload["event"])
        ),
        event_name=str(payload["event"]),
        status=str(payload["status"]),
        details=dict(payload.get("details") or {}),
    )
    if not inserted:
        return
    with open(path, "a", encoding="utf-8") as audit_file:
        audit_file.write(json.dumps(payload, ensure_ascii=True) + "\n")


@activity.defn
def upsert_lead_activity(input_data: dict) -> None:
    """Persist one lead in Postgres."""

    lead = input_data["lead"]
    if isinstance(lead, dict):
        lead = LeadInput(**lead)
    elif not isinstance(lead, LeadInput):
        raise TypeError("lead must be a LeadInput or lead dict")
    db.upsert_lead(
        workflow_id=str(input_data["workflow_id"]),
        lead=lead,
        status=str(input_data["status"]),
    )


@activity.defn
def update_lead_status_activity(input_data: dict[str, str]) -> None:
    """Persist a lead status change in Postgres."""

    db.update_lead_status(
        workflow_id=input_data["workflow_id"],
        status=input_data["status"],
    )
