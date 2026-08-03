# AGENTS.md — working on this project

Read this before touching anything. It is the contract, not an overview.

## What this is

A 1-on-1 trading card game where the cards are the designer's real friends, organized into
four **factions** (methodology) and six **crews** (loyalty). Two things have to be excellent:
the **gameplay** and the **lore**. Both have rubrics. Use them.

## Source of truth — in order

1. **`docs/rulebook/`** — how the game works. Beats everything.
2. **`data/*.yaml`** — what things *cost*. Beats card files and generated docs.
3. **`cards/**/*.md`** — individual cards.
4. **`legacy/`** — the original spreadsheet and docx. **Reference only. Never edit.**

When two disagree, the higher one wins and the conflict gets logged in
`docs/design/open-questions.md`. Do not silently reconcile.

## The two rubrics — this is the main instruction

- **`docs/rubrics/gameplay-rubric.md`** — 9 gates (G1–G9), 9 weighted dimensions (D1–D9)
- **`docs/rubrics/lore-rubric.md`** — 9 gates (L1–L9), 10 weighted dimensions (D1–D10), plus the
  required **Lore Packet**

**Any time you propose a card, mechanic, keyword, or piece of lore, you also report the gates
and score the dimensions.** A proposal without rubric output is incomplete work. Name the
weakest dimension and say how you'd fix it.

**Be adversarial by default.** The failure mode here is agreeable slop — cards that pass because
nobody argued against them. When reviewing anything, including your own output, make the
strongest case that it shouldn't be printed. If a card genuinely passes every gate, say which
dimension is weakest and why it still ships.

## Hard rules

1. **Never invent a rules term.** If a card needs a mechanic the rulebook doesn't define, the
   rulebook edit ships in the same change. Gate G2.
2. **Never invent a True Detail.** The Lore Packet's True Detail is a real fact about a real
   person. Only Yorman can supply it. Ask. Don't approximate it with a plausible-sounding
   biographical detail — that's the one thing that makes these cards fake.
3. **Never cross faction keywords.** Gate G4. `data/keywords.yaml` owns the mapping.
4. **Every ability declares its type** — `(Standard Ability)`, `(Fast Ability)`,
   `(Trigger Ability)`, `(Passive Ability)`. Gate G3.
5. **Run the tools before claiming a card is balanced.**
   ```
   python tools/balance.py --failing      # G1
   python tools/validate.py               # G1, G3, G4, G6, G8
   python tools/studio.py                 # the visual design workbench
   ```
6. **`docs/rulebook/12-keywords.md` is generated** from `data/keywords.yaml`. Edit the YAML.
7. **Append to `## Design Notes`, don't overwrite.** The history of why a card changed is worth
   more than the current state.
8. **Lore gate L2 (the dignity line) is not negotiable and not a joke gate.** These are real
   people. When in doubt, the answer is "ask them," not "it's probably fine."

## File layout

```
docs/rulebook/      the rules, one section per file, 01–13
docs/rubrics/       the two rubrics — read these first
docs/design/        open-questions.md (the backlog) · decisions.md (why) · canon.md (the world)
data/               keywords.yaml · effects.yaml · status-effects.yaml — the point economy
cards/              <subtype>/<crew>/<slug>.md — frontmatter for machines, prose for humans
tools/              card_io.py (read/write cards) · scoring.py (budget + gates)
                    balance.py · validate.py (CLIs) · studio.py + studio.html (workbench)
art/                characters/<crew>/ and ui/ — referenced by card frontmatter `art:`
legacy/             the original xlsx and docx. Reference only.
```

## Editing card files

Two ways in, and they produce the same result:

- `python tools/studio.py` — the visual workbench. Steppers, live budget meters, live gates,
  cost-neighbour comparison, faction weakness and Lore Packet on screen. Saves in place.
- Edit the markdown directly. `tools/card_io.py` round-trips every card byte-identically, so
  a hand edit and a workbench edit produce identical files.

**Never write a card file by hand from a template** — go through `card_io.render()` or the
workbench, so section order and the Design Notes history stay intact.

## Card file anatomy

Frontmatter is the machine-readable contract — `tools/` parses it. The body is for humans.

```yaml
---
name: Alvino, The Last Call
slug: alvino-the-last-call
card_type: Character
subtype: Ascendant          # or Descendant
faction: Assholes           # Warmongers | Overthinkers | Assholes | Icons
crew: Shea's                # or null, with a reason in Design Notes
cost: 4
stats: {PA: 3, PH: 4, MA: 3, MH: 3}
base:     {keywords: [], effects: [Direct Damage/Heal 1, Status Application (Minor)]}
ascended: {keywords: [], effects: [Counterspell, Soft Removal (Bounce)]}
art: {base: AlvinoTheLastCallv2, ascended: AlvinoTheLastCallv2LVLUP}
status: ported              # draft | ported | reviewed | playtested | final
---
```

Effect and keyword names must match `data/*.yaml` **exactly** — the balance engine errors on
unknown names rather than silently scoring zero. That's deliberate.

Body sections, in order: `# Name` · `## Base Side` · `## Level-Up` · `## Lore` (the Packet) ·
`## Design Notes`.

## The budget engine

```
budget = (cost × 3) + 1 + (3 if Ascendant)
spent  = PA + PH + MA + MH + base keyword points + base effect points
```

Ported verbatim from the original spreadsheet and verified to reproduce its verdict on all 25
costed cards. **Known hole:** the ascended side is charged nothing. See `open-questions.md`
OQ-04 and the `--charge-ascended` flag.

## Known state, so you don't rediscover it

- **31 cards exist. All 31 are Ascendants**, which the rules cap at 5 per 40-card deck. There
  are no Descendants, Tactics, Attachments or Arenas. (OQ-01)
- The **Icons** faction is five nameless stubs. (OQ-06)
- The **Influence** win condition has no printed support. (OQ-02)
- Read `docs/design/open-questions.md` before proposing new work. Thirteen structural issues are
  already catalogued; adding a fourteenth is more useful than re-finding the first.

## Working style

- Push back. If a card is worse than the alternative, say so before building it.
- No filler. Start with the substance.
- When unsure about a rules interaction, check the rulebook rather than reasoning from other
  TCGs. This game's Combat Wave, Blind Commit and Command System are all non-standard.
