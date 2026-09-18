# Gemini Task Card: <task ID and name>

<!--
This is the standard task-card template for Gemini builder tasks in Alandas System 1.
Codex completes this card before Gemini begins work. Cyril alone approves tasks requiring external action.
-->

## Objective

<!-- State the concrete, single-focus objective of this task. -->
<State the exact deliverable or change to be created.>

## Business reason

<!-- Explain why this task is needed for Alandas System 1. -->
<Explain the business context, e.g. qualification accuracy, audit reliability, commercial safety.>

## Approved scope

<!-- List the specific, bounded boundaries of what may be modified or created. -->
- <Bounded action 1>
- <Bounded action 2>
- Follow the approved implementation plan task specification exactly.
- Make one local commit only.

## Explicit non-goals

<!-- List what must NOT be done in this task. -->
- Do not modify files outside the allowed files list.
- Do not begin subsequent tasks.
- Do not push, deploy, add credentials, enable discovery, create a Temporal schedule, contact a provider, spend money, or send a customer message.

## Preconditions and authority

<!-- Authority requirements and preceding state. -->
- **Authority:** Cyril has explicitly approved this task. Codex plans, reviews, and independently verifies. Gemini implements locally.
- **Preconditions:** <List preceding tasks, verified branch state, or prerequisites that must be satisfied before starting.>

## Allowed files

<!-- Enumerate the exact files that Gemini is permitted to touch. -->
- `<exact/path/to/file1>`
- `<exact/path/to/file2>` (if applicable)

*Gemini must not create, edit, or delete any file outside this list.*

## Required reading

<!-- Documents Gemini must read in full before inspecting code or editing files. -->
1. `AGENTS.md`
2. `alandas/system_1/CURRENT_PROJECT_STATE.md`
3. `alandas/system_1/SESSION_HANDOFF_2026-09-17.md`
4. `alandas/system_1/LOCKED_SCOPE.md`
5. `alandas/system_1/GEMINI_BUILDER_PROTOCOL.md`
6. `alandas/docs/superpowers/specs/2026-09-18-gemini-codex-operating-model-design.md`
7. <Task-specific plan, spec, or source file>

## Required skills and how to use them

<!-- List the mandatory process skills and any domain skills. -->
- `using-superpowers` — Identify all applicable skills before taking action.
- `brainstorming` — Design the smallest change and confirm scope before editing.
- `using-git-worktrees` — Use an isolated worktree/branch; never work on `master`.
- `test-driven-development` — Write failing test first, observe failure, implement minimal passing code.
- `systematic-debugging` — Investigate root causes before proposing or applying fixes.
- `verification-before-completion` — Execute exact verification commands and inspect evidence before claiming completion.
- `requesting-code-review` — Format structured handoff for Codex review.
- <Domain skills as applicable, e.g. durable-systems-engineering, ai-security-governance, platform-operations>

### Skill-Tool Fallback Rule
If the active session runtime cannot register or load a required skill via the skill tool:
- Gemini must **not** attempt to install, copy, symlink, or modify skill directories.
- Gemini must directly read the exact `SKILL.md` file from its filesystem path (e.g. `C:\Users\Cyril Uzochukwu\.codex\skills\<skill-name>\SKILL.md`) and follow its instructions as written.
- Gemini must report that distinction honestly in the handoff. Gemini must **never fabricate a successful tool invocation**.
- If a required skill is missing from both the tool loader and the disk, Gemini must stop immediately and mark the task `BLOCKED`.

## Test-first contract

<!-- Define the TDD requirement for this task. -->
Gemini must follow the strict test-first flow:
```text
write focused test -> run and observe expected failure -> write the smallest change -> run focused test -> run task-wide verification
```
- For code tasks: Write the minimal failing unit or integration test before touching implementation code. Capture and report the failing test output.
- For documentation tasks: Run syntax, structure, or content-consistency verification commands (e.g. `git diff --check`, `rg` regex checks) before and after changes.

## Acceptance criteria

<!-- Specific, unambiguous conditions that define task completion. -->
- [ ] <Criterion 1>
- [ ] <Criterion 2>
- [ ] All verification commands pass with exit code 0.
- [ ] Local git history contains exactly one clean commit with the required message.

## Exact verification commands

<!-- Exact commands Codex and Gemini will run to verify the work. -->
```powershell
<Verification command 1>
git diff --check
git status --short
```

## External-effect stop conditions

<!-- Explicit list of prohibited actions. -->
Gemini must immediately halt execution and mark the task **`BLOCKED`** if any of these are needed or encountered:
- **Push:** Never execute `git push` or modify remote refs.
- **Deploy:** Never deploy to Coolify, restart production containers, or alter Docker Compose.
- **Credentials:** Never enter, view, request, or commit secrets, tokens, or private keys.
- **Provider Activation:** Never set `SYSTEM1_DISCOVERY_ENABLED=true`, call Apify or Outscraper, or run external scrapers.
- **Temporal:** Never register real Temporal schedules or trigger unapproved workflow executions.
- **Spend:** Never incur financial cost or consume paid API credits.
- **Dolibarr:** Never write to Dolibarr CRM, modify stock, or generate invoices.
- **Hermes:** Never integrate Hermes delivery or parse live orders.
- **OpenReply / Social:** Never automate Instagram or send social DMs.
- **Shopify / Meta:** Never alter Shopify production settings or run Meta ad campaigns.
- **Customer Outreach:** Never send emails, WhatsApp messages, or customer outreach.

## Required local commit message

<!-- Exact commit message format. -->
```text
<type>: <concise description matching task objective>
```
*Local commit only. Do not push.*

## Required handoff

<!-- Exact handoff format to return to Codex. -->
Upon completion, Gemini must report only:
1. **Worktree path and branch:** Full filesystem path of the isolated worktree and branch name.
2. **Skill-file paths read:** Exact list of skill files read directly from disk or invoked via tools.
3. **Failing-test evidence:** Exact output showing the test failing for the expected reason (for code tasks).
4. **Local commit hash:** Commit SHA of the local commit.
5. **Changed files:** Exact list of files created or modified.
6. **Exact verification output and exit status:** Full commands executed, raw outputs, and exit codes.
7. **Confirmation of zero external side effects:** Confirmation that nothing was pushed, deployed, enabled, scheduled, or spent.
8. **Risks or unresolved gaps:** Technical risks, boundary questions, or follow-up items for Codex.

*Stop after returning this handoff. Await Codex review verdict before starting any other task.*
