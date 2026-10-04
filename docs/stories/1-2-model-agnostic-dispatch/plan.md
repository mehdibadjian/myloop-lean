# Story 1-2: Model-Agnostic Dispatch — Implementation Plan

## Stage 3: Step-by-Step Implementation Plan
- **Story Key:** `1-2-model-agnostic-dispatch`
- **TDD Flow:** Red -> Green -> Refactor

## Phase 1: Test-First Specification (Red Phase)
1. Create Gherkin BDD feature file: `tests/features/model_agnostic_dispatch.feature`.
2. Implement unit and integration test suite: `tests/test_model_agnostic_dispatch.py`.
   - Test 1: `test_prompt_compiler_includes_rules_and_skill`: Validates compilation of rules, persona, and skill text.
   - Test 2: `test_provider_registry_resolution`: Validates provider and model resolution across tiers and personas.
   - Test 3: `test_openai_compatible_client_payload_construction`: Validates headers and JSON payload formatting.
   - Test 4: `test_dispatch_dry_run_cli`: Validates `--dry-run` CLI flag and JSON export without network connectivity.
   - Test 5: `test_sprint_dispatch_integration`: Validates integration with `sprint.py dispatch`.
3. Run `pytest` to confirm all tests fail for the expected reasons (Red).

## Phase 2: Implementation (Green Phase)
1. Create `scripts/dispatch.py`:
   - Implement `ProviderRegistry` and `ModelConfig`.
   - Implement `compile_prompt_context(workspace_root, story_key, persona, skill_name)`.
   - Implement `OpenAICompatibleClient` with standard `urllib.request`.
   - Implement CLI argument parsing and `--dry-run` output formatting.
2. Update `scripts/sprint.py`:
   - Add `dispatch` subcommand invoking `dispatch.py` dispatch logic.
3. Run `pytest` to verify all tests pass (Green).

## Phase 3: Verification & Anti-Cheat (Refactor & Gate)
1. Verify no test assertion tampering with `python3 scripts/sprint.py verify --anti-cheat`.
2. Validate artifact chain with `python3 scripts/sprint.py validate-chain docs/stories/1-2-model-agnostic-dispatch`.
3. Check git diff for zero AI comment slop.
4. Prepare story markdown tracker: `docs/stories/1-2-model-agnostic-dispatch.md`.
