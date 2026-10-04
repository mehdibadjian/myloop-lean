# Technical Specification: myloop-lean

> **Version:** 1.0.0  
> **Status:** Approved  
> **Repository:** https://github.com/mehdibadjian/myloop-lean.git  
> **Target Models:** Gemini 3.8 / Pro, DeepSeek-R1 / V3, Qwen 2.5 Coder, Claude, GPT-4o  

---

## 1. Overview & Philosophy

`myloop-lean` is a lightweight, model-agnostic agent lifecycle orchestrator designed for modern AI pair programming and autonomous development loops.

### 1.1 Core Tenets
1. **Zero Runtime Engine Bloat:** Completely removes heavy terminal wrappers, PTY scrapers, and compiled binaries. Replaces 31,000+ lines of Rust with pure Python standard tooling.
2. **Context-Native (No Micro-Step Splitting):** Eliminates brittle `render-skill` step files and artificial snapshot cascades. Leverages modern large-context models (1M+ tokens) with unified, cohesive runbooks.
3. **Open Standards First:** Standard Markdown skills with YAML frontmatter (`.agents/skills/`), hierarchical Markdown rules (`.agents/rules/`), and open agent declarations (`AGENTS.md`).
4. **Deterministic Sprint Ledger:** A human- and machine-readable YAML ledger (`sprint-status.yaml`) managed via an atomic CLI (`scripts/sprint.py`).
5. **Strict Test-First Discipline (TDD):** Red-Green-Refactor enforcement, test-backed verification gates, and zero AI noise in code comments.

---

## 2. Directory Structure

```
myloop-lean/
├── .agents/
│   ├── rules/
│   │   ├── tdd-discipline.md       # Kent Beck TDD, no AI commentary noise
│   │   ├── architecture-rules.md   # System invariants, boundary separation
│   │   └── security-hygiene.md     # Secrets, sanitization, dependency safety
│   └── skills/
│       ├── deep-recon/SKILL.md     # Grounded research and intelligence
│       ├── prd/SKILL.md            # Product requirements & JTBD
│       ├── architecture/SKILL.md   # Architectural spine & invariants
│       ├── decompose/SKILL.md      # Epics & user stories breakdown
│       ├── build/SKILL.md          # TDD implementation engine
│       ├── code-review/SKILL.md    # Multi-lens adversarial code review
│       ├── e2e-tests/SKILL.md      # Automated integration & regression tests
│       └── retrospective/SKILL.md  # Epic retro & invariant refinement
├── docs/
│   ├── SPEC_MYLOOP_LEAN.md         # This technical specification
│   ├── prd/                        # Project PRDs
│   ├── architecture/               # System invariants & ADRs
│   └── stories/                    # Story specification markdown files
├── scripts/
│   └── sprint.py                   # Python 3 CLI ledger manager
├── tests/
│   ├── features/                   # Gherkin BDD feature specifications
│   │   ├── sprint_ledger.feature
│   │   ├── verification_gate.feature
│   │   └── skill_hygiene.feature
│   ├── test_sprint_ledger.py       # BDD step implementations & unit tests
│   ├── test_verification_gate.py   # Verification gate assertions
│   └── test_skill_hygiene.py       # Structural schema & hygiene tests
├── sprint-status.yaml              # Active sprint status ledger
├── AGENTS.md                       # Antigravity project conventions & persona triggers
├── GEMINI.md                       # Gemini model instructions & tool discipline
├── README.md                       # Repository guide & quickstart
└── LICENSE                         # MIT License
```

---

## 3. Sprint Ledger State Machine (`scripts/sprint.py`)

### 3.1 Status Transitions
Stories move through a strictly validated unidirectional state machine:

```
[ backlog ] ──> [ ready-for-dev ] ──> [ in-progress ] ──> [ review ] ──> [ done ]
                                            │                 │
                                            └───<── [ blocked ]
```

- `backlog`: Story defined in epic breakdown, not yet groomed.
- `ready-for-dev`: Story specification written with Given/When/Then acceptance criteria.
- `in-progress`: Developer agent is actively writing tests and implementing.
- `review`: Implementation complete, test suite passing, ready for adversarial code review.
- `done`: Code review approved, verification gate passed, commit confirmed in git.
- `blocked`: Halting dependency requiring human or architectural intervention.

### 3.2 CLI Specification
The `scripts/sprint.py` CLI provides:
- `python3 scripts/sprint.py next`:
  - Returns the next unblocked `ready-for-dev` story key and execution tier in JSON or plain text.
- `python3 scripts/sprint.py update <key> --status <status>`:
  - Updates the story status atomically with comment and layout preservation.
  - Rejects invalid transitions (e.g. `backlog` -> `done`).
- `python3 scripts/sprint.py status`:
  - Renders a clean terminal summary of all epics, stories, and execution tiers.
- `python3 scripts/sprint.py verify [--cmd <test_command>]`:
  - Runs the test command, checks exit code, and validates clean working tree / git commit evidence.

---

## 4. Consolidated Skills Specification

### 4.1 Skill Taxonomy
0. **`grill-me`:** Relentless pre-flight adversarial grill session and design-tree interview combining the Fortress Architect vs. Velocity King duel with frontier round-based interrogation.
1. **`deep-recon`:** Synthesizes technical, domain, and competitive research into cited decision briefs.
2. **`prd`:** Creates customer-focused PRDs with user journeys, non-functional requirements, and testable acceptance criteria.
3. **`architecture`:** Defines the architectural spine—fixing durable invariants (design paradigms, data boundaries, state mutations) and ADRs.
4. **`decompose`:** Breaks requirements into prioritized epics and stories with Input/Output matrices.
5. **`build`:** Autonomous TDD engine: write failing test (Red) -> make test pass (Green) -> clean refactor -> commit.
6. **`code-review`:** Adversarial review across 4 lenses: architectural integrity, logic/edge cases, test coverage, and security.
7. **`e2e-tests`:** Generates automated integration, API, and end-to-end regression tests.
8. **`retrospective`:** Gathers git evidence, calculates velocity/verification gaps, and updates rules.

---

## 5. Verification & Security Gates

- **Git Commit Evidence:** A story cannot transition to `done` unless a valid git commit exists with changes related to the story.
- **Passing Test Suite:** Verification requires the configured test command (e.g. `pytest`, `cargo test`, `npm test`) to exit 0.
- **Zero AI Code Slop:** Code comments must explain architectural rationale, never inline AI workflow markers (`# Story: 1-1`).
