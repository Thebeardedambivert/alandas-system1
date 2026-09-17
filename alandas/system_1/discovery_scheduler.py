"""Schedule decisions for the bounded discovery trial.

Temporal wiring is intentionally kept out of module import and worker boot.
"""

from __future__ import annotations

from datetime import date

from system_1.discovery_policy import TrialPolicy


def schedule_action(policy: TrialPolicy, day: date) -> str:
    """Run only inside the seven-day policy window; otherwise pause."""

    return "run" if policy.for_date(day) else "pause"


def daily_workflow_id(policy: TrialPolicy, day: date) -> str:
    """Give retries of one calendar day's work the same Temporal identity."""

    return f"alandas-discovery-{policy.policy_version}-{day.isoformat()}"


def policy_for_trial_start(trial_starts_on: str) -> TrialPolicy:
    """Decode the fixed trial start used by every scheduled daily workflow."""

    return TrialPolicy.default(date.fromisoformat(trial_starts_on))
