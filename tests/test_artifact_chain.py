"""BDD Test Suite for Three-Stage Artifact Chain."""

import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import sprint


def test_valid_artifact_chain(tmp_path):
    """Scenario: Validating the artifact chain directory and schema."""
    story_dir = tmp_path / "story-101"
    story_dir.mkdir()
    
    (story_dir / "intent.md").write_text("# Intent\nUser goal...", encoding="utf-8")
    (story_dir / "spec.md").write_text("# Spec\nGiven/When/Then...", encoding="utf-8")
    (story_dir / "plan.md").write_text("# Plan\nStep 1...", encoding="utf-8")
    
    result = sprint.validate_artifact_chain(story_dir)
    assert result["valid"] is True
    assert len(result["missing_artifacts"]) == 0


def test_missing_plan_fails_validation(tmp_path):
    """Missing plan.md fails the pre-code verification check."""
    story_dir = tmp_path / "story-102"
    story_dir.mkdir()
    
    (story_dir / "intent.md").write_text("# Intent\nUser goal...", encoding="utf-8")
    (story_dir / "spec.md").write_text("# Spec\nGiven/When/Then...", encoding="utf-8")
    
    result = sprint.validate_artifact_chain(story_dir)
    assert result["valid"] is False
    assert "plan.md" in result["missing_artifacts"]
