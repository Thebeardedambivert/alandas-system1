# System 1 Go-Live Checklist

Use this when deploying `alandas-system1` into Coolify.

## Before deployment

- Payment status confirmed.
- Coolify dashboard accessible.
- Old Sidy project identified and left untouched.
- `alandas-system1` created as a separate Coolify resource.
- No paid lead tool selected yet.
- No customer messages scheduled for automatic sending.

## Required environment variables

Set these in Coolify:

```text
POSTGRES_USER=alandas
POSTGRES_PASSWORD=<long random password>
POSTGRES_DB=alandas_system1
TEMPORAL_POSTGRES_USER=temporal
TEMPORAL_POSTGRES_PASSWORD=<different long random password>
TEMPORAL_POSTGRES_DB=temporal
TEMPORAL_VERSION=1.27.2
TEMPORAL_ADMINTOOLS_VERSION=1.32.0
TEMPORAL_UI_VERSION=2.39.0
TEMPORAL_ADDRESS=temporal:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=alandas-system1
TEMPORAL_CORS_ORIGINS=http://localhost:8080
TEMPORAL_UI_AUTH_USER=<dedicated-ui-username>
TEMPORAL_UI_AUTH_PASSWORD_HASH=<bcrypt-hash; enable Is Literal>
LOG_LEVEL=info
```

## Recommended deployment path

Use the Git-backed Docker Compose path if possible.

File:

```text
docker-compose.system1.coolify.yml
```

Reason:

It uses normal Docker Compose syntax and can be checked locally before deployment.

## Fallback deployment path

Use Docker Compose Empty only if the code is not connected as a Git-backed app.

File:

```text
docker-compose.system1.coolify-empty.yml
```

Reason:

It includes Coolify `content:` file mounts so the required SQL and Temporal config files can be created from the pasted Compose definition.

## Expected services

After deployment, Coolify should show:

- `postgres`
- `temporal-postgres`
- `temporal`
- `temporal-admin-tools`
- `temporal-ui`
- `temporal-ui-gateway`
- `system1-worker`

## Security checks

- Do not publish Postgres port `5432`.
- Do not publish Temporal port `7233`.
- Do not assign public domains to `postgres`, `temporal-postgres`, `temporal`, `temporal-admin-tools`, `temporal-ui`, or `system1-worker`.
- Assign the public UI domain only to `temporal-ui-gateway`.
- Enable **Force HTTPS** in Coolify Advanced settings before redeploying.
- In a private/incognito browser, confirm that the UI domain prompts for credentials. Confirm that a wrong password does not reveal workflow data.
- Do not paste secrets into screenshots.
- Do not connect Shopify, Meta, WhatsApp, or Dolibarr production writes yet.

## Verification commands

Run inside the worker container:

```bash
python -m system_1.start_sample_workflow
```

Then check Temporal UI for a workflow ID starting with:

```text
alandas-lead-
```

Signal the test workflow:

```bash
temporal workflow signal --workflow-id <workflow-id> --name approve_by_sidy
temporal workflow signal --workflow-id <workflow-id> --name record_sent
```

Check the audit file:

```bash
cat /app/runtime/audit/system1_audit.jsonl
```

Check Postgres:

```bash
psql "$DATABASE_URL" -c "select workflow_id, venue_name, status from leads;"
psql "$DATABASE_URL" -c "select workflow_id, event_name, status from audit_events order by id;"
```

Import the first real lead CSV after the sample workflow passes:

```bash
python -m system_1.import_leads /app/data/system1_leads_template.csv
```

Operate a lead workflow:

```bash
python -m system_1.workflow_cli state <workflow-id>
python -m system_1.workflow_cli approve <workflow-id>
python -m system_1.workflow_cli record-sent <workflow-id>
```

## Done state

System 1 setup is live when:

- all seven services are running
- worker logs show a Temporal connection
- sample workflow starts
- CSV import script starts workflows
- approval signal works
- send-record signal works
- audit event is written to file
- lead row is written to Postgres
- Temporal UI is private behind `temporal-ui-gateway`, and its domain has a verified authentication prompt

## If something fails

Stop at the first failed check.

Do not keep clicking deploy. Read the failing service logs first.

The most likely failures:

- missing environment variable
- password mismatch between Temporal and `temporal-postgres`
- missing file mount when using the standard Compose path without Git-backed files
- old project already using the same exposed domain or port
