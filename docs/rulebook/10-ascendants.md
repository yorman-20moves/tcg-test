# 10. Ascendants & Leveling Up

Ascendants are your ultimate win conditions. They live in the **VIP Area** and are summoned like
standard Characters, but are much more powerful.

## The Level-Up

Every Ascendant has a specific **Level-Up condition** printed on its card.

## The Flip

When the condition is met, the card is physically flipped to reveal its ultimate form and stats.

## Descent

An ability may instruct an Ascendant to **Descend** — flip back to its base side. The ascended
form is not permanent; it is something a card can spend.

- **Only a card's own text may cause it to Descend.** No effect may force an *opponent's*
  Ascendant to Descend.
- **Permanent damage carries across the flip.** If carried damage meets or exceeds the base side's
  printed Health, the Character is set to **1** and is **not Murdered** — the
  [Safety Net](08-round-structure.md#phase-3-the-end-step) covers Descent, because a flip is not
  active damage.
- **Statuses and Counters persist.**
- **Buffs printed on the ascended side are lost.** Buffs applied by other cards remain.
- **The Level-Up condition becomes live again.** A Descended Ascendant may meet its condition and
  re-ascend. Descent is not once per Game unless the card says so.

> **Why an opponent can never force it.** A forced Descent is removal — it deletes the most
> expensive thing a deck can build, for a fraction of what [Hard Removal](12-keywords.md) costs,
> and it would invalidate every Level-Up condition in the game at once. Descent is a **cost a card
> pays**, never a weapon pointed at somebody else.

## Permadeath

If an Ascendant is Murdered on the Board it goes to the Graveyard. **It does not return to the
VIP Area.**

---

## Design constraints on Ascendants

These are enforced by the rubric and the balance engine, not by the printed rules — but they
are why the pool looks the way it does.

- An Ascendant gets **+3 points of budget** over a Descendant of the same cost
  (see [`../../tools/balance.py`](../../tools/balance.py)).
- The Level-Up condition must be something the card's *own base side actively pursues*. A
  condition that happens to you rather than because of you fails lore gate **L7**.
- **Currently the ascended side costs zero budget.** See open question **OQ-04** — this is the
  single largest known hole in the balance system. **Descent** is the first mechanism that gives it
  a price: an ascended side a card can spend is an ascended side that cost something. Priced as the
  `ascension_spent` credit in [`../../data/plan-credits.yaml`](../../data/plan-credits.yaml).
