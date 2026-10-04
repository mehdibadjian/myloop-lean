# myloop-lean

> A lean, model-agnostic agent lifecycle orchestrator and BDD framework for modern AI pair programming. Optimized for Gemini 3.8 / Pro, DeepSeek-R1 / V3, Qwen 2.5 Coder, Claude, and open coding harnesses.

[![Tests](https://img.shields.io/badge/tests-12%20passed-brightgreen.svg)](#testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## What is myloop-lean?

`myloop-lean` replaces monolithic, compiled terminal wrappers with an agile, open-standard architecture:
- **Zero-Dependency Python Ledger (`scripts/sprint.py`):** An atomic state machine and verification gate managing `sprint-status.yaml`.
- **8 Consolidated Antigravity Skills (`.agents/skills/`):** Cohesive, single-runbook skills leveraging modern 1M+ token context windows without fragile micro-step snapshot files.
- **Hierarchical Discipline Rules (`.agents/rules/`):** Non-negotiable engineering standards for strict TDD, architectural spine invariants, and security hygiene.
- **Model-Agnostic Portability:** Seamlessly orchestrates across Google Antigravity, OpenHands, Aider, Cline, or local vLLM/Ollama setups running DeepSeek-R1 and Qwen 2.5 Coder.

---

## Directory Overview

```
.
├── .agents/
│   ├── rules/                      # Contextual engineering guidelines
│   │   ├── tdd-discipline.md       # Kent Beck TDD, no AI noise in comments
│   │   ├── architecture-rules.md   # Architectural invariants & ADRs
│   │   └── security-hygiene.md     # Secrets, sanitization, safety
│   └── skills/                     # 8 high-signal lifecycle skills
│       ├── deep-recon/             # Research & evidence-backed briefs
│       ├── prd/                    # Product requirements & JTBD
│       ├── architecture/           # Invariant spine & ADRs
│       ├── decompose/              # Epic & story slicing
│       ├── build/                  # TDD execution engine
│       ├── code-review/            # Multi-lens adversarial review
│       ├── e2e-tests/              # Automated integration test generation
│       └── retrospective/          # Epic review & invariant refinement
├── docs/
│   ├── SPEC_MYLOOP_LEAN.md         # Technical architecture specification
│   ├── LEAN_GEMINI_ARCHITECTURE_PLAN.md
│   └── stories/                    # Story specifications
├── scripts/
│   └── sprint.py                   # Sprint ledger CLI & verification gate
├── tests/
│   ├── features/                   # Gherkin BDD feature specifications
│   │   ├── sprint_ledger.feature
│   │   ├── verification_gate.feature
│   │   └── skill_hygiene.feature
│   ├── test_sprint_ledger.py       # Ledger unit & state machine tests
│   ├── test_verification_gate.py   # Verification gate tests
│   └── test_skill_hygiene.py       # Skill schema and rule tests
├── sprint-status.yaml              # Active sprint status ledger
├── AGENTS.md                       # Persona definitions & subagent patterns
├── GEMINI.md                       # Model guidelines & pair programming rules
└── README.md
```

---

## Quickstart

### 1. Inspect Sprint Status
```bash
python3 scripts/sprint.py status
```

### 2. Query Next Actionable Story
```bash
python3 scripts/sprint.py next
# Output:
# NEXT_STORY=1-2-model-agnostic-dispatch
# TIER=pro
```

### 3. Update Story Status
```bash
python3 scripts/sprint.py update 1-2-model-agnostic-dispatch --status in-progress
```

### 4. Run Pre-Completion Verification Gate
```bash
python3 scripts/sprint.py verify --cmd "python3 -m pytest tests/"
```

---

## The 8 Consolidated Skills

| Skill | Role | Key Outcome |
|---|---|---|
| **`deep-recon`** | Research & Spikes | Decision-grade briefs with verified citations. |
| **`prd`** | Product Definition | JTBD requirements with Given/When/Then acceptance criteria. |
| **`architecture`** | System Design | Architecture spine fixing invariants and ADRs. |
| **`decompose`** | Sprint Breakdown | Vertically sliced stories with Input/Output matrices. |
| **`build`** | TDD Developer | Red-Green-Refactor implementation and clean commits. |
| **`code-review`** | Adversarial Review | Multi-lens check: architecture, logic, tests, and security. |
| **`e2e-tests`** | QA Engineering | Automated integration & regression test coverage. |
| **`retrospective`**| Epic Retrospective | Velocity analysis, git churn, and continuous rule updates. |

---

## Multi-Model & Harness Portability

This repository runs universally across platforms:
- **Google Antigravity:** Leverages native `invoke_subagent` and reactive wakeup.
- **DeepSeek & Qwen:** Map DeepSeek-R1 to `architecture` and `code-review`, and Qwen 2.5 Coder to `build` and `e2e-tests`.
- **Open Coding Harnesses:** Compatible out of the box with OpenHands, Aider, Cline, and Roo-Code.

---

## Testing

Run the full Behavior-Driven Development (BDD) test suite:
```bash
python3 -m pytest tests/ -v
```

---

## License

MIT © [Mehdi Badjian](https://github.com/mehdibadjian)
