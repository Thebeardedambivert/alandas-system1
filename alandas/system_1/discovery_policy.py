"""Temporary, bounded policy for the automated discovery trial."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class TrialPolicy:
    """Keep trial limits explicit and separate from future paid enrichment."""

    policy_version: str
    starts_on: date
    apify_allocations: Mapping[str, int]
    outscraper_limit: int = 50
    duration_days: int = 7
    timezone: str = "Europe/Berlin"
    daily_total_limit: int = 100
    paid_enrichment_enabled: bool = False
    apify_max_cost_usd: Decimal = Decimal("1.40")
    outscraper_max_cost_usd: Decimal = Decimal("0.60")

    @classmethod
    def default(cls, starts_on: date) -> "TrialPolicy":
        return cls(
            policy_version="trial-v1",
            starts_on=starts_on,
            apify_allocations=MappingProxyType(
                {
                    "cafe": 20,
                    "brunch venue": 10,
                    "specialty coffee venue": 10,
                    "boutique hotel": 10,
                }
            ),
        )

    def for_date(self, day: date) -> bool:
        """Return true only for one of the seven approved trial days."""

        return self.starts_on <= day < self.starts_on + timedelta(days=self.duration_days)

    def daily_run_id(self, day: date) -> str:
        """Create the stable identifier used for retries and audit writes."""

        return f"discovery:{self.policy_version}:{day.isoformat()}"
