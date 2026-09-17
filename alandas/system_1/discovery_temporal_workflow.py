"""Temporal wrapper around the deterministic daily discovery decisions."""

from __future__ import annotations

from datetime import date, timedelta

from temporalio import workflow

from system_1.discovery_scheduler import (
    daily_workflow_id,
    policy_for_trial_start,
    schedule_action,
)

with workflow.unsafe.imports_passed_through():
    from system_1.discovery_activities import create_daily_discovery_run_activity


@workflow.defn
class DailyDiscoveryWorkflow:
    """Create one durable daily trial record before provider work is enabled."""

    @workflow.run
    async def run(
        self, policy_version: str, trial_starts_on: str, scheduled_for: str
    ) -> dict[str, str]:
        day = date.fromisoformat(scheduled_for)
        policy = policy_for_trial_start(trial_starts_on)
        if policy.policy_version != policy_version:
            raise ValueError("unexpected discovery policy version")
        if schedule_action(policy, day) == "pause":
            return {"status": "paused", "scheduled_for": scheduled_for}
        daily_run_id = policy.daily_run_id(day)
        record = await workflow.execute_activity(
            create_daily_discovery_run_activity,
            {
                "daily_run_id": daily_run_id,
                "policy_version": policy_version,
                "scheduled_for": scheduled_for,
            },
            start_to_close_timeout=timedelta(seconds=30),
        )
        return {
            "status": "not_started",
            "daily_run_id": str(record["daily_run_id"]),
            "workflow_id": daily_workflow_id(policy, day),
        }
