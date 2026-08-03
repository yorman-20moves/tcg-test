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
