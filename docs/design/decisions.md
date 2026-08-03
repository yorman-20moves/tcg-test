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
