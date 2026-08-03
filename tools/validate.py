#!/usr/bin/env python3
"""Run the machine-checkable rubric gates over every card.

Covered here: G1 (budget), G3 (ability type declared), G4 (keyword faction exclusivity),
G6 (status applied without a duration), G8 (faction / art / crew present).

G2, G5, G7 and G9 need human judgement and are printed as a reminder, not checked.
See docs/rubrics/gameplay-rubric.md.

Usage:
    python tools/validate.py               # all cards, stubs skipped
    python tools/validate.py --strict      # stub cards fail instead of skipping
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import card_io  # noqa: E402
import scoring  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", help="stub cards fail instead of skipping")
    parser.add_argument("--tolerance", type=int, default=scoring.DEFAULT_TOLERANCE)
    args = parser.parse_args()

    total_failures, stubs, checked = 0, 0, 0
    for card in card_io.load_all():
        if card.meta.get("status") == "draft" and not args.strict:
            stubs += 1
            continue
        checked += 1
        failures = [msg for messages in scoring.gates(card, tolerance=args.tolerance).values()
                    for msg in messages]
        if failures:
            total_failures += len(failures)
            print(f"\n{card.rel_path}  ({card.name})")
            for failure in failures:
                print(f"  {failure}")

    print(f"\n{checked} cards checked, {stubs} stubs skipped, {total_failures} gate failures")
    print("\nGates requiring human judgement (not checked here):")
    for gate, description in sorted(scoring.HUMAN_ONLY_GATES.items()):
        print(f"  {gate}  {description}")
    return 1 if total_failures else 0


if __name__ == "__main__":
    sys.exit(main())
