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

## Tools

```bash
python tools/balance.py                    # score every card against its budget
python tools/balance.py --failing          # only the ones outside tolerance
python tools/balance.py --charge-ascended  # model charging the level-up side (see OQ-04)
python tools/validate.py                   # machine-checkable gates: G3, G4, G6, G8
```

Both are dependency-light — Python 3 and PyYAML.

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
