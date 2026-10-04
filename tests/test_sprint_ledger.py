"""BDD Test Suite for Sprint Status Ledger Management."""

import sys
import tempfile
from pathlib import Path
import pytest
import yaml

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

try:
    import sprint
except ImportError:
    sprint = None


SAMPLE_SPRINT_YAML = """# Sprint Status Ledger
project: Curious Hopper
tracking_system: file-system
story_location: docs/stories

development_status:
  epic-1: in-progress
  1-1-auth: done
  1-2-user: ready-for-dev
  1-3-post: backlog
  epic-1-retrospective: optional

execution_tiers:
  1-2-user: pro
  1-3-post: flash
"""


@pytest.fixture
def temp_ledger(tmp_path):
    ledger_path = tmp_path / "sprint-status.yaml"
    ledger_path.write_text(SAMPLE_SPRINT_YAML, encoding="utf-8")
    return ledger_path


def test_sprint_module_exists():
    assert sprint is not None, "scripts/sprint.py must exist and be importable"


def test_query_next_ready_story(temp_ledger):
    """Scenario: Querying the next ready-for-dev story."""
    ledger = sprint.SprintLedger(temp_ledger)
    next_story = ledger.get_next_actionable_story()
    
    assert next_story is not None
    assert next_story["key"] == "1-2-user"
    assert next_story["status"] == "ready-for-dev"
    assert next_story["tier"] == "pro"


def test_valid_status_transition(temp_ledger):
    """Scenario: Validating status transition order."""
    ledger = sprint.SprintLedger(temp_ledger)
    res = ledger.update_status("1-2-user", "in-progress")
    
    assert res is True
    assert ledger.get_status("1-2-user") == "in-progress"
    
    # Reload from disk to verify persistence
    reloaded = sprint.SprintLedger(temp_ledger)
    assert reloaded.get_status("1-2-user") == "in-progress"


def test_reject_invalid_status_transition(temp_ledger):
    """Scenario: Rejecting invalid status regressions or jumps."""
    ledger = sprint.SprintLedger(temp_ledger)
    with pytest.raises(ValueError, match="Invalid status transition"):
        ledger.update_status("1-3-post", "done")


def test_preserve_comments_and_format(temp_ledger):
    """Scenario: Updating story while preserving ledger structure."""
    ledger = sprint.SprintLedger(temp_ledger)
    ledger.update_status("1-2-user", "in-progress")
    ledger.update_status("1-2-user", "review")
    
    content = temp_ledger.read_text(encoding="utf-8")
    assert "# Sprint Status Ledger" in content
    assert "epic-1: in-progress" in content
    assert "1-2-user: review" in content
