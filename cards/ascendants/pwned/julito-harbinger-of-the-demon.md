---
name: Julito, Harbinger of the Demon
slug: julito-harbinger-of-the-demon
card_type: Character
subtype: Ascendant
faction: Warmongers
crew: Pwners
cost: 5
stats:
  PA: 4
  PH: 4
  MA: 1
  MH: 3
base:
  keywords:
  - Combo-Striker
  effects:
  - Permanent Buff 2
  - Permanent Buff 2
  abilities:
  - name: Build Meter
    type: Trigger Ability
    immersion: Julito lives for a bloody, unbroken combo.
    mechanics: Whenever Julito Murders an enemy Character, or deals damage to the opponent's Life Points, place an EX counter on him (maximum 3).
  - name: The EX Enhancements
    type: Passive Ability
    immersion: The meter is not a resource, it is a mood.
    mechanics: |-
      While Julito has 1 or more EX counters: +2 PA and +2 PH.
      While Julito has 2 or more EX counters: he gains (Combo-Striker). His combat resolves in two strikes — a free first strike without retaliation, then a simultaneous strike.
ascended:
  keywords:
  - Berserker
  effects:
  - Hard Removal
  abilities:
  - name: Demonic Ascension
    type: Passive Ability
    immersion: Julito is drunk with the power of the dark Hadou.
    mechanics: While Julito has 3 EX counters, he gains (Berserker). He gains +1 Physical Attack (PA) every time he takes permanent Physical Health (PH) damage.
  - name: Shun Goku Satsu
    type: Trigger Ability
    immersion: Julito delivers a thousand fatal strikes in the blink of an eye.
    mechanics: When Julito clashes with a Character in a Combat Wave, you may pay 1 Energy and spend all 3 EX counters. If you do, he Murders that Character outright, bypassing the standard math. Julito then Descends.
art:
  base: JulitoHarbingeroftheDemon
  ascended: JulitoHarbingeroftheDemonLVLUP
status: ported
---

# Julito, Harbinger of the Demon

**Warmongers** · Pwners · Ascendant

## Base Side

`Cost 5` — **PA 4 / PH 4 / MA 1 / MH 3**

Keywords: Combo-Striker

### Rules Text

[Build Meter] (Trigger Ability): Julito lives for a bloody, unbroken combo.
Whenever Julito Murders an enemy Character, or deals damage to the opponent's Life Points, place an EX counter on him (maximum 3).

[The EX Enhancements] (Passive Ability): The meter is not a resource, it is a mood.
While Julito has 1 or more EX counters: +2 PA and +2 PH.
While Julito has 2 or more EX counters: he gains (Combo-Striker). His combat resolves in two strikes — a free first strike without retaliation, then a simultaneous strike.

## Level-Up

### Condition

Julito loses his mind the second his meter is full. When Julito has 3 EX counters, he levels up.

Keywords gained: Berserker

### Ascended Rules Text

[Demonic Ascension] (Passive Ability): Julito is drunk with the power of the dark Hadou.
While Julito has 3 EX counters, he gains (Berserker). He gains +1 Physical Attack (PA) every time he takes permanent Physical Health (PH) damage.

[Shun Goku Satsu] (Trigger Ability): Julito delivers a thousand fatal strikes in the blink of an eye.
When Julito clashes with a Character in a Combat Wave, you may pay 1 Energy and spend all 3 EX counters. If you do, he Murders that Character outright, bypassing the standard math. Julito then Descends.

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
Overpowered by 7 pts
Stats: 12
Base Keywords: 4
Base Effects: 7
Lvl-Up Keywords: 2 [Free]
Lvl-Up Effects: 6 [Free]
```

### 2026-08-05 — rewritten against the four new primitives (D-010)

**"EX Meter token" was the worst collision in the pool.** §5 defines a **Token** as *a Character
created by an effect rather than played from a zone*, and adds that a Token is "a Character for
every rule." Read literally, `[Build Meter]` created up to three Characters. They are **EX
counters** now, under the new Counter primitive — which also carries the clause that makes this card
work at all: **counters survive an Ascendant's flip in both directions**, since he ascends *because*
he holds three and then spends them from the far side.

**"Level 1 / Level 2" invented a third leveling axis** on top of base/ascended, and never said what
either tier was keyed to — two players resolved it differently, which is a flat **G6** failure. Both
tiers are preserved exactly; they are keyed to counter thresholds now. Nothing was cut.

**`[Shun Goku Satsu]` was a 1-Energy Fast targeted non-combat Murder.** OQ-09 and gate **G7** both
lean on "the Warmongers have no printed non-combat removal" as a defining constraint, and Executioner
only ever Murders a *defender*, in combat. Yorman's call: **the constraint holds.** It is now a
Trigger resolving in **Step 4** of the Combat Wave — the slot §9 already documents for "Executioner
mechanics and other damage replacements" — so it needed no new timing rule. He still takes the clash
damage, which now matters, because Descent carries it and the Safety Net catches him at 1.

**Three windows, each naming a specific rule:** kill him before 3 counters (W1); **Silence** him,
which blanks printed abilities and therefore freezes both the Passive and the Trigger (W2);
Protector intercept or a Combat Tactic in Step 2 (W3).

**One flavour correction, not a silent typo fix.** `[Demonic Ascension]` read *"**Julio** is drunk
with the power of the dark Hadou."* **Julio, the Tyrant of the Tainted Touch** is a real card in Mobb
134, so on Julito's own card that word pointed at somebody else.

**Two pricing corrections, both findings rather than nerfs.** `Multiple Attacks` (5) was charged for
something the text never granted — **Combo-Striker already is** "attacks resolve in two strikes," so
it was double-charged. And `+2 PA and +2 PH` is two stat axes priced as one `Permanent Buff 2`.

**Cost 4 → 5, and he cannot credit his way out.** `cost_tests.bite` rates a cost that **is** the plan
at 0.0, and a Warmonger accumulating counters by winning fights is doing his job, not paying a price
— so the meter earns him nothing, correctly. Verified with `tools/scoring.py`: at cost 4 the
corrected card is base 20/16 and both faces 27/24, failing both checks; at cost 5 it is base 20/19
(inside the ±1 tolerance) and both faces 27/28. One number moved and no tier was lost.

**Descent earns him a credit** — `ascension_spent` (4), run through the tests as bite `competes`
(1.0), timing `at_payoff` (0.5), enabler `none` (1.0). Weakest test wins: **4 × 0.5 = 2** points of
Earned, undeclared here because he does not need the ceiling.

**Weakest dimension: D1 = 3.** Nothing on him is exposed to *"when a problem cannot be solved with
fists."* He is pure Warmonger strength with no Warmonger weakness printed. His near-dead Life Points
clause — §9 forbids attacking Life Points while the opponent has Characters, and he has neither
Prowler nor Juggernaut — is accidentally the honest version of that weakness. Worth making
deliberate. Flagged and deferred; Yorman is doing a card-tuning pass.
