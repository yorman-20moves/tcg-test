#!/usr/bin/env python3
"""Score every card against its point budget.

    budget = (cost x 3) + 1 + (3 if Ascendant)
    spent  = PA + PH + MA + MH + base keyword points + base effect points

Ported from the `Overall Balance` formula in the original spreadsheet and verified to
reproduce its verdict on all 25 costed cards.

The level-up side is charged NOTHING by default -- the spreadsheet's behaviour, kept so
ported cards reconcile against their old verdicts. It is also the largest known hole in
the system; see docs/design/open-questions.md (OQ-04) and --charge-ascended.

Usage:
    python tools/balance.py                     # score every card
    python tools/balance.py cards/**/alvino*.md # score specific cards
    python tools/balance.py --failing           # only cards outside tolerance
    python tools/balance.py --charge-ascended   # also bill the level-up side
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
    parser.add_argument("paths", nargs="*", help="card markdown files (default: all)")
    parser.add_argument("--failing", action="store_true", help="only show cards outside tolerance")
    parser.add_argument("--tolerance", type=int, default=0,
                        help="points of slack allowed either way (default 0)")
    parser.add_argument("--charge-ascended", action="store_true",
                        help="bill the level-up side against the same budget (proposed rule)")
    args = parser.parse_args()

    cards = ([card_io.load(Path(p)) for p in args.paths] if args.paths else card_io.load_all())

    rows, skipped = [], []
    for card in cards:
        result = scoring.score(card)
        if not result.scorable:
            skipped.append(f"{card.name}: {result.reason}")
            continue
        if result.unknown_names:
            skipped.append(f"{card.name}: unknown name(s) {', '.join(result.unknown_names)}")
            continue
        spent = result.base_spent + (result.ascended_spent if args.charge_ascended else 0)
        rows.append((card, result, spent, result.budget - spent))

    shown = [r for r in rows if abs(r[3]) > args.tolerance] if args.failing else rows
    for card, result, spent, delta in sorted(shown, key=lambda r: (r[3], r[0].name)):
        if abs(delta) <= args.tolerance:
            verdict = "BALANCED"
        else:
            verdict = f"OVER by {-delta}" if delta < 0 else f"UNDER by {delta}"
        print(f"{card.name[:44]:46} budget {result.budget:>3}  spent {spent:>3}  "
              f"(stats {result.stats_total}, kw {result.base_keyword_points}, "
              f"eff {result.base_effect_points}, asc {result.ascended_spent})  {verdict}")

    failing = [r for r in rows if abs(r[3]) > args.tolerance]
    print(f"\n{len(rows)} scored | {len(failing)} outside tolerance | {len(skipped)} unscorable")
    for note in skipped:
        print(f"  SKIP {note}")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
