# Technical Specification: AI-Native SDLC Optimization

> **Version:** 1.1.0  
> **Status:** Draft / Implementation  
> **Reference:** Anthropic AI-Native SDLC Playbook & myloop-lean Architecture  

---

## 1. Executive Summary & Purpose

This specification enhances `myloop-lean` by implementing Anthropic's **AI-Native SDLC Playbook** principles:
1. **The Three-Artifact Chain (`intent.md` → `spec.md` → `plan.md`):** Every story progresses through three explicit, reviewable markdown files in Git before production code is touched.
2. **Two-Layer Safety with Anti-Cheat Test Protection:** Hard deterministic verification hooks in `scripts/sprint.py verify` that prevent LLM agents from tampering with, deleting, or weakening test assertions to fake a passing build.
3. **Closed-Loop Maintenance (`scripts/sprint.py incident`):** Automated incident and bug triage that generates a fresh `intent.md` and restarts the development loop.
4. **Persistent Memory (`.agents/rules/lessons-learned.md`):** An auto-updating rule ledger that captures past mistakes, regressions, and anti-patterns so future agent sessions never repeat them.

---

## 2. The 6-Stage Closed Lifecycle

```
[ Stage 1: Plan ]  ────────►  [ Stage 2: Design ]  ────────►  [ Stage 3: Build ]
  intent.md (brief)             spec.md (ACs + ADR)            plan.md (steps)
         ▲                                                            │
         │                                                            ▼
[ Stage 6: Maintain ] ◄───────  [ Stage 5: Deploy ]  ◄─────────  [ Stage 4: Test ]
  incident.md                   code-review (PR)               anti-cheat verify
  lessons-learned.md            human sign-off                 TDD Green pass
```

### Stage 1: Plan (`intent.md`)
- **Producer:** [`grill-me`](file:///.agents/skills/grill-me/SKILL.md) / User Idea.
- **Artifact:** `docs/stories/<story-key>/intent.md` (or single-story format).
- **Contents:** User goal, problem statement, core value proposition, and explicit "Out of Scope" boundary.
- **Gate:** Human approval before advancing to Design.

### Stage 2: Design (`spec.md`)
- **Producer:** [`prd`](file:///.agents/skills/prd/SKILL.md) and [`architecture`](file:///.agents/skills/architecture/SKILL.md).
- **Artifact:** `docs/stories/<story-key>/spec.md`.
- **Contents:** Technical architecture invariants (`AD-n`), user journey mapping, and testable Given/When/Then acceptance criteria.
- **Gate:** Divergence test and invariant check.

### Stage 3: Build (`plan.md`)
- **Producer:** [`build`](file:///.agents/skills/build/SKILL.md) (pre-flight phase).
- **Artifact:** `docs/stories/<story-key>/plan.md`.
- **Constraint:** The agent **MUST NOT** edit production source code until `plan.md` is committed.
- **Contents:** Target test files to author (Red phase), production files to create/modify (Green phase), and refactoring notes.

### Stage 4: Test & Anti-Cheat Gate
- **Discipline:** Kent Beck TDD (Red -> Green -> Refactor).
- **Hard Gate:** `python3 scripts/sprint.py verify --anti-cheat`.
- **Anti-Cheat Validation:**
  - Ensures test suite exits 0.
  - Ensures tests were added or preserved.
  - Halts if test assertions (`assert `, `expect(`, `self.assert`) were deleted, commented out, or weakened.

### Stage 5: Deploy & Review
- **Producer:** [`code-review`](file:///.agents/skills/code-review/SKILL.md).
- **Checklist:** 4-lens review (Architecture, Logic, Test Completeness, Security).
- **Gate:** Human retains the merge button; autonomous PR created with full artifact evidence.

### Stage 6: Maintain & Continuous Memory
- **Incident Ingestion:** `python3 scripts/sprint.py incident "<description>"`.
  - Automatically writes an incident `intent.md` under `docs/stories/incidents/<id>-intent.md`.
  - Enters `sprint-status.yaml` with status `ready-for-dev`.
- **Memory Ledger:** `.agents/rules/lessons-learned.md`.
  - Populated during [`retrospective`](file:///.agents/skills/retrospective/SKILL.md).
  - Loaded automatically in every future agent turn via Antigravity rule discovery.

---

## 3. CLI Extensions (`scripts/sprint.py`)

### 3.1 `sprint.py verify --anti-cheat`
Inspects git diffs against the base commit of the story:
1. Identifies test files (`test_*.py`, `*_test.go`, `*.spec.ts`, etc.).
2. Checks for deleted assertion lines (`- *assert `, `- *expect(`, `- *def test_`).
3. If deleted assertions exceed added assertions without justification, exits with code 1 (`TEST_TAMPERING_DETECTED`).

### 3.2 `sprint.py incident <summary> [--tier flash|pro]`
Scaffolds a new incident:
1. Generates unique incident key `INC-<timestamp>`.
2. Creates `docs/stories/incidents/INC-<timestamp>-intent.md`.
3. Appends entry to `sprint-status.yaml` under `development_status` with `ready-for-dev`.
4. Outputs the file path for immediate agent action.
