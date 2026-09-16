name: skill-vetter
description: Security auditing protocol for AI skills. Use this skill to pre-vet any new skill or plugin before installation, especially those from third-party sources (GitHub, ClawHub, etc.). It scans for "Red Flags" like unauthorized network calls, credential access (SSH/AWS keys), code obfuscation, or suspicious use of eval/exec. It outputs a risk rating (LOW, MEDIUM, HIGH, EXTREME) and a structured security report.

# Skill Vetting Protocol (skill-vetter)

This skill implements a strict security auditing process to protect the host system and user credentials from malicious or poorly-written AI skills.

## When to Use
- Before installing any new skill with `npm`, `cargo`, `pip`, or manual `write_file`.
- When reviewing a skill's `SKILL.md` or source code.
- When a user asks "Is this skill safe to install?".

## The 4-Step Audit Process

### 1. Source & Reputation Check
- **Author**: Is the author known or verified?
- **Popularity**: GitHub stars > 10? (Tier 2/3 requirement)
- **Recency**: Last update < 6 months ago?
- **Documentation**: Is there a clear `SKILL.md` and `README.md`?

### 2. Mandatory Code Audit (Red Flags)
Scan the skill's source code and configuration for these critical indicators:
- 🚨 **Network**: Unauthorized `curl`, `wget`, or hidden `fetch` to unknown domains.
- 🚨 **Credentials**: Any access to `~/.ssh`, `~/.aws`, `~/.env`, or browser profile directories.
- 🚨 **Execution**: Use of `eval()`, `exec()`, or suspicious dynamic code generation.
- 🚨 **Obfuscation**: Minified or encoded strings intended to hide logic.
- 🚨 **Privilege**: Unnecessary `sudo` commands or system-level configuration changes.

### 3. Permission Mapping
- Does the skill require **File Write** access? (If so, why?)
- Does it require **Network** access? (If so, is it to a known API?)
- Does it request **Environment Variables**? (Check for sensitivity.)

### 4. Risk Classification
- 🟢 **LOW**: Local-only, formatting, notes, or static analysis tools. (Safe to install)
- 🟡 **MEDIUM**: API-based tools, browser automation to trusted sites. (Audit source code first)
- 🔴 **HIGH**: Tools interacting with private data, financial APIs, or cloud infrastructure. (Requires manual verification)
- ⛔ **EXTREME**: Skills requesting Root/Sudo or modifying system binaries. (**DO NOT INSTALL**)

## Standard Vetting Report Format
After every audit, produce a report in this format:

```markdown
### 🛡️ Skill Vetting Report: [Skill Name]
- **Risk Level**: [🟢/🟡/🔴/⛔]
- **Status**: [✅ Approved / ⚠️ Caution / ❌ Rejected]
- **Permissions Required**: [List files/network/env]
- **Findings**:
  - [X] No credential access detected.
  - [!] Suspicious network call to x.com (reasoning...).
- **Conclusion**: [Final recommendation]
```

## Security Mandate
If any "Red Flag" is found and not clearly justified in the documentation, **immediately reject the installation** and inform the user of the specific risks.
