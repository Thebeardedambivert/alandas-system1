# Alandas System 1 Command Center

System 1 is the first paid service layer for Alandas.

It does not try to build the full autonomous platform. It starts with the work Sidy verbally accepted on the last call:

- generate qualified cafe leads
- enrich leads with contact details
- draft outreach for the EUR 19 discovery tasting box
- keep Sidy in control of WhatsApp replies
- prepare the Dolibarr and Hermes repair path
- use Sidy's Hetzner server if it is available

## Current status

Status: Pending payment and access.

Locked by call:

- Alandas remains Sidy's business. This is paid service work, not equity.
- Start with Layer 1 only.
- Initial budget discussed: EUR 100 service start plus up to EUR 60 for lead tools.
- Tool costs must be named before they are spent.
- Sidy should send Meta Business screenshots before any Meta setup decision.
- Sidy's Hetzner server may be used.

Not locked yet:

- payment received
- exact lead tool
- Shopify access
- Dolibarr access
- Hetzner credentials
- Meta Business status
- production deployment date

## Files

- `LOCKED_SCOPE.md`: what System 1 includes and excludes
- `ACCESS_CHECKLIST.md`: what Sidy needs to send
- `LEAD_SCHEMA.md`: required fields for the first lead batch
- `OUTREACH_TEMPLATES.md`: human-approved messages for cafes
- `TEMPORAL_WORKFLOW.md`: the Layer 1 workflow and signal rules
- `DEPLOYMENT_COOLIFY.md`: Coolify deployment steps for Hetzner
- `GO_LIVE_CHECKLIST.md`: exact checks for deploying into Coolify
- `STATUS_AUDIT.md`: current setup evidence and remaining live checks
- `SETUP_RUNBOOK.md`: the full setup order from local package to live verification
- `../docker-compose.system1.coolify.yml`: standard Coolify Git-backed stack
- `../docker-compose.system1.coolify-empty.yml`: paste-ready Coolify Empty stack
- `../.env.system1.example`: environment variable template
- `../data/system1_leads_template.csv`: starter CSV for the first lead batch
- `../scripts/system1_generate_env.py`: prints random environment variables for Coolify
- `../scripts/system1_validate_leads.py`: offline validator for lead CSVs
- `../tests/test_system1_core.py`: offline tests for the pure lead logic
- `import_leads.py`: starts one Temporal workflow per valid CSV row
- `workflow_cli.py`: approves, rejects, records sends, and checks workflow state

## First execution order

1. Confirm payment and access status.
2. Fill `data/system1_leads_template.csv` with the first target venues.
3. Run `python scripts/system1_validate_leads.py data/system1_leads_template.csv`.
4. Fix any invalid rows.
5. Draft outreach from `OUTREACH_TEMPLATES.md`.
6. Send drafts to Sidy for approval before any customer contact.

## Operating rule

System 1 can suggest. Sidy sends.

That one rule protects the brand, the relationship with cafe owners, and the legal risk around product claims.

## Operations security rule

Temporal UI shows workflow and lead-operation metadata. Only `temporal-ui-gateway` may have a public domain. It requires a username and bcrypt password hash from Coolify environment variables before it forwards traffic to the private `temporal-ui` service. Verify the login prompt in a private browser before using it.
