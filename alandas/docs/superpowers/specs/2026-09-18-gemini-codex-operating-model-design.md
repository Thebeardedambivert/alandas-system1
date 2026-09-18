# Gemini Builder and Codex Release-Gate Operating Model

**Status:** Approved design; implementation plan not yet written
**Date:** 2026-09-18
**Applies to:** Alandas System 1 and future tasks in this workspace

## Purpose

Use Gemini as the scoped implementation agent while Codex plans work, reviews
changes, and independently verifies results. Cyril remains the authority for
all external or irreversible actions.

This reduces Codex token use on implementation while preserving a separate
quality and safety gate before code is pushed or deployed.

## Roles and authority

| Role | Owns | May do | Must not do |
|---|---|---|---|
| Cyril | Business decisions and external authority | Approve scope, pushes, deployments, credentials, provider use, spending, and customer-facing actions | Delegate those approvals implicitly |
| Gemini | Scoped implementation | Read the approved task context, edit only allowed files in an isolated branch/worktree, add tests, run local checks, and make local commits | Push, deploy, force-push, add secrets, change Coolify, enable providers, spend money, create a real schedule, or send a customer message |
| Codex | Planning, review, and release gate | Write task cards, inspect commits/diffs, run independent checks, identify risks, and accept/reject work with evidence | Implement ordinary scoped features, or take any unapproved external action |
| System 1 / Temporal | Durable approved process execution | Run the deployed workflow and preserve state/audit records | Bypass Sidy approval or feature-flag/cost controls |
| Sidy | Customer-message approval and business facts | Approve messages and confirm commercial facts | Be treated as a verified integration or technical access grant |

## Required workflow

```text
Cyril approves a bounded task
-> Codex writes a task card
-> Gemini reads the required context and selected skills
-> Gemini implements in an isolated branch/worktree and commits locally
-> Codex reviews the commit and independently verifies it
-> Gemini fixes named findings, if any
-> Codex issues an evidence-based accept/reject decision
-> Cyril alone approves push, deployment, credentials, provider use, or spend
```

One task card covers one coherent change. Gemini and Codex must not edit the
same files concurrently.

## Context Gemini must load for every task

Before changing anything, Gemini must read:

1. The workspace `AGENTS.md`.
2. `system_1/CURRENT_PROJECT_STATE.md`.
3. `system_1/SESSION_HANDOFF_2026-09-17.md`.
4. `system_1/LOCKED_SCOPE.md`.
5. The task card, target source files, and relevant tests.
6. `git status` and the relevant recent commits.

File access is not project understanding. These documents are the task's job
sheet and safety boundary.

## Mandatory Gemini skill sequence for code tasks

| Stage | Skill | Required use |
|---|---|---|
| Start | `using-superpowers` | Identify every relevant skill before acting. |
| Design | `brainstorming` | State the smallest design, scope, and test approach; wait for approval before editing. |
| Isolation | `using-git-worktrees` | Use one isolated worktree/branch; never work directly on `master`. |
| Build | `test-driven-development` | Add a focused failing test, observe the expected failure, then make the smallest change. |
| Failure | `systematic-debugging` | Trace the observed cause before proposing a fix; test one hypothesis at a time. |
| Final checks | `verification-before-completion` | Run the full task checks and read the output before claiming success or committing. |
| Handoff | `requesting-code-review` | Report commit hash, changed files, checks run, risks, and known gaps. |

Domain skills are selected per task. Examples include `ai-security-governance`
for secrets/external effects, `durable-systems-engineering` for Temporal and
retry/idempotency work, `platform-operations` for Coolify or Docker work,
`lead-qualification` for fit rules, `copywriting` for outreach drafts, and
`compliance-handling` for opt-out/delivery behaviour.

## Task-card contract

Every Gemini task card must state:

- Objective and business reason.
- Allowed files and explicit non-goals.
- Required context files and skills.
- Acceptance criteria and exact verification commands.
- External-effect boundary: credentials, providers, schedules, deploys,
  customer messages, and spending are prohibited unless Cyril separately
  approves them.
- Required handoff: local commit hash, summary, test output, and unresolved
  risks.

Codex reviews against the task card, not merely whether code looks plausible.

## Review verdicts

Codex returns exactly one practical result:

- **Accepted:** The implementation is in scope and independently verified.
- **Changes requested:** Specific findings identify the file, location, risk,
  and required correction.
- **Blocked:** Missing access, business decision, safe test data, or explicit
  user approval prevents safe progress.

No verdict authorizes a push, deployment, credential entry, provider activation,
spending, or customer message without Cyril's separate instruction.

## Model-use policy

Gemini carries normal implementation exploration and coding. Codex is used for
the initial task plan, architecture/safety decisions, review, and independent
verification. Keep Codex context narrow: task card, relevant files, Gemini's
commit/diff, and test evidence rather than the entire repository for every
task.

Use high reasoning effort for Codex planning, risk review, and release-gate
decisions. Do not use it for routine status messages. One normal task gets one
Gemini implementation pass and one Codex review pass; repeated failures return
to root-cause analysis instead of adding unchecked attempts.

## Layer 1 delegation boundary

Gemini may work on the strict Layer 1 tasks that produce a validated lead batch,
safe research/enrichment behaviour, Sidy-approved draft patterns, documented
access gaps, and a Dolibarr/Hermes repair plan.

Gemini must not implement the currently out-of-scope work: production Dolibarr
writes, Hermes delivery integration, OpenReply/Instagram automation, Shopify
production changes, Meta ads, or autonomous customer messaging.

## Success measures

The model split is working when:

- Every change has a task card and isolated local commit.
- No Gemini task creates an external side effect.
- Codex can reproduce the stated test evidence independently.
- Review findings are precise enough for one corrective Gemini pass.
- Cyril makes every push, deployment, credential, provider, spend, and
  customer-message decision explicitly.
