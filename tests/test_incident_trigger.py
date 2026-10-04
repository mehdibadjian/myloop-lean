"""BDD Test Suite for Autonomous Incident Maintenance Loop."""

import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import sprint

SAMPLE_LEDGER = """project: myloop-lean
tracking_system: file-system
story_location: docs/stories

development_status:
  epic-1: in-progress
  1-1-core: done

execution_tiers:
  1-1-core: flash
"""


@pytest.fixture
def temp_repo(tmp_path):
    ledger = tmp_path / "sprint-status.yaml"
    ledger.write_text(SAMPLE_LEDGER, encoding="utf-8")
    stories_dir = tmp_path / "docs" / "stories"
    stories_dir.mkdir(parents=True, exist_ok=True)
    return tmp_path, ledger


def test_create_incident(temp_repo):
    """Scenario: Creating an incident scaffolds intent.md and registers in sprint ledger."""
    repo_root, ledger_path = temp_repo
    
    incident = sprint.create_incident(
        ledger_path=ledger_path,
        summary="Checkout API returns 500 on valid token",
        tier="pro",
        stories_dir=repo_root / "docs" / "stories",
    )
    
    assert incident is not None
    assert incident["key"].startswith("INC-")
    assert incident["intent_file"].exists()
    
    # Check file content
    content = incident["intent_file"].read_text(encoding="utf-8")
    assert "Checkout API returns 500 on valid token" in content
    assert "Stage 1: Intent" in content
    
    # Check ledger registration
    ledger = sprint.SprintLedger(ledger_path)
    assert ledger.get_status(incident["key"]) == "ready-for-dev"
    assert ledger.get_tier(incident["key"]) == "pro"
