"""Durable discovery-run state and safe retry decisions."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class RetryDecision:
    action: str
    delay_seconds: int | None


@dataclass(frozen=True)
class ProviderRun:
    daily_run_id: str
    provider: str
    external_id: str
    estimated_cost_usd: Decimal
    status: str = "submitted"


def retry_decision(
    *, status_code: int | None, outcome_known: bool, attempt_number: int
) -> RetryDecision:
    """Retry only known transient errors; reconcile uncertain paid outcomes."""

    if not outcome_known:
        return RetryDecision("reconcile", None)
    if status_code in {429, 500, 502, 503, 504} and 1 <= attempt_number <= 3:
        return RetryDecision("retry", (30, 120, 600)[attempt_number - 1])
    return RetryDecision("needs_attention", None)


class InMemoryDiscoveryStore:
    """Small hermetic double for run-idempotency tests."""

    def __init__(self) -> None:
        self._runs: dict[tuple[str, str], ProviderRun] = {}

    def reserve_submission(
        self, daily_run_id: str, provider: str, estimated_cost_usd: Decimal
    ) -> ProviderRun:
        key = (daily_run_id, provider)
        if key not in self._runs:
            self._runs[key] = ProviderRun(
                daily_run_id=daily_run_id,
                provider=provider,
                external_id="",
                estimated_cost_usd=estimated_cost_usd,
                status="pending_submission",
            )
        return self._runs[key]

    def record_submission(
        self,
        daily_run_id: str,
        provider: str,
        external_id: str,
        estimated_cost_usd: Decimal,
    ) -> ProviderRun:
        key = (daily_run_id, provider)
        if key not in self._runs:
            self._runs[key] = ProviderRun(
                daily_run_id=daily_run_id,
                provider=provider,
                external_id=external_id,
                estimated_cost_usd=estimated_cost_usd,
            )
        return self._runs[key]
