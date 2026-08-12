# The Rulebook

The rulebook is the **authoritative source** for how the game works. Where the rulebook and
any spreadsheet, card file, or data file disagree, the rulebook wins — and the disagreement
gets logged in [`../design/open-questions.md`](../design/open-questions.md).

| § | Section | Covers |
|---|---|---|
| 01 | [Overview & Win Conditions](01-overview-and-win-conditions.md) | Match structure, Life Points, the three victories |
| 02 | [Deck Construction & Zones](02-deck-construction-and-zones.md) | Pool size, Ascendant limits, the seven zones |
| 03 | [The Factions](03-factions.md) | Warmongers, Overthinkers, Assholes, Icons — identity and printed weakness |
| 04 | [The Command System](04-command-system.md) | Why you need a live Character to cast anything |
| 05 | [Card Types & Subtypes](05-card-types.md) | Character, Tactic, Attachment, Commandment |
| 06 | [Anatomy of a Character](06-character-anatomy.md) | PA / PH / MA / MH, lethality, ability types |
| 07 | [The Economy](07-economy.md) | The Investment Engine, Energy, the Blind Commit |
| 08 | [Round Structure](08-round-structure.md) | The Ping-Pong System, the three phases |
| 09 | [The Combat Wave & The Stack](09-combat-and-stack.md) | Declaration, Reaction Window, LIFO resolution |
| 10 | [Ascendants & Leveling Up](10-ascendants.md) | The VIP Area, the Flip, permadeath |
| 11 | [Status Effects](11-status-effects.md) | The six statuses |
| 12 | [Keywords](12-keywords.md) | Faction-exclusive keywords, and what each costs |
| 13 | [Glossary](13-glossary.md) | Universal terms |
| 14 | [Randomization](14-randomization.md) | The Roll — who rolls, when, and why it is sealed |

## Editing rules

1. One concept, one home. If a rule appears in two sections, one of them is a cross-link.
2. Every rules term that has a precise meaning is **bolded on first use in its home section**
   and appears in the [Glossary](13-glossary.md) or in the section that owns it.
3. Changing a rule that a card depends on means updating that card in the same commit.
   Run `python tools/validate.py` to find the dependents.
4. Numbers that the balance engine consumes (keyword points, effect points) live in `data/`,
   not here. The rulebook says what a keyword *does*; `data/keywords.yaml` says what it *costs*.
