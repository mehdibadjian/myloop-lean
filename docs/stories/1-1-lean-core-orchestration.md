# Story 1-1: Lean Core Orchestration & BDD Harness

## Status
- **Status:** done
- **Tier:** flash
- **Epic:** epic-1

## Description
Establish the zero-dependency Python sprint status ledger manager (`scripts/sprint.py`), Gherkin BDD test specifications, and the 8 consolidated Antigravity skills.

## Acceptance Criteria
- **AC-1 (Given/When/Then):**
  - **Given** an active `sprint-status.yaml` ledger with stories in `ready-for-dev`
  - **When** `python3 scripts/sprint.py next` is executed
  - **Then** it prints the next actionable story key and execution tier.
- **AC-2 (Given/When/Then):**
  - **Given** an uncommitted working tree or broken test suite
  - **When** `python3 scripts/sprint.py verify` is executed
  - **Then** the verification gate halts with non-zero exit code.
- **AC-3 (Given/When/Then):**
  - **Given** the 8 consolidated skills in `.agents/skills/`
  - **When** verified against hygiene rules
  - **Then** all skills contain valid YAML frontmatter and zero legacy engine references.

## Tasks & Verification
- [x] Create Gherkin BDD feature specifications (`tests/features/`).
- [x] Implement BDD test suite with `pytest`.
- [x] Implement `scripts/sprint.py` with state machine and verification gate.
- [x] Author 8 consolidated skills and 3 architecture/TDD rules.
- [x] Verify all 12 BDD tests pass 100% green.
