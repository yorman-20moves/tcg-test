---
name: Angel, The Smiling Saboteur
slug: angel-the-smiling-saboteur
card_type: Character
subtype: Ascendant
faction: Assholes
crew: Mobb 134
cost: 4
stats:
  PA: 4
  PH: 3
  MA: 3
  MH: 3
base:
  keywords:
  - Infiltrator
  effects:
  - Energy Gen 1
  - Resource Denial
  abilities:
  - name: False Savior
    immersion: Angel smiles right in your face while he picks your pocket.
    mechanics: When summoned, place Angel onto the opponent's Board. The opponent takes control of him to attack or pay costs, but they cannot activate his printed abilities, and their other Characters cannot attack him.
    keyword: Infiltrator
  - name: The Siphon
    type: Trigger Ability
    mechanics: During Phase 1 (The Refresh), force the opponent to change 1 card in their Resource Row to Used (they lose 1 Energy this Round), and the controlling player gains +1 temporary Energy until the end of Phase 3.
ascended:
  keywords: []
  effects:
  - Mass Removal (Wipes)
  - Status Application (Major)
  abilities:
  - name: The Betrayal
    type: Passive Ability
    immersion: Angel snaps the trap shut and ruins them all.
    mechanics: The moment he levels up, he deals 4 Mental Attack (MA) damage to every Character on the opponent's Board. As long as he remains face-up, the maximum Mental Health (MH) of all enemy Characters is reduced by 4 (minimum of 1).
art:
  base: AngelTheSmilingSaboteur
  ascended: AngelTheSmilingSaboteurLVLUP
status: ported
plan:
  produces:
  - opponent_characters_gone
---

# Angel, The Smiling Saboteur

**Assholes** · Mobb 134 · Ascendant

## Base Side

`Cost 4` — **PA 4 / PH 3 / MA 3 / MH 3**

Keywords: Infiltrator

### Rules Text

[False Savior] (Infiltrator): Angel smiles right in your face while he picks your pocket.
When summoned, place Angel onto the opponent's Board. The opponent takes control of him to attack or pay costs, but they cannot activate his printed abilities, and their other Characters cannot attack him.

[The Siphon] (Trigger Ability): During Phase 1 (The Refresh), force the opponent to change 1 card in their Resource Row to Used (they lose 1 Energy this Round), and the controlling player gains +1 temporary Energy until the end of Phase 3.

## Level-Up

### Condition

Angel finally shows his true colors. Once Angel has successfully siphoned 4 Energy from the opponent, he levels up.

### Ascended Rules Text

[The Betrayal] (Passive Ability): Angel snaps the trap shut and ruins them all.
The moment he levels up, he deals 4 Mental Attack (MA) damage to every Character on the opponent's Board. As long as he remains face-up, the maximum Mental Health (MH) of all enemy Characters is reduced by 4 (minimum of 1).

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
Stats: 13
Base Keywords: -2
Base Effects: 5
Lvl-Up Keywords: 0 [Free]
Lvl-Up Effects: 20 [Free]
```
