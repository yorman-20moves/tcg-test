---
name: Caleb
slug: caleb
card_type: Character
subtype: Ascendant
faction: Assholes
crew: Pwners
cost: 3
stats:
  PA: 2
  PH: 3
  MA: 2
  MH: 2
base:
  keywords: []
  effects:
  - Soft Removal (Stun)
  abilities:
  - name: Teabag
    type: Trigger Ability
    immersion: Caleb dances on their bodies and ruins their game.
    mechanics: |-
      Once per Round, when an enemy Character is Murdered, you may pay 1 Energy to roll a d6 and target an enemy Character. Until the End Step, that Character is:
      1-3: Exhausted.
      4-5: Silenced.
      6: Stunned.
ascended:
  keywords: []
  effects:
  - Status Application (Major)
  - Status Application (Major)
  abilities:
  - name: Red Ring of Death
    type: Standard Ability
    immersion: Caleb bricks their system and traps them offline.
    mechanics: |-
      Once per Round, pay 2 Energy to inflict Stunned and Silenced on an enemy Character. Both persist until removed.

      At each End Step, that Character's controller may pay 1 Energy and roll a d6:

      4-6: The reboot succeeds and both statuses are removed.

      1-3: The reboot fails and they remain bricked.
art:
  base: CalebTheRedRingReaper
  ascended: CalebTheRedRingReaperLVLUP
status: ported
---

# Caleb

**Assholes** · Pwners · Ascendant

## Base Side

`Cost 3` — **PA 2 / PH 3 / MA 2 / MH 2**

### Rules Text

[Teabag] (Trigger Ability): Caleb dances on their bodies and ruins their game.
Once per Round, when an enemy Character is Murdered, you may pay 1 Energy to roll a d6 and target an enemy Character. Until the End Step, that Character is:
1-3: Exhausted.
4-5: Silenced.
6: Stunned.

## Level-Up

### Condition

Caleb starts literally melting the hardware with his toxicity. Place a Salt counter on Caleb whenever an enemy Character is Murdered while afflicted with Exhausted, Silenced or Stunned, while Caleb is face-up on the Board (maximum 3). When Caleb has 3 Salt counters, he levels up.

### Ascended Rules Text

[Red Ring of Death] (Standard Ability): Caleb bricks their system and traps them offline.
Once per Round, pay 2 Energy to inflict Stunned and Silenced on an enemy Character. Both persist until removed.

At each End Step, that Character's controller may pay 1 Energy and roll a d6:

4-6: The reboot succeeds and both statuses are removed.

1-3: The reboot fails and they remain bricked.

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
Perfectly Balanced
Stats: 9
Base Keywords: 0
Base Effects: 4
Lvl-Up Keywords: 0 [Free]
Lvl-Up Effects: 6 [Free]
```

### 2026-08-05 — rewritten against the four new primitives (D-010)

Five failures closed. Every edit traces to a named gate.

- **`[Teabag]` had no rate limit.** A Mass Removal fired it once per body, stacking statuses inside
  a single action with no window anywhere in it. Now `Once per Round`, which is what §6's new
  Trigger rule 3 requires of any Trigger whose effect accumulates.
- **A Trigger cannot "pay 1 Energy" and also fire automatically.** §6 now permits a Trigger to name
  a cost, with paying optional — hence `you may pay`.
- **No duration on any of the three statuses**, which is an automatic **G6** failure per §11. Now
  `Until the End Step`.
- **"personally witnessed 3 Characters die"** used two terms the rulebook does not define. Now
  **Salt counters** (max 3, per the new Counter primitive) and `while Caleb is face-up on the
  Board`; "die" became **Murdered**, which is the glossary term.
- **`[Bricked]` was not a status.** `data/status-effects.yaml` holds six and that was not one.
  It was Stunned + Silenced stapled together, and a 7th status for that does not clear **S7**, so
  the word stays as flavour and the mechanics print the two real statuses.

**The P2 fix is the reboot moving to the End Step.** As printed, "cannot be removed by card effects"
made both Cleanse entries dead text, and the reboot cost the opponent *their Phase 2 action* at 50%
— so application cost Caleb one action and removal cost the opponent two on average. Application
beat removal on rate, which is what made it a lock rather than a tempo hit. At the End Step the roll
is outside the action economy, fires every Round, and Cleanse works again. The humiliating coin flip
— the part worth keeping — is untouched.

**Pricing.** Under D-010's rule a random effect costs its most expensive outcome, so `[Teabag]` is
one `Soft Removal (Stun)` rather than a stun *plus* a minor status. Base 11 / 13. Ascended is two
`Status Application (Major)` because both statuses persist until removed: both faces 19 / 19.

**OQ-08 resolved in this card's favour (D-011).** `[Teabag]` applies Exhausted on a 1–3, and Exhausted
had two contradictory definitions — a +1 Energy attacker tax in §11, attack-halving in the Elements
sheet. This card broke the tie: his Level-Up counts enemies that die *while afflicted*, and halved
attack makes them lose fights and die afflicted where a tax on declaring an attacker does nothing.
**Exhausted now halves PA and MA, rounded down**, applied to printed values.

**Weakest dimension: D3 = 3.** Every answer to Caleb is the same kind — remove him, or Cleanse the
status. No pre-empt, no punish, no race. Flagged and deferred; Yorman is doing a card-tuning pass.

**Known blocking error, deliberately left (Yorman, 2026-08-05).** `check.py` reports
`[F4] base side under budget by 2`. This is not a number to nudge — it is **unsatisfiable** on the
no-plan branch of G1, which applies two constraints at once:

```
|base_spent - 13| <= 1        ->  base must be 12..14
base_spent + 8   <= 19        ->  base must be <= 11
```

No integer satisfies both, so adding base impact and cutting it both fail. With the ascended side at
8 points, the most base could ever be is 11; to satisfy the first constraint the ascended side would
have to come down to **7**, which means dropping either Stunned or Silenced from
`[Red Ring of Death]` — the exact thing this rewrite existed to preserve.

This is OQ-04 surfacing: the base side is underspent *because* the second face consumes the whole
allowance, and the shipped 1.5× rule was never built to hold one doing 8 points of work. **The fix
whenever the tuning pass happens is to declare a plan** — measured, a trial plan of
`board_state_required: 1` + `telegraph_rounds: 2` with three windows gives Reach 4, a Ceiling of 27
against 19 spent, and +8 headroom. It was not written here because the `cost_tests` answers are
judgments and the honest one is unflattering: engineering "an enemy dies while afflicted" is
plausibly `bite: on_plan`, worth **zero**, because afflicting things is his entire job. See D-005 for
why guessing generously on that question is the documented way this system goes wrong.
