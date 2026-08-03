#!/usr/bin/env python3
"""Rename a keyword, effect, crew, faction or game state everywhere at once.

Renaming by hand breaks references silently -- a card keeps the old name, the balance engine
scores it as zero, and nothing tells you. This updates every file that mentions it.

    python tools/rename.py effect  "Permanent Buff 5" "Permanent Buff 5+"
    python tools/rename.py crew    PWNED Pwners
    python tools/rename.py --dry-run keyword Prowler Ghost

Always run `python tools/check.py` afterwards.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import card_io  # noqa: E402

KIND_FILES = {
    "keyword": ["data/keywords.yaml"],
    "effect": ["data/effects.yaml"],
    "crew": ["data/crews.yaml"],
    "faction": ["data/factions.yaml"],
    "state": ["data/game-states.yaml"],
    "status": ["data/status-effects.yaml"],
}


def targets(kind: str) -> list[Path]:
    paths = [card_io.REPO_ROOT / p for p in KIND_FILES[kind]]
    paths += sorted(card_io.CARDS_DIR.rglob("*.md"))
    paths += [card_io.REPO_ROOT / "data" / "factions.yaml",
              card_io.REPO_ROOT / "data" / "crews.yaml"]
    paths += sorted((card_io.REPO_ROOT / "docs").rglob("*.md"))
    seen, unique = set(), []
    for path in paths:
        if path.exists() and path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kind", choices=sorted(KIND_FILES))
    parser.add_argument("old")
    parser.add_argument("new")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    pattern = re.compile(re.escape(args.old))
    touched, total = [], 0
    for path in targets(args.kind):
        text = path.read_text(encoding="utf-8")
        hits = len(pattern.findall(text))
        if not hits:
            continue
        total += hits
        touched.append((path, hits))
        if not args.dry_run:
            path.write_text(pattern.sub(args.new, text), encoding="utf-8")

    verb = "would change" if args.dry_run else "changed"
    for path, hits in touched:
        print(f"  {hits:>3}x  {path.relative_to(card_io.REPO_ROOT)}")
    print(f"\n{verb} {total} reference(s) across {len(touched)} file(s)")
    if touched and not args.dry_run:
        print("\nNow run:  python tools/generate.py && python tools/check.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
