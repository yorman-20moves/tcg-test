#!/usr/bin/env python3
"""Machine-checkable gates from docs/rubrics/gameplay-rubric.md.

Covers the gates a script can actually decide:
    G1  budget compliance (delegated to balance.py)
    G3  every printed ability declares its type
    G4  keywords belong to the card's own faction
    G6  partial -- statuses applied without a stated duration
    G8  faction present, art referenced, crew present or explicitly null

G2, G5, G7 and G9 need a human. They are listed as reminders at the end of a run.

Usage:
    python tools/validate.py               # all cards
    python tools/validate.py --strict      # stub cards also fail
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
BUDGET_TOLERANCE = 1

ABILITY_TYPES = {"Standard Ability", "Fast Ability", "Trigger Ability", "Passive Ability"}
DURATION_PHRASES = (
    "end of the round", "end step", "end of round", "permanent", "permanently",
    "until removed", "this round", "this turn", "once per round", "for the duration",
)
HUMAN_ONLY_GATES = {
    "G2": "every rules term is defined in the rulebook or data/",
    "G5": "no unbounded loop with any existing card",
    "G7": "answerable by at least one existing card, including by the poorest-tooled faction",
    "G9": "losing to it feels like being outplayed, not robbed or insulted",
}


def load_yaml(relative_path: str):
    return yaml.safe_load((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def split_card(path: Path) -> tuple[dict, str]:
    """Return (frontmatter, rules_body).

    rules_body stops at `## Lore` -- the Lore and Design Notes sections are prose about the
    card, not printed rules text, and scanning them produces false gate failures.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("no YAML frontmatter")
    _, frontmatter, body = text.split("---", 2)
    rules_body = re.split(r"^## Lore\s*$", body, maxsplit=1, flags=re.MULTILINE)[0]
    return yaml.safe_load(frontmatter), rules_body


def gate_g3_ability_types(body: str) -> list[str]:
    """Every bracketed ability name must be followed by a declared ability type."""
    failures = []
    for section in re.findall(r"\[([^\]]+)\]\s*(\([^)]*\))?", body):
        ability_name, declared = section
        if ability_name in ABILITY_TYPES:
            continue
        if not declared:
            failures.append(f"G3: ability [{ability_name}] declares no ability type")
            continue
        inner = declared.strip("()")
        if inner not in ABILITY_TYPES and inner not in KEYWORD_NAMES:
            failures.append(f"G3: ability [{ability_name}] declares unknown type '{inner}'")
    return failures


def gate_g4_keyword_exclusivity(card: dict) -> list[str]:
    faction = card.get("faction")
    failures = []
    for side in ("base", "ascended"):
        for keyword in (card.get(side) or {}).get("keywords") or []:
            owner = KEYWORD_FACTION.get(keyword)
            if owner is None:
                failures.append(f"G4: unknown keyword '{keyword}' on {side} side")
            elif owner != faction:
                failures.append(f"G4: {side} keyword '{keyword}' belongs to {owner}, card is {faction}")
    return failures


def gate_g6_status_duration(body: str) -> list[str]:
    lowered = body.lower()
    applied = [s for s in STATUS_NAMES if re.search(rf"\b{re.escape(s.lower())}\b", lowered)]
    if applied and not any(phrase in lowered for phrase in DURATION_PHRASES):
        return [f"G6: applies status ({', '.join(applied)}) with no stated duration"]
    return []


def gate_g8_identity(card: dict) -> list[str]:
    failures = []
    if not card.get("faction"):
        failures.append("G8: no faction")
    if not (card.get("art") or {}).get("base"):
        failures.append("G8: no base art reference")
    if "crew" not in card:
        failures.append("G8: crew key absent (use `crew: null` with a reason if intentional)")
    return failures


def main() -> int:
    global KEYWORD_FACTION, KEYWORD_NAMES, STATUS_NAMES
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", help="stub cards fail instead of skipping")
    args = parser.parse_args()

    KEYWORD_FACTION = {k["name"]: k["faction"] for k in load_yaml("data/keywords.yaml")["keywords"]}
    KEYWORD_NAMES = set(KEYWORD_FACTION)
    STATUS_NAMES = [s["name"] for s in load_yaml("data/status-effects.yaml")["status_effects"] if s["name"]]

    total_failures, stubs, checked = 0, 0, 0
    for path in sorted((REPO_ROOT / "cards").rglob("*.md")):
        if path.name.upper().startswith("README"):
            continue
        try:
            card, body = split_card(path)
        except ValueError as exc:
            print(f"{path.relative_to(REPO_ROOT)}\n  PARSE: {exc}")
            total_failures += 1
            continue

        if card.get("status") == "draft" and not args.strict:
            stubs += 1
            continue

        checked += 1
        failures = (gate_g3_ability_types(body) + gate_g4_keyword_exclusivity(card)
                    + gate_g6_status_duration(body) + gate_g8_identity(card))
        if failures:
            total_failures += len(failures)
            print(f"\n{path.relative_to(REPO_ROOT)}  ({card.get('name')})")
            for failure in failures:
                print(f"  {failure}")

    print(f"\n{checked} cards checked, {stubs} stubs skipped, {total_failures} gate failures")
    print("\nGates requiring human judgement (not checked here):")
    for gate, description in sorted(HUMAN_ONLY_GATES.items()):
        print(f"  {gate}  {description}")
    print("\nRun `python tools/balance.py --failing` for G1.")
    return 1 if total_failures else 0


if __name__ == "__main__":
    sys.exit(main())
