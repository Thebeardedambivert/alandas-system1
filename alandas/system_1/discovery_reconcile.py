"""Safe operator reconciliation command for discovery runs."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import json
import logging
import os
import sys
from typing import Any

from system_1 import db
from system_1.discovery_policy import TrialPolicy
from system_1.provider_http import HttpTransport, UrllibHttpTransport

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ApifyRunDetails:
    external_id: str
    status: str
    actual_cost_usd: Decimal | None
    raw_data: dict[str, Any]


def fetch_apify_run_details(token: str, transport: HttpTransport, external_id: str) -> ApifyRunDetails:
    """Fetch status and usage cost for an existing Apify run ID. Never starts a new run."""
    url = f"https://api.apify.com/v2/actor-runs/{external_id}"
    response = transport.request("GET", url, {"Authorization": f"Bearer {token}"}, None, 30)
    if response.status_code != 200:
        raise RuntimeError(f"Apify returned status {response.status_code} for run {external_id}")
    data = (response.json_body.get("data") or {})
    status = str(data.get("status", "unknown"))

    # usageTotalUsd or stats.computeUnits / pricing
    cost_val = data.get("usageTotalUsd")
    if cost_val is None and "usage" in data and isinstance(data["usage"], dict):
        cost_val = data["usage"].get("TOTAL_CHARGES_USD")
    actual_cost = Decimal(str(cost_val)) if cost_val is not None else None
    return ApifyRunDetails(
        external_id=external_id,
        status=status,
        actual_cost_usd=actual_cost,
        raw_data=data,
    )


def get_discovery_provider_runs(daily_run_id: str) -> list[dict[str, Any]]:
    """Retrieve all provider reservations and runs for a given daily run."""
    with db.connect() as connection:
        rows = connection.execute(
            """
            SELECT provider, external_id, estimated_cost_usd, actual_cost_usd, status, details
            FROM discovery_provider_runs
            WHERE daily_run_id = %s
            ORDER BY provider
            """,
            (daily_run_id,),
        ).fetchall()
    results = []
    for r in rows:
        results.append({
            "provider": r[0],
            "external_id": r[1],
            "estimated_cost_usd": Decimal(str(r[2])) if r[2] is not None else None,
            "actual_cost_usd": Decimal(str(r[3])) if r[3] is not None else None,
            "status": r[4],
            "details": r[5] if isinstance(r[5], dict) else {},
        })
    return results


def update_reconciled_provider_run(
    daily_run_id: str,
    provider: str,
    status: str,
    actual_cost_usd: Decimal | None,
    details: dict[str, Any],
) -> None:
    """Record verified status and actual cost in database."""
    with db.connect() as connection:
        connection.execute(
            """
            UPDATE discovery_provider_runs
            SET status = %s,
                actual_cost_usd = %s,
                details = %s::jsonb,
                updated_at = NOW()
            WHERE daily_run_id = %s AND provider = %s
            """,
            (
                status,
                str(actual_cost_usd) if actual_cost_usd is not None else None,
                json.dumps(details, ensure_ascii=True),
                daily_run_id,
                provider,
            ),
        )


def reconcile_daily_discovery_run(
    daily_run_id: str,
    environment: dict[str, str],
    transport: HttpTransport,
) -> dict[str, Any]:
    """Inspect and reconcile provider runs for daily_run_id without starting new work."""
    token = environment.get("APIFY_API_TOKEN", "").strip()
    records = get_discovery_provider_runs(daily_run_id)
    if not records:
        return {
            "daily_run_id": daily_run_id,
            "status": "no_records_found",
            "provider_runs": [],
        }

    summary: list[dict[str, Any]] = []
    for rec in records:
        provider = rec["provider"]
        external_id = rec["external_id"]
        current_status = rec["status"]

        if provider.startswith("apify:") and external_id:
            if not token:
                raise RuntimeError("APIFY_API_TOKEN required to reconcile submitted Apify run")
            details = fetch_apify_run_details(token, transport, external_id)
            final_status = details.status.lower()
            update_reconciled_provider_run(
                daily_run_id,
                provider,
                status=final_status,
                actual_cost_usd=details.actual_cost_usd,
                details={"apify_status": details.status, "reconciled": True},
            )
            summary.append({
                "provider": provider,
                "external_id": external_id,
                "status": final_status,
                "estimated_cost_usd": str(rec["estimated_cost_usd"]) if rec["estimated_cost_usd"] else None,
                "actual_cost_usd": str(details.actual_cost_usd) if details.actual_cost_usd is not None else None,
                "reconciled": True,
            })
        elif current_status == "pending_submission" or not external_id:
            summary.append({
                "provider": provider,
                "external_id": "",
                "status": "reserved_not_submitted",
                "estimated_cost_usd": str(rec["estimated_cost_usd"]) if rec["estimated_cost_usd"] else None,
                "actual_cost_usd": "0.00",
                "reconciled": False,
                "note": "Reserved but never submitted to provider",
            })
        else:
            summary.append({
                "provider": provider,
                "external_id": external_id,
                "status": current_status,
                "estimated_cost_usd": str(rec["estimated_cost_usd"]) if rec["estimated_cost_usd"] else None,
                "actual_cost_usd": str(rec["actual_cost_usd"]) if rec["actual_cost_usd"] else None,
                "reconciled": False,
            })

    return {
        "daily_run_id": daily_run_id,
        "status": "reconciled",
        "provider_runs": summary,
    }


def format_reconciliation_report(result: dict[str, Any]) -> str:
    """Format safe human-readable reconciliation report."""
    lines = [
        "=== Discovery Reconciliation Report ===",
        f"Daily Run ID: {result['daily_run_id']}",
        f"Overall Status: {result['status']}",
        "",
        "Provider Breakdown:",
    ]
    for r in result.get("provider_runs", []):
        lines.append(f"  - Provider: {r['provider']}")
        lines.append(f"    Status: {r['status']}")
        lines.append(f"    External ID: {r['external_id'] or '(none)'}")
        lines.append(f"    Estimated USD: {r['estimated_cost_usd'] or '0.00'}")
        lines.append(f"    Actual USD: {r['actual_cost_usd'] or '0.00'}")
        if r.get("note"):
            lines.append(f"    Note: {r['note']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    from datetime import date
    target_day = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    if target_day == "today":
        target_day = date.today().isoformat()
    policy = TrialPolicy.default(date.fromisoformat(target_day))
    daily_run_id = policy.daily_run_id(date.fromisoformat(target_day))

    transport = UrllibHttpTransport()
    try:
        report = reconcile_daily_discovery_run(daily_run_id, os.environ, transport)
        print(format_reconciliation_report(report))
        return 0
    except Exception as error:
        print(f"Reconciliation error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
