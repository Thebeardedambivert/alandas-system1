"""Deterministic decisions for the daily discovery workflow."""

from __future__ import annotations

from collections.abc import Mapping


def final_daily_status(provider_statuses: Mapping[str, str]) -> str:
    """Summarise providers without hiding a partial failure.

    A mixed result is degraded: it preserves successful work while putting the
    failed provider in front of the operator for the next run.
    """

    statuses = set(provider_statuses.values())
    if not statuses:
        return "needs_attention"
    if statuses == {"succeeded"}:
        return "succeeded"
    if "needs_attention" in statuses or "blocked" in statuses:
        return "degraded" if "succeeded" in statuses else "needs_attention"
    return "degraded"
