"""Database helpers for Alandas System 1."""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg import Connection

from system_1.models import LeadInput


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
                seat_estimate, fit_score, fit_reason, status, updated_at
            )
            VALUES (
                %(workflow_id)s, %(venue_name)s, %(city)s, %(venue_type)s,
                %(source_url)s, %(website)s, %(instagram)s, %(email)s,
                %(phone)s, %(impressum_url)s, %(decision_maker)s,
                %(seat_estimate)s, %(fit_score)s, %(fit_reason)s,
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
                "status": status,
            },
        )


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
