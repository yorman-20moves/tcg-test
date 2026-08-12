# Crew Lore Template

Copy this file to `docs/lore/<crew-key>.md` and fill it in. One file per crew.

**Where this sits.** Hand-written lore lives in `docs/lore/`. It is *not*
`docs/design/crews.md` — that file is generated from `data/crews.yaml` and must never be
hand-edited. When a section here is marked **→ feeds `data/crews.yaml`**, copy the finished
line into the YAML and run `python tools/generate.py`.

**What this template is for.** Every section maps to a gate or dimension in
`docs/rubrics/lore-rubric.md` §4, so a finished file passes crew review by construction. The
sections marked ⚡ are the drama layer — they are not in the rubric, and they are where the
immersion actually comes from.

---

## Five rules for the drama layer

Read these once before you fill anything in. They are the difference between a crew with a
backstory and a crew that feels alive.

1. **Drama is unresolved pressure, not history.** A war they won ten years ago is backstory. A
   debt that comes due next month is drama. Every section should leave something that could
   still go wrong.
2. **The conflict inside the crew must be sharper than the conflict outside it.** Rivals are
   cheap. What makes a crew feel real is that the five of them have a problem with each
   other and stay anyway.
3. **Every relationship has a direction.** Somebody owes, somebody is owed. "They don't get
   along" is not a relationship; "he still hasn't paid her back and both of them know it" is.
4. **Name a price that has already been paid.** Somebody lost something to make this crew
   exist. Until you can name it, the crew has no weight.
5. **The code exists to be broken.** A rule nobody is tempted to break is a policy. Write the
   rule *and* write who is closest to breaking it.

**Fill order that works:** §1 The True Thing → §3 Origin → §4 The Code → §6 The Fracture →
everything else. Do not start at the top; the top is a summary and summaries are written last.

---

## 1. The True Thing 🔒

*The crew-level version of the card rubric's True Detail — the load-bearing field. One real,
specific, verifiable thing about the actual group of friends. Not a vibe. A fact.*

> Good: "They all still have keys to an apartment none of them lives in anymore."
> Bad: "They're really tight."

**The True Thing:**

**What it explains about the crew:** *(one line — the mythologized version has to grow out of
this or the whole file drifts into stock gangster.)*

---

## 2. Identity

**Crew name:**
**What outsiders call them:**
**What they call themselves when nobody's listening:**
**One-line pitch:** *(the crew as a mythologized entity — 1 sentence)*
**Aesthetic tell:** *(→ crew dimension "Aesthetic coherence": what makes the art identifiable
at a glance — a color, an object, a posture, a piece of clothing)*

### Territory — **CG1**

*A named place a reader can picture. The city has no name yet (canon gate WG1), so stay local:
blocks, corners, a bar, a stairwell, a park, a parking lot. Specific beats grand.*

**The place:**
**What it looks like at 2am:**
**What they do there that they don't do anywhere else:**
**Who is not allowed in:**

→ feeds `docs/design/canon.md` **Places** table, and Arenas (OQ-07)

---

## 3. Origin — **CG2**

*Why these people, why together. Not a history — one incident.*

**The founding incident:** *(3–5 sentences. Something happened. They were not a crew before it
and they were after.)*

**Who was there:**
**Who was there and is not in the crew now:** ⚡ *(this person is free drama forever)*
**The price already paid:** *(rule 4 — what it cost, and who is still paying it)*

→ feeds `docs/design/canon.md` **Timeline** table as a fixed event

---

## 4. The Code — **CG3**

**The rule they do not break:** *(one sentence, stated the way a member would say it, not the
way a narrator would)*

**What happens to someone who breaks it:** *(be specific and be willing to have it happen on a
card)*

**The rule they all quietly break:** *(the hypocrisy. This is the single most useful line in the
file — it is where half your flavor text will come from.)*

**Who is closest to getting caught:** ⚡

---

## 5. The Roster

*→ crew dimension "Internal texture." One row per member. Jobs must differ; if two members do
the same job, one of them is decoration.*

| Member | Faction | Their Job in the crew | What they want that the crew can't give them |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**Who leads, and is it settled?** ⚡ *(if it's settled, say who would take over and how they'd
feel about it)*
**Who is the newest, and are they in?** ⚡
**Who does the crew protect that it probably shouldn't?** ⚡

### Faction spread — **CG4**

**Factions represented:**
**If it's only one faction, justify it here:** *(the rubric allows a mono-faction crew, but it
has to be a decision — "everyone here fights the same way because ___")*

---

## 6. The Fracture ⚡

*Not in the rubric. Do not skip it. This is the engine.*

**The disagreement that hasn't been settled:** *(2–3 sentences. Two members, a real question,
no obvious right answer. Both positions must be defensible — see world dimension "Moral
texture": nobody is simply wrong.)*

**Member A's position and why they're right:**
**Member B's position and why they're also right:**
**Why it hasn't come to a head yet:**
**What would force it:** *(name the trigger — this is a future card)*

---

## 7. Standing Relationships — **CG5**

*At least two other crews. Every entry needs a direction (rule 3).*

| Other crew | Type | The specific thing | Who owes whom | Current temperature |
|---|---|---|---|---|
| | alliance / debt / grudge | | | warm / cold / one incident from open war |
| | | | | |

**The one they will not talk about:** ⚡
**Which relationship changes if the crew wins the next thing they're going for:** ⚡

→ crew dimension "External position." Aim for at least one card *in another crew* that
references this one; note the card here when you write it.

---

## 8. The Open Wound ⚡

*→ crew dimension "Room to grow." The unfinished business. If the crew's story is complete, the
crew is done, and a done crew generates no cards.*

**What they're trying to get, right now:**
**What's standing in the way:**
**What they lost that they haven't replaced:**
**The thing they're wrong about:** *(they don't know it yet; you do)*

---

## 9. Voice

*→ crew dimension via lore gate L9. Register: hard, funny, mythologizing, present-tense,
specific. Never winks at the reader.*

Three lines only a member of this crew would say. Not slogans — things said in a room.

1.
2.
3.

**Word they use that no other crew uses:**

---

## 10. Mechanical Signature

*→ crew dimension "Mechanical signature," and this is where lore becomes rules. Mobb 134 has
Commandments; every crew needs something the others don't have.*

**The signature:** *(a mechanic, sub-type, or restriction unique to this crew)*
**Why the lore makes it inevitable:** *(if you can't answer this, the signature is a gimmick)*

**Plan (one sentence — how does this crew win a game?):**

→ feeds `data/crews.yaml`: `plan`, `lore_basis`, `signature`

**Coordination:** coordinated / chaotic
*(chaotic is not "they're wild" — it means no card in the crew may require a board state
another card in the same crew produces. `data/formations.yaml`, `no_internal_enablers`.)*

**Roads — one per card, all different destinations off the same plan:**

| Card | Road (how *this* member advances the plan differently) |
|---|---|
| | |

→ feeds `data/crews.yaml`: `expressions`

---

## 11. Three You Haven't Written

*→ crew dimension "Room to grow" scores a 5 only if you can name three more members. Names or
roles, one line each.*

1.
2.
3.

---

## 12. Self-Check

Fill this last. Any unchecked gate blocks the crew.

| Gate | Requirement | ✔ |
|---|---|:-:|
| **CG1** | Named territory a reader can picture | |
| **CG2** | Origin — why these people, why together | |
| **CG3** | A rule they don't break **and** one they all quietly break | |
| **CG4** | Spans ≥2 factions, or documented why not | |
| **CG5** | Standing relationships with ≥2 other crews | |

| Dimension | Wt | 1–5 | Note |
|---|--:|:-:|---|
| Internal texture | 4 | | roles + friction, not a shared logo |
| External position | 4 | | other crews' cards reference this one |
| Mechanical signature | 4 | | the crew *plays* differently |
| Aesthetic coherence | 3 | | identifiable from art alone |
| Room to grow | 3 | | three more members nameable |

**Weighted total (max 90):**

### Diagnostics

- **The Swap Test.** Swap this crew's territory and code with another crew's. Do both still
  work? Then both are generic.
- **The Loyalty Test.** Name what a member would give up for this crew that they wouldn't give
  up for a friend. No answer means the crew is a label — lore gate L6.
- **The Stranger Test.** Someone who knows none of you reads this file. Can they name the
  crew's problem? Not its vibe — its problem.
- **The Sober Test.** Every named person reads their row in §5 tomorrow, alone, having had a bad
  week. Still fine? That's lore gate L2, and it is a gate, not a courtesy.

### Sign-off

**Every named member has read and approved their entry:** ☐ *(lore gate L2 — consent is
required, not assumed)*

**`reviewed:` flag in `data/crews.yaml` set to `true`:** ☐ *(only Yorman flips this)*
