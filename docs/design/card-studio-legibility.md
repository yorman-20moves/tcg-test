# Card Studio — legibility overhaul

**Date:** 2026-08-05 · **Scope:** `tools/studio.html`, `data/plan-credits.yaml`, `tools/check.py`

Design and implementation in one document. Sections 1–3 are the reasoning; sections 4–11 are
the work, each stating what changes and why.

---

## 1. The problem

The Studio has all the right pieces and organises them for someone who already knows
`docs/design/balance-philosophy.md` by heart. The person making the balancing decisions does
not. That is the whole of it — every other complaint below is a symptom.

**F1 — Two competing verdicts on one page.** `proofPanel()` answers "is it on budget?" against
the **base budget**. `scorePanel()` answers "does it fit?" against the **Ceiling**. They sit
~500px apart in different visual languages. For a card with no plan they agree; for a card with
a plan they do not, and nothing on screen says which one is the real answer.

**F2 — The arithmetic is stated, never explained.** `cost 5 × 3 … 15` is a receipt. It never
says why Energy buys 3 points, what a credit is worth and why, or what to do about a number
that is wrong.

**F3 — The controls with the largest mechanical effect have the least explanation.** The
bite/timing/enabler selects render as three unlabelled dropdowns reading `bite…` `timing…`
`enabler…`. An `on_plan` answer multiplies a credit by **0.0**, silently deleting it. The credit
`anchor` strings — the entire justification for each price — are hidden in `title=` attributes.

**F4 — Selecting anything scrolls the page to the top.** Ticking a window, setting Reach or
choosing a cost test loses your place, every time.

**F5 — `check.py` does not run on this machine at all.** It exits with `UnicodeEncodeError`
before printing a finding, because Python on Windows defaults stdout to cp1252 and `check.py`
prints `─` box rules. CLAUDE.md calls it "the one that matters."

## 2. Root causes, verified in code

| # | Cause | Where |
|---|---|---|
| C1 | `preservingFocus()` returned early with a bare `render()` when the focused element had no `data-focus` key, so scroll was never saved. Checkboxes, `<select>`s and chip buttons have no such key. `replaceChildren()` then collapses `#main` to zero height and the browser clamps `scrollTop` to 0. | `studio.html` `preservingFocus` |
| C2 | The effect picker's filter `<input>` is constructed fresh inside `effectPicker()`, which `touch()` re-runs on every toggle. The typed query is destroyed on each tick. | `studio.html` `effectPicker` |
| C3 | The G2/G5/G7/G9 checkboxes are created with no backing state, so any re-render silently unticks them. | `studio.html` `gateStrip` |
| C4 | **The browser computed Reach differently from the checker.** JS used `min(4, windowCount)`. Python uses *the number of factions strong in at least one declared window*, from `data/factions.yaml`. The Studio could show a Ceiling `check.py` disagreed with, and `save()` only drift-checked `baseDelta`. | JS `scorePlan` vs `scoring.py:157-192` |
| C5 | `check.py` prints U+2500 to a stdout Python binds to the console codepage. | `check.py:63` |

## 3. Non-goals

- **`scoring.py` and `rules.py` are never edited.** They are source of truth. Where the JS mirror
  and the Python disagree, the JS is what changes.
- No card-schema change. Human-gate ticks are session state, not persisted.
- The card face, artwork, flip and lightbox are untouched.
- The left roster and right rail are untouched beyond what C1 fixes for free.

**Baseline that must not move:** `34 blocking, 77 warnings`, breakdown
`F2×7, F4×19, F6×8, GAP×10, W1×2, W10×2, W15×1, W2×2, W3×6, W4×12, W6×13, W8×4, W9×25`.

---

## 4. `check.py` on a legacy console — C5 ✅ done

`check.py` reconfigures its own stdout to UTF-8 at start-up. One line, no behavioural change.
Guarded by `tools/tests/test_check_encoding.py`, which runs the real CLI in a subprocess with
`PYTHONIOENCODING=cp1252` and fails if the fix is reverted.

*Commit `b2bf509`.*

## 5. Scroll and focus — C1 ✅ done

`preservingFocus()` saves and restores `scrollTop` for `#main` and `#rail` **unconditionally**,
before it asks about focus at all. Every interactive control gained a `data-focus` key:
`win:<key>`, `reach:<n>`, `credit-dn:<key>`, `credit-up:<key>`, `test:<credit>:<test>`,
`kw:<side>:<name>`, `ef:<side>:<name>`, `efsearch:<side>`, `status`, `step-dn:<label>`,
`step-up:<label>`.

**And the counterpart, which the first pass got wrong:** three call sites change *what you are
looking at* rather than redrawing it — `select()`, `setMode()`, and the Factions/Crews roster
row — so they explicitly reset scroll to 0 afterwards. Without that, unconditional restore
handed a scrolled card's offset to whatever you opened next, which was worse than the original
bug. `save()` deliberately does **not** reset: it redraws the same card, and losing your place
there would be the original bug returning.

*Commits `248fca3`, `9b71fa5`.*

## 6. Filter and gate state — C2, C3 ✅ done

Both are state held only in a DOM node that `touch()` throws away.

- `EF_QUERY = {base:"", ascended:""}` at module level. `effectPicker(side)` seeds the input from
  it and writes back on every keystroke, so filtering and ticking can happen in the same breath.
- `HUMAN_TICKS`, a `Set` keyed `"<relPath>|<gateId>"`. Per-card, session-scoped. The handler
  deliberately does **not** call `touch()` — reading a card against G9 is not an edit to the
  card, and marking it dirty over it would be wrong.

## 7. Reach, computed the way the checker computes it — C4 ✅ done

Mirrors `Plan.reach_value()` exactly:

1. explicit `plan.reach` wins, clamped 0–4;
2. otherwise no windows declared → `null`;
3. otherwise count factions with `windows[w] === "strong"` for any declared `w`;
4. if no faction carries window profiles at all, fall back to `min(4, windowCount)` — the
   `_answering() is None` branch in Python.

This can legitimately produce **Reach 0** — windows declared, no faction strong in any of them —
which means not printable, and §8 renders that loudly.

`scorePlan(s, plan)` and `costFactor(key, plan)` take the plan explicitly rather than reading the
module-level `draft` through `planOf()`, which is what makes the parity check below possible.
`planOf()` stays as-is for the editing UI.

**The guard.** The server ships its own authoritative `scoring.score(card).as_dict()` for every
card in the bootstrap payload, so the mirror is directly testable against it. `parityCheck()`
compares `budget`, `baseSpent`, `baseDelta`, `reach`, `ceiling` and `headroom` for every scorable
card on boot. Silent when they agree; a toast naming the first divergence when they do not. It
ships permanently — it is the guard that would have caught C4 the day it appeared. `save()`'s
drift check extends from `baseDelta` alone to `reach` and `ceiling` too.

## 8. The verdict panel — F1, F2 ✅ done

One ledger, read top to bottom as sentences: what the card is allowed to spend, then what it
actually spends, then what to do about the difference. Replaces the arithmetic half of
`proofPanel()` and the whole `scorebar` of `scorePanel()`.

**A card with no declared plan** genuinely has two limits — `_gate_g1` checks the base side
against the budget two-sidedly, and both faces against `budget × 1.5` one-sidedly — so it shows
both. Worked example is real (Moammar, cost 5, Ascendant, 6/6/0/3, *Searching (Tutors)* 4,
*Permanent Buff 5* 5):

```
POTENTIAL POWER — what this card is allowed to spend
  Because it costs 5 Energy ...............................  15
    Every point of Energy buys 3 points of power.
  Because every card gets a base allowance ................  +1
  Because it's an Ascendant — it has two faces ............  +3
  ───────────────────────────────────────────────────────────
  BASE BUDGET — what the base side may spend ..............  19
  Both faces together may spend 1.5× that .................  28

ACTUAL IMPACT — what it really spends
  Its stats — PA 6 · PH 6 · MA 0 · MH 3 ...................  15
  Its base keywords — none ................................  +0
  Its base effects — Searching (Tutors) ...................  +4
  ───────────────────────────────────────────────────────────
  BASE SIDE SPENDS ........................................  19
  Its level-up keywords — none ............................  +0
  Its level-up effects — Permanent Buff 5 .................  +5
  ───────────────────────────────────────────────────────────
  BOTH FACES SPEND ........................................  24
```

**A card that declares a plan** has one Ceiling covering both faces, so one ledger and one bar:

```
  BASE BUDGET .............................................  19
  Because 3 Characters must be on board first .............  +6
    2 each — half the cost of consuming one.
  Because it telegraphs for 2 full Rounds .................  +10
    5 each — a draw (3) plus a Round of tempo.
  ───────────────────────────────────────────────────────────
  ALLOWANCE — budget plus what it pays in other currencies   35
  But only 2 factions can answer it, so it's capped at 1.5×  28
    Warmongers and Assholes can. Overthinkers and Icons are blind.
  ───────────────────────────────────────────────────────────
  CEILING — the most this card may spend ..................  28
```

A discounted credit shows its arithmetic on its own row: `2 × 5 = 10 → ×0.5 → 5`.
**Reach 0** replaces the CEILING row with a full-width critical block naming what would fix it.

**The decision line**, which is what was missing entirely:

- **Over** — `9 over. Cut 9 points of impact, or buy more ceiling: +1 Energy buys 3 points, and
  giving a blind faction a window it can actually use raises the cap. Right now Overthinkers and
  Icons have no answer at all.`
- **Under** — `4 under. This is weaker than its cost pays for — underpowered is as wrong as
  overpowered here, it just fails quietly. Add 4 points of impact, or drop the cost by 1, which
  removes 3 points of budget.`
- **On** — `Exactly on budget. It spends precisely what its cost buys.`

## 9. Status colour ✅ done

The rule in the `studio.html` CSS header holds: **hue belongs to faction, fill belongs to
status.** Warmongers own red and Assholes own green, so status may not use them.

| State | Token | Value | Glyph | Word |
|---|---|---|---|---|
| On budget (`\|Δ\| ≤ tolerance`) | `--good` | `--color-ink-60`, unchanged | `✓` | In tolerance |
| **Under** (`Δ > tolerance`) | `--under` **new** | `#5c8f9e` dark / `#3d7383` light | `↓` | N under |
| Over, by magnitude | `--warning` / `--serious` / `--critical`, unchanged | existing ramp | `!` / `✕` | N over |

`--under` is a desaturated steel-teal, deliberately distinct from `--color-cyan` (`#1fb6e8`),
which already means *selected/focused*. **`--under` never touches an interactive control**, or a
dim meter and a pressed chip start speaking the same language.

**Under is a failure only against the base budget.** Spending less than a *ceiling* is fine, and
`ceiling_severity()` already encodes this:

- base side vs base budget → two-sided → may render `--under`;
- both faces vs `budget × 1.5` → one-sided → under renders `--good`;
- total vs Ceiling → one-sided → under renders `--good`; it is called headroom and it is good.

Colour never carries meaning alone: every state ships its glyph and its word.

## 10. The teaching layer — F3 ✅ done

Printed on screen: anything that changes a number being chosen. Left in tooltips: vocabulary.
The existing `GLOSSARY` / `tipped()` / `ruleDocs` machinery is extended, not replaced.

- **Credit anchors become visible text** — `Worth 5 because a draw (3) plus a Round of tempo.`
- **The three tests stop being bare dropdowns.** Each renders as its question, its reason, and
  options naming their consequence and multiplier, plus the live arithmetic underneath. Wording
  lives in `data/plan-credits.yaml` under `cost_test_copy:`, a **sibling** of `cost_tests:` —
  the multipliers are read from `cost_tests` and never duplicated into the copy block, so the two
  cannot disagree about a number. `cost_tests` keeps its exact current shape, because
  `Plan._discount()` reads it as a flat `{test: {answer: multiplier}}` map.
- **Reach becomes a derived readout** naming which factions can answer and which window earns
  each ✓. The 0–4 chips remain, relabelled as an explicit override.
- **Every machine gate failure gains a fix line.**

## 11. Page structure ✅ done

Five blocks. Blocks 2 and 3 are the two halves of the verdict in the same order, so the half of
the verdict that is wrong tells you which panel to scroll to.

| # | Panel | Contains |
|---|---|---|
| 1 | **The card** | face · rules text · level-up condition · ascended text · the §8 verdict |
| 2 | **What raises the ceiling** | Cost stepper · what it pays · the three tests · Reach · windows · prohibitions |
| 3 | **What spends it** | the four stat steppers · base keywords + effects · level-up keywords + effects |
| 4 | **Can it be printed** | gate strip, machine gates, human gates |
| 5 | **Context** | Job / Formation · cost neighbours · playtests |

Cost moves into block 2 and the stats into block 3, splitting the old combined `Cost & stats`
panel: cost is the only control that raises a ceiling, and the stats are the largest single line
of spend.

---

## 12. Verification

1. `python tools/check.py` runs with no `PYTHONIOENCODING` and prints exactly
   `34 blocking, 77 warnings   (F2×7, F4×19, F6×8, GAP×10, W1×2, W10×2, W15×1, W2×2, W3×6, W4×12, W6×13, W8×4, W9×25)`.
2. `python -m pytest tools/tests -q` → 13 passed.
3. `python tools/generate.py --check` → clean.
4. `parityCheck()` in the browser console → `[]`, and no drift toast on boot.
5. Ticking a window, setting Reach, changing a cost test, clicking a credit ±, a keyword chip, an
   effect → `#main` scrollTop unchanged, focus retained. Switching card or mode → scrollTop 0.
6. Effect filter query survives a tick. Human gate ticks survive a re-render and are per-card.
7. Both verdict forms render with figures matching `check.py`.
8. `--under` appears on under-budget meters and on no interactive control, in both themes.
9. No card file changes except through a deliberate studio edit.

## 13. Known follow-ups, deliberately not in scope

- **A window has no field naming the card or rule that exercises it.** The rulebook requires one
  ("someone could theoretically remove it" is not a window) but the schema has nowhere to put it,
  so the requirement is unenforceable. Needs a schema decision → `open-questions.md`.
- Human-gate ticks are session-only; persisting them is a schema change.
- `renderLibrary()`'s kind/row switch bleeds scroll the way `select()` did before §5 (measured
  1500 → 689 → 596). Not fixed there because the Library's list and editor share one pane, so
  reset-to-0 would scroll away from the row just clicked. The kind-switch arguably still wants a
  reset; the row-switch does not.
- `cardText()`'s `requestAnimationFrame`-deferred textarea auto-grow drifts scroll ~210px on any
  render touching those fields. Pre-existing.
- `preservingFocus` keys are not scoped by card, so a same-named control on a newly selected card
  could in principle capture focus. Unreachable via card-row click, since the row carries no key.
- Opening a card whose `plan` holds only `requires` makes `planOf()` write back empty `pays: {}`
  and `windows: []`. Harmless — `new_card()` writes those keys anyway — but it is a diff you did
  not make.
- **`data/factions.yaml` names its fifth window `race`; `data/plan-credits.yaml` names it
  `orthogonal`.** Nothing reconciles them, so a card declaring the `orthogonal` window finds no
  faction strong in it, computes Reach 0, and is reported as not printable. Verified against
  `scoring.py`, which agrees — so this is a live data inconsistency, not a Studio bug. One of the
  two names has to give.
