"""Print a token-safe discovery status for operators."""

from __future__ import annotations

import os
import sys
from datetime import date

from system_1.discovery_controls import format_daily_status
from system_1.discovery_policy import TrialPolicy


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] != "today":
        print("Usage: python -m system_1.discovery_status today")
        return 2
    policy = TrialPolicy.default(date.today())
    print(
        format_daily_status(
            {"daily_run_id": policy.daily_run_id(date.today()), "status": "not_started"},
            os.environ,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
