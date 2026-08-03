# 10. Ascendants & Leveling Up

Ascendants are your ultimate win conditions. They live in the **VIP Area** and are summoned like
standard Characters, but are much more powerful.

## The Level-Up

Every Ascendant has a specific **Level-Up condition** printed on its card.

## The Flip

When the condition is met, the card is physically flipped to reveal its ultimate form and stats.

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
  single largest known hole in the balance system.
