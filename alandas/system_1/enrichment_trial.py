"""Local-only enrichment trial command and controlled 10-lead trial path for System 1.

Operates in dry-run mode by default. Enforces strict safety gates:
- Max 10 leads in controlled trial mode
- Hard stop on budget/credit caps
- Public URL and actor ID validation
- Zero live provider calls unless explicitly configured and enabled
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from decimal import Decimal
import socket
import sys
from typing import Any, Callable, Sequence

from system_1 import db
from system_1.provider_http import HttpTransport, UrllibHttpTransport
from system_1.social_enrichment_provider import (
    ApifyEnrichmentAdapter,
    ApifyEnrichmentConfig,
    EnrichmentStatus,
    FirecrawlAdapter,
    FirecrawlConfig,
    PlannedEnrichmentAction,
    ProviderExecutionResult,
    normalize_and_validate_actor_id,
    plan_lead_provider_routing,
    validate_scrape_target_url,
)


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StepTrialDecision:
    workflow_id: str
    provider: str
    step_name: str
    target_value: str
    decision: str
    reason: str
    estimated_cost_usd: Decimal = Decimal("0.00")
    actor_id: str = ""


@dataclass(frozen=True)
class LeadTrialResult:
    workflow_id: str
    venue_name: str
    city: str
    step_decisions: list[StepTrialDecision]
    total_estimated_cost_usd: Decimal = Decimal("0.00")


@dataclass(frozen=True)
class EnrichmentTrialSummary:
    leads_inspected: int
    provider_steps_planned: int
    steps_skipped_disabled: int
    steps_blocked_missing_approval: int
    steps_blocked_cost_cap: int
    steps_would_call_provider: int
    estimated_max_spend_usd: Decimal


# ---------------------------------------------------------------------------
# Evaluation Logic
# ---------------------------------------------------------------------------

def evaluate_lead_trial_steps(
    lead: dict[str, Any],
    approvals: dict[tuple[str, str], dict[str, Any]],
    firecrawl_config: FirecrawlConfig,
    apify_config: ApifyEnrichmentConfig,
    max_total_budget: Decimal,
    current_total_estimated: Decimal,
    step_estimated_cost: Decimal | None = None,
    resolver: Callable[..., list[tuple]] = socket.getaddrinfo,
) -> LeadTrialResult:
    """Evaluate provider trial routing and safety gates for one lead."""
    workflow_id = str(lead.get("workflow_id") or "")
    venue_name = str(lead.get("venue_name") or "(unknown venue)")
    city = str(lead.get("city") or "")

    planned_routes = plan_lead_provider_routing(lead, firecrawl_config, apify_config)
    decisions: list[StepTrialDecision] = []
    lead_estimated_cost = Decimal("0.00")

    for route in planned_routes:
        provider = route.provider
        target = route.target_value
        actor = route.actor_id

        # Determine step name
        if provider == "firecrawl":
            step_name = "website_review"
            cost_usd = Decimal("0.00")
        elif provider == "apify_instagram":
            step_name = "instagram_review"
            cost_usd = step_estimated_cost or Decimal("0.50")
        elif provider == "apify_facebook":
            step_name = "facebook_review"
            cost_usd = step_estimated_cost or Decimal("0.50")
        elif provider == "apify_people_fallback":
            step_name = "people_fallback"
            cost_usd = step_estimated_cost or Decimal("0.50")
        else:
            step_name = route.target_type
            cost_usd = Decimal("0.00")

        # Check approval requirement
        approval = approvals.get((workflow_id, step_name))
        is_approved = approval is not None

        # Route-specific evaluations
        if route.status == "needs_operator_review":
            decisions.append(
                StepTrialDecision(
                    workflow_id=workflow_id,
                    provider=provider,
                    step_name=step_name,
                    target_value=target,
                    decision="needs_operator_review",
                    reason=route.reason,
                    estimated_cost_usd=cost_usd,
                    actor_id=actor,
                )
            )
            continue

        if route.status == "blocked_by_default" and not is_approved:
            decisions.append(
                StepTrialDecision(
                    workflow_id=workflow_id,
                    provider=provider,
                    step_name=step_name,
                    target_value=target,
                    decision="blocked_missing_approval",
                    reason="People fallback is blocked by default; explicit operator approval required",
                    estimated_cost_usd=cost_usd,
                    actor_id=actor,
                )
            )
            continue

        # 1. Check provider enabled flag
        if provider == "firecrawl" and not firecrawl_config.enabled:
            decisions.append(
                StepTrialDecision(
                    workflow_id=workflow_id,
                    provider=provider,
                    step_name=step_name,
                    target_value=target,
                    decision="skipped_disabled",
                    reason="Firecrawl enrichment is disabled (SYSTEM1_FIRECRAWL_ENABLED=false)",
                    estimated_cost_usd=Decimal("0.00"),
                    actor_id=actor,
                )
            )
            continue

        if provider.startswith("apify_") and not apify_config.enabled:
            decisions.append(
                StepTrialDecision(
                    workflow_id=workflow_id,
                    provider=provider,
                    step_name=step_name,
                    target_value=target,
                    decision="skipped_disabled",
                    reason="Apify enrichment is disabled (SYSTEM1_APIFY_ENRICHMENT_ENABLED=false)",
                    estimated_cost_usd=Decimal("0.00"),
                    actor_id=actor,
                )
            )
            continue

        # 2. Check API keys / tokens
        if provider == "firecrawl" and not firecrawl_config.api_key:
            decisions.append(
                StepTrialDecision(
                    workflow_id=workflow_id,
                    provider=provider,
                    step_name=step_name,
                    target_value=target,
                    decision="blocked_missing_key",
                    reason="FIRECRAWL_API_KEY is missing from environment",
                    estimated_cost_usd=Decimal("0.00"),
                    actor_id=actor,
                )
            )
            continue

        if provider.startswith("apify_") and not apify_config.api_token:
            decisions.append(
                StepTrialDecision(
                    workflow_id=workflow_id,
                    provider=provider,
                    step_name=step_name,
                    target_value=target,
                    decision="blocked_missing_key",
                    reason="APIFY_API_TOKEN is missing from environment",
                    estimated_cost_usd=Decimal("0.00"),
                    actor_id=actor,
                )
            )
            continue

        # 3. Target URL validation (Firecrawl)
        if provider == "firecrawl":
            try:
                validate_scrape_target_url(target, resolver=resolver)
            except ValueError as err:
                decisions.append(
                    StepTrialDecision(
                        workflow_id=workflow_id,
                        provider=provider,
                        step_name=step_name,
                        target_value=target,
                        decision="blocked_invalid_url",
                        reason=f"Target URL failed safety validation: {err}",
                        estimated_cost_usd=Decimal("0.00"),
                        actor_id=actor,
                    )
                )
                continue

        # 4. Actor ID normalization and validation (Apify)
        if provider.startswith("apify_") and actor:
            try:
                actor = normalize_and_validate_actor_id(actor)
            except ValueError as err:
                decisions.append(
                    StepTrialDecision(
                        workflow_id=workflow_id,
                        provider=provider,
                        step_name=step_name,
                        target_value=target,
                        decision="blocked_invalid_actor",
                        reason=f"Actor ID validation failed: {err}",
                        estimated_cost_usd=Decimal("0.00"),
                        actor_id=actor,
                    )
                )
                continue

        # 5. Cost and credit cap checks
        if provider == "firecrawl":
            pages_requested = firecrawl_config.max_pages_per_lead
            if pages_requested > firecrawl_config.max_credits_per_run:
                decisions.append(
                    StepTrialDecision(
                        workflow_id=workflow_id,
                        provider=provider,
                        step_name=step_name,
                        target_value=target,
                        decision="blocked_cost_cap",
                        reason=f"Requested pages ({pages_requested}) exceeds max credits ({firecrawl_config.max_credits_per_run})",
                        estimated_cost_usd=Decimal("0.00"),
                        actor_id=actor,
                    )
                )
                continue

        if provider.startswith("apify_"):
            if cost_usd > apify_config.max_cost_usd:
                decisions.append(
                    StepTrialDecision(
                        workflow_id=workflow_id,
                        provider=provider,
                        step_name=step_name,
                        target_value=target,
                        decision="blocked_cost_cap",
                        reason=f"Estimated step cost (${cost_usd:.2f}) exceeds Apify cap (${apify_config.max_cost_usd:.2f})",
                        estimated_cost_usd=Decimal("0.00"),
                        actor_id=actor,
                    )
                )
                continue

            if current_total_estimated + lead_estimated_cost + cost_usd > max_total_budget:
                decisions.append(
                    StepTrialDecision(
                        workflow_id=workflow_id,
                        provider=provider,
                        step_name=step_name,
                        target_value=target,
                        decision="blocked_cost_cap",
                        reason=f"Total estimated trial spend (${current_total_estimated + lead_estimated_cost + cost_usd:.2f}) exceeds trial budget cap (${max_total_budget:.2f})",
                        estimated_cost_usd=Decimal("0.00"),
                        actor_id=actor,
                    )
                )
                continue

        # Step passes all safety checks
        lead_estimated_cost += cost_usd
        decisions.append(
            StepTrialDecision(
                workflow_id=workflow_id,
                provider=provider,
                step_name=step_name,
                target_value=target,
                decision="would_call_provider",
                reason="All provider safety gates passed; ready for trial execution",
                estimated_cost_usd=cost_usd,
                actor_id=actor,
            )
        )

    return LeadTrialResult(
        workflow_id=workflow_id,
        venue_name=venue_name,
        city=city,
        step_decisions=decisions,
        total_estimated_cost_usd=lead_estimated_cost,
    )


# ---------------------------------------------------------------------------
# Reporting & Formatting
# ---------------------------------------------------------------------------

def format_lead_trial_result(result: LeadTrialResult) -> str:
    lines = [
        f"=== Lead: {result.workflow_id} ===",
        f"Venue: {result.venue_name} ({result.city})",
        f"Estimated Lead Spend: ${result.total_estimated_cost_usd:.2f}",
        "Trial Step Decisions:",
    ]
    if not result.step_decisions:
        lines.append("  (none)")
    else:
        for idx, step in enumerate(result.step_decisions, start=1):
            lines.append(f"  {idx}. Provider: {step.provider} ({step.step_name}) -> {step.decision}")
            lines.append(f"     - Target: {step.target_value or 'none'}")
            if step.actor_id:
                lines.append(f"     - Actor ID: {step.actor_id}")
            lines.append(f"     - Reason: {step.reason}")
            lines.append(f"     - Estimated Cost: ${step.estimated_cost_usd:.2f}")

    return "\n".join(lines)


def format_enrichment_trial_summary(summary: EnrichmentTrialSummary) -> str:
    lines = [
        "=== Enrichment Trial Summary ===",
        f"Leads Inspected:                 {summary.leads_inspected}",
        f"Provider Steps Planned:          {summary.provider_steps_planned}",
        f"Steps Skipped Because Disabled:  {summary.steps_skipped_disabled}",
        f"Steps Blocked Missing Approval:  {summary.steps_blocked_missing_approval}",
        f"Steps Blocked by Cost Cap:       {summary.steps_blocked_cost_cap}",
        f"Steps That Would Call Providers: {summary.steps_would_call_provider}",
        f"Estimated Maximum Spend:         ${summary.estimated_max_spend_usd:.2f}",
    ]
    return "\n".join(lines)


def render_enrichment_trial_report(
    results: Sequence[LeadTrialResult],
) -> tuple[str, EnrichmentTrialSummary]:
    leads_inspected = len(results)
    total_steps = 0
    skipped_disabled = 0
    blocked_approval = 0
    blocked_cost = 0
    would_call = 0
    total_spend = Decimal("0.00")

    blocks: list[str] = []
    for r in results:
        blocks.append(format_lead_trial_result(r))
        total_spend += r.total_estimated_cost_usd
        for step in r.step_decisions:
            total_steps += 1
            if step.decision == "skipped_disabled":
                skipped_disabled += 1
            elif step.decision == "blocked_missing_approval":
                blocked_approval += 1
            elif step.decision == "blocked_cost_cap":
                blocked_cost += 1
            elif step.decision == "would_call_provider":
                would_call += 1

    summary = EnrichmentTrialSummary(
        leads_inspected=leads_inspected,
        provider_steps_planned=total_steps,
        steps_skipped_disabled=skipped_disabled,
        steps_blocked_missing_approval=blocked_approval,
        steps_blocked_cost_cap=blocked_cost,
        steps_would_call_provider=would_call,
        estimated_max_spend_usd=total_spend,
    )

    full_text = "\n\n".join(blocks)
    if full_text:
        full_text += "\n\n"
    full_text += format_enrichment_trial_summary(summary)
    return full_text, summary


# ---------------------------------------------------------------------------
# Command Runner
# ---------------------------------------------------------------------------

def run_enrichment_trial(
    statuses: Sequence[str] = ("qualified", "needs_review"),
    limit: int = 10,
    dry_run: bool = True,
    execute: bool = False,
    max_total_budget_usd: Decimal | None = None,
    firecrawl_config: FirecrawlConfig | None = None,
    apify_config: ApifyEnrichmentConfig | None = None,
    transport: HttpTransport | None = None,
    resolver: Callable[..., list[tuple]] = socket.getaddrinfo,
) -> EnrichmentTrialSummary:
    """Execute local-only enrichment trial for up to 10 leads."""
    if limit > 10:
        raise ValueError(f"Controlled trial mode enforces a maximum limit of 10 leads (requested: {limit})")
    if limit <= 0:
        raise ValueError("Limit must be positive")

    max_budget = max_total_budget_usd if max_total_budget_usd is not None else Decimal("5.00")
    fc_config = firecrawl_config or FirecrawlConfig.from_env()
    ap_config = apify_config or ApifyEnrichmentConfig.from_env()
    active_transport = transport or UrllibHttpTransport()

    db.ensure_schema()
    leads = db.fetch_leads_for_enrichment_planning(statuses=statuses, limit=limit)
    workflow_ids = [str(l["workflow_id"]) for l in leads if l.get("workflow_id")]
    approvals = db.fetch_enrichment_step_approvals(workflow_ids)

    results: list[LeadTrialResult] = []
    current_total_estimated = Decimal("0.00")

    for lead in leads:
        res = evaluate_lead_trial_steps(
            lead=lead,
            approvals=approvals,
            firecrawl_config=fc_config,
            apify_config=ap_config,
            max_total_budget=max_budget,
            current_total_estimated=current_total_estimated,
            resolver=resolver,
        )
        current_total_estimated += res.total_estimated_cost_usd
        results.append(res)

    report_text, summary = render_enrichment_trial_report(results)
    print(report_text)

    # If execute mode requested and dry_run explicitly False
    if execute and not dry_run:
        fc_adapter = FirecrawlAdapter(fc_config, transport=active_transport)
        ap_adapter = ApifyEnrichmentAdapter(ap_config, transport=active_transport)
        for res in results:
            for step in res.step_decisions:
                if step.decision == "would_call_provider":
                    if step.provider == "firecrawl":
                        fc_adapter.scrape_url(step.target_value)
                    elif step.provider.startswith("apify_"):
                        group = step.provider.replace("apify_", "")
                        ap_adapter.run_actor(
                            actor_id=step.actor_id,
                            group=group,
                            input_data={},
                            estimated_cost_usd=step.estimated_cost_usd,
                        )

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Local-only enrichment trial command previewing/running 10-lead trial path."
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
        default=10,
        help="Maximum number of leads to inspect (max 10 in controlled trial mode, default: 10)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Run in dry-run mode without making provider calls (default: True)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        default=False,
        help="Allow trial execution if provider credentials and flags are explicitly enabled",
    )
    parser.add_argument(
        "--max-budget-usd",
        type=Decimal,
        default=Decimal("5.00"),
        help="Maximum allowable total spend for the trial run (default: 5.00)",
    )
    args = parser.parse_args()

    try:
        run_enrichment_trial(
            statuses=args.statuses,
            limit=args.limit,
            dry_run=not args.execute,
            execute=args.execute,
            max_total_budget_usd=args.max_budget_usd,
        )
        return 0
    except Exception as error:
        print(f"Enrichment trial failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
