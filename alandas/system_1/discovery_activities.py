"""Safe durable-record activity for a scheduled discovery day.

Provider submission remains deliberately separate. This activity creates the
one Postgres run record that makes repeated Temporal deliveries harmless.
"""

from __future__ import annotations

from temporalio import activity

from system_1 import db


@activity.defn
def create_daily_discovery_run_activity(input_data: dict[str, str]) -> dict[str, str]:
    """Persist an idempotent daily control record without contacting providers."""

    daily_run_id, status = db.create_or_get_discovery_run(
        input_data["daily_run_id"],
        input_data["policy_version"],
        input_data["scheduled_for"],
    )
    return {"daily_run_id": daily_run_id, "status": status}
