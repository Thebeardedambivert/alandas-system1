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
);

CREATE INDEX IF NOT EXISTS leads_website_domain_idx ON leads (website_domain);
CREATE INDEX IF NOT EXISTS leads_instagram_handle_idx ON leads (instagram_handle);
CREATE INDEX IF NOT EXISTS leads_venue_city_key_idx ON leads (venue_city_key);

CREATE TABLE IF NOT EXISTS lead_research_evidence (
    evidence_key TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL REFERENCES leads(workflow_id),
    field TEXT NOT NULL,
    value TEXT NOT NULL,
    source_url TEXT NOT NULL,
    method TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_events (
    id BIGSERIAL PRIMARY KEY,
    event_key TEXT UNIQUE,
    workflow_id TEXT NOT NULL,
    event_name TEXT NOT NULL,
    status TEXT NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
