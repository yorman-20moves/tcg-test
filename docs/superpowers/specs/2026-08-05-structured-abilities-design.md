# Structured Abilities — design

**Date:** 2026-08-05 · **Branch:** `studio-legibility` · **Status:** approved, not yet implemented

## Why

Gate G3 reported that Decoy's `[Improved Sangre Por Sangre]` "declares no ability type" while the
card plainly reads `(Fast Ability)`. The cause is one stray colon —
`[Improved Sangre Por Sangre]: (Fast Ability):` — against a regex in `tools/scoring.py` that
requires the type to sit immediately after `]`:

```python
re.findall(r"\[([^\]]+)\]\s*(\([^)]*\))?", text)
```

The defect is not the regex. It is that **the gate asserted absence from its own failure to
parse**. All it knew was "I could not read this"; what it printed was "this does not exist."

Tightening the pattern fixes one card. The corpus says the problem is larger.

### What the corpus actually contains

Measured across all 31 cards, 70 ability paragraphs:

| | count |
|---|---|
| Canonical `[Name] (Type): flavour. mechanics.` | 57 |
| Type present but malformed (the false error) | 1 |
| **No ability type at all** | **12** |
| Carrying a die-roll or tier outcome table | 4 |
| Soft-wrapped across lines by hand | 23 |

Ten of the twelve put a **Role keyword** where the type goes — `(Protector)`, `(Juggernaut)`,
`(Berserker)`, `(Infiltrator)`, `(Executioner)`, `(Extortionist)`, `(Combo-Striker)`,
`(Hustler +1/+2)`. `_gate_g3` passes them because it accepts
`ABILITY_TYPES | keyword_points()` in that slot. So the bracket slot is **overloaded** — it means
"type" on 57 abilities and "Role" on 10 — and those 10 have no declared ability type today,
in violation of `docs/rulebook/06-character-anatomy.md`:

> **Card-writing rule:** every printed ability must declare its type in brackets. A card whose
> ability type is unstated fails gameplay gate **G3**.

Ruvi's two abilities are undeclared outright.

Separately, **eight distinct scrapers** read this same prose (`rules.py` ×4, `scoring.py` ×2,
`studio.py` ×2). Every one is the same false-positive class waiting to happen.

And 58 of 70 bodies already split flavour-then-mechanics. The "immersion sentence" is not a new
concept being imposed on the cards — it is already how they are written, and it is lore rubric
**D3 Mechanical fusion** ("flavor explains rules"). Modelling it makes D3 scorable per ability
rather than per card.

## Decisions taken

| # | Decision | Rejected alternative |
|---|---|---|
| 1 | Frontmatter owns abilities; the markdown body is **generated** | Prose stays authoritative with a tolerant parser — keeps a parser forever, so the false-positive class shrinks but never closes |
| 2 | Ability record = `name`, `type`, `immersion`, `requires`, `mechanics`, optional `role` | Four core fields only — leaves `requires` invisible to `check.py` |
| 3 | Types live in `data/ability-types.yaml` and **generate** the rulebook table | Four types closed forever; or Studio-only editing with no data file |
| 4 | Studio shows each ability collapsed to its printed line, expanding to fields | All fields always visible; or base/ascended paired in two columns |

## 1. Data model

### `data/ability-types.yaml` (new)

```yaml
- key: standard
  name: Standard Ability
  when_usable: Only during Phase 2, as your single alternating action.
  requires_joiner: ": "     # a cost you pay
- key: fast
  name: Fast Ability
  when_usable: The only abilities fast enough for the Reaction Window or the Stack.
  requires_joiner: ": "
- key: trigger
  name: Trigger Ability
  when_usable: Costs no action. Fires automatically the moment its condition is met.
  requires_joiner: ", "     # a condition that fires
- key: passive
  name: Passive Ability
  when_usable: Always on, continuously, while the Character is face-up on the Board.
  requires_joiner: ", "
```

`requires_joiner` is what makes a type self-describing: it declares both *when the ability may be
used* and *how it prints*. Nothing about a fifth type ends up hardcoded in Python.

### Card frontmatter

Abilities nest inside the existing `base` / `ascended` blocks. The rulebook's flip *replaces* the
side (`docs/rulebook/10-ascendants.md`), so the two lists are independent — an ascended side
reprints anything it keeps.

```yaml
base:
  keywords: []
  effects: [Direct Damage/Heal 5, Permanent Buff 2]
  abilities:
    - name: La Familia
      type: Passive Ability
      immersion: Decoy's punishment for hesitation is far more agonizing than anything the enemy could inflict.
      mechanics: All allied Latin Kings gain +2 Physical Attack (PA).
    - name: Sangre Por Sangre
      type: Fast Ability
      immersion: Blood pays for blood, and Decoy uses his pawns as living weapons.
      requires: Pay 1 Energy and Sacrifice an allied Latin King
      mechanics: Deal permanent Physical Health (PH) damage equal to the Sacrificed Character's current PA to a target enemy Character.
```

**Field reference**

| Field | Required | Meaning |
|---|---|---|
| `name` | yes | The bracketed ability name |
| `type` | yes | Display name from `data/ability-types.yaml` |
| `immersion` | yes | The sentence that puts the player inside the card's world (lore D3) |
| `mechanics` | yes | What the ability does, in rules language |
| `requires` | no | The gate to the effect — a cost for Standard/Fast, a condition for Trigger |
| `role` | no | The Role keyword this ability is expressed through |

`type` and `role` are stored as **display names**, not keys, matching how `keywords` and `effects`
already work — so `tools/rename.py` keeps working and the YAML reads like the card.
(`data/jobs.yaml` uses keys; abilities follow the keyword convention instead, because these are
printed rules terms.)

## 2. Print grammar

One rule, applied by `card_io.render()`:

```
[{name}] ({type}{ · role}): {immersion} {requires}{joiner}{mechanics}
```

`{requires}{joiner}` is omitted entirely when `requires` is empty.

### Wrapping policy

**One ability, one line — except where the line breaks carry meaning.** A measured decision:

- **23 of 70** abilities are soft-wrapped across lines at inconsistent widths (measured 19 to 267
  characters, 22 lines already over 100). That is accumulated hand-editing, not a format.
  Generation **collapses** it. Re-wrapping to a fixed width instead would make every future word
  change re-flow the rest of the paragraph; one line per ability keeps a word change to a
  one-line diff.
- **4 of 70** carry deliberate internal structure — die-roll and tier outcome tables. Generation
  **preserves** these verbatim.

```
[Teabag] (Trigger Ability): Caleb dances on their bodies and ruins their game. When an
enemy Character is Murdered, pay 1 Energy to roll a 6-sided die (d6) and target an enemy
Character:
1-3: Inflict Exhausted.
4-5: Inflict Silenced.
6: Inflict Stunned.
```

The four are **Caleb** (`[Teabag]`, `[Red Ring of Death]`), **Julito** (`[The EX Enhancements]`,
a Level 1 / Level 2 tier table) and **Ruvi** (`[The Item Box]`, a six-outcome d6 table).

`mechanics` is therefore a YAML block scalar (`|`) when it holds an outcome table, and a plain
string otherwise. **No `outcomes:` schema.** Four abilities do not justify a new concept, and a
block scalar preserves them exactly at zero cost. If outcome tables proliferate, structure them
then — noted in §8.

**Discrimination rule for migration:** within an ability body, a single newline is soft wrap and
collapses; a blank line, or a line matching an outcome row (`1-3:`, `Level 2:`, `6 (Mushroom):`),
marks deliberate structure and the line breaks from that point are preserved.

**Verified:** under this grammar, **55 of the 57 canonical abilities reproduce exactly** once
whitespace is normalised. The two exceptions are both improvements, not losses:

- **Dilo** `[Gag Order]` prints `(Fast Ability):Dilo guarantees…` — a missing space after the
  colon. Generation normalises it.
- **Julito** `[The EX Enhancements]` is the tier table above; it reproduces once structure
  preservation is applied.

`### Rules Text` and `### Ascended Rules Text` join the generated-document set: **never
hand-edited**, with `generate.py --check` failing on staleness. This extends CLAUDE.md rule 6,
which currently names `03-factions.md`, `12-keywords.md` and `crews.md`. The rulebook's
"Character Ability Types" table in `06-character-anatomy.md` becomes generated from
`data/ability-types.yaml` and joins the same set.

**Consequence to document in CLAUDE.md:** hand-editing the Rules Text section of a card file
stops being legal. Editing goes through the Studio or through the frontmatter.

## 3. Gates

**G3 stops being a parser.** `type` is a field validated against `data/ability-types.yaml`. A
false negative becomes structurally impossible — there is no prose to misread. Decoy's error
disappears because the regex is gone, not because it got smarter.

G3's failure messages become:

- `ability [Name] has no type` — the field is empty
- `ability [Name] declares unknown type 'X'` — not in `data/ability-types.yaml`

The other seven scrapers keep reading the *generated* text, so nothing breaks. Retargeting them at
`mechanics` specifically — G6's duration hunt above all — is a follow-up, explicitly out of scope.

## 4. Studio surface

`faceText()` in `tools/studio.html` swaps its two tall textareas for ability lists in the same two
side-rule sections it uses today. The level-up condition stays a textarea — it is not an ability.

```
BASE SIDE                                          + Add ability
────────────────────────────────────────────────────────────────
  [La Familia] (Passive Ability)                          ⌄   ✕
  [Sangre Por Sangre] (Fast Ability)                      ⌃   ✕
      Name       ┃ Sangre Por Sangre                          ┃
      Type       ┃ Fast Ability ▾ ┃  Role  ┃ — none — ▾ ┃
      Immersion  ┃ Blood pays for blood, and Decoy uses his   ┃
                 ┃ pawns as living weapons.                   ┃
      Requires   ┃ Pay 1 Energy and Sacrifice an allied Latin ┃
      Mechanics  ┃ Deal permanent Physical Health (PH) damage ┃
                 ┃ equal to the Sacrificed Character's...     ┃
      ─────────────────────────────────────────────────────────
      prints as: [Sangre Por Sangre] (Fast Ability): Blood pays
      for blood, and Decoy uses his pawns as living weapons. Pay
      1 Energy and Sacrifice an allied Latin King: Deal perman…
```

Requirements:

- **Add** appends an empty ability to that side; **✕** deletes with confirmation; rows reorder.
- The live `prints as` line renders the §2 grammar, so the card's voice is never out of sight.
- The **Role** dropdown is filtered to the card's faction, so G4 cannot be violated by
  construction.
- The **Type** dropdown lists `data/ability-types.yaml`. Creating a type happens on the Library
  screen beside keywords and effects, and requires `when_usable`, `requires_joiner`, and a
  defence recorded in `docs/design/decisions.md` against at least two existing types — the same
  rule that governs pricing a new keyword.

## 5. Migration

`tools/migrate_abilities.py`, run once, with a hard safety property:

> It regenerates each card's rules text from the parsed fields and **refuses to modify any card
> whose regenerated output differs from the original once runs of whitespace are collapsed.**
> Any change to a word or a mark of punctuation aborts that card.

The comparison is whitespace-normalised rather than byte-exact, because §2 collapses the 23
soft-wrapped paragraphs. That is the one intended difference, and it is the *only* difference the
check tolerates. Migration writes the re-wrap diff to the review file so the churn is seen rather
than assumed, and the whole migration lands as its own commit so `git show` isolates it.

### Finding ability boundaries

Getting this wrong is the easiest way to corrupt the migration, and both naive rules fail:

- **"Split on blank lines"** breaks the 4 outcome-table abilities into fragments — it was how
  Julito's `[The EX Enhancements]` first looked like an ability with an empty body.
- **"Any line starting with `[`"** over-matches cross-references. Laura's
  `[Fatal Attraction] now costs 0 Energy.` is prose *referring* to another ability, not a new
  ability header. Treating it as one invents a 71st ability that does not exist.

The correct rule, which yields exactly 70:

```python
HEADER = re.compile(r"^\s*\[[^\]]+\]\s*(?:\([^)]*\))?\s*:")
```

A header is a bracketed name, an optional parenthesised slot, then a colon. An ability runs from
one header to the line before the next — blank lines included. Laura's reference has no colon
after the bracket and is correctly swallowed into the body it belongs to.

This rule must be unit-tested against Laura, Julito, Caleb, Ruvi and Decoy specifically. Each one
breaks a different simpler rule.

| Case | count | Outcome |
|---|---|---|
| Canonical `[Name] (Type): …` | 57 | Auto-migrate, round-trip verified |
| Decoy's stray colon | 1 | Auto-migrate, round-trip verified |
| Keyword in the type slot | 10 | `role` filled, `type` left blank, card flagged |
| Ruvi, undeclared | 2 | Flagged |

Two things migration must not guess:

**a) The 12 missing ability types.** Real design decisions. `Masochist (Protector)` reads like a
Fast Ability from "As a Reaction," but the rulebook decides that, not a heuristic. Migration emits
a 12-line worksheet; a human fills it.

**b) The immersion/mechanics split.** The round-trip check **cannot** validate this — both
orderings concatenate to identical text. Migration emits all 70 proposed splits as a single review
file for one scanning pass, rather than 31 card visits.

### Open decision — printed text on 10 cards

Fixing the 10 keyword-slot abilities changes what they print, because `(Protector)` alone violates
the rulebook's "must declare its type in brackets." Two options:

- `[Masochist] (Fast Ability)` — the Role is already in frontmatter, so nothing is lost to the
  machine
- `[Masochist] (Fast Ability · Protector)` — keeps the Role in the card's voice

**Default if not revisited: print both.** It is real flavour, and 9 of the 10 already declare the
keyword in frontmatter. This must be confirmed before migration runs, because it edits the printed
text of cards about real people.

### Data bug found during design

**Julio, The Tyrant of the Tainted Touch** — the ascended ability `[The Meek Executioner]` claims
`(Executioner)`, but `ascended.keywords` is empty. No current gate can see this. File as
**OQ-16**; the structured model makes this class of mismatch checkable, since `role` must name a
keyword the side actually declares.

## 6. The scroll bug (independent fix, same change)

Not an abilities bug, but it shares a root shape: prose in tall auto-sizing textareas.

`tools/studio.html:1230` sizes each textarea inside `requestAnimationFrame`. On every re-render the
boxes collapse to their 52px CSS minimum; `preservingFocus` then restores `scrollTop` against the
*collapsed* panel, the browser clamps it to the smaller `scrollHeight - clientHeight`, and `grow()`
restores the height a frame later without undoing the clamp. The view lands somewhere else.

Confirmed: the collapse is real (boxes measure 70px before `grow()` runs, against a settled height
of several hundred). **Not yet confirmed:** that the clamp fires at a real scroll position — the
measurement timed out. Implementation must reproduce the clamp before fixing it.

Fix, in `preservingFocus`:

```js
const tops = panes.map(p => p.scrollTop);
render();          // build + append
flushGrowers();    // NEW — size every auto-grow textarea now, synchronously
panes.forEach((p, i) => { p.scrollTop = tops[i]; });   // height is final, no clamp
```

`cardText()` registers its grower in a render-scoped list instead of calling
`requestAnimationFrame` itself. Because every clickable in the card view routes through
`renderMain()`, this one change covers Job chips, keyword chips, effect pickers, window ticks and
steppers together.

Then the explicit audit: every clickable control in `studio.html` verified to do what it says and
nothing else.

## 7. Testing

| Test | Asserts |
|---|---|
| Round-trip, all 31 cards | `render(load(p))` equals the original bytes — the property CLAUDE.md already claims. Must hold **after** migration has landed, since generation then owns the section |
| Migration round-trip | Every auto-migrated card regenerates identically under whitespace normalisation, else it is refused |
| Re-wrap is whitespace-only | For all 24 wrapped paragraphs, original and regenerated are equal after collapsing whitespace — proves the one tolerated difference really is only wrapping |
| G3 valid / empty / unknown type | Passes, fails, fails — with the right message |
| `generate.py --check` staleness | Fails when `06-character-anatomy.md` or a card body is stale |
| Print grammar per type | Each `requires_joiner` produces the corpus's existing text |
| Role/keyword agreement | An ability's `role` must appear in that side's `keywords` (catches Julio) |
| Boundary rule, named cards | Laura yields no phantom ability; Julito/Caleb/Ruvi stay whole; Decoy parses. 70 total, not 69 or 71 |
| Outcome tables survive | The 4 structured abilities regenerate with their line breaks intact |
| Render height stability | `#main.scrollHeight` after render equals its value one frame later |

## 8. Out of scope

Retargeting the other seven prose scrapers · a `duration` field for G6 · ability-level rubric
scoring · `upgrades:` pairing between base and ascended abilities · a structured `outcomes:` schema
for die-roll and tier tables. All defensible later; none needed to make this work.

## 9. Weakest parts

**The immersion/mechanics split is the one lossy step in an otherwise lossless migration.**
Everything else is provable — the round-trip check makes the text mathematically safe. The split is
a guess dressed as data, and once it is in fields nobody will re-examine it. The review file is not
optional polish; it is the only thing between the project and 70 silently-wrong D3 scores.

**`requires_joiner` assumes every future ability type prints as flavour → gate → effect.** A type
needing a different shape would have to change the grammar, not just add a row.

**The outcome tables are held as opaque text.** Four abilities (Caleb ×2, Julito, Ruvi) carry
die-roll and tier tables inside `mechanics` as a block scalar. Nothing checks that a d6 table
covers 1–6 exactly once, or that Julito's tiers match his 3-token maximum. That is the correct
trade at n=4 — but it is a known blind spot, not an oversight, and the moment a fifth appears the
`outcomes:` schema in §8 stops being deferrable.

**Migration surfaces 12 pieces of design work that do not exist yet.** That is the honest cost of
this change: it converts a hidden gate hole into visible, unavoidable work.
