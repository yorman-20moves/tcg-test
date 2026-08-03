# TCG — Working Repository

A 1-on-1 trading card game where the cards are my friends.

**Faction** is *how you fight* — Warmongers, Overthinkers, Assholes, Icons. **Crew** is *what
you're trying to do* — Latin Kings, Mobb 134, Shea's, Pimp Juice, Pwners, Fury Park. They're
independent axes: one crew spans several factions, and that's the point.

---

# Start here

## Running the Studio

Double-click **`Card Studio`** in this folder. A black window opens, then your browser. Leave
the black window open while you work; close it when you're done.

First run takes about a minute while it sets itself up. After that it's about three seconds.

*If it says Python isn't installed:* get it from [python.org/downloads](https://www.python.org/downloads/)
and **tick "Add python.exe to PATH"** during setup.

## The one command that matters

```
python tools/check.py
```

Checks all three levels of the game at once and tells you what's wrong, ranked worst-first. Its
exit code is the number of blocking errors. Everything else in this README is a variation on it.

## The six screens

| Screen | For |
|---|---|
| **Cards** | Designing one card — budget meters, gates, artwork, lore |
| **Factions** | What each faction uniquely owns, never has, and which windows it answers in |
| **Crews** | Each crew's plan, and the different road every card takes to it |
| **Matrix** | Crew × faction grid. Where the holes are |
| **Health** | Window coverage, cost curve, budget share, deck feasibility, playtest log |
| **Problems** | Everything wrong, ranked. Click through to the card |

---

# Scenarios

Everything below is a thing you'll actually want to do.

## I want to design a new card

1. **Cards** screen → **+ New card**. Give it a name (`Name, The Epithet`), faction, crew, type,
   cost. It opens as a draft.
2. **Write the lore first.** Right rail → Lore Packet. Start with **The True Detail** — one real,
   specific, verifiable thing about the actual person. Everything else hangs off it, and it's
   the one field nobody but you can supply.
3. **Set cost and stats.** Watch the big number at the top. Green is good, red is badly off.
4. **Pick keywords and effects.** Only your faction's keywords are offered. If you pick an effect
   another faction owns, `check.py` will tell you.
5. **Write the rules text.** Every ability declares its type: `(Standard Ability)`,
   `(Fast Ability)`, `(Trigger Ability)`, `(Passive Ability)`.
6. **Save**, then run `python tools/check.py --code F4` to confirm the numbers.
7. When both rubrics pass, move the status dropdown from `draft` to `reviewed`.

**Before you start**, open the **Crews** screen and read the crew's plan. A card that doesn't
advance its crew's plan is a card in the wrong crew.

## I want to make a variant of an existing card

**Cards** → select it → **Clone**. Copies cost, stats, keywords, effects, plan, and rules text.

**It deliberately does not copy the lore.** The Lore Packet is about a specific real person and
must never be inherited.

## My card is over budget

The Score panel tells you by how much. Three ways out, and the third is usually the best card:

1. **Make it smaller.** Sometimes right, usually boring.
2. **Make it cost more.** Raising the Energy cost raises the base allowance.
3. **Make it slower, louder and more interruptible.** Declare what it pays — setup, telegraph,
   sacrifice — and which windows the opponent can stop it in. That raises the Ceiling, and it
   almost always makes a better card.

**Watch out for fake costs.** Every cost gets three tests, and most costs fail at least one:

- **Bite** — does paying it make you *worse* at what this card wants to do? If it's on-plan, it's
  not a cost.
- **Timing** — do you pay before the payoff (full credit), at it (half), or after (nothing)?
- **Enabler** — does another card, especially in your own crew, hand it to you free?

## I want to make something genuinely crazy

Read [`docs/design/balance-philosophy.md`](docs/design/balance-philosophy.md) — it's written for
exactly this and teaches the whole system through Moammar, Corazon and Dre.

The short version: **power isn't capped, it's earned.** Build the outrageous version first, then
pay for it in setup, telegraph, sacrifice and interruptibility. A card everyone can answer is
allowed to be three times its base allowance.

**Reach is what caps you.** Not how many windows a card has — how many *factions* can answer it.
A card with five windows that all need a Counterspell has Reach 1, because only the Overthinkers
counter, and it earns nothing for its setup.

## I want to change what a faction can and can't do

**Factions** screen. Click any tool to cycle it:

**shared → unique to this faction → never for this faction → shared**

Tools already unique to someone else are faded, and clicking one tells you who owns it. Saving
regenerates `docs/rulebook/03-factions.md` automatically.

Then run `python tools/check.py --code F2` to see which existing cards you just made illegal.
That list is the point — it's the work the change created.

## I want to change where a faction is strong

**Factions** → Window profile. Click a level to cycle **strong → weak → blind**.

Two things happen. The "covered by" column shows whether that window still has two factions
answering it — fewer than two and it goes amber. And **every card's Reach recomputes**, because
Reach is derived from this map.

## I want to define a crew's plan

**Crews** screen.

1. **The plan** — one sentence: how does this crew win a game?
2. **Lore basis** — why that plan follows from who they are. The lore comes first.
3. **Coordination** — `coordinated`, or `chaotic` for a crew whose whole identity is that they
   don't cooperate. Chaotic crews skip the single-plan rule, but the chaos has to be
   mechanically real, not just flavour.
4. **Roads** — one line per card saying how *that card* advances the plan **differently**.
   Duplicate roads are flagged. If you can't write a distinct road for a card, that card is a
   duplicate and needs rewriting.

## I want to add a keyword or an effect

Edit `data/keywords.yaml` or `data/effects.yaml` directly. Price it against **at least two
existing entries** and say so in `docs/design/decisions.md`.

Then assign it to a faction on the **Factions** screen, or it'll show up as a dead entry (W8).

```
python tools/generate.py     # rebuilds the rulebook keyword table
python tools/check.py
```

## I want to rename something

**Never rename by hand.** A card keeps the old name, the balance engine scores it as zero, and
nothing tells you.

```
python tools/rename.py --dry-run effect "Permanent Buff 5" "Permanent Buff 5+"
python tools/rename.py effect "Permanent Buff 5" "Permanent Buff 5+"
python tools/generate.py && python tools/check.py
```

Works on `keyword`, `effect`, `crew`, `faction`, `state`, `status`. Updates every reference in
data, cards and docs at once.

## I want to retire a card

Set its status to **`retired`** in the dropdown. It stays on disk and in git history, stops
being validated, and drops out of the Matrix and Health counts.

Don't delete card files. The Design Notes are a record of why the card was what it was.

## I want to change a rule in the rulebook

Edit the section in [`docs/rulebook/`](docs/rulebook/README.md) — **except these three, which
are generated and will be overwritten:**

- `03-factions.md` ← `data/factions.yaml`
- `12-keywords.md` ← `data/keywords.yaml`
- `docs/design/crews.md` ← `data/crews.yaml`

If a card depends on the rule you're changing, update the card in the same commit. Run
`python tools/check.py` to find the dependents.

**Adding a new rules term?** It goes in the glossary in the same change, or every card using it
fails gate F8.

## I want to add a whole new card type

Descendants, Tactics, Attachments and Arenas all work today — pick the type in the New card
dialog. They land in `cards/<type>/<crew>/`.

**Arenas have no rules yet** (OQ-07). Write them before designing one.

## I just played a game

**Health** → Playtest log. Record when, who, who won, which cards were involved, and — most
importantly — **what felt bad**.

That last field is the only information in this entire system that the documents cannot produce.
A card that keeps showing up in "felt bad" is a card with a problem no amount of arithmetic will
reveal.

Playtests mentioning a card appear on that card's page automatically.

## I want to know what changed between playtests

Before you play: **Health** → Snapshots → name it (`before playtest 3`) → **Take snapshot**.

It records every card's cost, stats, impact, ceiling and reach. Playtest feedback is worthless
if you can't remember which version you played.

## I don't know what to work on

```
python tools/check.py --next 5     # the five most important problems
python tools/check.py --gaps       # what's MISSING, not what's wrong
```

`--gaps` is the one for "what should I design next." It tells you which card types you're short
of for a legal deck, which factions have no playable cards, which crews are thin, which board
conditions no card touches, and whether your printed win conditions have any support.

## I want to check everything before committing

```
python tools/generate.py --check   # are the generated docs stale?
python tools/check.py              # all three levels
```

## Something broke and I want to undo it

Everything is in git.

```
git diff                                    # what have I changed?
git checkout -- cards/path/to/card.md       # undo one file
git log --oneline -- cards/path/to/card.md  # a card's whole history
```

The Studio writes surgical diffs — change a stat and only that line changes — so `git diff` is
genuinely readable.

## I want to work on this with an AI

Point it at [`AGENTS.md`](AGENTS.md). That's the working contract: source-of-truth precedence,
the hard rules, the gate and rule codes, and the two things it must never invent (a rules term,
and a Lore Packet True Detail).

Ask for the rubric output with every proposal, and ask it to argue *against* the card. "Score
this" produces flattery; "find the gate this fails, and if it truly fails none, make the
strongest case it shouldn't be printed" produces design notes.

---

# Reference

## Commands

```bash
python tools/check.py                  # everything, ranked worst-first
python tools/check.py --next 5         # the five things to fix now
python tools/check.py --gaps           # what's missing
python tools/check.py --errors         # only what blocks
python tools/check.py --code F2        # one rule
python tools/check.py --json           # machine-readable

python tools/studio.py                 # the Studio (or double-click Card Studio)
python tools/generate.py [--check]     # rebuild the docs derived from data/
python tools/rename.py KIND OLD NEW    # safe rename everywhere
python tools/balance.py [--failing]    # just the budgets
python tools/validate.py               # just the card gates
```

## Where things live

```
Card Studio.bat        double-click to run
data/                  THE SOURCE OF TRUTH
  factions.yaml          identity, unique/never toolkits, window profiles
  crews.yaml             plans, lore basis, coordination, per-card roads
  game-states.yaml       board-condition vocabulary (drives enabler detection)
  keywords.yaml          faction-exclusive Roles + point costs
  effects.yaml           effect types + point costs
  plan-credits.yaml      the Score: credit values, reach caps, cost tests
  status-effects.yaml
cards/<type>/<crew>/   one markdown file per card
docs/rulebook/         the rules, 13 sections
docs/rubrics/          the gameplay and lore rubrics
docs/design/           balance philosophy · open questions · decisions · canon · studio plan
tools/                 card_io → scoring → rules → the CLIs and the Studio
art/                   character and UI artwork
legacy/                the original xlsx + docx, reference only
playtests.yaml         the playtest log
```

## Rule codes

**Hard errors — these block.**

| | |
|---|---|
| **F1** | A tool is marked unique to two factions |
| **F2** | A card uses a tool unique to another faction |
| **F3** | A card uses something on its own faction's never list |
| **F4** | A card's Impact exceeds its Ceiling |
| **F5** | A card claims more Reach than its windows deliver |
| **F6** | An ability doesn't declare its type |
| **F7** | A status is applied with no stated duration |
| **F8** | Rules text uses a term defined nowhere |
| **F9** | A reference points at something that doesn't exist |

**Warnings — read and judge.**

| | |
|---|---|
| **W1** | A window is covered by fewer than two factions |
| **W2** | **Enabler chain** — one card produces what another requires |
| **W3** | Two cards in a crew take the same road, or a card has none |
| **W4** | A crew has no plan, or a plan/toolkit nobody has reviewed |
| **W5** | Two cards are functionally identical |
| **W6** | Card text scales but is logged as a small fixed number |
| **W7** | Too many cards above 2× base budget |
| **W8** | A keyword or effect nobody uses and no faction owns |
| **W9** | A card past draft with an empty Lore Packet |
| **W10** | A faction is blind everywhere another is strong |
| **GAP** | Something missing rather than wrong |

## Vocabulary

| | |
|---|---|
| **Impact** | What a card actually does — its power level |
| **Allowance** | Base budget + credits. What it has *earned* |
| **Credit** | One point of **permission**, bought with something other than Energy. Not power |
| **Reach** | How many factions can answer this card. Caps the Allowance |
| **Ceiling** | The smaller of Allowance and the Reach cap |
| **Window** | One of five moments a plan can be stopped (W1–W5) |
| **Road** | How one card advances its crew's plan differently from the others |

---

# Where the game actually stands

Run `python tools/check.py` for the live numbers. As of the last pass:

| | |
|---|---|
| Cards designed | **31** — all Ascendants |
| Legal deck coverage | Short 24 Descendants, 8 Tactics, 3 Attachments |
| Factions with playable cards | **3 of 4** — the Icons are five stubs |
| Win conditions with printed support | **1 of 3** |
| Blocking errors | ~39 |
| Faction toolkits & crew plans | **drafts, unreviewed** |

Three things gate everything else, in order:

1. **Review the faction toolkits and crew plans.** They're my drafts and every other rule
   validates against them. Factions and Crews screens, then tick "reviewed".
2. **Design a real card pool.** Roughly 24 Descendants, 8 Tactics, 3 Attachments. The game has
   never been playable and every balance judgment so far was made against an imaginary format.
3. **Decide what the Icons are.** They own the only unsupported win condition, have zero playable
   cards, and already have finished artwork. One decision unblocks a faction and a victory.

Full list: [`docs/design/open-questions.md`](docs/design/open-questions.md).
