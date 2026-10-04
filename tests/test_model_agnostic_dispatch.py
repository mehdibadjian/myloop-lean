"""Tests for Model-Agnostic Story Dispatch."""

import json
import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

try:
    import dispatch
except ImportError:
    dispatch = None


def test_dispatch_module_exists():
    assert dispatch is not None, "scripts/dispatch.py must exist and be importable"


def test_prompt_compiler_includes_rules_and_skill():
    """Scenario: Compiling prompt context with persona, rules, and skill."""
    context = dispatch.compile_prompt_context(
        workspace_root=REPO_ROOT,
        story_key="1-2-model-agnostic-dispatch",
        persona="developer",
        skill_name="build",
    )

    assert "system_prompt" in context
    assert "user_message" in context

    system_prompt = context["system_prompt"]
    # Check that core rules are bundled
    assert "Test-Driven Development" in system_prompt or "TDD" in system_prompt
    assert "Kent Beck" in system_prompt
    assert "Architecture Invariants" in system_prompt or "Architectural Spine" in system_prompt

    # Check that skill instructions are bundled
    assert "Autonomous TDD implementation engine" in system_prompt or "Red-Green-Refactor" in system_prompt

    # Check that story context is bundled into user_message
    user_message = context["user_message"]
    assert "1-2-model-agnostic-dispatch" in user_message
    assert "Intent Brief" in user_message or "Model-Agnostic Dispatch" in user_message


def test_provider_registry_resolution():
    """Scenario: Resolving model configurations by persona and tier."""
    registry = dispatch.ProviderRegistry()

    # Reviewer with pro tier should resolve to deepseek-reasoner
    prov, model, base_url = registry.resolve(persona="reviewer", tier="pro")
    assert prov == "deepseek"
    assert model == "deepseek-reasoner"
    assert "deepseek" in base_url

    # Developer with flash tier should resolve to qwen or gpt-4o-mini
    prov, model, base_url = registry.resolve(persona="developer", tier="flash")
    assert prov in ["qwen", "openai", "gemini"]
    assert len(model) > 0

    # Overrides should take precedence
    prov, model, base_url = registry.resolve(
        persona="developer",
        tier="flash",
        provider_override="local",
        model_override="deepseek-r1:14b",
    )
    assert prov == "local"
    assert model == "deepseek-r1:14b"
    assert "localhost" in base_url or "127.0.0.1" in base_url


def test_openai_compatible_client_payload_construction():
    """Scenario: Formatting OpenAI-compatible payload and headers."""
    client = dispatch.OpenAICompatibleClient(
        base_url="https://api.deepseek.com/v1",
        api_key="test-key",
    )
    payload = client.format_payload(
        model="deepseek-reasoner",
        system_prompt="System instructions",
        user_message="User goal",
        temperature=0.1,
    )

    assert payload["model"] == "deepseek-reasoner"
    assert len(payload["messages"]) == 2
    assert payload["messages"][0]["role"] == "system"
    assert payload["messages"][0]["content"] == "System instructions"
    assert payload["messages"][1]["role"] == "user"
    assert payload["messages"][1]["content"] == "User goal"
    assert payload["temperature"] == 0.1

    headers = client.format_headers()
    assert headers["Authorization"] == "Bearer test-key"
    assert headers["Content-Type"] == "application/json"


def test_dispatch_dry_run_cli():
    """Scenario: Executing dispatch in dry-run mode via CLI."""
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "dispatch.py"),
        "1-2-model-agnostic-dispatch",
        "--dry-run",
        "--persona",
        "developer",
        "--skill",
        "build",
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert proc.returncode == 0, f"dispatch failed: {proc.stderr}"
    data = json.loads(proc.stdout)
    assert "model" in data
    assert "messages" in data
    assert len(data["messages"]) >= 2


def test_sprint_dispatch_integration():
    """Scenario: Integrating dispatch subcommand into sprint.py."""
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "sprint.py"),
        "dispatch",
        "1-2-model-agnostic-dispatch",
        "--dry-run",
        "--persona",
        "reviewer",
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert proc.returncode == 0, f"sprint dispatch failed: {proc.stderr}"
    data = json.loads(proc.stdout)
    assert data["model"] == "deepseek-reasoner"
