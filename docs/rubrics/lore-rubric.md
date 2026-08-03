# The Lore Rubric

**Purpose.** Make the lore *cohere* — as a world, as a set of portraits of real people, and as
an explanation of why the mechanics are what they are.

**The audience contract: friends first, strangers second.** The inside joke must land hardest
for the people in it. But every card must *also* read as a real character to someone who has
never met any of you. This is not a compromise — it is how the best of this genre works. A
stranger reading a card should feel they're missing a story, not that there isn't one.

**Two stages**, same as the gameplay rubric: gates (pass/fail), then weighted dimensions (1–5).

**Three scopes:** [card](#1-card-lore-gates), [crew](#4-crew-scope), [world](#5-world-scope).

---

## 0. The Lore Packet

Every card carries this block in its markdown, under `## Lore`. **The packet comes before the
flavor text, always.** Writing flavor text without the packet is how you get seven cards that
are all "he's crazy, and dangerous."

| Field | What goes there | Length |
|---|---|---|
| **Premise** | The one-line pitch of this person as a mythologized figure | 1 sentence |
| **The True Detail** | One specific, verifiable, real thing about the actual person. The anchor. | 1 sentence |
| **The Myth** | What the streets say happened. Exaggerated, unverifiable, better than the truth. | 2–3 sentences |
| **Why This Faction** | The methodology argument: why they win *this way* | 1–2 sentences |
| **Why This Crew** | The social argument: who they run with and what they owe them | 1–2 sentences |
| **The Fall** | Their exposure to the faction's printed weakness. **Required.** | 1–2 sentences |
| **The Ascension** | What levelling up *means* — the story beat, not the stat change | 1–2 sentences |

**The True Detail is the load-bearing field.** It's what makes the card land for the friends and
what makes it feel real to strangers. "He closes down every bar" is a True Detail. "He's the
life of the party" is a description of a category of person.

---

## 1. Card Lore Gates

### L1 — Person-truth

Someone in the crew, shown the card with the name covered, identifies the person. If it could
be three different friends, it's a stock character with a friend's name on it.

### L2 — The dignity line

*The most important gate in this document.*

The roast punches at something the person would **own in public**. Not at something they'd wince
at reading in front of the group.

The reliable test: **would they show this card to someone they're trying to impress?** A card
that makes them look ridiculous in a way they'd tell the story about themselves passes. A card
that names a real wound does not — no matter how funny it is, and *especially* if it's funny.

Three specific lines that don't get crossed even when the person would laugh:

- Anything that stops being funny if the group changes.
- Anything about a person not in the game and not consenting (family, exes, kids).
- Anything that reads as a slur to a stranger, whatever it means inside the group.

**Consent is required, not assumed.** Every named person signs off on their own card. That is a
gate, not a courtesy — and it's cheap, because asking is also the single best source of lore
you'll ever get.

Fails together with gameplay gate **G9**.

### L3 — Canon consistency

Contradicts nothing established: no resurrections of the dead, no geography that moved, no
timeline that doesn't fit, no crew allegiance that changed without a card documenting the
switch. Check `docs/design/canon.md` before writing.

### L4 — Mechanical marriage

**The flavor explains the rules text.** Read the ability, then the lore: the lore should make
the ability feel inevitable.

The gate is failed by the two commonest lore mistakes:
- **Decoration** — flavor that could sit on any card with those numbers.
- **Contradiction** — flavor that describes something the card doesn't do. Lore saying "nobody
  can touch him" on a card without Prowler or Untargetable is a broken promise, and players
  notice.

The strong version: **the ability is the punchline and the lore is the setup.**

### L5 — Faction justification

The card argues, in-fiction, why this person wins *this way*. Faction is methodology, not vibe.
A brawler who is smart is still a Warmonger if he wins by hitting. Being clever is not
Overthinker; **winning by being clever** is.

### L6 — Two-axis coherence

Faction and crew must both be legible and must **not** be redundant.

The system's best structural idea is that these axes are independent — the Latin Kings span
Overthinkers, Assholes and Warmongers, and that's what makes them feel like a real crew instead
of a color. A card fails L6 if its crew is doing no work: if you could move it to another crew
and change nothing, the crew is a label.

### L7 — Level-up causality

The Level-Up condition is a **story beat**, and the base side actively *pursues* it.

The model here is Alvino: his base ability hands out drinks that damage Mental Health, and he
levels up when four Characters have taken a shot from him and suffered that damage. He levels
up by *doing his thing until the bar is trashed*. The condition is a consequence of the
character, and the ascended ability — Closing Time — is what happens next.

Fails if the condition is something that merely *happens to* the card, or if the ascended side
is the same character with bigger numbers.

### L8 — Name discipline

Format: `Name, The Epithet` — or, for ranked crews, `Name, Nth Crown - Epithet`.

The epithet must be **earned by the card**, alliterate or scan, and not duplicate another card's
structure three times in a row. You currently have "The Last Call," "The Last Laugh" and "The
First Lady" — that's a family, which is good, and the ceiling is about four before it's a tic.

### L9 — Register

The world's voice, set by the rulebook, is: **hard, funny, mythologizing, present-tense,
specific.** It treats a neighborhood like an epic and never winks at the reader. Flavor that
goes ironic, generic-fantasy, or explains its own joke is off-register.

---

## 2. Card Lore Dimensions

Score 1–5 × weight. Max weighted **145**.

| # | Dimension | Weight | 1 | 3 | 5 |
|---|---|---:|---|---|---|
| **D1** | **Specificity** | 5 | Adjectives | One concrete detail | Detail so specific it could only be this person; a stranger believes it |
| **D2** | **Double legibility** | 5 | Only lands for insiders, *or* generic enough for anyone | Both layers exist, one is thin | Friends get the reference; strangers get a complete character. Neither needs the other |
| **D3** | **Mechanical fusion** | 5 | Flavor and rules coexist | Flavor explains rules | You couldn't design the ability differently after reading the lore |
| **D4** | **Faction weight** | 4 | Wears the color | Embodies the strength | Embodies the strength **and visibly carries the printed weakness** |
| **D5** | **Crew contribution** | 3 | Crew is a tag | Consistent with the crew | Makes the crew more itself; the crew is better for this card existing |
| **D6** | **Ascension arc** | 4 | Bigger numbers | A change of state | A transformation you'd want to *see*; the base card reads differently afterward |
| **D7** | **World texture** | 3 | Adds nothing outside itself | References an established place or event | **Adds** a place, a law of the world, or a piece of history other cards can use |
| **D8** | **Voice** | 3 | Off-register | On-register | On-register and quotable — someone says this line at the table |
| **D9** | **Reread value** | 2 | Read once | Fine twice | Funnier or darker the second time, once you know how the card plays |
| **D10** | **Restraint** | 3 | Explains the joke; over-written | Right length | Every word load-bearing; the best detail is the one it *doesn't* say |

### Reading the score

| Score | Verdict |
|---|---|
| **115+** | Ship it |
| **90–114** | Ship, note the weakest dimension |
| **70–89** | The packet is probably thin. Go back to **The True Detail** — that's almost always the missing piece |
| **< 70** | You wrote a description, not a character |

**Dominant-weakness rule:** any dimension at **1** blocks, same as gameplay. Most common
offender is **D2** — insider-only cards that are hilarious in the group and inert outside it.

---

## 3. Diagnostics

Fast checks that catch the common failures.

**The Swap Test (D1).** Swap two cards' names within the same faction. If both still work, both
are generic.

**The Stranger Test (D2).** Show it to someone who knows none of you. Ask what kind of person
this is. If they can answer with a real sentence, you passed. If they say "a tough guy," you
didn't.

**The Cover Test (L4).** Cover the rules text. Ask a player to guess the mechanic from the lore
alone. Getting close means fusion. Getting nowhere means decoration.

**The Weakness Test (D4).** Name the moment this card loses. If the answer is "when it gets
outstatted," the card has no printed weakness and D4 caps at 3.

**The Better Story Test (D6).** Would you rather read the base side or the ascended side? If
the base side is more interesting, the ascension is a downgrade with better numbers.

**The Sober Test (L2).** Read it back to yourself imagining the person reads it tomorrow,
sober, alone, having had a bad week. Still funny? Ship. Not sure? Ask them.

---

## 4. Crew Scope

Run when a crew reaches five cards. **Crews are the game's real social unit** — factions are
methodology, crews are loyalty — and they're currently under-defined relative to how much
structural weight they carry.

| Gate | Requirement |
|---|---|
| **CG1** | The crew has a **territory** — a named place a reader can picture |
| **CG2** | The crew has an **origin** — why these people, why together |
| **CG3** | The crew has a **code** — one rule its members do not break, and one they all quietly break |
| **CG4** | The crew spans **at least two factions**, or it is documented why it doesn't |
| **CG5** | The crew has a **standing relationship** with at least two other crews — an alliance, a debt, a grudge |

| Dimension | Weight | A 5 |
|---|---:|---|
| Internal texture | 4 | Members have roles and friction with each other, not just a shared logo |
| External position | 4 | Other crews' cards reference this one |
| Mechanical signature | 4 | The crew *plays* differently — Mobb 134 has Commandments; every crew should have something |
| Aesthetic coherence | 3 | You could identify the crew from art alone |
| Room to grow | 3 | You can name three more members you haven't written |

**Current state:** six crews (Latin Kings, Mobb 134, Shea's, Pimp Juice, PWNED, Fury Park),
five cards each except Fury Park with one, and none of them has a documented territory, origin,
or code. Only Mobb 134 has a mechanical signature. This is the highest-leverage lore work
available — five documents that would immediately make thirty-one existing cards better.

---

## 5. World Scope

The layer above crews. Run when adding a faction, a place, or a piece of history.

### World gates

| Gate | Requirement |
|---|---|
| **WG1** | **The city has a name.** It doesn't have one yet. Nothing else here is possible without it |
| **WG2** | **The stakes are stated** — what are the crews actually fighting *over*? Territory, respect, money, survival? The answer determines every future card |
| **WG3** | **The three victories are explained in-fiction.** Beatdown, Influence and Concession must be three *culturally real* ways to win in this world, not three rules |
| **WG4** | **The timeline exists.** Even three fixed events. Otherwise every card is set in an eternal present and nothing can reference anything |
| **WG5** | **Each faction's printed weakness has happened at least once**, on the record, to somebody |

### World dimensions

| Dimension | Weight | A 5 |
|---|---:|---|
| Coherence | 5 | No contradictions; the rules of the world hold across all cards |
| Specificity of place | 4 | The city has streets, bars, parks, corners with names |
| Consequence | 4 | Events have aftermath; the world has changed and cards show it |
| Moral texture | 4 | No faction is simply the villain; each is right about something |
| Generativity | 4 | The premise suggests cards you haven't written |
| Tone discipline | 3 | Consistent register across every card |

### The three big open world questions

1. **What is the city called, and what makes it worth fighting over?** Everything downstream
   waits on this.
2. **What are the Icons?** They're the only faction whose lore describes an institution rather
   than a personality — pillars, martyrs, sponsors, untouchable kings. They also have no cards,
   no crew and no Influence support. Deciding what the Icons *are* is simultaneously the biggest
   lore gap and the biggest gameplay gap. They're the same problem.
3. **Why do these crews fight instead of just being friends?** The real people are friends. The
   game says they're rival factions. The lore that reconciles those two facts is the heart of
   this whole thing, and it does not exist on paper yet. Get this right and every card gets
   easier to write.

---

## 6. Using this with AI

The prompt shape that works:

> Write the Lore Packet for [name], a [cost] [faction] [subtype] in the [crew] crew.
> Here is the True Detail: [one real thing about them].
> Here is the ability: [rules text].
> Fill all seven packet fields, then the flavor text, then score L1–L9 and D1–D10 and name the
> weakest dimension.

**Always supply the True Detail yourself.** It's the one field an AI cannot invent — it's the
thing only you know — and it's the field everything else hangs on. Hand over the real detail
and the mythologizing is easy; withhold it and you get seven interchangeable tough guys.

For review, ask adversarially: *"Apply the Swap Test and the Stranger Test to this card and make
the strongest case that it's generic."*
