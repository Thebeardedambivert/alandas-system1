"""Safe durable-record activity for a scheduled discovery day.

Provider submission remains deliberately separate. This activity creates the
one Postgres run record that makes repeated Temporal deliveries harmless.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from decimal import Decimal
import os
from urllib.parse import quote

from temporalio import activity

from system_1 import db
from system_1.apify_provider import ApifyProvider
from system_1.discovery_controls import (
    discovery_enabled,
    discovery_providers,
    validate_scheduler_environment,
)
from system_1.discovery_policy import TrialPolicy
from system_1.outscraper_provider import OutscraperProvider
from system_1.provider_http import UrllibHttpTransport


@activity.defn
def create_daily_discovery_run_activity(input_data: dict[str, str]) -> dict[str, str]:
    """Persist an idempotent daily control record without contacting providers."""

    daily_run_id, status = db.create_or_get_discovery_run(
        input_data["daily_run_id"],
        input_data["policy_version"],
        input_data["scheduled_for"],
    )
    return {"daily_run_id": daily_run_id, "status": status}


@activity.defn
def submit_daily_discovery_providers_activity(input_data: dict[str, str]) -> dict[str, str]:
    """Submit only reserved, policy-capped requests when explicitly enabled."""

    environment = os.environ
    if not discovery_enabled(environment):
        return {"status": "disabled"}
    validate_scheduler_environment(environment)
    providers = discovery_providers(environment)
    policy = replace(
        TrialPolicy.default(date.fromisoformat(input_data["trial_starts_on"])),
        apify_max_cost_usd=Decimal(environment.get("SYSTEM1_DISCOVERY_MAX_APIFY_USD", "1.40")),
        outscraper_max_cost_usd=Decimal(environment.get("SYSTEM1_DISCOVERY_MAX_OUTSCRAPER_USD", "0.60")),
    )
    daily_run_id = input_data["daily_run_id"]
    transport = UrllibHttpTransport()
    statuses: dict[str, str] = {}

    if "apify" in providers:
        apify = ApifyProvider(environment["APIFY_API_TOKEN"], transport)
        for category, limit in policy.apify_allocations.items():
            provider_name = f"apify:{category}"
            estimate = policy.apify_max_cost_usd * Decimal(limit) / Decimal(50)
            _, external_id, status, newly_reserved = db.reserve_discovery_provider_submission(
                daily_run_id, provider_name, str(estimate)
            )
            if not newly_reserved:
                statuses[provider_name] = "submitted" if external_id else "needs_attention"
                continue
            try:
                submitted = apify.submit_allocation(
                    policy, daily_run_id, category, limit, estimate
                )
                db.complete_discovery_provider_submission(
                    daily_run_id, provider_name, submitted.external_id
                )
                statuses[provider_name] = "submitted"
            except Exception:
                # The reservation stays pending. A later run must reconcile or ask
                # for help instead of creating a duplicate paid request.
                statuses[provider_name] = "needs_attention"

    if "outscraper" in providers:
        _, external_id, status, newly_reserved = db.reserve_discovery_provider_submission(
            daily_run_id, "outscraper", str(policy.outscraper_max_cost_usd)
        )
        if not newly_reserved:
            statuses["outscraper"] = "submitted" if external_id else "needs_attention"
        else:
            try:
                callback_base_url = environment["SYSTEM1_DISCOVERY_OUTSCRAPER_CALLBACK_BASE_URL"].rstrip("/")
                callback_url = (
                    callback_base_url
                    + "/webhooks/outscraper/google-maps?token="
                    + quote(environment["OUTSCRAPER_WEBHOOK_TOKEN"], safe="")
                )
                submitted = OutscraperProvider(
                    environment["OUTSCRAPER_API_KEY"], transport
                ).submit(
                    policy, daily_run_id, callback_url, policy.outscraper_max_cost_usd
                )
                db.complete_discovery_provider_submission(
                    daily_run_id, "outscraper", submitted.external_id
                )
                statuses["outscraper"] = "submitted"
            except Exception:
                statuses["outscraper"] = "needs_attention"
    return statuses
