# Alandas System 1

This repository contains the Alandas System 1 workspace.

System 1 is the locked Layer 1 setup for Alandas Tea Berlin. It is designed to support the first paid service layer without taking ownership away from Sidy Sow or jumping into the full autonomous platform too early.

## What Is Included

- Temporal workflow code for lead handling.
- Coolify deployment files for Sidy's Hetzner server.
- Postgres schema for leads and audit events.
- Lead CSV template and validation script.
- Outreach templates for the EUR 19 discovery tasting box.
- Setup runbook and go-live checklist.
- Strategy documents, diagrams, decks, and audit assets used to design the system.

## Current Status

The local System 1 package is ready for server deployment.

Already verified locally:

- Python unit tests pass.
- Lead CSV validation passes.
- Python files compile.
- Docker Compose renders correctly when environment variables are supplied.
- Environment variable helper prints fresh random passwords for Coolify.

Not yet verified:

- Coolify deployment on Sidy's Hetzner server.
- Worker connection to the live Temporal server.
- Sample workflow visible in Temporal UI.
- Approval and send signals against a live workflow.
- Postgres and audit log writes on the server.

## Main Files

- `alandas/system_1/README.md`: System 1 command center.
- `alandas/system_1/SETUP_RUNBOOK.md`: Full setup order.
- `alandas/system_1/DEPLOYMENT_COOLIFY.md`: Coolify deployment steps.
- `alandas/system_1/STATUS_AUDIT.md`: Current evidence and gaps.
- `alandas/docker-compose.system1.coolify.yml`: Standard Git-backed Compose stack.
- `alandas/docker-compose.system1.coolify-empty.yml`: Paste-ready Coolify Empty stack.
- `alandas/.env.system1.example`: Example environment variables with placeholder secrets.
- `alandas/scripts/system1_generate_env.py`: Prints fresh Coolify-ready environment variables.
- `alandas/scripts/system1_validate_leads.py`: Validates lead CSV files before import.

## Cost Rule

Do not spend money before Sidy approves the exact cost.

Current known position:

- Existing Hetzner server is already paid by Sidy.
- No new server is needed yet.
- Lead tool budget discussed on the call was up to EUR 60.
- Initial service start discussed was EUR 100.

## Security Notes

No real secrets should be committed.

Use `.env.system1.example` only as a template. Generate live values with:

```bash
python alandas/scripts/system1_generate_env.py
```

Paste the generated values into Coolify, not into the repository.

## Next Step

Get Coolify or SSH access for Sidy's Hetzner server, then deploy a separate resource named:

```text
alandas-system1
```

Keep Temporal and Postgres private. Do not expose database port `5432` or Temporal port `7233` publicly.
