"""Bounded raw-only Outscraper Maps submission contract."""

from __future__ import annotations

from decimal import Decimal
from urllib.parse import urlencode

from system_1.apify_provider import CostLimitExceeded, ProviderOutcome, ProviderSubmission
from system_1.discovery_policy import TrialPolicy
from system_1.provider_http import HttpTransport


class OutscraperProvider:
    def __init__(self, token: str, transport: HttpTransport) -> None:
        self._token = token
        self._transport = transport

    def submit(self, policy: TrialPolicy, daily_run_id: str, callback_url: str, estimated_cost_usd: Decimal) -> ProviderSubmission:
        if estimated_cost_usd > policy.outscraper_max_cost_usd:
            raise CostLimitExceeded("Outscraper estimate exceeds the trial cap")
        query = urlencode({"query": "cafes, Germany", "limit": policy.outscraper_limit, "async": "true", "webhook": callback_url})
        response = self._transport.request(
            "GET", f"https://api.outscraper.com/maps/search?{query}",
            {"X-API-KEY": self._token}, None, 30,
        )
        external_id = str(response.json_body.get("id", ""))
        if response.status_code not in {200, 201, 202} or not external_id:
            raise RuntimeError("Outscraper did not return a request ID")
        return ProviderSubmission("outscraper", external_id, estimated_cost_usd)

    def reconcile(self, external_id: str) -> ProviderOutcome:
        response = self._transport.request(
            "GET",
            f"https://api.outscraper.com/requests/{external_id}",
            {"X-API-KEY": self._token},
            None,
            30,
        )
        if response.status_code != 200:
            raise RuntimeError("Outscraper reconciliation did not return a request")
        return ProviderOutcome("outscraper", external_id, str(response.json_body.get("status", "unknown")))
