"""Pure System 1 lead logic.

This module has no Temporal or database imports. That makes it easy to test
before the server exists.
"""

from __future__ import annotations

from system_1.models import LeadInput, LeadWorkflowState, OutreachDraft


SAFE_ID_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789")


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


def validate_lead(lead: LeadInput) -> list[str]:
    """Check the minimum lead fields before drafting starts."""

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
    if not any([lead.website, lead.instagram, lead.email, lead.phone]):
        errors.append("at least one contact route is required")
    return errors


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
