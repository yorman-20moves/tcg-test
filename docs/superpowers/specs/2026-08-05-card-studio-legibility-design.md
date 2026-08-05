# Card Studio — legibility overhaul

**Date:** 2026-08-05
**Scope:** `tools/studio.html`, one additive block in `data/plan-credits.yaml`, one line in
`tools/check.py`
**Status:** approved design, not yet implemented

---

## 1. The problem

The Studio has all the right pieces and organises them for someone who already knows
`docs/design/balance-philosophy.md` by heart. The person making the balancing decisions does
not. Four concrete failures:

**F1 — Two competing verdicts on one page.** `proofPanel()` answers "is it on budget?" against
the **base budget**. `scorePanel()` answers "does it fit?" against the **Ceiling**. They sit
~500px apart in different visual languages. For a card with no plan they agree; for a card with
a plan they do not, and nothing on screen says which one is the real answer.

**F2 — The arithmetic is stated, never explained.** `cost 5 × 3 ... 15` is a receipt. It never
says *why* Energy buys 3 points, what a credit is worth and why, or what the designer should do
about a number that is wrong.

**F3 — The controls with the largest mechanical effect have the least explanation.** The
bite/timing/enabler selects render as three unlabelled dropdowns reading `bite…` `timing…`
`enabler…`. An `on_plan` answer multiplies a credit by **0.0** — silently deleting it. The
credit `anchor` strings, which are the entire justification for each price, are hidden in native
`title=` attributes.

**F4 — Selecting anything scrolls the page to the top.** Ticking a window, setting Reach, or
choosing a cost test loses your place, every time.

**F5 — `python tools/check.py` does not run on this machine at all.** It exits with an
`UnicodeEncodeError` before printing a single finding, because Python on Windows defaults stdout
to cp1252 and `check.py` prints `─` box-drawing rules ([check.py:63](../../../tools/check.py#L63)).
`balance.py`, `validate.py` and `generate.py` are unaffected. CLAUDE.md calls this "the one that
matters", and §10 of this spec depends on it, so it is fixed here rather than logged.

## 2. Root causes (verified in code, not inferred)

| # | Cause | Location |
|---|---|---|
| C1 | `preservingFocus()` returns early with a bare `render()` when the focused element has no `data-focus` key, so scroll is never saved. Checkboxes, `<select>`s and chip buttons have no such key. `replaceChildren()` then collapses `#main` to zero height and the browser clamps `scrollTop` to 0. | [studio.html:786–802](../../../tools/studio.html#L786) |
| C2 | The effect picker's filter `<input>` is constructed fresh inside `effectPicker()`, which `touch()` re-runs on every toggle. The typed query is destroyed on each tick. | [studio.html:1267–1303](../../../tools/studio.html#L1267) |
| C3 | The G2/G5/G7/G9 checkboxes are created with no backing state, so any re-render silently unticks them. | [studio.html:1486–1491](../../../tools/studio.html#L1486) |
| C4 | **The browser computes Reach differently from the checker.** JS uses `min(4, windowCount)`. Python uses *the number of factions strong in at least one declared window*, read from `data/factions.yaml`. The Studio can therefore display a Ceiling that `check.py` disagrees with, and `save()` only drift-checks `baseDelta`. | JS [studio.html:1357](../../../tools/studio.html#L1357) vs Python [scoring.py:157–192](../../../tools/scoring.py#L157) |

## 3. Non-goals

- No change to any budget arithmetic, credit value, gate or rule. `scoring.py` and `rules.py`
  are the source of truth and are **not** edited. This work makes the Studio agree with them and
  explain them; where the two disagree, the Studio is what changes.
- No change to the card file schema. The human-gate ticks are session state, not persisted.
- No change to the left roster, the right rail, or the Library / Factions / Crews / Matrix /
  Health / Problems screens — beyond the C1 fix, which they inherit for free.
- The card face, artwork, flip and lightbox are untouched.

---

## 4. The verdict panel

Replaces the arithmetic half of `proofPanel()` **and** the `scorebar` of `scorePanel()`. One
panel, one verdict, two halves — potential above, actual below. It keeps its current position:
to the right of the card face and the card text, which the designer confirmed works.

Every row is a sentence with a right-aligned figure, using the existing `.ledger` treatment
(leader dots, tabular numerals).

### 4.1 A card with no declared plan

Such a card genuinely has **two** limits — `_gate_g1` checks the base side against the budget
two-sidedly, and both faces against `budget × 1.5` one-sidedly — so both are shown. Worked
example is real: **Moammar, The One Punch Machine Gun**, cost 5, Ascendant, 6/6/0/3, base effect
*Searching (Tutors)* 4, level-up effect *Permanent Buff 5* 5.

```
POTENTIAL POWER — what this card is allowed to spend

  Because it costs 5 Energy ...............................  15
    every point of Energy buys 3 points of power
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

Two bars: base side against 19, both faces against 28.

### 4.2 A card that declares a plan

`_gate_g1` states the Ceiling covers both faces, so this form has one ledger and one bar. The
base budget rows from 4.1 are still shown first, then the credits continue the same ledger.

```
  BASE BUDGET .............................................  19
  Because 3 Characters must be on board first .............  +6
    2 each — they're committed to the plan but not consumed
  Because it telegraphs for 2 full Rounds .................  +10
    5 each — a draw is worth 3, plus a Round of tempo
  ───────────────────────────────────────────────────────────
  ALLOWANCE — budget plus what it pays in other currencies   35
  But only 2 factions can answer it, so it's capped at 1.5×
    Warmongers and Assholes can. Overthinkers and Icons are blind.
  ───────────────────────────────────────────────────────────
  CEILING — the most this card may spend ..................  28
```

A discounted credit shows its arithmetic on the same row rather than in a separate breakdown
list: `2 Rounds × 5 = 10 → ×0.5 → 5`.

**Reach 0 is loud.** When no faction can answer the card, `reach_caps[0]` is `null` and the card
is not printable. This renders as a full-width critical block replacing the CEILING row, naming
the windows that would fix it — not as a `·`-separated arrow in a bar, which is how it reads
today.

### 4.3 The decision line

The piece missing entirely today. Below the bar, one sentence naming the specific moves
available, derived from live state:

- **Over:** `9 over. Cut 9 points of impact, or buy more ceiling: +1 Energy buys 3 points, and
  giving a blind faction a window it can actually use raises the cap. Right now Overthinkers and
  Icons have no answer at all.` (The trailing clause appears only when a plan is declared and at
  least one faction is blind.)
- **Under:** `4 under. This is weaker than its cost pays for — underpowered is as wrong as
  overpowered here, it just fails quietly. Add 4 points of impact, or drop the cost by 1, which
  removes 3 points of budget.`
- **On:** `Exactly on budget. It spends precisely what its cost buys.`
- **Not scorable:** the existing stub message, unchanged.

---

## 5. Status colour model

The rule stated in the `studio.html` CSS header holds: **hue belongs to faction, fill belongs to
status.** Warmongers own red and Assholes own green, so status may not use them.

| State | Token | Value | Glyph | Word |
|---|---|---|---|---|
| On budget (`\|Δ\| ≤ tolerance`) | `--good` | `--color-ink-60` (unchanged) | `✓` | In tolerance |
| **Under** (`Δ > tolerance`) | `--under` **(new)** | `#5c8f9e` dark / `#3d7383` light | `↓` | N under |
| Over, by magnitude | `--warning` / `--serious` / `--critical` (unchanged) | existing ramp | `!` / `✕` | N over |

`--under` is a desaturated steel-teal, deliberately distinct from `--color-cyan` (`#1fb6e8`),
which the app already uses for *interactive* state — pressed chips, focus rings, section labels.
**`--under` must never be applied to an interactive control**, or a dim meter and a selected chip
start speaking the same language.

**Under is only a failure against the base budget.** Spending less than a *ceiling* is fine, and
`ceiling_severity()` already encodes this. So:

- Base side vs base budget → two-sided → may render `--under`.
- Both faces vs `budget × 1.5` → one-sided → under renders `--good`, never `--under`.
- Total vs Ceiling → one-sided → under renders `--good` (it is called headroom, and it is good).

Colour never carries meaning alone: every state ships its glyph and its word, as today.

---

## 6. Page structure

The card page becomes five blocks in this order. Blocks 2 and 3 are the same two halves as the
verdict, so the half of the verdict that is wrong tells you which panel to scroll to.

| # | Panel | Contains |
|---|---|---|
| 1 | **The card** | card face · rules text · level-up condition · ascended text · the §4 verdict panel — unchanged layout |
| 2 | **What raises the ceiling** | Cost stepper · what it pays (13 credits) · the three tests · Reach · windows · the four prohibitions |
| 3 | **What spends it** | the four stat steppers · base keywords + effects · level-up keywords + effects |
| 4 | **Can it be printed** | the gate strip, machine gates and human gates |
| 5 | **Context** | Job / Formation · cost neighbours · playtests |

The Cost stepper moves into block 2 and the four stat steppers into block 3, splitting today's
combined `Cost & stats` panel. This is deliberate: cost is the only control that raises the
ceiling, and the stats are the largest single line of spend.

---

## 7. The teaching layer

Printed on screen: anything that changes a number being chosen. Left in tooltips: vocabulary.
The existing `GLOSSARY` / `tipped()` / `ruleDocs` machinery is kept and extended, not replaced.

### 7.1 Credits

Each of the 13 credits shows its `anchor` as visible text under the label. `anchor` currently
reaches the DOM only as a `title=` attribute ([studio.html:1400](../../../tools/studio.html#L1400)).

### 7.2 The three tests

`bite` / `timing` / `enabler` stop being bare dropdowns. Each renders as its question, with each
option naming its consequence and its multiplier, and the live arithmetic below:

```
Full Rounds between commitment and payoff                      +5 ea
  Worth 5 because a draw is worth 3, plus a Round of tempo.
  Does paying it make you worse at your job?
    ○ It competes with the plan               full credit   ×1.0
    ● Neutral                                 half credit   ×0.5
    ○ It IS the plan — you'd do it anyway     no credit     ×0.0
  2 Rounds × 5 = 10  →  ×0.5  →  5 points earned
```

The question text and option wording come from `docs/design/balance-philosophy.md` Part Two and
are defined once in `data/plan-credits.yaml` (§8), not hardcoded in the markup.

### 7.3 Reach

Reach becomes derived and explained rather than guessed. A per-faction readout shows which
factions can answer the card and which declared window earns each ✓, read from
`DB.factions[name].windows`:

```
  Warmongers    ✓  strong at W3 On resolution
  Overthinkers  ✗  blind at every window you declared
  Assholes      ✓  strong at W1 Pre-assembly
  Icons         ✗  blind at every window you declared
                   → Reach 2 → cap 1.5× base = 28
```

The 0–4 chips remain, relabelled as an explicit **override**. When an override differs from the
computed value, both are shown and the override is marked as such — mirroring
`reachOverridden` in the server payload.

### 7.4 Gates

Every gate failure gains a fix line beside the complaint. The four human gates keep their
`HUMAN_ONLY_GATES` description and gain session-persistent ticks (§9.3).

---

## 8. Data change

One additive field per credit in `data/plan-credits.yaml`, and one block for the tests:

```yaml
credits:
  - key: telegraph_rounds
    label: Full Rounds between commitment and payoff
    points: 5
    anchor: a draw (3) plus a Round of tempo
    sentence: Because it telegraphs for {n} full Round{s}    # NEW
```

```yaml
cost_tests:
  bite:
    question: Does paying it make you worse at your job?      # NEW
    options:                                                  # NEW
      competes:  {value: 1.0, label: It competes with the plan,        note: full credit}
      neutral:   {value: 0.5, label: Neutral,                          note: half credit}
      on_plan:   {value: 0.0, label: It IS the plan — you'd do it anyway, note: no credit}
```

**Backward compatibility is required, and settles the shape.** `scoring.py` reads `cost_tests`
as a flat `{test: {answer: multiplier}}` map ([scoring.py:116–127](../../../tools/scoring.py#L116)).
The nested form sketched above would break that.

**The flat `cost_tests` map is therefore left exactly as it is**, and the copy goes in a sibling
block that only the Studio reads:

```yaml
cost_test_copy:
  bite:
    question: Does paying it make you worse at your job?
    options:
      competes: {label: It competes with the plan,             note: full credit}
      neutral:  {label: Neutral,                               note: half credit}
      on_plan:  {label: It IS the plan — you'd do it anyway,   note: no credit}
```

Multipliers are read from `cost_tests` and displayed; they are never duplicated into
`cost_test_copy`, so the two can never disagree about a number. An answer present in `cost_tests`
but missing from `cost_test_copy` falls back to its raw key, so a multiplier added later without
copy still renders. Nothing else reads these keys —
`rules.py` touches `plan_config()` only for `ceiling_quota`
([rules.py:670](../../../tools/rules.py#L670)) — but `scoring.py` is source of truth and is
not to be edited for a presentation change.

The JS falls back to `label` when `sentence` is absent, so a credit added later without copy
still renders correctly.

---

## 9. Interaction fixes

### 9.1 Scroll and focus (C1)

`preservingFocus()` saves and restores `scrollTop` for `#main` and `#rail`
**unconditionally**, before the `data-focus` early return. Focus restoration keeps its current
`data-focus` mechanism, and every interactive control gains a key:

| Control | Key |
|---|---|
| window checkbox | `win:<key>` |
| Reach chip | `reach:<n>` |
| credit ± buttons | `credit-<dir>:<key>` |
| cost-test control | `test:<credit>:<test>` |
| keyword chip | `kw:<side>:<name>` |
| effect checkbox | `ef:<side>:<name>` |
| effect filter box | `efsearch:<side>` |
| status select | `status` |
| human gate checkbox | `hg:<id>` |

### 9.2 Effect filter (C2)

The typed query moves to module-level state keyed by side, so it survives the re-render that
follows a tick. Paired with the `efsearch:<side>` focus key, filtering and ticking becomes
continuous instead of one-tick-per-retype.

### 9.3 Human gate ticks (C3)

Session-scoped `Set` keyed by `relPath + gate id`. Not written to the card file — that would be a
schema change, and is logged as a follow-up rather than done here.

### 9.4 `check.py` on Windows (F5)

`check.py` reconfigures its own stdout to UTF-8 at start-up, so the box-drawing rules it prints
survive a cp1252 console. One line, no behavioural change, no change to any finding. Verified by
the command running to completion without `PYTHONIOENCODING` set.

### 9.5 Reach correctness (C4)

`scorePlan()` is corrected to mirror `Plan.reach_value()` exactly:

1. explicit `plan.reach` wins, clamped to 0–4;
2. otherwise, if no windows are declared → `null`;
3. otherwise count factions with `windows[w] === "strong"` for any declared `w`;
4. if no faction carries window profiles at all, fall back to `min(4, windowCount)` — matching
   the `_answering() is None` branch in Python.

Note this can legitimately produce **Reach 0** — windows declared, no faction strong in any of
them — which means not printable. §4.2 requires that state to render loudly.

`save()`'s drift check is extended from `baseDelta` alone to also compare `reach` and `ceiling`
against the server's authoritative `saved.score`.

---

## 10. Verification

The server already ships its own authoritative `scoring.score(card).as_dict()` for every card in
the bootstrap payload ([studio.py:88](../../../tools/studio.py#L88)), which makes the browser's
mirror directly testable against it.

1. **Parity self-check.** On boot, compare the JS `scoreDraft()` + `scorePlan()` result against
   `card.score` for every card the server reports as `scorable` — stubs with no cost are skipped,
   since both sides agree there is nothing to score. Compared fields: `budget`, `baseSpent`,
   `baseDelta`, `reach`, `ceiling`, `headroom`.

   This ships permanently rather than being a throwaway test: it is the guard that would have
   caught C4 the day it was introduced. It stays silent when the two agree, and raises a toast
   naming the first divergent card and field when they do not. Zero divergences is the acceptance
   condition for §9.5.
2. `python tools/check.py` runs to completion on a stock Windows console with no
   `PYTHONIOENCODING` set (§9.4), and reports **exactly the recorded baseline: 34 blocking, 77
   warnings** — `F2×7, F4×19, F6×8, GAP×10, W1×2, W10×2, W15×1, W2×2, W3×6, W4×12, W6×13, W8×4,
   W9×25`. This work must not alter a single card verdict.
3. `python tools/generate.py --check` clean — no generated doc goes stale.
4. Browser verification of the four reported failures, with the studio running:
   - tick a window at the bottom of the page → **scroll does not move**, checkbox keeps focus;
   - set Reach, change a cost test, use a credit ± button → same;
   - type `removal` in the effect filter, tick a result → **filter text survives**;
   - tick human gate G9, change a stat → **G9 stays ticked**.
5. Read the verdict panel for one no-plan card (Moammar: budget 19, spends 19, exactly on) and
   one plan-declaring card, confirming both forms of §4 render and the figures match `check.py`.
6. Both themes, since `--under` is a new token in each.

---

## 11. Follow-ups, not in scope

- **A window has no field naming the card or rule that exercises it.** The rulebook requires one
  ("someone could theoretically remove it" is not a window) but the schema has nowhere to put it,
  so the requirement is unenforceable. Needs a schema decision → `open-questions.md`.
- Human gate ticks are session-only; persisting them is a schema change.
- Opening a card whose `plan` has only `requires` causes `planOf()` to write back empty
  `pays: {}` and `windows: []`. Harmless — `new_card()` already writes those keys — but it is a
  diff the designer did not make. Left alone deliberately.
