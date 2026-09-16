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
);

CREATE TABLE IF NOT EXISTS audit_events (
    id BIGSERIAL PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    event_name TEXT NOT NULL,
    status TEXT NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
