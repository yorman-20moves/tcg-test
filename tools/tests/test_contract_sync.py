"""F13 must be seen to fire: the working contract exists twice, and the copies drift.

The bug this rule exists for was silent by construction. AGENTS.md and CLAUDE.md carried
different versions of hard rule 6 -- one of them still describing three generated documents
long after cards' Rules Text became generated too -- while README.md went on routing human
collaborators to the stale copy. Nothing in the repo said a word. A rule you have never
watched fail is a rule you are trusting on faith.

Run: python tools/tests/test_contract_sync.py
"""
import contextlib
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import card_io                                                  # noqa: E402
import rules                                                    # noqa: E402

CANONICAL, MIRROR = rules.CONTRACT_FILES
CONTRACT = "# the contract\n\nhard rule 6\nhard rule 7\n"


@contextlib.contextmanager
def a_repo(canonical, mirror):
    """A throwaway repo root holding just the two contract files. None means absent."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, body in ((CANONICAL, canonical), (MIRROR, mirror)):
            if body is not None:
                (root / name).write_bytes(body.encode("utf-8"))
        real, card_io.REPO_ROOT = card_io.REPO_ROOT, root
        try:
            yield
        finally:
            card_io.REPO_ROOT = real


# f13 takes `world` only to match the uniform rule signature; it reads the repo, not the game.
def check():
    return rules.f13_contract_drift(None)


def in_sync():
    with a_repo(CONTRACT, CONTRACT):
        return check()


def drifted():
    with a_repo(CONTRACT, CONTRACT.replace("hard rule 6", "the OLD hard rule 6")):
        return check()


def mirror_missing():
    with a_repo(CONTRACT, None):
        return check()


def bytes_only():
    with a_repo(CONTRACT, CONTRACT.replace("\n", "\r\n")):
        return check()


def the_real_repo():
    """The actual AGENTS.md and CLAUDE.md, right now."""
    return check()


CASES = [
    ("identical copies stay quiet", in_sync, True),
    ("a drifted mirror fires", drifted, False),
    ("a missing mirror fires", mirror_missing, False),
    ("a bytes-only difference fires", bytes_only, False),
    ("the real repo is in sync", the_real_repo, True),
]


def assert_drift_is_reported_usefully():
    """A finding that does not say where to look is a finding nobody acts on."""
    found = drifted()
    assert len(found) == 1, found
    finding = found[0]
    assert finding.code == "F13" and finding.blocking, finding
    assert "line 3" in finding.message, finding.message
    assert finding.where == f"{MIRROR}:3", finding.where
    assert CANONICAL in finding.fix and MIRROR in finding.fix, finding.fix


def assert_a_bytes_only_difference_is_not_called_zero_lines():
    """CRLF drift has no differing *lines*; the message must not claim '0 differing lines'."""
    finding = bytes_only()[0]
    assert "0 differing" not in finding.message, finding.message
    assert "line endings" in finding.message, finding.message


CHECKS = [assert_drift_is_reported_usefully,
          assert_a_bytes_only_difference_is_not_called_zero_lines]


# ---------------------------------------------------------------------------
# The import is guarded because the script's whole point is that it runs on a
# bare PyYAML install with no test framework present.
# ---------------------------------------------------------------------------
try:
    import pytest
except ImportError:                                             # standalone run
    pytest = None

if pytest is not None:

    @pytest.mark.parametrize("label,fn,expect_zero", CASES,
                             ids=[label for label, _fn, _z in CASES])
    def test_rule_fires(label, fn, expect_zero):
        found = fn()
        if expect_zero:
            assert not found, f"{label}: expected silence, got {len(found)}: {found}"
        else:
            assert found, f"{label}: expected the rule to fire, it stayed quiet"

    @pytest.mark.parametrize("check_fn", CHECKS, ids=[c.__name__ for c in CHECKS])
    def test_finding_is_actionable(check_fn):
        check_fn()


if __name__ == "__main__":
    failures = 0
    for label, fn, expect_zero in CASES:
        found = fn()
        ok = (not found) if expect_zero else bool(found)
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    for check_fn in CHECKS:
        try:
            check_fn()
            print(f"  ok   {check_fn.__name__}")
        except AssertionError as exc:
            failures += 1
            print(f"  FAIL {check_fn.__name__}: {exc}")
    print(f"\n{failures} failing")
    sys.exit(min(failures, 125))
