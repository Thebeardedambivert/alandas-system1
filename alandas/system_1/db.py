"""Database helpers for Alandas System 1."""

from __future__ import annotations

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
