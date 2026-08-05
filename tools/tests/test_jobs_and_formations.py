"""Every Job/Formation rule must be seen to fire, and seen to stay quiet.

A linter you have never watched fail is a linter you are trusting on faith. W11 shipped with
false positives for exactly that reason. Run: python tools/tests/test_jobs_and_formations.py
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rules                                                    # noqa: E402

WORLD = rules.load_world()


def world_with(**overrides):
    clone = copy.deepcopy(WORLD)
    for key, value in overrides.items():
        setattr(clone, key, value)
    return clone


def a_card(index=0, **meta):
    card = copy.deepcopy(WORLD.cards[index])
    card.meta.update(meta)
    return card


def crews_where(name, **overrides):
    rows = [dict(c) for c in WORLD.crews]
    for row in rows:
        if row["name"] == name:
            row.update(overrides)
    return rows


CASES = []


def case(label, expected_zero=False):
    def wrap(fn):
        CASES.append((label, fn, expected_zero))
        return fn
    return wrap


@case("F11 rejects a Job that does not exist")
def _():
    card = a_card(job="nonsense", faction="Warmongers")
    return rules.f11_job_legality(world_with(cards=[card]))


@case("F11 rejects an Assholes Warden — 'they don't block'")
def _():
    return rules.f11_job_legality(world_with(cards=[a_card(job="warden", faction="Assholes")]))


@case("F11 allows a Warmongers Warden", expected_zero=True)
def _():
    return rules.f11_job_legality(world_with(cards=[a_card(job="warden", faction="Warmongers")]))


@case("F11 skips Icons entirely — they are exempt by design", expected_zero=True)
def _():
    return rules.f11_job_legality(world_with(cards=[a_card(job="warden", faction="Icons")]))


@case("F12 catches an enabler chain inside a crew that claims to be chaotic")
def _():
    producer = a_card(0, crew="Pwners", faction="Warmongers",
                      plan={"produces": ["own_board_wide"]})
    consumer = a_card(1, crew="Pwners", faction="Warmongers",
                      plan={"requires": ["own_board_wide"]})
    return rules.f12_chaotic_crew_enablers(
        world_with(cards=[producer, consumer], crews=crews_where("Pwners", coordination="chaotic")))


@case("F12 stays quiet for a coordinated crew — combos are the point there", expected_zero=True)
def _():
    producer = a_card(0, crew="Pwners", faction="Warmongers",
                      plan={"produces": ["own_board_wide"]})
    consumer = a_card(1, crew="Pwners", faction="Warmongers",
                      plan={"requires": ["own_board_wide"]})
    return rules.f12_chaotic_crew_enablers(world_with(cards=[producer, consumer]))


@case("W12 flags a Warden with no protective tool")
def _():
    card = a_card(job="warden", faction="Warmongers",
                  base={"keywords": [], "effects": []},
                  ascended={"keywords": [], "effects": []})
    return rules.w12_job_signature(world_with(cards=[card]))


@case("W12 accepts a Warden holding Protector", expected_zero=True)
def _():
    card = a_card(job="warden", faction="Warmongers",
                  base={"keywords": ["Protector"], "effects": []},
                  ascended={"keywords": [], "effects": []})
    return rules.w12_job_signature(world_with(cards=[card]))


@case("W13 reports the Jobs a declared Formation is missing")
def _():
    card = a_card(crew="Mobb 134", faction="Overthinkers", job="setter")
    return rules.w13_formation_coverage(
        world_with(cards=[card], crews=crews_where("Mobb 134", formation="the-engine")))


@case("W14 flags three cards sharing one Job — there is only one free slot")
def _():
    trio = [a_card(i, crew="Mobb 134", faction="Warmongers", job="enforcer", name=f"card{i}")
            for i in range(3)]
    return rules.w14_job_duplication(world_with(cards=trio))


@case("W14 allows two — the free slot may repeat a required Job", expected_zero=True)
def _():
    pair = [a_card(i, crew="Mobb 134", faction="Warmongers", job="enforcer", name=f"card{i}")
            for i in range(2)]
    return rules.w14_job_duplication(world_with(cards=pair))


@case("W15 reports the pool once, not once per card")
def _():
    blanks = [a_card(i, faction="Warmongers", name=f"card{i}") for i in range(4)]
    for card in blanks:
        card.meta.pop("job", None)
    found = rules.w15_jobs_undeclared(world_with(cards=blanks))
    assert len(found) == 1, f"W15 must consolidate; got {len(found)} findings"
    return found


def main() -> int:
    failures = 0
    for label, fn, expect_zero in CASES:
        found = fn()
        ok = (len(found) == 0) if expect_zero else (len(found) > 0)
        failures += not ok
        print(f"  {'PASS' if ok else 'FAIL'}  {label} — {len(found)} finding(s)")
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
