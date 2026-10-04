#!/usr/bin/env python3
"""myloop-lean Scaffolder: Reusable Framework Generator for Future Projects.

Exports or installs the myloop-lean architecture (.agents rules & skills,
sprint ledger CLI, model-agnostic dispatcher, AGENTS.md, and GEMINI.md) into
any target repository or globally into ~/.gemini/antigravity-cli/.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Optional


STARTER_SPRINT_YAML = """# Sprint Status Ledger ({project_name})
# Tracks epic and story progression across the development lifecycle.

project: {project_name}
tracking_system: file-system
story_location: docs/stories

development_status:
  epic-1: in-progress
  1-1-initial-setup: ready-for-dev
  epic-1-retrospective: optional

execution_tiers:
  1-1-initial-setup: flash

action_items: []
"""


def scaffold_project(
    source_root: Path,
    target_dir: Path,
    project_name: str = "My Project",
    global_antigravity: bool = False,
) -> Dict[str, Any]:
    """Copies myloop-lean assets into target directory or global Antigravity config."""
    target_dir = Path(target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    copied = []

    # 1. Copy .agents/ (rules and skills)
    src_agents = source_root / ".agents"
    if src_agents.exists():
        dst_agents = target_dir / ".agents"
        shutil.copytree(src_agents, dst_agents, dirs_exist_ok=True)
        copied.append(str(dst_agents))

    # 2. Copy scripts/ (sprint.py and dispatch.py)
    dst_scripts = target_dir / "scripts"
    dst_scripts.mkdir(parents=True, exist_ok=True)
    for script_name in ["sprint.py", "dispatch.py"]:
        src_script = source_root / "scripts" / script_name
        if src_script.exists():
            shutil.copy2(src_script, dst_scripts / script_name)
            copied.append(str(dst_scripts / script_name))

    # 3. Copy root agent markdown standards (AGENTS.md, GEMINI.md)
    for root_file in ["AGENTS.md", "GEMINI.md"]:
        src_file = source_root / root_file
        if src_file.exists():
            shutil.copy2(src_file, target_dir / root_file)
            copied.append(str(target_dir / root_file))

    # 4. Generate clean starter sprint-status.yaml if it doesn't exist
    target_ledger = target_dir / "sprint-status.yaml"
    if not target_ledger.exists():
        target_ledger.write_text(
            STARTER_SPRINT_YAML.format(project_name=project_name),
            encoding="utf-8",
        )
        copied.append(str(target_ledger))

    # 5. Create starter docs directories
    for doc_sub in ["stories", "prd", "architecture", "retrospectives"]:
        (target_dir / "docs" / doc_sub).mkdir(parents=True, exist_ok=True)

    # 6. Optional Global Antigravity Installation
    if global_antigravity:
        home = Path.home()
        global_cli = home / ".gemini" / "antigravity-cli"
        if global_cli.exists():
            # Copy skills
            global_skills = global_cli / "skills"
            global_skills.mkdir(parents=True, exist_ok=True)
            if (source_root / ".agents" / "skills").exists():
                shutil.copytree(
                    source_root / ".agents" / "skills",
                    global_skills,
                    dirs_exist_ok=True,
                )
                copied.append(str(global_skills))

            # Copy rules
            global_rules = global_cli / "rules"
            global_rules.mkdir(parents=True, exist_ok=True)
            if (source_root / ".agents" / "rules").exists():
                shutil.copytree(
                    source_root / ".agents" / "rules",
                    global_rules,
                    dirs_exist_ok=True,
                )
                copied.append(str(global_rules))

    return {
        "success": True,
        "target_dir": str(target_dir),
        "copied_artifacts": copied,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold myloop-lean into a new or existing repository",
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="Target directory to initialize (default: current directory)",
    )
    parser.add_argument(
        "--project",
        default="My New Project",
        help="Name of the project to initialize in sprint ledger",
    )
    parser.add_argument(
        "--global-antigravity",
        action="store_true",
        help="Also install skills and rules into ~/.gemini/antigravity-cli/",
    )

    args = parser.parse_args()
    source_root = Path(__file__).resolve().parent.parent
    target_path = Path(args.target_dir)

    print(f"Scaffolding myloop-lean into '{target_path.resolve()}'...")
    res = scaffold_project(
        source_root=source_root,
        target_dir=target_path,
        project_name=args.project,
        global_antigravity=args.global_antigravity,
    )

    print(f"Successfully scaffolded {len(res['copied_artifacts'])} assets into '{res['target_dir']}':")
    for f in res["copied_artifacts"]:
        print(f"  + {f}")
    print("\nNext steps:")
    print("  1. Edit sprint-status.yaml to define your first stories.")
    print("  2. Run 'python3 scripts/sprint.py next' to fetch the first story.")
    print("  3. Happy autonomous pair programming!")


if __name__ == "__main__":
    main()
