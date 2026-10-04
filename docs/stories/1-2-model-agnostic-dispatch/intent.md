# Story 1-2: Model-Agnostic Dispatch — Intent

## Stage 1: Intent Brief
- **Story Key:** `1-2-model-agnostic-dispatch`
- **Epic:** `epic-1`
- **Execution Tier:** `pro`
- **Status:** `in-progress`

## 1. Problem Statement
The legacy `myLoop` framework was tightly coupled to Claude Code's internal CLI architecture via pseudo-terminal (PTY) emulation and proprietary hook files. Modern autonomous workflows require agility across multiple foundation models:
- **Gemini 2.5 / Pro** for large-context native Antigravity pair programming.
- **DeepSeek-R1 / V3** for deep architectural reasoning, invariant enforcement, and adversarial code reviews.
- **Qwen 2.5 Coder (32B / 72B)** for fast, highly accurate Kent Beck TDD code generation.
- **Local / Self-Hosted Models (Ollama, vLLM)** for offline, secure, or zero-cost execution.

Without a model-agnostic dispatch layer, developers are locked into a single vendor's CLI, preventing optimal persona-to-model specialization.

## 2. Core Job-to-be-Done (JTBD)
> **When** I am ready to implement, review, or verify a story in `myloop-lean`,  
> **I want to** dispatch tasks across Gemini, DeepSeek, Qwen, or OpenAI-compatible endpoints with persona rules, skills, and story artifacts automatically bundled,  
> **So that** each lifecycle stage is executed by the best-suited model without proprietary harness lock-in or engine bloat.

## 3. Scope & Boundaries
- **In Scope:**
  - Declarative provider & model registry (Gemini, DeepSeek, Qwen, OpenAI, Anthropic, Ollama/vLLM).
  - Persona and tier mapping (Architect, Developer, Reviewer, PM, QA, Fortress Architect, Velocity King).
  - Zero-dependency prompt compiler (`AGENTS.md` persona + `.agents/rules/*.md` + `.agents/skills/*/SKILL.md` + story artifacts).
  - Zero-dependency OpenAI-compatible HTTP client (`urllib.request`).
  - CLI commands (`scripts/dispatch.py` and `scripts/sprint.py dispatch`) with `--dry-run` and JSON export capabilities.
- **Out of Scope:**
  - Heavy terminal scrapers or PTY emulation.
  - Complex multi-agent background daemons or WebSocket brokers.
