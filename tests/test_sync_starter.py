"""Tests for automated sync from myloop-lean to myloop-starter."""

import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

try:
    import sync_starter
except ImportError:
    sync_starter = None


def test_sync_starter_module_exists():
    assert sync_starter is not None, "scripts/sync_starter.py must exist and be importable"


def test_sync_starter_local_push(tmp_path):
    """Scenario: Syncing clean starter to a local bare repository."""
    # 1. Create a local bare repository to serve as the remote
    bare_remote = tmp_path / "starter_remote.git"
    subprocess.run(
        ["git", "init", "--bare", str(bare_remote)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # 2. Run sync_starter pointing to the bare remote
    res = sync_starter.sync_to_starter(
        source_root=REPO_ROOT,
        remote_url=str(bare_remote),
        project_name="myloop-starter",
        branch="main",
    )

    assert res["success"] is True

    # 3. Verify content in bare remote by cloning into a verification dir
    clone_dir = tmp_path / "cloned_verify"
    subprocess.run(
        ["git", "clone", "-b", "main", str(bare_remote), str(clone_dir)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert (clone_dir / "README.md").exists()
    assert (clone_dir / "sprint-status.yaml").exists()
    assert (clone_dir / ".agents" / "skills" / "grill-me" / "SKILL.md").exists()
    assert (clone_dir / "scripts" / "sprint.py").exists()
    assert not (clone_dir / "docs" / "SPEC_MYLOOP_LEAN.md").exists()
