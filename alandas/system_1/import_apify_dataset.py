"""Import candidates from an existing completed Apify discovery dataset into System 1."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import logging
import os
import sys
from typing import Any, Sequence

from system_1 import db
from system_1.apify_google_maps import candidate_to_lead, map_apify_dataset
from system_1.core import audit_event_key, lead_workflow_id, validate_intake
from system_1.provider_http import HttpTransport, UrllibHttpTransport

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ApifyImportSummary:
    daily_run_id: str
    provider: str
    run_id: str
    dataset_id: str
    fetched: int
    mapped: int
    inserted: int
    duplicate_skipped: int
    invalid_skipped: int
    failed: int


def get_provider_run_external_id(daily_run_id: str, provider: str) -> str:
    """Look up external_id from discovery_provider_runs."""
    with db.connect() as connection:
        row = connection.execute(
            """
            SELECT external_id, status FROM discovery_provider_runs
            WHERE daily_run_id = %s AND provider = %s
            """,
            (daily_run_id, provider),
        ).fetchone()
    if row is None:
        raise RuntimeError(f"no provider run found for {daily_run_id} and {provider}")
    external_id = (row[0] or "").strip()
    if not external_id:
        raise RuntimeError(f"provider run for {daily_run_id} and {provider} has no external_id")
    return external_id


def fetch_apify_dataset_items(
    token: str,
    transport: HttpTransport,
    run_id: str,
) -> tuple[str, list[dict[str, Any]]]:
    """Fetch items from an existing completed Apify actor run dataset.

    Strict invariant: ONLY performs GET requests. Never creates or starts a run.
    """
    # 1. Inspect actor run to obtain defaultDatasetId
    run_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    run_resp = transport.request("GET", run_url, {"Authorization": f"Bearer {token}"}, None, 30)
    if run_resp.status_code != 200:
        raise RuntimeError(f"Apify API returned HTTP {run_resp.status_code} for run {run_id}")
    run_data = run_resp.json_body.get("data") or {}
    dataset_id = run_data.get("defaultDatasetId") or ""
    if not dataset_id:
        # Fallback to direct dataset if run_id is dataset_id or dataset items endpoint
        dataset_id = run_data.get("id") or run_id

    # 2. Fetch dataset items
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?clean=true"
    items_resp = transport.request("GET", items_url, {"Authorization": f"Bearer {token}"}, None, 60)
    if items_resp.status_code != 200:
        raise RuntimeError(f"Apify API returned HTTP {items_resp.status_code} for dataset {dataset_id}")
    items = items_resp.json_body
    if not isinstance(items, list):
        if isinstance(items, dict) and "data" in items and isinstance(items["data"], list):
            items = items["data"]
        else:
            raise RuntimeError(f"unexpected dataset response format for dataset {dataset_id}")
    return dataset_id, items


def import_apify_candidates(
    daily_run_id: str,
    provider: str,
    items: Sequence[Mapping[str, Any]],
    dataset_id: str,
    run_id: str,
) -> ApifyImportSummary:
    """Map and import Apify candidate items into System 1 with duplicate checks and audit logging."""
    fetched = len(items)
    inserted = 0
    duplicate_skipped = 0
    invalid_skipped = 0
    failed = 0

    # Delegate mapping to canonical map_apify_dataset to enforce MAX_RESULTS_PER_RUN,
    # placeId deduplication, and filtering of closed/ad/invalid records.
    candidates, mapper_notes = map_apify_dataset(items)
    mapped = len(candidates)

    # Classify mapper notes into duplicate_skipped (duplicate Google Place ID) and invalid_skipped
    for note in mapper_notes:
        if "duplicate Google Place ID" in note:
            duplicate_skipped += 1
        else:
            invalid_skipped += 1

    seen_in_batch: set[str] = set()

    for idx, candidate in enumerate(candidates, start=1):
        try:
            lead = candidate_to_lead(candidate)
        except Exception as err:
            logger.warning("Candidate %s conversion error: %s", idx, err)
            invalid_skipped += 1
            continue

        intake_errors = validate_intake(lead)
        if intake_errors:
            logger.info("Candidate %s failed intake validation: %s", idx, intake_errors)
            invalid_skipped += 1
            continue

        workflow_id = lead_workflow_id(lead)
        if workflow_id in seen_in_batch:
            duplicate_skipped += 1
            continue
        seen_in_batch.add(workflow_id)

        # Check existing lead by workflow_id or internal duplicate fields
        existing_matches = db.find_internal_duplicates(workflow_id, lead)
        # Also check if exact lead row exists in DB
        with db.connect() as connection:
            existing_lead = connection.execute(
                "SELECT workflow_id, status FROM leads WHERE workflow_id = %s",
                (workflow_id,),
            ).fetchone()

        if existing_lead or existing_matches:
            duplicate_skipped += 1
            # Record audit event indicating duplicate skipped (idempotent ON CONFLICT)
            db.insert_audit_event(
                workflow_id=workflow_id,
                event_key=audit_event_key(workflow_id, "discovery_import_duplicate_skipped"),
                event_name="discovery_import_duplicate_skipped",
                status="skipped",
                details={
                    "daily_run_id": daily_run_id,
                    "provider": provider,
                    "run_id": run_id,
                    "dataset_id": dataset_id,
                    "source_record_id": candidate.source_record_id,
                    "matched_existing": bool(existing_lead),
                    "duplicate_matches": existing_matches,
                },
            )
            continue

        try:
            # Insert lead into database in 'new' status
            db.upsert_lead(workflow_id, lead, status="new")
            # Log audit event for insertion
            db.insert_audit_event(
                workflow_id=workflow_id,
                event_key=audit_event_key(workflow_id, "discovery_lead_imported"),
                event_name="discovery_lead_imported",
                status="new",
                details={
                    "daily_run_id": daily_run_id,
                    "provider": provider,
                    "run_id": run_id,
                    "dataset_id": dataset_id,
                    "source_record_id": candidate.source_record_id,
                    "venue_name": lead.venue_name,
                    "city": lead.city,
                },
            )
            inserted += 1
        except Exception as err:
            logger.error("Failed to insert lead %s: %s", workflow_id, err, exc_info=True)
            failed += 1

    return ApifyImportSummary(
        daily_run_id=daily_run_id,
        provider=provider,
        run_id=run_id,
        dataset_id=dataset_id,
        fetched=fetched,
        mapped=mapped,
        inserted=inserted,
        duplicate_skipped=duplicate_skipped,
        invalid_skipped=invalid_skipped,
        failed=failed,
    )


def execute_apify_import(
    daily_run_id: str,
    provider: str,
    environment: Mapping[str, str],
    transport: HttpTransport,
    *,
    direct_run_id: str | None = None,
) -> ApifyImportSummary:
    """Execute the end-to-end import flow for an existing completed Apify discovery run."""
    token = environment.get("APIFY_API_TOKEN", "").strip()
    if not token:
        raise RuntimeError("missing required APIFY_API_TOKEN environment variable")

    run_id = direct_run_id.strip() if direct_run_id else ""
    if not run_id:
        run_id = get_provider_run_external_id(daily_run_id, provider)

    dataset_id, items = fetch_apify_dataset_items(token, transport, run_id)
    summary = import_apify_candidates(daily_run_id, provider, items, dataset_id, run_id)
    return summary


def format_import_summary(summary: ApifyImportSummary) -> str:
    """Format clean, secret-free summary for operators."""
    lines = [
        "=== Apify Discovery Dataset Import Summary ===",
        f"Daily Run ID:      {summary.daily_run_id}",
        f"Provider:          {summary.provider}",
        f"Apify Run ID:      {summary.run_id}",
        f"Apify Dataset ID:  {summary.dataset_id}",
        f"Fetched Records:   {summary.fetched}",
        f"Mapped Candidates: {summary.mapped}",
        f"Inserted Leads:    {summary.inserted}",
        f"Duplicate Skipped: {summary.duplicate_skipped}",
        f"Invalid Skipped:   {summary.invalid_skipped}",
        f"Failed:            {summary.failed}",
    ]
    return "\n".join(lines)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Import candidates from a completed Apify discovery dataset into System 1."
    )
    parser.add_argument("daily_run_id", help="Daily run ID, e.g. discovery:trial-v1:2026-09-18")
    parser.add_argument("provider", help="Provider name, e.g. apify:cafe")
    parser.add_argument("--run-id", default=None, help="Optional direct Apify run ID override for recovery")

    args = parser.parse_args()
    transport = UrllibHttpTransport()
    try:
        summary = execute_apify_import(
            args.daily_run_id,
            args.provider,
            os.environ,
            transport,
            direct_run_id=args.run_id,
        )
        print(format_import_summary(summary))
        return 0 if summary.failed == 0 else 1
    except Exception as error:
        print(f"Import failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
