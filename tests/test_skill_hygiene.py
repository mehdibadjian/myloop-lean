"""BDD Test Suite for Skill Hygiene and Open Standards Compliance."""

from pathlib import Path
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
RULES_DIR = REPO_ROOT / ".agents" / "rules"

EXPECTED_SKILLS = [
    "deep-recon",
    "prd",
    "architecture",
    "decompose",
    "build",
    "code-review",
    "e2e-tests",
    "retrospective",
]

EXPECTED_RULES = [
    "tdd-discipline.md",
    "architecture-rules.md",
    "security-hygiene.md",
]


def parse_frontmatter(content: str):
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except Exception:
        return None


def test_expected_skills_exist():
    """Scenario: All 8 consolidated skills exist."""
    assert SKILLS_DIR.exists(), f"{SKILLS_DIR} must exist"
    for name in EXPECTED_SKILLS:
        skill_file = SKILLS_DIR / name / "SKILL.md"
        assert skill_file.exists(), f"Skill file {skill_file} must exist"


def test_skill_frontmatter_valid():
    """Scenario: All skills have valid YAML frontmatter with name and description."""
    for name in EXPECTED_SKILLS:
        skill_file = SKILLS_DIR / name / "SKILL.md"
        if not skill_file.exists():
            continue
        content = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        assert fm is not None, f"Skill {name} missing YAML frontmatter"
        assert "name" in fm and fm["name"] == name, f"Skill {name} invalid 'name' frontmatter"
        assert "description" in fm and len(fm["description"].strip()) > 10, f"Skill {name} invalid 'description'"


def test_zero_legacy_engine_references():
    """Scenario: Zero legacy engine references in skills."""
    legacy_terms = ["engine-rust", "render-skill", "customize.toml"]
    for skill_file in SKILLS_DIR.glob("**/*.md"):
        content = skill_file.read_text(encoding="utf-8")
        for term in legacy_terms:
            assert term not in content, f"Legacy term '{term}' found in {skill_file}"


def test_expected_rules_exist():
    """Scenario: Native rules are properly structured in .agents/rules."""
    assert RULES_DIR.exists(), f"{RULES_DIR} must exist"
    for rule_name in EXPECTED_RULES:
        rule_file = RULES_DIR / rule_name
        assert rule_file.exists(), f"Rule file {rule_file} must exist"
        content = rule_file.read_text(encoding="utf-8")
        assert len(content.strip()) > 50, f"Rule {rule_name} is too brief or empty"
