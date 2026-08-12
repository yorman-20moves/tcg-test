# 14. Randomization

Some abilities do not decide what they do until they resolve. This section owns **the Roll** —
the only randomizer in the game.

---

## The Roll

When an ability says **roll a d6**, roll one standard six-sided die.

| | |
|---|---|
| **Who rolls** | The **controller of the ability**, unless the ability says otherwise. |
| **Where** | Somewhere both players can see it. A roll is always public. |
| **How many** | Exactly **one** roll each time the ability resolves. |
| **When** | At **resolution**, never at declaration. |

## The result is locked

Once the die comes to rest, its result **cannot be re-rolled, modified, or replaced** unless a
card explicitly says so. No card currently says so.

## A roll is not an interaction window

The roll happens **inside** the ability's resolution. Neither player may respond between the die
coming to rest and its effect applying — not with a Combat Tactic, not with a Fast Ability, not by
adding to the Stack.

An ability that rolls while on the Stack rolls when it **resolves**, not when it was played. So a
Fast Ability placed on the Stack during a Reaction Window has not rolled yet, and the opponent
responding to it is responding to the ability, not to a number.

> **Why the roll is sealed.** If either player could act between the die and its effect, every d6
> would open a new timing window that the [Combat Wave](09-combat-and-stack.md) does not have a
> step for, and the Stack would need a whole second layer. A roll is a **telegraph**, not a window:
> the opponent watches it happen and cannot touch it. Where they get to act is *before* — deciding
> whether to leave you a target worth rolling for.

## Card-writing rule

An ability that names an outcome for **some** results must name an outcome for **every** result
1 through 6, or it fails gameplay gate **G6**.

There is no default and no "nothing happens" unless the card prints it. A card with a gap in its
table is a rules argument at the table, which is exactly what G6 exists to stop.

## Pricing

A random effect is priced at its **most expensive outcome**, and a bad outcome earns no credit.
See [balance-philosophy.md §Pricing a random effect](../design/balance-philosophy.md).

## Related

- [Glossary](13-glossary.md) — Roll
- [Combat Wave & The Stack](09-combat-and-stack.md) — the Reaction Window and LIFO resolution
