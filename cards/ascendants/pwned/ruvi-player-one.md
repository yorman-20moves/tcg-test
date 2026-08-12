---
name: Ruvi, Player One
slug: ruvi-player-one
card_type: Character
subtype: Ascendant
faction: Overthinkers
crew: Pwners
cost: 5
stats:
  PA: 1
  PH: 3
  MA: 5
  MH: 4
base:
  keywords: []
  effects:
  - Direct Damage/Heal 4
  abilities:
  - name: The Item Box
    type: Fast Ability
    immersion: Ruvi is bored and wants to see if pure RNG can carry him.
    mechanics: |-
      Once per Round, pay 1 Energy and roll a d6. Apply the result immediately:

      1-2 (Banana Peel): Bad luck. Ruvi takes 1 permanent Mental Health (MH) damage.

      3-4 (Green Shell): Ruvi deals 2 physical damage to a target enemy Character.

      5 (Mushroom): Ruvi permanently gains +2 Physical Health (PH) and +2 Mental Health (MH).

      6 (The Blue Shell): Ruvi deals 4 mental damage to a target enemy Character.
ascended:
  keywords: []
  effects:
  - Mass Status Application
  - Direct Damage/Heal 5
  abilities:
  - name: You Know This Is Just A Game, Right?
    type: Standard Ability
    immersion: Ruvi has realized that he is just a card and uses a GameShark to hack the system.
    mechanics: 'Once per Round, pay 2 Energy: until the End Step, every other Character on the Board — allied and enemy — is Silenced.'
  - name: The Glitch
    type: Fast Ability
    immersion: Ruvi looks past the cardboard and finds the seam.
    mechanics: Once per Game, when you declare a Combat Wave in which Ruvi is an attacker, you may say "it's just a game" out loud. If you do, Ruvi may target Life Points directly this Combat Wave, the damage he deals to Life Points is his Mental Attack (MA) instead of his Physical Attack (PA), and that damage cannot be prevented or reduced.
art:
  base: RuviPlayerONE
  ascended: RuviPlayerONELVLUP
status: ported
---

# Ruvi, Player One

**Overthinkers** · Pwners · Ascendant

## Base Side

`Cost 5` — **PA 1 / PH 3 / MA 5 / MH 4**

### Rules Text

[The Item Box] (Fast Ability): Ruvi is bored and wants to see if pure RNG can carry him.
Once per Round, pay 1 Energy and roll a d6. Apply the result immediately:

1-2 (Banana Peel): Bad luck. Ruvi takes 1 permanent Mental Health (MH) damage.

3-4 (Green Shell): Ruvi deals 2 physical damage to a target enemy Character.

5 (Mushroom): Ruvi permanently gains +2 Physical Health (PH) and +2 Mental Health (MH).

6 (The Blue Shell): Ruvi deals 4 mental damage to a target enemy Character.

## Level-Up

### Condition

Ruvi hits the jackpot and realizes the world is a game. When Ruvi rolls a 6 on [The Item Box], he levels up.

### Ascended Rules Text

[You Know This Is Just A Game, Right?] (Standard Ability): Ruvi has realized that he is just a card and uses a GameShark to hack the system.
Once per Round, pay 2 Energy: until the End Step, every other Character on the Board — allied and enemy — is Silenced.

[The Glitch] (Fast Ability): Ruvi looks past the cardboard and finds the seam.
Once per Game, when you declare a Combat Wave in which Ruvi is an attacker, you may say "it's just a game" out loud. If you do, Ruvi may target Life Points directly this Combat Wave, the damage he deals to Life Points is his Mental Attack (MA) instead of his Physical Attack (PA), and that damage cannot be prevented or reduced.

## Lore

<!-- Fill using docs/rubrics/lore-rubric.md — the Lore Packet is required for every card. -->

**Premise (one line):** _TBD_

**The True Detail:** _TBD_

**The Myth:** _TBD_

**Why This Faction:** _TBD_

**Why This Crew:** _TBD_

**The Fall (printed weakness):** _TBD_

**The Ascension (what the level-up MEANS):** _TBD_

## Design Notes

<!-- Rubric scores, balance decisions, playtest results. Append, don't overwrite. -->

Spreadsheet balance verdict at time of port:

```
Overpowered by 2 pts
Stats: 13
Base Keywords: 0
Base Effects: 8
Lvl-Up Keywords: 0 [Free]
Lvl-Up Effects: 9 [Free]
```

### 2026-08-05 — rewritten against the four new primitives (D-010)

**The global Silence was Pacifier, and Pacifier is prohibited.** As printed,
`[You Know This Is Just A Game, Right?]` was a continuous Passive, which means Cleanse (Minor) *and*
Cleanse (Major) could never answer it — the Passive re-applies — so only removal could. That is
**P2**, and it is the identical reasoning by which OQ-09 ruled Pacifier unprintable. D3 scored 1,
which the dominant-weakness rule blocks regardless of total. It is an **activation** now: once per
Round, 2 Energy, until the End Step. It costs him his whole action every Round, and Cleanse works.
Yorman picked this over an upkeep version and over reframing it as a punish on ability use — the
activation is the shortest distance from the printed card, and "everything shuts up for two Energy"
is still the most obnoxious button in the game, which was the point.

**`[The Item Box]` had no rate limit, at Fast speed.** He rolled as many times as he had Energy,
inside a single Reaction Window, stacking Blue Shells. Now `Once per Round` — which incidentally
turns his Level-Up from "roll until it happens" into a genuine three-to-four-Round telegraph that
*earns* ceiling instead of dodging it.

**"deals 2 Physical Attack (PA) damage" named a stat and supplied a different number.** His printed
PA is 1. Now "2 physical damage" and "4 mental damage" — and the mental one lands on MH, making Ruvi
the **first card in the pool that attacks the psyche natively**, which is what OQ-05 says the
Overthinkers were promised and never given.

**Both ascended abilities declared no type** — the only true **F6** failures across the three Pwners
cards; Caleb's three were a prose-parser artifact. Standard and Fast respectively.

**`[The Glitch]` bypassed the Reaction Window.** CLAUDE.md names the alternating-action window as the
game's best structural asset, so it does not get bypassed. The window stays open — Protector can
still intercept, Combat Tactics still work — and what is unpreventable is the *damage* if it lands.
"Look the opponent in the eye" is gone because it cannot be resolved (how long counts as looking?);
saying it out loud can be, so the sentence stays. It is the best line on the card.

**And it dealt 1 damage.** `[The Glitch]` dealt "his PA," which is 1, because there is no ascended
stat block anywhere in the schema — the ability that broke the most sacred rule in the game was a
1-point ping. Repointed at his MA (5). The underlying gap is now filed as **OQ-16**; it affects all
31 Ascendants, not this card.

**Pricing.** Under D-010's rule a random effect costs its most expensive outcome, so `[The Item Box]`
is one `Direct Damage/Heal 4` rather than a sum of every branch — which alone takes the base side
from 21/19 (over) to **17/19**. The Banana Peel branch earns no credit; variance is a choice, not a
cost. Ascended is the new `Mass Status Application` (6) plus `Direct Damage/Heal 5`.

**Known blocking error, deliberately left (Yorman, 2026-08-05).** `check.py` reports
`[F4] base side under budget by 2`, and like Caleb it is **unsatisfiable** rather than mistuned. The
no-plan branch of G1 applies two constraints together:

```
|base_spent - 19| <= 1         ->  base must be 18..20
base_spent + 11  <= 28         ->  base must be <= 17
```

No integer satisfies both. With the ascended side at 11 points the ascended cap is **10**, so
satisfying the no-plan branch means cutting either the mass Silence or the MA Glitch. **The fix is to
declare a plan** — measured, `telegraph_rounds: 2` + `extra_energy: 1` with three windows gives
Reach 4, a Ceiling of 32 against 28 spent, +4 headroom. Not written here because the window citations
and the `cost_tests` answers are design judgments (see D-005).

**And the pricing is entangled with the margin.** Both faces land at exactly **28 / 28**. At
`Mass Status Application` = 7 he fails the both-faces check by one point, and 6 is the end of a
defensible 6–7 band that happens to make this card legal — which is a bad way to price a mechanic.
Recorded in D-010 as a v0.1 hypothesis. Declaring a plan is what makes the entry's price stop being
load-bearing here, which is a second reason to prefer it over cutting two points.

**Weakest dimension: D6 = 3.** Two abilities, a six-outcome die table, a once-per-Game trigger and a
spoken sentence. It resolves cleanly but it does not teach a rule. Flagged and deferred; Yorman is
doing a card-tuning pass.
