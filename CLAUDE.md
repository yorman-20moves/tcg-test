# AGENTS.md / CLAUDE.md — working on this project

Read this before touching anything. It is the contract, not an overview.

**This file exists twice.** `AGENTS.md` and `CLAUDE.md` are one document under two names —
agents disagree about which filename to read, and `README.md` sends human collaborators to
`AGENTS.md`. They must stay **byte-identical**: edit one, copy it over the other in the same
change. `python tools/check.py` blocks on any difference (rule **F13**). If they have already
drifted and it is not obvious which side is newer, **`CLAUDE.md` is canonical** — that is the
one an agent auto-loads, so it is where edits land.

## What this is

**Known Associates** — a 1-on-1 trading card game where the cards are the designer's real
friends, organized into four **factions** (methodology) and six **crews** (loyalty). The founding
edition is **Known Associates: Local Legends** (D-014). Two things have to be excellent:
the **gameplay** and the **lore**. Both have rubrics. Use them.

**The name is used flat.** Applying police-file language to a friend group is the joke; nothing
printed may acknowledge that it is one. The register never winks — see `docs/design/canon.md`.

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
5. **Run the tools before claiming anything is finished.**
   ```
   python tools/check.py                  # EVERYTHING -- one command, one exit code
   python tools/check.py --next 5         # the five things to fix now
   python tools/generate.py               # regenerate the docs derived from data/
   python tools/studio.py                 # the workbench: Cards Factions Crews Matrix Health Problems
   python tools/balance.py --failing      # just the budgets
   ```
   `check.py` is the one that matters. It validates all three levels at once and its exit code
   is the number of blocking errors.
6. **Generated content must never be hand-edited.** Edit the source, then run
   `python tools/generate.py`. `generate.py --check` fails if anything is stale.

   | Generated | From |
   |---|---|
   | `docs/rulebook/03-factions.md` — whole file | `data/factions.yaml` |
   | `docs/rulebook/12-keywords.md` — whole file | `data/keywords.yaml` |
   | `docs/design/crews.md` — whole file | `data/crews.yaml` |
   | `docs/rulebook/06-character-anatomy.md` — the ability-types table only | `data/ability-types.yaml` |
   | **every card's `### Rules Text` and `### Ascended Rules Text`** | that card's `abilities:` frontmatter |
   | **`AGENTS.md` — whole file** | **`CLAUDE.md`** (this file) |

   **This document is that last row.** It exists under two names because agents disagree about
   which filename to read and `README.md` sends humans to `AGENTS.md`. **`CLAUDE.md` is
   canonical; `AGENTS.md` is a byte-identical generated mirror.** Edit this file, run
   `generate.py`, and never edit `AGENTS.md`. Keeping both by hand is exactly how they drifted
   (D-016).

   **`check.py` enforces all of it** — rule **F14** blocks on any stale generated file, stale
   region, or card body that no longer matches its frontmatter, and **F13** blocks on the two
   contract copies disagreeing. You do not have to remember to run `generate.py --check`
   separately; the one command covers it.

   That last row is the one that changes how you work. **An ability is data.** It lives in
   frontmatter as a record with `name`, `type`, `immersion`, `mechanics` and optional `requires`
   and `role`; the printed prose is built from it by `card_io.print_ability()`. Editing the Rules
   Text section of a card by hand is no longer legal — the next `generate.py` overwrites it. Edit
   the frontmatter, or use the Studio's ability editor. Gate G3 reads the `type` field, so a card
   can no longer fail it because a regex could not parse a sentence.

   The delimited region in `06-character-anatomy.md` is marked with
   `<!-- GENERATED:ability-types ... -->` / `<!-- /GENERATED:ability-types -->`. Prose outside
   those markers is hand-written and stays that way.

Faction identity, toolkits and window profiles live in `data/factions.yaml`. Crew plans live in
`data/crews.yaml`. Board conditions live in `data/game-states.yaml`, and every card declares
`plan.requires` / `plan.produces` against that vocabulary so `check.py` can find enabler chains
automatically — that is how Dre feeding Moammar was caught.

## Jobs and Formations

**A Job is not a keyword.** A Job is the position a Character plays for its crew; a keyword
is one of the tools it plays it with. Two Wardens in different factions do the same job with
different tools. See D-015 for the vocabulary decision behind those two words.

- `data/jobs.yaml` — 28 Jobs in four families (front · damage · support · specialist). Every
  Character declares one in frontmatter as `job: <key>`. Each Job carries a `signature`
  (guidance, not law), a `factions` allow-list (null = any), and `status: built | unbuilt`.
- `data/formations.yaml` — 8 Formations. A crew declares one; it names **four required Jobs and
  one free slot**. **No crew has one assigned yet** — lore leads, the plan follows the lore, the
  Formation follows the plan. Do not assign them by reading off existing cards.
- **`Every Man For Himself` is not an exemption**, it is a different rule: no card may require a
  state a crewmate produces (F12), and no card may reference or buff its own crew. In exchange
  those cards get a higher individual rate. **No crew is chaotic yet** — that crew is still to be
  designed.
- Rules: F11 legality (error) · F12 chaotic enablers (error) · W12 signature fit · W13 Formation
  coverage · W14 Job duplication · W15 undeclared. Plus GAP reporting of unfilled Jobs.

Read [`docs/design/jobs-and-formations.md`](docs/design/jobs-and-formations.md) before touching
any of it.

7. **Append to `## Design Notes`, don't overwrite.** The history of why a card changed is worth
   more than the current state.
8. **Lore gate L2 (the dignity line) is not negotiable and not a joke gate.** These are real
   people. When in doubt, the answer is "ask them," not "it's probably fine."

## Keywords, effects and statuses

They live in `data/keywords.yaml`, `data/effects.yaml`, `data/status-effects.yaml` and are
edited on the Studio's **Library** screen, which also shows ownership and per-card usage.

Pricing a new entry means defending it against **at least two existing entries** and recording
the reasoning in `docs/design/decisions.md`. Keywords are faction-exclusive: a keyword's own
`faction` field and the owning faction's `unique` list must agree, or F10 fails.

## Creating, cloning, retiring

Never hand-write a card file from a template — go through `card_io.new_card()` or the Studio's
**+ New card**, so the frontmatter schema and section order are guaranteed. Clone copies
mechanics but never lore. Retire with `status: retired` rather than deleting; the Design Notes
are the record of why the card was what it was.

Never rename a keyword, effect, crew or faction by hand — use `python tools/rename.py`. A hand
rename leaves cards pointing at the old name, the engine scores them as zero, and nothing warns.

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

## The balance system — The Score

**Read [`docs/design/balance-philosophy.md`](docs/design/balance-philosophy.md) before pricing
anything.** It is the reasoning; this is the summary.

```
Base Budget = (cost × 3) + 1 + (3 if Ascendant)        [the original spreadsheet formula]
Earned      = Base Budget + credits paid in non-Energy currencies
Ceiling     = Earned × (1 + 0.25 × interaction windows)
```

**Power is not capped, it is earned.** A card pays in setup, telegraph, sacrifice, cards, life,
and matchup narrowness (`data/plan-credits.yaml`), and it earns a multiplier for every real
window where the opponent can stop it. Counterplay is the *engine* of power here, not a
restriction on it — the more chances you give the opponent, the bigger you are allowed to be.

A card that declares no plan has Ceiling = Base Budget, i.e. exactly the old rule. Every existing
card is unaffected.

**Four prohibitions no Ceiling buys past:** P1 no self-restarting payoff · P2 no passive lock ·
P3 no unbounded repetition · P4 no cheap + wide + uninterruptible.

**Ceiling discipline:** at most one card in ten, and one per crew, above 2× base budget.

Declare a plan in frontmatter:

```yaml
plan:
  pays: {characters_required: 3, telegraph_rounds: 2, characters_consumed: 3}
  windows: [pre_assembly, during_assembly, on_resolution, orthogonal]
```

Each claimed window must name **a specific existing card or rule** that exercises it. "Someone
could theoretically remove it" is not a window.

## Known state, so you don't rediscover it

- **31 cards exist. All 31 are Ascendants**, which the rules cap at 5 per 40-card deck. There
  are no Descendants, Tactics, Attachments or Arenas. (OQ-01)
- **Six mechanics were built on 2026-08-05 and no card uses them yet**: `Range 2`/`Range 3`
  (Aiming, Overthinkers), `Collector` (taxation, Assholes), `Breaker` (anti-PH, Warmongers),
  `Additional Action` (Assholes), `Token Generation 1/2/3`, `Arena Rule Edit (Minor|Major)`.
  The rules for all of them are written; the cards are not. See D-007 and D-008.
- **The rules layer moves before the pricing layer, always.** A rulebook change invalidates card
  tuning; a card never invalidates the rulebook. Do not tune cards while a mechanic is still
  being designed — that is how you end up re-playtesting everything.
- The **Icons** faction is five nameless stubs. (OQ-06) **Icons are deliberately outside the
  system.** They are not a crew, they have no Formation, and they are not required to be
  internally consistent — each one is a rule-breaker and a one-person army. They represent the
  designers' mothers, and the reverence is the point. **They are being designed last.** Do not
  use Icons as the home for a mechanic the rest of the game needs, do not fold them into crew
  or Formation validation, and do not treat Influence as a live win condition on their account.
- The **Influence** win condition has no printed support. (OQ-02)
- Read `docs/design/open-questions.md` before proposing new work. Fifteen structural issues are
  already catalogued; adding a sixteenth is more useful than re-finding the first.
- **Phase 2's alternating actions are the game's best structural asset** — a five-step plan
  automatically hands the opponent four interaction windows. Protect that. Trigger and Passive
  abilities bypass it, which is why P3 exists.

## Working style

- Push back. If a card is worse than the alternative, say so before building it.
- No filler. Start with the substance.
- When unsure about a rules interaction, check the rulebook rather than reasoning from other
  TCGs. This game's Combat Wave, Blind Commit and Command System are all non-standard.
