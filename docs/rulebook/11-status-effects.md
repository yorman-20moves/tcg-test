# 11. Status Effects

Status effects are debilitating conditions placed on a Character. This section is
**authoritative**; `data/status-effects.yaml` carries the same list for tooling.

| Status | Effect |
|---|---|
| **Exhausted** | Pushing this Character into a fight requires heavy investment. It costs an **additional 1 Energy** to declare them as an attacker. |
| **Feared** | Terrified. Cannot declare attacks, and takes **+1 damage** from all incoming sources. |
| **Shattered** | Mentally broken. **MH cannot be healed.** On the next separate combat or effect that deals MA damage to them, they take an extra **1 permanent MH damage**, then Shattered is removed. |
| **Silenced** | Shut down. All printed Character abilities are **blanked**. |
| **Stunned** | Completely paralyzed. Cannot declare attacks, use abilities, or act as a **Protector**. |
| **Wounded** | Physically broken. **PH cannot be healed.** On the next separate combat or effect that deals PA damage to them, they take an extra **1 permanent PH damage**, then Wounded is removed. |

> **Open question (OQ-08):** The spreadsheet's Elements sheet defines **Exhausted** as
> *"attack power (both physical and mental) is halved"* — a completely different effect from the
> +1 Energy tax above. One of these is dead text. Until resolved, the rulebook wins.

## Design notes

- **Wounded** and **Shattered** are the setup halves of **Executioner** and of MA-based removal.
  They are the game's "you are now killable" markers. Any card that applies them is doing more
  than its point cost suggests if the deck also runs the payoff.
- No status currently has a printed **duration** other than "for the duration of the effect."
  Every card applying a status must state its own duration (End Step, permanent, until removed),
  or it fails gameplay gate **G6**.
