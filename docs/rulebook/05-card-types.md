# 5. Card Types & Subtypes

## Character

The physical units on the Board, with stats.

- **Descendant** — standard crew members, played from the Main Deck.
- **Ascendant** — legendary boss versions, played from the VIP Area. Double-sided, with
  Level-Up conditions. See [Ascendants](10-ascendants.md).
- **Token** — a Character that was never a card. See below.

### Token

A Token is a Character created by an effect rather than played from a zone. It has printed
stats, no cost, and no card behind it.

- A Token is a **Character for every rule**. It can attack, be attacked, be targeted, be
  Protected, be Murdered, and it counts toward board-state conditions.
- A Token inherits the **faction and crew of the effect that created it**, so faction and
  crew synergies see it.
- Tokens are never Ascendants, are never double-sided, and have no Level-Up.
- Tokens **do not count** toward the 40-card minimum or the 3-copy limit. They are not in
  any deck or pool.
- **When a Token leaves the Board for any reason it is removed from the Game.** It never
  reaches the Graveyard, so it can never be returned by Recursion.

> That last rule is load-bearing. It is what stops a Recursion engine from turning free
> bodies into an unbounded loop (**P3**).

## Tactic

Action/spell cards played from the Hand. Requires a caster — see [Command System](04-command-system.md).

- **Standard Tactic** — playable only as a standard Phase 2 action. **Cannot be played during combat.**
- **Combat Tactic** — the only Tactics fast enough to be played during the **Reaction Window**
  of a Combat Wave.

## Attachment

Permanent buffs or gear. Played face-up in the **Tactic Zone** behind your Characters.

**Fragility rule:** if the Character an Attachment is equipped to is Murdered, or leaves the
Board for **any** reason (including card effects), the Attachment is immediately destroyed and
sent to the Graveyard.

- **Commandment** — a sub-type of Attachment unique to the Mobb 134 crew.

## Arena

An Arena edits the rules of the table. It is the only card type whose text changes what is
legal rather than what happens.

- **Playing one** is a standard Phase 2 action. It goes face-up into your **Tactic Zone**.
- **One per player.** Playing a second Arena destroys your own first one. Both players may
  have an Arena active at the same time, and both are in effect simultaneously.
- **Arena text is symmetric.** An Arena's rule applies **equally to both players**. An Arena
  may never say "your Characters" or "the opponent's Characters."
- **Arenas are objects, not auras.** Any effect that destroys an Attachment can destroy an
  Arena. It goes to its owner's Graveyard.
- **Conflicting Arenas both apply.** If two active Arenas modify the same cost, apply both.
  If one forbids what another requires, the **forbidding** Arena wins.

> **Why symmetric.** A one-sided rule edit is a passive lock with no off-switch (**P2**). A
> symmetric one is a puzzle: the Arena is only good because *your* deck was built to like the
> rule and theirs wasn't. The asymmetry comes from deckbuilding, not from the card. It also
> means an Arena is never dead — the opponent can play around it, and can blow it up.

*(Resolves OQ-07.)*
