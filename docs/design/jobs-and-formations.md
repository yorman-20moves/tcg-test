# Jobs & Formations — adapting the role catalogue

The catalogue is written for 5v5 real-time games and 5-person tabletop parties. This game is
neither. This document is the translation: what carries over, what has to be rebuilt in your
mechanics, what to cut, and — most usefully — **the roles the catalogue names that your game
currently has no way to express.**

Nothing here is built yet. This is the design decision first.

---

# Part One — Three decisions before anything else

## 1. It's called a **Job**, not a Role

Your rulebook already says: *"Keywords are specific **Roles** that a Character plays on the
Board. Each Role is completely exclusive to its specific Faction."*

So "Role" is taken, and it means something narrower — a faction-exclusive mechanic. Using it for
two things would break the one vocabulary you've been strict about.

**Job** is the catalogue's own term ("Team Job"), and it's the right language for this world:
*what's your job in this crew?* Clean separation:

> **Keyword / Role** — a faction-exclusive mechanic. *Protector. Prowler. Troll.*
> **Job** — what you do for your crew. *Warden. Ghost. Quartermaster.*
>
> A Job is usually *expressed through* Roles, but it isn't one. Two Wardens in different
> factions do the same job with different tools.

## 2. You already have four of the catalogue's six axes. Don't add them again.

The catalogue's central claim is that "role" is really six independent axes. That's right — but
you've already built four of them under different names. Adding all six would double-count.

| Catalogue axis | What you already have | Decision |
|---|---|---|
| **1. Team Job** | *nothing* | **ADD — this is the whole point** |
| **2. Power Pattern** | The Score's credits describe *how* a card delivers power | **Light tags only** |
| **3. Tempo / Scaling** | Cost, and the Ascendant level-up curve | **Light tags only** |
| **4. Delivery & Range** | **Your keywords.** Prowler, Troll, Juggernaut, Combo-Striker *are* delivery | **Already covered — do not duplicate** |
| **5. Resource Economy** | The Investment Engine, plus `once_per_game` in plan-credits | **Already covered** |
| **6. Pillar** | **Your three victories.** Beatdown = Combat. Influence = Social | **Map, don't add** |

**Axis 6 is the interesting one.** The catalogue says a 5v5 game has one pillar and tabletop has
three. **You have two** — Beatdown and Influence — and you built the second one and never used
it. The Icons are your entire social pillar, sitting empty.

So the only genuinely new axis is Job. Everything else is a light tag or already exists.

## 3. Range doesn't exist here, and that collapses half the catalogue

This is the biggest translation problem and it's worth being blunt about.

Most of the catalogue's damage distinctions — Marksman vs Juggernaut vs Skirmisher vs Sniper —
are about **range and mobility**. Your game has neither. Every attack is a Combat Wave clash at
the same notional distance. There's no kiting, no positioning, no dodging, no aim.

So those archetypes don't collapse into fewer jobs by accident — **they collapse because the
axis that separated them doesn't exist in your game.** What actually distinguishes a damage card
here is:

- Does it attack **PH or MH**? *(PA vs Troll — your second, unused damage axis)*
- Does it **get past blockers**? *(Prowler, Juggernaut spillover)*
- Does it **kill in one hit**? *(Executioner, Hard Removal)*
- Does it damage **without declaring a Combat Wave**? *(Direct Damage effects)*
- Does it hit **everything at once**? *(Mass Removal)*
- Does it **grow the longer it survives**? *(Berserker, stacking)*

The Jobs below are organised by *those* axes. That's the adaptation, not a translation.

---

# Part Two — The Job catalogue

Twenty-one Jobs in four families. Each carries a **signature** written in your own vocabulary,
so a card can be checked against the Job it claims.

Jobs marked **⚠ NO MECHANICS YET** are the valuable ones — the catalogue names a real position
your game currently cannot fill. Those are in Part Three.

---

## FRONT — cards whose output is space, not damage

*The universal test, and it survives translation intact:* **if the opponent ignores me I win; if
they deal with me my crew wins.** A Front card that can be safely ignored *and* safely killed has
no job.

### F1 · Vanguard
- **Identity** — decides *when* the Combat Wave happens.
- **Job** — make declaring a Combat Wave profitable on a Round your opponent didn't want one.
- **Signature** — high PA and PH · Juggernaut or Combo-Striker · effects that trigger on attacking.
- **Beats** — boards that want to build. Opponents holding cards for later.
- **Loses to** — Pacifier, Prevent Attack, Protector walls, being Feared or Stunned.
- **The line** — a Vanguard *starts* fights. A Ghost *avoids* them.
- **Note** — the catalogue's "engage cooldown is the team's tempo clock" translates perfectly:
  a Combat Wave is once per Round per player, so a Vanguard's Round *is* the clock.

### F2 · Warden
- **Identity** — a bodyguard. Stands between the threat and whoever can't survive it.
- **Job** — deny access to one Character. Punish the opponent's Combat Wave rather than declare one.
- **Signature** — **Protector** · high PH, low PA · Prevent 1 Attack · Protection (Immunity) on allies.
- **Beats** — single-target removal, Executioner lines, anything that needs a clean hit.
- **Loses to** — Prowler (goes around the hitbox), Mass Removal, Silenced, being ignored entirely.
- **The line** — a Warden protects with a **body**. A Backer protects with **effects cast from safety**.

### F3 · Wall
- **Identity** — must be dealt with. Occupies rather than attacks.
- **Job** — force the opponent to spend actions and cards on you instead of on the plan.
- **Signature** — **Instigator** · very high PH · Prevent Multiple Attacks · low or zero PA.
- **Beats** — Combat-Wave plans, engines that need a quiet Round.
- **Loses to** — Prowler, Troll (goes at MH instead), Direct Damage, Bounce.
- **The line** — a Wall's power is a **duration**; a Vanguard's is a **moment**.

### F4 · Collector — **⚠ NO MECHANICS YET**
- **Identity** — doesn't stop you attacking your target; makes it the worst available choice.
- **Job** — attach a price to every attack that isn't aimed at it.
- **Why it's a gap** — Instigator is **compulsion** (you *must* target me). The catalogue's
  sharpest single idea is that **taxation** is the better version: let them through and charge a
  fee. You have no marks, no threat, no retaliation riders. See Part Three.

---

## DAMAGE — cards hired to convert time into dead Characters or Life Points

### D1 · Enforcer
- **Identity** — wins straight clashes and keeps winning them.
- **Job** — reliable Combat Wave damage every Round. The floor the crew is built on.
- **Signature** — strong PA relative to cost · solid PH · Multiple Attacks · no conditions.
- **Beats** — anything that has to trade with it on board.
- **Loses to** — Protector, Prevent Attack, Stun, Fear, and specialists in their own context.
- **The line** — the Enforcer has **no gimmick**, and that's the point. It's variance reduction:
  the card that never has an off Round. Uniquely valuable in a crew of specialists.

### D2 · Executioner
- **Identity** — finishes what somebody else started.
- **Job** — convert damaged Characters into dead ones. Doesn't open, closes.
- **Signature** — **Executioner** keyword · Hard Removal · effects keyed to Wounded or permanent damage.
- **Beats** — anything already hurt. Boards that traded last Round.
- **Loses to** — a fresh board (nothing to finish), Protection (Immunity), healing.
- **The line** — an Enforcer wins a fight. An Executioner **prices being in one at all.**
- **Note** — this is a genuinely great fit for your game. **Permanent damage** means a damaged
  Character stays damaged across Rounds, so an Executioner threatens *everything that has ever
  been hit.* Very few card games can express that.

### D3 · Ghost
- **Identity** — the board isn't in the way.
- **Job** — bypass blockers entirely and put damage on Life Points.
- **Signature** — **Prowler** · Extortionist · Untargetable · moderate PA, low PH.
- **Beats** — Warden and Wall (goes around both), slow builds, anyone at low Life Points.
- **Loses to** — **Tracker** (the printed hard counter), Mass Removal, Direct Damage.
- **The line** — this one Job absorbs four catalogue archetypes — Flanker, Sniper, Diver
  Assassin, Stealth Ambusher — because all four are separated by *range and concealment*, and
  your game has neither. Here they are one thing: **can't be blocked.**

### D4 · Headcase
- **Identity** — hits the mind, not the body.
- **Job** — attack MH instead of PH, going around every defence built for physical damage.
- **Signature** — **Troll** · high MA · Shattered application · MA-based Direct Damage.
- **Beats** — anything with a big PH and a small MH — which today is *most Warmongers.*
- **Loses to** — high MH, Status Immunity, Cleanse.
- **The line** — the only Job defined by **which health bar it empties.**
- **Note** — this is the Job that turns MA/MH from dead weight into a second axis (OQ-05). One
  keyword currently supports it. If you want the mental game to exist, this Job is where it lives.

### D5 · Artillery
- **Identity** — damage without ever declaring a Combat Wave.
- **Job** — grind Life Points and Characters down from outside combat entirely.
- **Signature** — Direct Damage 1–5 · low PA · Trigger and Passive abilities rather than attacks.
- **Beats** — Pacifier, Protector, Wall — **everything built to answer combat.**
- **Loses to** — healing, Cleanse, and a clock (it's slow).
- **The line** — the only damage Job **immune to the entire Front family.** That's why it exists.

### D6 · Wrecker
- **Identity** — deletes boards, not Characters.
- **Job** — punish a wide board; reset the game.
- **Signature** — **Mass Removal** · high cost · usually a level-up payoff, never cheap.
- **Beats** — wide boards, token strategies, anyone who over-committed.
- **Loses to** — one big Character (damage wasted), holding cards in hand, Protection.
- **The line** — value scales **inversely with the opponent's card quality**. Strongest against
  many weak, weakest against one strong.

### D7 · Grinder
- **Identity** — gets worse for you every Round it survives.
- **Job** — win the long game. Grow while the fight lasts.
- **Signature** — **Berserker** · stacking or per-Round triggers · self-sustain · high PH.
- **Beats** — attrition plans, boards that can't kill it quickly.
- **Loses to** — Hard Removal, Bounce, Stun, and any Round it isn't allowed to act.
- **The line** — the Grinder's power is a **curve**; the Enforcer's is a **flat line.**

---

## SUPPORT — cards whose output passes through other cards

*The catalogue's warning holds exactly:* a Support card's numbers are meaningless alone. The same
card is excellent next to a Ghost and worthless next to another Support. **This is the most
pairing-dependent family, and it's the one the crew Formation exists to protect.**

### S1 · Backer
- **Identity** — makes one Character into two.
- **Job** — buff, shield and protect an ally so they survive to do their job.
- **Signature** — Permanent Buff · Protection (Immunity) · Spell Shield · targets allies, low own PA.
- **Beats** — single-target removal, Executioner, chip damage.
- **Loses to** — Mass Removal, Silenced, and **bad pairings** — a Backer next to nothing worth
  backing is a blank card.

### S2 · Grabber
- **Identity** — one button ends a Character's Round.
- **Job** — take the opponent's best card out of the game long enough to win the exchange.
- **Signature** — Soft Removal (Stun) · Status Application (Minor/Major) · Feared · Bounce.
- **Beats** — anything that needs to act. Vanguards, Grinders, engines.
- **Loses to** — Status Immunity, Cleanse, wide boards (it only stops one thing).

### S3 · Fixer
- **Identity** — refuses to let anyone die slowly.
- **Job** — heal permanent damage; make attrition unwinnable for the opponent.
- **Signature** — **Nurturer** · Direct Heal · Cleanse.
- **Beats** — Artillery, chip damage, Grinders, long games.
- **Loses to** — burst that outpaces it, **Wounded and Shattered** (which forbid healing outright
  — your printed anti-heal), Executioner.
- **Note** — the catalogue's honest warning applies: healing only restores what the opponent
  already paid to remove. In your game a Fixer is strong specifically because **damage is
  permanent**, so undoing it is undoing a real investment.

### S4 · Bailout
- **Identity** — does nothing for four Rounds and then wins the game.
- **Job** — undo a kill that already happened. One enormous, rationed button.
- **Signature** — Protection (Immunity) · Recursion · Counterspell · once per Game.
- **Beats** — Executioner lines, Wrecker, all-in Combat Waves.
- **Loses to** — attrition (nothing to save from), and being **baited** into spending it early.
- **The line** — a Backer's mitigation is **continuous**; a Bailout's is **one moment.**

### S5 · Quartermaster
- **Identity** — pays for everyone else's plan.
- **Job** — generate Energy and cards so the crew can act above its cost.
- **Signature** — **Sponsor** · **Hustler +X** · Energy Gen · Card Draw.
- **Beats** — anything slower than you. Expensive plans that would otherwise never assemble.
- **Loses to** — Resource Denial, Taxing, Hand Destruction, and pressure that kills it early.
- **Note** — this replaces the catalogue's Tempo Support. It has no movement to grant, so in
  your game **tempo is Energy.** The Investment Engine makes this a first-class Job.

### S6 · Silencer
- **Identity** — turns off the opponent's best card rather than killing it.
- **Job** — apply Silenced, anti-heal and Resource Denial so their plan stops functioning.
- **Signature** — Silenced · Wounded/Shattered (anti-heal) · Resource Denial · Taxing.
- **Beats** — Fixers, Backers, engines, anything with printed abilities.
- **Loses to** — a crew with no abilities to turn off — against which it's a **blank card**.
- **The line** — defined entirely by *what it negates*, so its value is a pure function of the
  opponent's crew.

### S7 · Cleaner
- **Identity** — undoes the opponent's best play after it lands.
- **Job** — remove statuses; restore a locked-down Character to functional.
- **Signature** — Cleanse (Minor/Major) · Status Immunity.
- **Beats** — Grabbers, Silencers, status-stacking, Shattered/Wounded setups.
- **Loses to** — straight damage with no status attached — **0% useful in that matchup.**
- **The line** — the exact mirror of the Grabber. The most swingy Job here: match-winning or dead
  weight with no change in how you play it.

### S8 · Boss — **⚠ NO MECHANICS YET**
- **Identity** — gives your best card another action.
- **Job** — manipulate the Phase 2 action economy directly.
- **Why it's a gap** — and why it's the **single most valuable thing on this list.** See Part Three.

---

## SPECIALIST — cards whose contribution is information, denial or presence

### X1 · Spy
- **Identity** — works for you from their side of the table.
- **Job** — sit on the opponent's Board providing value just by existing there.
- **Signature** — **Infiltrator** · Passive abilities · low stats.
- **Beats** — opponents who can't or won't remove their own Character.
- **Loses to** — the opponent sacrificing it, Mass Removal.
- **Note** — Infiltrator is the strangest keyword you have and the only one priced **negative**.
  The catalogue calls this "attention laundering." Worth re-reading OQ-11 with that lens.

### X2 · Snitch
- **Identity** — converts knowledge into advantage.
- **Job** — reveal the opponent's hand and plans so the crew can act with certainty.
- **Signature** — **Interrogator** · forced reveals · Hand Destruction as follow-up.
- **Beats** — held answers, Bailouts, anything relying on surprise.
- **Loses to** — an opponent playing everything face-up anyway.
- **The line** — the catalogue's warning is real: **information you can't act on is worth
  nothing.** A Snitch in a crew with no follow-up is a wasted slot.

### X3 · Cutoff
- **Identity** — doesn't beat the plan, cancels it.
- **Job** — Counter cards and abilities in the Reaction Window; kill the caster before it resolves.
- **Signature** — **Counterspell** · Fast Abilities · Combat Tactics.
- **Beats** — one-big-card plans, level-up payoffs, Bailouts.
- **Loses to** — many small threats (nothing worth countering), and being baited.
- **Note** — your **Command System** makes this Job unusually strong. Killing the caster in
  response cancels the card entirely. That's a Cutoff mechanic baked into your rules, and no
  card currently exploits it.

### X4 · Setter
- **Identity** — wins Rounds it set up three Rounds ago.
- **Job** — place Attachments and permanents in advance; convert planning into inevitability.
- **Signature** — Attachments · **Commandments** · Trigger abilities on a delay.
- **Beats** — slow opponents, predictable plans.
- **Loses to** — Attachment removal — and remember **an Attachment dies with its Character**, so
  a Setter's whole investment is bolted to bodies.
- **Note** — Dre is the purest Setter in the game.

### X5 · Legend
- **Identity** — doesn't need to kill you.
- **Job** — accumulate Influence toward the third victory.
- **Signature** — **Martyr** · Guilt-Tripper · Influence generation · often 0 PA.
- **Beats** — anyone playing only the Beatdown game.
- **Loses to** — a fast clock, and — currently — **the fact that no card grants Influence** (OQ-02).
- **Note** — this Job is your entire social pillar. It exists on paper and nowhere else.

### X6 · Landlord — **⚠ NO MECHANICS YET**
- **Identity** — edits the rules of the table.
- **Job** — change what's allowed for both players.
- **Why it's a gap** — this is what **Arenas** were always going to be. See Part Three.

### X7 · Recruiter — **⚠ NO MECHANICS YET**
- **Identity** — fields more bodies than it has cards.
- **Job** — flood the board with cheap Characters that demand answers.
- **Why it's a gap** — no token or summon mechanic exists. See Part Three.

---

# Part Three — What the catalogue proves you're missing

The most useful thing an outside framework does is name a position your system can't fill. Five
of those, ranked by how much they'd change the game.

## ① The Boss — an extra Phase 2 action *(the big one)*

The catalogue is emphatic that this archetype "exists only where turns exist," and that most
real-time games can only approximate it. **Your game has turns.** Phase 2 is explicit alternating
single actions — an action is a real, countable, spendable thing.

Which means *"take an additional action this Phase"* is a coherent, enormous, perfectly
expressible effect, and **you have no card that does it.**

Why it matters more here than anywhere else: your whole balance system is denominated in actions.
The Score charges +2 credits per opponent action surrendered. Per-action initiative is the valve
that makes big plans fair. A card that hands *you* an extra action is attacking the game's
central currency directly — which makes it both the most powerful possible support effect and
the one most in need of the four prohibitions.

**It also brings its own printed failure mode, which is good design:** granting the action to the
wrong card is strictly worse than doing nothing. The catalogue calls this the force-multiplier
trap. That's real decision-making, not just power.

**Suggested shape:** an Icons ability. *"Once per Game, an allied Character may take an
additional action this Phase."* Price it as a new effect around 6–8 points, and check it hard
against P1 — a Boss that generates actions which generate more actions is exactly the
self-restarting payoff that prohibition exists for.

## ② The Collector — taxation instead of compulsion

Your only "deal with me" tool is **Instigator**: the opponent *must* target it. That's
compulsion, and the catalogue argues convincingly it's the cruder tool. The better version lets
them through and **charges a fee**.

You already have the raw material: **Guilt-Tripper** (attacker takes 2 MA damage for hitting
this). That's a taxation rider — it just isn't generalised.

**Suggested shape:** a new keyword. *"Whenever an enemy Character attacks anyone other than
this one, they take 1 permanent PH damage."* Now the opponent's targeting decision is a real
choice with two costed answers instead of a forced move. It also plays beautifully with your
**Executioner**, because now everything on their board is quietly picking up permanent damage.

## ③ The Landlord — Arenas finally have a job

Arenas are referenced in §4 and §5 of your rulebook, have an art folder, and have **no rules at
all** (OQ-07). The catalogue's Control Mage — *"the only archetype that edits the map"* — is
exactly what they should be.

You have no map, so an Arena shouldn't edit space. **It should edit the rules.** *"While this
Arena is in play, Combat Waves cost 1 additional Energy."* *"Characters cannot be healed."*
*"Each player draws an additional card in Phase 1."*

The catalogue's warning transfers precisely: terrain authorship is **entirely
context-dependent** — S-tier in one matchup, blank in another. Which means Arenas should be
cheap, few, and symmetric-but-asymmetrically-useful. And note it satisfies prohibition **P2**
naturally, because an Arena is an object on the table that can be destroyed.

## ④ The Recruiter — bodies, and the reason Mass Removal exists

You have Mass Removal priced at 8 — the most expensive effect in the game — and **nothing to
use it on.** Nobody can field a wide board, because every Character costs a card and Energy.

The catalogue's numbers triangle is the missing piece:

> **Swarm → single-target damage → Mass Removal → Swarm**

Without the swarm corner, Mass Removal is a card that says "kill their two guys," which is
overpriced. Add tokens and the whole triangle switches on — and Wrecker, Blaster and the
grouping-punishment layer all become real.

## ⑤ The Breaker — nothing punishes a big body

Your defensive stat is PH, and nothing inverts it. A Character with enormous PH is simply better
than one without, forever.

The catalogue's Shredder exists to stop exactly that: *"without this archetype, stacking health
would be strictly correct."* In your game, stacking PH **is** strictly correct.

**Suggested shape:** an effect that deals damage equal to a fraction of the target's maximum PH,
or one that ignores PH entirely. **Troll already does a version of this** by going at MH instead
— so the cheapest fix isn't a new mechanic, it's *building out the Headcase Job* until high-PH
Characters have a real reason to fear something.

---

# Part Four — Formations: the 5-person crew structure

A crew is five Ascendants. That's your party, and the catalogue's §10.2 and §13 are about
exactly this.

## The rule

> **A crew declares a Formation. The Formation says which Jobs the five slots must cover.
> The Formation must follow from the crew's plan, and the plan must follow from the lore.**

The catalogue's observation about the fifth slot transfers directly and is worth keeping:

> *"In both a 5v5 comp and a five-person party, four slots are near-mandatory and the fifth is a
> strategic declaration about how you intend to win."*

So a Formation should name **four required Jobs and one free slot** — and the free slot is where
the crew says something about itself.

## Eight Formations

Adapted from the catalogue's comp archetypes, rebuilt around your mechanics. Proposed crew
assignments are drafts — the lore is yours.

| Formation | The plan | Required Jobs | Free slot | Loses to |
|---|---|---|---|---|
| **The Engine** | Build a machine over several Rounds, then detonate it | Setter · Quartermaster · Warden · Wrecker | anything that buys time | Cutoff, pressure before assembly |
| **The Court** | A hierarchy — the top buffs everyone below | Vanguard · Backer · Enforcer · Warden | usually a second Enforcer | Mass Removal, killing the head |
| **The Shakedown** | Take what they have until they can't act | Quartermaster · Silencer · Ghost · Grabber | Spy or Snitch | crews that don't need resources |
| **The Long Night** | Everyone leaves worse, including you | Grinder · Fixer · Wall · Headcase | Enforcer | burst, a fast clock |
| **The Ambush** | End it before it starts | Ghost · Executioner · Grabber · Snitch | Cutoff | a wide board, Cleaner |
| **The Congregation** | Win on Influence, never on damage | Legend · Fixer · Wall · Cleaner | Backer | a fast Beatdown clock |
| **The Brawl** | Walk at them and keep walking | Vanguard · Enforcer · Grinder · Warden | Fixer | Artillery, Pacifier, Prowler |
| **No Formation** | *Deliberately uncoordinated* | none — but must be **mechanically** chaotic | all five | anything with a plan |

**No Formation is the real exception you asked for.** A crew whose lore is that they don't
coordinate declares this. It's exempt from Job coverage — but then the chaos has to be
mechanically true, including for its own player. That's the price of the exemption, and PWNED is
the obvious candidate.

## Proposed crew Formations — drafts

| Crew | Formation | Why |
|---|---|---|
| **Mobb 134** | The Engine | Commandments, Dre tutoring the Bible, a delayed mass payoff. Already true. |
| **Latin Kings** | The Court | Ranked Crowns, "La Familia" buffing all allied Latin Kings. Already true. |
| **Pimp Juice** | The Shakedown | Corazon feeding Energy to collect on it, Dilo, the Convincer. |
| **Shea's** | The Long Night | Alvino's drinks damage both sides. The bar wears everyone down. |
| **Pwners** | No Formation | Dice rolls, glitches, item boxes. **Your call — this is the exemption.** |
| **Fury Park** | *unwritten* | One card. Needs a plan before it needs a Formation. |
| **Icons** | The Congregation | The only Formation that wins on Influence. It's why they exist. |

---

# Part Five — What this lets the tool check

Once Jobs and Formations are data, the consistency engine gets a whole new class of rule. These
are the checks worth having.

**Job ↔ mechanics fit.** Each Job has a signature. A card claiming **Warden** with no Protector,
no protective effect and 6 PA isn't a Warden. *(A warning — signatures are guidance, not law.)*

**Formation coverage.** A crew declares a Formation; do its five cards actually cover the
required Jobs? Right now Mobb 134 would report *no Warden, no Quartermaster* — which is a real
finding about a real crew.

**Job duplication.** Two cards with the same Job in one crew, where the Formation doesn't allow
it. This is the catalogue's swap test made mechanical, and it's a sharper version of the "road"
diversity rule you already have — **a Job is a testable road.**

**Job coverage across the pool.** Which Jobs does no card anywhere fill? That's the design
backlog, and today it would report: *Collector, Boss, Landlord, Recruiter — no cards exist.*

**Faction ↔ Job legality.** Some Jobs shouldn't be available to some factions. An Assholes
**Warden** contradicts their printed lore — *"they don't block."* An Icons **Executioner**
contradicts theirs. This is the faction toolkit rule applied one level up, and it's the check
that stops Jobs from becoming a second, contradictory identity system.

**The counter-web.** The catalogue's triangles translate. Ghost beats Wall; Wall beats Vanguard;
Vanguard beats Ghost. Once Jobs are data the Health screen can show whether the pool has a
functioning counter-web — or whether one Job has no answer anywhere.

---

# What I'd want you to decide before I build

1. **Job as the word** — confirmed, or something else? "Role" is taken by keywords.
2. **Twenty-one Jobs, or fewer?** I'd cut nothing, but the four with no mechanics could sit in a
   separate "not yet built" list rather than the main catalogue.
3. **Which of the five gaps are you actually going to build?** The Boss is the one I'd push
   hardest for — it's expressible today, it's unique to turn-based games, and it's the biggest
   piece of design space you're not using.
4. **Pwners as No Formation** — your call. It's the only crew where the exemption fits.
5. **Are the proposed Formations right?** They're read off the cards you already have, not
   decided. The lore leads.
