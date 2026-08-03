# TCG — Working Repository

A 1-on-1 trading card game where the cards are my friends.

Four **factions** are methodologies — how you win. Six **crews** are loyalties — who you run
with. They're independent axes: one crew spans several factions. Two things have to be
excellent, and each has a rubric: the **gameplay** and the **lore**.

## Start here

| If you want to | Read |
|---|---|
| Know how the game works | [`docs/rulebook/`](docs/rulebook/README.md) |
| Design or judge a card's **gameplay** | [`docs/rubrics/gameplay-rubric.md`](docs/rubrics/gameplay-rubric.md) |
| Design or judge a card's **lore** | [`docs/rubrics/lore-rubric.md`](docs/rubrics/lore-rubric.md) |
| Know what's broken | [`docs/design/open-questions.md`](docs/design/open-questions.md) |
| Know what the world is | [`docs/design/canon.md`](docs/design/canon.md) |
| Work on this with an AI | [`AGENTS.md`](AGENTS.md) |

## Layout

```
docs/rulebook/     the rules, one section per file
docs/rubrics/      the two rubrics
docs/design/       open questions · decisions · canon
data/              keywords · effects · status effects — the point economy
cards/             one markdown file per card
tools/             balance.py · validate.py
art/               character and UI artwork
legacy/            original xlsx + docx, reference only
```

## The design workbench

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows.  macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python tools/studio.py
```

A browser opens on `127.0.0.1:8765` (loopback only — nothing on your network can reach it).
Pick a card, push the stat and cost steppers, and the budget meters move as you type. Hitting
**Save** — or Ctrl-S — writes the card's `.md` file in place, so `git diff` shows exactly the
lines you changed and nothing else.

On screen while you design: the budget delta, the base and level-up meters, the live gate
results, the cost/stat steppers, every card within one cost of this one, and — in the right
rail — the faction's identity, its printed weakness, and this card's Lore Packet.

**Two meters, not one.** The base meter is the old spreadsheet number. The second charges the
level-up side against a ×1.5 ceiling, which the spreadsheet never did. A card can sit perfectly
on the base budget and still be a problem; see OQ-04.

## Command line

```bash
python tools/balance.py                    # score every card against its budget
python tools/balance.py --failing          # only the ones outside tolerance
python tools/balance.py --charge-ascended  # model charging the level-up side (see OQ-04)
python tools/validate.py                   # machine-checkable gates: G3, G4, G6, G8
```

`tools/card_io.py` reads and writes the card files; `tools/scoring.py` holds the budget
arithmetic and the gates. Everything else — the CLIs and the workbench — goes through them,
so the number in the browser is the number on the command line.

## Current state

| | |
|---|---|
| Cards designed | **31** — all Ascendants |
| Playable deck coverage | **~12%** of a legal 40-card pool (OQ-01) |
| Factions with playable cards | **3 of 4** — the Icons are stubs (OQ-06) |
| Win conditions with printed support | **1 of 3** (OQ-02, OQ-03) |
| Cards failing the budget gate | **9 of 25** — or 25 of 25 if the level-up side is charged (OQ-04) |
| Crews with a written identity | **0 of 6** (OQ-12) |

That table is the roadmap. See [`docs/design/open-questions.md`](docs/design/open-questions.md)
for the suggested order.
