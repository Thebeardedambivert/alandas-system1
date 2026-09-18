"""Production-grade discovery lead qualification engine for System 1.

Inspects imported leads in PostgreSQL, evaluates layered evidence (venue name,
category, domain type, contact surfaces, signal consistency), scores each lead (0-100),
and persists the qualification status without external side effects or network calls.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import logging
import sys
from typing import Any
from urllib.parse import urlparse

from system_1 import db

logger = logging.getLogger(__name__)

HOSTED_OR_SOCIAL_DOMAINS = {
    "canva.site",
    "canva.com",
    "sumup.link",
    "sumup.store",
    "metro.rest",
    "metro.biz",
    "facebook.com",
    "fb.com",
    "instagram.com",
    "linktr.ee",
    "wixsite.com",
    "business.site",
}

NON_TARGET_KEYWORDS = (
    "wholesaler",
    "großhandel",
    "electrical",
    "elektro",
    "repair",
    "reparatur",
    "werkstatt",
    "car dealer",
    "autohandel",
    "autowerkstatt",
    "medical",
    "arzt",
    "zahnarzt",
    "praxis",
    "legal",
    "anwalt",
    "kanzlei",
    "school",
    "schule",
    "fahrschule",
    "retail",
    "kleidung",
    "modehaus",
    "clothing",
    "shoe",
    "schuhe",
    "supermarket",
    "supermarkt",
    "baumarkt",
    "bauhaus",
    "plumbing",
    "klempner",
    "sanitär",
)

HOSPITALITY_CATEGORIES = (
    "cafe",
    "café",
    "coffee shop",
    "coffee store",
    "espresso bar",
    "coffee roastery",
    "rösterei",
    "bakery",
    "bäckerei",
    "konditorei",
    "bistro",
    "restaurant",
    "brunch",
    "boutique hotel",
    "hotel",
    "patisserie",
    "tea house",
    "teestube",
    "gastronomie",
    "hospitality",
)

HOSPITALITY_NAME_TERMS = (
    "cafe",
    "café",
    "coffee",
    "kaffee",
    "espresso",
    "roastery",
    "rösterei",
    "bakery",
    "bäckerei",
    "bistro",
    "brunch",
    "barista",
    "konditorei",
    "patisserie",
    "hotel",
    "restaurant",
)


@dataclass(frozen=True)
class QualificationResult:
    status: str  # "qualified" | "rejected" | "needs_review"
    score: int
    reasons: list[str]
    evidence: dict[str, Any]


@dataclass(frozen=True)
class QualificationSummary:
    total_inspected: int
    qualified: int
    rejected: int
    needs_review: int
    failed: int


def _clean_domain(domain_or_url: str) -> str:
    val = domain_or_url.strip().lower()
    if not val:
        return ""
    if "://" in val:
        parsed = urlparse(val)
        val = parsed.netloc or parsed.path
    if ":" in val:
        val = val.split(":")[0]
    if val.startswith("www."):
        val = val[4:]
    return val


def evaluate_lead_qualification(lead: dict[str, Any]) -> QualificationResult:
    """Evaluate layered evidence for one lead and return deterministic score and classification.

    Never makes network calls.
    """
    venue_name = str(lead.get("venue_name") or "").strip()
    venue_type = str(lead.get("venue_type") or "").strip()
    website = str(lead.get("website") or "").strip()
    phone = str(lead.get("phone") or "").strip()
    city = str(lead.get("city") or "").strip()
    instagram = str(lead.get("instagram") or "").strip()

    raw_domain = str(lead.get("website_domain") or "") or website
    domain = _clean_domain(raw_domain)

    name_lower = venue_name.lower()
    type_lower = venue_type.lower()

    has_website = bool(website)
    has_phone = bool(phone)
    is_hosted_domain = any(domain == h or domain.endswith("." + h) for h in HOSTED_OR_SOCIAL_DOMAINS)

    evidence: dict[str, Any] = {
        "venue_name": venue_name,
        "venue_type": venue_type,
        "city": city,
        "has_website": has_website,
        "website_domain": domain,
        "is_hosted_or_social_domain": is_hosted_domain,
        "has_phone": has_phone,
        "has_instagram": bool(instagram),
    }

    category_is_non_target = any(k in type_lower for k in NON_TARGET_KEYWORDS)
    name_has_hospitality = any(k in name_lower for k in HOSPITALITY_NAME_TERMS)
    category_is_hospitality = any(k in type_lower for k in HOSPITALITY_CATEGORIES)

    # Policy 1: Conflicting signals or non-target category
    if category_is_non_target:
        if name_has_hospitality:
            # Conflicting signals: name says cafe/hospitality but category is non-target
            return QualificationResult(
                status="needs_review",
                score=55,
                reasons=["conflicting_signal: name contains cafe/hospitality keyword but category is non-target"],
                evidence=evidence,
            )
        # Clear non-target
        return QualificationResult(
            status="rejected",
            score=12,
            reasons=[f"non_target_category: {venue_type or 'unrelated business'}"],
            evidence=evidence,
        )

    # Policy 2: Hospitality Category
    if category_is_hospitality:
        if is_hosted_domain:
            # Hosted / social-only page (Canva, SumUp, Metro, Facebook, Instagram)
            return QualificationResult(
                status="needs_review",
                score=65,
                reasons=["category_hospitality", f"hosted_or_social_domain: {domain}"],
                evidence=evidence,
            )
        if not has_website and has_phone:
            # Missing website with only phone
            return QualificationResult(
                status="needs_review",
                score=55,
                reasons=["category_hospitality", "missing_website_phone_only"],
                evidence=evidence,
            )
        if not has_website and not has_phone:
            # Missing both contact surfaces
            return QualificationResult(
                status="needs_review",
                score=40,
                reasons=["category_hospitality", "missing_contact_surface"],
                evidence=evidence,
            )

        # Standard qualified hospitality venue with custom domain website
        score = 82 if has_phone else 72
        reasons = ["category_hospitality", "custom_domain_website"]
        if has_phone:
            reasons.append("phone_present")
        return QualificationResult(
            status="qualified",
            score=score,
            reasons=reasons,
            evidence=evidence,
        )

    # Policy 3: Plausible hospitality name with vague / unlisted category
    if name_has_hospitality:
        score = 55 if has_website else 45
        return QualificationResult(
            status="needs_review",
            score=score,
            reasons=["weak_category_plausible_hospitality_name"],
            evidence=evidence,
        )

    # Policy 4: No hospitality signal
    return QualificationResult(
        status="rejected",
        score=10,
        reasons=["no_hospitality_signal"],
        evidence=evidence,
    )


def qualify_leads_batch(status: str = "new", limit: int = 50) -> QualificationSummary:
    """Load leads matching status, evaluate qualification, and update DB idempotently."""
    db.ensure_schema()
    leads = db.fetch_leads_by_status(status=status, limit=limit)

    total_inspected = len(leads)
    qualified = 0
    rejected = 0
    needs_review = 0
    failed = 0

    for lead in leads:
        workflow_id = str(lead.get("workflow_id") or "")
        if not workflow_id:
            continue
        try:
            result = evaluate_lead_qualification(lead)
            db.update_lead_qualification(
                workflow_id=workflow_id,
                qualification_status=result.status,
                qualification_score=result.score,
                qualification_reasons=result.reasons,
                qualification_evidence=result.evidence,
            )
            if result.status == "qualified":
                qualified += 1
            elif result.status == "rejected":
                rejected += 1
            elif result.status == "needs_review":
                needs_review += 1
            else:
                failed += 1
        except Exception as error:
            logger.error("Failed to qualify lead %s: %s", workflow_id, error, exc_info=True)
            failed += 1

    return QualificationSummary(
        total_inspected=total_inspected,
        qualified=qualified,
        rejected=rejected,
        needs_review=needs_review,
        failed=failed,
    )


def format_qualification_summary(summary: QualificationSummary) -> str:
    """Format clean, secret-free summary for operators."""
    lines = [
        "=== Discovery Lead Qualification Summary ===",
        f"Total Inspected: {summary.total_inspected}",
        f"Qualified:       {summary.qualified}",
        f"Rejected:        {summary.rejected}",
        f"Needs Review:    {summary.needs_review}",
        f"Failed:          {summary.failed}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Qualify imported discovery leads based on layered evidence."
    )
    parser.add_argument(
        "--status",
        default="new",
        help="Current status of leads to inspect (default: new)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of leads to inspect (default: 50)",
    )
    args = parser.parse_args()

    try:
        summary = qualify_leads_batch(status=args.status, limit=args.limit)
        print(format_qualification_summary(summary))
        return 0 if summary.failed == 0 else 1
    except Exception as error:
        print(f"Qualification run failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
