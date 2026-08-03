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
