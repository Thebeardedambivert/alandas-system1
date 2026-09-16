name: control-center
description: Centralized command and control for AI skills and context management. Use this skill to organize, index, and orchestrate multiple skills across different projects. It acts as a "Mission Control" to identify the best tool for a task, manage shared context between skills, and reduce "context pollution" by selectively activating only necessary resources.

# Control Center (Mission Control for AI Agents)

This skill provides a centralized logic layer to manage multiple tools, skills, and project contexts efficiently.

## Core Capabilities
1. **Skill Discovery**: Indexes all available skills in `.gemini/skills/` and `.agents/skills/`.
2. **Context Orchestration**: Decides which skill to activate based on the complexity and scope of a task.
3. **Efficiency Optimization**: Prevents "context flooding" by loading only relevant `SKILL.md` content and documentation.
4. **Tool Chaining**: Designs workflows that involve multiple skills (e.g., `agent-browser` + `pdf` + `xlsx`).

## Standard Operating Procedures

### Step 1: Capability Mapping
When a complex task is received, identify all required capabilities:
- **Search**: `search-skill`, `google_web_search`
- **Automation**: `agent-browser`, `control-center`
- **Analysis**: `codebase_investigator`, `skill-vetter`
- **Production**: `pdf`, `xlsx`, `docx`

### Step 2: Workflow Design
Instead of running tools one-by-one, design a sequence:
- **Phase A (Research)**: Use `agent-browser` or `search-skill`.
- **Phase B (Verification)**: Use `skill-vetter` (if installing new tools).
- **Phase C (Execution)**: Use project-specific tools (e.g., `xlsx`).
- **Phase D (Documentation)**: Record results to KM.

### Step 3: Context Governance
- **Is the context too large?** If so, use `control-center` to summarize previous steps and clear irrelevant history.
- **Is the task multi-turn?** Maintain a "Session State" to track progress across multiple skill calls.

## Reporting Format
When managing a complex workflow, provide a brief "Mission Briefing":
- **Mission Name**: [Clear goal]
- **Activated Tools**: [Skill A, Skill B]
- **Current Status**: [Researching/Executing/Validating]
- **Next Milestone**: [Clear next step]

## Best Practices
- **Prefer Specialization**: If a specialized skill exists (e.g., `pdf`), always use it instead of a generalist tool.
- **Enforce Security**: Always run `skill-vetter` through `control-center` whenever a new source is involved.
- **Document Everything**: Use the KM workflow to ensure every "Mission" leaves a permanent record.
