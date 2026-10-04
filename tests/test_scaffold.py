"""Tests for myloop-lean Scaffolder and Reuse Tool."""

import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

try:
    import scaffold
except ImportError:
    scaffold = None


def test_scaffold_module_exists():
    assert scaffold is not None, "scripts/scaffold.py must exist and be importable"


def test_scaffold_new_project(tmp_path):
    """Scenario: Scaffolding myloop-lean into a new target repository."""
    target_dir = tmp_path / "new-service"
    target_dir.mkdir()

    res = scaffold.scaffold_project(
        source_root=REPO_ROOT,
        target_dir=target_dir,
        project_name="New Microservice",
    )

    assert res["success"] is True

    # Check .agents rules and skills
    assert (target_dir / ".agents" / "rules" / "tdd-discipline.md").exists()
    assert (target_dir / ".agents" / "rules" / "architecture-rules.md").exists()
    assert (target_dir / ".agents" / "rules" / "security-hygiene.md").exists()
    assert (target_dir / ".agents" / "rules" / "lessons-learned.md").exists()
    assert (target_dir / ".agents" / "skills" / "grill-me" / "SKILL.md").exists()
    assert (target_dir / ".agents" / "skills" / "build" / "SKILL.md").exists()
    assert (target_dir / ".agents" / "skills" / "code-review" / "SKILL.md").exists()

    # Check scripts
    assert (target_dir / "scripts" / "sprint.py").exists()
    assert (target_dir / "scripts" / "dispatch.py").exists()

    # Check root convention files
    assert (target_dir / "AGENTS.md").exists()
    assert (target_dir / "GEMINI.md").exists()

    # Check fresh sprint ledger
    ledger_file = target_dir / "sprint-status.yaml"
    assert ledger_file.exists()
    content = ledger_file.read_text(encoding="utf-8")
    assert "project: New Microservice" in content
    assert "epic-1: in-progress" in content


def test_scaffold_cli(tmp_path):
    """Scenario: Running scaffold via CLI."""
    target_dir = tmp_path / "cli-repo"
    target_dir.mkdir()

    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "scaffold.py"),
        str(target_dir),
        "--project",
        "CLI Project",
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert proc.returncode == 0, f"scaffold CLI failed: {proc.stderr}"
    assert (target_dir / "sprint-status.yaml").exists()
    assert (target_dir / ".agents" / "rules").exists()
