# Story 1-2: Model-Agnostic Dispatch

## Status
- **Status:** done
- **Tier:** pro
- **Epic:** epic-1

## Description
Provide a model-agnostic dispatch engine (`scripts/dispatch.py` and `scripts/sprint.py dispatch`) that compiles persona instructions, system invariants, rules, and skills into standardized OpenAI-compatible payloads for Gemini, DeepSeek, Qwen, and local endpoints.

## Acceptance Criteria
- **AC-1 (Context Assembly):** Given rules, skills, and story artifacts, the prompt compiler deterministically bundles them into coherent system and user prompt messages.
- **AC-2 (Model & Provider Resolution):** Execution tiers and personas map to optimal foundation models (e.g. Developer -> Qwen 2.5 Coder, Reviewer -> DeepSeek-R1).
- **AC-3 (Dry Run & Zero-Dependency Dispatch):** The CLI supports `--dry-run` and JSON export without requiring third-party libraries or active network credentials.
- **AC-4 (Sprint Integration):** `python3 scripts/sprint.py dispatch <key>` dispatches the story via the unified dispatch engine.

## Tasks & Verification
- [x] Author Gherkin BDD specification (`tests/features/model_agnostic_dispatch.feature`).
- [x] Implement unit & integration test suite (`tests/test_model_agnostic_dispatch.py`).
- [x] Implement `scripts/dispatch.py` with zero external dependencies.
- [x] Add `dispatch` subcommand to `scripts/sprint.py`.
- [x] Verify test suite passes with `--anti-cheat`.
