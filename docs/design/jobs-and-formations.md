# Jobs & Formations — adapting the role catalogue

The catalogue is written for 5v5 real-time games and 5-person tabletop parties. This game is
neither. This document is the translation: what carries over, what has to be rebuilt in your
mechanics, what to cut, and — most usefully — **the roles the catalogue names that your game
had no way to express.**

> **STATUS — 2026-08-05.** Decided and built. Yorman confirmed "Job" as the word, kept the
> unbuilt Jobs in the main catalogue with a `status` flag, and chose to build **all five gaps
> at once** rather than one at a time: *"I want all of it on the board and then we tweak and
> adjust little by little until it's perfect. But I don't want to tweak and adjust and
> introduce something in the end that will require us to playtest everything all over again."*
>
> Three corrections since the first draft, all his:
>
> **Icons are out.** They are not a crew and not a faction like the others — each is a
> rule-breaker and a one-person army, they represent the designers' mothers, and they are being
> designed **last**. They are now flagged `exempt` in `factions.yaml` and skipped by every Job,
> Formation and toolkit check. The Congregation Formation is deleted with them, the **Legend**
> Job is parked, and Influence is not treated as a live win condition. The **Boss** moved from
> Icons to Assholes for the same reason — parking the most valuable unbuilt mechanic in the
> faction designed last means it never ships.
>
> **Pwners are not the chaotic crew.** *"So far I don't think we have the chaotic crew yet, but
> we will be designing one soon. The chaotic crew is the crew where each one is meant to advance
> a plan of their own, not working together."* Pwners are back to `coordinated` and need a real
> plan like everyone else. See Part Four for what that reframe bought.
>
> **Range now exists.** See Part Three ⑥.
>
> Two counts in the original draft were wrong and are corrected here: the catalogue below was
> described as 21 Jobs and was actually **26**; building the gaps took it to **28**.
> Crew Formation assignments are **on hold** at his request — the lore leads.

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

## 3. Range didn't exist here — and building it was the biggest single change

This was the biggest translation problem, and the answer turned out to be the most valuable
mechanic in the whole exercise. **Range now exists, expressed as time.** See Part Three ⑥ for
the design and Part Four for the Formation it created.

The problem, stated as it was before: most of the catalogue's damage distinctions — Marksman vs Juggernaut vs Skirmisher vs Sniper —
are about **range and mobility**. Your game has neither. Every attack is a Combat Wave clash at
the same notional distance. There's no kiting, no positioning, no dodging, no aim.

So those archetypes didn't collapse into fewer jobs by accident — **they collapsed because the
axis that separated them didn't exist in your game.** What actually distinguishes a damage card
here is:

- Does it attack **PH or MH**? *(PA vs Troll — your second, unused damage axis)*
- Does it **get past blockers**? *(Prowler, Juggernaut spillover)*
- Does it **kill in one hit**? *(Executioner, Hard Removal)*
- Does it damage **without declaring a Combat Wave**? *(Direct Damage effects)*
- Does it hit **everything at once**? *(Mass Removal)*
- Does it **grow the longer it survives**? *(Berserker, stacking)*
- Does it **spend Rounds aiming**? *(Range — new, 2026-08-05)*
- Does it **punish being big**? *(Breaker — new, 2026-08-05)*

The Jobs below are organised by *those* axes. That's the adaptation, not a translation.

---

# Part Two — The Job catalogue

**Twenty-eight Jobs in four families**, now living in [`data/jobs.yaml`](../../data/jobs.yaml).
Each carries a **signature** written in your own vocabulary, so a card can be checked against
the Job it claims — the Studio warns when a card claims a Job it doesn't mechanically look like.

Jobs marked **⚠ NO MECHANICS YET** were the valuable ones — the catalogue named a real position
your game could not fill. **All but one are now built.** The exception is the Legend, which
needs Influence to exist first (OQ-02) and whose only home would have been the Icons.

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

### F4 · Collector — **BUILT 2026-08-05** · *Assholes*
- **Identity** — doesn't stop you attacking your target; makes it the worst available choice.
- **Job** — attach a price to every attack that isn't aimed at it.
- **Signature** — the **Collector** keyword: *whenever an enemy Character attacks any target
  other than this one, that attacker takes 1 permanent PH damage.*
- **Beats** — wide boards, anyone who wants to attack every Round, Vanguards.
- **Loses to** — a patient opponent who simply stops attacking, Silenced, Hard Removal.
- **The line** — Instigator is **compulsion** (you *must* target me). Collector is **taxation**
  (go around, and pay for it). Taxation is the better tool because it leaves the opponent a real
  choice with two costed answers instead of a forced move.
- **Note** — pairs viciously with **Executioner**: everything on their board quietly accumulates
  permanent damage, and permanent damage is what an Executioner hunts.

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

### D5 · Artillery — **REBUILT 2026-08-05** · *Overthinkers*
- **Identity** — spends Rounds aiming, then deletes something.
- **Job** — convert patience into a single strike larger than any defender's PH, at a moment
  of your choosing.
- **Signature** — **Range 2** or **Range 3** · high PA · low PH.
- **Beats** — big single blockers, anyone who has to hold still, opponents at burst range.
- **Loses to** — Stun, Fear, Silence and Bounce (all clear Aim outright), Tokens used as chump
  blocks, and any clock fast enough that two idle Rounds lose the game.
- **The line** — the only Job that is genuinely **helpless while doing its job.** That isn't a
  flaw; it's the reason the entire Front family has employment.
- **Note** — before Range, this Job meant "direct damage" and shared a box with what is now the
  Burner. Range gave it real mechanics and the two separated.

### D5b · Burner — *name not settled*
- **Identity** — damage without ever declaring a Combat Wave.
- **Job** — grind Life Points and Characters down from outside combat entirely.
- **Signature** — Direct Damage 1–5 · low PA · Trigger and Passive abilities rather than attacks.
- **Beats** — Pacifier, Protector, Wall — **everything built to answer combat.**
- **Loses to** — healing, Cleanse, and a clock (it's slow).
- **The line** — the only damage Job **immune to the entire Front family.** That's why it exists.
- **⚠ Name needs your ear.** Split off from Artillery when Range landed. "Burner" carries the
  TCG sense (burn = non-combat damage) and the street sense at once, but it's a placeholder.

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

### S8 · Boss — **BUILT 2026-08-05** · *Assholes*
- **Identity** — gives your best card another action.
- **Job** — manipulate the Phase 2 action economy directly.
- **Signature** — the **Additional Action** effect, 7 points.
- **Beats** — anything that assumed it had one more action than it does, which is every plan.
- **Loses to** — its own printed failure mode (pointing the action at the wrong Character is
  strictly worse than not having it), Silenced, and being killed on the setup Round.
- **The line** — the alternating single action is the game's fundamental unit. This Job attacks
  the currency itself.
- **Note** — **bounded by rule, not by price**: a player may never take more than two
  consecutive actions, so an unbounded chain is impossible rather than merely expensive.

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
- **⚠ STILL UNBUILT — the only one.** Influence is a printed win condition with zero printed
  support, and the only faction that could carry it is the Icons, who are exempt and being
  designed last. Doubly parked. The Health screen reports it as backlog, never as an error.

### X6 · Landlord — **BUILT 2026-08-05** · *any faction*
- **Identity** — edits the rules of the table.
- **Job** — change what's legal for both players, then build a crew that likes the new rule.
- **Signature** — **Arena Rule Edit (Minor)** 2 pts · **(Major)** 5 pts.
- **Beats** — any crew whose plan depends on the rule being edited.
- **Loses to** — a crew that doesn't care about that rule. Entirely context-dependent: S-tier in
  one matchup, blank in another. Also Attachment removal, since an Arena is an object.
- **Note** — Arena text is **symmetric by rule**. A one-sided rule edit is a passive lock with
  no off-switch (P2); a symmetric one is a puzzle. Closes OQ-07.

### X7 · Recruiter — **BUILT 2026-08-05** · *not Assholes*
- **Identity** — fields more bodies than it has cards.
- **Job** — flood the board with cheap Characters that demand answers.
- **Signature** — **Token Generation 1/2/3**, 2 points per 1 PA / 1 PH body.
- **Beats** — single-target removal, Executioner, and **Artillery** (a Token chump-blocks the
  big shot — which is the counter-web doing its job unprompted).
- **Loses to** — Mass Removal, any wide-punishing effect.
- **Note** — not available to Assholes. Solo operators; a crew of hustlers is not a swarm.

### X8 · Breaker — **BUILT 2026-08-05** · *Warmongers*
- **Identity** — punishes being big. *(Filed under Damage in `jobs.yaml`.)*
- **Job** — make a large PH a liability instead of a pure upgrade.
- **Signature** — the **Breaker** keyword: PA plus half the defender's **printed** PH.
- **Loses to** — wide boards of small bodies, Prowler, evasion.
- **The line** — without this Job, stacking PH is strictly correct forever.

---

# Part Three — What the catalogue proved you were missing

The most useful thing an outside framework does is name a position your system can't fill. Six
of those. **All six are now built** — the sections below are kept as written, because the
reasoning for a mechanic is worth more than the mechanic, plus a note on what shipped.

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

## ⑥ Range — the one you found, and the biggest of the six

This wasn't in the catalogue. It came out of the catalogue *failing* to translate: half its
damage archetypes are separated by range and mobility, and you had neither. You proposed three
ways to build it, and the third is the one that fits.

**Range N.** A Character that doesn't attack gains an **Aim** counter at the End Step. Its next
attack deals **printed PA × (1 + Aim counters)**. Range 2 costs 2 points; Range 3 costs 4.

**Why this one and not the other two.** *Attacking without taking a return hit* is first strike,
not range — it makes a card **safer** than everyone else, which is backwards, because what makes
range interesting is that the ranged card is fragile and needs protecting. Print it under another
name. *Flying* is a binary access axis you already have as Prowler/Tracker; adding it means two
evasion keywords and two counter-keywords for one design idea, with no new decision for the
player, and nobody in this world flies.

**Why the third one is better than it looks.** It expresses range as **time**, which is the
currency your balance system is already denominated in — Range 3 literally *is*
`telegraph_rounds: 2`, a plan credit you built and barely used. It generates its own counterplay
(two Rounds where the opponent can Stun, Bounce, Fear or kill it), so it **earns its own
multiplier through machinery already in place**. And it creates the first card in the game that
is valuable, fragile and slow at the same time — which is what finally gives the Front family
something to protect.

**The honest maths.** Two Rounds of Aiming forgoes two attacks to triple one. The totals are
identical. What you buy is the **lump** — a number bigger than any single defender's PH,
delivered in one clash, when you choose. What you sell is two Rounds of being useless and fully
telegraphed. Range is not a damage increase; it's a damage **reshaping**, which is much easier
to balance and much more honest.

**Three guardrails, all load-bearing.** The multiplier applies to **printed** PA only — otherwise
buff-then-multiply is the only deck anyone builds. Aim counters sit **visible on the board**,
because a telegraph nobody can see isn't a telegraph and earns no credits. Stun, Fear, Silence
and Bounce clear aim; **damage does not**, or chip damage trivially answers a two-Round
investment and the card never gets printed.

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

In [`data/formations.yaml`](../../data/formations.yaml). The Congregation is gone with the Icons;
**The Siege** replaced it once Range existed.

| Formation | The plan | Required Jobs | Free slot | Loses to |
|---|---|---|---|---|
| **The Engine** | Build a machine over several Rounds, then detonate it | Setter · Quartermaster · Warden · Wrecker | anything that buys time | Cutoff, pressure before assembly |
| **The Court** | A hierarchy — the top buffs everyone below | Vanguard · Backer · Enforcer · Warden | usually a second Enforcer | Mass Removal, killing the head |
| **The Shakedown** | Take what they have until they can't act | Quartermaster · Silencer · Ghost · Grabber | Spy or Snitch | crews that don't need resources |
| **The Long Night** | Everyone leaves worse, including you | Grinder · Fixer · Wall · Headcase | Enforcer | burst, a fast clock |
| **The Ambush** | End it before it starts | Ghost · Executioner · Grabber · Snitch | Cutoff | a wide board, Cleaner |
| **The Brawl** | Walk at them and keep walking | Vanguard · Enforcer · Grinder · Warden | Fixer | Burner damage, Pacifier, Prowler |
| **The Siege** | Put one enormous shot on the table and spend everything else keeping it alive | Artillery · Warden · Wall · Fixer | Cleaner, or a Burner for a clock while the gun aims | Grabbers, Recruiters, any short race |
| **Every Man For Himself** | Five people advancing five separate plans | *none — see below* | all five | anything with a plan |

**The Siege is the proof that Range did its job.** Before it, nothing in the game was valuable,
fragile and slow at the same time, so the Front family had nobody to protect and a Formation was
a name rather than a structure. Now there's a Formation whose entire premise is *keep the gun
alive*, and every slot in it follows from that.

## Every Man For Himself — the chaotic crew, reframed

The first draft called this **No Formation** and made it an *exemption* from Job coverage. That
was wrong, and your correction is what fixed it.

> *"The chaotic crew is the crew where each one is meant to advance a plan of their own, not
> working together."*

That is a **mechanical claim**, and a mechanical claim is checkable. So it isn't an exemption
from validation — it's its own validation rule:

> **No card in this crew may require a board state that another card in the same crew produces.
> Zero enabler chains inside the crew.** Also forbidden: cards that reference their own crew by
> name, or that buff or protect allied members of it — "all allied *&lt;crew&gt;*" is a
> coordination effect by definition.

The elegant part: this is enforced with **the exact same producer/requirer graph that caught Dre
feeding Moammar**. The tool built to find unwanted combos is precisely the tool that proves this
crew has none. It's rule **F12**, and it's a hard error.

**And the exemption has to buy something.** These cards permanently forgo comboing with each
other, which is the single biggest source of power in the game. So each one is allowed a higher
individual rate — a chaotic crew is five *good* cards, not five weak ones. Without that, nobody
would ever choose it and the Formation would be decorative.

**Not Pwners.** They're back to `coordinated`. Their randomness is a **texture, not a plan** —
how they do it, not what they're doing — and they need a real game plan like every other crew.
Every Man For Himself is unassigned until the chaotic crew gets designed.

## Crew Formations — ON HOLD

> *"I don't know if they are right yet, I need to spend more time thinking about it."*

Correct call, and it's the rule working. Lore leads → the plan follows the lore → the Formation
follows the plan. Every assignment I drafted was read off the cards that already exist, which is
that rule running **backwards**. No crew carries a `formation:` key; the drafts sit commented out
in `formations.yaml` as a starting point for when you come back to it.

The two I'd defend hardest are Mobb 134 → The Engine and Latin Kings → The Court, because those
are already mechanically true on the printed cards rather than inferred. Fury Park needs a plan
before a Formation means anything at all.

---

# Part Five — What the tool now checks

All of it is built. `python tools/check.py` runs these with everything else, and the Studio
shows them live.

| Rule | What it catches | Severity |
|---|---|---|
| **F11** Job legality | A card declares a Job that doesn't exist, or one its faction may not hold | **error** |
| **F12** Chaotic enablers | A crew claims `chaotic` but one card requires what a crewmate produces | **error** |
| **W12** Job signature | A card claims a Job but carries none of its signature tools | warning |
| **W13** Formation coverage | A crew's five cards don't cover the Jobs its Formation requires | warning |
| **W14** Job duplication | More cards share a Job than the one free slot allows | warning |
| **W15** Jobs undeclared | Cards with no Job at all — **one finding for the whole pool**, not one per card | warning |
| **GAP** Job coverage | Which Jobs nobody in the pool plays. The design backlog. | gap |
| **GAP** Unbuilt Jobs | Jobs the rules still can't express. Listed, never flagged. | gap |

Notes on why they're shaped that way:

**Legality is an error, signature is a warning.** An Assholes **Warden** contradicts printed
lore — *"they don't block"* is the same sentence that puts Counterspell on their `never` list —
so that's a hard stop. Whether a card *looks* like a Warden is judgement, so that's a nudge. The
Studio shows the two differently: a red block for the first, an amber note for the second.

**W15 reports once, not thirty times.** A linter that fires for every card missing the same field
teaches you to ignore the linter. That lesson came from W9 firing four times per card.

**Job coverage is the most useful output.** Today the Health screen reports Front **0/4**, Damage
**1/9**, Support **0/8**, Specialist **1/6** — every empty cell is a card waiting to be designed,
and it's a far more actionable backlog than "you need 24 Descendants."

**Faction ↔ Job legality is what stops Jobs becoming a second identity system.** It's the faction
toolkit rule applied one level up, and it's derived from the toolkits rather than declared
separately, so the two can't drift apart.

**Icons are skipped by every rule here**, via `exempt: true` in `factions.yaml`. Coherence checks
would report their design intent as a defect.

**Not yet built: the counter-web.** The catalogue's triangles translate — Ghost beats Wall, Wall
beats Vanguard, Vanguard beats Ghost — and once enough cards carry Jobs the Health screen could
show whether the pool has a functioning counter-web or whether some Job has no answer anywhere.
It needs cards first; with two Jobs assigned it would render an empty graph.

---

# Where this stands

**Built:** the rulebook layer (Range, Tokens, Arenas, Additional Actions), the pricing layer
(4 keywords, 6 effects, faction assignments), `jobs.yaml` and `formations.yaml`, six validation
rules, and the Studio surfaces for all of it.

**Deliberately not done:** crew Formation assignments (on hold — the lore leads), and the
re-scoring pass over the existing 31 cards. That last one is by design: the rules and pricing
had to stop moving first, which was your own constraint.

**Open, and yours:**

1. **The Burner's name.** Split off from Artillery when Range landed. Placeholder.
2. **28 Jobs is a lot of taxonomy for a 31-card pool.** The risk is that assignment becomes
   arbitrary. The mitigation is that Formations only ever *require* 12 of the 28, so the long
   tail is descriptive rather than load-bearing — but it's worth watching for cards whose Job
   feels like a coin flip.
3. **Two Jobs are seeded** as a demonstration — Dre as Setter, Moammar as Enforcer. Every other
   card is unassigned. Both are changeable in one click.
