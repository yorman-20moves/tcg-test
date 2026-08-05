"""check.py must survive a legacy-codepage console.

CLAUDE.md calls check.py "the one that matters", and it printed box-drawing rules to a
stdout that Python defaults to cp1252 on Windows -- so on the designer's own machine the
command died with UnicodeEncodeError before showing a single finding.
"""
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_check_runs_on_a_legacy_codepage_console():
    # Inherit the real environment -- a bare dict drops SYSTEMROOT and Windows fails to start
    # the interpreter at all, which would pass this test for entirely the wrong reason.
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "check.py")],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=REPO_ROOT, env=env,
    )
    assert "UnicodeEncodeError" not in result.stderr, result.stderr
    assert "blocking" in result.stdout
