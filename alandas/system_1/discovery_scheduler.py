"""Schedule decisions for the bounded discovery trial.

Temporal wiring is intentionally kept out of module import and worker boot.
"""

from __future__ import annotations

from datetime import date

from system_1.discovery_policy import TrialPolicy


def schedule_action(policy: TrialPolicy, day: date) -> str:
    """Run only inside the seven-day policy window; otherwise pause."""

    return "run" if policy.for_date(day) else "pause"
