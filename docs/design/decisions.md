# Decision Log

Append-only. Newest at the top. When an open question in
[`open-questions.md`](open-questions.md) gets resolved, the reasoning lands here and the OQ is
marked `DECIDED`.

**Format**

```
## D-000 · Short title — YYYY-MM-DD
**Decides:** OQ-xx (or "new")
**Decision:** what we're doing, in one or two sentences.
**Because:** the reasoning. Include what was rejected and why — future-you will want it.
**Affects:** which cards, rules, or data files change.
**Revisit if:** the condition that would make us reconsider.
```

---

## D-016 · The contract is generated, and check.py can finally see generated drift — 2026-08-06

**Decides:** new (tooling) · completes F13

**Decision:** `CLAUDE.md` is canonical and **`AGENTS.md` is generated from it** as a byte-identical
mirror, by `python tools/generate.py`. And a new rule **F14** makes `check.py` block on *any*
generated content that no longer matches its source — the three whole-file targets, the §6 region,
and all 31 card bodies.

**Because:** two separate problems, one of them mine.

**The drift was self-inflicted.** At `HEAD` the two contract files were already byte-identical
(12449 bytes each, zero diff). The divergence was created in the working tree on 2026-08-05 when
hard rule 6 was rewritten in `CLAUDE.md` and not in `AGENTS.md` — by me, during D-013. `README.md`
sends human collaborators to `AGENTS.md`, so for the length of that session anyone following the
README got a contract that still described three generated documents and said nothing about card
Rules Text being generated. The failure mode is precise: **they would have hand-edited a card's
Rules Text and been told it was fine.** F13 was written to detect exactly that, and did.

**But F13 only detects.** Fixing it meant copying one file over the other by hand — the same
manual sync that caused the drift. Generation removes the discipline requirement: one command,
and the mirror cannot be wrong. Kept **byte-identical rather than banner-topped** on purpose, since
a "do not edit" banner would make the two files differ forever and F13 compares bytes. The
do-not-edit instruction lives in rule 6 instead, which both copies carry.

**The larger hole was that `check.py` was blind to all of this.** Measured: hand-editing
`docs/rulebook/12-keywords.md` left `check.py` at 35 blocking errors, never mentioning the file.
Only `generate.py --check` caught it. Hard rule 5 says *"check.py is the one that matters — it
validates all three levels at once,"* and hard rule 6 now lists five kinds of generated content
including every card's rules text. So the one command everyone is told to run could not see the
entire class of drift that rule 6 exists to prevent. **A rule the tool cannot check is a
convention, not a rule.**

**Verified by breaking it four ways**, each reverted:

| Hand edit | Before | After |
|---|---|---|
| whole generated file (`12-keywords.md`) | 35, silent | **36, F14** |
| generated region (`06-character-anatomy.md`) | 35, silent | **36, F14** |
| a card's Rules Text, frontmatter untouched | 35, silent | **36, F14** |
| the contract mirror | 36, F13 | **36, F13** |

The third case initially read as a miss and was a bad test, not a bad rule: the string I mutated
appears in *both* the frontmatter `immersion:` and the generated body, so replacing it changed the
source too and the two legitimately agreed. Mutating only the body catches it.

**F13 is kept rather than folded into F14.** It gives a far better diagnosis for the contract pair
— differing line count and the first line number — and F14 skips that pair so nothing is reported
twice. F13's fix text now points at `generate.py` instead of a manual copy.

**Affects:** `tools/generate.py` (`CONTRACT_MIRROR`), `tools/rules.py` (F14, F13's fix text),
`CLAUDE.md` rule 6 (the table gains a sixth row and states which file to edit), `README.md`,
`AGENTS.md` (now generated). **Verified:** `check.py` unchanged at 35 blocking with everything
fresh, so F14 has no false positives; `generate.py --check` clean on 6 targets; the two contract
files hash identically.

**Revisit if:** a third filename joins the pile (`GEMINI.md`, `.cursorrules`). `CONTRACT_MIRROR` is
a dict for that reason — add the name, and both the generator and F14 pick it up.

---

## D-015 · "Role" is retired; a keyword is a keyword — 2026-08-06

**Decides:** new (vocabulary) · simplifies D-009 and D-013

**Decision:** the word **Role** is gone. A faction-exclusive mechanic is a **keyword**, full stop.
§12 is now titled *"Faction-Exclusive Keywords."* The ability record's field is `keyword`, not
`role`, and the Studio's dropdown is labelled **Keyword**.

**Because:** Yorman asked what the difference between a Role and a keyword was. There wasn't one —
§12's own title read *"Exclusive Keywords (The Roles)"* and its first line said *"Keywords are
Roles a Character plays."* One concept, two names, and the question proves the cost: if the person
who commissioned the game can't tell them apart, no player will.

Three specific harms, all measured rather than asserted:

1. **The synonym cost a paragraph of disambiguation everywhere it appeared.** `data/jobs.yaml`,
   `tools/rules.py`, `tools/studio.html` (three places), `docs/design/jobs-and-formations.md` and
   both contract files each carried prose whose *only* job was explaining that a Job isn't a Role.
   Every one of those paragraphs is now shorter or gone. **S7** asks that an addition retire
   something; this retirement pays S7 back directly.
2. **The two words are swapped from where intuition puts them.** "Role" reads like a position —
   which is exactly what a **Job** is. The synonym was actively pointing readers at the wrong
   concept, which is why D-009 needed a whole section titled "It's called a Job, not a Role."
3. **It was never load-bearing.** "Role" appeared in two sentences of actual rules text. The file
   is `keywords.yaml`, gate **G4** is "faction keyword exclusivity", and the Studio's chip list
   says keywords. The word was decoration with a maintenance cost.

**Rejected: retiring "keyword" instead** and keeping Role as the printed term. Defensible —
`(Passive Ability · Juggernaut)` is a Role-shaped thing, and "Role" reads better on a card. It
loses because the *machine-facing* name is the one that has to be unambiguous: the data file, the
gate, the scorer and the Studio all say keyword, and renaming those to match a card's voice is a
much larger change for a smaller gain.

**The rename is text-invisible.** All 11 `role:` fields across 9 cards became `keyword:`, and
`print_ability()` builds the slot identically either way — verified by printing every affected
slot before and after (`(Protector)`, `(Passive Ability · Juggernaut)`, and nine others,
unchanged), and by `render(load(p))` staying byte-identical for all 31 cards.

**A regression guard ships with it.** `tools/test_abilities.py` now scans every `.md`, `.yaml`,
`.py` and `.html` file in the repo and fails if any uses `Role`. It found five hits I had already
missed by hand — `data/README.md`, `data/jobs.yaml`, and three separate pieces of UI copy in
`studio.html` — plus my own explanatory parentheticals in `CLAUDE.md`/`AGENTS.md`, which are gone
too: the contract should not have to explain a word it no longer uses. Exempt from the scan:
`decisions.md` (append-only history), `docs/superpowers/` (dated design records),
`jobs-and-formations.md` (it documents the retirement) and `.claude/` (tooling state).
`tools/fonts/README.md` used "Role in the system" as ordinary English about typefaces; it was
reworded rather than exempted, because a per-file exemption would hide a real hit later.

**Earlier log entries keep the word on purpose.** D-009 and D-013 describe systems as they were
when written, and this file is append-only — superseding is the convention here, not editing. A
reader hitting "Role dropdown" in D-013 should land on this entry, which is why it names them.

**Affects:** `tools/generate.py` (§12's heading and lead, then regenerated),
`docs/rulebook/README.md`, `data/keywords.yaml`, `data/jobs.yaml`, `data/README.md`, `README.md`,
`tools/rules.py`, `tools/card_io.py`, `tools/scoring.py`, `tools/migrate_abilities.py`,
`tools/studio.html`, `tools/fonts/README.md`, `tools/test_abilities.py`, `CLAUDE.md`, `AGENTS.md`,
`docs/design/jobs-and-formations.md`, `docs/design/open-questions.md` (OQ-18),
`docs/lore/_crew-template.md`, and 9 card files. **Verified:** 29 assertions pass including the new
guard; `generate.py --check` clean; `check.py` unchanged at 35 blocking; round-trip byte-identical.

**Also noticed, unrelated:** `CLAUDE.md` and `AGENTS.md` have drifted — they are meant to be the
same contract and their hashes differ. Both were edited here; the wider divergence is untouched
and worth a look.

**Revisit if:** printing `(Passive Ability · Juggernaut)` on a physical card reads badly enough
that the *card face* wants a friendlier word. That is a card-layout decision and can be made
without reviving the synonym in the data model.

---

## D-014 · The game is named Known Associates — 2026-08-06

**Decides:** new (product) · does **not** close WG1

**Decision:** the game is **Known Associates**. The founding edition is **Known Associates:
Local Legends**. The city is still unnamed — lore gate **WG1** is untouched and still blocks the
Timeline, Places and Arenas.

**Because:** the name had to do the one job no other TCG can do — say *these are real people*
before anybody reads a card. `canon.md` fixes the register as *hard, funny, mythologizing,
present-tense, specific — a neighborhood treated like an epic, never winking at the reader*, and
that sentence killed most of the field on its own.

**Known Associates** is the police-file term for the people you run with. It is hard (cop
language), funny (applied to your friends), and mythologizing without ever explaining itself. It
also describes the crew system structurally: crews are **loyalty, not methodology** — they are
literally associations. And it is *relational*, so the player is implied as the subject of the
file rather than a spectator.

**Local Legends** is the phrase for someone famous inside three blocks, which is the canon thesis
said out loud. It lost as the *game* name for being nostalgic where the register says
present-tense, and for pointing at the cast instead of putting the player in it. As an *edition*
name both faults invert: an edition is allowed to be a retrospective label for one specific cast,
and the founding 31 are exactly a set of local legends.

**Rejected:**

- **Equilibrium / Balance / Parity.** The original instinct. Abstract, Latinate, the register of a
  design document rather than of Shea's. It also names the *engine* — the Score, the Ceiling, the
  four prohibitions — which is invisible to a player. Nobody buys a game named after its budget
  formula.
- **Even Money · Pound for Pound.** Both strong. The first is literal equilibrium in gambling
  idiom; the second is the exact boxing phrase for a hypothetical fight. Both name the
  *argument*, and any game can host an argument. Only this one has the roster.
- **Street Names.** Best pun in the field — alias plus geography, and it would have tied the
  naming conceit into the Arena gap (OQ-07). But "street" is the most worn word in the genre, and
  it fits PWNED and the Icons worst of every candidate.
- **Next of Kin.** Devastating alongside permadeath (§10), and unclaimed in TCG space. Hard, but
  not funny — the register demands both, and this one is all funeral.
- **A.K.A.** Names the card layout (`Name, The Epithet`), not the premise. Three letters is an
  unsearchable brand.

**The Icons do not fit the name, and that is the point.** A mother is kin, not an associate.
`data/factions.yaml` already carries `exempt: true` — *"ICONS ARE DELIBERATELY OUTSIDE THE
SYSTEM"* — and the name excluding them hardens that status rather than exposing a hole.

**PWNED was the real test, and it passed.** Applying police-file language to *Fernando, The
Dualshock Disciple* and *Lenny, The Kawaii Connoisseur* is funny in exactly the direction the
register asks for. That is the mythologizing move, performed on a basement.

**The standing constraint — the name is used flat.** Applying cop language to a friend group is
ironic, and irony is winking's neighbour. It stays on the right side of the register only if
nothing printed ever *acknowledges* the joke: no card, no flavour sentence, no rulebook line. Now
recorded in `canon.md` as a lore constraint.

**"Edition" is branding, not a rules term.** Nothing in `02-deck-construction-and-zones.md`
references a set, and nothing may until the rulebook defines set legality in the same change
(hard rule 1). Naming an edition creates no rotation, no set symbol and no format legality. A
note saying so ships in §1 with this change.

**Affects:** `README.md`, `AGENTS.md`, `CLAUDE.md`,
`docs/rulebook/01-overview-and-win-conditions.md`, `docs/design/canon.md`. No card file, no
`data/` file, and nothing generated changes. **Verified:** `generate.py --check` clean;
`check.py` reports **35 blocking errors with the change stashed and 35 with it applied**.

**Revisit if:** a trademark clearance search turns up a live Class 28 registration for *Known
Associates*; or the world drifts far enough from the crime frame that police-file language stops
reading as ironic and starts reading as simply wrong.

---

## D-013 · An ability is data, not a sentence — 2026-08-05

**Decides:** implements the structured-abilities spec · files OQ-18

**Decision:** every ability is a record in card frontmatter — `name`, `type`, `immersion`,
`mechanics`, optional `requires` and `role` — nested inside the `base` / `ascended` blocks. The
printed `### Rules Text` sections are **generated** from those records by
`card_io.print_ability()`. Gate **G3** reads the `type` field. `data/ability-types.yaml` owns the
four types and generates §6's table. The Studio gained a per-ability editor: add, delete, reorder,
a Type dropdown from the data file, and a Role dropdown filtered to the card's own faction so
**G4 cannot be violated by construction**.

**Because:** G3 once told Decoy that `[Improved Sangre Por Sangre]` "declares no ability type"
while the card plainly read `(Fast Ability)`. One stray colon defeated the regex, and the gate then
asserted absence **from its own failure to parse**. Eight separate scrapers read the same prose.
The defect was never the pattern; it was that a rules term the machine has to check was living in
a sentence.

**Measured before writing code, and the spec was wrong in three ways that mattered:**

| The spec said | Actually |
|---|---|
| 70 abilities, 57 canonical, 12 untyped | 70 ✓, but **59** canonical, **10** Role-in-type-slot, **1** slotless |
| 23 abilities are hand-soft-wrapped; collapse them | **Zero** mid-sentence wraps. Those 23 put flavour on its own line — the newline **is** the immersion/mechanics boundary |
| The immersion/mechanics split is a guess for all 70 | Derived for **23**, guessed for **44**, N/A for 3 tables |

The second one nearly caused real damage. Collapsing those newlines would have destroyed the only
signal in the corpus that locates the flavour/rules boundary — the exact field split the whole
change exists to create. **The design's cleanup step would have deleted the design's own input.**

**The safety property, restated.** The spec asked that a card be refused if its regenerated text
differs from the original beyond whitespace. Run as written, that refused three cards — and all
three were the spec's *own* named intended fixes (Decoy's stray colon, Dilo's missing space after
the colon, a Role moving into the printed slot). So the property was aimed slightly wrong. It now
guarantees that **not one word of rules prose changes**, and reports header-slot changes separately
for review. Result: **0 refusals, 2 declared slot normalisations, 70 abilities migrated.**

**A defect found in my own migration heuristic.** The first version filed a single-sentence body as
`immersion`, which put pure rules text — Enzo's *"When he attacks, he temporarily increases his
Physical Attack (PA)…"* — into the flavour field on 10 abilities. That is precisely the lossy step
the spec's §9 warned would go unexamined once it was in fields. Fixed with a rules-vocabulary test,
**tuned against all 70 candidates rather than guessed**: an early draft matched `inflict` and
`Murder`, which are ordinary English too, and misread Decoy's *"more agonizing than anything the
enemy could inflict"* as mechanics. The final pattern flags 8 of 70, and all 8 genuinely have no
flavour written for them.

**Rejected:** collapsing every ability to one line, per the spec. It would have changed the printed
text of 22 cards *and* destroyed the split signal. Generation now puts flavour on the header line
and rules underneath — which is how 23 abilities were already written by hand, and is lore rubric
**D3** ("flavor explains rules") expressed as layout.

**Two things migration refuses to guess**, both real design work it converts from hidden to
visible: the 10 missing ability types (OQ-18 — `check.py` is the worksheet) and `requires`, whose
split a round-trip check cannot validate because both orderings concatenate to identical text.
`requires` is left empty everywhere; it is schema-legal and prints identically.

**Also fixed, both pre-existing and both found by testing rather than reading:**

- **`06-character-anatomy.md` needed partial generation.** Its table is derived but the section is
  mostly hand-written prose, so `generate.py` gained delimited-region targets rather than dragging
  the rulebook's voice into Python. Card bodies joined the staleness check at the same time.
- **Saving an unchanged card still rewrote the file.** The browser always sent an empty
  `plan: {pays: {}, windows: []}` skeleton, so `git diff` could never answer "did I change
  anything?" on the one screen where that question matters. `apply_edit` now drops a plan that
  declares nothing.

**Affects:** `data/ability-types.yaml` (new), `tools/migrate_abilities.py` (new),
`tools/card_io.py` (ability records, print grammar, literal-block YAML dumper),
`tools/scoring.py` (G3), `tools/generate.py` (regions + card bodies), `tools/studio.py`,
`tools/studio.html` (the editor, field-based client-side G3), all 26 cards with rules text,
CLAUDE.md rule 6. **Verified:** `render(load(p))` byte-identical for all 31 cards *after*
migration; the only text changes across the corpus are the 3 declared normalisations; `generate.py
--check` clean on 5 targets including 31 card bodies; a Studio save is byte-idempotent; F6 rose
from 3 to 11, which is the gate getting honest.

**Revisit if:** a fifth outcome table appears. Three abilities hold die-roll tables as opaque block
scalars, and nothing checks that a d6 table covers 1–6 exactly once. That is the right trade at
n=3 and a known blind spot, not an oversight — at n=5 the `outcomes:` schema stops being
deferrable.

---

## D-012 · Caches key on their sources, instead of being cleared by hand — 2026-08-05

**Decides:** new (tooling)

**Decision:** every cached loader in `tools/` is now declared with
`@card_io.cached_on("<source>")`, which memoises it against its own sources' modification times.
A hand edit to any `data/*.yaml`, any card, the rulebook or the art folder is visible on the next
call, in the same process, with no invalidation call anywhere.

**Because:** there were **eight** `@lru_cache(maxsize=1)` loaders reading files off disk, and
`studio.py` cleared six of them, on some paths. So the Studio answered from files that no longer
existed on disk — and did it silently, which is the actual defect: a stale table still answers
every question asked of it, confidently and wrongly.

The symptom does not look like staleness. `data/effects.yaml` gained `Mass Status Application`
(D-010); a running Studio had never heard of it; unknown effect names are a hard error by design,
so a refresh reported **a broken card** rather than a stale server. `art_index()` was never
cleared anywhere, so a newly added art file was invisible to G8 the same way.

**The root cause was the shape, not the missing lines.** Enumerating caches at the call site means
the list has to be complete and stay complete — and it never was. `bootstrap()` cleared
`plan_config` alone; `rename_library_entry()` cleared six; the correct set was written out two
hundred lines away from the place that needed it. Adding a loader silently re-opened the bug.
Keying on mtime moves the knowledge next to the loader, where it cannot be forgotten, and fixes
it for the CLIs at the same time rather than only for the Studio.

**Rejected:** adding the four missing `cache_clear()` calls to `bootstrap()`. Fixes today's
symptom and leaves the trap armed for the next loader. This exact repair had already been made
once, for `plan_config` alone, with a comment explaining the bug class — and the bug came back
anyway, which is the evidence that the repair does not hold.

**The explicit clears are kept on write paths** (`write_table`, `findings_payload`,
`rename_library_entry`) and are now belt-and-braces with a stated reason: a rewrite landing inside
one filesystem clock tick at an identical byte length is the one change an mtime stamp cannot see,
and a write followed immediately by a read is exactly where that can happen.

**Affects:** `tools/card_io.py` (`source_stamp`, `cached_on`, `art_index`), `tools/scoring.py`
(5 loaders), `tools/rules.py` (`load_world`, `defined_terms`), `tools/studio.py` (comments and one
removed call). **Verified:** `check.py` reports an identical 27 blocking / 80 warnings with an
identical code breakdown; `generate.py --check` clean; `card_io` round-trips all 31 cards
byte-identically; median `check.py` runtime unchanged at 0.21s across 3 runs; and a live test
edits `data/effects.yaml` mid-process and sees the new entry through both `effect_points()` and
`load_world()` with no `cache_clear()` call.

**Revisit if:** a loader ever needs to depend on something outside the repo, which `source_stamp`
cannot fingerprint — it resolves paths against `REPO_ROOT` only.

---

## D-011 · Exhausted halves attack; the rulebook loses one — 2026-08-05

**Decides:** OQ-08 · splits out OQ-17

**Decision:** **Exhausted halves both PA and MA, rounded down.** Halving is a multiplier, so it
applies to the **printed** value and buffs are added afterwards — a printed 5 PA with a +2 Attachment
attacks for `(5 ÷ 2 → 2) + 2 = 4`. The rulebook's "+1 Energy to declare them as an attacker" is
retired.

**Because:** the two definitions were not two wordings of one idea, they were a **tax** and a
**debuff**, and they would price differently. What broke the tie was a card. Caleb's `[Teabag]`
applies Exhausted on a 1–3, so half his base side was undefined text — and his Level-Up counts enemy
Characters that die *while afflicted*. Halved attack makes afflicted Characters lose fights and die
afflicted; a tax on declaring an attacker does nothing toward that at all. One definition makes his
card work and the other makes it inert, which is a stronger argument than either definition had on
its own.

**Why the rulebook lost, which is not the normal order.** Source-of-truth order exists so conflicts
resolve without argument, and the rulebook wins by rule. But it had been winning here **by default
rather than by decision** — nobody ever chose the tax; it was simply the text that happened to sit in
the higher-priority file while the spreadsheet said something else. Deferring to authority in that
situation preserves an accident. The order still holds for genuine disputes.

**Rejected:** keeping the +1 Energy tax and striking the Elements definition. Cleaner on process, and
it costs Caleb his level-up. Also rejected: printing **both** as two statuses. That is a 7th status
for one idea, and **S7** already counts six.

**Also fixed, one word:** §8 Phase 1 read *"turn all horizontally exhausted cards in your Resource
Row vertically"* — using "exhausted" for a tapped Resource Row card while **Exhausted** is a status
name. §7 already owns that vocabulary as **Used** / **Unused**, so §8 now says "Used" and links to
it. No rules change; it removes a collision with the status this decision just rewrote.

**Affects:** [§11 Status Effects](../rulebook/11-status-effects.md),
[§8 Round Structure](../rulebook/08-round-structure.md), `data/status-effects.yaml` (conflict warning
removed), and **Caleb** — the only card in the pool that references Exhausted, verified by grep
across `cards/`, `data/` and `docs/`. No pricing changes: Exhausted is charged as
`Status Application (Minor)` either way.

**Revisit if:** halving turns out to be fiddly in play. Two Characters halving each other, or a
halved Character being buffed mid-Round, are the arithmetic to watch — the tax version was uglier
thematically but trivial to resolve at the table, and that is the trade being made.

---

## D-010 · Four primitives the Pwners cards assumed existed — 2026-08-05

**Decides:** new · gives OQ-04 its first pricing lever · files OQ-16

**Decision:** Caleb, Julito and Ruvi were ported from the spreadsheet with their text intact, and
that text quietly assumed four rules the game did not have. All four ship:
**Randomization** ([§14](../rulebook/14-randomization.md)), **Counters**
([§13](../rulebook/13-glossary.md)), **Descent** ([§10](../rulebook/10-ascendants.md)) and
**Trigger discipline** ([§6](../rulebook/06-character-anatomy.md)). Then the three cards were
rewritten against them. **No new ability type was needed** — Standard / Fast / Trigger / Passive
covers all nine abilities on the three cards; everything missing sat in a layer below ability types.

**Because:** three of the four were load-bearing for text already printed, and the fourth was a
contradiction in §6. Two collisions in particular were not tuning problems:

1. **"EX Meter token" collided with Token.** §5 defines a Token as *a Character created by an
   effect* and adds that it is "a Character for every rule." Julito's accumulator therefore read,
   literally, as creating up to three Characters. The word had to become **Counter**.
2. **Ruvi's global Silence was Pacifier.** A continuous Passive means Cleanse can never answer it —
   the Passive re-applies — so only removal can, which is **P2** and the exact reasoning that ruled
   Pacifier prohibited in OQ-09. It became an activation: once per Round, 2 Energy, until the End
   Step.

**Counters were chosen over a new word because the addition retires a special case instead of
adding one.** Aim already worked this way privately inside Range; naming the primitive makes §9
an instance of it and needs no edit to §9 at all. That is the only kind of addition **S7** likes.
The one real cost is that the glossary now holds both *Countering* (verb, negate) and *Counter*
(noun, marker), so both entries carry an explicit disambiguation.

### Randomization — and why a random effect is priced at its best outcome

Nothing in the rulebook defined a die roll, though two cards roll one and `data/crews.yaml` names
randomness as the Pwners' crew signature. **G6 already lists "random" as a legal answer to *who
chooses the target*,** so this was a sanctioned gap rather than a violation.

The sealed-roll rule is the load-bearing one: the roll happens inside resolution and neither player
may act between the die landing and its effect. Otherwise every d6 opens a timing window the Combat
Wave has no step for, and the Stack needs a second layer. A roll is a **telegraph**, not a window.

**Pricing, defended against two existing entries:** a random effect costs its **most expensive
outcome**, and a bad branch earns **no** credit. `data/effects.yaml` has never priced by frequency —
`Direct Damage/Heal 4` costs 4 whether or not you draw it. And **Range 3** charges 4 for the ×3
shot, not the average of aiming zero, one or two Rounds; a variable outcome priced at its ceiling
was already the precedent. **Rejected: expected value.** It makes variance a discount, which makes
the swingiest card the most point-efficient card, which drifts the whole set toward slot machines.
The second half is not decoration — crediting a one-in-three downside while charging the best upside
prices the same variance twice in opposite directions.

Measured consequence: this alone takes Ruvi's base side from 21/19 (over) to 17/19 (under), because
his frontmatter was paying for every branch of the Item Box rather than its biggest.

### Descent — the first thing that makes OQ-04's second face cost something

An Ascendant may be told **by its own text** to flip back down. Damage carries, statuses and
Counters persist, the Level-Up condition goes live again, and the Safety Net extends to cover it —
a flip is not active damage, so a Descent into insufficient Health sets the Character to 1 rather
than Murdering it.

**No effect may force an opponent's Ascendant to Descend.** A forced Descent is removal that
invalidates every Level-Up condition in the game for a fraction of Hard Removal's price.

**Why it ships for one card, against MG4.** MG4 wants three cards' worth of design space and
Descent has exactly one. It ships because it is a direct lever on **OQ-04**, the largest known hole
in the balance system: the ascended side is free precisely because nothing can ever take it away.
An ascended side a card can **spend** is an ascended side with a price. **Pricing:** below
`characters_consumed` (5), because you keep the body and may re-ascend; equal to
`board_state_required` (4), because re-ascending is that state engineered again. **4.**

### Mass Status Application — 6, and the pricing smell that comes with it

**Pricing, defended against two existing entries:** **Arena Rule Edit (Major) = 5** is the same
shape — *"forbids or forces an entire category of action, symmetrically for both players"* — so
price above it, because an Arena is a destroyable object and a Character carrying the same effect is
not, and because the symmetry is partly false (Ruvi's own abilities keep working). **Mass Removal =
8** is the upper bound: it ends the board permanently, this ends at the End Step. **6.**

**Recorded because it is a real smell:** at 6 Ruvi lands at exactly 28/28. At 7 he fails F4 by one
point. The band 6–7 is defensible on its own merits, but 6 is the end of the band that happens to
make the card legal, and deriving a mechanic's price from what one card needs is backwards. Treat 6
as a v0.1 hypothesis and revisit it the moment a second card wants the entry — not by asking
whether Ruvi still passes.

### Warmonger non-combat removal — the constraint held

Shun Goku Satsu was a 1-Energy Fast targeted non-combat Murder. OQ-09 and gate **G7** both lean on
"the Warmongers have no printed non-combat removal" as a defining constraint, and Executioner only
ever Murders a *defender*, in combat. Yorman's call, 2026-08-05: **the constraint holds and Julito
retunes.** It became a Trigger resolving in **Step 4** of the Combat Wave — the slot §9 already
documents for "Executioner mechanics and other damage replacements" — so it needed no new timing
rule at all. **Rejected:** printing the Fast Murder as a documented one-card faction privilege,
which weakens the constraint two gates cite and invites the next Warmonger to ask for the same.

**Two pricing corrections found while retuning Julito, both findings rather than nerfs:**
`Multiple Attacks` (5) was charged for something his text never granted — **Combo-Striker already
is** "attacks resolve in two strikes" — and `+2 PA and +2 PH` is two stat axes priced as one
`Permanent Buff 2`. He cannot credit his way out of the remainder, because `cost_tests.bite` rates a
cost that **is** the plan at 0.0 and a Warmonger accumulating counters by winning fights is doing
his job. Hence **cost 4 → 5**: verified at cost 4 the corrected card is base 20/16 and both faces
27/24, failing both checks; at cost 5 it is base 20/19 (inside ±1) and both faces 27/28.

**Also decided:** **Bricked is flavour, not a status** — it was Stunned + Silenced stapled together,
and a 7th status for that does not clear **S7**. Caleb's reboot moved from the opponent's Phase 2
action to the **End Step**, because the action cost was the P2 violation: application cost Caleb one
action, removal cost the opponent two on average, so application beat removal on rate. And
`[The Glitch]` keeps the Reaction Window open — only the damage is unpreventable — because CLAUDE.md
names the alternating-action window as the game's best structural asset.

**Affects:** rulebook §6, §10, §13, §14 (new), README; `data/effects.yaml`,
`data/plan-credits.yaml`; `balance-philosophy.md`; all three Pwners cards named above;
`open-questions.md` (OQ-16 filed, OQ-08 annotated). Full design:
[`../superpowers/specs/2026-08-05-pwners-rules-primitives-design.md`](../superpowers/specs/2026-08-05-pwners-rules-primitives-design.md).

**Revisit if:** a second card wants `Mass Status Application`, which is when its 6 gets tested on
its merits instead of on Ruvi's margin. Also if Descent stays a one-card mechanic through the next
set — at that point it is Julito's ability wearing a rulebook section, and MG4 wins after all.

---

## D-009 · Jobs and Formations — the crew's fighting structure becomes data — 2026-08-05

**Decides:** new

**Decision:** Every Character declares one **Job** — what it does for its crew — from
[`data/jobs.yaml`](../../data/jobs.yaml) (28 Jobs in four families). Every crew declares one
**Formation** from [`data/formations.yaml`](../../data/formations.yaml) (8), which names four
required Jobs and leaves the fifth slot free.

**Because:** "Role" was already spent — the rulebook says *"Keywords are specific Roles that a
Character plays on the Board."* A Job is the position; a Role is one of the tools. The source
catalogue Yorman supplied argues that "role" is really six independent axes, but four of those
already existed here under other names (keywords are delivery, the Investment Engine is
resource economy, The Score's credits are the power pattern, the three victories are the
pillars). Only Team Job was genuinely new, so only Team Job was added — adding all six would
have double-counted.

**Rejected:** treating a chaotic crew as *exempt* from validation. "Uncoordinated" is a
mechanical claim and therefore checkable, so `Every Man For Himself` is its own rule
(`no_internal_enablers`, F12) enforced with the same producer/requirer graph that caught Dre
feeding Moammar. The exemption also has to buy something — a chaotic crew permanently forgoes
comboing, so its cards get a higher individual rate — or nobody would ever choose it.

**Affects:** `data/jobs.yaml`, `data/formations.yaml` (new), `card_io.new_card()` (`job:` in
the schema), rules F11/F12 and W12–W15, the Studio's Cards, Crews and Health screens.
**Crew Formation assignments are deliberately unset** — lore leads, the plan follows the lore,
the Formation follows the plan, and reading assignments off existing cards is that rule running
backwards. On hold at Yorman's request.

**Revisit if:** 28 Jobs turns out to be too fine-grained to assign consistently. The tell would
be cards whose Job feels arbitrary. Note that Formations only ever *require* 12 of the 28, so
the long tail is descriptive rather than load-bearing.

---

## D-008 · The action economy is bounded by rule, not by price — 2026-08-05

**Decides:** new

**Decision:** `Additional Action` (7 points, Assholes-unique) grants one extra Phase 2 action,
taken immediately. **A player may never take more than two consecutive actions in a Phase**,
regardless of how many are granted; surplus is lost.

**Because:** the alternating single action is the game's fundamental unit — every cost, every
telegraph and every interaction window is denominated in it, and The Score literally charges
+2 credits per opponent action surrendered. So a card that hands *you* an action attacks the
central currency. The hard cap makes an unbounded action chain **impossible by the rules**
rather than merely expensive, which is a far stronger guarantee than prohibition P3 on a page.

**Pricing, defended against two existing entries:** Card Draw 1 = 3 buys a *card*, not the
action to use it. Multiple Attacks = 5 buys an extra *attack*, which is a strict subset of an
action. An arbitrary action must therefore exceed 5; Energy Gen 2 = 6 and an action is worth
more than 2 Energy. **7.**

**Rejected:** parking this on the Icons, which was the original proposal. Icons are exempt
from the system and are being designed last — parking the most valuable unbuilt mechanic there
means it never ships. It went to the Assholes, whose printed toolkit is already Energy Gen,
Hustler and Taxing: the tempo faction gets the ultimate tempo card.

**Affects:** [§8 Round Structure](../rulebook/08-round-structure.md#additional-actions),
`data/effects.yaml`, `data/factions.yaml`, the **Boss** Job.

---

## D-007 · Four mechanics built at once, rules layer first — 2026-08-05

**Decides:** OQ-07 · partially OQ-05

**Decision:** Range, Tokens, Arenas and Additional Actions all land together, and the
**rulebook changes land before any pricing**.

**Because:** Yorman's constraint was explicit — *"I don't want to tweak and adjust and
introduce something in the end that will require us to playtest everything all over again."*
That has a precise implication: build in order of how deep in the stack a change sits. A
rulebook change invalidates card tuning; a card never invalidates the rulebook. So rules →
data/pricing → validation → tool → cards, and the existing 31 cards get re-scored **once**, at
the end, rather than continuously while the foundation is still moving.

### Range N — *Overthinkers*, 2 points (Range 2) / 4 points (Range 3)

A Character that does not attack gains an **Aim** counter at the End Step; its next attack
deals **printed PA × (1 + Aim counters)**.

**Because** range as other games mean it — distance, kiting, positioning — does not exist here,
so it had to be re-expressed in a currency this game has. It is expressed as **time**, which is
the currency the whole balance system is already denominated in: Range 3 *is*
`telegraph_rounds: 2`, a plan credit that already existed and was barely used. It also generates
its own counterplay, so it earns its own multiplier through machinery already built. And it
creates the first card in the game that is valuable, fragile and slow at once — which is what
finally gives the Front family a reason to exist and makes Formations structural rather than
thematic.

**Rejected — "range means no return damage":** that is first strike, not range. It makes a card
*safer* than everyone else, which is backwards: what makes range interesting is that the ranged
card is fragile and needs protecting. Worth printing on its own merits, under another name.

**Rejected — flying:** a binary access axis that already exists as Prowler/Tracker. It would
mean two evasion keywords and two counter-keywords for one design idea, with no new decision
for the player, and nobody in this world flies.

**Three guardrails, all load-bearing.** The multiplier applies to **printed** PA only, or
buff-then-multiply becomes the only deck anyone builds (P4). Aim counters are **visible on the
board**, because a telegraph nobody can see is not a telegraph and earns no credits. Stun,
Fear, Silence and Bounce clear aim; **damage does not**, or chip damage trivially answers a
two-Round investment and nobody prints the card.

**Pricing:** Range 2 is worse than Combo-Striker (4) in every way except lump size → **2**.
Range 3 delivers the only number in the game that can exceed a large PH in a single clash
without Hard Removal (5), and it is fully telegraphed and interruptible, unlike Multiple
Attacks (5) → **4**.

### Tokens — shared, 2 points per body

A Character created by an effect, not a card. **Removed from the Game** when it leaves the
Board rather than sent to the Graveyard.

**Because** Mass Removal has been priced at 8 — the most expensive effect in the game — with
nothing to use it on, since every Character costs a card and Energy. Without a swarm corner the
numbers triangle (swarm → single-target → mass removal → swarm) has no third side and Mass
Removal is an overpriced "kill their two guys."

**The removed-from-Game rule is the P3 guardrail**, and it is why Recursion can never turn free
bodies into a loop. **Pricing:** a Token chump-blocks once (Prevent 1 Attack = 1) and threatens
(Direct Damage 1 = 1) → **2**. **Not available to Assholes** — solo operators; a crew of
hustlers is not a swarm of bodies.

### Arenas — shared, 2 / 5 points *(closes OQ-07)*

One per player, played as a Phase 2 action into the Tactic Zone, destroyable as an object.
**Arena text is symmetric** — it may never say "your Characters."

**Because** there is no map here, so an Arena cannot edit space. It edits the **rules**. And a
one-sided rule edit is a passive lock with no off-switch (**P2**), while a symmetric one is a
puzzle: the Arena is good because *your* deck was built to like the rule and theirs was not.
The asymmetry has to come from deckbuilding, not from the card — which also means an Arena is
never a dead draw and never uninteractive.

**Pricing:** Taxing 1 = 2 one-sided; a symmetric tax is worth less to you but you build around
it → Minor **2**. A global permanent category ban sits above Status Application (Major) = 4 →
**5**.

### Breaker — *Warmongers*, 4 points

Attacks deal PA plus half the defender's **printed** PH.

**Because** PH is the defensive stat and nothing inverted it, so stacking PH was strictly
correct forever. **Pricing:** Executioner (2) instantly murders but only a *damaged* defender —
conditional. Juggernaut (3) converts overkill but only against a small body. Breaker is
unconditional and scales with the thing it punishes → **4**.

### Collector — *Assholes*, 3 points

Enemies who attack anything *other* than this Character take 1 permanent PH damage.

**Because** Instigator is compulsion — *you must target me* — and taxation is the better tool: it
leaves the opponent a real choice with two costed answers instead of a forced move. Guilt-Tripper
was already a taxation rider; this generalises it. **Pricing:** Instigator (2) compels but is
rigid; Guilt-Tripper (2) is narrower, triggers only on being hit, and deals MA. Collector is
wider, deals **permanent PH**, and therefore feeds Executioner → **3**.

**Affects:** rulebook §2, §5, §8, §9, §13; `data/keywords.yaml`, `data/effects.yaml`,
`data/factions.yaml`. Verified: `card_io` still round-trips all 31 cards byte-identically, and
blocking-error count is unchanged at 34 (all pre-existing).

**Revisit if:** Range's break-even damage maths turns out to make Artillery unplayable rather
than merely fragile. The knob to turn is the multiplier, not the guardrails.

---

## D-006 · The Studio, and the features writing the README exposed — 2026-08-03

**Decides:** implements docs/design/studio-plan.md, all five phases

**Decision:** factions and crews become data (`data/factions.yaml`, `data/crews.yaml`,
`data/game-states.yaml`); three documents are generated from them; a 19-rule consistency engine
(`tools/rules.py`, `tools/check.py`) validates all three levels in one command; the workbench
grows to six screens; Reach is computed from the faction window map rather than guessed.

**Because:** faction identity, toolkits and crew plans lived in prose, which cannot be validated,
cross-referenced, or used in a calculation — that is the whole reason things drifted. Lifting
them into data and generating the prose back out is what makes a change propagate instead of
being retyped.

**What the engine found on its own:** F2 caught 7 toolkit violations including Moammar's tutor
and both Asshole Counterspells. W2 found Dre→Moammar *and* an unspotted second chain,
Decoy→RoaR in the Latin Kings. F9 caught that cards say crew "Pwners" while crews.yaml said
"PWNED".

**Features added while writing the README**, each because documenting a scenario revealed there
was no way to do it:

- **Create a card.** There was no way to make a new one — only edit existing ones.
- **Clone a card.** Copies mechanics; deliberately does NOT copy the Lore Packet, which is about
  a specific real person and must never be inherited.
- **Retire a card.** `status: retired` keeps the file and its Design Notes but drops it from
  validation and the counts. Better than deleting.
- **`tools/rename.py`.** Renaming a keyword or effect by hand breaks every reference silently —
  the card keeps the old name, the engine scores it as zero, and nothing says so.
- **Search by content.** The card list searched names only; it now searches effects, keywords and
  rules text, so "counterspell" finds every card using it.
- **`check.py --gaps`.** The engine reported what was *wrong* but never what was *missing*, which
  is the actual question when deciding what to design next.
- **Playtests on the card page.** Games mentioning a card surface on it, so a card that keeps
  appearing in "felt bad" is visible where you'd act on it.
- **Status lifecycle control** in the card header.

**Revisit if:** the rule set grows past what one person can hold. At that point the codes need
grouping by level rather than by severity.

---

## D-005 · Three levels of balance; Reach caps instead of multiplying — 2026-08-03

**Decides:** revises D-003. Adds Levels 2 and 3.

**Decision:** balance is checked at three levels — card, crew, faction. At the card level,
Credits earn an **Allowance** and **Reach** (how many factions can answer the card) **caps** it,
rather than multiplying it. Every declared cost is discounted by three tests: does paying it make
you worse at your job (bite), when do you pay relative to the payoff (timing), and does another
card hand it to you free (enabler).

**Because:** three faults surfaced from one question — why did Moammar have 50 points of headroom
when he plays as a strong card?

1. **Costs were priced nominally, not by whether they bite.** Moammar's board-state condition is
   what a Warmonger deck already does; his self-destruction is paid *after* a punch that wins the
   game; once-per-Game doesn't restrict a card that only needs once. All three were charged in
   full and all three are worth nothing.
2. **The Enabler Test was missing entirely, and it is the important one.** Dre's ascended text
   destroys every Character, Tactic and Attachment on the opponent's board. Moammar's level-up
   fires when the opponent has zero cards on their board. Dre's payoff *is* Moammar's condition,
   word for word, and they are both Mobb 134. A cost your own crewmate removes was never a cost.
3. **Multiplying by window count double-counted interactivity** — the setup was already in the
   Credits — and it pushed every card toward having all five windows, which homogenises. Capping
   by Reach instead rewards being answerable by *different factions* rather than by more moments,
   which is what crew and faction identity actually need.

Under the revision Moammar reads as over rather than under, Corazon lands within a point of his
Ceiling, and Dre keeps modest headroom — matching the designer's own read of all three.

**Levels 2 and 3 added:** every crew needs one written plan sentence plus a diversity rule (each
card advances the plan by a different mechanism), and every faction gets a toolkit and a window
profile derived from its printed lore. Measurement that motivated this: 13 of 28 effect types are
currently used by more than one faction; Overthinkers use 16 effect types including Mass Removal
and Hard Removal; the Assholes have Counterspell on two cards while their lore says they don't
block; Moammar is a Warmonger with a tutor. Nobody owns anything, so nobody feels like anything.

**Also documented:** the window map shows W3 (the moment it lands) and W5 (race it) are each
covered by only one faction. That is why cards answerable only in the Reaction Window keep coming
out Blue-mandatory.

**Affects:** `docs/design/balance-philosophy.md` rewritten around the three levels;
`data/plan-credits.yaml` gains `reach_caps` and `cost_tests`; `tools/scoring.py` and the
workbench panel rebuilt. Backwards compatible: a card with no declared plan is held to its base
budget exactly as before, and all 31 existing cards score identically.

**Revisit if:** the reach caps (3.0 / 2.0 / 1.5 / 1.0) prove too generous at the top end. That
multiple is now the most sensitive number in the system.

---

## D-004 · Balance philosophy rewritten as a teaching document — 2026-08-03

**Decides:** presentation of D-003 (the system itself is unchanged)

**Decision:** `balance-philosophy.md` is now written as plain-language instruction, not as an
argument. It states how the game works, explains every part of the machinery without assuming
any technical background, and teaches the whole system through three worked examples —
Moammar (one moment), Corazon (slow burn), Dre (deep build). The comparative research and the
case for replacing the old formula are no longer in it.

**Because:** the document's job is to make someone able to price a card, not to defend a
decision that is already made. Justification is dead weight in a reference people return to.

**Affects:** `docs/design/balance-philosophy.md` rewritten. `data/plan-credits.yaml` gained four
credit types that working the three examples exposed as missing: resources handed to the
opponent (Corazon's whole design is built on this and there was nowhere to record it),
Attachments required in play (Dre's seven Commandments), a board state you must engineer
(Moammar's empty-board condition), and once-per-Game (Moammar's single attack). Every figure in
the document is verified against `tools/scoring.py`.

**Also surfaced by the exercise:** two of Dre's five interaction windows are shut — his payoff
fires in Phase 3, which is not a Reaction Window, so it cannot be responded to at all. Announcing
in Phase 2 and resolving in Phase 3 opens W3, costs one more action, and raises his Ceiling from
82 to 98. The card gets stronger by becoming more fair, which is the clearest demonstration of
the system available.

**Revisit if:** a fourth card archetype appears that none of the three examples covers.

---

## D-003 · The Score replaces the flat point budget — 2026-08-03

**Decides:** new; supersedes the ascended-ceiling proposal in OQ-04; resolves OQ-09

**Decision:** power is earned, not capped. `Ceiling = (Base Budget + credits) × (1 + 0.25 ×
windows)`, where credits are paid in non-Energy currencies (setup, telegraph, sacrifice, cards,
life, narrowness) and windows are the five places an opponent can intervene. Four absolute
prohibitions sit above the arithmetic. Full reasoning and sources in
[balance-philosophy.md](balance-philosophy.md).

**Because:** the old formula was purely additive, so a combo — "cards that interact in a way
significantly stronger than the sum of their parts" — was not discouraged but *unrepresentable*.
It also had no time axis, so setup, telegraph and matchup narrowness were literally not
variables: a card requiring four Characters held for two Rounds scored identically to the same
effect with no conditions. And the ceiling was arithmetically low — on a 5-cost the single
biggest legal effect leaves 3 points for four stats, and across the whole pool 73% of every
point spent went to vanilla stats, because vanilla stats were the only thing the system could
price with confidence.

The inversion matters more than the arithmetic: counterplay used to be a pass/fail gate bolted
on the side, so it was pure cost. Now it is the multiplier, so a designer maximising a card's
power is pushed by the gradient itself toward interactive design.

Rejected: raising the flat budget (doesn't fix additivity); a separate "combo budget" (two
systems drift); pricing conditions as flat discounts à la Magic's delve (cost-reduction
mechanics are the documented dangerous family — Storm Scale 8 — precisely because the discount
is unbounded).

**Affects:** `data/plan-credits.yaml` (new), `tools/scoring.py` (Plan/Score, G1 rewritten),
`tools/studio.py` + `studio.html` (The Score panel), the gameplay rubric's G1 and G7, AGENTS.md.
No card content changed. Verified: every existing card scores identically, because a card with no
declared plan has Ceiling = Base Budget; browser and server agree exactly on a worked example
(budget 22 → credits 31 → earned 53 → ×2.0 → Ceiling 106).

**Revisit if:** playtesting shows the window multiplier is the wrong shape. Expect it to be the
most sensitive number in the system, and expect every credit value to have only two or three
usable steps — Gwent's Jackpot took −1 provision with no effect and −2 to disappear entirely.

---

## D-002 · Card Studio replaces the spreadsheet's conditional formatting — 2026-08-03

**Decides:** new (follows D-001)

**Decision:** `python tools/studio.py` serves a local design workbench that reads and writes
`cards/**/*.md` directly. The budget arithmetic and the machine-checkable gates move into
`tools/scoring.py`; card parsing and rendering move into `tools/card_io.py`. `balance.py`,
`validate.py` and the workbench are all thin layers over those two, so the number in the
browser is by construction the number on the command line.

**Because:** the spreadsheet's real value was never the storage, it was the *feedback loop* —
tweak a stat, see the cell turn red. Moving to markdown kept the data and lost the loop, and a
design system you can't feel is a design system you stop using. Two things the workbench does
that the spreadsheet could not: it shows the base budget and the level-up ceiling side by side
(the spreadsheet only ever showed the first, which is why 9 cards looked fine while 25 were
over — OQ-04), and it puts the faction's printed weakness and the card's Lore Packet on screen
beside the numbers, so mechanics and lore get decided together rather than lore being written
afterwards to fit.

Rejected: a read-only dashboard (keeps the manual edit step that makes iteration expensive) and
a browser-only tool using the File System Access API (no install, but a folder-permission prompt
every session and no path to running the same code on the command line).

**Affects:** `tools/` (six files), `requirements.txt`, `README.md`, `AGENTS.md`. No card content
changed. Verified: `card_io` round-trips all 31 cards byte-identically; `balance.py` still
reproduces the original spreadsheet verdicts on all 25 costed cards; a workbench edit and the
CLI report the same delta for the same card.

**Also changed:** G1's tolerance is now ±1 rather than exact, and the ascended side is checked
against a base × 1.5 ceiling. Under the stricter gate 27 failures surface across 25 cards, up
from 10. That is the gate getting honest, not the cards getting worse.

**Revisit if:** the workbench needs to edit anything the frontmatter doesn't hold (art crops,
playtest logs), or if a second person needs to design at the same time — this is single-user by
design and has no locking.

---

## D-001 · Repository restructured for AI-assisted development — 2026-08-03

**Decides:** new

**Decision:** Markdown + YAML is the source of truth for cards, rules and point tables. The
`TCG CARD TEST.xlsx` balance formula is ported to `tools/balance.py`. The spreadsheet is kept
in `legacy/` as a reference snapshot but is no longer edited.

**Because:** the spreadsheet's budget engine was the most valuable asset in the project and the
least legible — the formula lived inside a nested `LET()` in one cell. As plain text it can be
read, diffed, reviewed, tested and extended, and any AI assistant can work on a card directly
instead of round-tripping edits through a human and a spreadsheet. Rejected: keeping the xlsx
as source and generating markdown from it, which preserves the workflow but makes every card
edit a manual step.

**Affects:** all 31 cards, all point tables, the rulebook. Verified: `tools/balance.py`
reproduces the spreadsheet's `Overall Balance` verdict for all 25 costed cards exactly.

**Revisit if:** the spreadsheet's charting or filtering turns out to be load-bearing for
day-to-day design work.
