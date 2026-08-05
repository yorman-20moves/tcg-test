# Card Studio Legibility Overhaul — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Card Studio explain the balance philosophy at the point of decision, instead of assuming the designer already knows it — and fix the four interaction defects that make it painful to use.

**Architecture:** `tools/studio.html` is a single self-contained page: inline `<style>`, then inline `<script>` with a hand-rolled `el()` DOM builder. There is no framework and no build step. Every edit is a direct edit to that one file. `tools/scoring.py` is the source of truth for all arithmetic; the JS in `studio.html` is a *mirror* of it, and where they disagree the JS is what changes. A new boot-time parity check compares the two across all cards so the mirror can never drift again.

**Tech Stack:** Python 3.14 (stdlib `http.server`), vanilla ES2022, no dependencies, no bundler. Tests are pytest (`tools/tests/`). JS is verified by the in-page parity check plus browser acceptance steps.

## Global Constraints

- **`tools/scoring.py` and `tools/rules.py` are NOT edited.** They are source of truth. Every task in this plan is presentation. If the JS and Python disagree, the JS changes.
- **The baseline must not move: `34 blocking, 77 warnings`**, breakdown `F2×7, F4×19, F6×8, GAP×10, W1×2, W10×2, W15×1, W2×2, W3×6, W4×12, W6×13, W8×4, W9×25`. Verify with `python tools/check.py` after every task.
- **The card file schema does not change.** No new frontmatter keys.
- **Hue belongs to faction, fill belongs to status** (the rule stated in the `studio.html` CSS header, line 18–29). Status may never use red or green — Warmongers own `#e23b3b`, Assholes own `#3fa757`.
- **`--under` (`#5c8f9e` dark / `#3d7383` light) may never be applied to an interactive control.** `--color-cyan` already means "selected/focused"; `--under` means "under budget". Keeping them apart is the point of using a separate token.
- **Colour never carries meaning alone.** Every status ships a glyph and a word, as the existing code already does.
- **Comments explain *why*, in the voice of the surrounding file** — full sentences, present tense, explaining the reason a thing is the way it is. Match the density already in `studio.html`. Do not add narrating comments (`// loop over cards`).
- **Spec:** `docs/superpowers/specs/2026-08-05-card-studio-legibility-design.md`. Read the relevant section before starting each task.

---

### Task 1: Make `check.py` run on Windows

Spec §9.4 / F5. Smallest task, and it unblocks the verification step every later task depends on.

**Files:**
- Modify: `tools/check.py` (imports block near line 1–20, and add the reconfigure before `main()` runs)
- Test: `tools/tests/test_check_encoding.py` (create)

**Interfaces:**
- Consumes: nothing.
- Produces: nothing importable. Later tasks rely on `python tools/check.py` running to completion without `PYTHONIOENCODING` set.

- [ ] **Step 1: Reproduce the failure**

Run, with no `PYTHONIOENCODING` in the environment:

```bash
.venv/Scripts/python.exe tools/check.py
```

Expected: `UnicodeEncodeError: 'charmap' codec can't encode characters in position 2-3` raised from `tools/check.py:63`, which is the `print(f"\n── {current} " + "─" * (72 - len(current)))` line. Exit code is non-zero for the wrong reason — the crash, not the findings.

- [ ] **Step 2: Write the failing test**

Create `tools/tests/test_check_encoding.py`. This runs the real CLI in a subprocess with a legacy-codepage stdout forced on, which is what a stock Windows console gives you:

```python
"""check.py must survive a legacy-codepage console.

CLAUDE.md calls check.py "the one that matters", and it printed box-drawing rules to a
stdout that Python defaults to cp1252 on Windows -- so on the designer's own machine the
command died with UnicodeEncodeError before showing a single finding.
"""
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_check_runs_on_a_legacy_codepage_console():
    # Inherit the real environment -- a bare dict drops SYSTEMROOT and Windows fails to start
    # the interpreter at all, which would pass this test for entirely the wrong reason.
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "check.py")],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=REPO_ROOT, env=env,
    )
    assert "UnicodeEncodeError" not in result.stderr, result.stderr
    assert "blocking" in result.stdout
```

- [ ] **Step 3: Run the test and confirm it fails**

Run: `.venv/Scripts/python.exe -m pytest tools/tests/test_check_encoding.py -v`
Expected: FAIL, with `UnicodeEncodeError` present in the captured stderr.

- [ ] **Step 4: Implement the fix**

In `tools/check.py`, immediately after the existing imports, add:

```python
# The report draws box rules with U+2500. Python picks the console codepage for stdout on
# Windows, which is cp1252 here, so the first section header killed the process before it
# printed a single finding -- on the one command the contract calls the one that matters.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

If `sys` is not already imported in `check.py`, add `import sys` to the stdlib import block, keeping the existing alphabetical grouping.

- [ ] **Step 5: Run the test and confirm it passes**

Run: `.venv/Scripts/python.exe -m pytest tools/tests/test_check_encoding.py -v`
Expected: PASS.

- [ ] **Step 6: Confirm the baseline and the whole suite**

Run: `.venv/Scripts/python.exe tools/check.py`
Expected: runs to completion with no `PYTHONIOENCODING` set, final line reads exactly `34 blocking, 77 warnings   (F2×7, F4×19, F6×8, GAP×10, W1×2, W10×2, W15×1, W2×2, W3×6, W4×12, W6×13, W8×4, W9×25)`.

Run: `.venv/Scripts/python.exe -m pytest tools/tests -q`
Expected: 13 passed.

- [ ] **Step 7: Commit**

```bash
git add tools/check.py tools/tests/test_check_encoding.py
git commit -m "Let check.py print its box rules on a cp1252 console"
```

---

### Task 2: Stop the page resetting on every selection

Spec §9.1 / C1. This is the defect the designer reported first.

**Files:**
- Modify: `tools/studio.html:786-802` (`preservingFocus`)
- Modify: `tools/studio.html` — add `data-focus` to the controls listed below

**Interfaces:**
- Consumes: nothing.
- Produces: the convention that **every interactive control carries a `data-focus` key**. Later tasks that create controls must follow it.

- [ ] **Step 1: Reproduce the failure in the browser**

Start the studio (`preview_start` with the `card-studio` config in `.claude/launch.json`, or reuse the server already on `127.0.0.1:8765`). Select a card that has a plan, e.g. `Decoy, 1st Crown - Supreme Inca`. Scroll to the windows checkboxes near the bottom of The Score panel. Tick one.

Expected: `#main` jumps to `scrollTop === 0`. Confirm by reading `document.querySelector("#main").scrollTop` with `javascript_tool` before and after.

- [ ] **Step 2: Rewrite `preservingFocus`**

Replace `tools/studio.html:786-802` entirely with:

```js
function preservingFocus(render){
  /* Scroll is saved unconditionally, before anything asks about focus. It used to be saved
     only when the caret sat in a keyed text field, so every checkbox, chip and <select> --
     none of which carry a key -- fell straight through to a bare render(). replaceChildren()
     then collapsed the panel to zero height, the browser clamped scrollTop to 0, and ticking
     a window at the bottom of the page threw you back to the top of it. */
  const panes=[$("#main"),$("#rail")].filter(Boolean);
  const tops=panes.map(p=>p.scrollTop);
  const live=document.activeElement;
  const key=live&&live.dataset?live.dataset.focus:null;
  /* type=number throws on selectionStart rather than returning null, so both ends are read
     and re-applied defensively */
  let head=null, tail=null;
  try{ head=live.selectionStart; tail=live.selectionEnd; }catch{}

  render();

  panes.forEach((p,i)=>{ p.scrollTop=tops[i]; });
  if(!key) return;
  const back=document.querySelector(`[data-focus="${CSS.escape(key)}"]`);
  if(!back || back===live) return;             /* nothing rebuilt it -- the caret never moved */
  back.focus({preventScroll:true});
  if(head!=null && back.setSelectionRange){ try{ back.setSelectionRange(head,tail); }catch{} }
}
```

- [ ] **Step 3: Add a `data-focus` key to every control that lacks one**

Each of these is an existing `el(...)` call; add the `"data-focus"` property to its props object. Do not change any other behaviour.

| File location | Element | Key to add |
|---|---|---|
| `scorePanel` windows loop | the `<input type=checkbox>` | `"data-focus":"win:"+w.key` |
| `scorePanel` reach loop | the `<button class="chip">` | `"data-focus":"reach:"+n` |
| `scorePanel` credit grid | the `−` `.sbtn` | `"data-focus":"credit-dn:"+c.key` |
| `scorePanel` credit grid | the `+` `.sbtn` | `"data-focus":"credit-up:"+c.key` |
| `scorePanel` cost tests | each `<select>` | `"data-focus":"test:"+c.key+":"+test` |
| `keywordChips` | the `<button class="chip">` | `"data-focus":"kw:"+side+":"+k.name` |
| `effectPicker` `drawList` | the `<input type=checkbox>` | `"data-focus":"ef:"+side+":"+e.name` |
| `effectPicker` | the `.efsearch` input | `"data-focus":"efsearch:"+side` |
| `renderMainNow` card head | the status `<select>` | `"data-focus":"status"` |
| `stepper` | the `−` and `+` `.sbtn` | `"data-focus":"step-dn:"+label` / `"step-up:"+label` |

`effectPicker(side)` and `keywordChips(side)` already receive `side`. The `stepper()` helper already receives `label`.

- [ ] **Step 4: Verify in the browser**

Reload. For each of these, record `#main` scrollTop before and after with `javascript_tool`, and confirm it is unchanged:

- tick a window checkbox at the bottom of the page
- click a Reach chip
- click a credit `+` button
- change a cost-test `<select>`
- click a keyword chip
- tick an effect checkbox

Then confirm focus survives: after ticking a window, `document.activeElement.dataset.focus` should read `win:<key>`.

- [ ] **Step 5: Confirm nothing else broke**

Switch through every mode — Cards, Library, Factions, Crews, Matrix, Health, Problems — and confirm each renders. Read console messages; expected: no errors.

Run: `.venv/Scripts/python.exe tools/check.py` — expected: unchanged baseline.

- [ ] **Step 6: Commit**

```bash
git add tools/studio.html
git commit -m "Keep your place when you tick a window

preservingFocus only saved scroll when the caret sat in a keyed text field.
Checkboxes, chips and selects carry no key, so they fell through to a bare
render(), replaceChildren() collapsed the panel, and the browser clamped
scrollTop to 0. Scroll is now saved before focus is even considered, and
every interactive control carries a key so focus comes back too."
```

---

### Task 3: Stop the effect filter and the human gates forgetting

Spec §9.2 and §9.3 / C2 and C3.

**Files:**
- Modify: `tools/studio.html:1267-1303` (`effectPicker`)
- Modify: `tools/studio.html:1486-1491` (the human gates block inside `gateStrip`)

**Interfaces:**
- Consumes: the `data-focus` convention from Task 2.
- Produces: `EF_QUERY` (module-level `{base:"", ascended:""}`) and `HUMAN_TICKS` (module-level `Set` of `"<relPath>|<gateId>"`).

- [ ] **Step 1: Reproduce both failures**

In the browser: type `removal` into the base-side effect filter, then tick a result. Expected failure: the filter box is empty and the full 51-entry list is back.

Then tick human gate G9, then click the Cost `+` stepper. Expected failure: G9 is unticked.

- [ ] **Step 2: Persist the effect filter query**

Above `effectPicker`, add:

```js
/* The filter query outlives the re-render that a tick triggers. touch() rebuilds the whole
   picker, so a query held only in the input's own value was destroyed by the very act of
   ticking a result -- you got one effect per retype. */
const EF_QUERY={base:"",ascended:""};
```

Inside `effectPicker(side)`, change the search input construction to seed from and write to that store:

```js
  const search=el("input",{class:"efsearch",placeholder:`Filter ${DB.effects.length} effect types…`,
    "data-focus":"efsearch:"+side, value:EF_QUERY[side]||""});
```

and change the `drawList` query read plus the listener:

```js
  const drawList=()=>{
    const q=(EF_QUERY[side]||"").toLowerCase();
    ...unchanged...
  };
  search.addEventListener("input",()=>{ EF_QUERY[side]=search.value; drawList(); });
```

Note `el()` sets `value` via `setAttribute`, which for a text input seeds the initial value correctly.

- [ ] **Step 3: Persist the human gate ticks**

Above `gateStrip`, add:

```js
/* Session-scoped, keyed by card. The four human gates were plain checkboxes with nothing
   behind them, so any re-render silently unticked them -- reading G9 and then touching a
   stat threw the answer away. Not written to the card file: that would be a schema change,
   and the schema is not this change's to move. */
const HUMAN_TICKS=new Set();
const humanKey=id=>`${draft.relPath}|${id}`;
```

Replace the human gates loop body inside `gateStrip` with:

```js
  for(const [id,desc] of Object.entries(DB.humanGates))
    human.append(el("label",{class:"hg"},
      el("input",{type:"checkbox",checked:HUMAN_TICKS.has(humanKey(id)),
        "data-focus":"hg:"+id,
        onchange:e=>{ e.target.checked?HUMAN_TICKS.add(humanKey(id)):HUMAN_TICKS.delete(humanKey(id)); }}),
      tipped(el("b",{text:id}), id),
      el("span",{class:"sec",text:desc})));
```

The handler deliberately does **not** call `touch()` — a human gate tick is not a change to the card, and marking the card dirty over it would be wrong.

- [ ] **Step 4: Verify in the browser**

- Type `removal` in the base effect filter, tick a result → filter text still reads `removal`, list still filtered, tick applied.
- Tick G9, click Cost `+` → G9 still ticked, and the save bar shows dirty from the cost change only.
- Select a different card and come back → G9 tick is still there for the first card and absent on the second (the key includes `relPath`).

- [ ] **Step 5: Confirm the baseline**

Run: `.venv/Scripts/python.exe tools/check.py` — expected: unchanged baseline.

- [ ] **Step 6: Commit**

```bash
git add tools/studio.html
git commit -m "Stop the effect filter and the human gates forgetting

Both were state held only in a DOM node that touch() throws away. The filter
query wiped itself on every tick, so filtering and ticking could not be done
in the same breath; the human gate ticks had nothing behind them at all."
```

---

### Task 4: Make the browser compute Reach the way the checker does

Spec §9.5 and §10.1 / C4. This must land before the verdict panel, so the panel displays numbers that agree with `check.py`.

**Files:**
- Modify: `tools/studio.html:1326-1371` (`planOf`, `costFactor`, `scorePlan`)
- Modify: `tools/studio.html` `save()` — extend the drift check
- Modify: `tools/studio.html` boot IIFE — add the parity check

**Interfaces:**
- Produces:
  - `scorePlan(s, plan)` — `plan` optional, defaults to `planOf()`. Return value gains three fields on top of today's: `reachComputed` (number|null), `answering` (array of faction-name strings), `reachOverridden` (boolean).
  - `costFactor(key, plan)` — `plan` now an explicit second parameter.
  - `answeringFactions(windows)` → `string[]|null` — null means `factions.yaml` carries no window profiles at all.
  - `parityCheck()` → array of `{name, field, js, py}`.

- [ ] **Step 1: Read the Python this must mirror**

Read `tools/scoring.py:157-196` (`Plan.reach_value`, `computed_reach`, `_answering`, `window_count`). The rule is:

1. explicit `plan.reach` wins, clamped 0–4;
2. otherwise no windows declared → `null`;
3. otherwise count factions with `windows[w] === "strong"` for **any** declared `w`;
4. if `factions.yaml` yields no factions at all, fall back to `min(4, windowCount)`.

The current JS does **only** step 4, which is the bug.

- [ ] **Step 2: Give `costFactor` and `scorePlan` an explicit plan parameter**

Do this *first*, before the parity check, and change **nothing else about the arithmetic yet.**
`scorePlan` currently reads the module-level `draft` through `planOf()`, so it can only ever
score the card that happens to be open — which makes the parity check in Step 3 impossible to
write. `planOf()` stays exactly as it is for the editing UI.

```js
/* Mirrors scoring.py. Credits earn the Allowance; Reach CAPS it.
   Each cost is discounted by the three tests (bite / timing / enabler). */
function costFactor(key, plan){
  const scales=DB.plan.cost_tests||{}, chosen=(plan.tests||{})[key]||{};
  let f=1;
  for(const [test,opts] of Object.entries(scales)){
    const ans=chosen[test];
    if(ans!==undefined && opts[ans]!==undefined) f*=Number(opts[ans]);
  }
  return f;
}
```

In `scorePlan`, change the signature to `function scorePlan(s, plan){`, add `plan = plan || planOf();`
as its first line, delete the old `const plan=planOf();`, and change the one `costFactor(k)` call to
`costFactor(k,plan)`. Guard the two reads that assumed `planOf()` had already defaulted them:
`Object.entries(plan.pays||{})` and `(plan.windows||[])`.

**Leave the buggy Reach line alone for now** — Step 4 has to be able to watch it fail.

- [ ] **Step 3: Add the parity check**

Add above `scorePlan`:

```js
/* The server ships its own authoritative score for every card in the bootstrap payload, which
   makes this mirror directly testable against it. It stays quiet when the two agree. It exists
   because they silently stopped agreeing: this file computed Reach from how many windows were
   ticked, while scoring.py computes it from how many factions are strong in one, so the Studio
   could show a Ceiling check.py disagreed with and nothing said so. */
function parityCheck(){
  const out=[];
  for(const c of cards){
    if(!c.score || !c.score.scorable) continue;   /* stubs: both sides agree there is nothing to score */
    const js=scoreDraft(c), p=scorePlan(js, c.meta.plan||{});
    const mine={budget:js.budget, baseSpent:js.baseSpent, baseDelta:js.baseDelta,
                reach:p.reach, ceiling:p.ceiling, headroom:p.headroom};
    for(const [field,value] of Object.entries(mine))
      if(value!==c.score[field]) out.push({name:c.meta.name, field, js:value, py:c.score[field]});
  }
  return out;
}
```

- [ ] **Step 4: Run it and watch it fail**

Reload the studio, then in the console via `javascript_tool`: `JSON.stringify(parityCheck())`.

Expected: a non-empty array containing `reach` and `ceiling` disagreements on cards that declare
windows. **Record the output verbatim in your report** — it is the proof C4 was real, and it is
the only evidence that the fix in Step 5 actually fixed something.

If the array comes back empty, stop: either no card declares a window (check with
`cards.filter(c=>(c.meta.plan||{}).windows?.length).map(c=>c.meta.name)`), or Step 2 was
implemented incorrectly.

- [ ] **Step 5: Add `answeringFactions` and correct `scorePlan`**

```js
/* Which factions can actually answer a card that offers these windows -- the same question
   scoring.py's Plan._answering asks, off the same window profiles in data/factions.yaml.
   null means no faction carries a profile at all, which is the one case where falling back
   to counting windows is right. */
function answeringFactions(windows){
  const briefs=DB.factions||{};
  const names=Object.keys(briefs);
  if(!names.length) return null;
  const declared=new Set(windows||[]);
  return names.filter(n=>{
    const prof=(briefs[n]||{}).windows||{};
    for(const w of declared) if(prof[w]==="strong") return true;
    return false;
  });
}

function scorePlan(s, plan){
  plan = plan || planOf();
  const cfg=DB.plan;
  const table=Object.fromEntries(cfg.credits.map(c=>[c.key,c]));
  let credits=0;
  for(const [k,q] of Object.entries(plan.pays||{})){
    const e=table[k]; if(!e||!q) continue;
    let raw=e.points*q;
    if(k==="narrowness") raw=Math.min(raw,cfg.narrowness_cap);
    credits+=Math.trunc(raw*costFactor(k,plan));
  }
  const valid=new Set(cfg.windows.map(w=>w.key));
  const declaredWindows=(plan.windows||[]).filter(w=>valid.has(w));
  const windows=declaredWindows.length;
  const declared = credits>0 || windows>0 || plan.reach!=null;

  /* Reach is how many FACTIONS can answer it, not how many windows you ticked. Counting
     windows was this file's own invention and it disagreed with the checker. */
  const answering=answeringFactions(declaredWindows);
  const reachComputed = windows>0
    ? (answering===null ? Math.min(4,windows) : answering.length)
    : null;
  const reachOverridden = plan.reach!=null;
  const reach = reachOverridden ? Math.max(0,Math.min(4,plan.reach)) : reachComputed;

  const allowance=s.budget+credits;
  const caps=cfg.reach_caps||{};
  let cap;
  if(reach===null) cap=s.budget;                       // no plan: the original rule
  else {
    const mult = caps[reach]!==undefined ? caps[reach] : caps[String(reach)];
    cap = (mult===null||mult===undefined) ? null : Math.trunc(s.budget*Number(mult));
  }
  const ceiling = cap===null ? 0 : Math.min(allowance,cap);
  const total=s.baseSpent+s.ascendedSpent;
  return {credits,windows,declaredWindows,reach,reachComputed,reachOverridden,
          answering:answering||[],allowance,earned:allowance,cap,ceiling,total,
          headroom:ceiling-total, hasPlan:declared};
}
```

- [ ] **Step 6: Update the one existing caller**

`gatesOf()` calls `scorePlan(s)` — that still works, since `plan` defaults. `scorePanel(s)` calls `scorePlan(s)` — same. No signature breakage.

- [ ] **Step 7: Run the parity check and watch it pass**

In the browser: `JSON.stringify(parityCheck())`.
Expected: `[]`.

If it is not empty, the JS is still wrong — `scoring.py` is right by definition. Fix the JS.

- [ ] **Step 8: Ship the parity check on boot and extend the save drift check**

In the boot IIFE, after `select(cards[0])`:

```js
  const drift=parityCheck();
  if(drift.length){
    const first=drift[0];
    console.warn("score parity", drift);
    toast(`Scoring drift: ${first.name} ${first.field} — studio ${first.js}, server ${first.py}. `
          +`${drift.length} in total; see the console.`, 9000);
  }
```

In `save()`, replace the `baseDelta`-only drift check with:

```js
    /* reconcile the browser's arithmetic against the server's */
    const local=scoreDraft(draft), lp=scorePlan(local, draft.meta.plan||{});
    const drift = local.scorable && saved.score.scorable &&
      (local.baseDelta!==saved.score.baseDelta || lp.reach!==saved.score.reach
       || lp.ceiling!==saved.score.ceiling);
```

- [ ] **Step 9: Verify**

Reload with a clean console. Expected: no drift toast, no console warning.

Run: `.venv/Scripts/python.exe tools/check.py` — expected: unchanged baseline.

- [ ] **Step 10: Commit**

```bash
git add tools/studio.html
git commit -m "Compute Reach the way the checker computes it

The browser counted the windows you ticked; scoring.py counts the factions
that are strong in one. The Studio could therefore show a Ceiling check.py
disagreed with, and save() only ever drift-checked baseDelta so nothing
warned. A boot-time parity check now compares every scorable card against
the server's own authoritative score, so the mirror cannot drift silently
again."
```

---

### Task 5: Add the narrative copy to `data/plan-credits.yaml`

Spec §8. Data-only; no behaviour change until Tasks 6–7 read it.

**Files:**
- Modify: `data/plan-credits.yaml`

**Interfaces:**
- Produces: `sentence:` on each of the 13 credits, and a new top-level `cost_test_copy:` block. Both are read only by `studio.html`.

- [ ] **Step 1: Confirm nothing in Python reads these keys**

Run: `grep -rn "cost_test_copy\|\bsentence\b" tools/` — expected: no hits.
Read `tools/scoring.py:113-128` (`Plan._discount`) and confirm it iterates `plan_config()["cost_tests"]` as a flat `{test: {answer: multiplier}}` map. **`cost_tests` must therefore keep its exact current shape.** The copy goes in a sibling block.

- [ ] **Step 2: Add `sentence:` to each credit**

`{n}` is substituted with the quantity; `{s}` with `""` or `"s"`. Add one line per credit, after its `anchor:`:

| key | `sentence:` |
|---|---|
| `cards_spent` | `Because it permanently spends {n} other card{s}` |
| `extra_energy` | `Because it costs {n} Energy above its printed cost` |
| `characters_consumed` | `Because it sacrifices {n} of your own Character{s}` |
| `attachments_consumed` | `Because it consumes {n} of your own Attachment{s}` |
| `characters_required` | `Because {n} Character{s} must be on board first` |
| `telegraph_rounds` | `Because it telegraphs for {n} full Round{s}` |
| `actions_surrendered` | `Because it hands the opponent {n} action{s}` |
| `life_paid` | `Because it pays {n} × 2 Life Points` |
| `opponent_resources_given` | `Because it hands the opponent {n} Energy, card{s} or piece{s} of board` |
| `attachments_required` | `Because {n} Attachment{s} or other non-Character piece{s} must be in play` |
| `board_state_required` | `Because you have to engineer {n} specific board state{s} first` |
| `once_per_game` | `Because it can only ever happen once in the whole Game` |
| `narrowness` | `Because it is live only in some matchups — narrowness {n}` |

- [ ] **Step 3: Add the `cost_test_copy` block**

Append after the existing `cost_tests:` block, leaving `cost_tests:` itself **completely unchanged**:

```yaml
# Studio-only wording for the three tests above. The multipliers are NOT repeated here -- they
# are read from cost_tests, so the two can never disagree about a number. An answer with no
# copy falls back to its raw key.
cost_test_copy:
  bite:
    question: Does paying it make you worse at the thing this card wants to do?
    why: A cost you were happy to pay is not a cost. It only earns credit if it hurts.
    options:
      competes: {label: It competes with the plan, note: it costs you something you wanted}
      neutral:  {label: Neutral, note: you would not have used it either way}
      on_plan:  {label: It IS the plan, note: you would have done this anyway}
  timing:
    question: When do you pay it, relative to the payoff?
    why: Paying afterwards is not a risk. By then you already have what you paid for.
    options:
      before:    {label: Before the payoff, note: you pay, then hope}
      at_payoff: {label: At the moment it pays, note: you pay and collect together}
      after:     {label: After it has landed, note: you already have the payoff}
  enabler:
    question: Does another card hand this to you for free?
    why: A cost a crewmate pays for you is a cost the card never actually pays.
    options:
      none:    {label: Nothing hands it to you, note: you pay it yourself}
      faction: {label: A faction card does, note: it is available but costs a slot}
      crew:    {label: A crewmate does, note: your own crew sets it up for free}
```

- [ ] **Step 4: Verify the YAML still loads and nothing moved**

Run:

```bash
.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'tools'); import scoring; c=scoring.plan_config(); print(sorted(c['cost_tests'].keys())); print(len(c['credits'])); print(all('sentence' in x for x in c['credits'])); print(sorted(c['cost_test_copy'].keys()))"
```

Expected: `['bite', 'enabler', 'timing']` / `13` / `True` / `['bite', 'enabler', 'timing']`.

Run: `.venv/Scripts/python.exe tools/check.py` — expected: unchanged baseline. Any movement means a credit value was disturbed; revert and redo.

Run: `.venv/Scripts/python.exe tools/generate.py --check` — expected: clean.

- [ ] **Step 5: Commit**

```bash
git add data/plan-credits.yaml
git commit -m "Give every credit and cost test its plain-language wording

The prices were already anchored; what was missing was the sentence that
says what paying one actually means. Multipliers stay in cost_tests and are
not repeated in the copy block, so the two cannot disagree about a number."
```

---

### Task 6: The verdict panel

Spec §4 and §5 — the centrepiece. Replaces the arithmetic half of `proofPanel()` and the `scorebar` of `scorePanel()` with one narrative ledger.

**Files:**
- Modify: `tools/studio.html` `:root` and `:root[data-theme="light"]` (lines ~63–95) — add `--under`
- Modify: `tools/studio.html` ~line 344–347 — add `.under-c` / `.under-bg`
- Modify: `tools/studio.html` — add `.vledger` styles near the existing `.ledger` block (~line 358)
- Modify: `tools/studio.html:1206-1251` (`proofPanel`)
- Modify: `tools/studio.html:1373-1393` — delete the `bar` from `scorePanel`

**Interfaces:**
- Consumes: `scorePlan(s, plan)` and its `answering` / `reachComputed` fields from Task 4; `sentence:` from Task 5.
- Produces:
  - `verdictOf(delta, twoSided)` → `{dir:"on"|"under"|"over", cls, glyph, word}`
  - `creditSentence(creditDef, n)` → string
  - `verdictPanel(s)` → the panel node, called from `proofPanel`

- [ ] **Step 1: Add the `--under` token and its classes**

In `:root`, in the status ramp block:

```css
  /* status ramp — fill channel. Neutral, then the system orange escalating. Under-budget gets
     its own cool tone rather than a step on that ramp: it is a quiet failure, the card simply
     does nothing, and it must not be mistaken for the cyan that means "selected". */
  --good:var(--color-ink-60); --under:#5c8f9e; --warning:#c08a3e;
  --serious:var(--color-orange); --critical:#ff4d3d;
```

In `:root[data-theme="light"]`, alongside the existing `--warning` / `--critical` overrides:

```css
  --under:#3d7383;
```

Beside the existing `.good-c` / `.good-bg` rules:

```css
.under-c{color:var(--under)} .under-bg{background:var(--under)}
```

- [ ] **Step 2: Add `verdictOf`**

Place immediately after `ceilingSeverity` (~line 999):

```js
/* Magnitude and direction are different questions. Magnitude picks how loud; direction picks
   which voice. Over runs the system's hot ramp. Under gets one cool tone and no ramp, because
   under is a quiet failure and there is nothing to escalate to.

   Under is a failure only against the BASE budget, which is two-sided -- an underspent card is
   a card that does nothing for its cost. Under a CEILING is called headroom and it is good,
   which is exactly what ceilingSeverity already encodes. */
function verdictOf(delta, twoSided){
  const cls = twoSided ? severity(delta) : ceilingSeverity(delta);
  if(cls==="good") return {dir:"on", cls:"good", glyph:"✓",
    word: twoSided||delta<=0 ? "In tolerance" : `${delta} headroom`};
  if(delta>0) return {dir:"under", cls:"under", glyph:"↓", word:`${delta} under`};
  return {dir:"over", cls, glyph: cls==="critical"?"✕":"!", word:`${-delta} over`};
}
```

- [ ] **Step 3: Add `creditSentence`**

```js
/* The credit's own words from data/plan-credits.yaml, with the quantity folded in. Falls back
   to the label so a credit added later without copy still reads. */
function creditSentence(def, n){
  const raw=def.sentence||("Because of "+def.label.toLowerCase());
  return raw.replace(/\{n\}/g,String(n)).replace(/\{s\}/g, n===1?"":"s");
}
```

- [ ] **Step 4: Style the narrative ledger**

Beside the existing `.ledger` rules:

```css
.vledger{font-family:var(--data);font-size:12px;margin-top:var(--s3);max-width:560px}
.vledger .r{display:flex;align-items:baseline;gap:var(--s2)}
.vledger .lbl{color:var(--pencil)}
.vledger .dots{flex:1;border-bottom:1px dotted var(--edge);transform:translateY(-3px);min-width:12px}
.vledger .v{color:var(--key);font-variant-numeric:tabular-nums;white-space:nowrap}
.vledger .sub{font-family:var(--text);font-size:11px;color:var(--ghost);line-height:1.45;
  margin:1px 0 7px 0;max-width:52ch}
.vledger .rule{border-top:1px solid var(--edge);margin:6px 0 5px}
.vledger .tot .lbl,.vledger .tot .v{color:var(--key);font-weight:700}
.vledger .cap{font-family:var(--display);font-size:15px;letter-spacing:.04em;text-transform:uppercase}
.vhead{margin:var(--s4) 0 2px;display:block}
.notprintable{border:1px solid var(--critical);border-radius:var(--radius-btn);
  padding:9px 11px;margin-top:var(--s2);font-size:12px;color:var(--key)}
.decision{font-size:12.5px;color:var(--pencil);margin-top:var(--s3);max-width:56ch;line-height:1.55}
.decision b{color:var(--key)}
```

- [ ] **Step 5: Build `verdictPanel`**

Insert before `proofPanel`. Two forms, chosen on `p.hasPlan`, exactly as spec §4.1 and §4.2:

```js
/* One ledger, read top to bottom as sentences: what the card is allowed to spend, then what it
   actually spends. It replaces two separate verdicts that used to sit 500px apart in different
   visual languages -- proofPanel answered "on budget?" against the base budget while The Score
   answered "does it fit?" against the Ceiling, and for a card with a plan those are different
   questions with different answers and nothing said which one was the real one. */
function verdictPanel(s){
  const m=draft.meta, plan=planOf(), p=scorePlan(s,plan), cfg=DB.plan;
  const row=(label,value,cls="")=>el("div",{class:"r "+cls},
    el("span",{class:"lbl",text:label}), el("span",{class:"dots"}),
    el("span",{class:"v",text:value===null?"":String(value)}));
  const note=t=>el("div",{class:"sub",text:t});
  const rule=()=>el("div",{class:"rule"});
  const led=el("div",{class:"vledger"});
  const isAsc=(m.subtype||"").toLowerCase()==="ascendant";

  /* ---- potential ---- */
  led.append(row(`Because it costs ${m.cost} Energy`, m.cost*DB.constants.costMultiplier),
             note(`Every point of Energy buys ${DB.constants.costMultiplier} points of power.`),
             row("Because every card gets a base allowance", "+"+DB.constants.baseAllowance));
  if(isAsc) led.append(row("Because it's an Ascendant — it has two faces","+"+DB.constants.ascendantBonus));
  led.append(rule());

  if(!p.hasPlan){
    led.append(row("BASE BUDGET — what the base side may spend", s.budget, "tot"),
               row(`Both faces together may spend ${DB.constants.ascendedMultiplier}× that`,
                   s.ascendedBudget));
  } else {
    led.append(row("BASE BUDGET", s.budget, "tot"));
    const table=Object.fromEntries(cfg.credits.map(c=>[c.key,c]));
    for(const [k,q] of Object.entries(plan.pays||{})){
      const def=table[k]; if(!def||!q) continue;
      let raw=def.points*q;
      if(k==="narrowness") raw=Math.min(raw,cfg.narrowness_cap);
      const f=costFactor(k,plan), earned=Math.trunc(raw*f);
      led.append(row(creditSentence(def,q), "+"+earned));
      led.append(note(f===1
        ? `${def.points} each — ${def.anchor||"see the balance philosophy"}.`
        : `${q} × ${def.points} = ${raw}, then ×${f} — ${def.anchor||""}`.trim()));
    }
    led.append(rule(),
      row("ALLOWANCE — budget plus what it pays in other currencies", p.allowance, "tot"));
    if(p.cap===null){
      led.append(el("div",{class:"notprintable"},
        el("b",{text:"Reach 0 — not printable. "}),
        "No faction can answer this card with the windows you have declared. "
        +"Declare a window a faction is strong in, or this cannot be printed."));
    } else if(p.reach!==null){
      const mult=(cfg.reach_caps||{})[p.reach];
      led.append(row(`But only ${p.reach} faction${p.reach===1?"":"s"} can answer it, `
                     +`so it's capped at ${mult}× base`, p.cap));
      const can=p.answering, cant=Object.keys(DB.factions||{}).filter(n=>!can.includes(n));
      led.append(note(
        (can.length?`${can.join(" and ")} can. `:"No faction can. ")
        +(cant.length?`${cant.join(" and ")} ${cant.length===1?"is":"are"} blind.`:"")
        +(p.reachOverridden?`  You have overridden this — computed Reach is ${p.reachComputed}.`:"")));
    }
    led.append(rule(), row("CEILING — the most this card may spend", p.ceiling, "tot"));
  }

  /* ---- actual ---- */
  const act=el("div",{class:"vledger"});
  const names=(a)=>a&&a.length?a.join(", "):"none";
  act.append(
    row(`Its stats — ${DB.statKeys.map(k=>`${k} ${m.stats?.[k]??"–"}`).join(" · ")}`, s.statsTotal),
    row(`Its base keywords — ${names(m.base?.keywords)}`, "+"+s.baseKeywordPoints),
    row(`Its base effects — ${names(m.base?.effects)}`, "+"+s.baseEffectPoints),
    rule(), row("BASE SIDE SPENDS", s.baseSpent, "tot"),
    row(`Its level-up keywords — ${names(m.ascended?.keywords)}`, "+"+s.ascendedKeywordPoints),
    row(`Its level-up effects — ${names(m.ascended?.effects)}`, "+"+s.ascendedEffectPoints),
    rule(), row("BOTH FACES SPEND", s.baseSpent+s.ascendedSpent, "tot"));

  /* ---- bars and the decision ---- */
  const bars=el("div",{});
  let head;
  if(p.hasPlan){
    head=verdictOf(p.headroom,false);
    bars.append(meterV("Both faces against the Ceiling", p.total, p.ceiling, head));
  } else {
    head=verdictOf(s.baseDelta,true);
    bars.append(meterV("Base side against its budget", s.baseSpent, s.budget, head),
      meterV(`Both faces against ${DB.constants.ascendedMultiplier}× budget`,
             s.baseSpent+s.ascendedSpent, s.ascendedBudget,
             verdictOf(s.ascendedDelta,false)));
  }

  return el("div",{},
    el("span",{class:"herolabel vhead",text:"Potential power — what this card is allowed to spend"}),
    led,
    el("span",{class:"herolabel vhead",text:"Actual impact — what it really spends"}),
    act, bars, decisionLine(s,p,head));
}
```

- [ ] **Step 6: Add `meterV` and `decisionLine`**

`meterV` is the existing `meter()` taking a verdict object instead of a bare severity string, so the glyph and word travel with the colour:

```js
/* meter(), but carrying the verdict so the glyph and the word travel with the colour. */
function meterV(label, spent, budget, v){
  const max=Math.max(spent,budget,1), pct=x=>Math.min(100,(x/max)*100);
  return el("div",{class:"meter"},
    el("div",{class:"cap"},
      el("span",{}, label),
      el("span",{class:`${v.cls}-c`,style:"font-weight:600"},
        el("span",{class:`glyph ${v.cls}-bg`,text:v.glyph}), " ",
        el("b",{text:String(spent)}), " / ", el("b",{text:String(budget)}), " · ", v.word)),
    el("div",{class:"track"},
      el("div",{class:"fill",style:`width:${pct(spent)}%;background:var(--${v.cls})`}),
      el("div",{class:"budgetmark",style:`left:calc(${pct(budget)}% - 1px)`,title:`limit ${budget}`})));
}

/* What to actually do about it. The old panel stated the verdict and stopped, which is fine if
   you already know what raises a ceiling and what spends one. */
function decisionLine(s,p,v){
  const step=DB.constants.costMultiplier;
  if(v.dir==="on")
    return el("div",{class:"decision"}, el("b",{text:"Exactly on budget. "}),
      "It spends precisely what its cost buys.");
  if(v.dir==="under")
    return el("div",{class:"decision"}, el("b",{text:`${s.baseDelta} under. `}),
      "This is weaker than its cost pays for — underpowered is as wrong as overpowered here, "
      +`it just fails quietly. Add ${s.baseDelta} points of impact, or drop the cost by 1, `
      +`which removes ${step} points of budget.`);
  const over = p.hasPlan ? -p.headroom : -s.baseDelta;
  const blind = p.hasPlan ? Object.keys(DB.factions||{}).filter(n=>!p.answering.includes(n)) : [];
  return el("div",{class:"decision"}, el("b",{text:`${over} over. `}),
    `Cut ${over} points of impact, or buy more ceiling: +1 Energy buys ${step} points`,
    p.hasPlan ? ", and giving a blind faction a window it can actually use raises the cap." : ".",
    blind.length ? ` Right now ${blind.join(" and ")} ${blind.length===1?"has":"have"} no answer at all.` : "");
}
```

- [ ] **Step 7: Wire it into `proofPanel` and delete the old arithmetic**

In `proofPanel(s)`, replace the whole `if(s.scorable){ ... }` branch body with `right.append(verdictPanel(s));`. Keep the `else` stub branch exactly as it is. Keep `syncProof()`, the `PROOF` node and `faceText()` untouched — the card face, the flip and the card text are not changing.

- [ ] **Step 8: Delete the duplicate bar from `scorePanel`**

Remove the `const bar=el("div",{class:"scorebar"}, ...)` construction and the `bar,` entry from `scorePanel`'s returned children. The panel keeps its credit grid, Reach row, windows and prohibitions — those are controls, and they move in Task 8. Everything the bar said now lives in the verdict panel.

- [ ] **Step 9: Verify in the browser**

- **Moammar, The One Punch Machine Gun** (cost 5, Ascendant, 6/6/0/3, *Searching (Tutors)*, *Permanent Buff 5*, no declared plan): potential reads 15 / +1 / +3 / BASE BUDGET 19 / both faces 28. Actual reads stats 15 / keywords +0 / effects +4 / BASE SIDE SPENDS 19 / level-up +0 / +5 / BOTH FACES SPEND 24. Verdict: on budget, `✓`, neutral ink.
- A card with a declared plan renders the §4.2 single-ledger form with credits, the Reach cap line and the faction sentence.
- Force `--under`: drop a stat by 3 on a no-plan card and confirm the bar turns steel-teal with `↓` and the decision line offers the two moves. Confirm no interactive control turned teal.
- Force over: raise a stat by 5 and confirm the hot ramp and the "cut N points" line.
- Toggle the theme and confirm both tokens read correctly in light mode.
- Console: no errors. `parityCheck()` still returns `[]`.

- [ ] **Step 10: Commit**

```bash
git add tools/studio.html
git commit -m "One verdict, read as sentences

The page stated its verdict twice, in two systems, 500px apart: proofPanel
answered 'on budget?' against the base budget while The Score answered 'does
it fit?' against the Ceiling. For a card with a plan those disagree and
nothing said which was real. Now it is one ledger -- what the card is allowed
to spend, what it actually spends, and what to do about the difference."
```

---

### Task 7: The teaching layer on the plan controls

Spec §7.1, §7.2, §7.3, §7.4.

**Files:**
- Modify: `tools/studio.html` `scorePanel` — the credit grid, the tests, the Reach row
- Modify: `tools/studio.html` `gateStrip` — fix lines
- Modify: `tools/studio.html` CSS — `.testq`, `.testopt`, `.reachtable`, `.gatefix`

**Interfaces:**
- Consumes: `cost_test_copy` and `sentence` from Task 5; `p.answering` / `p.reachComputed` from Task 4.

- [ ] **Step 1: Print each credit's anchor**

In the credit grid, the label currently hides its justification in a `title=`:

```js
      el("div",{class:"lb",text:c.label,title:c.anchor||""}),
```

Replace with a visible two-line block:

```js
      el("div",{class:"lb",text:c.label}),
      c.anchor?el("div",{class:"anchor",text:`Worth ${c.points} because ${c.anchor}.`}):null,
```

CSS beside the other credit rules:

```css
.credit .anchor{font-size:11px;color:var(--ghost);line-height:1.4;margin:2px 0 5px;max-width:44ch}
```

- [ ] **Step 2: Replace the three bare dropdowns with named questions**

Replace the `q?el("div",{class:"tests"}, ...)` block. Read the multiplier from `cfg.cost_tests` and the wording from `cfg.cost_test_copy`; never duplicate a number:

```js
      q?el("div",{class:"tests"}, ...Object.entries(cfg.cost_tests||{}).map(([test,opts])=>{
        const copy=(cfg.cost_test_copy||{})[test]||{};
        const chosen=((plan.tests||{})[c.key]||{})[test];
        const pick=v=>{ plan.tests=plan.tests||{}; plan.tests[c.key]=plan.tests[c.key]||{};
          if(v) plan.tests[c.key][test]=v; else delete plan.tests[c.key][test]; touch(); };
        return el("div",{class:"testblock"},
          el("div",{class:"testq",text:copy.question||test}),
          copy.why?el("div",{class:"testwhy",text:copy.why}):null,
          el("div",{class:"testopts"}, ...Object.keys(opts).map(o=>{
            const oc=((copy.options||{})[o])||{};
            return el("button",{class:"testopt","aria-pressed":chosen===o,
              "data-focus":`test:${c.key}:${test}:${o}`,
              onclick:()=>pick(chosen===o?null:o)},
              el("b",{text:oc.label||o}),
              el("span",{class:"note",text:oc.note||""}),
              el("span",{class:"mult",text:"×"+Number(opts[o]).toFixed(1)}));
          })));
      })):null),
```

CSS:

```css
.testblock{margin-top:9px;padding-top:8px;border-top:1px solid var(--rule)}
.testq{font-size:12px;color:var(--key);font-weight:600}
.testwhy{font-size:11px;color:var(--ghost);margin-top:2px;max-width:52ch;line-height:1.45}
.testopts{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px}
.testopt{display:flex;flex-direction:column;align-items:flex-start;gap:1px;cursor:pointer;
  background:var(--well);border:1px solid var(--rule);border-radius:var(--radius-btn);
  padding:6px 9px;font-size:11.5px;text-align:left;max-width:210px}
.testopt:hover{border-color:var(--edge)}
.testopt[aria-pressed="true"]{border-color:var(--color-cyan);background:var(--color-cyan-tint);
  color:var(--color-cyan)}
.testopt .note{color:var(--ghost);font-size:10.5px;line-height:1.35}
.testopt .mult{font-family:var(--data);font-size:10.5px;color:var(--pencil)}
```

- [ ] **Step 3: Show the live arithmetic under each priced credit**

Immediately after the tests block, inside the same `.credit` div:

```js
      q?(()=>{ let raw=c.points*q;
        if(c.key==="narrowness") raw=Math.min(raw,cfg.narrowness_cap);
        const f=costFactor(c.key,plan);
        return el("div",{class:"creditmath",
          text: f===1 ? `${q} × ${c.points} = ${raw} points earned`
                      : `${q} × ${c.points} = ${raw}  →  ×${f}  →  ${Math.trunc(raw*f)} points earned`});
      })():null),
```

```css
.credit .creditmath{font-family:var(--data);font-size:11px;color:var(--pencil);margin-top:7px}
```

- [ ] **Step 4: Replace the Reach chip row with the derived readout**

Keep the 0–4 chips, relabel them as an override, and put the computed answer above them:

```js
  const p2=scorePlan(s,plan);
  const reachBox=el("div",{});
  if(p2.declaredWindows.length){
    const tbl=el("div",{class:"reachtable"});
    for(const n of Object.keys(DB.factions||{})){
      const prof=(DB.factions[n]||{}).windows||{};
      const hit=p2.declaredWindows.find(w=>prof[w]==="strong");
      const wl=(cfg.windows.find(w=>w.key===hit)||{}).label;
      tbl.append(el("div",{class:"rrow"},
        factionChip(n),
        el("span",{class:hit?"good-c":"muted",text:hit?"✓":"✗"}),
        el("span",{class:"muted",text:hit?`strong at ${wl}`:"blind at every window you declared"})));
    }
    tbl.append(el("div",{class:"rsum",
      text:`→ computed Reach ${p2.reachComputed} → cap ${(cfg.reach_caps||{})[p2.reachComputed]}× base = ${p2.cap===null?"not printable":p2.cap}`}));
    reachBox.append(tbl);
  } else {
    reachBox.append(el("div",{class:"muted",style:"font-size:11.5px",
      text:"Declare a window below and this fills in — Reach is computed from which factions are strong in the windows you offer."}));
  }
```

Then the existing chip row, with its label changed from `Factions that can answer this card:` to `Override the computed Reach:` and a muted note reading `Only if you know something the window profiles in data/factions.yaml do not.` Add `"data-focus":"reach:"+n` per Task 2, and a chip that clears the override (`plan.reach=null`).

```css
.reachtable{border:1px solid var(--rule);border-radius:var(--radius-btn);padding:8px 10px;margin:4px 0 8px;
  font-size:11.5px;max-width:520px}
.reachtable .rrow{display:flex;align-items:center;gap:9px;padding:3px 0}
.reachtable .rsum{font-family:var(--data);color:var(--key);border-top:1px solid var(--rule);
  margin-top:6px;padding-top:6px}
```

- [ ] **Step 5: Give every gate failure a fix**

In `gateStrip`, beside each failure message, append a fix line. Map by gate id:

```js
/* A complaint without a move is just a complaint. G2/G5/G7/G9 are human gates and carry their
   own description already. */
const GATE_FIX={
  G1:"Cut impact, raise the cost, or declare a plan that earns a higher ceiling.",
  G3:"Add the type in parentheses after the ability name — (Standard Ability), (Fast Ability), (Trigger Ability) or (Passive Ability).",
  G4:"Keywords never cross factions. Swap it for one of this faction's own, or move the card.",
  G6:"Say how long it lasts — 'until the end of the round', 'permanently', 'this turn'.",
  G8:"Set the missing piece: a faction, a base art reference, or an explicit `crew: null` with a reason in Design Notes.",
};
```

and in the failure loop append `el("div",{class:"gatefix",text:GATE_FIX[id]||""})`.

```css
.gatefix{font-size:11.5px;color:var(--color-cyan);margin-top:2px}
```

- [ ] **Step 6: Verify in the browser**

- Every credit shows `Worth N because …` as visible text.
- Set a credit to 1 → the three questions appear with named options and multipliers; picking `It IS the plan` shows `1 × 5 = 5 → ×0 → 0 points earned` and the verdict panel's Allowance does not move.
- A card with windows declared shows the four-faction readout with the window that earns each ✓, and the computed Reach line matches the verdict panel.
- Break G4 (put a foreign keyword on a card) → the fix line appears. Undo.
- Console clean; `parityCheck()` returns `[]`.

- [ ] **Step 7: Confirm the baseline**

Run: `.venv/Scripts/python.exe tools/check.py` — expected: unchanged baseline.

- [ ] **Step 8: Commit**

```bash
git add tools/studio.html
git commit -m "Explain the controls that move the numbers

The credit anchors were in title= attributes nobody would find, and the three
tests -- one of which multiplies a credit by zero -- rendered as dropdowns
labelled 'bite', 'timing' and 'enabler'. Reach was a number to guess at;
it is now derived from the window profiles and shows its working."
```

---

### Task 8: Regroup the card page into two stacks

Spec §6. Pure reorganisation — no new behaviour. Last, so it moves finished panels.

**Files:**
- Modify: `tools/studio.html:2424-2495` (`renderMainNow`)
- Modify: `tools/studio.html` `scorePanel` and the `Cost & stats` panel — split their contents

**Interfaces:**
- Consumes: everything built in Tasks 6 and 7.

- [ ] **Step 1: Split `Cost & stats`**

The Cost stepper is the only control that raises the ceiling; the four stats are the largest single line of spend. Delete the combined panel and put `stepper("Cost", ...)` at the top of the ceiling panel and the four stat steppers at the top of the spend panel. The stats grid drops from `repeat(5,1fr)` to `repeat(4,1fr)`; add a `.stats4` class rather than changing `.stats`.

- [ ] **Step 2: Reorder `renderMainNow`**

The card head and `proofPanel(s)` stay first. Then, replacing today's sequence:

```js
  main.append(proofPanel(s));

  /* Blocks 2 and 3 are the two halves of the verdict above, in the same order: everything that
     raises the ceiling, then everything that spends it. Whichever half of the verdict is wrong
     tells you which panel to scroll to. */
  if(s.scorable) main.append(scorePanel(s));   /* now titled "What raises the ceiling" */
  main.append(spendPanel());                   /* "What spends it" */
  main.append(gateStrip());                    /* "Can it be printed" */
  main.append(jobPanel(draft));
  main.append(siblingTable());
```

- [ ] **Step 3: Build `spendPanel`**

Merges today's two mechanics panels and the stat steppers into one:

```js
/* Everything that spends the ceiling, in the order the verdict lists it: stats, then the base
   side, then the level-up side. These were three separate panels with the stat steppers in a
   fourth, above two read-only panels. */
function spendPanel(){
  const m=draft.meta;
  return el("div",{class:"panel"},
    el("h3",{text:"What spends it"}),
    el("label",{class:"fl",text:"Stats — the largest single line of spend"}),
    el("div",{class:"grid stats4",style:"margin-top:var(--s3)"},
      ...DB.statKeys.map(k=>stepper(k, m.stats?.[k],
        v=>{m.stats=m.stats||{}; m.stats[k]=v; touch();}))),
    el("div",{class:"side-rule",text:"Base side"}),
    el("label",{class:"fl"},"Keywords — ",m.faction||"?"," only (",term("G4"),")"), keywordChips("base"),
    el("label",{class:"fl",text:"Effect types"}), effectPicker("base"),
    el("div",{class:"side-rule lvl",text:"Level-up"}),
    el("label",{class:"fl",text:"Keywords gained"}), keywordChips("ascended"),
    el("label",{class:"fl",text:"Effect types"}), effectPicker("ascended"));
}
```

```css
.stats4{grid-template-columns:repeat(4,1fr);max-width:480px}
```

- [ ] **Step 4: Retitle the panels**

- `scorePanel`'s `h3` → `What raises the ceiling`, with the muted subtitle kept.
- `gateStrip`'s `h3` → `Can it be printed`, subtitle kept.
- Delete the old `Base side — priced mechanics` and `Level-up side — priced mechanics` panels from `renderMainNow`; their contents now live in `spendPanel`.

- [ ] **Step 5: Verify in the browser**

Walk a full card top to bottom: card + verdict → What raises the ceiling (cost, pays, tests, Reach, windows, prohibitions) → What spends it (stats, base, level-up) → Can it be printed → Job → cost neighbours → playtests. Confirm every control still edits and the verdict panel still updates live. Confirm no control appears twice and none has gone missing — in particular the Cost stepper, all four stat steppers, both keyword chip sets and both effect pickers.

Confirm the Task 2 fix still holds after the move: tick a window, tick an effect, click a stat stepper — scroll must not jump.

Console clean; `parityCheck()` returns `[]`.

- [ ] **Step 6: Full verification**

```bash
.venv/Scripts/python.exe tools/check.py
.venv/Scripts/python.exe -m pytest tools/tests -q
.venv/Scripts/python.exe tools/generate.py --check
```

Expected: `34 blocking, 77 warnings` unchanged; 13 tests pass; generate clean.

Then edit a card in the studio, save it, and run `git diff` on the card file — confirm the diff contains only the field that was changed, and that `card_io` round-tripping is intact.

- [ ] **Step 7: Commit**

```bash
git add tools/studio.html
git commit -m "Regroup the card page into the two halves of the verdict

Everything that raises the ceiling, then everything that spends it, in the
same order the verdict states them -- so the half of the verdict that is
wrong tells you which panel to scroll to. The cost stepper and the stat
steppers separate for the same reason: cost is the only control that raises
a ceiling and the stats are the biggest thing that spends one."
```

---

## Final acceptance

All of these must hold at the end:

1. `python tools/check.py` runs with no `PYTHONIOENCODING` and prints exactly `34 blocking, 77 warnings   (F2×7, F4×19, F6×8, GAP×10, W1×2, W10×2, W15×1, W2×2, W3×6, W4×12, W6×13, W8×4, W9×25)`.
2. `python -m pytest tools/tests -q` → 13 passed.
3. `python tools/generate.py --check` → clean.
4. `parityCheck()` in the browser console → `[]`, and no drift toast on boot.
5. Ticking a window, setting Reach, changing a cost test, clicking a credit ±, clicking a keyword chip, ticking an effect → `#main` scrollTop unchanged and focus retained.
6. Effect filter query survives a tick. Human gate ticks survive a re-render and are per-card.
7. The verdict panel renders both forms (§4.1 no-plan and §4.2 plan-declared) with figures matching `check.py`.
8. `--under` appears on under-budget meters and on no interactive control, in both themes.
9. No card file changed except through a deliberate studio edit.
