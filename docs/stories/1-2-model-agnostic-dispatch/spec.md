# Story 1-2: Model-Agnostic Dispatch — Specification

## Stage 2: Technical Specification
- **Story Key:** `1-2-model-agnostic-dispatch`
- **Component:** `scripts/dispatch.py` and `scripts/sprint.py`

## 1. Architectural Spine & Invariants
1. **Zero External Dependencies:** Use Python 3 standard library exclusively (`urllib.request`, `json`, `os`, `re`, `argparse`, `pathlib`).
2. **Provider Agnostic:** Common request/response interface conforming to OpenAI Chat Completions API standard (supported natively by DeepSeek, vLLM, Ollama, OpenRouter, and OpenAI).
3. **Strict Credential Hygiene:** No hardcoded tokens. Environment variables (`DEEPSEEK_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`) or custom endpoint configurations (`OPENAI_BASE_URL`, `OLLAMA_BASE_URL`).
4. **Context Integrity:** Prompt compiler must assemble system instructions deterministically:
   `Persona Definition` + `Architecture Rules` + `TDD Rules` + `Security Hygiene` + `Lessons Learned` + `Skill Instructions` + `Story Context`.

## 2. Component Design

### 2.1 Provider & Model Registry
Supported Providers:
- `deepseek`: Default models `deepseek-chat` (DeepSeek-V3), `deepseek-reasoner` (DeepSeek-R1). Base URL `https://api.deepseek.com`.
- `qwen`: Default models `qwen2.5-coder-32b-instruct`, `qwen2.5-coder-72b-instruct`. Base URL customizable or default DashScope/vLLM.
- `openai`: Default models `gpt-4o`, `gpt-4o-mini`, `o3-mini`. Base URL `https://api.openai.com/v1`.
- `local` / `ollama`: Default models `deepseek-r1:14b`, `qwen2.5-coder:7b`. Base URL `http://localhost:11434/v1`.
- `gemini`: Native Antigravity subagent format (`flash`, `pro`).

### 2.2 Persona & Tier Mapping Table
| Persona | Default Provider | Default Model | Tier |
|---|---|---|---|
| `architect` | `deepseek` | `deepseek-reasoner` | `pro` |
| `developer` | `qwen` / `openai` | `qwen2.5-coder-32b-instruct` / `gpt-4o-mini` | `flash` |
| `reviewer` | `deepseek` | `deepseek-reasoner` | `pro` |
| `product-manager` | `deepseek` / `openai` | `deepseek-chat` / `gpt-4o` | `flash` |
| `qa-engineer` | `qwen` | `qwen2.5-coder-32b-instruct` | `flash` |
| `fortress-architect` | `deepseek` | `deepseek-reasoner` | `pro` |
| `velocity-king` | `qwen` / `openai` | `qwen2.5-coder-32b-instruct` / `gpt-4o-mini` | `flash` |

### 2.3 Prompt Compiler (`compile_prompt_context`)
Given a `persona`, `skill_name`, and `story_key`:
1. Reads persona role definition from `AGENTS.md`.
2. Reads all rule files from `.agents/rules/*.md`.
3. Reads skill instructions from `.agents/skills/<skill_name>/SKILL.md` (if provided).
4. Reads story artifacts from `docs/stories/<story_key>/` (`intent.md`, `spec.md`, `plan.md`).
5. Assembles:
   - `system_prompt`: Persona identity + Core Rules + Skill Instructions.
   - `user_message`: Story artifacts + Task objective.

### 2.4 Dispatch Client (`OpenAICompatibleClient`)
- Executes HTTP POST request to `<base_url>/chat/completions`.
- Request body:
  ```json
  {
    "model": "<model>",
    "messages": [
      {"role": "system", "content": "<compiled_system_prompt>"},
      {"role": "user", "content": "<compiled_user_message>"}
    ],
    "temperature": 0.2
  }
  ```
- Error handling: Graceful capture of HTTP errors, timeouts, and missing API keys.
- Dry-run capability: Returns the payload without making network calls.

### 2.5 CLI Interface
- `python3 scripts/dispatch.py <story_key> --persona <persona> --skill <skill> [--provider <p>] [--model <m>] [--dry-run] [--export <path>]`
- `python3 scripts/sprint.py dispatch <story_key> [--persona <persona>] [--dry-run]`

## 3. Acceptance Criteria (Given/When/Then)
- **AC-1 (Context Assembly):**
  - **Given** valid rules, skills, and story artifacts in the workspace
  - **When** `compile_prompt_context` is executed for persona `developer` and skill `build`
  - **Then** the compiled system prompt contains the persona instructions, TDD discipline rules, and build skill steps.
- **AC-2 (Model Mapping):**
  - **Given** the provider registry
  - **When** resolving model for `reviewer` or `pro` tier
  - **Then** it resolves to a high-reasoning model (e.g. `deepseek-reasoner`).
- **AC-3 (Dry Run & Payload Export):**
  - **Given** a story with artifact files
  - **When** `dispatch` is run with `--dry-run`
  - **Then** it outputs or exports the structured JSON request payload without attempting HTTP calls or requiring API keys.
- **AC-4 (API Request Generation):**
  - **Given** a target provider and compiled messages
  - **When** constructing an OpenAI-compatible request
  - **Then** proper `Authorization` headers, JSON payload, and URL endpoints are formatted correctly.
