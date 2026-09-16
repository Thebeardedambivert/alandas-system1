# Alandas System 1 Setup Runbook

This is the working order for getting System 1 fully set up.

## Goal

Put the whole locked Layer 1 into Sidy's existing Hetzner and Coolify setup without mixing it into the old Sidy platform.

System 1 means:

- qualified cafe leads
- enrichment fields captured in one CSV shape
- outreach drafts for Sidy's approval
- one Temporal workflow per lead
- clear approval and send signals
- database audit trail
- file audit trail
- private server networking

## Cost rule

Do not spend money before Sidy approves the exact cost.

Current known cost position:

- Existing Hetzner server: already paid by Sidy.
- New server: not needed yet.
- Lead tools: discussed cap was up to EUR 60.
- Cyril setup work: EUR 100 start was discussed on the call.

## Phase 1, local package

Status: ready.

Evidence:

- Scope is captured in `LOCKED_SCOPE.md`.
- Access needs are captured in `ACCESS_CHECKLIST.md`.
- Lead data shape is captured in `LEAD_SCHEMA.md`.
- Outreach copy is captured in `OUTREACH_TEMPLATES.md`.
- Temporal workflow is specified in `TEMPORAL_WORKFLOW.md`.
- Coolify deployment steps are captured in `DEPLOYMENT_COOLIFY.md`.
- Live checklist is captured in `GO_LIVE_CHECKLIST.md`.
- Worker code exists in this folder.
- Database schema exists in `../deployment/postgres/init/01-system1-schema.sql`.
- Compose files exist at the project root.

## Phase 2, Coolify deployment

Status: waiting for live access.

Needed from the browser or server:

- Coolify dashboard URL or opened Coolify tab.
- Access to create a new Coolify resource.
- Confirmation that the existing server is still `sidy-platform-prod`.
- Confirmation that no public database or Temporal ports are exposed.

Deployment choice:

- Use `../docker-compose.system1.coolify.yml` if Coolify can deploy from this Git workspace.
- Use `../docker-compose.system1.coolify-empty.yml` if pasting the stack into Coolify's Docker Compose Empty resource.

Secret setup:

- Use `python scripts/system1_generate_env.py` to print random passwords for Coolify.
- Paste those values into Coolify's Environment Variables screen.
- Do not commit the generated values.

Naming rule:

- Create a separate project or resource named `alandas-system1`.
- Do not edit the previous project unless Sidy explicitly approves it.

## Phase 3, server verification

Status: not yet done.

Done means these checks pass on the server:

1. All containers are running.
2. The worker connects to Temporal.
3. A sample workflow starts.
4. The workflow appears in Temporal UI.
5. Sidy approval signal works.
6. Send-record signal works.
7. A lead row is written to Postgres.
8. An audit event is written to the JSONL audit file.
9. Temporal UI is private or protected.
10. Postgres and Temporal ports are not public.

## Phase 4, first real lead batch

Status: waiting for Sidy's target market choice and lead tool approval.

First batch rule:

- Start with one city and one venue type.
- Use a small batch first.
- Validate the CSV before importing it.
- Let Sidy approve the message before any contact goes out.

Commands:

```bash
python scripts/system1_validate_leads.py data/system1_leads_template.csv
python -m system_1.import_leads /app/data/system1_leads_template.csv
python -m system_1.workflow_cli state <workflow-id>
python -m system_1.workflow_cli approve <workflow-id>
python -m system_1.workflow_cli record-sent <workflow-id>
```

## Current blocker

The local package can be prepared and tested here.

The live setup cannot be honestly called done until Coolify or SSH access is available. This is like packing a parcel and printing the label. The parcel is ready, but it has not yet been handed to the courier.
