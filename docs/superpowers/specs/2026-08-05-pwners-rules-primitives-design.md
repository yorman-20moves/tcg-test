# Pwners Rules Primitives — design

**Date:** 2026-08-05 · **Branch:** `studio-legibility` · **Status:** approved, not yet implemented

## Why

Three Pwners cards — Caleb, Julito and Ruvi — carry abilities that assume rules the game does not
have. They were ported from the spreadsheet with their text intact, and the text quietly invents a
randomiser, a counter system, a reverse Ascendant flip, and a status that no card effect can
remove.

`check.py` sees only the shallowest layer of this. It reports Caleb's `[Bricked]` three times as
"declares no ability type" — a prose-parser artifact already diagnosed in
[`2026-08-05-structured-abilities-design.md`](2026-08-05-structured-abilities-design.md). The real
defect is that **Bricked is not a status.** `data/status-effects.yaml` holds six and that is not
one of them.

Measured across the three cards, against `docs/rulebook/` and `data/`:

| Class | Count | Examples |
|---|---:|---|
| Terms used that the rulebook never defines | 6 | d6 roll, "EX Meter token", "personally witnessed", "Level 1 / Level 2", flip-back, `[Bricked]` |
| Statuses applied with no stated duration (auto-fail **G6**) | 3 | all three Teabag outcomes |
| Abilities with no printed rate limit | 2 | `[The Item Box]`, `[Teabag]` |
| Frontmatter that prices something the text never grants | 1 | Julito's `Multiple Attacks` |
| Pieces prohibited outright by **P2** | 2 | Ruvi's global Silence, Caleb's unremovable status |
| Pieces that bypass a structural guarantee | 1 | `[The Glitch]` bypasses the Reaction Window |

**No new ability type is needed.** Standard / Fast / Trigger / Passive covers all nine abilities on
the three cards. Everything missing sits in a layer *below* ability types.

### The two collisions worth naming up front

**"Token" is already taken.** Julito's `[Build Meter]` accumulates "EX Meter tokens."
[§5 Card Types](../../rulebook/05-card-types.md#token) defines a Token as *a Character created by
an effect rather than played from a zone*, and adds that a Token is "a Character for every rule."
Julito's text therefore reads, literally, as creating up to three Characters.

**Ruvi's global Silence is Pacifier.** `[You Know This Is Just A Game, Right?]` is a continuous
Passive, so Cleanse (Minor) and Cleanse (Major) can never answer it — the Passive re-applies. Only
removal answers it, which puts D3 at 1 and trips the rubric's dominant-weakness rule regardless of
total score. That is the identical reasoning by which
[OQ-09](../../design/open-questions.md) already ruled Pacifier
prohibited under **P2**.

## Decisions taken

| # | Decision | Rejected alternative |
|---|---|---|
| 1 | Build four rules primitives: **Randomization, Counters, Descent, Trigger discipline** | Build only Randomization + Counters and drop Julito's flip-back — cheapest, but forfeits the one idea in the three cards that gives OQ-04 a pricing lever |
| 2 | A random effect is priced at its **most expensive outcome**; a bad outcome earns **no credit** | Price at expected value — makes variance a discount and the highest-variance card the most efficient card |
| 3 | **Bricked is flavour, not a status.** Print Stunned + Silenced | A 7th status; two existing statuses stapled together does not clear **S7** |
| 4 | Caleb's reboot moves to the **End Step**, not the opponent's Phase 2 action | Add a "Recover" action to §8 — a fifth primitive, and the action cost was the P2 violation |
| 5 | Warmonger "no non-combat removal" **holds**; Shun Goku Satsu becomes combat-gated | Print the Fast Murder as a documented one-card exception — weakens the constraint OQ-09 and G7 both cite |
| 6 | Ruvi's Silence becomes an **activation** (option a) | (b) continuous with printed upkeep — per-Round bookkeeping, and "Ruvi Silences himself" is a strange failure state. (c) reframe as a punish on ability use — better card by the rubric, but a different card |
| 7 | `[The Glitch]` keeps the Reaction Window open; only the **damage** is unpreventable | Let it bypass the window as printed — CLAUDE.md names the alternating-action window as the game's best structural asset |
| 8 | `[The Glitch]` deals Ruvi's **MA**, not his PA | Leave it at PA — his PA is 1 and there is no ascended stat block, so the ability that breaks the game's most sacred rule deals 1 damage |
| 9 | Julito **cost 4 → 5** | Cut 4 points of stats or drop Combo-Striker from the base side — both lose a tier of the card |

## 1. Randomization

New file `docs/rulebook/14-randomization.md`, plus glossary entries in §13.

Two cards need it, and `data/crews.yaml` names randomness as the Pwners' crew signature — so this
is a subsystem the design already committed to and never wrote. **G6 already lists "random" as a
legal answer to "who chooses the target,"** so the rubric anticipated this gap rather than
forbidding it.

```
The Roll
- Some abilities instruct a player to roll a six-sided die (d6).
- The controller of the ability rolls, unless the ability says otherwise.
- The die is rolled where both players can see it. The result is public.
- The roll happens inside the ability's resolution. Neither player may respond between the
  die coming to rest and its effect applying. A roll is a telegraph, not an interaction window.
- An ability that rolls on the Stack rolls when it RESOLVES, not when it is declared.
- Once a die comes to rest its result cannot be re-rolled, modified or replaced unless a card
  explicitly says so. No card currently says so.
- An ability that names an outcome for some results must name an outcome for EVERY result
  1 through 6, or it fails gate G6.
```

The last clause is deliberately gate-shaped. Both existing d6 abilities already satisfy it —
Caleb covers 1-3 / 4-5 / 6, Ruvi covers 1-2 / 3-4 / 5 / 6.

### Pricing rule (goes in `docs/design/balance-philosophy.md`)

> **A random effect is priced at its most expensive outcome. A bad outcome earns no credit.**

Variance is a choice the controller makes, not a cost the card pays. Two comparables, as **MG1**
requires:

- `data/effects.yaml` has never priced by frequency. `Direct Damage/Heal 4` costs 4 whether or not
  you ever draw the card.
- **Range 3** charges 4 points for the ×3 shot, not the average of aiming zero, one or two Rounds.
  The existing file already prices a variable outcome at its ceiling.

The mirror clause matters as much as the rule: Ruvi's Banana Peel branch (1 permanent MH damage to
himself) earns **no** plan credit. Crediting a one-in-three downside while charging the best upside
would price the same variance twice, in opposite directions. This also means no new
`self_damage` credit entry is required — one fewer addition.

## 2. Counters

Glossary entry in §13, plus a paragraph in §6.

```
Counter — a physical marker placed on a Character by a card effect.
- Every counter is NAMED by the effect that creates it. Counters of different names never
  interact.
- A counter has no inherent effect. It does something only because a card's text reads it.
- Counters are public information. Either player may count them at any time.
- Counters are removed when the Character leaves the Board, and do not carry to a new copy.
- Counters SURVIVE an Ascendant's flip, in both directions, unless the card says otherwise.
- A card that creates counters must print a maximum, or it fails gate G6.
```

This addition **retires a special case rather than adding one**, which is the only kind of
addition **S7** likes. Aim becomes an instance of the primitive and
[§9 Aiming](../../rulebook/09-combat-and-stack.md#aiming-the-range-keyword) needs no edit — its
text already says "Aim counter" and already prints a maximum of N−1.

The flip-survival clause is load-bearing for Julito: he ascends *because* he holds 3 EX counters,
then spends them from the ascended side.

## 3. Descent

Addition to [§10 Ascendants](../../rulebook/10-ascendants.md).

```
Descent
An ability may instruct an Ascendant to Descend: flip it back to its base side.

- Only a card's OWN text may cause it to Descend. No effect may force an opponent's Ascendant
  to Descend.
- Permanent PH/MH damage carries across the flip. If carried damage meets or exceeds the base
  side's printed Health, the Character is set to 1 and is NOT Murdered — the Safety Net covers
  Descent, because a flip is not active damage.
- Statuses and counters persist.
- Buffs printed on the ascended side are lost. Buffs applied by other cards remain.
- The Level-Up condition becomes live again. A Descended Ascendant may re-ascend. Descent is
  not once per Game unless the card says so.
```

The opponent-immunity clause closes a door that would otherwise open wide: a forced Descent is
removal that invalidates every level-up in the game, at a fraction of Hard Removal's price.

**Why this earns its slot despite serving one card.** **MG4** wants three cards' worth of design
space and Descent has one. It ships anyway because it is a direct lever on
[OQ-04](../../design/open-questions.md), the largest known hole in
the balance system: the ascended side is free because nothing can ever take it away. An ascended
side that can be *spent* is an ascended side with a price. Descent is the first mechanism in the
game that makes OQ-04's second face cost something.

### New credit: `data/plan-credits.yaml`

```yaml
  - key: ascension_spent
    label: Gives up its own ascended side (Descends)
    points: 4
    anchor: cheaper than consuming a Character (5) -- you keep the body; same shape as
            board_state_required (4) -- you have to engineer the state again
    sentence: Because it gives up its own ascended side
```

Two comparables per **MG1**: below `characters_consumed` (5), because you keep the body and may
re-ascend; equal to `board_state_required` (4), because that is exactly what you are re-engineering.

Applied to Julito, the credit runs through `cost_tests` as: `bite: competes` (1.0 — losing his
ascended side plainly makes him worse at his job), `timing: at_payoff` (0.5 — he pays as it lands),
`enabler: none` (1.0). Weakest test wins, so **4 × 0.5 = 2 points of Earned**.

## 4. Trigger discipline

Addition to [§6 Character Anatomy](../../rulebook/06-character-anatomy.md).

```
- A Trigger Ability may name a COST. If it does, its controller chooses whether to pay when the
  trigger fires; declining means the ability does not resolve. Paying a cost never costs an action.
- A Trigger Ability fires once per OCCURRENCE of its condition. If the condition occurs several
  times at once, it fires that many times and its controller chooses the order.
- A Trigger Ability with an unbounded firing rate and a cumulative effect fails gate G6 unless it
  prints a rate limit.
```

§6 currently says a Trigger "fires **automatically** the moment its condition is met," which
contradicts Caleb's "pay 1 Energy to roll." The first clause resolves that.

**This does not solve OQ-15.** Whether a chain of triggers deserves a response window is a
separate and much larger question, and it stays open. What ships here is only the firing-count
rule, optional costs, and the requirement that cumulative triggers print a cap.

## 5. The three cards

### Caleb — Assholes · Pwners · cost 3 · PA 2 / PH 3 / MA 2 / MH 2

```
[Teabag] (Trigger Ability): Caleb dances on their bodies and ruins their game.
Once per Round, when an enemy Character is Murdered, you may pay 1 Energy to roll a d6
and target an enemy Character. Until the End Step, that Character is:
1-3: Exhausted.   4-5: Silenced.   6: Stunned.
```

**Level-Up condition.** Place a Salt counter on Caleb whenever an enemy Character is Murdered
while afflicted with Exhausted, Silenced or Stunned, while Caleb is face-up on the Board
(maximum 3). At 3 Salt counters, he levels up.

```
[Red Ring of Death] (Standard Ability): Caleb bricks their system and traps them offline.
Once per Round, pay 2 Energy to inflict Stunned and Silenced on an enemy Character. Both
persist until removed. At each End Step, that Character's controller may pay 1 Energy and
roll a d6: on 4-6 both are removed, on 1-3 they remain.
```

Five edits, each closing a named failure:

| Was | Now | Closes |
|---|---|---|
| No rate limit on `[Teabag]` | `Once per Round` | Mass removal fired it once per body |
| `pay 1 Energy` on an automatic trigger | `you may pay` | §6 contradiction |
| `Inflict Exhausted` | `Until the End Step` | **G6** auto-fail, no duration |
| "personally witnessed 3 Characters die" | Salt counters, max 3, "face-up on the Board" | Two undefined terms; "die" → **Murdered** |
| `[Bricked]` + "cannot be removed by card effects" | Stunned + Silenced, End Step reboot roll | **P2**; and Cleanse works again |

**Why the reboot moved to the End Step.** As printed, application cost Caleb 2 Energy and one
action; removal cost the opponent 1 Energy and, at 50% per attempt, **two actions on average**.
Application beat removal on rate, which is what made it a lock rather than a tempo hit. At the End
Step the roll is outside the action economy and fires every Round. The humiliating coin flip — the
thing worth keeping — survives untouched.

**Blocker: Caleb cannot ship until [OQ-08](../../design/open-questions.md)
is resolved.** Half of `[Teabag]`'s outcomes apply Exhausted, and Exhausted has two contradictory
definitions. Note which way helps him: the Elements definition (attack power halved) makes
afflicted Characters lose fights and die afflicted, which is exactly what feeds Salt counters. The
rulebook definition (+1 Energy attacker tax) does nothing for him. That is a design argument for
resolving OQ-08 **against** the current authority — worth recording either way, since the rulebook
currently wins by default rather than by decision.

### Julito — Warmongers · Pwners · **cost 5** · PA 4 / PH 4 / MA 1 / MH 3

```
[Build Meter] (Trigger Ability): Julito lives for a bloody, unbroken combo.
Whenever Julito Murders an enemy Character, or deals damage to the opponent's Life Points,
place an EX counter on him (maximum 3).

[The EX Enhancements] (Passive Ability):
While Julito has 1 or more EX counters: +2 PA and +2 PH.
While Julito has 2 or more EX counters: he gains (Combo-Striker).
```

**Level-Up condition.** When Julito has 3 EX counters, he levels up.

```
[Demonic Ascension] (Passive Ability): Julito is drunk with the power of the dark Hadou.
While Julito has 3 EX counters, he gains (Berserker).

[Shun Goku Satsu] (Trigger Ability): Julito delivers a thousand fatal strikes in the blink
of an eye. When Julito clashes with a Character in a Combat Wave, you may pay 1 Energy and
spend all 3 EX counters. If you do, he Murders that Character outright, bypassing the
standard math. Julito then Descends.
```

Both original tiers are preserved exactly — "Level 1" and "Level 2" were never *wrong*, they were
never **keyed to a number**, which is what made them unresolvable under G6.

One silent correction, flagged because it is not a typo fix in a vacuum: `[Demonic Ascension]`
currently reads *"**Julio** is drunk with the power of the dark Hadou."* There is a different card
named **Julio, the Tyrant of the Tainted Touch** in Mobb 134, so on Julito's own card that word
reads as a reference to someone else. Corrected to "Julito."

**Shun Goku Satsu resolves in Step 4**, the slot
[§9](../../rulebook/09-combat-and-stack.md#step-4--simultaneous-resolution) already documents for
"Executioner mechanics and other damage replacements." No new timing rule. He still takes the clash
damage, which now matters — Descent carries it, and the Safety Net catches him at 1.

Three windows, each naming a specific rule or card as `plan-credits.yaml` requires:

- **W1 pre-assembly** — kill him before he reaches 3 EX counters.
- **W2 during assembly** — **Silence** him; Silenced blanks printed abilities, which turns off
  both the Passive and the Trigger and freezes the meter.
- **W3 on resolution** — Protector intercept, or a Combat Tactic, in Step 2 of the Combat Wave.

**Two pricing corrections, both findings rather than nerfs:**

1. `Multiple Attacks` (5) is charged in frontmatter for something the card text never grants.
   **Combo-Striker already *is*** "attacks resolve in two strikes." Removing it corrects a
   double-charge; the printed card is unchanged.
2. `+2 PA and +2 PH` is two stat axes priced as one `Permanent Buff 2`. It is two.

**Why the cost bump, and why he cannot credit his way out.** `cost_tests.bite` rates a cost that
**is** the plan at 0.0. A Warmonger accumulating counters by winning fights is doing his job, not
paying a price — so his meter earns him nothing, correctly. Verified with the real scorer: at cost
4 the corrected card is base 20/16 and both faces 27/24, failing both checks. At cost 5 it is base
20/19 (inside the ±1 tolerance) and both faces 27/28. One number moves and no tier is lost.

### Ruvi — Overthinkers · Pwners · cost 5 · PA 1 / PH 3 / MA 5 / MH 4

```
[The Item Box] (Fast Ability): Ruvi is bored and wants to see if pure RNG can carry him.
Once per Round, pay 1 Energy and roll a d6:
1-2 (Banana Peel): Ruvi takes 1 permanent Mental Health (MH) damage.
3-4 (Green Shell): Ruvi deals 2 physical damage to a target enemy Character.
5 (Mushroom): Ruvi permanently gains +2 PH and +2 MH.
6 (The Blue Shell): Ruvi deals 4 mental damage to a target enemy Character.
```

**Level-Up condition.** When Ruvi rolls a 6 on `[The Item Box]`, he levels up.

```
[You Know This Is Just A Game, Right?] (Standard Ability): Ruvi uses a GameShark to hack
the system. Once per Round, pay 2 Energy: until the End Step, every other Character on the
Board — allied and enemy — is Silenced.

[The Glitch] (Fast Ability): Ruvi has realized he is just a card.
Once per Game, when you declare a Combat Wave in which Ruvi is an attacker, you may say
"it's just a game" out loud. If you do, Ruvi may target Life Points directly this Combat
Wave, and the damage he deals to Life Points is his Mental Attack (MA) and cannot be
prevented or reduced.
```

| Was | Now | Closes |
|---|---|---|
| `[The Item Box]` with no rate limit, at Fast speed | `Once per Round` | Rolled as many times as you had Energy, in one Reaction Window |
| "deals 2 Physical Attack (PA) damage" | "2 physical damage" | Named a stat, supplied a different number. His PA is 1 |
| Continuous global Silence (Passive) | Once per Round, 2 Energy, until End Step (Standard) | **P2**; and Cleanse can answer it now |
| Two abilities with no declared type | Standard, Fast | **G3 / F6** — the only true F6 failures of the three cards |
| "look the opponent in the eye and say…" | "say … out loud" | Unresolvable ("how long counts as looking?"). The sentence is kept; it is the best line on the card |
| Bypasses the Reaction Window | Window stays open; only the damage is unpreventable | Protects the structural guarantee named in CLAUDE.md |
| `[The Glitch]` deals his PA | deals his MA | PA 1 and no ascended stat block, so it dealt 1 damage |

**Two gains worth naming.** The Blue Shell now reads "mental damage," which lands on MH — making
Ruvi the **first card in the pool that attacks the psyche natively**, which is what
[OQ-05](../../design/open-questions.md) says the
Overthinkers were promised and never given. And the once-per-Round limit turns his Level-Up from
"roll until it happens" into a genuine three-to-four-Round telegraph, which *earns* ceiling instead
of dodging it.

### New effect: `data/effects.yaml`

```yaml
- name: Mass Status Application
  points: 6
  description: >-
    Apply one temporary status to every Character on the Board other than the source.
```

Two comparables per **MG1**:

- **Arena Rule Edit (Major) = 5** — *"forbids or forces an entire category of action, symmetrically
  for both players."* That is the same shape. Price above it, because an Arena is a destroyable
  object and this is bolted to a Character whose own abilities keep working, so the symmetry is
  partly false.
- **Mass Removal (Wipes) = 8** — the upper bound. That ends the board permanently; this ends at the
  End Step.

**Recorded honestly:** at 6, Ruvi lands at exactly 28/28. At 7 he fails F4 by one point. The band
6–7 is defensible on its own merits, but 6 is the end of the band that happens to make the card
legal, and deriving a mechanic's price from what a card needs is backwards. Two consequences to
carry forward: the price is a v0.1 hypothesis to revisit the moment a second card wants it, and
**Ruvi has zero headroom** — the next edit to his card breaks F4. Caleb is likewise at exactly
19/19, though he is already there as shipped, so this design does not worsen him.

## 6. Verified numbers

Produced by `tools/scoring.py` against the proposed frontmatter, not by hand. `both` is
`base_spent + ascended_spent`, which is what F4 tests against `int(budget × 1.5)`.

| Card | cost | budget | base | Δ | asc | both | 1.5× | Δ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Caleb — shipped | 3 | 13 | 13 | +0 | 6 | 19 | 19 | +0 |
| **Caleb — proposed** | 3 | 13 | 11 | **+2** | 8 | 19 | 19 | **+0** |
| Julito — shipped | 4 | 16 | 23 | **−7** ✗ | 8 | 31 | 24 | **−7** ✗ |
| Julito — proposed, cost 4 | 4 | 16 | 20 | **−4** ✗ | 7 | 27 | 24 | **−3** ✗ |
| **Julito — proposed, cost 5** | 5 | 19 | 20 | **−1** (±1) | 7 | 27 | 28 | **+1** |
| Ruvi — shipped | 5 | 19 | 21 | **−2** ✗ | 9 | 30 | 28 | **−2** ✗ |
| Ruvi — proposed, Mass Status 8 | 5 | 19 | 17 | +2 | 13 | 30 | 28 | **−2** ✗ |
| **Ruvi — proposed, Mass Status 6** | 5 | 19 | 17 | **+2** | 11 | 28 | 28 | **+0** |

**Corrected 2026-08-05, during implementation.** An earlier draft of this section claimed "F4 never
consults plan credits, so a declared plan cannot rescue a card from this check." That is wrong, and
the distinction matters. `ascended_delta` (`tools/scoring.py:268`) is indeed plan-blind — but F4
reports **G1**, and `_gate_g1` *branches*:

- **No plan declared** → the two-sided base check (±1, under is as wrong as over) **and** the 1.5×
  both-faces check. This is the branch the table above measures.
- **Plan declared** → total spend against the earned **Ceiling**, and both of the above are skipped
  entirely.

So a declared plan *is* the sanctioned escape from the 1.5× rule. Mass Status Application at 6 still
stands on its own comparables, but it was not forced by the arithmetic the way this section
originally said.

**Consequence discovered during implementation (see §10).** On the no-plan branch, the base check
and the both-faces check together make Caleb and Ruvi **unsatisfiable** — not merely tight. All three
cards leave the *over-budget* F4 list, but Caleb and Ruvi land on the *under-budget* one.

## 7. Order of operations

There is a real dependency on the **structured abilities** spec, which is approved and not yet
implemented. That spec names all three of these cards as the four abilities carrying die-roll or
tier tables that migration must preserve verbatim — and this design rewrites three of those four
tables.

1. **Rules primitives and data.** §14 Randomization · §13 glossary (Roll, Counter, Descent) ·
   §10 Descent · §6 Trigger discipline · `plan-credits.yaml` +`ascension_spent` ·
   `effects.yaml` +`Mass Status Application` · `balance-philosophy.md` pricing rule ·
   `decisions.md` for both pricing arguments. Independent of everything else.
2. **OQ-08 resolution.** A decision, not an implementation. Blocks Caleb only.
3. **Structured abilities** — the existing approved spec.
4. **The three card rewrites**, straight into frontmatter.

Doing step 4 before step 3 means writing prose that step 3 then migrates, and it invalidates that
spec's measurements ("55 of 57 reproduce exactly") mid-flight. Doing step 3 first makes these three
rewrites an ordinary frontmatter edit with no prose migration at all.

Nothing here touches `keywords.yaml`, `factions.yaml` or `crews.yaml`, so `generate.py` needs no
run for the three generated documents.

## 8. Out of scope

- **The weakest dimension on each card.** Caleb D3 = 3 (every answer is the same kind), Julito
  D1 = 3 (no exposure to the Warmonger printed weakness), Ruvi D6 = 3 (resolves cleanly but
  teaches no rule). Yorman, 2026-08-05: still adjusting cards, to be dealt with later.
- **OQ-15** — whether trigger chains deserve a response window. §4 above adds only the firing-count
  rule.
- **Ruvi's 2 points of headroom.** A card-content decision, deliberately left open.
- **Retargeting the other seven prose scrapers** — already out of scope in the structured abilities
  spec.

## 10. Discovered during implementation — Caleb and Ruvi are unsatisfiable without a plan

The design was implemented as specified and all three cards score exactly as §6 predicted. But two
of them now trip the **other** half of the no-plan check, and it is not a tuning problem — it is
arithmetically impossible.

On the no-plan branch, `_gate_g1` applies two constraints at once:

```
|base_spent - budget| <= 1          # under budget is as wrong as over (scoring.py:75)
base_spent + ascended_spent <= int(budget * 1.5)
```

Solve both together and the ascended side has a hard cap of `int(budget × 1.5) − (budget − 1)`:

| Card | budget | asc side | 1.5× cap | legal base values | max legal asc |
|---|---:|---:|---:|---|---:|
| Caleb | 13 | 8 | 19 | **none** | 7 |
| Ruvi | 19 | 11 | 28 | **none** | 10 |

Caleb's base must be ≥ 12 to clear the first constraint and ≤ 11 to clear the second. There is no
integer that satisfies both. Same for Ruvi at ≥ 18 and ≤ 17. **Adding base impact and cutting base
impact both fail**, which is why this reads as "under budget by 2" rather than as a number to nudge.

This is [OQ-04](../../design/open-questions.md) surfacing exactly where it was predicted to. The base
side is underspent *because* the ascended side consumes the whole allowance, and the shipped 1.5×
rule was never designed to hold a second face doing 8–11 points of work.

**A declared plan clears both, with room to spare.** Measured, using a trial plan of
`board_state_required: 1` + `telegraph_rounds: 2` for Caleb and `telegraph_rounds: 2` +
`extra_energy: 1` for Ruvi, three windows each:

| Card | Reach | cap | earned | Ceiling | spend | headroom |
|---|---:|---:|---:|---:|---:|---:|
| Caleb | 4 | 39 | 27 | 27 | 19 | **+8** |
| Ruvi | 4 | 57 | 32 | 32 | 28 | **+4** |

**Deliberately not done here.** A plan block changes no printed text — it records costs the card
already asks of you — so writing one is arguably in scope. Two things stop it being automatic:

1. Every claimed window must **name a specific existing card or rule**, per `plan-credits.yaml`.
   Julito's are written out in his Design Notes; Caleb's and Ruvi's are not yet.
2. The `cost_tests` answers are judgments, and getting them generous is the precise documented
   disaster in this repo's history — **D-005** exists because Moammar carried 50 points of phantom
   headroom from three costs that were charged in full and were worth nothing. Caleb's board state is
   the live risk: engineering "an enemy dies while afflicted" is arguably `bite: on_plan`, which
   earns **zero**, because afflicting things is his entire job.

Three paths, for the designer to pick:

- **(a) Declare plans on both.** The system's designed answer, and what §3 says Descent exists to
  enable. Needs the window citations and honest `cost_tests` answers.
- **(b) Cut the ascended sides** to 7 and 10 respectively, and raise both base sides. Satisfies the
  no-plan branch, and costs Caleb either Stunned or Silenced on `[Red Ring of Death]` — i.e. the
  thing the rewrite was for.
- **(c) Leave both errors documented** for the card-tuning pass already planned.

## 9. New open question to file

**OQ-16 · Ascendants have no ascended stat block.**
[§10](../../rulebook/10-ascendants.md) promises the flip reveals "its ultimate form **and stats**,"
but the frontmatter schema carries one `stats` map and not one of the 31 cards has ascended stats.
`tools/scoring.py` charges `stats_total` once, against the base side only.

This surfaced as the reason `[The Glitch]` dealt 1 damage, but it is not a Ruvi problem — it
affects all 31 Ascendants and it interacts with OQ-04, since an unpriced second side that also
cannot change its stats is a second side with only one lever. Severity: medium. Not one of the
fifteen already catalogued.
