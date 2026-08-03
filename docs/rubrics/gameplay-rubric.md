# The Gameplay Rubric

**Purpose.** Decide whether a piece of gameplay is good *before* it is printed, and diagnose
*why* when it isn't. This rubric is opinionated on purpose — a rubric that approves everything
is decoration.

**How it works.** Two stages, always in this order.

1. **Gates.** Pass/fail. A gate failure is not a low score, it is a broken card. You do not
   average your way past a gate. Fix it or cut it.
2. **Dimensions.** Weighted 1–5. These tell you whether a *legal* card is a *good* card.

**Three scopes.** Run the rubric at the scope you're working in.

| Scope | When | Where it lives |
|---|---|---|
| **Card** | Designing or revising a single card | [§1 Gates](#1-card-gates), [§2 Dimensions](#2-card-dimensions) |
| **Mechanic** | A new keyword, status, or subsystem | [§3](#3-mechanic-scope) |
| **System** | Health of the whole game | [§4](#4-system-scope) |

---

## 1. Card Gates

Nine gates. Any failure blocks print. Run `python tools/validate.py <card>` for G1, G3, G4 and
G8 — the rest need a human.

### G1 — Budget compliance

The card's spent points must equal its budget, within tolerance.

```
budget = (cost × 3) + 1 + (3 if Ascendant)
spent  = PA + PH + MA + MH + keyword points + effect points
```

**Tolerance: ±1.** Not zero — zero forces you to pad stats to hit a number, which is how you get
a Character with 1 MA for no reason. Not ±3 — that's 20% of a 3-cost card's entire budget.

**Ascendants must additionally pass the ascended-side check:** run with `--charge-ascended`.
The ascended side may exceed the base budget by at most **+50%**, because levelling up costs
the player real setup work. Exceeding that means the level-up isn't a reward, it's a different
card stapled on.

> Automated: `python tools/balance.py --failing` and `--charge-ascended`.

### G2 — Every term is defined

Every rules term on the card appears in the rulebook or in `data/`. No card may be the first
place a mechanic is defined. If your card needs a new term, the rulebook edit ships in the
**same commit**.

*Currently failing at the system level:* Sacrifice, Hexproof/Untargetable, Spell Shield, Taxing,
Recursion and Arena are all used but undefined. See [`../design/open-questions.md`](../design/open-questions.md).

### G3 — Ability type declared

Every printed ability states its type: `(Standard Ability)`, `(Fast Ability)`, `(Trigger
Ability)` or `(Passive Ability)`. And the declared type must be **capable of what the text
says**:

- A Standard Ability cannot say "in response to."
- A Trigger Ability cannot cost an action.
- A Passive Ability cannot have a one-shot effect.
- Only a Fast Ability may reference the Reaction Window or the Stack.

### G4 — Faction keyword exclusivity

A card carries keywords only from its own faction. No exceptions, including for Ascendants.
Cross-faction power is expressed through **crew**, never through keywords.

### G5 — No unbounded loop

The card cannot produce infinite Energy, damage, cards, or Influence in combination with any
existing card. Pay special attention to **Hustler** (Energy on hit) plus anything that grants
extra attacks or untaps, and to **Recursion** plus any death trigger.

*Test:* write the loop out longhand. If you cannot find a natural stopping point that isn't
"the player chooses to stop," it fails.

### G6 — Deterministic resolution

Two players reading the card reach the same board state. The text must answer, explicitly:

- **Who chooses** the target — you, the opponent, or random?
- **How many** — exact number, not "some."
- **When does it end** — End Step, permanent, until removed, once per Round?
- **What happens on a miss** — no legal target, target already dead, cost unpayable?

Any card applying a status without stating a duration fails this gate automatically.

### G7 — Answerability

At least one **existing** card or rule can interact with this card meaningfully — not merely
"you could also win faster." Removal counts. A Counter counts. Racing does not.

Ask specifically: **can the faction with the fewest tools answer it?** The Warmongers have no
printed Counter and no printed removal that isn't combat. If your card can only be answered by
Blue, you have written a Blue-mandatory card.

### G8 — Art and identity present

`art.base` resolves to a real file, the card has a faction, and if it is a Character it has a
crew or an explicit `crew: null` with a reason in Design Notes. Stub cards (`status: draft`)
are exempt but cannot be playtested.

### G9 — The friendship gate

*This gate exists because the cards are your friends, and it is not a joke gate.*

Losing to this card must feel like being **outplayed or roasted**, not **robbed or insulted**.
A card fails G9 if the loser's most natural reaction at the table is "well, I couldn't do
anything" or "that's actually mean."

Two failure modes, both real:

- **Mechanically robbed.** Turn-1 lock, unanswerable lock, or a card that wins while the
  opponent is not allowed to act. **Pacifier** is a live risk here.
- **Personally stung.** The mechanic encodes a real insecurity rather than a bit. The
  difference: a bit is something they'd tell a stranger at a party. Cross-checked by lore gate
  **L2** — the two gates fail together.

**The test:** would you be happy to *lose* to this card, played by the friend it's named after?

---

## 2. Card Dimensions

Score 1–5. Multiply by weight. Max weighted score **100**.

| # | Dimension | Weight | 1 | 3 | 5 |
|---|---|---:|---|---|---|
| **D1** | **Faction fantasy fidelity** | 5 | Could be recolored to any faction without noticing | Fits the faction's strength | Expresses the faction's strength **and is exposed to its printed weakness** |
| **D2** | **Decision density** | 4 | Plays itself; no choice at any point | One real choice (when to play it) | Creates choices for *both* players, repeatedly, across several Rounds |
| **D3** | **Counterplay texture** | 4 | Answerable only by removal | Two or three answers, all the same kind | Multiple *different-feeling* answers: pre-empt, respond, punish, race |
| **D4** | **Curve fit** | 3 | Cost bears no relation to when you want it | Costed correctly for its slot | Costed so it competes with its neighbours instead of dominating them |
| **D5** | **Combo surface** | 3 | Combos with nothing; a card island | Slots into an existing line | Enables a new deck without enabling a degenerate one |
| **D6** | **Cognitive load** | 3 | Needs a rules argument to resolve | Reads once, resolves cleanly | Reads once, resolves cleanly, **and teaches a rule** |
| **D7** | **Feel of losing** | 3 | "I couldn't do anything" | "I should have played around it" | "That was sick, do it again" |
| **D8** | **Format impact** | 2 | Warps deckbuilding: auto-include or auto-answer | Neutral; a fine card | Opens design space for future cards |
| **D9** | **Table theatre** | 3 | Silent bookkeeping | Fine | Something physically happens — a flip, a reveal, a card crossing the table — that makes the table react |

**Total weight 30. Score = Σ(rating × weight), max 150.**

### Reading the score

| Score | Verdict |
|---|---|
| **120+** | Print it. |
| **95–119** | Print it, flag the lowest dimension in Design Notes, revisit after playtest. |
| **75–94** | Playable but forgettable. Usually **D1 or D2** is the problem — the card is legal and boring. |
| **< 75** | Redesign. Do not tune numbers; the numbers aren't the problem. |

**The dominant-weakness rule:** if any single dimension scores **1**, the card cannot be
printed regardless of total. A 5 in eight dimensions does not redeem "the opponent can't
interact with it."

### Why D1 carries the most weight

The factions each end their rulebook entry with a rhetorical question naming their own
weakness. That's the best design constraint in the whole document and it's currently unused.
A Warmonger card that has *no* exposure to "what happens when fists don't work" is a card
wearing red, not a red card. **D1 = 5 requires the weakness to be present, not just the
strength.**

---

## 3. Mechanic Scope

For a new keyword, status, or subsystem. Gates first.

### Mechanic gates

| Gate | Requirement |
|---|---|
| **MG1** | It has a **priced entry** in `data/keywords.yaml` or `data/effects.yaml`, and the price was derived by comparison to at least two existing entries. |
| **MG2** | It belongs to **exactly one faction** and could not be reassigned without the faction losing something. |
| **MG3** | It is **answerable by every faction**, or its unanswerability is a deliberate, documented faction privilege. |
| **MG4** | It has **at least three cards' worth of design space** — a keyword that supports one card is that card's ability, not a keyword. |
| **MG5** | It does not require a **new zone, new phase, or new timing window.** If it does, it is a rules change, and it goes through §4. |

### Mechanic dimensions

| # | Dimension | Weight | What a 5 looks like |
|---|---|---:|---|
| **M1** | Identity carry | 5 | You could infer the faction from the keyword alone |
| **M2** | Depth-to-complexity ratio | 5 | One sentence of text, many Rounds of implications |
| **M3** | Design space | 4 | Suggests its own next five cards, at different costs |
| **M4** | Interaction with existing keywords | 4 | Creates interesting non-obvious pairings; no dead pairings |
| **M5** | Pricing confidence | 3 | You can defend the point value against three comparables |
| **M6** | Teachability | 3 | A new player gets it from the name plus one example |
| **M7** | Failure mode | 3 | When it's bad it's *dead*, not *frustrating* |

**Max 135.** Below 90, the mechanic is probably a card ability.

---

## 4. System Scope

Run quarterly, or after any set of ~15 new cards. These are the questions that individual cards
cannot answer and that will quietly kill the game if unasked.

### S1 — Win-condition parity

Each of the printed win conditions must be *reachable*. Measure it: what fraction of the pool
advances each one?

- Beatdown: near 100%.
- **Influence: currently ~0%.** Nothing in the pool grants a defined amount of Influence.
- Concession isn't a win condition (see OQ-03).

**Target:** at least 15% of cards meaningfully advance a non-Beatdown condition, or cut the
condition from the rulebook. A printed win condition nobody can pursue is a lie in the box.

### S2 — Faction parity

Not equal winrates — equal *access*. Each faction needs, at some cost, an answer to: a big
body, a wide board, an unanswered Attachment, a Character it cannot target, and an opposing
win condition.

Build the 4×5 grid. Empty cells are your design backlog.

### S3 — Clock

How many Rounds does an average Game take? With 30 Life Points, one Combat Wave per player per
Round, and an economy that ramps at most 3 Energy per Round, do the arithmetic and then check it
against actual play. **There is currently no deck-out loss, so there is no upper bound.** If two
control decks can play forever, S3 fails.

### S4 — Snowball vs comeback

At what point is a Game decided? Identify the losing player's outs. If the honest answer at
Round 4 is "none," you have a snowball problem, and the Blind Commit makes it worse — the
player behind on board is also the player who can least afford to invest cards.

### S5 — Economy tension

The Investment Engine is the game's best mechanic: your hand *is* your fuel, so every card is a
choice between playing it and powering it. Protect this. Any card that generates Energy without
spending a card from hand (Sponsor, Hustler) is eroding the central tension and should be
scarce and expensive.

### S6 — Stat-axis utilization

Half the stat line (MA/MH) currently does almost nothing in standard combat. Either build the
MA game — Troll, Shattered, mental removal, an Overthinker aggro identity — or collapse to two
stats. **Four stats that behave like two-and-a-half is complexity you're paying for and not
using.**

### S7 — Complexity budget

Count: keywords (22), statuses (6), effect types (52), zones (7), phases (3), card types (5+).
That is already a lot for a game played after a few drinks. Every addition should retire
something or earn its slot loudly.

### S8 — Rules/data drift

Zero tolerance. `python tools/validate.py` must exit clean. Every conflict between the rulebook
and a data file is a rules argument waiting to happen at the table.

---

## 5. Using this with AI

When you ask for a card, ask for the rubric output with it. The useful prompt shape:

> Design a 4-cost Overthinker Descendant for the Shea's crew.
> Return: the card, then the G1–G9 gate results, then the D1–D9 scores with one line of
> justification each, then the single lowest dimension and how you'd fix it.

And when reviewing: **make it argue against the card.** "Score this card" produces flattery.
"Find the gate this card fails, and if it truly fails none, find its weakest dimension and make
the strongest case that it shouldn't be printed" produces design notes.

## 6. Changing this rubric

Weights are hypotheses about what makes *this* game good. After every playtest block, ask:
which dimension predicted the cards we actually liked? Raise that weight. Which dimension
scored high on a card that turned out to be boring? That dimension is measuring the wrong
thing. Log changes in [`../design/decisions.md`](../design/decisions.md).
