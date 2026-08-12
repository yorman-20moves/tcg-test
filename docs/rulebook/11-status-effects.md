# 11. Status Effects

Status effects are debilitating conditions placed on a Character. This section is
**authoritative**; `data/status-effects.yaml` carries the same list for tooling.

| Status | Effect |
|---|---|
| **Exhausted** | Physically spent. Both **PA and MA are halved**, rounded down. |
| **Feared** | Terrified. Cannot declare attacks, and takes **+1 damage** from all incoming sources. |
| **Shattered** | Mentally broken. **MH cannot be healed.** On the next separate combat or effect that deals MA damage to them, they take an extra **1 permanent MH damage**, then Shattered is removed. |
| **Silenced** | Shut down. All printed Character abilities are **blanked**. |
| **Stunned** | Completely paralyzed. Cannot declare attacks, use abilities, or act as a **Protector**. |
| **Wounded** | Physically broken. **PH cannot be healed.** On the next separate combat or effect that deals PA damage to them, they take an extra **1 permanent PH damage**, then Wounded is removed. |

**Halving is a multiplier, so it applies to printed values.** Halve the **printed** PA or MA first,
round down, then add buffs, Attachments and Permanent Buffs on top — the same order the
[Glossary](13-glossary.md) entry for **Printed** sets for Range's multiplier. A Character with a
printed 5 PA and a +2 Attachment attacks for `(5 ÷ 2 → 2) + 2 = 4`, not 3.

*(OQ-08 resolved 2026-08-05, D-011. The rulebook previously defined Exhausted as a +1 Energy tax on
declaring an attacker; that text is retired.)*

## Design notes

- **Wounded** and **Shattered** are the setup halves of **Executioner** and of MA-based removal.
  They are the game's "you are now killable" markers. Any card that applies them is doing more
  than its point cost suggests if the deck also runs the payoff.
- No status currently has a printed **duration** other than "for the duration of the effect."
  Every card applying a status must state its own duration (End Step, permanent, until removed),
  or it fails gameplay gate **G6**.
