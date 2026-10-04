#!/usr/bin/env python3
"""myloop-lean: Deterministic sprint status ledger manager and verification gate."""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    yaml = None


VALID_STATUSES = [
    "backlog",
    "ready-for-dev",
    "in-progress",
    "review",
    "done",
    "blocked",
    "optional",
]

ALLOWED_TRANSITIONS = {
    "backlog": ["ready-for-dev", "blocked"],
    "ready-for-dev": ["in-progress", "blocked", "backlog"],
    "in-progress": ["review", "blocked", "ready-for-dev"],
    "review": ["done", "in-progress", "blocked"],
    "blocked": ["backlog", "ready-for-dev", "in-progress", "review"],
    "done": ["review"],  # Allow reopening if review finds regressions
    "optional": ["done", "in-progress"],
}


class SprintLedger:
    """Manages sprint-status.yaml reading, updating, and querying."""

    def __init__(self, ledger_path: Path):
        self.path = Path(ledger_path)
        if not self.path.exists():
            raise FileNotFoundError(f"Sprint ledger not found at {self.path}")
        self._load()

    def _load(self):
        self.raw_content = self.path.read_text(encoding="utf-8")
        if yaml:
            self.data = yaml.safe_load(self.raw_content) or {}
        else:
            self.data = {}

    def get_status(self, story_key: str) -> Optional[str]:
        dev_status = self.data.get("development_status", {})
        return dev_status.get(story_key)

    def get_tier(self, story_key: str) -> str:
        tiers = self.data.get("execution_tiers", {})
        return tiers.get(story_key, "standard")

    def get_next_actionable_story(self) -> Optional[Dict[str, str]]:
        """Finds the first story marked 'ready-for-dev'."""
        dev_status = self.data.get("development_status", {})
        for key, status in dev_status.items():
            if status == "ready-for-dev":
                return {
                    "key": key,
                    "status": status,
                    "tier": self.get_tier(key),
                }
        return None

    def update_status(self, story_key: str, new_status: str) -> bool:
        """Updates story status atomically while preserving comments."""
        if new_status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {VALID_STATUSES}")

        current_status = self.get_status(story_key)
        if current_status:
            allowed = ALLOWED_TRANSITIONS.get(current_status, [])
            if new_status not in allowed:
                raise ValueError(
                    f"Invalid status transition: cannot move '{story_key}' from '{current_status}' to '{new_status}'"
                )

        # Update file using line-preserving regex replacement
        pattern = re.compile(
            rf"^([ \t]*{re.escape(story_key)}[ \t]*:[ \t]*)([^\n#]+)(.*)$",
            re.MULTILINE,
        )

        match = pattern.search(self.raw_content)
        if match:
            prefix = match.group(1)
            comment = match.group(3)
            new_line = f"{prefix}{new_status}{comment}"
            new_content = self.raw_content[: match.start()] + new_line + self.raw_content[match.end() :]
        else:
            # If not found in raw content, locate development_status: section and append
            dev_idx = self.raw_content.find("development_status:")
            if dev_idx != -1:
                next_newline = self.raw_content.find("\n", dev_idx)
                insert_pos = next_newline + 1 if next_newline != -1 else len(self.raw_content)
                new_entry = f"  {story_key}: {new_status}\n"
                new_content = self.raw_content[:insert_pos] + new_entry + self.raw_content[insert_pos:]
            else:
                new_content = self.raw_content + f"\ndevelopment_status:\n  {story_key}: {new_status}\n"

        self.path.write_text(new_content, encoding="utf-8")
        self._load()
        return True

    def format_status_board(self) -> str:
        """Renders an ASCII status table."""
        lines = []
        lines.append(f"Sprint Status: {self.data.get('project', 'Unknown Project')}")
        lines.append("=" * 60)
        lines.append(f"{'Item / Story Key':<35} | {'Status':<12} | {'Tier':<8}")
        lines.append("-" * 60)

        dev_status = self.data.get("development_status", {})
        for key, status in dev_status.items():
            tier = self.get_tier(key) if not key.startswith("epic-") else "-"
            lines.append(f"{key:<35} | {status:<12} | {tier:<8}")
        lines.append("=" * 60)
        return "\n".join(lines)


def run_verification(test_command: str, work_dir: Path) -> Dict[str, Any]:
    """Runs tests and captures output and exit code."""
    try:
        proc = subprocess.run(
            test_command,
            shell=True,
            cwd=str(work_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
        )
        return {
            "passed": proc.returncode == 0,
            "test_exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except Exception as e:
        return {
            "passed": False,
            "test_exit_code": -1,
            "stdout": "",
            "stderr": str(e),
        }


def check_git_status(work_dir: Path) -> Dict[str, Any]:
    """Checks git status for uncommitted changes."""
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(work_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        output = proc.stdout.strip()
        uncommitted = [line for line in output.splitlines() if line] if output else []
        return {
            "clean": len(uncommitted) == 0,
            "dirty": len(uncommitted) > 0,
            "uncommitted_files": uncommitted,
        }
    except Exception as e:
        return {
            "clean": False,
            "dirty": True,
            "uncommitted_files": [f"Error checking git: {e}"],
        }


def main():
    parser = argparse.ArgumentParser(description="myloop-lean sprint ledger manager")
    parser.add_argument(
        "--ledger",
        default="sprint-status.yaml",
        help="Path to sprint-status.yaml",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # next
    subparsers.add_parser("next", help="Get next ready-for-dev story")

    # update
    update_p = subparsers.add_parser("update", help="Update story status")
    update_p.add_argument("story_key", help="Key of the story")
    update_p.add_argument("--status", required=True, choices=VALID_STATUSES, help="New status")

    # status
    subparsers.add_parser("status", help="Print sprint status board")

    # verify
    verify_p = subparsers.add_parser("verify", help="Run verification gate")
    verify_p.add_argument("--cmd", default="python3 -m pytest tests/", help="Test command to run")

    args = parser.parse_args()

    ledger_path = Path(args.ledger)
    if args.command in ["next", "update", "status"]:
        if not ledger_path.exists():
            print(f"Error: ledger file '{ledger_path}' not found.", file=sys.stderr)
            sys.exit(1)
        ledger = SprintLedger(ledger_path)

    if args.command == "next":
        story = ledger.get_next_actionable_story()
        if story:
            print(f"NEXT_STORY={story['key']}")
            print(f"TIER={story['tier']}")
        else:
            print("NO_STORIES_READY")

    elif args.command == "update":
        try:
            ledger.update_status(args.story_key, args.status)
            print(f"Updated '{args.story_key}' to status '{args.status}'")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "status":
        print(ledger.format_status_board())

    elif args.command == "verify":
        work_dir = Path.cwd()
        print(f"Running verification with command: {args.cmd}")
        res = run_verification(args.cmd, work_dir)
        git_res = check_git_status(work_dir)

        if not res["passed"]:
            print("VERIFICATION FAILED: Tests exited non-zero.", file=sys.stderr)
            print(res["stdout"])
            print(res["stderr"], file=sys.stderr)
            sys.exit(1)

        print("Tests passed successfully.")
        if git_res["dirty"]:
            print("Warning: Uncommitted changes in working tree:")
            for f in git_res["uncommitted_files"][:5]:
                print(f"  {f}")
        else:
            print("Git working tree is clean.")
        print("VERIFICATION PASSED.")


if __name__ == "__main__":
    main()
