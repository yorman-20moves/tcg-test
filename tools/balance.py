#!/usr/bin/env python3
"""Point-budget engine for the TCG.

Ports the `Overall Balance` formula that lived in the Master Card DB spreadsheet:

    budget      = (cost * 3) + 1 + (3 if the card is an Ascendant else 0)
    spent       = sum(stats) + sum(base keyword points) + sum(base effect points)
    verdict     = budget - spent

The level-up (ascended) side is currently charged NOTHING. That is the spreadsheet's
behaviour, faithfully reproduced here so ported cards reconcile against their old
verdicts -- it is also a known design hole. See docs/design/open-questions.md (OQ-04)
and the --charge-ascended flag below, which models the proposed fix.

Usage:
    python tools/balance.py                     # score every card
    python tools/balance.py cards/**/alvino*.md # score specific cards
    python tools/balance.py --failing           # only cards outside tolerance
    python tools/balance.py --charge-ascended   # also bill the level-up side
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

ASCENDANT_BUDGET_BONUS = 3
COST_TO_BUDGET_MULTIPLIER = 3
BUDGET_BASE_ALLOWANCE = 1
DEFAULT_TOLERANCE = 0


class CardDataError(Exception):
    """Raised when a card file cannot be scored at all."""


def load_point_table(filename: str, collection_key: str) -> dict[str, int]:
    path = REPO_ROOT / "data" / filename
    if not path.exists():
        raise CardDataError(f"missing point table: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return {entry["name"]: int(entry["points"]) for entry in payload[collection_key]}


def parse_card(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise CardDataError(f"{path}: no YAML frontmatter")
    _, frontmatter, _ = text.split("---", 2)
    return yaml.safe_load(frontmatter)


@dataclass
class Verdict:
    path: Path
    name: str
    budget: int
    spent: int
    stats_total: int
    keyword_points: int
    effect_points: int
    ascended_points: int

    @property
    def delta(self) -> int:
        return self.budget - self.spent

    def label(self, tolerance: int) -> str:
        if abs(self.delta) <= tolerance:
            return "BALANCED"
        return f"OVER by {-self.delta}" if self.delta < 0 else f"UNDER by {self.delta}"


def score_card(path: Path, keyword_points: dict[str, int], effect_points: dict[str, int],
               charge_ascended: bool) -> Verdict:
    card = parse_card(path)

    cost = card.get("cost")
    if cost is None:
        raise CardDataError(f"{card.get('name', path.name)}: no cost defined (stub card)")

    stats = card.get("stats") or {}
    if any(stats.get(k) is None for k in ("PA", "PH", "MA", "MH")):
        raise CardDataError(f"{card.get('name', path.name)}: incomplete stat line")
    stats_total = sum(int(stats[k]) for k in ("PA", "PH", "MA", "MH"))

    def sum_points(names: list[str], table: dict[str, int], kind: str) -> int:
        total = 0
        for entry in names or []:
            if entry not in table:
                raise CardDataError(f"{card.get('name', path.name)}: unknown {kind} '{entry}'")
            total += table[entry]
        return total

    base = card.get("base") or {}
    ascended = card.get("ascended") or {}

    kw_points = sum_points(base.get("keywords"), keyword_points, "keyword")
    ef_points = sum_points(base.get("effects"), effect_points, "effect")
    asc_points = (sum_points(ascended.get("keywords"), keyword_points, "keyword")
                  + sum_points(ascended.get("effects"), effect_points, "effect"))

    is_ascendant = (card.get("subtype") or "").lower() == "ascendant"
    budget = (int(cost) * COST_TO_BUDGET_MULTIPLIER + BUDGET_BASE_ALLOWANCE
              + (ASCENDANT_BUDGET_BONUS if is_ascendant else 0))

    spent = stats_total + kw_points + ef_points
    if charge_ascended:
        spent += asc_points

    return Verdict(path=path, name=card.get("name", path.stem), budget=budget, spent=spent,
                   stats_total=stats_total, keyword_points=kw_points, effect_points=ef_points,
                   ascended_points=asc_points)


def collect_card_paths(argv_paths: list[str]) -> list[Path]:
    if argv_paths:
        return [Path(p) for p in argv_paths]
    return sorted((REPO_ROOT / "cards").rglob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", help="card markdown files (default: all)")
    parser.add_argument("--failing", action="store_true", help="only show cards outside tolerance")
    parser.add_argument("--tolerance", type=int, default=DEFAULT_TOLERANCE,
                        help=f"points of slack allowed either way (default {DEFAULT_TOLERANCE})")
    parser.add_argument("--charge-ascended", action="store_true",
                        help="bill the level-up side against the same budget (proposed rule)")
    args = parser.parse_args()

    keyword_points = load_point_table("keywords.yaml", "keywords")
    effect_points = load_point_table("effects.yaml", "effects")

    verdicts, skipped = [], []
    for path in collect_card_paths(args.paths):
        if path.name.upper().startswith("README"):
            continue
        try:
            verdicts.append(score_card(path, keyword_points, effect_points, args.charge_ascended))
        except CardDataError as exc:
            skipped.append(str(exc))

    shown = [v for v in verdicts if abs(v.delta) > args.tolerance] if args.failing else verdicts
    for v in sorted(shown, key=lambda v: (v.delta, v.name)):
        print(f"{v.name[:44]:46} budget {v.budget:>3}  spent {v.spent:>3}  "
              f"(stats {v.stats_total}, kw {v.keyword_points}, eff {v.effect_points}, "
              f"asc {v.ascended_points})  {v.label(args.tolerance)}")

    failing = [v for v in verdicts if abs(v.delta) > args.tolerance]
    print(f"\n{len(verdicts)} scored | {len(failing)} outside tolerance | {len(skipped)} unscorable")
    for note in skipped:
        print(f"  SKIP {note}")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
