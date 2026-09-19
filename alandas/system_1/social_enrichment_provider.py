"""Safe, disabled-by-default provider adapters and dry-run planner for Firecrawl & Apify.

Zero network calls by default. Strictly bounded by credit and cost caps.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from decimal import Decimal
import os
import sys
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse

from system_1 import db
from system_1.provider_http import HttpResponse, HttpTransport, UrllibHttpTransport


# ---------------------------------------------------------------------------
# Provider Configurations & Safety Guards
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FirecrawlConfig:
    api_key: str
    enabled: bool = False
    max_credits_per_run: int = 50
    max_pages_per_lead: int = 5

    @classmethod
    def from_env(cls) -> "FirecrawlConfig":
        enabled = os.environ.get("SYSTEM1_FIRECRAWL_ENABLED", "").lower() in {"1", "true", "yes"}
        api_key = os.environ.get("FIRECRAWL_API_KEY", "")
        max_credits = int(os.environ.get("SYSTEM1_FIRECRAWL_MAX_CREDITS_PER_RUN", "50"))
        max_pages = int(os.environ.get("SYSTEM1_FIRECRAWL_MAX_PAGES_PER_LEAD", "5"))
        if max_credits <= 0:
            raise ValueError("Firecrawl max credits per run must be positive")
        if max_pages <= 0:
            raise ValueError("Firecrawl max pages per lead must be positive")
        return cls(
            api_key=api_key,
            enabled=enabled,
            max_credits_per_run=max_credits,
            max_pages_per_lead=max_pages,
        )


@dataclass(frozen=True)
class ApifyEnrichmentConfig:
    api_token: str
    enabled: bool = False
    max_cost_usd: Decimal = Decimal("1.00")
    max_results_per_actor: int = 10
    instagram_profile_actors: tuple[str, ...] = ()
    facebook_page_actors: tuple[str, ...] = ()
    people_fallback_actors: tuple[str, ...] = ()

    @classmethod
    def from_env(cls) -> "ApifyEnrichmentConfig":
        enabled = os.environ.get("SYSTEM1_APIFY_ENRICHMENT_ENABLED", "").lower() in {"1", "true", "yes"}
        token = os.environ.get("APIFY_API_TOKEN", "")
        max_cost = Decimal(os.environ.get("SYSTEM1_APIFY_ENRICHMENT_MAX_COST_USD", "1.00"))
        max_results = int(os.environ.get("SYSTEM1_APIFY_ENRICHMENT_MAX_RESULTS_PER_ACTOR", "10"))
        if max_cost <= Decimal("0.00"):
            raise ValueError("Apify enrichment max cost must be positive")
        if max_results <= 0:
            raise ValueError("Apify enrichment max results must be positive")

        def parse_actors(env_var: str) -> tuple[str, ...]:
            raw = os.environ.get(env_var, "").strip()
            if not raw:
                return ()
            actors = [a.strip() for a in raw.split(",") if a.strip()]
            for a in actors:
                if len(a) > 100:
                    raise ValueError(f"Actor ID '{a}' is excessively long")
            return tuple(actors)

        return cls(
            api_token=token,
            enabled=enabled,
            max_cost_usd=max_cost,
            max_results_per_actor=max_results,
            instagram_profile_actors=parse_actors("SYSTEM1_APIFY_INSTAGRAM_PROFILE_ACTORS"),
            facebook_page_actors=parse_actors("SYSTEM1_APIFY_FACEBOOK_PAGE_ACTORS"),
            people_fallback_actors=parse_actors("SYSTEM1_APIFY_PEOPLE_FALLBACK_ACTORS"),
        )


# ---------------------------------------------------------------------------
# Provider Adapters (Safe & Disabled by Default)
# ---------------------------------------------------------------------------

class FirecrawlAdapter:
    """Safe adapter for Firecrawl web scraping. Enforces disabled switch and credit caps."""

    def __init__(self, config: FirecrawlConfig, transport: HttpTransport | None = None) -> None:
        self.config = config
        self._transport = transport or UrllibHttpTransport()

    def scrape_url(self, target_url: str, pages_limit: int | None = None) -> HttpResponse:
        if not self.config.enabled:
            raise RuntimeError("Firecrawl enrichment is disabled (SYSTEM1_FIRECRAWL_ENABLED=false)")
        if not self.config.api_key:
            raise ValueError("FIRECRAWL_API_KEY is missing but Firecrawl is enabled")
        limit = pages_limit or self.config.max_pages_per_lead
        if limit > self.config.max_pages_per_lead:
            raise ValueError(f"Requested pages ({limit}) exceeds configured max pages ({self.config.max_pages_per_lead})")
        if self.config.max_credits_per_run <= 0:
            raise ValueError("Firecrawl max credits limit exceeded")

        return self._transport.request(
            method="POST",
            url="https://api.firecrawl.dev/v1/scrape",
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            body=f'{{"url": "{target_url}", "pageOptions": {{"limit": {limit}}}}}'.encode("utf-8"),
            timeout_seconds=30,
        )


class ApifyEnrichmentAdapter:
    """Safe adapter for Apify social and people enrichment actors."""

    def __init__(self, config: ApifyEnrichmentConfig, transport: HttpTransport | None = None) -> None:
        self.config = config
        self._transport = transport or UrllibHttpTransport()

    def run_actor(
        self,
        actor_id: str,
        group: str,
        input_data: dict[str, Any],
        estimated_cost_usd: Decimal,
        approved_by: str | None = None,
    ) -> HttpResponse:
        if not self.config.enabled:
            raise RuntimeError("Apify enrichment is disabled (SYSTEM1_APIFY_ENRICHMENT_ENABLED=false)")
        if not self.config.api_token:
            raise ValueError("APIFY_API_TOKEN is missing but Apify enrichment is enabled")
        if estimated_cost_usd > self.config.max_cost_usd:
            raise ValueError(
                f"Estimated cost (${estimated_cost_usd:.2f}) exceeds configured max cost (${self.config.max_cost_usd:.2f})"
            )

        # People/email/phone fallback actors are hard-blocked unless explicitly approved
        if group == "people_fallback":
            if not approved_by:
                raise ValueError("People fallback actors are blocked by default; explicit approval is required")

        return self._transport.request(
            method="POST",
            url=f"https://api.apify.com/v2/acts/{actor_id}/runs?maxTotalChargeUsd={estimated_cost_usd:.2f}",
            headers={
                "Authorization": f"Bearer {self.config.api_token}",
                "Content-Type": "application/json",
            },
            body=b"{}",
            timeout_seconds=30,
        )


# ---------------------------------------------------------------------------
# Dry-Run Enrichment Routing Logic
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PlannedEnrichmentAction:
    provider: str
    target_type: str
    target_value: str
    actor_id: str = ""
    status: str = "would_route"
    reason: str = ""


def plan_lead_provider_routing(
    lead: dict[str, Any],
    firecrawl_config: FirecrawlConfig,
    apify_config: ApifyEnrichmentConfig,
) -> list[PlannedEnrichmentAction]:
    """Determine provider enrichment routes for a single lead without calling providers."""
    actions: list[PlannedEnrichmentAction] = []

    website = str(lead.get("website") or "").strip()
    instagram = str(lead.get("instagram") or "").strip()
    source_url = str(lead.get("source_url") or "").strip()

    # Detect Facebook URL if in website or source_url
    facebook_url = ""
    for candidate in [website, source_url]:
        if "facebook.com" in candidate.lower():
            facebook_url = candidate
            break

    # 1. Firecrawl Route: Custom Website (target website / impressum / contact / menu)
    is_custom_website = bool(website and "instagram.com" not in website.lower() and "facebook.com" not in website.lower())
    if is_custom_website:
        actions.append(
            PlannedEnrichmentAction(
                provider="firecrawl",
                target_type="website_pages",
                target_value=website,
                reason="Target website, impressum, contact, and menu pages for business signals",
            )
        )

    # 2. Apify Instagram Actor Group
    # Only runs when an Instagram URL/handle is present
    has_instagram = bool(instagram or "instagram.com" in website.lower())
    if has_instagram:
        actor = apify_config.instagram_profile_actors[0] if apify_config.instagram_profile_actors else "unregistered_instagram_actor"
        target = instagram or website
        actions.append(
            PlannedEnrichmentAction(
                provider="apify_instagram",
                target_type="instagram_profile",
                target_value=target,
                actor_id=actor,
                reason="Extract profile metadata, bio contact details, and activity signals",
            )
        )

    # 3. Apify Facebook Actor Group
    # Only runs when Facebook page URL is present
    if facebook_url:
        actor = apify_config.facebook_page_actors[0] if apify_config.facebook_page_actors else "unregistered_facebook_actor"
        actions.append(
            PlannedEnrichmentAction(
                provider="apify_facebook",
                target_type="facebook_page",
                target_value=facebook_url,
                actor_id=actor,
                reason="Extract official business page details, email, and opening hours",
            )
        )

    # 4. If no social URL is present, no social actor call: needs operator review
    if not has_instagram and not facebook_url and not is_custom_website:
        actions.append(
            PlannedEnrichmentAction(
                provider="none",
                target_type="no_social_url",
                target_value="",
                status="needs_operator_review",
                reason="No custom website or social URL present; requires operator review or approved search mode",
            )
        )

    # 5. People / Fallback Actor Group: Always blocked by default
    if apify_config.people_fallback_actors:
        for actor in apify_config.people_fallback_actors:
            actions.append(
                PlannedEnrichmentAction(
                    provider="apify_people_fallback",
                    target_type="email_phone_fallback",
                    target_value="",
                    actor_id=actor,
                    status="blocked_by_default",
                    reason="People/email/phone fallback actors are blocked by default unless explicitly approved",
                )
            )

    return actions


@dataclass(frozen=True)
class ProviderPlanningSummary:
    leads_inspected: int
    firecrawl_routes: int
    instagram_routes: int
    facebook_routes: int
    people_fallback_blocked: int
    needs_operator_review: int


def format_provider_planning_summary(summary: ProviderPlanningSummary) -> str:
    lines = [
        "=== Provider Enrichment Planning Summary ===",
        f"Leads Inspected:           {summary.leads_inspected}",
        f"Firecrawl Website Routes:  {summary.firecrawl_routes}",
        f"Instagram Actor Routes:    {summary.instagram_routes}",
        f"Facebook Actor Routes:     {summary.facebook_routes}",
        f"People Fallback Blocked:   {summary.people_fallback_blocked}",
        f"Needs Operator Review:     {summary.needs_operator_review}",
    ]
    return "\n".join(lines)


def render_provider_planning_report(
    leads: Sequence[dict[str, Any]],
    firecrawl_config: FirecrawlConfig,
    apify_config: ApifyEnrichmentConfig,
) -> tuple[str, ProviderPlanningSummary]:
    lead_blocks: list[str] = []
    fc_count = 0
    ig_count = 0
    fb_count = 0
    fallback_count = 0
    review_count = 0

    for lead in leads:
        wid = str(lead.get("workflow_id") or "")
        venue = str(lead.get("venue_name") or "(unknown venue)")
        city = str(lead.get("city") or "")
        lines = [
            f"=== Lead: {wid} ===",
            f"Venue: {venue} ({city})",
            "Provider Routing Actions:",
        ]
        actions = plan_lead_provider_routing(lead, firecrawl_config, apify_config)
        if not actions:
            lines.append("  (none)")
        for idx, act in enumerate(actions, start=1):
            lines.append(f"  {idx}. Provider: {act.provider} -> {act.status}")
            lines.append(f"     - Target: {act.target_type} ({act.target_value or 'none'})")
            if act.actor_id:
                lines.append(f"     - Actor ID: {act.actor_id}")
            lines.append(f"     - Reason: {act.reason}")

            if act.provider == "firecrawl":
                fc_count += 1
            elif act.provider == "apify_instagram":
                ig_count += 1
            elif act.provider == "apify_facebook":
                fb_count += 1
            elif act.provider == "apify_people_fallback":
                fallback_count += 1
            elif act.status == "needs_operator_review":
                review_count += 1

        lead_blocks.append("\n".join(lines))

    summary = ProviderPlanningSummary(
        leads_inspected=len(leads),
        firecrawl_routes=fc_count,
        instagram_routes=ig_count,
        facebook_routes=fb_count,
        people_fallback_blocked=fallback_count,
        needs_operator_review=review_count,
    )

    full_output = "\n\n".join(lead_blocks)
    if full_output:
        full_output += "\n\n"
    full_output += format_provider_planning_summary(summary)
    return full_output, summary


def plan_provider_enrichment(
    statuses: Sequence[str] = ("qualified", "needs_review"),
    limit: int = 50,
) -> ProviderPlanningSummary:
    """Read leads from DB and preview provider routing without making network calls."""
    db.ensure_schema()
    leads = db.fetch_leads_for_enrichment_planning(statuses=statuses, limit=limit)
    fc_config = FirecrawlConfig.from_env()
    apify_config = ApifyEnrichmentConfig.from_env()
    report, summary = render_provider_planning_report(leads, fc_config, apify_config)
    print(report)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run planner previewing Firecrawl and Apify social enrichment routing."
    )
    parser.add_argument(
        "--statuses",
        nargs="+",
        default=["qualified", "needs_review"],
        help="Qualification statuses to inspect (default: qualified needs_review)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of leads to inspect (default: 50)",
    )
    args = parser.parse_args()

    try:
        plan_provider_enrichment(statuses=args.statuses, limit=args.limit)
        return 0
    except Exception as error:
        print(f"Provider planning failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
