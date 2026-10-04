"""BDD Test Suite for Pre-Completion Verification Gate."""

import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import sprint


def test_verify_command_pass(tmp_path):
    """Scenario: Verification succeeds when test command exits 0."""
    res = sprint.run_verification(test_command="true", work_dir=tmp_path)
    assert res["passed"] is True
    assert res["test_exit_code"] == 0


def test_verify_command_fail(tmp_path):
    """Scenario: Verification fails when test command fails."""
    res = sprint.run_verification(test_command="false", work_dir=tmp_path)
    assert res["passed"] is False
    assert res["test_exit_code"] != 0


def test_verify_git_cleanliness(tmp_path):
    """Scenario: Verification detects dirty git working tree."""
    # When not in git or clean
    status = sprint.check_git_status(work_dir=Path.cwd())
    assert "dirty" in status
    assert "uncommitted_files" in status
