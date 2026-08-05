#!/usr/bin/env python3
"""The consistency engine.

Every rule that keeps the three levels of the game agreeing with each other. One place, so
the CLI, the workbench and the generated docs all report the same thing.

Hard errors (F*) block. Warnings (W*) are read and judged. See docs/design/studio-plan.md.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache

import yaml

import card_io
import scoring

WINDOW_KEYS = ("pre_assembly", "during_assembly", "on_resolution", "post_resolution", "race")
WINDOW_LABELS = {
    "pre_assembly": "W1 Before it starts",
    "during_assembly": "W2 While it builds",
    "on_resolution": "W3 The moment it lands",
    "post_resolution": "W4 After it lands",
    "race": "W5 Race it",
}
MIN_FACTIONS_PER_WINDOW = 2
SCALING_PHRASES = ("equal to", "for each", "per ", "number of", "cumulative", "total number")
LORE_TRUE_DETAIL = "The True Detail"


@dataclass
class Finding:
    code: str
    severity: str          # "error" | "warning"
    subject: str           # what it's about (card name, faction, window)
    message: str
    where: str = ""        # file path when there is one
    fix: str = ""

    @property
    def blocking(self) -> bool:
        return self.severity == "error"

    def as_dict(self) -> dict:
        return {"code": self.code, "severity": self.severity, "subject": self.subject,
                "message": self.message, "where": self.where, "fix": self.fix}


@dataclass
class World:
    """Everything loaded once, so rules can cross-reference freely."""
    factions: list = field(default_factory=list)
    crews: list = field(default_factory=list)
    states: list = field(default_factory=list)
    cards: list = field(default_factory=list)
    keywords: list = field(default_factory=list)
    effects: list = field(default_factory=list)
    jobs: list = field(default_factory=list)
    formations: list = field(default_factory=list)

    def faction(self, name: str) -> dict | None:
        return next((f for f in self.factions if f["name"] == name), None)

    def crew(self, name: str) -> dict | None:
        return next((c for c in self.crews if c["name"] == name), None)

    def job(self, key: str) -> dict | None:
        return next((j for j in self.jobs if j["key"] == key), None)

    def formation(self, key: str) -> dict | None:
        return next((f for f in self.formations if f["key"] == key), None)

    def is_exempt(self, faction_name: str) -> bool:
        """Icons are outside the system by design. Coherence checks would report intent
        as a defect, so every Job/Formation/toolkit rule skips them."""
        faction = self.faction(faction_name or "")
        return bool(faction and faction.get("exempt"))


def _table(filename: str, key: str) -> list:
    path = card_io.REPO_ROOT / "data" / filename
    if not path.exists():
        return []
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get(key, []) or []


RETIRED = "retired"


@lru_cache(maxsize=1)
def load_world() -> World:
    return World(
        factions=_table("factions.yaml", "factions"),
        crews=_table("crews.yaml", "crews"),
        states=_table("game-states.yaml", "states"),
        cards=[c for c in card_io.load_all() if c.meta.get("status") != RETIRED],
        keywords=_table("keywords.yaml", "keywords"),
        effects=_table("effects.yaml", "effects"),
        jobs=_table("jobs.yaml", "jobs"),
        formations=_table("formations.yaml", "formations"),
    )


def card_tools(card) -> list[tuple[str, str, str]]:
    """(kind, name, side) for everything the card uses.

    `kind` matches the plural keys used in factions.yaml ("keywords"/"effects") so lookups
    against the unique/never tables key correctly.
    """
    out = []
    for side in ("base", "ascended"):
        block = card.side(side)
        out += [("keywords", n, side) for n in block["keywords"]]
        out += [("effects", n, side) for n in block["effects"]]
    return out


# ------------------------------------------------------------------ hard errors

def f1_unique_conflicts(world: World) -> list[Finding]:
    """The same tool marked unique to more than one faction."""
    owners: dict[tuple, list[str]] = {}
    for faction in world.factions:
        unique = faction.get("unique") or {}
        for kind in ("keywords", "effects"):
            for name in unique.get(kind) or []:
                owners.setdefault((kind, name), []).append(faction["name"])
    findings = []
    for (kind, name), holders in sorted(owners.items()):
        if len(holders) > 1:
            findings.append(Finding(
                "F1", "error", name,
                f"{kind[:-1]} '{name}' is marked unique to {len(holders)} factions: "
                f"{', '.join(holders)}. It can only be unique to one.",
                where="data/factions.yaml",
                fix=f"Remove '{name}' from the unique list of all but one faction."))
    return findings


def f10_keyword_ownership(world: World) -> list[Finding]:
    """A keyword carries its own `faction` field AND appears in a faction's unique list.
    Those two can disagree, and if they do the toolkit check silently reads the wrong one."""
    unique_owner = {}
    for faction in world.factions:
        for name in (faction.get("unique") or {}).get("keywords") or []:
            unique_owner[name] = faction["name"]
    findings = []
    for keyword in world.keywords:
        name, stated = keyword.get("name"), keyword.get("faction")
        owner = unique_owner.get(name)
        if owner and stated and owner != stated:
            findings.append(Finding(
                "F10", "error", name,
                f"is listed as a {stated} keyword in data/keywords.yaml but is marked unique to "
                f"the {owner} in data/factions.yaml.",
                where="data/keywords.yaml",
                fix=f"Pick one. The Library screen edits the keyword's faction; the Factions "
                    f"screen edits who owns it."))
        elif stated and not owner:
            findings.append(Finding(
                "F10", "error", name,
                f"is a {stated} keyword but no faction claims it as unique. Keywords are "
                f"faction-exclusive by rule.",
                where="data/factions.yaml",
                fix=f"Mark '{name}' unique to the {stated} on the Factions screen."))
    return findings


def f2_f3_toolkit_violations(world: World) -> list[Finding]:
    """Cards reaching for tools their faction doesn't own."""
    owner: dict[tuple, str] = {}
    for faction in world.factions:
        for kind in ("keywords", "effects"):
            for name in (faction.get("unique") or {}).get(kind) or []:
                owner.setdefault((kind, name), faction["name"])

    findings = []
    for card in world.cards:
        faction = world.faction(card.faction or "")
        if faction is None:
            continue
        never = set((faction.get("never") or {}).get("effects") or []) | \
                set((faction.get("never") or {}).get("keywords") or [])
        for kind, name, side in card_tools(card):
            holder = owner.get((kind, name))
            if holder and holder != card.faction:
                findings.append(Finding(
                    "F2", "error", card.name,
                    f"uses the {kind[:-1]} '{name}' on its {side} side, "
                    f"which is unique to the {holder}.",
                    where=card.rel_path,
                    fix=f"Either change the card's faction, drop '{name}', or stop reserving "
                        f"it for the {holder}."))
            elif name in never:
                findings.append(Finding(
                    "F3", "error", card.name,
                    f"uses '{name}' on its {side} side, which the {card.faction} never have.",
                    where=card.rel_path,
                    fix=f"Drop '{name}' or remove it from the {card.faction} never list."))
    return findings


def f4_over_ceiling(world: World) -> list[Finding]:
    findings = []
    for card in world.cards:
        if card.meta.get("status") == "draft":
            continue
        for message in scoring.gates(card).get("G1", []):
            findings.append(Finding("F4", "error", card.name, message.replace("G1: ", ""),
                                    where=card.rel_path))
    return findings


def f5_reach_overclaim(world: World) -> list[Finding]:
    """A card can't claim more Reach than its declared windows actually deliver."""
    findings = []
    for card in world.cards:
        plan = card.meta.get("plan") or {}
        claimed = plan.get("reach")
        if claimed is None:
            continue
        computed = computed_reach(world, card)
        if computed is None:
            continue
        if claimed > computed and not plan.get("reach_reason"):
            findings.append(Finding(
                "F5", "error", card.name,
                f"claims Reach {claimed} but its declared windows only give {computed} "
                f"({', '.join(answering_factions(world, card)) or 'no faction'}).",
                where=card.rel_path,
                fix="Add plan.reach_reason explaining the answer the window map doesn't model, "
                    "or lower the claim."))
    return findings


def f6_f7_card_gates(world: World) -> list[Finding]:
    findings = []
    for card in world.cards:
        if card.meta.get("status") == "draft":
            continue
        gates = scoring.gates(card)
        for code, gate in (("F6", "G3"), ("F7", "G6")):
            for message in gates.get(gate, []):
                findings.append(Finding(code, "error", card.name,
                                        re.sub(r"^G\d: ", "", message), where=card.rel_path))
    return findings


@lru_cache(maxsize=1)
def defined_terms() -> set[str]:
    """Every term the rulebook or the data files define."""
    terms = set()
    rulebook = card_io.REPO_ROOT / "docs" / "rulebook"
    if rulebook.is_dir():
        for path in rulebook.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            terms |= {m.lower() for m in re.findall(r"\*\*([A-Z][\w '/+-]{2,30})\*\*", text)}
            terms |= {m.lower() for m in re.findall(r"^\| \*\*([^*]+)\*\*", text, re.MULTILINE)}
    world = load_world()
    terms |= {k["name"].lower() for k in world.keywords}
    terms |= {e["name"].lower() for e in world.effects}
    return terms


UNDEFINED_WATCHLIST = ("sacrifice", "hexproof", "untargetable", "spell shield",
                       "taxing", "recursion", "arena")


def f8_undefined_terms(world: World) -> list[Finding]:
    known = defined_terms()
    findings = []
    for card in world.cards:
        blob = f"{card.rules_text}\n{card.ascended_text}".lower()
        for term in UNDEFINED_WATCHLIST:
            if re.search(rf"\b{re.escape(term)}", blob) and term not in known:
                findings.append(Finding(
                    "F8", "error", card.name,
                    f"uses the term '{term}', which is defined nowhere in the rulebook or data.",
                    where=card.rel_path,
                    fix=f"Define '{term}' in docs/rulebook/13-glossary.md in the same change."))
    return findings


def f9_broken_references(world: World) -> list[Finding]:
    known_kw = {k["name"] for k in world.keywords}
    known_ef = {e["name"] for e in world.effects}
    known_crews = {c["name"] for c in world.crews}
    known_factions = {f["name"] for f in world.factions}
    known_states = {s["key"] for s in world.states}
    findings = []
    for card in world.cards:
        if card.faction and card.faction not in known_factions:
            findings.append(Finding("F9", "error", card.name,
                                    f"faction '{card.faction}' is not in data/factions.yaml",
                                    where=card.rel_path))
        crew = card.meta.get("crew")
        if crew and crew not in known_crews:
            findings.append(Finding("F9", "error", card.name,
                                    f"crew '{crew}' is not in data/crews.yaml", where=card.rel_path))
        for kind, name, side in card_tools(card):
            pool = known_kw if kind == "keywords" else known_ef
            if name not in pool:
                findings.append(Finding("F9", "error", card.name,
                                        f"unknown {kind[:-1]} '{name}' on the {side} side",
                                        where=card.rel_path))
        plan = card.meta.get("plan") or {}
        for field_name in ("requires", "produces"):
            for state in plan.get(field_name) or []:
                if state not in known_states:
                    findings.append(Finding(
                        "F9", "error", card.name,
                        f"plan.{field_name} names '{state}', which is not in data/game-states.yaml",
                        where=card.rel_path))
    return findings


# ------------------------------------------------------------------ jobs & formations
#
# A Job is what a Character does for its crew; a Role (keyword) is one of the tools it does it
# with. These rules check that the claim and the mechanics agree, and that a crew's five slots
# actually cover the Formation it declared.
#
# Every rule here skips exempt factions (Icons). See World.is_exempt.

def crew_members(world: World, crew: dict) -> list:
    return [c for c in world.cards if c.meta.get("crew") == crew["name"]]


def f11_job_legality(world: World) -> list[Finding]:
    """A card's declared Job must exist, and its faction must be allowed to hold it."""
    findings = []
    known = {j["key"] for j in world.jobs}
    for card in world.cards:
        job_key = card.meta.get("job")
        if not job_key or world.is_exempt(card.faction):
            continue
        if job_key not in known:
            findings.append(Finding(
                "F11", "error", card.name,
                f"declares job '{job_key}', which is not in data/jobs.yaml",
                where=card.rel_path,
                fix="Use a key from data/jobs.yaml, or add the Job there first."))
            continue
        job = world.job(job_key)
        allowed = job.get("factions")
        if allowed and card.faction:
            faction = world.faction(card.faction)
            if faction and faction["key"] not in allowed:
                findings.append(Finding(
                    "F11", "error", card.name,
                    f"is {card.faction} but '{job['name']}' is restricted to "
                    f"{', '.join(allowed)}. "
                    + (job.get("faction_note") or "").strip(),
                    where=card.rel_path,
                    fix=f"Either change the Job, or widen `factions:` on {job_key} in "
                        f"data/jobs.yaml — but only if the faction's printed lore allows it."))
    return findings


def f12_chaotic_crew_enablers(world: World) -> list[Finding]:
    """A chaotic crew's defining claim is mechanical, so it is checkable.

    Reuses the same producer/requirer graph as W2 — the tool built to FIND unwanted combos is
    exactly the tool that proves a chaotic crew has none.
    """
    findings = []
    for crew in world.crews:
        if crew.get("coordination") != "chaotic":
            continue
        members = crew_members(world, crew)
        produced: dict[str, list] = {}
        for card in members:
            for state in (card.meta.get("plan") or {}).get("produces") or []:
                produced.setdefault(state, []).append(card)
        for card in members:
            for state in (card.meta.get("plan") or {}).get("requires") or []:
                for other in produced.get(state, []):
                    if other.name == card.name:
                        continue
                    findings.append(Finding(
                        "F12", "error", crew["name"],
                        f"declares itself chaotic, but {card.name} requires '{state}' and "
                        f"crewmate {other.name} produces it. That is an enabler chain, which "
                        f"is coordination.",
                        where=card.rel_path,
                        fix="Either break the chain, or drop `coordination: chaotic` — a crew "
                            "cannot claim the higher individual rate AND combo internally."))
    return findings


def w12_job_signature(world: World) -> list[Finding]:
    """A card claiming a Job should look like one. Guidance, never law — hence a warning."""
    findings = []
    for card in world.cards:
        job_key = card.meta.get("job")
        if not job_key or world.is_exempt(card.faction):
            continue
        job = world.job(job_key)
        if not job:
            continue                                   # F11 already reported it
        signature = job.get("signature") or {}
        wanted_kw = set(signature.get("keywords_any") or [])
        wanted_ef = set(signature.get("effects_any") or [])
        if not wanted_kw and not wanted_ef:
            continue                                   # nothing mechanical to check against
        held = {name for kind, name, _ in card_tools(card)}
        if held & (wanted_kw | wanted_ef):
            continue
        article = "An" if job["name"][0].upper() in "AEIOU" else "A"
        findings.append(Finding(
            "W12", "warning", card.name,
            f"claims the Job '{job['name']}' but has none of its signature. "
            f"{article} {job['name']} usually shows one of: "
            f"{', '.join(sorted(wanted_kw | wanted_ef)[:6])}"
            f"{'…' if len(wanted_kw | wanted_ef) > 6 else ''}",
            where=card.rel_path,
            fix=f"Either give it a tool that does the Job — {job.get('job', '').strip()} — "
                f"or pick the Job it is actually doing."))
    return findings


def w13_formation_coverage(world: World) -> list[Finding]:
    """A crew declared a Formation. Do its five cards actually cover the required Jobs?"""
    findings = []
    for crew in world.crews:
        formation_key = crew.get("formation")
        if not formation_key:
            continue
        formation = world.formation(formation_key)
        if not formation:
            findings.append(Finding(
                "W13", "warning", crew["name"],
                f"declares formation '{formation_key}', which is not in data/formations.yaml",
                where="data/crews.yaml"))
            continue
        members = [c for c in crew_members(world, crew) if not world.is_exempt(c.faction)]
        held = {c.meta.get("job") for c in members if c.meta.get("job")}
        missing = [j for j in formation["required_jobs"] if j not in held]
        if missing:
            names = [(world.job(m) or {}).get("name", m) for m in missing]
            findings.append(Finding(
                "W13", "warning", crew["name"],
                f"declares {formation['name']} but has no "
                f"{', no '.join(names)} among its {len(members)} cards.",
                where="data/crews.yaml",
                fix=f"Design a {names[0]}, or declare a Formation the crew actually fields. "
                    f"The plan is: {formation['plan'].strip()}"))
    return findings


def w14_job_duplication(world: World) -> list[Finding]:
    """Two cards doing the same Job in one crew — the swap test, made mechanical.

    A Formation has four required Jobs and one free slot, so exactly one duplicate is legal
    (the free slot may repeat a required Job). Two duplicates means a card has no seat.
    """
    findings = []
    for crew in world.crews:
        members = [c for c in crew_members(world, crew) if not world.is_exempt(c.faction)]
        seen: dict[str, list] = {}
        for card in members:
            if card.meta.get("job"):
                seen.setdefault(card.meta["job"], []).append(card.name)
        formation = world.formation(crew.get("formation") or "")
        allowance = 1 if formation else 1           # the free slot
        for job_key, names in seen.items():
            if len(names) > 1 + allowance:
                job = world.job(job_key) or {}
                findings.append(Finding(
                    "W14", "warning", crew["name"],
                    f"{len(names)} cards all do the Job '{job.get('name', job_key)}': "
                    f"{', '.join(names)}. A Formation has one free slot, not two.",
                    where="data/crews.yaml",
                    fix="Give one of them a different Job and redesign it to match — a Job is "
                        "a testable version of the crew's 'different road' rule."))
    return findings


def w15_jobs_undeclared(world: World) -> list[Finding]:
    """One finding for the whole pool, not one per card.

    A linter that fires 30 times for the same missing field teaches you to ignore the linter.
    """
    missing = [c.name for c in world.cards
               if not c.meta.get("job") and not world.is_exempt(c.faction)]
    if not missing:
        return []
    return [Finding(
        "W15", "warning", "the card pool",
        f"{len(missing)} of {len(world.cards)} cards declare no Job: "
        f"{', '.join(missing[:5])}{'…' if len(missing) > 5 else ''}",
        where="cards/",
        fix="Set `job:` in the frontmatter, or pick it on the Studio's Cards screen. Until a "
            "card has a Job, Formation coverage cannot see it.")]


# ------------------------------------------------------------------ reach

def answering_factions(world: World, card) -> list[str]:
    """Factions that are STRONG in at least one window this card declares."""
    declared = set((card.meta.get("plan") or {}).get("windows") or [])
    if not declared:
        return []
    out = []
    for faction in world.factions:
        windows = faction.get("windows") or {}
        if any(windows.get(w) == "strong" for w in declared):
            out.append(faction["name"])
    return out


def computed_reach(world: World, card) -> int | None:
    declared = (card.meta.get("plan") or {}).get("windows") or []
    if not declared:
        return None
    return len(answering_factions(world, card))


# ------------------------------------------------------------------ warnings

def w1_window_coverage(world: World) -> list[Finding]:
    findings = []
    for window in WINDOW_KEYS:
        strong = [f["name"] for f in world.factions if (f.get("windows") or {}).get(window) == "strong"]
        if len(strong) < MIN_FACTIONS_PER_WINDOW:
            findings.append(Finding(
                "W1", "warning", WINDOW_LABELS[window],
                f"only {len(strong)} faction is strong here ({', '.join(strong) or 'none'}). "
                f"Cards answerable only in this window will be {strong[0] if strong else 'un'}"
                f"{'-mandatory' if strong else 'answerable'}.",
                where="data/factions.yaml",
                fix="Give a second faction a strong profile here, or accept that this window "
                    "is a faction privilege and price cards accordingly."))
    return findings


def w2_enabler_chains(world: World) -> list[Finding]:
    """Card A produces exactly what card B requires -- the Enabler Test, automated."""
    producers: dict[str, list] = {}
    for card in world.cards:
        for state in (card.meta.get("plan") or {}).get("produces") or []:
            producers.setdefault(state, []).append(card)
    findings = []
    for card in world.cards:
        for state in (card.meta.get("plan") or {}).get("requires") or []:
            for other in producers.get(state, []):
                if other.name == card.name:
                    continue
                same_crew = other.meta.get("crew") and other.meta.get("crew") == card.meta.get("crew")
                findings.append(Finding(
                    "W2", "warning", card.name,
                    f"requires '{state}', which {other.name} produces"
                    + (f" — and they are both {card.meta.get('crew')}." if same_crew
                       else f" ({other.meta.get('crew') or 'no crew'})."),
                    where=card.rel_path,
                    fix="Set the enabler test on that cost to 'crew' (credit 0) if they will be "
                        "played together." if same_crew else
                        "Set the enabler test to 'faction' (half credit) if this pairing is likely."))
    return findings


def w3_crew_diversity(world: World) -> list[Finding]:
    findings = []
    for crew in world.crews:
        members = [c for c in world.cards if c.meta.get("crew") == crew["name"]]
        expressions = crew.get("expressions") or []
        roads = {}
        for entry in expressions:
            road = (entry.get("road") or "").strip().lower()
            if road:
                roads.setdefault(road, []).append(entry.get("card"))
        for road, cards in roads.items():
            if len(cards) > 1:
                findings.append(Finding(
                    "W3", "warning", crew["name"],
                    f"{len(cards)} cards share the road \"{road}\": {', '.join(cards)}.",
                    where="data/crews.yaml",
                    fix="Rewrite one of them to reach the crew's plan a different way."))
        described = {e.get("card") for e in expressions}
        missing = [c.meta.get("slug") for c in members if c.meta.get("slug") not in described]
        if missing and crew.get("coordination") != "chaotic":
            findings.append(Finding(
                "W3", "warning", crew["name"],
                f"{len(missing)} of {len(members)} cards have no declared road: "
                f"{', '.join(m for m in missing if m)}",
                where="data/crews.yaml",
                fix="Say in one line how each card advances the crew's plan differently."))
    return findings


def w4_crew_plan_missing(world: World) -> list[Finding]:
    findings = []
    for crew in world.crews:
        plan = (crew.get("plan") or "").strip()
        if not plan or plan.upper().startswith(("UNWRITTEN", "UNDECIDED", "TODO")):
            findings.append(Finding(
                "W4", "warning", crew["name"],
                "has no written plan. Its cards will drift into being unrelated good cards.",
                where="data/crews.yaml",
                fix="Write one sentence: how does this crew win a game?"))
        if not crew.get("reviewed"):
            findings.append(Finding(
                "W4", "warning", crew["name"],
                "plan is a draft nobody has reviewed. Everything downstream validates against it.",
                where="data/crews.yaml", fix="Set reviewed: true once you've confirmed it."))
    for faction in world.factions:
        if not faction.get("reviewed"):
            findings.append(Finding(
                "W4", "warning", faction["name"],
                "toolkit and window profile are drafts nobody has reviewed.",
                where="data/factions.yaml", fix="Set reviewed: true once you've confirmed them."))
    return findings


def w5_twins(world: World) -> list[Finding]:
    """Two cards anywhere in the pool with the same functional signature."""
    signatures: dict[tuple, list] = {}
    for card in world.cards:
        if card.meta.get("cost") is None:
            continue
        signature = (card.meta["cost"], card.faction,
                     tuple(sorted(card.side("base")["effects"])),
                     tuple(sorted(card.side("base")["keywords"])))
        if not signature[2] and not signature[3]:
            continue
        signatures.setdefault(signature, []).append(card.name)
    findings = []
    for signature, names in signatures.items():
        if len(names) > 1:
            findings.append(Finding(
                "W5", "warning", names[0],
                f"is functionally identical to {', '.join(names[1:])} — same cost, faction, "
                f"keywords and effects.", fix="Differentiate in type, not in value."))
    return findings


def w6_scaling_text(world: World) -> list[Finding]:
    """Card text that scales, against an effect table whose entries stop at 5."""
    ceiling = max((int(e["points"]) for e in world.effects), default=0)
    findings = []
    for card in world.cards:
        for side, text in (("base", card.rules_text), ("ascended", card.ascended_text)):
            if not text:
                continue
            hit = next((p for p in SCALING_PHRASES if p in text.lower()), None)
            if not hit:
                continue
            logged = sum(scoring.effect_points().get(n, 0) for n in card.side(side)["effects"])
            findings.append(Finding(
                "W6", "warning", card.name,
                f"{side} text scales (\"{hit}\") but is logged as only {logged} points. "
                f"A scaling effect can be worth far more than any entry in the table "
                f"(largest is {ceiling}).",
                where=card.rel_path,
                fix="Record the realistic maximum, or add a bigger entry to data/effects.yaml."))
    return findings


def w7_ceiling_quota(world: World) -> list[Finding]:
    quota = scoring.plan_config().get("ceiling_quota", 0.10)
    big = []
    for card in world.cards:
        result = scoring.score(card)
        if result.scorable and result.budget and result.ceiling > result.budget * 2:
            big.append(card.name)
    total = len([c for c in world.cards if scoring.score(c).scorable])
    if total and len(big) > total * quota:
        return [Finding("W7", "warning", "the pool",
                        f"{len(big)} of {total} cards sit above 2x base budget "
                        f"(quota is {int(quota*100)}%). If every card is a heist, nothing is.",
                        fix="Lower the ambition on the least interesting of them.")]
    return []


def w8_dead_entries(world: World) -> list[Finding]:
    used = set()
    for card in world.cards:
        used |= {n for _, n, _ in card_tools(card)}
    owned = set()
    for faction in world.factions:
        for kind in ("keywords", "effects"):
            owned |= set((faction.get("unique") or {}).get(kind) or [])
    findings = []
    for entry in world.effects + world.keywords:
        name = entry["name"]
        if name not in used and name not in owned:
            findings.append(Finding("W8", "warning", name,
                                    "is in the tables but no card uses it and no faction owns it.",
                                    where="data/", fix="Assign it to a faction or delete it."))
    return findings


LORE_FALL = "The Fall (printed weakness)"
LORE_ASCENSION = "The Ascension (what the level-up MEANS)"
LORE_WHY_CREW = "Why This Crew"
LORE_WHY_FACTION = "Why This Faction"


def w9_lore_gates(world: World) -> list[Finding]:
    """The Lore Packet is working notes, but some fields are load-bearing for the mechanics.

    The Fall feeds gameplay D1 and lore D4 -- a card carrying only its faction's strength is a
    card wearing the colour. The Ascension is what makes a level-up earned rather than a stat
    bump. Why This Crew is the card's road, which the crew diversity rule (W3) reads.

    One finding per card, not one per field -- four separate warnings about the same card is
    noise, and noise is how a linter teaches you to ignore it.
    """
    findings = []
    for card in world.cards:
        status = card.meta.get("status")
        if status in (None, "draft"):
            continue
        lore = card.lore or {}
        required = [(LORE_TRUE_DETAIL, "the one real fact about the real person")]
        if card.faction:
            required.append((LORE_FALL, f"how it is exposed to the {card.faction} weakness"))
        if card.meta.get("crew"):
            required.append((LORE_WHY_CREW, "which is also its road for the crew diversity rule"))
        if card.is_ascendant and card.levelup_condition:
            required.append((LORE_ASCENSION, "what levelling up MEANS, beyond the stat change"))

        missing = [(field, why) for field, why in required if not (lore.get(field) or "").strip()]
        if not missing:
            continue
        names = ", ".join(f.split(" (")[0] for f, _ in missing)
        findings.append(Finding(
            "W9", "warning", card.name,
            f"is '{status}' but its Lore Packet is missing {len(missing)} required field"
            f"{'s' if len(missing) > 1 else ''}: {names}.",
            where=card.rel_path,
            fix="; ".join(f"{f.split(' (')[0]} — {why}" for f, why in missing)))
    return findings


# This game capitalises its rules terms ("pay 1 Energy", "a Character", "the Board") and
# lower-cases prose. That, plus digits, separates mechanism from flavour far more reliably
# than a keyword list -- "he draws all the squad's heat" and "feeds on the heavy energy of a
# wild room" are both flavour, and a word list flags both.
GAME_TERMS = ("Energy", "Board", "Round", "Character", "Life Point", "Physical Attack",
              "Mental Attack", "Physical Health", "Mental Health", "Phase", "Combat Wave",
              "Graveyard", "Hand", "Resource Row", "Attachment", "Tactic", "Murder",
              "Ascendant", "Descendant", "Influence", "Commandment")
MIN_FLAVOUR_WORDS = 5


def w11_no_flavour(world: World) -> list[Finding]:
    """The card's printed flavour: the one line of story inside the rules text.

    The Lore Packet is private working notes; this sentence is what players actually read.
    A card whose rules text is pure mechanism has no voice at the table.
    """
    findings = []
    for card in world.cards:
        if card.meta.get("status") in (None, "draft") or not card.rules_text:
            continue
        text = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", card.rules_text)
        prose = []
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", text):
            sentence = sentence.strip()
            if len(sentence.split()) < MIN_FLAVOUR_WORDS:
                continue
            if re.search(r"\d", sentence):
                continue
            if any(term in sentence for term in GAME_TERMS):
                continue
            prose.append(sentence)
        if not prose:
            findings.append(Finding(
                "W11", "warning", card.name,
                "has no flavour sentence — every line of its rules text is mechanism.",
                where=card.rel_path,
                fix="Write one line of story into the rules text, drawn from the Lore Packet. "
                    "That sentence is the part players actually read."))
    return findings


def w10_faction_gaps(world: World) -> list[Finding]:
    """A faction blind in every window another is strong in has no game against them."""
    findings = []
    for attacker in world.factions:
        strong = {w for w in WINDOW_KEYS if (attacker.get("windows") or {}).get(w) == "strong"}
        for defender in world.factions:
            if defender is attacker:
                continue
            profile = defender.get("windows") or {}
            if strong and all(profile.get(w) == "blind" for w in strong):
                findings.append(Finding(
                    "W10", "warning", defender["name"],
                    f"is blind in every window the {attacker['name']} are strong in "
                    f"({', '.join(WINDOW_LABELS[w] for w in sorted(strong))}).",
                    where="data/factions.yaml",
                    fix="Give them one weak profile in one of those windows, or accept this as "
                        "a designed hard matchup and document it."))
    return findings


# ------------------------------------------------------------------ runner

HARD = [f1_unique_conflicts, f10_keyword_ownership, f2_f3_toolkit_violations, f4_over_ceiling, f5_reach_overclaim,
        f6_f7_card_gates, f8_undefined_terms, f9_broken_references,
        f11_job_legality, f12_chaotic_crew_enablers]
SOFT = [w1_window_coverage, w2_enabler_chains, w3_crew_diversity, w4_crew_plan_missing,
        w5_twins, w6_scaling_text, w7_ceiling_quota, w8_dead_entries, w9_lore_gates,
        w10_faction_gaps, w11_no_flavour,
        w12_job_signature, w13_formation_coverage, w14_job_duplication, w15_jobs_undeclared]


def run_all(world: World | None = None) -> list[Finding]:
    world = world or load_world()
    findings = []
    for rule in HARD + SOFT:
        try:
            findings += rule(world)
        except Exception as exc:                      # a broken rule must not hide the others
            findings.append(Finding("RULE", "error", rule.__name__,
                                    f"rule crashed: {type(exc).__name__}: {exc}"))
    return findings


DECK_TARGET = {"Descendant": 24, "Tactic": 8, "Attachment": 3, "Ascendant": 5}


def gaps(world: World | None = None) -> list[Finding]:
    """What's MISSING, as opposed to what's wrong. The answer to 'what do I build next'."""
    world = world or load_world()
    out = []

    counts: dict[str, int] = {}
    for card in world.cards:
        counts[card.meta.get("subtype") or "?"] = counts.get(card.meta.get("subtype") or "?", 0) + 1
    for subtype, want in DECK_TARGET.items():
        have = counts.get(subtype, 0)
        if have < want:
            out.append(Finding("GAP", "gap", subtype,
                               f"{have} of the ~{want} a legal 40-card deck wants — short {want - have}.",
                               fix=f"Design {want - have} more {subtype}s."))

    for faction in world.factions:
        mine = [c for c in world.cards if c.faction == faction["name"]]
        playable = [c for c in mine if c.meta.get("cost") is not None]
        if not playable:
            out.append(Finding("GAP", "gap", faction["name"],
                               f"has {len(mine)} cards and none of them are playable "
                               f"(no cost, no stats).",
                               fix="This faction cannot be built with. Start with one card."))

    for crew in world.crews:
        mine = [c for c in world.cards if c.meta.get("crew") == crew["name"]]
        if len(mine) < 5:
            out.append(Finding("GAP", "gap", crew["name"],
                               f"has {len(mine)} cards. A crew needs about five to express a plan "
                               f"through different roads.",
                               fix=f"Design {5 - len(mine)} more."))

    covered = set()
    for card in world.cards:
        covered |= set((card.meta.get("plan") or {}).get("produces") or [])
        covered |= set((card.meta.get("plan") or {}).get("requires") or [])
    unused = [s["key"] for s in world.states if s["key"] not in covered]
    if unused:
        out.append(Finding("GAP", "gap", "game states",
                           f"{len(unused)} board conditions are defined but no card touches them: "
                           f"{', '.join(unused[:6])}{'…' if len(unused) > 6 else ''}",
                           where="data/game-states.yaml",
                           fix="Either design cards that use them, or trim the vocabulary."))

    # Which Jobs does nobody in the whole pool do? That is the design backlog, and it is the
    # single most useful thing the Job layer produces.
    filled = {c.meta.get("job") for c in world.cards if c.meta.get("job")}
    empty_built = [j for j in world.jobs if j["status"] == "built" and j["key"] not in filled]
    if empty_built:
        by_family: dict[str, list] = {}
        for job in empty_built:
            by_family.setdefault(job["family"], []).append(job["name"])
        summary = "; ".join(f"{fam}: {', '.join(sorted(names))}"
                            for fam, names in sorted(by_family.items()))
        out.append(Finding("GAP", "gap", "unfilled Jobs",
                           f"{len(empty_built)} Jobs the rules CAN express have no card doing "
                           f"them — {summary}",
                           where="data/jobs.yaml",
                           fix="Each one is a card waiting to be designed. Start with a Job "
                               "its Formation requires."))

    unbuilt = [j for j in world.jobs if j["status"] == "unbuilt"]
    if unbuilt:
        out.append(Finding("GAP", "gap", "Jobs with no mechanics",
                           f"{len(unbuilt)} Jobs are real positions the rules still cannot "
                           f"express: {', '.join(j['name'] for j in unbuilt)}",
                           where="data/jobs.yaml",
                           fix="These need a RULES change before a card can be designed. They "
                               "stay listed on purpose — never as an error."))

    unclaimed = [f["name"] for f in world.formations
                 if not any(c.get("formation") == f["key"] for c in world.crews)]
    if unclaimed:
        out.append(Finding("GAP", "gap", "Formations",
                           f"{len(unclaimed)} Formations are declared by no crew: "
                           f"{', '.join(unclaimed)}",
                           where="data/formations.yaml",
                           fix="Assignments are on hold until the lore decides. Lore leads, "
                               "plan follows, Formation follows the plan."))

    influence = [c for c in world.cards
                 if "influence" in f"{c.rules_text}\n{c.ascended_text}".lower()]
    if len(influence) < 3:
        out.append(Finding("GAP", "gap", "the Influence victory",
                           f"only {len(influence)} cards mention Influence, and it is one of the "
                           f"three printed win conditions.",
                           fix="Build it or cut it from the rulebook (OQ-02)."))
    return out


def worklist(findings: list[Finding]) -> list[Finding]:
    """Ranked: errors first, then by how many things share the cause."""
    counts: dict[str, int] = {}
    for f in findings:
        counts[f.code] = counts.get(f.code, 0) + 1
    order = {"error": 0, "warning": 1, "gap": 2}
    return sorted(findings, key=lambda f: (order.get(f.severity, 3), -counts[f.code],
                                           f.code, f.subject))
