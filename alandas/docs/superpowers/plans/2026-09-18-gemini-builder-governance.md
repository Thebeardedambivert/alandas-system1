# Gemini Builder Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create reusable Alandas documents that let Gemini make scoped local changes while Codex reviews and Cyril retains every external approval.

**Architecture:** Three Markdown documents live in `system_1/`: a builder protocol, a task-card template, and a strict Layer 1 backlog. This plan changes no application code, Coolify setting, provider, schedule, or external service.

**Tech Stack:** Markdown and Git.

**Spec:** `docs/superpowers/specs/2026-09-18-gemini-codex-operating-model-design.md`

## Global Constraints

- Read `AGENTS.md`, `system_1/CURRENT_PROJECT_STATE.md`, `system_1/SESSION_HANDOFF_2026-09-17.md`, and `system_1/LOCKED_SCOPE.md` before editing.
- Use one isolated worktree/branch and make local commits only; never edit or commit directly on `master`.
- Cyril alone approves pushes, deployments, credentials, provider activation, spending, and customer-facing actions.
- Do not put secrets, token-bearing URLs, or customer data in any document.
- Gemini must read approved `SKILL.md` files directly when its skill tool cannot resolve them. It must report that distinction honestly and never fabricate a successful tool invocation.
- Preserve the exclusions: production Dolibarr writes, Hermes delivery integration, OpenReply/Instagram automation, Shopify production changes, Meta ads, autonomous messaging, and unapproved spend.

---

### Task 1: Create the Gemini builder protocol

**Files:**
- Create: `system_1/GEMINI_BUILDER_PROTOCOL.md`
- Read: `docs/superpowers/specs/2026-09-18-gemini-codex-operating-model-design.md`
- Read: `system_1/CURRENT_PROJECT_STATE.md`
- Read: `system_1/LOCKED_SCOPE.md`
- Test: `git diff --check`

**Interfaces:**
- Consumes: Approved operating-model design and current Layer 1 state.
- Produces: Authority and handoff rules that every Gemini task card references.

- [ ] **Step 1: Read the inputs and inspect the working tree**

Run:

```powershell
Get-Content -Raw 'docs\superpowers\specs\2026-09-18-gemini-codex-operating-model-design.md'
Get-Content -Raw 'system_1\CURRENT_PROJECT_STATE.md'
Get-Content -Raw 'system_1\LOCKED_SCOPE.md'
git status --short
```

Expected: Existing untracked files are listed but not staged, deleted, or edited.

- [ ] **Step 2: Write the protocol with these exact sections**

```markdown
# Gemini Builder Protocol — Alandas System 1

## Authority
## Required reading before every task
## Skill preflight and direct-file fallback
## Isolated branch and local-commit rule
## External-effect stop conditions
## Test-first, debugging, and verification fallback procedures
## Mandatory handoff format
## Codex review verdicts
```

The authority table must say: Gemini edits only allowed task-card files and makes local commits; Codex plans/reviews/verifies; Cyril alone approves external actions; Sidy approves commercial facts and customer messages.

The external-effect stop list must explicitly prohibit: push, deployment, credentials, provider activation/calls, real Temporal schedules, spending, production Dolibarr writes, Hermes delivery integration, Instagram/OpenReply, Shopify changes, Meta ads, and customer-message sending.

The fallback procedures must contain these literal flows:

```text
Test-first: write focused test -> run and observe expected failure -> write the smallest change -> run focused test -> run task-wide verification.
Debugging: capture exact error -> reproduce it -> inspect recent changes and component boundaries -> state one hypothesis -> test one minimal change.
Verification: report exact commands, exit status, changed files, and remaining risks before committing.
```

- [ ] **Step 3: Verify the protocol**

Run:

```powershell
rg -n "push|deploy|credential|provider|Temporal|Dolibarr|Hermes|OpenReply|Shopify|Meta|customer" system_1/GEMINI_BUILDER_PROTOCOL.md
git diff --check
```

Expected: All listed boundaries are present and `git diff --check` exits 0.

- [ ] **Step 4: Commit only the protocol**

Run:

```powershell
git add system_1/GEMINI_BUILDER_PROTOCOL.md
git commit -m "docs: add gemini builder protocol"
```

Expected: One local commit; do not push.

### Task 2: Create the reusable Gemini task-card template

**Files:**
- Create: `system_1/GEMINI_TASK_TEMPLATE.md`
- Read: `system_1/GEMINI_BUILDER_PROTOCOL.md`
- Read: `docs/superpowers/specs/2026-09-18-gemini-codex-operating-model-design.md`
- Test: `git diff --check`

**Interfaces:**
- Consumes: Task authority, safety, and handoff requirements from the protocol.
- Produces: A copyable card Codex completes before Gemini changes anything.

- [ ] **Step 1: Read the protocol and check the prior commit**

Run:

```powershell
Get-Content -Raw 'system_1\GEMINI_BUILDER_PROTOCOL.md'
git log -1 --oneline
git status --short
```

Expected: The protocol is in the local history and unrelated untracked files are untouched.

- [ ] **Step 2: Write the template with these exact headings**

```markdown
# Gemini Task Card: <task ID and name>

## Objective
## Business reason
## Approved scope
## Explicit non-goals
## Preconditions and authority
## Allowed files
## Required reading
## Required skills and how to use them
## Test-first contract
## Acceptance criteria
## Exact verification commands
## External-effect stop conditions
## Required local commit message
## Required handoff
```

The template must require Gemini to report branch/worktree path, read skill-file paths, failing-test evidence, final verification output, commit hash, changed files, and unresolved risks. It must state that a missing skill-tool registration requires the direct-file fallback or a `BLOCKED` result, never a fabricated invocation.

- [ ] **Step 3: Verify the template**

Run:

```powershell
rg -n "Objective|Allowed files|Verification|stop|push|deploy|provider|spend|handoff" system_1/GEMINI_TASK_TEMPLATE.md
git diff --check
```

Expected: Every heading and safety boundary is present; `git diff --check` exits 0.

- [ ] **Step 4: Commit only the template**

Run:

```powershell
git add system_1/GEMINI_TASK_TEMPLATE.md
git commit -m "docs: add gemini task template"
```

Expected: One local commit; do not push.

### Task 3: Create the strict Layer 1 Gemini backlog

**Files:**
- Create: `system_1/GEMINI_LAYER1_BACKLOG.md`
- Read: `system_1/GEMINI_BUILDER_PROTOCOL.md`
- Read: `system_1/GEMINI_TASK_TEMPLATE.md`
- Read: `system_1/CURRENT_PROJECT_STATE.md`
- Read: `system_1/LOCKED_SCOPE.md`
- Test: `git diff --check`

**Interfaces:**
- Consumes: Layer 1 scope, discovery controls, and the protocol/template.
- Produces: Ordered task-card source with owners, prerequisites, skills, and stop conditions.

- [ ] **Step 1: Read scope and state**

Run:

```powershell
Get-Content -Raw 'system_1\CURRENT_PROJECT_STATE.md'
Get-Content -Raw 'system_1\LOCKED_SCOPE.md'
Get-Content -Raw 'system_1\GEMINI_BUILDER_PROTOCOL.md'
Get-Content -Raw 'system_1\GEMINI_TASK_TEMPLATE.md'
git status --short
```

Expected: Discovery is described as disabled. No task assumes providers are configured or approved.

- [ ] **Step 2: Write the backlog table and ordered rows**

Use this exact table header:

```markdown
| ID | Task | Owner | Preconditions | Gemini role | Required skills | Stop condition | Done evidence |
```

Include these rows:

```text
L1-01 Provider configuration readiness — Cyril enters Coolify values directly; Gemini has no secret access; discovery stays disabled.
L1-02 Dashboard estimate and approval record — Cyril records exact displayed amounts and approves them; Gemini does not infer a price or trigger a run.
L1-03 Manual discovery-run audit — only after Cyril-approved run; Gemini inspects supplied records and makes only scoped test-first fixes. Skills: durable-systems-engineering, systematic-debugging, ai-security-governance.
L1-04 Commercial-fact record and draft safeguards — only after Sidy confirms price, credit policy, stock, and shipping. Skills: copywriting, compliance-handling, test-driven-development.
L1-05 Dolibarr/Hermes access-gap and repair-plan documentation — only after normal-screen evidence or safe test access; no production write. Skills: ai-security-governance, platform-operations.
L1-06 Read-only Dolibarr capability check — only after safe test access and field agreement; no prospect, stock, invoice, or customer write. Skills: platform-operations, ai-security-governance, test-driven-development, systematic-debugging.
```

Add an **Out of scope** section naming production Dolibarr writes, Hermes delivery integration, OpenReply/Instagram automation, Shopify changes, Meta ads, autonomous customer messaging, and unapproved spend.

- [ ] **Step 3: Verify no scope leak**

Run:

```powershell
rg -n "L1-0|Out of scope|Dolibarr|Hermes|OpenReply|Shopify|Meta|spend|disabled" system_1/GEMINI_LAYER1_BACKLOG.md
git diff --check
```

Expected: Six Layer 1 rows and all exclusions are present; no row authorizes an external action.

- [ ] **Step 4: Commit only the backlog**

Run:

```powershell
git add system_1/GEMINI_LAYER1_BACKLOG.md
git commit -m "docs: add gemini layer1 backlog"
```

Expected: One local commit; do not push.

## Plan self-review

### Spec coverage

- Task 1 implements authority, local-commit, safety, skill-fallback, and review rules.
- Task 2 implements repeatable scoped task definition and verifiable Gemini handoff.
- Task 3 implements strict Layer 1 sequencing, user-only approvals, and exclusions.

### Placeholder scan

The angle-bracket title in Task 2 is an intentional reusable template field. There are no unfinished plan steps or unspecified verification commands.

### Boundary consistency

All tasks are documentation-only. Each creates one file, makes one local commit, and prohibits external effects. Task 2 depends on Task 1; Task 3 depends on Tasks 1 and 2.
