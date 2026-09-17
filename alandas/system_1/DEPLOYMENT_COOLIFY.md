# Deploy System 1 With Coolify

This is the deployment path for Sidy's Hetzner server.

Server seen in Hetzner:

- name: `sidy-platform-prod`
- public IP: `95.216.205.99`
- type: `CX33`
- disk: `80 GB`
- region: Helsinki

## Cost

No new server cost is expected if we use the existing Hetzner server.

Paid tools are separate. The call budget was EUR 60 max for tools at the start. Do not spend from that budget until the exact tool and price are approved.

## What gets deployed

System 1 deploys as a separate Coolify Docker Compose service:

- `postgres`: Alandas app database
- `temporal-postgres`: Temporal state database
- `temporal`: Temporal server
- `temporal-admin-tools`: Temporal CLI tools
- `temporal-ui`: Temporal web UI, private behind the gateway
- `temporal-ui-gateway`: password gate for the Temporal web UI
- `system1-worker`: Python worker for lead workflows

## Coolify steps

1. Open Coolify on `sidy-platform-prod`.
2. Create a new project or resource named `alandas-system1`.
3. Best path: choose a Git-backed Docker Compose application and use `docker-compose.system1.coolify.yml`.
4. If using `Docker Compose Empty`, paste the contents of `docker-compose.system1.coolify-empty.yml`.
5. Save and let Coolify parse the services.
6. Open Environment Variables.
7. Add values from `.env.system1.example`.
8. Replace both password values with long random passwords.
   To generate a paste-ready block locally, run:

```bash
python scripts/system1_generate_env.py
```

9. Review Persistent Storages. Confirm these volumes appear:
   - `system1-postgres-data`
   - `temporal-postgres-data`
   - `system1-runtime`
10. If using `Docker Compose Empty`, confirm the Source Compose contains file mounts with `content:` for:
   - `/docker-entrypoint-initdb.d/01-system1-schema.sql`
   - `/etc/temporal/config/dynamicconfig/development-sql.yaml`
11. Deploy.
12. Check logs for `system1-worker`.

## Network rule

Keep Temporal private.

Do not expose:

- Postgres port `5432`
- Temporal port `7233`

Do not assign a public domain to `postgres`, `temporal-postgres`, `temporal`, `temporal-admin-tools`, `temporal-ui`, or `system1-worker`.

`temporal-ui-gateway` is the only service that may have a public domain. It requires credentials before it forwards requests to the private Temporal UI.

## Protect Temporal UI before use

This gateway is necessary because the current Coolify version does not show its built-in authentication control for this Compose application.

1. Update Coolify from the Git revision that contains `temporal-ui-gateway` (or reload the changed Compose file).
2. Choose a dedicated UI username and a long unique password. Store the password in Sidy's approved password manager, not in chat, screenshots, or Git.
3. Generate a Base64-encoded bcrypt password hash locally. This command prompts for the password without echoing it, then prints only the encoded hash. It avoids Coolify expanding the `$` characters inside bcrypt values:

```bash
docker run --rm -it caddy:2.8.4-alpine sh -c 'caddy hash-password --algorithm bcrypt | base64 | tr -d "\\r\\n"; echo'
```

4. In Coolify **Environment Variables**, set:

```text
TEMPORAL_UI_AUTH_USER=<dedicated-ui-username>
TEMPORAL_UI_AUTH_PASSWORD_HASH_B64=<the-command-output>
```

Only the Base64-encoded bcrypt hash goes into Coolify. Do not store the plaintext password in the repository.

5. In **Configuration** > **General**, remove every existing service domain.
6. Assign the Temporal UI URL only to `temporal-ui-gateway`.
7. In **Advanced**, enable **Force HTTPS** and save it.
8. Redeploy the Compose application.
9. In a private/incognito browser window, open the gateway URL. The browser must ask for the new credentials before the Temporal page appears.
10. Test once with an incorrect password. It must return an authentication failure and must not show workflow data.

If the gateway does not start, inspect its logs and the two authentication environment variables. Do not restore a direct public `temporal-ui` domain as a troubleshooting shortcut.

## First verification

After deployment:

1. Open the `system1-worker` logs.
2. Confirm it connects to Temporal.
3. Run the sample workflow from the worker container:

```bash
python -m system_1.start_sample_workflow
```

4. Open Temporal UI.
5. Confirm a workflow with ID starting `alandas-lead-` exists.
6. Signal approval only for test data:

```bash
temporal workflow signal --workflow-id <workflow-id> --name approve_by_sidy
temporal workflow signal --workflow-id <workflow-id> --name record_sent
```

7. Confirm the audit file exists inside the worker volume:

```bash
cat /app/runtime/audit/system1_audit.jsonl
```

8. Confirm Postgres has the workflow row:

```bash
psql "$DATABASE_URL" -c "select workflow_id, venue_name, status from leads;"
```

9. Import leads from CSV after the sample workflow passes:

```bash
python -m system_1.import_leads /app/data/system1_leads_template.csv
```

10. Operate the workflow:

```bash
python -m system_1.workflow_cli state <workflow-id>
python -m system_1.workflow_cli approve <workflow-id>
python -m system_1.workflow_cli record-sent <workflow-id>
```

## Failure rules

- If the worker cannot connect to Temporal, check `TEMPORAL_ADDRESS`.
- If Temporal cannot start, check the `temporal-postgres` password and logs.
- If a volume is missing, stop before using the stack. Persistence is required.
- If an old Sidy project is running on the same server, do not edit it.

## Done means

Setup is done when:

- all containers are running
- worker connects to Temporal
- sample workflow starts
- CSV import starts lead workflows
- approval signal works
- send-record signal works
- audit log is written
- lead row is written to Postgres
- no public database or Temporal port is exposed
- Temporal UI asks for credentials before it exposes workflow metadata
