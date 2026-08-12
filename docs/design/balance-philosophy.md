# How We Balance

Balance happens at **three levels**, and a card can be perfect at one and broken at another.

> **Level 1 — The Card.** Is this one card allowed to do what it does?
> **Level 2 — The Crew.** Does this crew have one coherent way to win, expressed in varied ways?
> **Level 3 — The Faction.** Does this faction only reach for tools its lore says it owns?

Most of this document is Level 1, because that's where the arithmetic lives. But Levels 2 and 3
are what make the game *feel* like something, and a card that passes Level 1 while breaking
Level 3 is still a broken card.

---

# Part One — What a Credit Actually Is

This needs to be said plainly, because it's the thing that causes confusion.

**A Credit is not power. A Credit is permission.**

Two completely different quantities:

> **IMPACT** — how much the card actually does. Stats, keywords, effects. This is the card's
> power level. Higher Impact = the card matters more in a game.
>
> **ALLOWANCE** — how much Impact this card is *permitted* to have.

You earn Allowance by paying Credits. A Credit is one point of permission, bought with something
other than Energy — setup, time, sacrifice, risk.

**Balance at Level 1 is one sentence:** *Impact must not exceed Allowance.*

So when you see a card with "40 headroom," that does **not** mean the card is weak. It means the
card has paid for more power than it currently uses. It could be scarier. Whether it *should* be
is your call.

And when you see a card "over by 30," that means it is doing more than it has paid for. That
card is too strong — not because 30 is a big number, but because nothing in its design bought
that power.

---

# Part Two — Level 1: The Card

## The shape of it

```
   BASE          set by the Energy cost — (cost × 3) + 1 + 3 if Ascendant
 + CREDITS       everything the card asks of you besides Energy
 = ALLOWANCE     the power it has earned

   REACH         how many of the four factions can answer this card at all
 → CAP           Reach sets a hard ceiling as a multiple of BASE

   CEILING       whichever is smaller: ALLOWANCE or CAP
   IMPACT        what the card actually does
```

**Credits earn you power. Reach decides whether you're allowed to collect it.**

That separation is the important part. A card with an enormous setup cost that only one faction
can answer earns a lot and is allowed almost none of it. A card anyone can answer gets to keep
everything it earned.

## Reach — the cap

| Factions that can answer it | Cap |
|---|---|
| **All four** | Base × 3 |
| **Three** | Base × 2 |
| **Two** | Base × 1.5 |
| **One** | Base × 1 — *your setup earns you nothing* |
| **None** | Not printable |

**Reach is not "how many windows does this card have."** You do not need a weakness at every
moment. You need *some* moment where each faction, using tools its lore lets it own, can do
something.

A card with exactly one window that all four factions can use has Reach 4. A card with five
windows that all require a Counterspell has Reach 1, because only the Overthinkers counter.

## The three tests — is this cost real?

This is the part that was wrong before, and it's why numbers came out too generous. **A cost only
counts if it actually costs you something.** Three tests, and a cost has to survive all three.

### ① The Bite Test — does it make you worse at your job?

If paying it is *what the card wants you to do anyway*, it isn't a cost.

A Warmonger card that requires "the opponent's board is empty" is asking a Warmonger deck to do
the thing it already does. That's not a price. That's a Tuesday.

**Full credit** if paying it competes with your plan. **Half** if it's neutral. **None** if it
advances your plan.

### ② The Timing Test — when do you pay?

| When you pay | Credit |
|---|---|
| **Before** the payoff, while it can still fail | Full |
| **At** the moment of payoff | Half |
| **After** the payoff resolves | Little or none |

A card that kills itself *after* winning the game has not paid anything. You don't need him
anymore. The cost lands on a player who has already won.

### ③ The Enabler Test — does something else hand it to you free?

Look at the rest of the crew, then the rest of the faction. **If another card produces this
condition as a side effect, the credit is zero.**

This is the test that was missing entirely, and it's the most important one, because crews are
built to work together. A cost that one of your own crewmates removes was never a cost.

## What you can pay with

| | Credits | |
|---|---:|---|
| Each card permanently spent | **+3** | your table prices "draw 1" at 3 |
| Each Energy paid above the cost | **+3** | your table prices "gain 1 Energy" at 3 |
| Each 2 Life Points paid | **+1** | your table prices 1 damage at 1 |
| Each of your Characters sacrificed | **+5** | your table prices "destroy a Character" at 5 |
| An Ascendant giving up its own ascended side | **+4** | below sacrificing a Character (5) — you keep the body |
| Each of your Attachments consumed | **+2** | |
| Each Character required on board | **+2** | |
| Each Attachment required in play | **+2** | |
| A board state you must engineer | **+4** | |
| Each full Round of warning | **+5** | a draw (3) plus a Round of tempo |
| Each opponent action handed over | **+2** | |
| Each Energy or card given to the opponent | **+3** | *if it's permanent; +1 if temporary* |
| Once per Game instead of once per Round | **+5** | |

Then apply the three tests to every line. Most cards lose about half their raw credits to the
tests, and that is the system working.

## Pricing a random effect

Some abilities roll a d6 and do a different thing on each result. One rule, in two halves:

> **A random effect is priced at its most expensive outcome. A bad outcome earns no credit.**

An ability with four branches is **one** effect costing whatever its biggest branch costs — not the
sum of all four, and not their average.

**Why not the average.** Averaging makes variance a *discount*, and a discount on variance means
the most swingy card in the game is also the most point-efficient. Design a few cards under that
rule and the whole set drifts toward slot machines, because rolling dice is the cheapest way to buy
impact. Two places your own tables already reject averaging:

- `data/effects.yaml` has never priced by frequency. `Direct Damage/Heal 4` costs 4 whether you
  draw the card in game one or never.
- **Range 3** charges 4 for the ×3 shot, not the average of aiming zero, one or two Rounds. A
  variable outcome priced at its ceiling is already the precedent in the file.

**Why the second half matters as much.** If a branch *hurts* you — Ruvi's Banana Peel deals him a
point of permanent MH damage on a 1 or 2 — it earns **no** credit. Crediting a one-in-three downside
while charging for the best upside would price the same variance twice, in opposite directions, and
hand back most of what the first half just collected. **Variance is a choice the controller makes,
not a cost the card pays.**

The consequence for the designer is clean: a die table is not a way to get more card for your
points. It is a way to make the same points feel different every time you draw them, which is a
[D9 table-theatre](../rubrics/gameplay-rubric.md) win and nothing else.

---

# Part Three — Level 2: The Crew

**A crew is a plan.** Faction is *how you fight*; crew is *what you're trying to do*.

Every crew needs one written sentence: **how does this crew win a game?** Not their vibe — their
plan. Everything about them should point at it.

## The two rules

### Rule 1 — One plan, written down

If you can't say a crew's plan in a sentence, the crew doesn't have one, and its cards will drift
into being five unrelated good cards. A player should be able to pick up a crew and understand
what they're supposed to be doing.

**The exception, and it's a real one:** a crew whose *lore* is that they're not coordinated
doesn't need a unified plan — but then that has to be their plan. "Nobody here is on the same
page and it somehow works" is a legitimate strategy, and it should be mechanically true, not just
flavor. If PWNED are chaos, their cards should genuinely produce chaos, including for their own
player.

### Rule 2 — One plan, many expressions

Here's the rule that stops a crew from being boring: **each card must advance the plan by a
different mechanism.**

Five cards that all say "gain Influence" is not a crew, it's one card printed five times. Five
cards that each reach the same destination by a different road — one through combat, one through
the economy, one through the opponent's hand, one by surviving, one by sacrificing — that's a
crew you can build decks out of.

**The test:** cover the names. Can you still tell the five cards apart by what they *do*? If two
of them collapse into each other, one needs rewriting.

## The crew sheet

Every crew needs this filled in. **These are drafts — the lore is yours, and the plan should
follow the lore, not the other way around.** But the slots are the point.

| Crew | Proposed plan | Signature | Status |
|---|---|---|---|
| **Latin Kings** | Hierarchy — the Crowns empower each other; you win by getting the command structure intact onto the board | Ranked Crowns (1st–5th); "La Familia" buffs all allied Latin Kings | Strongly implied by the cards already |
| **Mobb 134** | Law — accumulate Commandments, then execute all of them at once | **Commandments**, an Attachment subtype nobody else has | Already mechanically real |
| **Pimp Juice** | Economy — control what the opponent has and what it costs them | Resource manipulation, persuasion, taking what's yours | Implied |
| **Shea's** | Attrition — everyone leaves the bar worse than they came in, including you | Damage that lands on both sides; the long night | Implied |
| **PWNED** | *Chaos?* — randomness, glitches, rules-breaking | Dice, item boxes, "you know this is just a game, right?" | **Needs your decision** — is this the uncoordinated crew? |
| **Fury Park** | *Unwritten* | — | **One card exists. Needs everything.** |

---

# Part Four — Level 3: The Faction

**A faction is a toolbox, and the lore says what's in it.**

Right now this level does not exist. Measured across the pool: **13 of 28 effect types are used
by more than one faction.** The Overthinkers use 16 different effect types including Mass
Removal, Hard Removal and Direct Damage 5. The Assholes have Counterspell on two cards, while
their own rulebook entry says *"they don't block; they evade."* Moammar is a Warmonger with
Searching (Tutors).

Nobody owns anything, so nobody feels like anything.

## The toolkits

Each faction **owns** some tools outright, **shares** some, and **can never have** others. Every
line traces to a sentence already printed in the rulebook.

### 🟥 Warmongers — *"they endure, they adapt, they break you"*

| | |
|---|---|
| **Owns** | Large permanent buffs · Multiple Attacks · damage that spills over · interception (Protector) · turning damage taken into power |
| **Shares** | Direct damage · Hard Removal — **but only through combat** · Stun |
| **Never** | Counterspell · Card Draw · Searching/Tutors · Hand Destruction · Energy manipulation · Untargetable · stealth |

*Their weakness is printed: "when a problem cannot be solved with fists." Everything in the Never
column is a problem that can't be solved with fists.*

**Current violation:** Moammar's tutor.

### 🟦 Overthinkers — *"they bypass the body entirely"*

| | |
|---|---|
| **Owns** | Counterspell · Card Draw · Searching/Tutors · MA-based attack · redirection · Untargetable · preventing attacks · information |
| **Shares** | Bounce · Status effects · Mass Removal — **only as a deep-setup payoff, never as a cheap Tactic** |
| **Never** | Large permanent buffs · Multiple Attacks · Healing · Energy generation |

*Their weakness is printed: "how long can a genius survive a street fight?" They must lose to
speed.*

### 🟩 Assholes — *"they don't block; they evade"*

| | |
|---|---|
| **Owns** | Energy theft and denial · Hand Destruction · Taxing · stealth (Prowler) · Infiltrator · evasion |
| **Shares** | Status effects · Bounce |
| **Never** | **Counterspell** · Healing · protecting anyone but themselves · Mass Removal · large permanent buffs |

*Their weakness is printed: "forced into a fair, head-on collision, do they have the spine?"
Countering is blocking. Blocking is a fair fight. They don't do it.*

**Current violation:** two cards with Counterspell.

### 🟨 Icons — *"they fight for the soul of the city"*

| | |
|---|---|
| **Owns** | Healing · Influence · Cleanse · prevention · protecting others · Recursion · gifting Energy (Sponsor) |
| **Shares** | Status immunity · Protection |
| **Never** | Direct damage to Life Points · Hand Destruction · stealth · Multiple Attacks |

*Their weakness is printed: "can a symbol actually bleed?" They win by lasting, never by killing.*

**Current state:** zero cards. This faction is a stub.

## The window map — where each faction attacks, and where it's blind

This is the part you were reaching for. **Windows are where a card's weakness shows.** You don't
need a weakness at every moment — you need factions that specialize in different moments.

| | W1 Before it starts | W2 While it builds | W3 The moment it lands | W4 After it lands | W5 Race it |
|---|---|---|---|---|---|
| 🟥 **Warmongers** | blind | **STRONG** | weak *(Protector only)* | blind | **STRONG** |
| 🟦 **Overthinkers** | **STRONG** | weak | **STRONG** | weak | blind |
| 🟩 **Assholes** | **STRONG** | **blind** *(their printed weakness)* | weak | **STRONG** | weak |
| 🟨 **Icons** | blind | **STRONG** | blind | **STRONG** | blind |

Read it across and you get each faction's personality. Read it *down* and you get the health of
the game:

| Window | Who covers it | |
|---|---|---|
| W1 Before | Overthinkers, Assholes | fine |
| W2 While | Warmongers, Icons | fine |
| **W3 The moment** | **Overthinkers only** | ⚠️ **thin** |
| W4 After | Assholes, Icons | fine |
| **W5 Race** | **Warmongers only** | ⚠️ **thin** |

Two windows are covered by one faction each. That's a real gap and it's why cards that can only
be answered in the Reaction Window keep coming out Blue-mandatory.

## The accessibility rule

**Narrow, but cheap.** A faction should be nearly untouchable in the windows it's strong in — and
the way you beat it should be **a common card, not a rare one.**

You have to hit them in the right place. But once you know where, the tool should be something a
normal deck already runs. That's the difference between a crew that's *hard* and a crew that's
*unfair*.

---

# Part Five — The Four Things You Can Never Do

No Allowance buys past these.

**① The payoff can't restart itself.** If pulling it off makes the next one easier, it isn't a
plan, it's an engine that never stops.

**② You can't just switch the opponent off.** Anything that stops your opponent doing something
must be an activation they can respond to, or carry an off-switch — a cost to maintain, a time
limit, or a way to attack it. *This is why Pacifier as written isn't legal: it shuts off Combat
Waves, isn't an activation, and to remove it you'd have to attack it — which it's preventing.*

**③ Nothing repeats forever.** Hard once per Round on anything repeatable, unless it eats a
resource each time.

**④ Nothing is cheap and broad and unstoppable at once.** Pick two.

**The test that catches everything:** *if your opponent knows exactly what's coming, is there
anything at all they can do?* If no, it doesn't get printed, whatever the ledger says.

---

# Part Six — Why Moammar Had So Much Headroom

Your instinct was right. He shouldn't have. Here's exactly what went wrong.

## What he was charged before

| | |
|---|---:|
| Base | 19 |
| A board state you must engineer *(opponent has zero cards)* | +4 |
| He destroys himself | +5 |
| Once per Game | +5 |
| Old ceiling *(after a ×2.25 window multiplier)* | **74** |

## What the three tests do to that

**The board state — fails the Enabler Test. → 0**

Dre's ascended text: *"immediately destroy every Character, Tactic, and Attachment on the
opponent's Board."*

Moammar's level-up: *"the exact moment the opponent has zero cards on their Board (Characters,
Tactics, or Attachments)."*

**Dre's payoff is Moammar's condition, word for word — and they are both Mobb 134.** In any deck
running Dre, Moammar's setup costs nothing. I charged him for work his own crewmate does.

*(It also fails the Bite Test independently: clearing the opponent's board is what a Warmonger
deck already does.)*

**He destroys himself — fails the Timing Test. → 0**

He dies at the End Step, *after* the punch. The punch adds his opponent's entire Life Point total
to his attack. If it connects, the game is over. **A cost you pay after winning is not a cost.**

**Once per Game — fails the Bite Test. → 0**

Once is all he needs. A restriction that never restricts you isn't a restriction.

## What he actually is

| | |
|---|---:|
| Base | 19 |
| Credits, after the tests | **0** |
| **Allowance** | **19** |
| Reach — all four factions can answer him | Cap = 19 × 3 = 57 |
| **Ceiling** | **19** |
| **Impact** — 19 base, plus an ascended side worth up to +30 PA | **49** |
| | **OVER BY 30** |

> **The workbench will show a smaller number** — around 24, i.e. over by 5. That's because his
> ascended side is currently *logged* as "Permanent Buff 5," worth 5 points, when what it does is
> add the opponent's whole Life Point total to his attack. The effect table simply has no entry
> bigger than 5, so there is nowhere to record what he really does. The tool is right about the
> arithmetic and wrong about the input. **Fixing the effect table's ceiling is a separate job
> from fixing the balance system**, and it affects every card whose text scales rather than
> stating a fixed number.

**That matches what you felt.** He's not a card with room to grow. He's a card doing thirty
points more than anything in his design paid for.

## What to do about it

Three options, and the second is the interesting one.

**Cap the payoff.** *"+PA equal to half the opponent's Life Points"* instead of all of it. Now
it's a haymaker, not a guaranteed kill, and the opponent's remaining life is a real variable.

**Buy the condition back — make it hard for Mobb 134 specifically.** Right now Dre gives it away.
Change the level-up to something Dre *doesn't* produce: *"the opponent has no Characters and you
control no other Characters."* Now he's the last man standing, which is a far better story for a
man who dies from his own punch — and Dre can't hand it to him.

**Make it a real gamble.** *"Declare the punch during Phase 2. It resolves at the End Step."* One
full round where everyone can see it coming and act. That opens a window, and the drama goes up,
not down.

Any of these brings Impact under Ceiling. **The second one also fixes the crew.**

---

# Part Seven — The Other Two

## Corazon — this one was right all along

| | |
|---|---:|
| Base *(cost 3)* | 13 |
| Hands the opponent 3 Energy — but **temporary**, and feeding them is his own plan, so the Bite Test cuts it | +3 |
| Two Rounds of warning, publicly, on the table — this genuinely bites | +10 |
| **Allowance** | **26** |
| Reach — all four can answer, and the answer is free *(spend your Energy)* | Cap 39 |
| **Ceiling** | **26** |
| **Impact** | **25** |
| | **1 headroom — almost exactly right** |

He's the best-balanced card in your pool and he got there by accident, which is worth knowing.
Note what the Bite Test did: giving the opponent Energy looks like a huge cost, but his ascended
side *punishes them for having Energy*. The cost is the plan, so it earns much less than it
appears to. He's still fine, because the two Rounds of warning are real.

**His counterplay is a decision, not a card.** The penalty scales with their *unused* Energy, so
the answer is "stop hoarding." Every faction can do it, it costs nothing, and it teaches the
player something. Aim for more of this.

## Dre — the ledger tells you what to change

| | |
|---|---:|
| Base *(cost 5)* | 19 |
| Seven Commandments in play — real cards, but they work for you every End Step, so half credit | +10 |
| Seven surrendered actions — your opponent really does get seven free turns | +14 |
| **Allowance** | **43** |
| Reach — all four can kill Dre or the bodies carrying the Commandments | Cap 57 |
| **Ceiling** | **43** |
| **Impact** | **33** |
| | **10 headroom** |

He's fine, and he's allowed to be bigger. But the more useful finding is a gap: **his payoff
fires as a Trigger Ability in Phase 3, which is not a Reaction Window.** At the moment the board
is erased, nobody can respond. Many Rounds of warning, zero seconds of reaction.

**Announce the Verdict in Phase 2, resolve it in Phase 3.** Costs one more action, opens the
moment, and it's a better scene — he announces judgment and everyone gets one last chance.

---

# Part Eight — Using It

## Designing a card

1. Build the version you actually want. Don't pre-shrink it.
2. List what it asks of you. **Run all three tests on every line.** Most costs lose half.
3. Ask **Reach**: can each of the four factions do *something*, using tools its toolkit allows?
4. Check Impact against Ceiling.

If it's over: cap the payoff, make the setup genuinely expensive, or open another faction's
window. The third is usually the best card.

## Designing a crew

Write the plan sentence first. Then, for each card, say **which different road it takes to that
destination.** If two cards take the same road, rewrite one.

## Designing a faction

Stay in the toolbox. If a card needs a tool the faction doesn't own, either it's the wrong
faction for that card, or you're deliberately making an exception — and an exception should be
rare, deliberate, and written down in [`decisions.md`](decisions.md).

## Tuning the numbers

Expect the Credit values to move. Two things to know: change **one at a time**, and expect only
**two or three settings to matter** — these knobs are coarse, and the step between "no effect"
and "too much" is usually a single point.
