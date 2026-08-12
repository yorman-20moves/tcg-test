# 6. Anatomy of a Character

Every Descendant and Ascendant has four stats.

| Stat | Name | Meaning |
|---|---|---|
| **PA** | Physical Attack | Damage dealt by physical strikes. **The default stat in standard Combat Waves.** |
| **PH** | Physical Health | Physical stamina. |
| **MA** | Mental Attack | Damage dealt by psychological strikes. Used through Tactics, Attachments, or specific abilities/keywords. **Not used in standard combat unless explicitly stated.** |
| **MH** | Mental Health | Mental fortitude. |

## Combat Rules for Stats

**Lethality:** if a Character's PH **or** MH drops to 0 from damage or a card effect, they are
immediately **Murdered**.

**Permanent damage:** all damage to PH or MH is permanent and persists across Rounds unless
explicitly healed.

**The Safety Net:** a Character can only be Murdered by *active* damage or effects — never by a
buff wearing off. See [Round Structure §Phase 3](08-round-structure.md#phase-3-the-end-step).

> **Open question (OQ-05):** MA/MH is half the stat system but reaches the board through
> almost nothing. Only the Troll keyword converts an attack to MA-vs-MH natively.

## Character Ability Types

Unless **Silenced**, a Character can use the abilities printed on its card.

<!-- GENERATED:ability-types — from data/ability-types.yaml via tools/generate.py -->
| Type | When it can be used |
|---|---|
| **Standard Ability** | Only during Phase 2, as your single alternating action. |
| **Fast Ability** | The only abilities fast enough for the Reaction Window or the Stack. |
| **Trigger Ability** | Costs no action. Fires automatically the moment its condition is met. |
| **Passive Ability** | Always on, continuously, while the Character is face-up on the Board. |
<!-- /GENERATED:ability-types -->

**Card-writing rule:** every printed ability must declare its type in brackets. A card whose
ability type is unstated fails gameplay gate **G3**.

### Trigger Abilities in detail

"Fires automatically" needs three qualifications, because a Trigger is the one ability type that
costs no action and therefore has no natural brake.

1. **A Trigger may name a cost.** If it does, its controller chooses whether to pay at the moment
   the trigger fires; declining means the ability simply does not resolve. Paying a cost **never**
   costs an action — that is what makes it a Trigger and not a Standard Ability.
2. **A Trigger fires once per *occurrence* of its condition.** If the condition occurs several
   times at once — five Characters Murdered by one effect — it fires five times, and its controller
   chooses the order they resolve in.
3. **A Trigger whose effect accumulates must print a rate limit** (`Once per Round`), or it fails
   gameplay gate **G6**.

> **Why rule 3 is a gate and not advice.** Rule 2 means a board wipe can fire one Trigger five
> times inside a single action, with no window for the opponent anywhere in it. That is the
> structural hole described in **OQ-15**, and it is not solved here — what rule 3 does is make each
> individual card state its own ceiling, so the hole cannot be widened by a card that forgot to.

## Related

- [Round Structure §Phase 2](08-round-structure.md#phase-2-the-action-phase-alternating) — what an action is
- [Combat §Step 2](09-combat-and-stack.md#step-2--the-reaction-window) — where Fast Abilities live
- [Glossary](13-glossary.md) — Counter
