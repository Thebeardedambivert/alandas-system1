"""Operate System 1 Temporal lead workflows from the command line."""

from __future__ import annotations

import argparse
import asyncio
import os
from dataclasses import asdict, is_dataclass
from pprint import pprint
from typing import Any

from temporalio.client import Client

from system_1.workflows import CafeLeadWorkflow


def clean(value: Any) -> Any:
    """Convert dataclasses to plain objects for printing."""

    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, list):
        return [clean(item) for item in value]
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items()}
    return value


async def connect() -> Client:
    """Connect to Temporal."""

    address = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
    namespace = os.environ.get("TEMPORAL_NAMESPACE", "default")
    return await Client.connect(address, namespace=namespace)


async def run(args: argparse.Namespace) -> int:
    client = await connect()
    handle = client.get_workflow_handle(args.workflow_id)

    if args.command == "approve":
        await handle.signal(CafeLeadWorkflow.approve_by_sidy)
        print(f"approved {args.workflow_id}")
        return 0

    if args.command == "reject":
        await handle.signal(CafeLeadWorkflow.reject_by_sidy, args.reason)
        print(f"rejected {args.workflow_id}")
        return 0

    if args.command == "record-sent":
        state = await handle.query(CafeLeadWorkflow.current_state)
        if state is None or state.status != "approved":
            print(
                f"cannot record a send for {args.workflow_id}: "
                "Sidy must approve the drafted message first"
            )
            return 2
        await handle.signal(CafeLeadWorkflow.record_sent)
        print(f"send recorded for {args.workflow_id}")
        return 0

    if args.command == "state":
        state = await handle.query(CafeLeadWorkflow.current_state)
        pprint(clean(state), sort_dicts=False)
        return 0

    raise ValueError(f"unknown command: {args.command}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Operate Alandas System 1 workflows")
    subparsers = root.add_subparsers(dest="command", required=True)

    approve = subparsers.add_parser("approve")
    approve.add_argument("workflow_id")

    reject = subparsers.add_parser("reject")
    reject.add_argument("workflow_id")
    reject.add_argument("reason")

    record_sent = subparsers.add_parser("record-sent")
    record_sent.add_argument("workflow_id")

    state = subparsers.add_parser("state")
    state.add_argument("workflow_id")

    return root


def main() -> int:
    args = parser().parse_args()
    return asyncio.run(run(args))


if __name__ == "__main__":
    raise SystemExit(main())
