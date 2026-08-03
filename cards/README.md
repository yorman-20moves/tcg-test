# Cards

One markdown file per card: `cards/<subtype>/<crew>/<slug>.md`.

Frontmatter is parsed by `tools/`; names in `base.effects`, `base.keywords`, `ascended.effects`
and `ascended.keywords` must match `data/*.yaml` exactly. See [`../AGENTS.md`](../AGENTS.md) for
the full anatomy.

## Inventory

| Directory | Cards | Note |
|---|---:|---|
| `ascendants/` | 31 | Every card designed so far |
| `descendants/` | 0 | **The bulk of a real deck. Nothing here yet — OQ-01** |
| `tactics/` | 0 | Standard and Combat Tactics |
| `attachments/` | 0 | Including Mobb 134's Commandments |
| `arenas/` | 0 | No rules defined yet — OQ-07 |

A legal deck is 40+ cards with at most 5 Ascendants. The pool is currently ~12% of one deck,
and it's the 12% that's capped.

## Statuses

`draft` (stub, unscorable) → `ported` (data carried over, unreviewed) → `reviewed` (passed both
rubrics) → `playtested` → `final`.

All 31 existing cards are `ported` or `draft`. **None has been through either rubric yet.**
