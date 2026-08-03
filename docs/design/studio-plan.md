# The Studio — Plan

What you asked for is three features. It's actually **one system**, and seeing that changes the
build order.

---

# The realization

Right now you set **Reach** by hand — you look at a card and guess how many factions can answer
it. That guess is the most important number in the balance system and it has nothing behind it.

But look at what you just asked for:

> **(1)** what's unique to a faction and what it never has
> **(2)** each faction's strengths and weaknesses by window
> **(3)** what cards exist across factions and crews

**Those three things are exactly the inputs needed to compute Reach.** A card declares which
windows it's vulnerable in. The faction window map says which factions are strong in those
windows. Cross-reference them and Reach falls out — no guessing, and it updates automatically
when you change either side.

So this isn't a tool that shows you three new screens. It's a tool where **the faction and crew
definitions become real data that the card math reads from.** That's what makes changes
propagate: everything downstream is computed, not typed twice.

---

# Part One — The one architectural change

**Today:** cards, keywords and effects are data. Faction identity, toolkits, window profiles and
crew plans live in **prose documents**.

Prose can't be validated, can't be cross-referenced, and can't drive a calculation. That's the
whole reason things drift.

**The change:** lift factions and crews into data, then **generate the prose from the data.**

```
data/factions.yaml      identity · unique tools · never tools · window profile
data/crews.yaml         plan sentence · lore basis · coordination style · per-card "road"
data/game-states.yaml   controlled vocabulary of board conditions
data/keywords.yaml      (exists)
data/effects.yaml       (exists)
cards/**/*.md           (exists) + requires/produces declarations
        ↓
   validation engine  →  every rule below, one command, one exit code
        ↓
   generated docs     →  rulebook §3, §12, faction pages, crew pages
```

Once faction identity is data, **`docs/rulebook/03-factions.md` becomes generated**, exactly like
§12 already is. You edit one YAML file and the rulebook, the workbench, and the balance math all
move together. That is what "propagate" means in practice.

## The data model

### `data/factions.yaml`

```yaml
- key: warmongers
  name: Warmongers
  color: red
  identity: "To the Warmongers, the world is forged in violence..."
  weakness: "But when a problem cannot be solved with fists..."

  unique:                     # ONLY this faction may have these
    keywords: [Berserker, Combo-Striker, Executioner, Juggernaut, Protector]
    effects:  [Multiple Attacks, Permanent Buff 4, Permanent Buff 5]

  never:                      # this faction may NEVER have these
    effects:  [Counterspell, Searching (Tutors), Hand Destruction 1, Card Draw 1]

  windows:                    # strong | weak | blind
    pre_assembly:    blind
    during_assembly: strong
    on_resolution:   weak
    post_resolution: blind
    race:            strong
```

You said you don't care about declaring what's *shared* — good. **Anything not marked unique to
someone and not on your never list is shared by default.** That's less to maintain and it fails
in the right direction.

### `data/crews.yaml`

```yaml
- key: mobb-134
  name: Mobb 134
  plan: "Accumulate Commandments, then execute all of them at once."
  lore_basis: "They took the chaos of the streets and turned it into law."
  coordination: coordinated        # or: chaotic
  signature: commandments

  expressions:                     # your diversity rule, made checkable
    - card: dre-mastermind-of-the-134
      road: "Builds the engine and pulls the trigger"
    - card: moammar
      road: "Cashes a cleared board into lethal damage"
```

`expressions` is the diversity rule with teeth. **Every card in a crew must state a different
road to the same destination.** If you can't write a distinct road for a card, that card is a
duplicate and the file makes you notice.

`coordination: chaotic` is your exception — a crew whose lore is that they don't coordinate skips
the single-plan requirement, but then has to declare chaos as its plan and be mechanically
chaotic, not just flavored that way.

### `data/game-states.yaml` — the piece that catches Dre and Moammar

A short controlled vocabulary of board conditions:

```yaml
- key: opponent_board_empty
  label: The opponent controls no cards on their Board
- key: opponent_energy_hoarded
  label: The opponent has unused Energy in their Resource Row
```

Then every card declares what it needs and what it makes:

```yaml
# moammar
plan:
  requires: [opponent_board_empty]
# dre
plan:
  produces: [opponent_board_empty]
```

**The tool builds a graph and finds every enabler chain automatically.** Dre → Moammar is one
edge, same crew, flagged. You'd never have to spot that by eye again — and there will be more of
them once Tactics exist.

---

# Part Two — The validation engine

This is the heart of it. One command, everything checked, exit code you can trust.

## Hard errors — these block

| | Rule | What it catches |
|---|---|---|
| **F1** | An effect or keyword is marked unique to **two** factions | Your feature (1). Names both factions in the error |
| **F2** | A card uses something unique to **another** faction | Moammar's tutor; the Assholes' two Counterspells |
| **F3** | A card uses something on its **own** faction's never list | The same problem from the other direction |
| **F4** | A card's Impact exceeds its Ceiling | Existing G1 |
| **F5** | A card claims **Reach 4** but its declared windows aren't ones four factions are strong in | Stops Reach from being wishful |
| **F6** | An ability doesn't declare its type | Existing G3 |
| **F7** | A status is applied with no stated duration | Existing G6 |
| **F8** | Rules text uses a term that exists nowhere in the rulebook or data | Sacrifice, Hexproof, Taxing, Recursion, Arena — all currently undefined |
| **F9** | A card references a crew, faction, art file, effect or keyword that doesn't exist | Typos and renames |

## Warnings — these you read and judge

| | Rule | What it catches |
|---|---|---|
| **W1** | A **window is covered by fewer than two factions** | Your feature (2). Currently W3 and W5 both fail this |
| **W2** | **Enabler chain**: card A produces card B's required state | Dre → Moammar. Same crew = louder warning |
| **W3** | A card has no `road` in its crew's expressions, or two cards share a road | Your diversity requirement |
| **W4** | A card's effect profile doesn't fit its crew's plan | Crew drift |
| **W5** | Two cards anywhere in the pool are functionally near-identical | The twin check |
| **W6** | Card text implies a magnitude larger than any entry in the effect table | **The Moammar mis-logging** — his ascended does +30 and the table stops at 5 |
| **W7** | More than 1 card in 10 sits above 2× base budget | Ceiling quota |
| **W8** | An effect or keyword in the tables that **no card uses and no faction owns** | Dead entries |
| **W9** | A card left `draft` with an empty Lore Packet, or `reviewed` with no True Detail | Lore completeness gates |
| **W10** | A faction has no answer to another faction's signature plan | Faction matchup gaps |

**W6 is worth calling out.** It's the thing that made Moammar read as "over by 5" when he's over
by 30. Any card whose text says *"equal to"* or *"for each"* is scaling, and scaling cards can't
be logged accurately against a table that stops at 5. The linter should catch the phrasing and
make you record a real magnitude.

## Change impact preview

The feature that makes iteration safe. **Before a change saves, show what it breaks.**

```
Marking "Counterspell" unique to Overthinkers will break 2 cards:
   Alvino, The Last Call     (Assholes)  — ascended effect
   Jean H, The Irish Exit    (Overthinkers) — ok, no change

Continue?  [show me]  [cancel]
```

Same for changing a credit value, a window profile, or a crew plan. You never make a change and
find out three weeks later.

---

# Part Three — The views

Card Studio becomes one mode of five.

### 1 · Cards — what exists today, plus
- Reach **computed** from the card's windows × the faction window map, with a manual override
- Live faction-toolkit check as you pick effects — illegal ones greyed out with the reason
- `requires` / `produces` pickers from the state vocabulary
- Compare two cards side by side

### 2 · Factions
- Identity and printed weakness, editable
- **Unique** and **Never** lists, with the conflict validation you asked for
- The **window profile** — strong / weak / blind per window, five toggles
- Roster, and every violation in the faction
- A **budget-share readout**: how much of this faction's total points go to stats vs effects vs
  keywords. Right now the pool is 73% stats — per faction that number is an identity signal

### 3 · Crews
- The plan sentence and its lore basis
- The five cards with their **roads**, and duplicates highlighted
- Faction spread — a crew spanning one faction is a warning
- Coordination style, including the chaotic exception

### 4 · The Matrix — your feature (3)
The crew × faction grid, cards in the cells.

```
                Warmongers   Overthinkers   Assholes   Icons
Latin Kings         2             1            1         0
Mobb 134            2             1            1         0
Shea's              1             1            3         0
Pimp Juice          0             2            3         0
PWNED               1             3            1         0
Fury Park           1             0            0         0
Icons (none)        0             0            0         5     ← all stubs
```

The empty column is the finding. Filter cells by cost, by status, by whether they're over
Ceiling. **This is the view that shows you where to design next.**

### 5 · Health — the game-level dashboard
- **Window coverage** — which windows are thin (W3 and W5 today)
- **Effect ownership** — who owns what, and which tools are contested
- **Cost curve** per faction and per crew — where the holes are
- **Deck feasibility** — can a legal 40-card deck actually be built from this pool? Today: no
- **Win-condition support** — what fraction of cards advance each of the three victories
- **Faction matchup grid** — for each pair, can A answer B's signature plan?

---

# Part Four — Things you didn't name

Ordered by how much I think they'll matter to you.

**① The enabler graph.** Covered above. Automatically finds the Dre/Moammar class of problem.
Nothing else on this list changes the balance math the way this does.

**② Reach computed instead of guessed.** Your features (1) and (2) make this possible. Removes
the softest number in the system.

**③ Change impact preview.** Turns "I'm afraid to change the faction toolkits" into a
two-second check.

**④ The scaling-text linter (W6).** Catches every card whose real power can't be expressed in the
current effect table. There are more than Moammar.

**⑤ Playtest log.** Record a game: who played what, who won, and one line on what felt bad. Tie
entries to cards. Then a card's Design Notes shows its own record, and the Health view can rank
cards by how often they're involved in a game somebody hated. **This is the only thing on this
list that produces information the documents can't.**

**⑥ Status lifecycle gates.** `draft → reviewed → playtested → final`, with requirements to
advance: reviewed needs both rubrics passed, playtested needs three logged games. Right now every
card is `ported` and nothing has been through either rubric.

**⑦ Snapshot diffs.** Tag a state ("before playtest 3"), then diff: what changed, which cards
moved, what broke. Playtest feedback is worthless if you can't remember what version you played.

**⑧ Worklist.** One ranked list: every error, every warning, every empty required field, ordered
by blast radius. The answer to "what do I work on now."

**⑨ Lore↔mechanic traceability.** Each card's *Why This Crew* line, shown next to its effects.
If the lore says one thing and the mechanics do another, you see it in one glance. This is the
thing you said matters most and it's mostly a layout decision.

**⑩ Export back to CS3.** Regenerate the card-image CSV from markdown so your art pipeline stays
connected. You said not now — it goes here when you want it.

---

# Part Five — Build order

Sequenced so each phase is usable on its own and pays for itself before the next starts.

### Phase 1 — Make faction and crew real *(the foundation)*
Create `factions.yaml`, `crews.yaml`, `game-states.yaml`, seeded from the philosophy doc. Add
`requires`/`produces` to cards. Wire F1–F3 and F9. Generate rulebook §3 from data.

*After this: your feature (1) works and the tool tells you Moammar's tutor is illegal.*

### Phase 2 — The consistency engine
The rest of the hard errors, all warnings, the worklist, `python tools/check.py` as one command.

*After this: nothing drifts silently, and you have a ranked list of what's broken.*

### Phase 3 — Faction & Crew views
The two new editor modes. Window profiles become editable. **Reach becomes computed.**

*After this: your feature (2) works and the softest number in the balance system is derived.*

### Phase 4 — Matrix & Health
Your feature (3) plus the game-level dashboard.

*After this: you can see where to design next instead of guessing.*

### Phase 5 — Iteration support
Playtest log, snapshots, change impact preview, status gates.

*After this: the tool helps you learn from playing, not just from designing.*

---

# What I'd push back on

**You have 31 cards and no Descendants.** The whole pool is one card type that the rules cap at 5
per deck. A tool that helps you design cards is only worth as much as the designing it enables,
and right now the highest-value work is still *making a playable pool*.

So: **Phases 1 and 2 pay for themselves immediately**, because they stop you building 60 more
cards on an inconsistent foundation — that's rework you avoid.

**Phases 3 and 4 pay off at scale.** The Matrix view of 31 cards tells you what you already
know. At 150 cards it's indispensable.

**Phase 5 pays off only once you're actually playing.**

My honest recommendation: **build Phases 1 and 2, then go design cards for a while.** Come back
for 3 and 4 when the pool is big enough that you can't hold it in your head — which is roughly
the moment the Matrix view stops being a novelty.

One more thing worth saying: every rule in the validation engine is a rule *you have to be
willing to obey*. A linter you override every time is worse than no linter, because it teaches
you to ignore warnings. Start with the hard errors you actually believe in, and promote warnings
to errors only after they've been right a few times.
