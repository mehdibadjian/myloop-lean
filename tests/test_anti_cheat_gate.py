"""BDD Test Suite for Anti-Cheat Test Tampering Detection."""

import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import sprint


SAMPLE_CLEAN_DIFF = """diff --git a/tests/test_calc.py b/tests/test_calc.py
index 1234567..89abcdef 100644
--- a/tests/test_calc.py
+++ b/tests/test_calc.py
@@ -10,3 +10,6 @@ def test_add():
+def test_multiply():
+    assert multiply(2, 3) == 6
+
"""

SAMPLE_TAMPERED_DIFF = """diff --git a/tests/test_auth.py b/tests/test_auth.py
index 1111111..2222222 100644
--- a/tests/test_auth.py
+++ b/tests/test_auth.py
@@ -15,5 +15,3 @@ def test_jwt_expiry():
-    assert token.is_valid() is False
-    assert token.is_expired() is True
+    pass
"""


def test_clean_diff_passes_anti_cheat():
    """Scenario: Clean test execution with anti-cheat verification."""
    result = sprint.detect_test_tampering(SAMPLE_CLEAN_DIFF)
    assert result["tampered"] is False
    assert len(result["deleted_assertions"]) == 0


def test_tampered_diff_fails_anti_cheat():
    """Scenario: Detecting deleted or weakened test assertions."""
    result = sprint.detect_test_tampering(SAMPLE_TAMPERED_DIFF)
    assert result["tampered"] is True
    assert len(result["deleted_assertions"]) == 2
    assert "assert token.is_valid()" in result["deleted_assertions"][0]


def test_non_test_file_diff_ignored():
    """Non-test files removing assert statements (e.g. debug asserts in prod) are ignored."""
    prod_diff = """diff --git a/src/engine.py b/src/engine.py
--- a/src/engine.py
+++ b/src/engine.py
@@ -5,3 +5,2 @@
-    assert len(items) > 0
"""
    result = sprint.detect_test_tampering(prod_diff)
    assert result["tampered"] is False
