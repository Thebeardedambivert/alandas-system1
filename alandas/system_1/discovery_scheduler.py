"""Schedule decisions for the bounded discovery trial.

Temporal wiring is intentionally kept out of module import and worker boot.
"""

from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta
import os
import sys
from zoneinfo import ZoneInfo

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


def scheduled_day_in_berlin(instant: datetime) -> date:
    """Turn Temporal's UTC clock into the business calendar date."""

    return instant.astimezone(ZoneInfo("Europe/Berlin")).date()


def trial_schedule_definition(policy: TrialPolicy) -> dict[str, str]:
    """Return the small, inspectable schedule contract used by the CLI."""

    return {
        "schedule_id": f"alandas-discovery-{policy.policy_version}",
        "cron": "0 9 * * *",
        "timezone": policy.timezone,
        "ends_on": (policy.starts_on + timedelta(days=policy.duration_days)).isoformat(),
    }


async def start_trial_schedule(client: object, policy: TrialPolicy, task_queue: str) -> str:
    """Create the one expiring Temporal schedule; never call this at boot."""

    from temporalio.client import (
        Schedule,
        ScheduleActionStartWorkflow,
        ScheduleSpec,
        ScheduleState,
    )

    from system_1.discovery_temporal_workflow import DailyDiscoveryWorkflow

    definition = trial_schedule_definition(policy)
    berlin = ZoneInfo(policy.timezone)
    end_at = datetime.combine(
        policy.starts_on + timedelta(days=policy.duration_days),
        datetime.min.time(),
        tzinfo=berlin,
    )
    await client.create_schedule(
        definition["schedule_id"],
        Schedule(
            action=ScheduleActionStartWorkflow(
                DailyDiscoveryWorkflow.run,
                args=[policy.policy_version, policy.starts_on.isoformat()],
                id=definition["schedule_id"],
                task_queue=task_queue,
            ),
            spec=ScheduleSpec(
                cron_expressions=[definition["cron"]],
                time_zone_name=definition["timezone"],
                end_at=end_at,
            ),
            state=ScheduleState(
                note="Alandas seven-day discovery trial; expires before day eight."
            ),
        ),
    )
    return definition["schedule_id"]


async def pause_trial_schedule(client: object, schedule_id: str) -> None:
    """Pause without deleting history or workflows already started."""

    await client.get_schedule_handle(schedule_id).pause(
        note="Paused by Alandas discovery operator"
    )


async def start_manual_daily_run(client: object, policy: TrialPolicy, task_queue: str) -> str:
    """Start the one separately approved live contract check."""

    from system_1.discovery_temporal_workflow import DailyDiscoveryWorkflow

    day = scheduled_day_in_berlin(datetime.now(tz=ZoneInfo("UTC")))
    workflow_id = daily_workflow_id(policy, day)
    await client.start_workflow(
        DailyDiscoveryWorkflow.run,
        args=[policy.policy_version, policy.starts_on.isoformat()],
        id=workflow_id,
        task_queue=task_queue,
    )
    return workflow_id


async def _main() -> int:
    from temporalio.client import Client

    from system_1.discovery_controls import validate_scheduler_environment

    if len(sys.argv) != 2 or sys.argv[1] not in {
        "start-manual",
        "start-trial",
        "pause-trial",
    }:
        print("Usage: python -m system_1.discovery_scheduler start-manual|start-trial|pause-trial")
        return 2
    action = sys.argv[1]
    if action != "pause-trial":
        validate_scheduler_environment(os.environ)
    address = os.environ.get("TEMPORAL_ADDRESS", "temporal:7233")
    namespace = os.environ.get("TEMPORAL_NAMESPACE", "default")
    task_queue = os.environ.get("TEMPORAL_TASK_QUEUE", "alandas-system1")
    client = await Client.connect(address, namespace=namespace)
    if action == "pause-trial":
        await pause_trial_schedule(client, "alandas-discovery-trial-v1")
        print("trial schedule paused")
        return 0
    policy = policy_for_trial_start(
        os.environ.get(
            "SYSTEM1_DISCOVERY_TRIAL_START_DATE",
            scheduled_day_in_berlin(datetime.now(tz=ZoneInfo("UTC"))).isoformat(),
        )
    )
    if action == "start-manual":
        print(f"started manual workflow: {await start_manual_daily_run(client, policy, task_queue)}")
        return 0
    print(f"started trial schedule: {await start_trial_schedule(client, policy, task_queue)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main()))
