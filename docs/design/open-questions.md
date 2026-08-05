# Open Questions — Design Audit

Everything below was found by reading the rulebook against the card database and the point
tables. Each item is a **structural** problem, not a tuning problem — you can't fix any of them
by changing a number on one card.

**This file is the backlog.** It's the first thing to run the rubrics against.

Status: `OPEN` · `DECIDED` (move the reasoning to `decisions.md`) · `WONTFIX`

---

## OQ-01 · The pool is 100% Ascendants — `OPEN` — **severity: critical**

All 31 designed cards are Ascendants. The rulebook caps Ascendants at **5 per 40-card pool**.

That means **~88% of a legal deck consists of card types that do not exist**: zero Descendants,
zero Tactics, zero Attachments, zero Arenas.

This isn't a small gap — it means the game as documented has never been playable, and every
balance judgment made so far was made against an imaginary format. An Ascendant is balanced
*relative to the Descendants it fights*, and there aren't any.

**It also explains a second symptom:** eight of the level-up conditions reference "Characters"
generically. With only Ascendants in the world, those conditions are far harder to meet than
they'd be in a real board state, so they read as balanced when they aren't.

**Recommended next move.** Before designing another Ascendant, build **one complete 40-card
pool**: roughly 24 Descendants, 8 Tactics, 3 Attachments, 5 Ascendants. Use existing Ascendants
as the reference power ceiling and design *down*. This is the single highest-value thing to do
next and everything else on this list gets easier once it exists.

---

## OQ-02 · The Influence win condition has no support — `OPEN` — **severity: critical**

The rulebook prints a win condition: accumulate 30 Influence Points.

- No card in the pool grants a defined amount of Influence.
- Exactly one keyword references it — **Martyr**: *"grants massive Influence Points when
  Murdered."* "Massive" is not a number.
- There is no rule for where Influence is tracked, whether it persists across Games, or whether
  it can be removed.

A printed win condition nobody can pursue is a lie in the rulebook. Either build it — which
means giving the Icons a real Influence engine, probably 8–12 cards — or cut it to a single
faction mechanic. Gameplay rubric **S1**.

---

## OQ-03 · No deck-out loss, so no clock — `OPEN` — **severity: high**

If your deck is empty you simply don't draw. There's no loss condition. Combined with:
- Attacks costing Energy (so attacking is *expensive*),
- Protector, Pacifier and Instigator all discouraging attacks,
- Permanent damage making trades costly,

...two defensive boards have no terminating condition other than someone conceding. Concession
is listed as a win condition, which papers over the problem: **the game has no clock.**

Options: deck-out loss; an escalating per-Round Life Point drain; a Round limit with Life Points
as tiebreak. Gameplay rubric **S3**.

---

## OQ-04 · The level-up side is free — `OPEN` — **severity: critical**

The budget formula charges **nothing** for the ascended side. The spreadsheet even labels it
`[Free]`. Every Ascendant is getting an entire second card of effects at no cost.

Measured, with `python tools/balance.py --charge-ascended`:

| | Base only (shipped rule) | Ascended charged |
|---|---:|---:|
| Cards outside ±0 | 9 of 25 | **25 of 25** |
| Worst offender | RoaR, +10 | Julito & RoaR, **+15** |
| Median overage | 0 | **+8** |

Free ascended sides ranging from 2 to 13 points. **Enzo pays 13 points of budget for his base
side and gets 13 more for free.**

Why it matters beyond fairness: with the ascended side unpriced, there is no design pressure to
make level-ups *interesting* rather than just *bigger*, which is exactly what lore gate **L7**
and dimension **D6** are trying to prevent. The economics and the storytelling are failing
together.

**Proposal, superseded and improved.** The original proposal was a flat "base budget + 50%"
ceiling on the ascended side. The Score replaces it with something better: the ascended side is
charged against the **earned Ceiling**, which the card can raise by paying for its level-up in
setup, telegraph, and interaction windows.

This is the right shape, because the level-up condition *is* the setup, and the two-Round wait
*is* the telegraph. Under the old rule an Ascendant's second side was free and therefore
unpriced; under The Score it is paid for by exactly the thing that makes it interesting.
See [balance-philosophy.md](balance-philosophy.md) §4.

---

## OQ-05 · Half the stat system is dormant — `OPEN` — **severity: high**

Every Character has PA / PH / MA / MH. But MA is explicitly *"not used in standard combat unless
stated,"* and exactly one keyword (**Troll**) converts an attack to MA-vs-MH.

Consequence: **MA is a near-dead stat that every card still pays budget points for.** Vince has
5 MA and 5 MH — 10 of his 16 budget points sunk into an axis that barely resolves. Cards with
high MA are silently overcosted and cards that dump MA to 0 (Moammar) are silently efficient.

This is also the clearest Overthinker identity in the game going unused: they *"bypass the body
entirely and attack your psyche."* That is the printed faction fantasy, and the mechanics don't
deliver it.

Either build the mental-combat game (more Troll-likes, MA-based removal, Shattered payoffs, an
"attack with MA" declaration option in the Combat Wave) or collapse to two stats. Gameplay
rubric **S6**.

---

## OQ-06 · The Icons don't exist — `OPEN` — **severity: critical**

All five Icons cards (Any, Fefe, Jocelyn, Myra, Rosula) are **name-only stubs**: no cost, no
stats, no rules text, no crew. They're the only cards with no crew assigned at all.

**They do, however, have finished artwork** — `Any Nunez.jpg`, `Doña Fefa.jpg`, `joselyn.jpg`,
`Mayra De Los Angeles.jpg` and `Matria Rosula.jpg`, now filed under `art/characters/icons/`.
That changes the shape of this problem: the art exists and the names exist, so what's missing is
the *design*, not the *intent*. Somebody knew who these five were.

The Icons are simultaneously:
- the only faction with no playable cards,
- the owner of the only unsupported win condition (OQ-02),
- the only faction whose lore describes an *institution* rather than a personality,
- the holder of the most alarming keyword (Pacifier, OQ-09).

These are one problem, not four. Deciding what the Icons *are* resolves all of it. See lore
rubric §5, world question 2.

Worth noting: the five names read as a different kind of figure than the rest of the roster —
which may be exactly right, and may be the most interesting thing in the game. It's also the
place where lore gate **L2** matters most, because these are the cards most likely to be about
people who aren't sitting at the table.

---

## OQ-07 · Arenas are referenced but undefined — `DECIDED` — **severity: medium**

**Resolved 2026-08-05.** See [D-007](decisions.md). An Arena edits the RULES, symmetrically for
both players; one per player; destroyable as an object. Rules in
[§5 Card Types](../rulebook/05-card-types.md#arena). Priced as `Arena Rule Edit (Minor|Major)`.
This also gives the **Landlord** Job something to do.

*Original:* Arenas were named in §4 (Command System) and had an art folder but no rules — how
many can be active, whether both players can have one, whether they're owned or shared, how
they leave play, whether they're Attachments. Arenas are the obvious home for the *place* half
of the worldbuilding — the bar, the park, the block. Lore rubric **WG2** and dimension **D7**
both want them to exist.

---

## OQ-08 · Exhausted has two contradictory definitions — `OPEN` — **severity: medium**

| Source | Definition |
|---|---|
| Rulebook §11 | Costs an **additional 1 Energy** to declare them as an attacker |
| Elements sheet | Attack power (physical and mental) is **halved** |

These are entirely different effects — one is a tax, the other is a debuff — and they'd be
priced differently. The rulebook is authoritative for now and `data/status-effects.yaml` carries
a warning. Pick one.

Same class of problem: the Elements sheet has a sixth unnamed status with the note
*"tate qieto - low attack but lowers your attack"* — an undesigned idea sitting in a data file.

---

## OQ-09 · Pacifier may be un-gateable — `DECIDED` — **severity: high**

**Pacifier** (Icons, 5 points): *"An aura that completely prevents the declaration of a Combat
Wave as long as they are on the Board."*

This shuts off the game's primary damage mechanism unconditionally. To remove it you must kill
the Character — but you can't attack, so you need non-combat removal. **The Warmongers have no
printed non-combat removal at all.**

A Warmonger player facing a Pacifier they can't kill has no game. That's a clean failure of
gameplay gate **G7** (answerability) and a likely failure of **G9** (losing to it feels like
being robbed, not outplayed).

Compare the pricing: Pacifier costs 5, Mass Removal costs 8. Turning combat off permanently is
priced below destroying a board once.

**Fixes worth considering:** make it cost Energy each Round to maintain; let attackers pay a tax
to attack anyway; limit it to one Combat Wave per Round rather than all of them; or make the
Pacifier itself attackable as an exception to its own aura — which is also the better story.

**Resolved by prohibition P2** (see [balance-philosophy.md](balance-philosophy.md) §5): an effect
that prevents an opponent action must be an activation, or carry an off-switch. Pacifier as
printed is prohibited. Any of the four repairs above satisfies P2 — pick one. The precedent is
Kashtira 2023, where passive floodgates gave a format with fifteen answers per deck an
*effective* answer density of zero, because hand traps answer activations and floodgates never
activate.

---

## OQ-10 · Six undefined rules terms — `OPEN` — **severity: medium**

Used in card text or the effect table, defined nowhere: **Sacrifice**, **Hexproof /
Untargetable**, **Spell Shield**, **Taxing**, **Recursion**, **Arena**.

Each is a gate **G2** failure the moment a card printing it hits the table. Cheap to fix — one
glossary pass — and it prevents rules arguments in the middle of a game.

---

## OQ-11 · Infiltrator is priced as a drawback — `OPEN` — **severity: medium**

**Infiltrator** is the only negative entry in the point table (−2): you're *paid* budget for
handing the opponent a body.

But read what it does: it sits on the opponent's board, they can't activate its abilities, their
other Characters **can't attack it**, and it *"exists to provide massive passive benefits to its
original owner just by surviving behind enemy lines."*

An untargetable permanent that generates value for you every Round is not obviously a drawback.
It might be the strongest keyword in the game, priced at −2.

Angel, The Smiling Saboteur is the test case: he's rated "Perfectly Balanced" partly *because*
Infiltrator refunded him 2 points.

---

## OQ-12 · Six crews, no crew documents — `OPEN` — **severity: medium**

Latin Kings, Mobb 134, Shea's, Pimp Juice, PWNED, Fury Park. Five cards each, except Fury Park
with one. **None has a documented territory, origin, code, or relationship to the others.** Only
Mobb 134 has a mechanical signature (Commandments).

The faction × crew split is the best structural idea in the design — crews genuinely span
factions, which is what makes them read as real social groups rather than color-coded teams.
It's currently carried entirely by a spreadsheet column.

Five crew documents would immediately improve all 31 existing cards without touching one of
them. Lore rubric §4.

---

## OQ-13 · ~600 MB of images in git without LFS — `OPEN` — **severity: low, rising**

The repo has ~100 image files averaging 2.7 MB, committed directly. Every future revision of a
card's art adds another full copy to history permanently.

At the current rate this becomes painful to clone within a year. `git lfs migrate` gets harder
the longer you wait. Not urgent this month; don't let it reach next year.

---

## OQ-14 · The Command System has no rubber band — `OPEN` — **severity: high**

Section 4 states it outright: *"a wiped board means you cannot cast Tactics to save yourself!"*

That is textbook **slippery slope** — falling behind causes you to fall further behind — with no
perpetual-comeback mechanism anywhere. The player who most needs a Tactic is structurally
forbidden from casting one.

**The fix is proven and cheap.** Print a cycle of Tactics carrying a rubber-band clause, lifted
near-verbatim from Yu-Gi-Oh's Infinite Impermanence and Evenly Matched:

> *"If you control no Characters, you may play this card without declaring a caster."*

Dead when you're winning, live when you're losing. Costs the format nothing and converts an
unwinnable position into a hard one. Highest-value single rules addition available.

See [balance-philosophy.md](balance-philosophy.md) §7.1.

---

## OQ-15 · No universal interaction layer — `OPEN` — **severity: medium**

Phase 2's alternating actions give the opponent a window between every card — that's the game's
best structural asset. But **Trigger Abilities cost no action** and Passive Abilities are always
on, so a chain of triggers resolves inside a single action with no window at all. That is
exactly where a first-turn kill would eventually live (cf. Firewall Dragon).

Two additions, both in [balance-philosophy.md](balance-philosophy.md) §7.2: a small cycle of
Combat Tactics playable from hand with no board requirement (your hand traps), and a Nibiru
clause that taxes the *length* of a plan rather than banning it.

---

## Suggested order

The dependencies matter more than the severities.

1. **OQ-06 (Icons) + OQ-02 (Influence)** — one decision, unblocks a faction and a win condition
2. **OQ-01 (build a real card pool)** — the biggest single unlock; everything gets testable
3. **OQ-04 (price the ascended side)** — do it before designing more Ascendants, not after
4. **OQ-09 + OQ-11 (Pacifier, Infiltrator)** — two keywords likely mispriced
5. **OQ-05 (mental combat)** — decide whether MA lives or dies
6. **OQ-03 (the clock)** — needs a real pool to test against
7. **OQ-07, OQ-08, OQ-10, OQ-12** — cleanup and lore, cheap, do them between the big ones
8. **OQ-13** — before it's expensive
