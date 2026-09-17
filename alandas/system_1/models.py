"""Shared data models for Alandas System 1."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LeadInput:
    """A cafe lead entering the Layer 1 workflow."""

    venue_name: str
    city: str
    venue_type: str
    source_url: str
    website: str = ""
    instagram: str = ""
    email: str = ""
    phone: str = ""
    impressum_url: str = ""
    decision_maker: str = ""
    seat_estimate: int | None = None
    fit_score: int | None = None
    fit_reason: str = ""


@dataclass
class OutreachDraft:
    """A draft that must be approved by Sidy before customer contact."""

    channel: str
    subject: str
    body: str
    allowed_to_send: bool = False


@dataclass(frozen=True)
class ResearchEvidence:
    """One public business-data finding and the page that supports it."""

    field: str
    value: str
    source_url: str
    method: str


@dataclass
class LeadWorkflowState:
    """Current state for one cafe lead."""

    lead: LeadInput
    status: str = "new"
    enrichment_notes: list[str] = field(default_factory=list)
    research_evidence: list[ResearchEvidence] = field(default_factory=list)
    outreach_draft: OutreachDraft | None = None
    sidy_approved: bool = False
    sent_recorded: bool = False
    rejection_reason: str = ""
    follow_up_due: bool = False
