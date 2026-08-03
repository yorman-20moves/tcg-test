#!/usr/bin/env python3
"""Check the whole game for consistency. One command, one exit code.

    python tools/check.py              # everything, ranked worst-first
    python tools/check.py --errors     # only what blocks
    python tools/check.py --code F2    # one rule
    python tools/check.py --next 5     # the five things to fix now
    python tools/check.py --json       # machine-readable

Exit code is the number of blocking errors, capped at 125.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rules  # noqa: E402

SEVERITY_MARK = {"error": "✗", "warning": "!", "gap": "+"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--errors", action="store_true", help="only blocking errors")
    parser.add_argument("--warnings", action="store_true", help="only warnings")
    parser.add_argument("--code", help="filter to one rule code, e.g. F2")
    parser.add_argument("--next", type=int, metavar="N", help="just the next N things to fix")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--gaps", action="store_true", help="what's MISSING, not what's wrong")
    parser.add_argument("--quiet", action="store_true", help="summary only")
    args = parser.parse_args()

    findings = rules.worklist(rules.run_all() + rules.gaps())
    blocking = [f for f in findings if f.blocking]

    shown = findings
    if args.errors:
        shown = [f for f in shown if f.blocking]
    if args.warnings:
        shown = [f for f in shown if f.severity == "warning"]
    if args.gaps:
        shown = [f for f in shown if f.severity == "gap"]
    if args.code:
        shown = [f for f in shown if f.code == args.code.upper()]
    if args.next:
        shown = shown[:args.next]

    if args.json:
        print(json.dumps([f.as_dict() for f in shown], indent=1))
        return min(len(blocking), 125)

    if not args.quiet:
        current = None
        for finding in shown:
            if finding.code != current:
                current = finding.code
                print(f"\n── {current} " + "─" * (72 - len(current)))
            print(f"  {SEVERITY_MARK[finding.severity]} {finding.subject}: {finding.message}")
            if finding.where:
                print(f"      {finding.where}")
            if finding.fix:
                print(f"      fix: {finding.fix}")

    counts = Counter(f.code for f in findings)
    print("\n" + "=" * 78)
    print(f"{len(blocking)} blocking, {len(findings) - len(blocking)} warnings"
          f"   ({', '.join(f'{c}×{n}' for c, n in sorted(counts.items()))})")
    if blocking:
        print("\nStart here:")
        for finding in rules.worklist(blocking)[:3]:
            print(f"  • [{finding.code}] {finding.subject}: {finding.message}")
    return min(len(blocking), 125)


if __name__ == "__main__":
    sys.exit(main())
