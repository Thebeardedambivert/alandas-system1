"""Database helpers for Alandas System 1."""

from __future__ import annotations

from decimal import Decimal
import json
import os
from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg import Connection

from system_1.core import instagram_handle, venue_city_key, website_domain
from system_1.models import LeadInput, ResearchEvidence


def database_url() -> str:
    """Return the configured Postgres URL."""

    value = os.environ.get("DATABASE_URL")
    if not value:
        raise RuntimeError("DATABASE_URL is required")
    return value


@contextmanager
def connect() -> Iterator[Connection[tuple]]:
    """Open a Postgres connection with automatic commit."""

    with psycopg.connect(database_url()) as connection:
        yield connection


def ensure_schema() -> None:
    """Create the System 1 tables if they do not exist."""

    with connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                workflow_id TEXT PRIMARY KEY,
                venue_name TEXT NOT NULL,
                city TEXT NOT NULL,
                venue_type TEXT NOT NULL,
                source_url TEXT NOT NULL,
                website TEXT NOT NULL DEFAULT '',
                instagram TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT '',
                phone TEXT NOT NULL DEFAULT '',
                impressum_url TEXT NOT NULL DEFAULT '',
                decision_maker TEXT NOT NULL DEFAULT '',
                seat_estimate INTEGER,
                fit_score INTEGER,
                fit_reason TEXT NOT NULL DEFAULT '',
                website_domain TEXT NOT NULL DEFAULT '',
                instagram_handle TEXT NOT NULL DEFAULT '',
                venue_city_key TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'new',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_events (
                id BIGSERIAL PRIMARY KEY,
                event_key TEXT UNIQUE,
                workflow_id TEXT NOT NULL,
                event_name TEXT NOT NULL,
                status TEXT NOT NULL,
                details JSONB NOT NULL DEFAULT '{}'::JSONB,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        connection.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS website_domain TEXT NOT NULL DEFAULT ''"
        )
        connection.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS instagram_handle TEXT NOT NULL DEFAULT ''"
        )
        connection.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS venue_city_key TEXT NOT NULL DEFAULT ''"
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS leads_website_domain_idx ON leads (website_domain)"
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS leads_instagram_handle_idx ON leads (instagram_handle)"
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS leads_venue_city_key_idx ON leads (venue_city_key)"
        )
        connection.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS qualification_status TEXT NOT NULL DEFAULT ''"
        )
        connection.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS qualification_score INTEGER"
        )
        connection.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS qualification_reasons JSONB NOT NULL DEFAULT '[]'::JSONB"
        )
        connection.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS qualification_evidence JSONB NOT NULL DEFAULT '{}'::JSONB"
        )
        connection.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS qualified_at TIMESTAMPTZ"
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS leads_qualification_status_idx ON leads (qualification_status)"
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS lead_enrichment_plans (
                workflow_id TEXT PRIMARY KEY REFERENCES leads(workflow_id),
                qualification_status TEXT NOT NULL,
                steps JSONB NOT NULL DEFAULT '[]'::JSONB,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS lead_enrichment_step_approvals (
                workflow_id TEXT NOT NULL REFERENCES leads(workflow_id),
                step_name TEXT NOT NULL,
                approved_by TEXT NOT NULL,
                max_cost_usd NUMERIC(10, 4) NOT NULL DEFAULT 0.00,
                approved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                PRIMARY KEY (workflow_id, step_name)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS lead_manual_enrichment_evidence (
                workflow_id TEXT NOT NULL REFERENCES leads(workflow_id),
                step_name TEXT NOT NULL,
                field TEXT NOT NULL,
                value TEXT NOT NULL,
                source_url TEXT NOT NULL,
                recorded_by TEXT NOT NULL,
                recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                PRIMARY KEY (workflow_id, step_name, field)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS lead_research_evidence (
                evidence_key TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL REFERENCES leads(workflow_id),
                field TEXT NOT NULL,
                value TEXT NOT NULL,
                source_url TEXT NOT NULL,
                method TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        connection.execute(
            "ALTER TABLE audit_events ADD COLUMN IF NOT EXISTS event_key TEXT"
        )
        connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS audit_events_event_key_unique
            ON audit_events (event_key)
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS discovery_runs (
                daily_run_id TEXT PRIMARY KEY,
                policy_version TEXT NOT NULL,
                scheduled_for DATE NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS discovery_provider_runs (
                daily_run_id TEXT NOT NULL REFERENCES discovery_runs(daily_run_id),
                provider TEXT NOT NULL,
                external_id TEXT NOT NULL DEFAULT '',
                estimated_cost_usd NUMERIC(10,4),
                actual_cost_usd NUMERIC(10,4),
                status TEXT NOT NULL DEFAULT 'pending',
                details JSONB NOT NULL DEFAULT '{}'::JSONB,
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                PRIMARY KEY (daily_run_id, provider)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS discovery_attempts (
                daily_run_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                attempt_number INTEGER NOT NULL,
                status_code INTEGER,
                error_class TEXT NOT NULL DEFAULT '',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                PRIMARY KEY (daily_run_id, provider, attempt_number)
            )
            """
        )


def upsert_lead(workflow_id: str, lead: LeadInput, status: str) -> None:
    """Insert or update one lead row."""

    with connect() as connection:
        connection.execute(
            """
            INSERT INTO leads (
                workflow_id, venue_name, city, venue_type, source_url, website,
                instagram, email, phone, impressum_url, decision_maker,
                seat_estimate, fit_score, fit_reason, website_domain,
                instagram_handle, venue_city_key, status, updated_at
            )
            VALUES (
                %(workflow_id)s, %(venue_name)s, %(city)s, %(venue_type)s,
                %(source_url)s, %(website)s, %(instagram)s, %(email)s,
                %(phone)s, %(impressum_url)s, %(decision_maker)s,
                %(seat_estimate)s, %(fit_score)s, %(fit_reason)s,
                %(website_domain)s, %(instagram_handle)s, %(venue_city_key)s,
                %(status)s, NOW()
            )
            ON CONFLICT (workflow_id) DO UPDATE SET
                venue_name = EXCLUDED.venue_name,
                city = EXCLUDED.city,
                venue_type = EXCLUDED.venue_type,
                source_url = EXCLUDED.source_url,
                website = EXCLUDED.website,
                instagram = EXCLUDED.instagram,
                email = EXCLUDED.email,
                phone = EXCLUDED.phone,
                impressum_url = EXCLUDED.impressum_url,
                decision_maker = EXCLUDED.decision_maker,
                seat_estimate = EXCLUDED.seat_estimate,
                fit_score = EXCLUDED.fit_score,
                fit_reason = EXCLUDED.fit_reason,
                website_domain = EXCLUDED.website_domain,
                instagram_handle = EXCLUDED.instagram_handle,
                venue_city_key = EXCLUDED.venue_city_key,
                status = EXCLUDED.status,
                updated_at = NOW()
            """,
            {
                "workflow_id": workflow_id,
                "venue_name": lead.venue_name,
                "city": lead.city,
                "venue_type": lead.venue_type,
                "source_url": lead.source_url,
                "website": lead.website,
                "instagram": lead.instagram,
                "email": lead.email,
                "phone": lead.phone,
                "impressum_url": lead.impressum_url,
                "decision_maker": lead.decision_maker,
                "seat_estimate": lead.seat_estimate,
                "fit_score": lead.fit_score,
                "fit_reason": lead.fit_reason,
                "website_domain": website_domain(lead.website),
                "instagram_handle": instagram_handle(lead.instagram),
                "venue_city_key": venue_city_key(lead),
                "status": status,
            },
        )


def find_internal_duplicates(workflow_id: str, lead: LeadInput) -> list[dict[str, str]]:
    """Find other local workflow rows with a strong deterministic identity match."""

    identities = {
        "website_domain": website_domain(lead.website),
        "instagram_handle": instagram_handle(lead.instagram),
        "venue_city_key": venue_city_key(lead),
    }
    clauses: list[str] = []
    values: list[str] = [workflow_id]
    for column, value in identities.items():
        if value:
            clauses.append(f"{column} = %s")
            values.append(value)
    if not clauses:
        return []
    with connect() as connection:
        rows = connection.execute(
            f"""
            SELECT workflow_id, website_domain, instagram_handle, venue_city_key
            FROM leads
            WHERE workflow_id <> %s AND ({' OR '.join(clauses)})
            ORDER BY created_at ASC
            """,
            values,
        ).fetchall()
    matches: list[dict[str, str]] = []
    for row in rows:
        row_workflow_id, row_domain, row_instagram, row_venue_city = row
        row_values = {
            "website_domain": row_domain,
            "instagram_handle": row_instagram,
            "venue_city_key": row_venue_city,
        }
        for field, value in identities.items():
            if value and row_values[field] == value:
                matches.append({"workflow_id": row_workflow_id, "match_field": field})
    return matches


def insert_research_evidence(workflow_id: str, evidence: ResearchEvidence) -> bool:
    """Store one evidence finding once even if its research activity retries."""

    key = ":".join(
        [workflow_id, "research", evidence.field, evidence.value, evidence.source_url]
    )
    with connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO lead_research_evidence
                (evidence_key, workflow_id, field, value, source_url, method)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING evidence_key
            """,
            (
                key,
                workflow_id,
                evidence.field,
                evidence.value,
                evidence.source_url,
                evidence.method,
            ),
        )
        return cursor.fetchone() is not None


def update_lead_status(workflow_id: str, status: str) -> None:
    """Update one lead status."""

    with connect() as connection:
        connection.execute(
            "UPDATE leads SET status = %s, updated_at = NOW() WHERE workflow_id = %s",
            (status, workflow_id),
        )


def insert_audit_event(
    workflow_id: str,
    event_key: str,
    event_name: str,
    status: str,
    details: dict[str, object],
) -> bool:
    """Insert one audit event, returning false when its transition is already stored."""

    with connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO audit_events (event_key, workflow_id, event_name, status, details)
            VALUES (%s, %s, %s, %s, %s::jsonb)
            ON CONFLICT DO NOTHING
            RETURNING id
            """,
            (
                event_key,
                workflow_id,
                event_name,
                status,
                json.dumps(details, ensure_ascii=True),
            ),
        )
        return cursor.fetchone() is not None


def create_or_get_discovery_run(
    daily_run_id: str, policy_version: str, scheduled_for: str
) -> tuple[str, str]:
    """Create one daily run once and return its stable ID and status."""

    with connect() as connection:
        connection.execute(
            """
            INSERT INTO discovery_runs (daily_run_id, policy_version, scheduled_for)
            VALUES (%s, %s, %s::date)
            ON CONFLICT (daily_run_id) DO NOTHING
            """,
            (daily_run_id, policy_version, scheduled_for),
        )
        row = connection.execute(
            "SELECT daily_run_id, status FROM discovery_runs WHERE daily_run_id = %s",
            (daily_run_id,),
        ).fetchone()
    if row is None:
        raise RuntimeError("discovery run was not persisted")
    return row[0], row[1]


def record_discovery_provider_submission(
    daily_run_id: str, provider: str, external_id: str, estimated_cost_usd: str
) -> tuple[str, str, str]:
    """Persist one provider request once so retries cannot buy another one."""

    with connect() as connection:
        connection.execute(
            """
            INSERT INTO discovery_provider_runs
                (daily_run_id, provider, external_id, estimated_cost_usd, status)
            VALUES (%s, %s, %s, %s::numeric, 'submitted')
            ON CONFLICT (daily_run_id, provider) DO NOTHING
            """,
            (daily_run_id, provider, external_id, estimated_cost_usd),
        )
        row = connection.execute(
            """
            SELECT provider, external_id, status FROM discovery_provider_runs
            WHERE daily_run_id = %s AND provider = %s
            """,
            (daily_run_id, provider),
        ).fetchone()
    if row is None:
        raise RuntimeError("provider submission was not persisted")
    return row[0], row[1], row[2]


def reserve_discovery_provider_submission(
    daily_run_id: str, provider: str, estimated_cost_usd: str
) -> tuple[str, str, str, bool]:
    """Reserve an outbound provider call before it can spend money.

    A retry finding this unfinished reservation must reconcile or ask for help;
    it must never create a second paid request.
    """

    with connect() as connection:
        inserted = connection.execute(
            """
            INSERT INTO discovery_provider_runs
                (daily_run_id, provider, estimated_cost_usd, status)
            VALUES (%s, %s, %s::numeric, 'pending_submission')
            ON CONFLICT (daily_run_id, provider) DO NOTHING
            RETURNING provider, external_id, status
            """,
            (daily_run_id, provider, estimated_cost_usd),
        )
        row = inserted.fetchone()
        if row is None:
            row = connection.execute(
            """
            SELECT provider, external_id, status FROM discovery_provider_runs
            WHERE daily_run_id = %s AND provider = %s
            """,
            (daily_run_id, provider),
            ).fetchone()
    if row is None:
        raise RuntimeError("provider submission reservation was not persisted")
    return row[0], row[1], row[2], bool(inserted.rowcount)


def complete_discovery_provider_submission(
    daily_run_id: str, provider: str, external_id: str
) -> tuple[str, str, str]:
    """Attach the returned provider ID to its existing reservation once."""

    with connect() as connection:
        connection.execute(
            """
            UPDATE discovery_provider_runs
            SET external_id = %s, status = 'submitted', updated_at = NOW()
            WHERE daily_run_id = %s AND provider = %s
              AND status = 'pending_submission' AND external_id = ''
            """,
            (external_id, daily_run_id, provider),
        )
        row = connection.execute(
            """
            SELECT provider, external_id, status FROM discovery_provider_runs
            WHERE daily_run_id = %s AND provider = %s
            """,
            (daily_run_id, provider),
        ).fetchone()
    if row is None:
        raise RuntimeError("provider submission completion was not persisted")
    return row[0], row[1], row[2]


def fetch_leads_by_status(status: str, limit: int = 50) -> list[dict[str, object]]:
    """Query leads by current status for qualification or review."""
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT workflow_id, venue_name, city, venue_type, source_url,
                   website, instagram, email, phone, website_domain,
                   qualification_status, qualification_score, status
            FROM leads
            WHERE status = %s
            ORDER BY created_at ASC
            LIMIT %s
            """,
            (status, limit),
        ).fetchall()
    leads = []
    for r in rows:
        leads.append({
            "workflow_id": r[0],
            "venue_name": r[1],
            "city": r[2],
            "venue_type": r[3],
            "source_url": r[4],
            "website": r[5],
            "instagram": r[6],
            "email": r[7],
            "phone": r[8],
            "website_domain": r[9],
            "qualification_status": r[10],
            "qualification_score": r[11],
            "status": r[12],
        })
    return leads


def update_lead_qualification(
    workflow_id: str,
    qualification_status: str,
    qualification_score: int,
    qualification_reasons: list[str],
    qualification_evidence: dict[str, object],
) -> None:
    """Persist qualification result and timestamp for one lead."""
    with connect() as connection:
        connection.execute(
            """
            UPDATE leads
            SET qualification_status = %s,
                qualification_score = %s,
                qualification_reasons = %s::jsonb,
                qualification_evidence = %s::jsonb,
                qualified_at = NOW(),
                updated_at = NOW()
            WHERE workflow_id = %s
            """,
            (
                qualification_status,
                qualification_score,
                json.dumps(qualification_reasons, ensure_ascii=True),
                json.dumps(qualification_evidence, ensure_ascii=True),
                workflow_id,
            ),
        )


def fetch_leads_for_enrichment_planning(
    statuses: Sequence[str], limit: int = 50
) -> list[dict[str, object]]:
    """Query leads by qualification status for enrichment planning."""
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT workflow_id, venue_name, city, venue_type, source_url,
                   website, instagram, email, phone, website_domain,
                   qualification_status, qualification_score, status
            FROM leads
            WHERE qualification_status = ANY(%s)
            ORDER BY created_at ASC
            LIMIT %s
            """,
            (list(statuses), limit),
        ).fetchall()
    leads = []
    for r in rows:
        leads.append({
            "workflow_id": r[0],
            "venue_name": r[1],
            "city": r[2],
            "venue_type": r[3],
            "source_url": r[4],
            "website": r[5],
            "instagram": r[6],
            "email": r[7],
            "phone": r[8],
            "website_domain": r[9],
            "qualification_status": r[10],
            "qualification_score": r[11],
            "status": r[12],
        })
    return leads


def upsert_enrichment_plan(
    workflow_id: str,
    qualification_status: str,
    steps: list[dict[str, object]],
) -> bool:
    """Insert or update lead enrichment plan. Returns True if created, False if updated."""
    with connect() as connection:
        existing = connection.execute(
            "SELECT workflow_id FROM lead_enrichment_plans WHERE workflow_id = %s",
            (workflow_id,),
        ).fetchone()
        if existing is None:
            connection.execute(
                """
                INSERT INTO lead_enrichment_plans
                    (workflow_id, qualification_status, steps)
                VALUES (%s, %s, %s::jsonb)
                """,
                (workflow_id, qualification_status, json.dumps(steps, ensure_ascii=True)),
            )
            return True
        connection.execute(
            """
            UPDATE lead_enrichment_plans
            SET qualification_status = %s,
                steps = %s::jsonb,
                updated_at = NOW()
            WHERE workflow_id = %s
            """,
            (qualification_status, json.dumps(steps, ensure_ascii=True), workflow_id),
        )
        return False


def fetch_enrichment_plans(
    statuses: Sequence[str], limit: int = 50
) -> list[dict[str, object]]:
    """Fetch lead enrichment plans joined with lead metadata for display."""
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT p.workflow_id, l.venue_name, l.city,
                   p.qualification_status, l.qualification_score, p.steps
            FROM lead_enrichment_plans p
            JOIN leads l ON p.workflow_id = l.workflow_id
            WHERE p.qualification_status = ANY(%s)
            ORDER BY p.created_at ASC
            LIMIT %s
            """,
            (list(statuses), limit),
        ).fetchall()
    plans = []
    for r in rows:
        plans.append({
            "workflow_id": r[0],
            "venue_name": r[1],
            "city": r[2],
            "qualification_status": r[3],
            "qualification_score": r[4],
            "steps": r[5] if isinstance(r[5], list) else json.loads(r[5] or "[]"),
        })
    return plans


def fetch_enrichment_plan(workflow_id: str) -> dict[str, object] | None:
    """Fetch the enrichment plan for a single workflow_id."""
    with connect() as connection:
        row = connection.execute(
            """
            SELECT workflow_id, qualification_status, steps
            FROM lead_enrichment_plans
            WHERE workflow_id = %s
            """,
            (workflow_id,),
        ).fetchone()
    if row is None:
        return None
    return {
        "workflow_id": row[0],
        "qualification_status": row[1],
        "steps": row[2] if isinstance(row[2], list) else json.loads(row[2] or "[]"),
    }


def fetch_enrichment_step_approvals(
    workflow_ids: Sequence[str],
) -> dict[tuple[str, str], dict[str, object]]:
    """Fetch approval records for the given workflow_ids, keyed by (workflow_id, step_name)."""
    if not workflow_ids:
        return {}
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT workflow_id, step_name, approved_by, max_cost_usd, approved_at
            FROM lead_enrichment_step_approvals
            WHERE workflow_id = ANY(%s)
            """,
            (list(workflow_ids),),
        ).fetchall()
    approvals = {}
    for r in rows:
        approvals[(r[0], r[1])] = {
            "workflow_id": r[0],
            "step_name": r[1],
            "approved_by": r[2],
            "max_cost_usd": Decimal(str(r[3])),
            "approved_at": r[4],
        }
    return approvals


def record_enrichment_step_approval(
    workflow_id: str,
    step_name: str,
    approved_by: str,
    max_cost_usd: Decimal,
) -> tuple[dict[str, object], bool]:
    """Insert or retrieve approval record for a planned enrichment step.

    Returns (approval_dict, is_new).
    """
    with connect() as connection:
        existing = connection.execute(
            """
            SELECT workflow_id, step_name, approved_by, max_cost_usd, approved_at
            FROM lead_enrichment_step_approvals
            WHERE workflow_id = %s AND step_name = %s
            """,
            (workflow_id, step_name),
        ).fetchone()
        if existing is not None:
            return (
                {
                    "workflow_id": existing[0],
                    "step_name": existing[1],
                    "approved_by": existing[2],
                    "max_cost_usd": Decimal(str(existing[3])),
                    "approved_at": existing[4],
                },
                False,
            )
        connection.execute(
            """
            INSERT INTO lead_enrichment_step_approvals
                (workflow_id, step_name, approved_by, max_cost_usd)
            VALUES (%s, %s, %s, %s::numeric)
            """,
            (workflow_id, step_name, approved_by, str(max_cost_usd)),
        )
        row = connection.execute(
            """
            SELECT workflow_id, step_name, approved_by, max_cost_usd, approved_at
            FROM lead_enrichment_step_approvals
            WHERE workflow_id = %s AND step_name = %s
            """,
            (workflow_id, step_name),
        ).fetchone()
    if row is None:
        raise RuntimeError("approval record was not persisted")
    return (
        {
            "workflow_id": row[0],
            "step_name": row[1],
            "approved_by": row[2],
            "max_cost_usd": Decimal(str(row[3])),
            "approved_at": row[4],
        },
        True,
    )


def record_manual_enrichment_evidence(
    workflow_id: str,
    step_name: str,
    field: str,
    value: str,
    source_url: str,
    recorded_by: str,
) -> tuple[dict[str, object], str]:
    """Insert or update manual enrichment evidence.

    Returns (evidence_dict, status) where status is 'created', 'already_exists', or 'updated'.
    """
    with connect() as connection:
        existing = connection.execute(
            """
            SELECT workflow_id, step_name, field, value, source_url, recorded_by, recorded_at
            FROM lead_manual_enrichment_evidence
            WHERE workflow_id = %s AND step_name = %s AND field = %s
            """,
            (workflow_id, step_name, field),
        ).fetchone()
        if existing is not None:
            if existing[3] == value and existing[4] == source_url and existing[5] == recorded_by:
                return (
                    {
                        "workflow_id": existing[0],
                        "step_name": existing[1],
                        "field": existing[2],
                        "value": existing[3],
                        "source_url": existing[4],
                        "recorded_by": existing[5],
                        "recorded_at": existing[6],
                    },
                    "already_exists",
                )
            connection.execute(
                """
                UPDATE lead_manual_enrichment_evidence
                SET value = %s,
                    source_url = %s,
                    recorded_by = %s,
                    recorded_at = NOW()
                WHERE workflow_id = %s AND step_name = %s AND field = %s
                """,
                (value, source_url, recorded_by, workflow_id, step_name, field),
            )
            row = connection.execute(
                """
                SELECT workflow_id, step_name, field, value, source_url, recorded_by, recorded_at
                FROM lead_manual_enrichment_evidence
                WHERE workflow_id = %s AND step_name = %s AND field = %s
                """,
                (workflow_id, step_name, field),
            ).fetchone()
            if row is None:
                raise RuntimeError("manual enrichment evidence update failed")
            return (
                {
                    "workflow_id": row[0],
                    "step_name": row[1],
                    "field": row[2],
                    "value": row[3],
                    "source_url": row[4],
                    "recorded_by": row[5],
                    "recorded_at": row[6],
                },
                "updated",
            )

        connection.execute(
            """
            INSERT INTO lead_manual_enrichment_evidence
                (workflow_id, step_name, field, value, source_url, recorded_by)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (workflow_id, step_name, field, value, source_url, recorded_by),
        )
        row = connection.execute(
            """
            SELECT workflow_id, step_name, field, value, source_url, recorded_by, recorded_at
            FROM lead_manual_enrichment_evidence
            WHERE workflow_id = %s AND step_name = %s AND field = %s
            """,
            (workflow_id, step_name, field),
        ).fetchone()
    if row is None:
        raise RuntimeError("manual enrichment evidence insertion failed")
    return (
        {
            "workflow_id": row[0],
            "step_name": row[1],
            "field": row[2],
            "value": row[3],
            "source_url": row[4],
            "recorded_by": row[5],
            "recorded_at": row[6],
        },
        "created",
    )


def fetch_manual_enrichment_evidence(workflow_id: str) -> list[dict[str, object]]:
    """Fetch manual enrichment evidence records for a workflow_id."""
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT workflow_id, step_name, field, value, source_url, recorded_by, recorded_at
            FROM lead_manual_enrichment_evidence
            WHERE workflow_id = %s
            ORDER BY recorded_at ASC
            """,
            (workflow_id,),
        ).fetchall()
    evidence_list = []
    for r in rows:
        evidence_list.append({
            "workflow_id": r[0],
            "step_name": r[1],
            "field": r[2],
            "value": r[3],
            "source_url": r[4],
            "recorded_by": r[5],
            "recorded_at": r[6],
        })
    return evidence_list
