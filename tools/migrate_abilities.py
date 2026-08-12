#!/usr/bin/env python3
"""Migrate card rules text from prose into structured abilities. Run once.

    python tools/migrate_abilities.py                 # dry run, writes the review files
    python tools/migrate_abilities.py --apply         # write the cards
    python tools/migrate_abilities.py --review-dir D  # where the review files land

THE SAFETY PROPERTY. A card is written only if regenerating its rules text from the parsed
fields reproduces the original once runs of whitespace are collapsed. Any change to a word or
a mark of punctuation refuses that card. Migration can re-wrap; it can never reword a card
about a real person.

WHAT IT WILL NOT GUESS. Two things, both real design decisions:

  * `type`, when the card put a keyword in the type slot. Ten abilities read `(Protector)`
    or `(Juggernaut)` where the ability type belongs. Which type each one is depends on the
    rulebook, not on a heuristic, so `type` is left empty and gate G3 reports it. check.py is
    the worksheet.
  * `requires`, the gate an ability puts in front of its effect. The whole rules sentence goes
    into `mechanics` and `requires` is left empty. Splitting it means deciding where a cost ends
    and an effect begins, and the round-trip check cannot catch a wrong answer -- both orderings
    concatenate to the same text. An empty `requires` is schema-legal and prints identically.

THE ONE GUESS IT DOES MAKE is the immersion/mechanics boundary, and it is bounded by shape:

  * 4 abilities carry a die-roll or tier table. Flavour is the first sentence; everything after
    it keeps its exact line structure.
  * 22 abilities already put flavour on its own line. That newline IS the boundary -- reading it
    is not a guess. (An earlier draft of the design read these 22 as accidental hand-wrapping and
    proposed collapsing them, which would have destroyed the only signal that locates the split.)
  * 44 abilities are a single line. Flavour is the first sentence. This is the real guess, and
    every one of them is listed in the splits review file.
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

import card_io
import scoring

HEADER = re.compile(r"^[ \t]*\[([^\]]+)\][ \t]*(?:\(([^)]*)\))?[ \t]*:", re.M)
OUTCOME_ROW = re.compile(r"^[ \t]*(?:\d+[ \t]*[-–][ \t]*\d+|\d+)[ \t]*(?:\([^)]*\))?[ \t]*:", re.M)
SENTENCE_END = re.compile(r"(?<=[.!?])[ \t]+")
LEADING_PAREN = re.compile(r"^[ \t]*\(([^)]*)\)[ \t]*:?[ \t]*")

SIDES = ("base", "ascended")


def normalise(text: str) -> str:
    """Collapse every run of whitespace. The only difference migration may introduce."""
    return " ".join(text.split())


# Rules vocabulary. A candidate immersion containing any of this is not flavour -- it is the
# card's mechanics, and assigning it to `immersion` would file rules text as lore and corrupt
# every D3 score. Deliberately narrow: technical markers only, so ordinary prose about a real
# person never trips it.
#
# Tuned against all 70 candidate immersions, not guessed. A first draft also matched `inflict`,
# `Sacrifice` and `Murder`, which are ordinary English as well as game terms -- it misread
# Decoy's "more agonizing than anything the enemy could inflict" and Tasha's flavour as rules.
# Only zone names, stat abbreviations, signed numbers and named windows survive. Flags 8 of 70,
# and all 8 really are rules text with no flavour written for them.
RULES_WORDS = re.compile(
    r"\((?:PA|PH|MA|MH)\)|\b(?:PA|PH|MA|MH)\b"
    r"|\bEnergy\b|\bLife Points\b|\bCombat Wave\b|\bReaction Window\b|\bResource Row\b"
    r"|\bGraveyard\b|\bVIP Area\b|\bPhase \d\b|\bd6\b|[+-]\d|\bonce per (?:Round|Game)\b")


def looks_mechanical(text: str) -> bool:
    return bool(RULES_WORDS.search(text))


def split_body(body: str) -> tuple[str, str, str]:
    """(immersion, mechanics, which rule fired).

    Flavour first, rules second, is how the corpus is written. The job is finding the boundary
    without inventing one -- and without filing rules text as flavour when there is no flavour
    at all, which 10 abilities turn out to be.
    """
    body = body.strip()
    if not body:
        return "", "", "empty"

    def guard(immersion: str, mechanics: str, rule: str) -> tuple[str, str, str]:
        """A candidate immersion full of rules vocabulary is not flavour. Keep the body whole."""
        if immersion and looks_mechanical(immersion):
            return "", body.strip("\n"), f"{rule}->all-mechanics"
        return immersion, mechanics, rule

    if OUTCOME_ROW.search(body):
        match = SENTENCE_END.search(body)
        if match:
            return guard(body[:match.start()].strip(), body[match.end():].strip("\n"), "table")
        return "", body.strip("\n"), "table-no-flavour"

    if "\n" in body:
        first, rest = body.split("\n", 1)
        return guard(first.strip(), rest.strip("\n"), "own-line")

    match = SENTENCE_END.search(body)
    if match:
        return guard(body[:match.start()].strip(), body[match.end():].strip(), "first-sentence")
    # A single sentence with no break: mechanics if it reads technical, flavour if it does not.
    # The 10 keyword-carries-the-rule abilities are the flavour case -- their keyword IS the effect.
    return ("", body, "mechanics-only") if looks_mechanical(body) else (body, "", "flavour-only")


def parse_face(text: str, side_keywords: list[str]) -> tuple[list[dict], list[str]]:
    """Parse one face into ability records. Returns (abilities, notes)."""
    types = set(card_io.ability_type_names())
    keywords = set(scoring.keyword_points())
    notes: list[str] = []

    hits = list(HEADER.finditer(text))
    abilities = []
    for index, match in enumerate(hits):
        end = hits[index + 1].start() if index + 1 < len(hits) else len(text)
        name, slot = match.group(1).strip(), (match.group(2) or "").strip()
        body = text[match.end():end]

        kind = claimed = ""
        if slot in types:
            kind = slot
        elif slot in keywords:
            claimed = slot
            notes.append(f"[{name}] put the keyword '{slot}' in the type slot; type left empty for G3")
        elif slot:
            notes.append(f"[{name}] has an unrecognised slot '({slot})'; left as the type verbatim")
            kind = slot

        # Decoy: "[Improved Sangre Por Sangre]: (Fast Ability): He executes..." -- the stray colon
        # put the real type inside the body.
        if not kind:
            lead = LEADING_PAREN.match(body)
            if lead and lead.group(1).strip() in types:
                kind = lead.group(1).strip()
                body = body[lead.end():]
                notes.append(f"[{name}] recovered type '{kind}' from a stray colon in the body")

        # Angel G: "(Juggernaut) Angel soaks up the boos..." -- a keyword marker inside the prose.
        if not claimed:
            lead = LEADING_PAREN.match(body)
            if lead and lead.group(1).strip() in keywords:
                claimed = lead.group(1).strip()
                body = body[lead.end():]
                notes.append(f"[{name}] lifted the keyword '{claimed}' out of the body prose")

        immersion, mechanics, rule = split_body(body)
        record = {"name": name, "type": kind, "immersion": immersion, "mechanics": mechanics}
        if claimed:
            record["keyword"] = claimed
            if claimed not in side_keywords:
                notes.append(f"[{name}] claims keyword '{claimed}' but the side does not declare it "
                             f"(see OQ-18)")
        record["_rule"] = rule
        record["_body"] = body          # post-strip prose, for the safety check
        record["_slot_was"] = slot
        abilities.append(record)
    return abilities, notes


def migrate(card: card_io.Card) -> dict:
    """Parse both faces and verify. Returns a report; does not write."""
    report = {"card": card.name, "path": card.rel_path, "faces": {}, "notes": [],
              "safe": True, "abilities": 0}
    for side in SIDES:
        original = card.rules_text if side == "base" else card.ascended_text
        if not original.strip():
            continue
        abilities, notes = parse_face(original, card.side(side)["keywords"])
        report["notes"] += [f"{side}: {n}" for n in notes]
        if not abilities:
            report["notes"].append(f"{side}: no ability header found; left as prose")
            continue

        clean = [{k: v for k, v in a.items() if not k.startswith("_") and v} for a in abilities]
        regenerated = card_io.print_abilities(clean)

        # THE SAFETY PROPERTY, stated precisely: not one word of rules PROSE may change. Compare
        # each ability's parsed immersion+mechanics against the body it was parsed out of, under
        # whitespace normalisation.
        #
        # Header slots are checked separately and reported, because three changes to them are
        # deliberate and were decided in the design: Decoy's stray colon disappears, Dilo's
        # missing space after the colon is added, and a keyword sitting where the ability
        # type belongs moves into the printed `(Type · keyword)` slot. Folding those in with
        # corruption would mean either refusing all three forever or loosening the check until it
        # stops catching real damage.
        prose_ok, header_changes = True, []
        for ability in abilities:
            rebuilt = f"{ability['immersion']} {ability['mechanics']}"
            if normalise(rebuilt) != normalise(ability["_body"]):
                prose_ok = False
            was, now = ability["_slot_was"], card_io.print_ability(
                {k: v for k, v in ability.items() if not k.startswith("_")}).split("]", 1)[1]
            now = now.split(":", 1)[0].strip(" ()")
            if was != now:
                header_changes.append(f"[{ability['name']}] ({was or '—'}) -> ({now or '—'})")

        report["faces"][side] = {"abilities": abilities, "clean": clean, "ok": prose_ok,
                                 "original": original, "regenerated": regenerated,
                                 "headerChanges": header_changes}
        report["abilities"] += len(abilities)
        if not prose_ok:
            report["safe"] = False
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="write the cards")
    parser.add_argument("--review-dir", default=".", help="where the review files land")
    args = parser.parse_args()

    review = Path(args.review_dir)
    review.mkdir(parents=True, exist_ok=True)

    reports = [migrate(c) for c in card_io.load_all()]
    safe = [r for r in reports if r["safe"] and r["faces"]]
    refused = [r for r in reports if not r["safe"]]
    total = sum(r["abilities"] for r in reports)

    rules_used: dict[str, int] = {}
    splits, diffs, worksheet = [], [], []
    for report in reports:
        for side, face in report["faces"].items():
            for ability, clean in zip(face["abilities"], face["clean"]):
                rules_used[ability["_rule"]] = rules_used.get(ability["_rule"], 0) + 1
                splits.append(
                    f"### {report['card']} · {side} · [{ability['name']}]  ({ability['_rule']})\n"
                    f"- **type:** {ability['type'] or '*** MISSING ***'}"
                    f"{'  · keyword: ' + ability['keyword'] if ability.get('keyword') else ''}\n"
                    f"- **immersion:** {ability['immersion'] or '*(none)*'}\n"
                    f"- **mechanics:** {ability['mechanics'][:400] or '*(none)*'}\n")
                if not ability["type"]:
                    worksheet.append(f"{report['card']} · {side} · [{ability['name']}]"
                                     f"{'  (keyword: ' + ability['keyword'] + ')' if ability.get('keyword') else ''}")
            if normalise(face["original"]) != normalise(face["regenerated"]) or \
                    face["original"] != face["regenerated"]:
                diffs.append(f"--- {report['card']} · {side}\n" + "\n".join(
                    difflib.unified_diff(face["original"].split("\n"),
                                         face["regenerated"].split("\n"),
                                         lineterm="", n=1)))

    (review / "splits.md").write_text(
        "# Immersion / mechanics splits — review\n\n"
        "The `own-line` ones were read off an existing newline and are not guesses. The\n"
        "`first-sentence` ones are. Scan those.\n\n" + "\n".join(splits), encoding="utf-8")
    (review / "rewrap.diff").write_text("\n".join(diffs) or "(no textual change)\n",
                                        encoding="utf-8")
    (review / "missing-types.txt").write_text(
        "Abilities with no ability type. Each needs a rulebook decision, not a heuristic.\n"
        "check.py reports these as F6 once migration lands.\n\n" + "\n".join(worksheet),
        encoding="utf-8")

    print(f"{len(reports)} cards · {total} abilities")
    print("  boundary rule used:", ", ".join(f"{k}={v}" for k, v in sorted(rules_used.items())))
    print(f"  safe to migrate: {len(safe)}")
    print(f"  REFUSED (text would change): {len(refused)}")
    for report in refused:
        print(f"    REFUSED {report['card']}")
        for side, face in report["faces"].items():
            if not face["ok"]:
                for line in difflib.unified_diff(
                        normalise(face["original"]).split(" "),
                        normalise(face["regenerated"]).split(" "), lineterm="", n=0):
                    if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
                        print(f"        {line}")
    changes = [(r["card"], s, c) for r in reports for s, f in r["faces"].items()
               for c in f["headerChanges"]]
    print(f"  abilities with no type: {len(worksheet)}")
    print(f"  header slots normalised: {len(changes)} (declared, see design)")
    for card, side, change in changes:
        print(f"      {card} · {side} · {change}")
    print(f"  review files in {review.resolve()}")

    if not args.apply:
        print("\ndry run — pass --apply to write")
        return 0
    if refused:
        print("\nrefusing to write anything while any card is refused")
        return 1

    written = 0
    for report in reports:
        if not report["faces"]:
            continue
        card = card_io.load(card_io.REPO_ROOT / report["path"])
        for side, face in report["faces"].items():
            block = card.meta.setdefault(side, {})
            items = list(block.items())
            block.clear()
            block.update(items)
            block["abilities"] = face["clean"]
        card.path.write_text(card_io.render(card), encoding="utf-8")
        written += 1
    print(f"\nwrote {written} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
