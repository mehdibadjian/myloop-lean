# myloop-lean

> A lean, model-agnostic agent lifecycle orchestrator and BDD framework for modern AI pair programming. Optimized for Gemini 3.8 / Pro, DeepSeek-R1 / V3, Qwen 2.5 Coder, Claude, and open coding harnesses.

[![Tests](https://img.shields.io/badge/tests-18%20passed-brightgreen.svg)](#testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## What is myloop-lean?

`myloop-lean` is an agile, open-standard AI-native SDLC orchestrator inspired by Anthropic's Playbook and Kent Beck's TDD:
- **6-Stage Closed SDLC Loop:** Plan (`intent.md`) → Design (`spec.md`) → Build (`plan.md`) → Test (anti-cheat verify) → Deploy (code review) → Maintain (incident triage).
- **Two-Layer Safety:** Soft engineering rules (`.agents/rules/`) paired with deterministic hard CLI hooks (`scripts/sprint.py verify --anti-cheat`).
- **Zero-Dependency Python Ledger (`scripts/sprint.py`):** An atomic state machine, incident creator, and verification gate managing `sprint-status.yaml`.
- **Persistent Institutional Memory (`lessons-learned.md`):** Automatically inherits past regressions so future sessions never repeat defects.
- **Model-Agnostic Portability:** Seamlessly orchestrates across Google Antigravity, OpenHands, Aider, Cline, or local vLLM/Ollama setups running DeepSeek-R1 and Qwen 2.5 Coder.

---

## Directory Overview

```
.
├── .agents/
│   ├── rules/                      # Contextual engineering guidelines
│   │   ├── tdd-discipline.md       # Kent Beck TDD, no AI noise in comments
│   │   ├── architecture-rules.md   # Architectural invariants & ADRs
│   │   ├── security-hygiene.md     # Secrets, sanitization, safety
│   │   └── lessons-learned.md      # Auto-updating institutional memory
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

### 4. Run Pre-Completion Verification Gate (with Anti-Cheat)
```bash
python3 scripts/sprint.py verify --cmd "python3 -m pytest tests/" --anti-cheat
```

### 5. Trigger an Incident (Closed-Loop Maintenance)
```bash
python3 scripts/sprint.py incident "Checkout API returns 500 on valid token" --tier pro
```

### 6. Validate Three-Stage Artifact Chain
```bash
python3 scripts/sprint.py validate-chain docs/stories/1-1/
```

---

## The Consolidated Skills

| Skill | Role | Key Outcome |
|---|---|---|
| **`grill-me`** | Pre-Flight Grill | Adversarial Duel (Fortress vs. Velocity) & frontier design-tree interrogation. |
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

## Reusing `myloop-lean` in Future Repositories

You can easily instantiate or embed `myloop-lean` into any existing or new project using 4 methods:

### Method 1: Turn into a GitHub Template (1-Click for New Repos)
1. On GitHub, navigate to **`https://github.com/mehdibadjian/myloop-lean/settings`**.
2. Under **General**, check the box **"Template repository"**.
3. When creating any new repository on GitHub, choose **`mehdibadjian/myloop-lean`** under **"Repository template"**.
4. Every new repo starts with the lean BDD architecture, `.agents` skills, rules, and sprint tooling pre-configured.

### Method 2: CLI Scaffolder (`scripts/scaffold.py`)
To inject `myloop-lean` into an existing local project or a new folder:
```bash
# Scaffold into an existing repository:
python3 scripts/scaffold.py /path/to/my-future-project --project "Payment Service"
```
This automatically copies:
- `.agents/rules/` and `.agents/skills/`
- `scripts/sprint.py` and `scripts/dispatch.py`
- `AGENTS.md` and `GEMINI.md`
- Starter `sprint-status.yaml` and `docs/` hierarchy

### Method 3: Global Antigravity Installation
Make all skills (`grill-me`, `build`, `code-review`, etc.) and rules available globally in every project you open in Antigravity:
```bash
python3 scripts/scaffold.py --global-antigravity
```
Installs directly to `~/.gemini/antigravity-cli/skills/` and `~/.gemini/antigravity-cli/rules/`.

### Method 4: Git Subtree (Receive Upstream Skill & Rule Updates)
If you want future repos to track updates made to `myloop-lean`:
```bash
# In your target repo:
git subtree add --prefix=.agents https://github.com/mehdibadjian/myloop-lean.git main --squash

# Pull skill and rule updates in the future:
git subtree pull --prefix=.agents https://github.com/mehdibadjian/myloop-lean.git main --squash
```

---

## License

MIT © [Mehdi Badjian](https://github.com/mehdibadjian)
