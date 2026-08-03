#!/usr/bin/env python3
"""Read and write card markdown files.

A card file is YAML frontmatter (the machine-readable contract) followed by a fixed
sequence of markdown sections (the human-readable card). This module is the only place
that knows that layout -- every other tool goes through it, so the format lives in one file.

Round-trip guarantee: load(path) -> save(card) reproduces an equivalent file. The
`## Design Notes` section is preserved verbatim because it is an append-only history.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = REPO_ROOT / "cards"
ART_DIR = REPO_ROOT / "art"

IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp", ".gif")

STAT_KEYS = ("PA", "PH", "MA", "MH")

LORE_PACKET_FIELDS = (
    "Premise (one line)",
    "The True Detail",
    "The Myth",
    "Why This Faction",
    "Why This Crew",
    "The Fall (printed weakness)",
    "The Ascension (what the level-up MEANS)",
)

_UNWRITTEN = {"", "_TBD_", "_Not written._", "TBD"}

_LORE_COMMENT = ("<!-- Fill using docs/rubrics/lore-rubric.md "
                 "— the Lore Packet is required for every card. -->")
_NOTES_COMMENT = ("<!-- Rubric scores, balance decisions, playtest results. "
                  "Append, don't overwrite. -->")


class CardFormatError(Exception):
    """A card file could not be parsed."""


@dataclass
class Card:
    path: Path
    meta: dict
    rules_text: str = ""
    levelup_condition: str = ""
    ascended_text: str = ""
    lore: dict = field(default_factory=dict)
    design_notes: str = ""

    # -- convenience accessors used by the scorer and the UI ------------------
    @property
    def name(self) -> str:
        return self.meta.get("name") or self.path.stem

    @property
    def faction(self) -> str | None:
        return self.meta.get("faction")

    @property
    def is_ascendant(self) -> bool:
        return (self.meta.get("subtype") or "").lower() == "ascendant"

    @property
    def stats(self) -> dict:
        return self.meta.get("stats") or {}

    @property
    def has_full_stats(self) -> bool:
        return all(self.stats.get(k) is not None for k in STAT_KEYS)

    @property
    def rel_path(self) -> str:
        return self.path.relative_to(REPO_ROOT).as_posix()

    def side(self, which: str) -> dict:
        block = self.meta.get(which) or {}
        return {"keywords": block.get("keywords") or [], "effects": block.get("effects") or []}


def _section(body: str, heading: str) -> str:
    """Text under `heading` up to the next heading of the same or higher level."""
    level = len(heading) - len(heading.lstrip("#"))
    pattern = rf"^{re.escape(heading)}\s*$\n(.*?)(?=^#{{1,{level}}} |\Z)"
    match = re.search(pattern, body, flags=re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


_KEYWORD_LINE = re.compile(r"^Keywords(?: gained)?:.*$\n?", flags=re.MULTILINE)


def _clean(text: str) -> str:
    """Strip the generated `Keywords:` lines -- they are rendered from frontmatter, so
    leaving them in the prose would duplicate them on every save."""
    text = _KEYWORD_LINE.sub("", text).strip()
    return "" if text in _UNWRITTEN else text


def _parse_lore(body: str) -> dict:
    section = _section(body, "## Lore")
    lore = {}
    for label in LORE_PACKET_FIELDS:
        match = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.*?)$", section, flags=re.MULTILINE)
        lore[label] = _clean(match.group(1)) if match else ""
    return lore


def load(path: Path) -> Card:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise CardFormatError(f"{path}: no YAML frontmatter")
    _, frontmatter, body = text.split("---", 2)
    meta = yaml.safe_load(frontmatter) or {}

    return Card(
        path=path,
        meta=meta,
        rules_text=_clean(_section(body, "### Rules Text")),
        levelup_condition=_clean(_section(body, "### Condition")),
        ascended_text=_clean(_section(body, "### Ascended Rules Text")),
        lore=_parse_lore(body),
        design_notes=_section(body, "## Design Notes").replace(_NOTES_COMMENT, "").strip(),
    )


def render(card: Card) -> str:
    meta, stats = card.meta, card.stats
    lines = [
        "---",
        yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000).rstrip(),
        "---",
        "",
        f"# {card.name}",
        "",
    ]

    subtitle = f"**{card.faction or 'UNASSIGNED FACTION'}**"
    if meta.get("crew"):
        subtitle += f" · {meta['crew']}"
    subtitle += f" · {meta.get('subtype') or 'Card'}"
    lines += [subtitle, "", "## Base Side", ""]

    if meta.get("cost") is not None and card.has_full_stats:
        stat_line = " / ".join(f"{k} {stats[k]}" for k in STAT_KEYS)
        lines += [f"`Cost {meta['cost']}` — **{stat_line}**", ""]
    else:
        lines += ["> **STUB.** No cost, stats, or rules text defined yet.", ""]

    base = card.side("base")
    if base["keywords"]:
        lines += [f"Keywords: {', '.join(base['keywords'])}", ""]

    lines += ["### Rules Text", "", card.rules_text or "_Not written._", "",
              "## Level-Up", "",
              "### Condition", "", card.levelup_condition or "_Not written._", ""]

    ascended = card.side("ascended")
    if ascended["keywords"]:
        lines += [f"Keywords gained: {', '.join(ascended['keywords'])}", ""]

    lines += ["### Ascended Rules Text", "", card.ascended_text or "_Not written._", "",
              "## Lore", "", _LORE_COMMENT, ""]
    for label in LORE_PACKET_FIELDS:
        lines += [f"**{label}:** {card.lore.get(label) or '_TBD_'}", ""]

    lines += ["## Design Notes", "", _NOTES_COMMENT, ""]
    if card.design_notes:
        lines += [card.design_notes, ""]

    return "\n".join(lines).rstrip() + "\n"


def save(card: Card) -> None:
    card.path.write_text(render(card), encoding="utf-8")


def load_all(root: Path | None = None) -> list[Card]:
    cards = []
    for path in sorted((root or CARDS_DIR).rglob("*.md")):
        if path.name.upper().startswith("README"):
            continue
        cards.append(load(path))
    return cards


def _art_key(text: str) -> str:
    """Card frontmatter stores art references with punctuation and spaces stripped
    (`AlvinoTheLastCallv2`), while the files on disk keep them
    (`Alvino, The Last Call v2.jpg`). Normalising both ends matches them."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


@lru_cache(maxsize=1)
def art_index() -> dict[str, str]:
    """normalised filename -> repo-relative path.

    Where the same name exists both as a character portrait and as a finished card
    render, the portrait wins -- it is the reference a designer wants on screen.
    """
    index: dict[str, list[Path]] = {}
    if ART_DIR.is_dir():
        for path in ART_DIR.rglob("*"):
            if path.suffix.lower() in IMAGE_SUFFIXES:
                index.setdefault(_art_key(path.stem), []).append(path)
    return {
        key: sorted(paths, key=lambda p: (0 if "characters" in p.parts else 1,
                                          p.as_posix()))[0]
             .relative_to(REPO_ROOT).as_posix()
        for key, paths in index.items()
    }


def resolve_art(reference: str | None) -> str | None:
    """Repo-relative path for an art reference, or None if nothing matches."""
    if not reference:
        return None
    return art_index().get(_art_key(reference))


def load_table(filename: str, key: str) -> list[dict]:
    payload = yaml.safe_load((REPO_ROOT / "data" / filename).read_text(encoding="utf-8"))
    return payload[key]
