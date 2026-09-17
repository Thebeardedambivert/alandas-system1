"""Pure System 1 lead logic.

This module has no Temporal or database imports. That makes it easy to test
before the server exists.
"""

from __future__ import annotations

from dataclasses import replace
from urllib.parse import urlparse

from system_1.models import LeadInput, LeadWorkflowState, OutreachDraft, ResearchEvidence


SAFE_ID_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789")


def audit_event_key(workflow_id: str, event_name: str) -> str:
    """Return the stable key for one workflow transition audit event."""

    if not workflow_id.strip() or not event_name.strip():
        raise ValueError("workflow_id and event_name are required for an audit event")
    return f"{workflow_id}:{event_name}"


def slug(value: str) -> str:
    """Return a stable lowercase slug."""

    output: list[str] = []
    previous_dash = False
    for char in value.lower():
        if char in SAFE_ID_CHARS:
            output.append(char)
            previous_dash = False
        elif not previous_dash:
            output.append("-")
            previous_dash = True
    return "".join(output).strip("-") or "lead"


def lead_workflow_id(lead: LeadInput) -> str:
    """Return the stable workflow ID for a lead."""

    return f"alandas-lead-{slug(lead.city)}-{slug(lead.venue_name)}"


def website_domain(value: str) -> str:
    """Return a normalized website host for deterministic duplicate checks."""

    parsed = urlparse(value.strip())
    host = (parsed.hostname or "").lower().strip(".")
    return host.removeprefix("www.")


def instagram_handle(value: str) -> str:
    """Return a normalized Instagram handle without making a network request."""

    candidate = value.strip().lower()
    if not candidate:
        return ""
    if "://" in candidate:
        parsed = urlparse(candidate)
        if parsed.hostname and parsed.hostname.lower().removeprefix("www.") == "instagram.com":
            candidate = parsed.path.strip("/").split("/", 1)[0]
    return candidate.lstrip("@").strip("/")


def venue_city_key(lead: LeadInput) -> str:
    """Return the fallback identity used when no stronger public identifier exists."""

    return f"{slug(lead.venue_name)}:{slug(lead.city)}"


def normalize_lead(lead: LeadInput) -> LeadInput:
    """Normalize stable identifiers before persistence and duplicate checks."""

    return replace(
        lead,
        venue_name=lead.venue_name.strip(),
        city=lead.city.strip(),
        venue_type=lead.venue_type.strip().lower(),
        source_url=lead.source_url.strip(),
        website=lead.website.strip().rstrip("/"),
        instagram=instagram_handle(lead.instagram),
        email=lead.email.strip().lower(),
        phone=lead.phone.strip(),
        impressum_url=lead.impressum_url.strip().rstrip("/"),
        decision_maker=lead.decision_maker.strip(),
        fit_reason=lead.fit_reason.strip(),
    )


def validate_intake(lead: LeadInput) -> list[str]:
    """Check the minimum fields needed to accept a raw research candidate."""

    errors: list[str] = []
    if not lead.venue_name.strip():
        errors.append("venue_name is required")
    if not lead.city.strip():
        errors.append("city is required")
    if not lead.venue_type.strip():
        errors.append("venue_type is required")
    if not lead.source_url.strip():
        errors.append("source_url is required")
    if lead.fit_score is not None and not 1 <= lead.fit_score <= 5:
        errors.append("fit_score must be between 1 and 5")
    return errors


def validate_lead(lead: LeadInput) -> list[str]:
    """Check whether an enriched lead is ready for outreach drafting."""

    errors = validate_intake(lead)
    if not any([lead.website, lead.instagram, lead.email, lead.phone]):
        errors.append("at least one contact route is required")
    return errors


def apply_research_evidence(
    lead: LeadInput, evidence: list[ResearchEvidence]
) -> LeadInput:
    """Fill only blank public contact fields; existing operator data wins."""

    values = {item.field: item.value for item in evidence if item.value.strip()}
    return replace(
        lead,
        email=lead.email or values.get("email", ""),
        phone=lead.phone or values.get("phone", ""),
        instagram=lead.instagram or values.get("instagram", ""),
        impressum_url=lead.impressum_url or values.get("impressum_url", ""),
    )


def enrich_lead(lead: LeadInput) -> list[str]:
    """Record known lead data and missing research steps."""

    notes: list[str] = []
    if lead.impressum_url:
        notes.append("Impressum source already present")
    else:
        notes.append("Find public Impressum or contact page")

    if lead.email:
        notes.append("Email present, verify before outreach")
    else:
        notes.append("Find email from website, Impressum, or approved tool")

    if lead.phone:
        notes.append("Phone present, confirm WhatsApp suitability manually")
    else:
        notes.append("Phone missing, do not buy mobile lookup without approval")

    if lead.instagram:
        notes.append("Instagram route present")
    else:
        notes.append("Find Instagram profile if available")

    return notes


def draft_outreach(lead: LeadInput) -> OutreachDraft:
    """Create a first-contact draft for Sidy's approval."""

    recipient = lead.decision_maker or lead.venue_name
    body = (
        f"Hi {recipient},\n\n"
        "I am Sidy from Alandas Tea Berlin.\n\n"
        f"I found {lead.venue_name} while looking for cafes that could fit a better "
        "loose-leaf tea service.\n\n"
        "We have a EUR 19 discovery box for cafes. It includes a glass teapot, "
        "bamboo tray, dosing spoon, and 5 tea samples. It lets you test the setup "
        "before making a bigger decision.\n\n"
        "Would you like me to send the details?\n\n"
        "Best,\n"
        "Sidy"
    )
    return OutreachDraft(
        channel="email_or_whatsapp",
        subject=f"Loose-leaf tea setup for {lead.venue_name}",
        body=body,
        allowed_to_send=False,
    )


def can_approve_outreach(state: LeadWorkflowState) -> bool:
    """Return whether Sidy may approve the current, drafted message."""

    return (
        state.status == "drafted"
        and state.outreach_draft is not None
        and not state.rejection_reason
    )


def can_record_send(state: LeadWorkflowState) -> bool:
    """Return whether a recorded send belongs to an approved draft."""

    return (
        state.status == "approved"
        and state.sidy_approved
        and state.outreach_draft is not None
        and state.outreach_draft.allowed_to_send
        and not state.rejection_reason
    )
