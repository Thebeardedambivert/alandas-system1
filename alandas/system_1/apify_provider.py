"""Bounded Apify submission contract; no request runs at import time."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import json

from system_1.discovery_policy import TrialPolicy
from system_1.provider_http import HttpTransport


class CostLimitExceeded(ValueError):
    """The displayed/approved estimate is outside the current policy."""


@dataclass(frozen=True)
class ProviderSubmission:
    provider: str
    external_id: str
    estimated_cost_usd: Decimal


@dataclass(frozen=True)
class ProviderOutcome:
    provider: str
    external_id: str
    status: str


class ApifyProvider:
    def __init__(self, token: str, transport: HttpTransport) -> None:
        self._token = token
        self._transport = transport

    def submit(self, policy: TrialPolicy, daily_run_id: str, estimated_cost_usd: Decimal) -> ProviderSubmission:
        if estimated_cost_usd > policy.apify_max_cost_usd:
            raise CostLimitExceeded("Apify estimate exceeds the trial cap")
        raise ValueError("Apify submissions must name one approved category allocation")

    def submit_allocation(
        self,
        policy: TrialPolicy,
        daily_run_id: str,
        category: str,
        limit: int,
        estimated_cost_usd: Decimal,
    ) -> ProviderSubmission:
        approved_limit = policy.apify_allocations.get(category)
        if approved_limit != limit:
            raise ValueError("Apify allocation is outside the approved trial policy")
        allocation_cap = policy.apify_max_cost_usd * Decimal(limit) / Decimal(
            sum(policy.apify_allocations.values())
        )
        if estimated_cost_usd > allocation_cap:
            raise CostLimitExceeded("Apify allocation estimate exceeds its trial cap")
        response = self._transport.request(
            "POST",
            "https://api.apify.com/v2/acts/compass~crawler-google-places/runs?maxTotalChargeUsd="
            f"{estimated_cost_usd:.2f}",
            {"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"},
            json.dumps(
                {
                    "searchStringsArray": [category],
                    "locationQuery": "Germany",
                    "maxCrawledPlacesPerSearch": limit,
                    "maxImages": 0,
                    "scrapeImageAuthors": False,
                    "scrapeSocialMediaProfiles": {
                        "facebooks": False,
                        "instagrams": False,
                        "youtubes": False,
                        "tiktoks": False,
                        "twitters": False,
                    },
                    "maximumLeadsEnrichmentRecords": 0,
                }
            ).encode("utf-8"),
            30,
        )
        external_id = str((response.json_body.get("data") or {}).get("id", ""))
        if response.status_code not in {200, 201} or not external_id:
            raise RuntimeError("Apify did not return a run ID")
        return ProviderSubmission(f"apify:{category}", external_id, estimated_cost_usd)

    def reconcile(self, external_id: str) -> ProviderOutcome:
        response = self._transport.request(
            "GET",
            f"https://api.apify.com/v2/actor-runs/{external_id}",
            {"Authorization": f"Bearer {self._token}"},
            None,
            30,
        )
        if response.status_code != 200:
            raise RuntimeError("Apify reconciliation did not return a run")
        run = response.json_body.get("data") or {}
        return ProviderOutcome("apify", external_id, str(run.get("status", "unknown")))
