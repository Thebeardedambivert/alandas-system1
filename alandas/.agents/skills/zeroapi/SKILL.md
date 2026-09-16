---
name: zeroapi
description: Intelligent model routing for OpenClaw. Automatically selects between Gemini 3, GPT-5.3 Codex, and Claude 4.6 based on task complexity.
author: dorukardahan
version: 2026.1.0
---

# ZeroAPI Skill (2026 Edition)

This skill implements the high-performance routing logic for OpenClaw, optimized for the 2026 model landscape.

## Model Tiers & Routing

- **SIMPLE**: Gemini 2.5 Flash-Lite (Speed, basic formatting).
- **FAST**: Gemini 3 Flash (Instruction following, structured output).
- **RESEARCH**: Gemini 3 Pro (Long context, scientific analysis, >100k tokens).
- **CODE**: GPT-5.3 Codex (Coding, mathematics, logical rigor).
- **DEEP**: Claude Opus 4.6 (Reasoning, planning, complex decision making).
- **ORCHESTRATE**: Kimi K2.5 (Multi-agent coordination).

## Core Capabilities

- **Automatic Routing**: 9-step algorithm to match task to the best tier.
- **Fallback Chain**: Seamlessly drops to the next best model if a provider is rate-limited.
- **Context Awareness**: Forces Gemini 3 Pro for tasks exceeding 100k tokens.

## Commands

- `/zeroapi status`: Show active routing rules and model availability.
- `/zeroapi sync`: Refresh API tokens and provider health.
- `/zeroapi mode <auto|manual>`: Toggle between intelligent routing and fixed model usage.
