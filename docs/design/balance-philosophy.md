# Balance Philosophy — The Score

> **The design goal, in your words:** crazy techniques and huge plays should be *possible*;
> everything should have an appropriate cost — setup, time, matchup — rather than just an energy
> cost; a big plan that works should pay off big; and there must always be counterplay.
>
> **The verdict:** the current point system cannot do this. Not "discourages it" — cannot
> represent it. This document proves that arithmetically, then replaces the system.

---

## Part 1 — Why the current system can't do what you want

Today's rule is one line:

```
spent = stats + keyword points + effect points     must equal     budget = (cost × 3) + 1 + 3
```

Three structural facts follow, and all three are fatal to your stated goal.

### 1.1 It is additive, so combo is not merely discouraged — it is unrepresentable

There is no term in that formula that references another card, a prior round, a board state, or
a condition. The value of a card is the sum of its own parts, evaluated in isolation, forever.

Melissa DeTora's definition of a combo is *"cards that interact in a way that's significantly
stronger than the sum of their parts."* Your formula's only operation **is** the sum of the
parts. A system whose sole operation is addition cannot express superlinearity. Every card you
design will be worth exactly what it looks like, alone, on an empty board.

That is the whole of it. The rest is detail.

### 1.2 It has no time axis, so "setup cost" is invisible

Setup, telegraph, matchup narrowness, and risk are not variables in the equation. There is
nowhere to put them. A card that says *"deal 5 damage"* and a card that says *"if you have
controlled four Characters for two consecutive Rounds and sacrifice them all, deal 5 damage"*
score **identically**. The second card is strictly worse and the system says they're the same.

So the system doesn't just fail to reward setup — it actively taxes it. Every condition you add
is free power you gave away.

### 1.3 The ceiling is arithmetically low. Here is the actual number.

Run the numbers on your own tables:

| Cost | Budget | Biggest single effect you can afford | Points left for all four stats |
|---:|---:|---|---:|
| 3 | 13 | Card Draw 4 (12) | **1** |
| 4 | 16 | Hand Destruction 4 (16) | **0** |
| 5 | 19 | Hand Destruction 4 (16) | **3** |
| 6 | 22 | Hand Destruction 5 (20) | **2** |
| 8 | 28 | Hand Destruction 5 (20) | **8** |

A 5-cost Ascendant that takes your single biggest legal effect is a **0/1/1/1 body**. Mass
Removal — destroy every Character on the board — costs 8, which on a 5-cost leaves 11 points,
about a 3/3/3/2. **That is your ceiling on "crazy": a board wipe on a slightly-below-average
body.** Two of your printed effects (Hand Destruction 4 and 5) cannot be put on a card at all
below cost 6 without a 1/1/1/1 statline.

And the pool shows the consequence. Across all 25 costed cards:

**73% of every point ever spent went to vanilla stats. 23% to effects. 4% to keywords.**

The system spends three-quarters of its budget on plain numbers, because plain numbers are the
only thing it can price with confidence. That ratio is the system telling you what it is.

### 1.4 It measures the card, not the play

Two cards with identical point totals can have completely different interaction profiles — one
answerable at four separate moments, one uninterruptible — and the formula cannot tell them
apart. Counterplay is currently a pass/fail gate bolted on the side (G7), not part of the
valuation. So the system is indifferent to the exact quality you say the game must have.

---

## Part 2 — The one thing you already got right, and it's big

**Phase 2 is alternating single actions.** You play one thing, then your opponent acts, then
you play the next thing.

That is *per-action initiative*, and it is the same structural valve Legends of Runeterra was
built around. Riot's design director Andrew Yip called the goal *"deep interactive
conversational gameplay where you see your opponent's plan unfold over a series of actions."*
Mastering Runeterra states the trade plainly: *"Developing a unit gives your opponent the next
action. This creates a trade-off — you gain board presence but surrender initiative."*

The arithmetic consequence is enormous and you should understand it precisely:

> **A five-step plan in your game automatically hands your opponent four interaction windows.**

The same five-step plan in Yu-Gi-Oh hands them *zero* — which is why Yu-Gi-Oh had to invent
hand traps, an entire universal card class costing a third of every deck, just to buy back what
your Phase 2 gives away for free.

**This is the single most valuable structural asset in your design, and your point system does
not know it exists.** You are already paying the tax that licenses huge plays. You are just not
collecting the benefit.

The rest of this document is about collecting it.

### 2.1 Which means your real currency isn't Energy

Energy is what a card costs to *play*. But in a game of alternating actions, the thing that
actually constrains a plan is **how many actions it takes**, because every action you spend is
an action your opponent gets to respond with.

Digimon made this its entire economy: memory is a shared slider, and the cost of a play is
literally *how much turn you hand your opponent*. You can do anything on turn one — you just
pay for it in their tempo. Your game has the same shape and doesn't price it.

**Actions surrendered is your native unit of account. Energy is secondary.**

---

## Part 3 — What the good games actually do

Five games, five different valves. Each solves the same problem: *when is a huge play
acceptable?* The condensed answer across all of them:

> **A huge play is acceptable when the opponent can pay to stop it, in a currency the plan-maker
> cannot pre-empt, at a moment the plan-maker cannot skip.**

| Game | The valve | Currency of counterplay | Timing |
|---|---|---|---|
| Yu-Gi-Oh | Hand traps | Cards in hand | Mid-chain, on the opponent's turn |
| Legends of Runeterra | Per-action initiative | Banked spell mana | Between every single action |
| Netrunner | The tax (runtime pricing) | Credits + clicks | The moment of rez |
| Marvel Snap | The exit option | Cubes (stake, not wins) | Any turn, before reveal |
| Slay the Spire | Rate-limited assembly | Run economy | Deck construction |

**You already own the LoR valve.** So the techniques worth stealing are the ones that stack on
top of it.

### 3.1 Techniques worth taking

**Tax the scaling variable, not the strategy.** Nibiru counts summons — the sixth costs your
whole board. Time Eater counts cards played — the thirteenth ends your turn. Beat of Death
charges HP per card. None of these says *"you may not combo."* All of them say *"combo length
has a price."* The result is that the combo **changes** rather than dying: competitive Yu-Gi-Oh
lines are now built to stop at four summons. **That is the answer working, not failing.**

**Time and visibility are a currency you can spend on power.** Magic's suspend is explicit: a
creature with suspend 1 is *"almost the same as having a creature come into play tapped,"* and
longer suspend buys a bigger effect at lower mana. Planeswalker loyalty exists so the huge
effect can't happen immediately — Rosewater: without it, *"they could do their big effect the
first chance they had. Kind of anti-climactic."* Every LoR alt-win condition is a public,
accumulating counter on a destroyable object with a long clock.

**Convert absolutes into rates.** Hexproof became ward (pay a tax instead of "can't be
targeted"). Affinity-for-artifacts (Storm Scale 8, format-destroying) versus affinity-for-basic-
lands (Storm Scale 6, safe) — the *only* difference is that land drops are rate-limited and
artifacts aren't. **A cost reduction whose input is rate-limited is safe; one whose input is
unbounded is not.** This is the most transferable single rule in the whole research.

**Give losing players rubber-band clauses.** Yu-Gi-Oh writes catch-up conditions directly into
card text: Lightning Storm is *"if you control no face-up cards"*; Evenly Matched and Infinite
Impermanence are *"if you control no cards, you can activate this from your hand."* These cards
are **dead when you're winning and live when you're losing**. That's a handicap system hidden
inside card text, and it costs the format nothing.

**The answer must be immune to the thing it answers.** Dark Ruler No More and Super
Polymerization both say *"neither player can activate cards in response."* An answer to a board
of negates is worth zero if it can be negated.

**Staged payoffs beat binary ones.** Hearthstone's three generations are the clearest documented
lesson in this exact area: Un'Goro (hard requirement → one huge terminal card) → Uldum (easy
requirement → small permanent upgrade) → Stormwind Questlines (staged, payout at every step).
Liv Breeden on why: *"you get payout along the way, but you still have the moment where you go,
'Alright, now we're entering the second phase.'"*

### 3.2 The failure modes, so you can avoid them by name

Four ways a valve breaks. Every documented disaster is one of these:

| Failure | Signature | Case |
|---|---|---|
| **Answer on the wrong axis** | High nominal answer density, zero effective density | Kashtira 2023 — hand traps answer *activations*; floodgates are passive, so they answer nothing |
| **Answer too strong** | The answer becomes the format | Maxx "C" — "draw 20 or don't play" isn't counterplay. Forbidden since 2018 |
| **Answer can be answered for free** | Valve closes silently | Called by the Grave / Crossout Designator held at 1 copy on purpose |
| **No response window at all** | FTKs | Firewall Dragon with no once-per-turn → one-card kills; the opponent never gets a turn |

And two payoff-shape failures worth memorizing:

- **The payoff regenerates its own setup.** Quest Mage's Time Warp gave an extra turn, which
  generated more spells, which re-completed the quest. Blizzard nerfed the *requirement* twice
  over seven years before reaching for the right knob — capping the *payoff* at once per game.
- **The payoff scales with earliness.** Quest Rogue's Crystal Core made your whole deck 5/5s, so
  completing it sooner made it *bigger*. When payoff and requirement are positively correlated,
  raising the requirement is an inverted knob and cannot work.

---

## Part 4 — The Score

The replacement system. One sentence:

> **Power is not capped. Power is earned — by paying in currencies other than Energy, and by
> handing your opponent windows to stop you.**

The critical inversion: counterplay stops being a restriction and becomes **the engine of
power**. The more real chances you give your opponent, the bigger you are allowed to be. A
designer trying to maximise a card's power under this system is forced, by the gradient itself,
toward interactive design.

### 4.1 The three ledgers

```
  A. THE PRICE      what the card costs beyond Energy      → earns Credits
  B. THE WINDOWS    where the opponent can intervene       → earns a Multiplier
  C. THE SCORE      what the card is allowed to do         = (Budget + Credits) × Multiplier
```

Formally:

```
  Base Budget = (cost × 3) + 1 + (3 if Ascendant)          [unchanged]
  Earned      = Base Budget + Σ Credits
  Ceiling     = Earned × (1 + 0.25 × Windows)              [Windows 0–5, so ×1.00 to ×2.25]
```

A card with no setup, no telegraph and no interaction windows earns nothing and is capped at
exactly today's budget. **Small, instant, uninterruptible effects stay exactly as small as they
are now.** Everything above that has to be bought.

### 4.2 The Price — the credit table

Every credit below is anchored to a value **your own effects table already prints**, so the two
halves of the system agree with each other.

| You pay | Credit | Anchored to |
|---|---:|---|
| Each **card** permanently spent (discarded, exiled, banked) beyond this one | **+3** | Card Draw 1 = 3, so a card is worth 3 |
| Each **Energy** paid above the printed cost | **+3** | Energy Gen 1 = 3 |
| Each of your own **Characters** consumed / sacrificed | **+5** | Hard Removal = 5 — you're doing removal to yourself |
| Each of your own **Attachments** consumed | **+2** | Soft removal band |
| Each **Character required on board** as a condition (not consumed) | **+2** | Half of consuming it |
| Each full **Round of telegraph** between commitment and payoff | **+5** | A draw (3) plus a round of tempo |
| Each **opponent action** the card itself surrenders | **+2** | Half a card of tempo |
| Each **2 Life Points** paid | **+1** | Direct Damage 1 = 1, scaled to a 30-LP pool |
| **Narrowness** — live in only some matchups or board states | **+2 / +4** | Capped. See §6 |

**Anti-double-count rule.** Actions that happen *inside* a Round already paid for as telegraph
are not counted again. Count telegraph Rounds, or count actions, never both for the same
interval.

**Narrowness is hard-capped at +4** and may never be a boolean. See §6.

### 4.3 The Windows — the multiplier

Five places a plan can be stopped. Count only the ones that are **real**.

| # | Window | The question |
|---|---|---|
| **W1** | **Pre-assembly** | Can the opponent stop you gathering the pieces? (kill the required Characters, strip the hand, deny the Energy) |
| **W2** | **During assembly** | Can they disrupt it after you've committed but before it pays? (remove a piece mid-telegraph, Silence the caster) |
| **W3** | **On resolution** | Can they respond in the Reaction Window? (Combat Tactic, Fast Ability, Counter) |
| **W4** | **Post-resolution** | Can they recover, undo, or moot it after it lands? (heal through it, rebuild, bounce) |
| **W5** | **Orthogonal** | Can they simply win first? Is the clock long enough to race? |

**The Window Proof requirement.** Each claimed window must name **a specific existing card or
rule** that exercises it. "Someone could theoretically remove it" is not a window. This is
Melissa DeTora's rule — healthy combos *"can be disrupted using cards that people commonly
play"* — and it is the thing that stops the multiplier from being free money.

**The faction check.** For each window, ask: *can the faction with the fewest tools use it?*
Your Warmongers have no printed Counter and no non-combat removal. A card whose only window is
W3 is a Blue-mandatory card, and W3 does not count for it.

### 4.4 Worked example — the kind of card you actually want

**"The Takeover"** — hypothetical 5-cost Latin Kings Ascendant.

*Base side:* while he's on the Board, at the start of each Round put a Crown counter on him.
*Level-up:* at 2 Crowns, sacrifice three other Latin Kings Characters → the huge payoff.

| Ledger | | |
|---|---:|---|
| Base Budget (5-cost Ascendant) | **19** | |
| 3 Latin Kings required on board | +6 | 3 × 2 |
| 2 Rounds of telegraph (public Crown counters) | +10 | 2 × 5 |
| 3 Characters consumed on resolution | +15 | 3 × 5 |
| The summon action itself | +2 | |
| **Earned** | **52** | |
| W1 kill the Latin Kings before he assembles | ✓ | Hard Removal, any faction |
| W2 kill *him* during the two-Round charge | ✓ | he's a Character with printed PH |
| W3 Counter the activation in the Reaction Window | ✓ | Combat Tactic |
| W5 race him — two Rounds is a real clock | ✓ | any aggro board |
| **Multiplier** (4 windows) | **×2.0** | |
| **CEILING** | **104** | |

**104 points.** Mass Removal costs 8. This card is allowed to do something roughly thirteen
times more powerful than destroying the entire board — which means it should just *win the
game*, and under this system that is **correct and priced**, not a designer indulgence.

Compare: the same effect with no setup, no telegraph, no sacrifice and no windows is capped at
19. The system is not stopping you from being crazy. It is charging you for it, in the currency
you said you wanted to pay in.

### 4.5 Ceiling discipline

The Ceiling is a **ceiling, not a target**. Most cards should sit far below it — that's how the
big ones feel big.

Ben Brode on Galactus, the most powerful card in Marvel Snap:

> *"If the best part of the game is Galactus, then it's not the best part of the game."*

**The quota:** at most **one card per ten** in the pool may exceed **2× its base budget**, and
at most **one per crew**. If every card is a heist, nothing is.

---

## Part 5 — The Four Prohibitions

No amount of Credits buys past these. Each is a documented disaster, not a preference.

### P1 — No self-restarting payoff

The payoff may not regenerate its own setup condition. *(Time Warp: extra turn → more spells →
re-complete the quest. Seven years to fix, and the fix was capping the payoff, not the
requirement.)*

**Test:** after the card resolves, is the player measurably closer to doing it again than they
were before they started? If yes, it is prohibited regardless of budget.

### P2 — No passive lock

An effect that prevents an opponent's action must either be an **activation** (so it can be
responded to) or carry an **off-switch** (a cost to maintain, a duration, or an exception that
lets it be attacked).

*(Kashtira 2023: hand traps answer activations; floodgates are passive continuous effects, so a
format with 15 answers per deck had an effective answer density of zero.)*

**This resolves OQ-09.** Pacifier — *"an aura that completely prevents the declaration of a
Combat Wave"* — is a passive lock on the game's only damage mechanism, and Warmongers have no
non-combat removal. It is currently prohibited. Three legal repairs: make it cost Energy each
Round to maintain; let attackers pay a tax to attack anyway; or make the Pacifier itself
attackable as an exception to its own aura — which is also the better story.

### P3 — No unbounded repetition

Every repeatable ability carries a hard **once per Round** unless a resource is consumed on each
use. *(Firewall Dragon had no once-per-turn and produced one-card kills — the terminal failure
state, where the opponent never gets a turn at all and per-action initiative never engages.)*

**Test:** write the loop out longhand. If the only stopping point is "the player chooses to
stop," it is prohibited.

### P4 — No cheap + wide + uninterruptible

Celia Wagar's grid: a counter is **hard or soft** (guaranteed vs. wiggle room) and **wide or
narrow** (many options vs. one). An effect may be at most **two** of {cheap, wide,
uninterruptible}. Hard-and-wide is the most expensive class of effect in any game and must be
priced like it.

**Corollary — the Sirlin test**, the sharpest counterplay check available:

> *"A dominant move probably has no real counter, so even if the opponent knows you will do it,
> there's not a lot they can do."*

Ask it of every card: **if the opponent knows exactly what's coming, can they do anything?** If
no, the card fails P4 no matter what the ledger says.

---

## Part 6 — Faction asymmetry, done properly

You asked for cards that are *"stronger vs specific factions."* This is a real design space and
it has real rules, from Rosewater's treatment of colour hosers. Adapted:

**F1 — Target your faction's designed enemy, not an arbitrary one.** The matchup asymmetry
should follow the fiction, not the spreadsheet.

**F2 — Keep faction flavour.** Don't give the Warmongers a counterspell to fix a bad matchup.
Rosewater's own example of failure is red destroying enchantments — it violates the colour's
designed weakness, so it fixes a matchup by deleting an identity.

**F3 — Scale with the degree of the condition, never a boolean.** *"For each enemy Overthinker
Character, +1 PA"* is legitimate. *"If your opponent is Blue, you win"* is not. A gradient turns
a matchup coinflip into a difficulty curve. **This is the single most important rule here.**

**F4 — Exploit the *printed weakness*.** And here is the gift you already gave yourself: each of
your four factions ends its rulebook entry with a rhetorical question naming its own weakness.
Those four questions are the four legitimate hoser axes, pre-authorised and pre-flavoured.

| Faction | The printed weakness | The legitimate asymmetry axis |
|---|---|---|
| 🟥 Warmongers | *"when a problem cannot be solved with fists…"* | Cards that make combat unprofitable or irrelevant |
| 🟦 Overthinkers | *"how long can a genius survive a street fight?"* | Cards that punish holding up answers; raw speed |
| 🟩 Assholes | *"forced into a fair, head-on collision, do they have the spine?"* | Cards that force open confrontation and deny evasion |
| 🟨 Icons | *"can a symbol actually bleed?"* | Cards that attack reputation, followers, and Influence |

**F5 — Never auto-win.** A hoser must leave the target counterplay. Rosewater names *Perish* and
*Dystopia* as the violations.

**The two failure modes to name and avoid** (DeTora's taxonomy):
- **The Faerie problem** — narrow but *invalidating*. A card so good against one strategy that
  the strategy stops existing.
- **The Doom Blade problem** — universal and *mandatory*. A card too good not to run, warping
  the format around itself.

They need opposite fixes: the first needs a gradient (F3), the second needs a cost.

---

## Part 7 — Three structural gaps you should close

These aren't card problems. They're rules problems, and they gate everything above.

### 7.1 The Command System has a death spiral with no rubber band

Section 4 says it out loud: *"a wiped board means you cannot cast Tactics to save yourself!"*

That is textbook **slippery slope** (Sirlin): *"falling behind causes you to fall even further
behind."* The player who most needs a Tactic is the player structurally forbidden from casting
one. The consequence — *"the real victor is decided early on and the rest of the game is futile
to play out."*

**The fix is proven and cheap: the rubber-band clause.** Print it on a cycle of Tactics, lifted
almost verbatim from Infinite Impermanence and Evenly Matched:

> *"If you control no Characters, you may play this card without declaring a caster."*

These cards are dead when you're winning and live when you're losing. They cost the format
nothing and they convert an unwinnable position into a hard one. This is the highest-value
single rules addition available to you.

### 7.2 You need a universal interaction layer

Per-action initiative protects you during Phase 2 — but **Trigger Abilities cost no action**,
and Passive Abilities are always on. A chain of triggers resolves inside a single action with no
window. That is exactly where a first-turn kill would eventually live.

Two additions:

- **A small cycle of Combat Tactics playable from hand at zero board requirement** — your hand
  traps. Universal, faction-agnostic, and the price of admission for letting Ascendants be
  enormous. Yu-Gi-Oh spends a third of every deck on this; you'd need far less, because Phase 2
  already does most of the work.
- **A Nibiru clause.** Tax the scaling variable: something that triggers when a player takes
  *N* actions in a Round, or plays *N* Characters. It doesn't ban the plan — it prices the
  length of the plan, and combo lines will reshape themselves around it. That reshaping is the
  mechanic succeeding.

### 7.3 The Influence win condition is the natural home for all of this

Influence is currently a printed win condition with zero printed support (OQ-02), owned by a
faction with zero printed cards (OQ-06). That's not two problems and a gap — it's an empty lane
with the perfect shape for exactly what you're asking for.

Build it on the LoR alt-win pattern, which is the most successful telegraphed-payoff design in
any modern card game. **Star Spring**: *"Round End: Heal damaged allies 1. Then, if I've seen you
heal 22+ damage from allies, win the game."* Four separate answer surfaces in one card — it's a
destroyable object, the counter resets if it's destroyed and replayed, 22 at 1 per round is a
very long clock, and you can just kill them faster.

The pattern to copy: **a public, accumulating counter, attached to a destroyable object, with a
long clock, whose first tick is deliberately sub-lethal.** Mastering Runeterra on Frostguard
Thrall: *"getting a single one out rarely has any effect on the game state"* — so the opponent
gets multiple full Rounds between the first visible threat and the lethal one.

And stage it. Un'Goro → Uldum → Stormwind is the documented three-iteration lesson: binary
payoff → small permanent payoff → **staged payoff with payout at every step**. Your Ascendants
already have two stages. The biggest plans should have three.

---

## Part 8 — Migration

**This is not a retune. It's a new ceiling.** Every existing card remains legal — they all sit
at or below their base budget, which under the new system is the floor for a card that pays
nothing and gives nothing.

Order of work:

1. **Close P2 first.** Pacifier is currently prohibited. Repair it before anything else.
2. **Print the rubber-band cycle (§7.1).** Cheap, high-impact, unblocks everything downstream.
3. **Build one Score card** — one card at 2× base — and play it twenty times before building a
   second. The credit values below are hypotheses, not findings.
4. **Then** the Icons and Influence (§7.3), which is where the design space actually is.

### Tuning warning, from the evidence

Every scalar knob in every game researched turned out to have **two or three usable steps, not
ten**:

- Gwent's *Jackpot*: −1 provision *"impacted it but still left it dominant"*; −2 made it
  disappear entirely.
- Quest Rogue: 4 → 5 minions moved completion by roughly one turn.
- Quest Mage: 6 → 8 spells cost about one turn, and the card needed a functional rewrite seven
  years later anyway.

CDPR's own conclusion is worth keeping on the wall: *"Users are very good at identifying how
they feel, but often misidentify why, and give undesirable solutions."*

So: expect the credit values in §4.2 to move in **whole points, coarsely**, and expect the
Windows multiplier (currently 0.25) to be the most sensitive number in the system. Change one
thing at a time and log it in [`decisions.md`](decisions.md).

---

## Sources

The research behind this document, condensed. Primary sources only.

**Cost systems** — [Gwent's Design 01: Provision](https://www.playgwent.com/en/news/41252/gwents-design-01-provision) and [02: Balancing](https://www.playgwent.com/en/news/43034/gwents-design-02-balancing) (CDPR) · [Digimon Comprehensive Rules](https://world.digimoncard.com/rule/pdf/general_rule.pdf) (Bandai) · [Revealing Cycles](https://fabtcg.com/articles/revealing-cycles/) and [Pitch Perfect](https://fabtcg.com/articles/pitch-perfect/) (Legend Story Studios) · [One Piece Play Guide](https://en.onepiece-cardgame.com/play-guide/) (Bandai)

**Combo and build-around design** — [Philosophy of Combo](https://magic.wizards.com/en/news/feature/philosophy-combo-2017-08-04) (Melissa DeTora) · [Play Design Lessons Learned](https://magic.wizards.com/en/news/feature/play-design-lessons-learned-2019-11-18) (Bryan Hawley) · [Threats and Answers](https://magic.wizards.com/en/news/feature/threats-and-answers-2014-09-08) · [Storm Scale: Khans](https://magic.wizards.com/en/news/making-magic/storm-scale-khans-tarkir-block-2016-02-29) and [Mirrodin](https://magic.wizards.com/en/news/making-magic/storm-scale-mirrodin-and-scars-mirrodin-blocks-2018-06-11) (Mark Rosewater) · [Needing a Little Time](https://magic.wizards.com/en/news/making-magic/needing-little-time-2006-09-11) (suspend) · [The Saga of Sagas](https://magic.wizards.com/en/news/making-magic/saga-sagas-2018-05-07) · [Planeswalk on the Wild Side II](https://magic.wizards.com/en/news/making-magic/planeswalk-wild-side-part-ii-2007-11-12) (loyalty) · [Introducing Ward](https://magic.wizards.com/en/news/card-preview/introducing-ward-2021-03-25) · [Enemy Mine](https://magic.wizards.com/en/news/making-magic/enemy-mine-2002-02-18) (hosers)

**Counterplay theory** — [Counterplay and Teamplay in Multiplayer Game Design](https://gdcvault.com/play/1018273/Counterplay-and-Teamplay-in-Multiplayer) (Tom Cadwell, Riot, GDC 2013) · [Building Counterplay for PvP Games](https://critpoints.net/2025/05/06/building-counterplay-for-pvp-games/) (Celia Wagar — the hard/soft × wide/narrow grid) · [Balancing Multiplayer Games Part 2: Viable Options](https://www.sirlin.net/articles/balancing-multiplayer-games-part-2-viable-options) and [Slippery Slope and Perpetual Comeback](https://www.sirlin.net/articles/slippery-slope-and-perpetual-comeback) (David Sirlin) · [Ten Things Every Game Needs](https://magic.wizards.com/en/news/making-magic/ten-things-every-game-needs-part-1-2011-10-24) (Rosewater)

**Structural valves** — [Hearthside Chat: Un'Goro Quests](https://us.battle.net/hearthstone/en/blog/20567342/hearthside-chat-ungoro-quests-with-peter-whalen-3-22-2017) (Peter Whalen) · [Mike Donais on the Quest Rogue change](https://gamesbeat.com/hearthstones-top-game-designer-breaks-down-quest-rogue-change/) · [Designing MARVEL SNAP](https://gdcvault.com/play/1029024/Designing-MARVEL-SNAP) (Ben Brode, GDC 2023) · [Andrew Yip on LoR's design](https://www.ungeek.ph/2020/05/design-director-andrew-yip-shares-how-legends-of-runeterra-challenges-the-norm-of-digital-card-games/) · [Mastering LoR Priority](https://masteringruneterra.com/mastering-lor-priority/) · Yu-Gi-Oh card text via [Yugipedia](https://yugipedia.com/wiki/Hand_trap)
