# 8. Round Structure (The Ping-Pong System)

The game is played in continuous Rounds. An **Initiative Token** dictates who takes the first
action in Phase 2. The first Round's Initiative is decided by a coin flip.

---

## Phase 1: The Refresh (Simultaneous)

Both players execute these steps at the same time.

1. **Draw** — both players draw 1 card.
   *If your Main Deck is empty you simply do not draw. There is no automatic loss for running
   out of cards; you must win with what remains on the board and in hand, or concede.*
2. **Un-tap** — turn all horizontal **Used** cards in your Resource Row back to vertical. See
   [§7 Used and Unused Energy](07-economy.md#used-and-unused-energy).
3. **The Blind Commit** — both players take **0, 1, 2, or 3** cards from Hand and place them
   face-down on the table. Once both players are **Locked**, the cards are flipped
   simultaneously into their Resource Rows, raising maximum Energy capacity.

> **Open question (OQ-03):** No deck-out loss means a Game between two defensive boards has no
> terminating condition other than concession.

---

## Phase 2: The Action Phase (Alternating)

The player holding the Initiative Token takes **one action**. Then the opponent takes one
action. This alternates continuously.

An action is exactly ONE of:

- Play a **Descendant** from your Hand to the Board.
- Summon an **Ascendant** from the VIP Area.
- Play a **Standard Tactic** or an **Attachment**.
- Activate a **Standard Ability**.
- Declare a **Combat Wave** — *limit once per Round per player*.

**Passing:** if you have no action, declare a **Pass**. Your opponent may continue taking single
actions until they also Pass. When both players Pass consecutively, the phase ends.

### Additional Actions

Some effects grant a player an **additional action**. This is the most powerful thing a card
can do, because the alternating single action is the game's fundamental unit — it is what every
cost, every telegraph and every interaction window is measured in.

1. An additional action is taken **immediately**, before Initiative passes to the opponent.
2. **A player may never take more than two consecutive actions in a Phase**, no matter how many
   additional actions they are granted. Surplus additional actions are **lost**, not banked.
3. Granting an additional action to a specific Character grants it to that Character only. If
   that Character cannot act, the action is lost.

> **Why the hard cap.** Rule 2 is not a balance dial, it is a structural guarantee. It makes an
> unbounded action chain **impossible by the rules** rather than merely expensive, which is a
> far stronger version of prohibition **P3**. Two consecutive actions is a real, swingy,
> game-deciding thing. Three is a different game.
>
> Note the failure mode this creates on purpose: pointing an additional action at the wrong
> Character is strictly worse than not having it. That is a decision, not just power.

---

## Phase 3: The End Step

1. All temporary buffs/debuffs and temporary Energy expire.
2. **The Safety Net Rule** — if a temporary Health buff (PH or MH) expires and leaves a
   Character at 0 Health, they **do not die**. Their Health is immediately set to 1. A Character
   can only be Murdered by active damage or effects, never by a buff wearing off.
3. The Initiative Token is physically handed to the other player.
