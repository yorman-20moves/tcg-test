# 12. Factions & Exclusive Keywords (The Roles)

Keywords are specific **Roles** a Character plays on the Board. **Each Role is completely
exclusive to its faction.** A card carrying a keyword from another faction fails gameplay
gate **G4**.

The point values below are the budget cost charged by [`tools/balance.py`](../../tools/balance.py).
They live in [`data/keywords.yaml`](../../data/keywords.yaml), which is the source of truth —
**this table is generated from it.** Edit the YAML, not this file.

A negative cost means the keyword is a *drawback* and the designer is paid budget for taking it.

---

## 🟥 The Warmongers

| Keyword | Pts | Effect |
|---|---:|---|
| **Berserker** | 2 | Gains +1 PA every time they take permanent PH damage. |
| **Executioner** | 2 | Instantly Murders any defending Character with permanent PH damage, bypassing math. |
| **Protector** | 2 | Can intercept one attack intended for Life Points or another Character. |
| **Juggernaut** | 3 | Excess PA damage beyond defender's PH spills over to Life Points. |
| **Combo-Striker** | 4 | Attacks resolve in two strikes. The first deals damage without simultaneous retaliation. |

---

## 🟦 The Overthinkers

| Keyword | Pts | Effect |
|---|---:|---|
| **Instigator** | 2 | Opponent must target this unit before Life Points or others. |
| **Interrogator** | 2 | On successful strike, opponent must reveal their Hand. |
| **Tracker** | 2 | Can target/intercept Prowlers, bypassing stealth. |
| **Troll** | 2 | Bypasses PA to attack MH directly. |

---

## 🟩 The Assholes

| Keyword | Pts | Effect |
|---|---:|---|
| **Infiltrator** | -2 | Summoned to opponent's board for them to use, providing passive benefits to you. |
| **Hustler +1** | 3 | Generates 1 temporary Energy on hit. |
| **Prowler** | 3 | Stealth unit. Cannot be intercepted/targeted (unless Tracker); can hit Life Points directly. |
| **Extortionist** | 5 | When hitting Life Points, opponent discards a card. |
| **Hustler +2** | 5 | Generates 2 temporary Energy on hit. |
| **Hustler +3** | 7 | Generates 3 temporary Energy on hit. |
| **Hustler +4** | 9 | Generates 4 temporary Energy on hit. |
| **Hustler +5** | 11 | Generates 5 temporary Energy on hit. |

---

## 🟨 The Icons

| Keyword | Pts | Effect |
|---|---:|---|
| **Guilt-Tripper** | 2 | Enemy takes 2 MA damage purely from the shame of hitting them. |
| **Martyr** | 2 | 0 PA/MA, but grants massive Influence Points when Murdered. |
| **Sponsor** | 2 | On play, place one card from Hand face-down into Resource Row for free. |
| **Nurturer** | 4 | Uses an action to heal permanent PH or MH damage. |
| **Pacifier** | 5 | Aura completely preventing the declaration of a Combat Wave. |
---

## Reading the point curve

The spread is the designer's honest opinion of power, and it is worth reading as a document.

- **2 points** is the baseline "this Character has a job." Most Roles sit here.
- **3–5 points** buys a Role that changes how the opponent is allowed to play (Prowler ignores
  the target rule; Pacifier turns combat off entirely).
- **Hustler scales super-linearly** (3 / 5 / 7 / 9 / 11) because Energy compounds — correct.
- **Infiltrator at −2** is the only negative in the table: you are paid to hand the opponent a
  body. Whether that is actually a drawback depends entirely on the card, and it is the most
  likely mispriced entry in the system.
- **Pacifier at 5** buys an unconditional lock on the game's only damage mechanism. Compare it
  to Mass Removal at 8 and ask whether 5 is right. See open question **OQ-09**.

## Cross-references

- [Combat Wave & The Stack](09-combat-and-stack.md) — Protector, Juggernaut, Combo-Striker,
  Executioner, Prowler and Tracker all resolve inside combat steps.
- [Status Effects](11-status-effects.md) — Executioner pays off Wounded.
- [`../rubrics/gameplay-rubric.md`](../rubrics/gameplay-rubric.md) — gate G4 (keyword exclusivity)
  and dimension D1 (faction fantasy fidelity).
