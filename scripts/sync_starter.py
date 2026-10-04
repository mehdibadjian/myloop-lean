#!/usr/bin/env python3
"""Automated Synchronizer: myloop-lean -> myloop-starter.

Exports a clean, bloat-free template of myloop-lean and pushes it to
https://github.com/mehdibadjian/myloop-starter.git.
Can be invoked locally via CLI or automatically in CI/CD on merge to main.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

# Add current scripts directory to import scaffold
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scaffold

DEFAULT_STARTER_URL = "https://github.com/mehdibadjian/myloop-starter.git"


def get_current_sha(repo_root: Path) -> str:
    """Gets HEAD commit SHA or returns 'head'."""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return proc.stdout.strip() or "head"
    except Exception:
        return "head"


def sync_to_starter(
    source_root: Path,
    remote_url: str = DEFAULT_STARTER_URL,
    project_name: str = "myloop-starter",
    branch: str = "main",
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Scaffolds clean template and pushes to the starter remote."""
    source_root = Path(source_root).resolve()
    temp_dir = Path(tempfile.mkdtemp(prefix="starter_sync_"))

    try:
        # 1. Scaffold clean template into temporary directory
        scaffold.scaffold_project(
            source_root=source_root,
            target_dir=temp_dir,
            project_name=project_name,
        )

        sha = get_current_sha(source_root)
        commit_msg = f"chore: sync starter template from myloop-lean ({sha})"

        # 2. Initialize git repository in temp directory
        subprocess.run(["git", "init"], cwd=str(temp_dir), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "checkout", "-b", branch], cwd=str(temp_dir), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get author name/email from git or fallback
        user_name = "github-actions[bot]"
        user_email = "github-actions[bot]@users.noreply.github.com"
        try:
            name_proc = subprocess.run(["git", "config", "user.name"], cwd=str(source_root), stdout=subprocess.PIPE, text=True, check=False)
            email_proc = subprocess.run(["git", "config", "user.email"], cwd=str(source_root), stdout=subprocess.PIPE, text=True, check=False)
            if name_proc.stdout.strip():
                user_name = name_proc.stdout.strip()
            if email_proc.stdout.strip():
                user_email = email_proc.stdout.strip()
        except Exception:
            pass

        subprocess.run(["git", "config", "user.name", user_name], cwd=str(temp_dir), check=True)
        subprocess.run(["git", "config", "user.email", user_email], cwd=str(temp_dir), check=True)

        # 3. Add and commit
        subprocess.run(["git", "add", "."], cwd=str(temp_dir), check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(temp_dir), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "commit_message": commit_msg,
                "temp_dir": str(temp_dir),
            }

        # 4. Push to remote
        push_proc = subprocess.run(
            ["git", "push", "--force", remote_url, branch],
            cwd=str(temp_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        if push_proc.returncode != 0:
            raise RuntimeError(f"Git push failed: {push_proc.stderr}")

        return {
            "success": True,
            "dry_run": False,
            "remote_url": remote_url,
            "branch": branch,
            "commit_message": commit_msg,
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Sync clean starter template to myloop-starter remote")
    parser.add_argument(
        "--remote-url",
        default=os.environ.get("STARTER_REMOTE_URL", DEFAULT_STARTER_URL),
        help=f"Target remote URL (default: {DEFAULT_STARTER_URL})",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("STARTER_REPO_TOKEN", ""),
        help="Optional GitHub token for authenticated push in CI",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Target branch on starter repository (default: main)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build template without pushing",
    )

    args = parser.parse_args()
    source_root = Path(__file__).resolve().parent.parent

    target_url = args.remote_url
    if args.token and "github.com" in target_url and not ("@" in target_url):
        target_url = target_url.replace("https://github.com/", f"https://x-access-token:{args.token}@github.com/")

    print(f"Syncing myloop-lean -> {args.remote_url} (branch: {args.branch})...")
    res = sync_to_starter(
        source_root=source_root,
        remote_url=target_url,
        branch=args.branch,
        dry_run=args.dry_run,
    )

    if res.get("dry_run"):
        print(f"Dry run complete. Commit message: '{res['commit_message']}'")
    else:
        print(f"Successfully synced template to {args.remote_url} ({res['commit_message']})")


if __name__ == "__main__":
    main()
