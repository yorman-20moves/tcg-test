#!/usr/bin/env python3
"""Tests for the structured ability model. Run: python tools/test_abilities.py

Every case here is one row of the test table in the structured-abilities design, plus the
regressions found while implementing it. Exit code is the number of failures.
"""
from __future__ import annotations

import re
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import card_io
import generate
import migrate_abilities as M
import rules
import scoring

FAILURES: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  ok    {label}")
    else:
        FAILURES.append(label)
        print(f"  FAIL  {label}" + (f"\n          {detail}" if detail else ""))


def card(slug: str) -> card_io.Card:
    hit = [c for c in card_io.load_all() if c.meta.get("slug") == slug]
    assert hit, f"no card with slug {slug}"
    return hit[0]


def main() -> int:
    cards = card_io.load_all()
    files = [c.path for c in cards]

    print("round-trip")
    drift = [c.rel_path for c in cards
             if card_io.render(c) != c.path.read_text(encoding="utf-8")]
    check("render(load(p)) is byte-identical for all 31 cards, generation now owning the section",
          not drift, f"drifted: {drift}")

    print("\nboundary rule — each named card breaks a different simpler rule")
    counts = {}
    for c in cards:
        n = 0
        for side in ("base", "ascended"):
            text = c.rules_text if side == "base" else c.ascended_text
            n += len(M.HEADER.findall(text))
        counts[c.meta.get("slug")] = n
    check("70 abilities total, not 69 or 71", sum(counts.values()) == 70,
          f"got {sum(counts.values())}")
    laura = card("laura-the-first-lady-of-the-game")
    laura_refs = laura.rules_text + laura.ascended_text
    check("Laura's [Fatal Attraction] cross-reference is not counted as an ability",
          laura_refs.count("[Fatal Attraction]") >= 2
          and len(card_io.load(laura.path).side("base")["abilities"])
          + len(card_io.load(laura.path).side("ascended")["abilities"]) == counts[laura.meta["slug"]],
          "a bracketed name with no following colon must be swallowed into its body")
    for slug, expect in (("caleb", 2), ("julito-harbinger-of-the-demon", 4),
                         ("ruvi-player-one", 3), ("decoy-1st-crown-supreme-inca", 4)):
        c = card(slug)
        got = len(c.side("base")["abilities"]) + len(c.side("ascended")["abilities"])
        check(f"{c.name} parses to {expect} abilities, kept whole", got == expect, f"got {got}")

    print("\nprint grammar, one case per requires_joiner")
    check("Fast/Standard join `requires` with ': '",
          card_io.print_ability({"name": "X", "type": "Fast Ability", "immersion": "Flavour.",
                                 "requires": "Pay 1 Energy", "mechanics": "Do a thing."})
          == "[X] (Fast Ability): Flavour.\nPay 1 Energy: Do a thing.")
    check("Trigger/Passive join `requires` with ', '",
          card_io.print_ability({"name": "X", "type": "Trigger Ability", "immersion": "Flavour.",
                                 "requires": "When it happens", "mechanics": "Do a thing."})
          == "[X] (Trigger Ability): Flavour.\nWhen it happens, Do a thing.")
    check("a keyword prints inside the slot alongside the type",
          card_io.print_ability({"name": "X", "type": "Passive Ability", "keyword": "Juggernaut",
                                 "mechanics": "Spills over."})
          == "[X] (Passive Ability · Juggernaut): Spills over.")
    check("no immersion collapses to a single line",
          card_io.print_ability({"name": "X", "type": "Fast Ability", "mechanics": "Do it."})
          == "[X] (Fast Ability): Do it.")
    check("no type still prints, so G3 has something to complain about",
          card_io.print_ability({"name": "X", "mechanics": "Do it."}) == "[X]: Do it.")

    print("\noutcome tables survive")
    multiline = [(c.name, a["name"]) for c in cards for s in ("base", "ascended")
                 for a in c.side(s)["abilities"] if "\n" in (a.get("mechanics") or "")]
    check("4 abilities keep their internal line breaks", len(multiline) == 4, f"got {multiline}")
    # Three of those four are numeric d6 tables; the fourth is Julito's tier list, which is
    # structured prose rather than a roll table. Both must survive, for different reasons.
    numeric = [t for t in multiline
               if M.OUTCOME_ROW.search(next(
                   a["mechanics"] for c in cards for s in ("base", "ascended")
                   for a in c.side(s)["abilities"] if (c.name, a["name"]) == t))]
    check("3 of them are d6 outcome tables, 1 is Julito's tier list",
          len(numeric) == 3 and ("Julito, Harbinger of the Demon", "The EX Enhancements")
          in set(multiline) - set(numeric), f"numeric: {numeric}")
    teabag = next(a for a in card("caleb").side("base")["abilities"] if a["name"] == "Teabag")
    check("Caleb's d6 table still names an outcome for every result 1-6",
          all(row in teabag["mechanics"] for row in ("1-3:", "4-5:", "6:")))

    print("\nG3 reads fields")
    good = card_io.Card(path=pathlib.Path("x.md"), meta={
        "base": {"abilities": [{"name": "A", "type": "Fast Ability"}], "keywords": []},
        "ascended": {}})
    check("valid type passes", not scoring._gate_g3(good))
    empty = card_io.Card(path=pathlib.Path("x.md"), meta={
        "base": {"abilities": [{"name": "A", "type": ""}], "keywords": []}, "ascended": {}})
    check("empty type fails with 'has no type'",
          scoring._gate_g3(empty) == ["G3: ability [A] has no type"])
    unknown = card_io.Card(path=pathlib.Path("x.md"), meta={
        "base": {"abilities": [{"name": "A", "type": "Sneaky Ability"}], "keywords": []},
        "ascended": {}})
    check("unknown type fails naming the value",
          scoring._gate_g3(unknown) == ["G3: ability [A] declares unknown type 'Sneaky Ability'"])
    check("Decoy's stray colon no longer produces a false G3",
          not [f for f in scoring._gate_g3(card("decoy-1st-crown-supreme-inca"))
               if "Improved Sangre Por Sangre" in f])

    print("\nrole / keyword agreement — the bug no gate could see before")
    mismatch = card_io.Card(path=pathlib.Path("x.md"), meta={
        "base": {"abilities": [{"name": "A", "type": "Fast Ability", "keyword": "Executioner"}],
                 "keywords": []}, "ascended": {}})
    check("a keyword the side does not declare fails",
          any("claims keyword 'Executioner'" in f for f in scoring._gate_g3(mismatch)))
    agreeing = card_io.Card(path=pathlib.Path("x.md"), meta={
        "base": {"abilities": [{"name": "A", "type": "Fast Ability", "keyword": "Executioner"}],
                 "keywords": ["Executioner"]}, "ascended": {}})
    check("a declared keyword passes", not scoring._gate_g3(agreeing))
    check("Julio's [The Meek Executioner] is caught in the live corpus",
          any("claims keyword 'Executioner'" in f
              for f in scoring._gate_g3(card("julio-the-tyrant-of-the-tainted-touch"))))

    print("\nrules-vocabulary guard (the migration defect)")
    check("pure rules text is not filed as flavour",
          M.looks_mechanical("When he attacks, he increases his Physical Attack (PA) by 1."))
    check("flavour using 'inflict' as English is not mistaken for rules",
          not M.looks_mechanical("Decoy's punishment for hesitation is far more agonizing than "
                                "anything the enemy could inflict."))
    check("flavour is left alone",
          not M.looks_mechanical("Caleb dances on their bodies and ruins their game."))

    print("\ngeneration and staleness")
    world = rules.load_world()
    table = generate.ability_types_table(world)
    doc = (card_io.REPO_ROOT / "docs/rulebook/06-character-anatomy.md").read_text(encoding="utf-8")
    check("the ability-types region in §6 is current", table in doc)
    check("every type in the data file reaches the rulebook table",
          all(t["name"] in table for t in card_io.ability_types()))
    check("a hand edit to a card body would be reported stale",
          all(card_io.render(c) == c.path.read_text(encoding="utf-8") for c in cards))

    print("\nYAML shape")
    raw = card("caleb").path.read_text(encoding="utf-8")
    check("a multi-line mechanics field dumps as a literal block, not folded quotes",
          "mechanics: |-" in raw and "mechanics: 'Once per Round" not in raw)

    print("")
    print("vocabulary -- \"Role\" is retired (D-015)")
    # decisions.md is append-only history and the specs are dated design records; both keep the
    # word on purpose. jobs-and-formations.md explains the retirement, so it has to name it.
    SKIP = ("docs/design/decisions.md", "docs/superpowers", "legacy", ".git", ".snapshots",
            ".claude",          # worktrees and tooling state, not the project
            "docs/design/jobs-and-formations.md", "tools/test_abilities.py")
    offenders = []
    for path in card_io.REPO_ROOT.rglob("*"):
        rel = path.relative_to(card_io.REPO_ROOT).as_posix()
        if path.is_dir() or path.suffix not in (".md", ".yaml", ".py", ".html"):
            continue
        if any(rel.startswith(s) for s in SKIP):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for number, line in enumerate(text.split("\n"), 1):
            if re.search(r"\bRoles?\b", line):
                offenders.append(f"{rel}:{number}: {line.strip()[:70]}")
    check("no file uses \"Role\" as a rules term", not offenders,
          "\n          ".join(offenders))
    check("no card frontmatter carries a `role:` field",
          not any("role" in a for c in cards for s in ("base", "ascended")
                  for a in c.side(s)["abilities"]))
    check("the ability schema names the field `keyword`",
          "keyword" in card_io.ABILITY_FIELDS and "role" not in card_io.ABILITY_FIELDS)

    print(f"\n{len(files)} cards checked · {len(FAILURES)} failure(s)")
    for failure in FAILURES:
        print(f"  FAILED: {failure}")
    return len(FAILURES)


if __name__ == "__main__":
    sys.exit(main())
