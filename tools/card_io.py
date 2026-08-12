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
from functools import lru_cache, wraps
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = REPO_ROOT / "cards"
ART_DIR = REPO_ROOT / "art"

IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp", ".gif")

STAT_KEYS = ("PA", "PH", "MA", "MH")


# --- source-dependent caching -------------------------------------------------------------
#
# Every loader in tools/ reads a file and memoises the result. In a short-lived CLI run that
# is free. In a long-running process -- tools/studio.py -- it silently answers from a file
# that no longer exists on disk, and silence is the whole problem: the stale table still
# answers every question asked of it, confidently and wrongly.
#
# Keying each cache on its own sources' modification times fixes that once, for every
# consumer, so no caller anywhere has to remember to invalidate anything. Adding a new loader
# means adding a decorator that already does the right thing.

def source_stamp(*relative_paths: str) -> tuple:
    """A hashable fingerprint of the given repo-relative files or directories.

    Directories are walked. The stamp changes whenever a file's modification time or size
    changes, and whenever a file appears or disappears.
    """
    parts: list[tuple] = []
    for relative in relative_paths:
        target = REPO_ROOT / relative
        if target.is_dir():
            paths = sorted(p for p in target.rglob("*") if p.is_file())
        else:
            paths = [target]
        for path in paths:
            try:
                info = path.stat()
            except OSError:
                parts.append((str(path), -1, -1))      # absent is a state worth caching too
            else:
                parts.append((str(path), info.st_mtime_ns, info.st_size))
    return tuple(parts)


def cached_on(*relative_paths: str):
    """Memoise a zero-argument loader, reloading whenever its sources change on disk.

    The decorated loader keeps `.cache_clear()` and `.cache_info()` so existing callers still
    work. Those calls are now belt-and-braces rather than load-bearing, and they still earn
    their keep on write-then-read paths: a rewrite landing inside one filesystem clock tick at
    an identical byte length is the one change an mtime stamp cannot see.
    """
    def decorate(load):
        cached = lru_cache(maxsize=1)(lambda _stamp: load())

        @wraps(load)
        def fresh():
            return cached(source_stamp(*relative_paths))

        fresh.cache_clear = cached.cache_clear
        fresh.cache_info = cached.cache_info
        fresh.sources = relative_paths
        return fresh
    return decorate


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


class _CardDumper(yaml.SafeDumper):
    """Dumps multi-line strings as literal blocks so an ability's outcome table stays readable.

    PyYAML's default for a string containing newlines is folded single-quoted style, which
    renders a d6 table as quoted prose with blank lines between every row. Frontmatter is the
    machine's contract but a human still has to read it.
    """


def _literal_for_multiline(dumper, data):
    style = None
    if "\n" in data and not any(line != line.rstrip() for line in data.split("\n")):
        style = "|"          # trailing whitespace cannot survive a block scalar; fall back if any
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_CardDumper.add_representer(str, _literal_for_multiline)


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
        return {"keywords": block.get("keywords") or [], "effects": block.get("effects") or [],
                "abilities": block.get("abilities") or []}

    def face_text(self, which: str) -> str:
        """The printed rules text for a face.

        Generated from `abilities` when the side declares them, which is the migrated state and
        the one that makes G3 a field lookup. Falls back to the stored prose for any card not yet
        migrated, so both forms coexist and `render(load(p))` stays byte-identical either way.
        """
        abilities = self.side(which)["abilities"]
        if abilities:
            return print_abilities(abilities)
        return self.rules_text if which == "base" else self.ascended_text


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
        yaml.dump(meta, Dumper=_CardDumper, sort_keys=False, allow_unicode=True,
                  width=1000).rstrip(),
        "---",
        "",
        f"# {card.name}",
        "",
    ]

    subtitle = f"**{card.faction or 'UNASSIGNED FACTION'}**"
    if meta.get("crew"):
        subtitle += f" · {meta['crew']}"
    subtitle += f" · {meta.get('subtype') or 'Card'}"
    if meta.get("job"):
        subtitle += f" · *{meta['job']}*"
    lines += [subtitle, "", "## Base Side", ""]

    if meta.get("cost") is not None and card.has_full_stats:
        stat_line = " / ".join(f"{k} {stats[k]}" for k in STAT_KEYS)
        lines += [f"`Cost {meta['cost']}` — **{stat_line}**", ""]
    else:
        lines += ["> **STUB.** No cost, stats, or rules text defined yet.", ""]

    base = card.side("base")
    if base["keywords"]:
        lines += [f"Keywords: {', '.join(base['keywords'])}", ""]

    lines += ["### Rules Text", "", card.face_text("base") or "_Not written._", "",
              "## Level-Up", "",
              "### Condition", "", card.levelup_condition or "_Not written._", ""]

    ascended = card.side("ascended")
    if ascended["keywords"]:
        lines += [f"Keywords gained: {', '.join(ascended['keywords'])}", ""]

    lines += ["### Ascended Rules Text", "", card.face_text("ascended") or "_Not written._", "",
              "## Lore", "", _LORE_COMMENT, ""]
    for label in LORE_PACKET_FIELDS:
        lines += [f"**{label}:** {card.lore.get(label) or '_TBD_'}", ""]

    lines += ["## Design Notes", "", _NOTES_COMMENT, ""]
    if card.design_notes:
        lines += [card.design_notes, ""]

    return "\n".join(lines).rstrip() + "\n"


def save(card: Card) -> None:
    card.path.write_text(render(card), encoding="utf-8")


def slugify(text: str) -> str:
    return re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", text.lower())).strip("-")


SUBTYPE_DIR = {"Ascendant": "ascendants", "Descendant": "descendants",
               "Tactic": "tactics", "Attachment": "attachments", "Arena": "arenas"}


def new_card(name: str, faction: str, crew: str | None, subtype: str = "Descendant",
             cost: int | None = None) -> Card:
    """A blank card in the right folder, with every required field present.

    Always go through here rather than copying a file -- it guarantees the frontmatter
    schema and the section order the tools expect.
    """
    slug = slugify(name)
    folder = CARDS_DIR / SUBTYPE_DIR.get(subtype, "descendants") / (slugify(crew) if crew else "unassigned")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{slug}.md"
    if path.exists():
        raise FileExistsError(f"{path.relative_to(REPO_ROOT)} already exists")
    card = Card(
        path=path,
        meta={"name": name, "slug": slug, "card_type": "Character" if subtype in
              ("Ascendant", "Descendant") else subtype,
              "subtype": subtype, "faction": faction, "crew": crew, "job": None, "cost": cost,
              "stats": {k: None for k in STAT_KEYS},
              "base": {"keywords": [], "effects": []},
              "ascended": {"keywords": [], "effects": []},
              "plan": {"pays": {}, "windows": [], "requires": [], "produces": []},
              "art": {"base": None, "ascended": None},
              "status": "draft"},
        lore={f: "" for f in LORE_PACKET_FIELDS},
    )
    save(card)
    return card


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


@cached_on("art")
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


# --- abilities -----------------------------------------------------------------------------
#
# An ability is data, not a sentence. The printed rules text is GENERATED from these fields by
# print_ability(), which is why gate G3 can read a field instead of guessing at prose.
#
# The grammar, one rule:
#
#     [{name}] ({type}{ · keyword}): {immersion}
#     {requires}{joiner}{mechanics}
#
# `joiner` comes from the type (data/ability-types.yaml): a cost for Standard and Fast, a
# condition for Trigger and Passive. Flavour goes on the header line, rules go underneath --
# which is how 22 of the corpus's abilities were already written by hand, and is lore rubric
# D3 ("flavor explains rules") made visible in the layout.

ABILITY_FIELDS = ("name", "type", "immersion", "requires", "mechanics", "keyword")


@cached_on("data/ability-types.yaml")
def ability_types() -> list[dict]:
    return load_table("ability-types.yaml", "ability_types")


@cached_on("data/ability-types.yaml")
def ability_joiners() -> dict[str, str]:
    """Display name -> the string that joins `requires` to `mechanics`."""
    return {t["name"]: t.get("requires_joiner", ": ") for t in ability_types()}


def ability_type_names() -> tuple[str, ...]:
    return tuple(t["name"] for t in ability_types())


def print_ability(ability: dict) -> str:
    """One ability as it appears on the card. The inverse of the migration's parser."""
    name = (ability.get("name") or "").strip()
    kind = (ability.get("type") or "").strip()
    keyword = (ability.get("keyword") or "").strip()

    slot = f"{kind} · {keyword}" if kind and keyword else (kind or keyword)
    header = f"[{name}] ({slot}):" if slot else f"[{name}]:"

    immersion = (ability.get("immersion") or "").strip()
    mechanics = (ability.get("mechanics") or "").strip("\n")
    requires = (ability.get("requires") or "").strip()
    if requires:
        mechanics = f"{requires}{ability_joiners().get(kind, ': ')}{mechanics}"

    if immersion and mechanics:
        return f"{header} {immersion}\n{mechanics}"
    return f"{header} {immersion or mechanics}".rstrip()


def print_abilities(abilities: list[dict]) -> str:
    """A whole face. Abilities are separated by a blank line, as the corpus already writes them."""
    return "\n\n".join(print_ability(a) for a in abilities if a)
