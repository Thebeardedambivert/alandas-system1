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
    from system_1.discovery_activities import (
        create_daily_discovery_run_activity,
        submit_daily_discovery_providers_activity,
    )
    from system_1.discovery_workflows import final_daily_status


@workflow.defn
class DailyDiscoveryWorkflow:
    """Create one durable daily trial record before provider work is enabled."""

    @workflow.run
    async def run(
        self,
        policy_version: str,
        trial_starts_on: str,
        target_day: str | None = None,
    ) -> dict[str, str]:
        if target_day:
            day = date.fromisoformat(target_day)
        else:
            now_dt = workflow.now()
            # In Temporal sandbox, now_dt is UTC. Extract UTC calendar components
            # deterministically without calling astimezone(ZoneInfo(...)).
            # When scheduled via cron in Europe/Berlin, workflow runs at 09:00 Berlin (07:00 or 08:00 UTC),
            # where the UTC calendar date is identical to the Berlin calendar date.
            day = date(now_dt.year, now_dt.month, now_dt.day)
        scheduled_for = day.isoformat()
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
        provider_statuses = await workflow.execute_activity(
            submit_daily_discovery_providers_activity,
            {
                "daily_run_id": daily_run_id,
                "trial_starts_on": trial_starts_on,
            },
            start_to_close_timeout=timedelta(minutes=5),
        )
        if provider_statuses.get("status") == "disabled":
            return {
                "status": "disabled",
                "daily_run_id": str(record["daily_run_id"]),
                "workflow_id": daily_workflow_id(policy, day),
            }
        return {
            "status": final_daily_status(provider_statuses),
            "daily_run_id": str(record["daily_run_id"]),
            "workflow_id": daily_workflow_id(policy, day),
        }
