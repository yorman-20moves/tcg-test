#!/usr/bin/env python3
"""Budget arithmetic and the machine-checkable rubric gates.

One implementation, consumed by balance.py, validate.py and studio.py, so the number
shown in the design workbench is by construction the same number the CLI reports.

See docs/rubrics/gameplay-rubric.md for what the gates mean.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache

from card_io import STAT_KEYS, Card, load_table

COST_TO_BUDGET_MULTIPLIER = 3
BUDGET_BASE_ALLOWANCE = 1
ASCENDANT_BUDGET_BONUS = 3

# The ascended side may spend this multiple of the base budget (gameplay rubric G1).
ASCENDED_BUDGET_MULTIPLIER = 1.5

DEFAULT_TOLERANCE = 1

# |delta| thresholds -> severity, matching the status palette used in the UI.
SEVERITY_BANDS = ((1, "good"), (3, "warning"), (6, "serious"))
SEVERITY_WORST = "critical"

ABILITY_TYPES = ("Standard Ability", "Fast Ability", "Trigger Ability", "Passive Ability")
DURATION_PHRASES = (
    "end of the round", "end step", "end of round", "permanent", "permanently",
    "until removed", "this round", "this turn", "once per round", "for the duration",
)
HUMAN_ONLY_GATES = {
    "G2": "every rules term is defined in the rulebook or data/",
    "G5": "no unbounded loop with any existing card",
    "G7": "answerable by at least one existing card, including by the poorest-tooled faction",
    "G9": "losing to it feels like being outplayed or roasted, never robbed or insulted",
}


@lru_cache(maxsize=1)
def keyword_points() -> dict[str, int]:
    return {k["name"]: int(k["points"]) for k in load_table("keywords.yaml", "keywords")}


@lru_cache(maxsize=1)
def keyword_faction() -> dict[str, str]:
    return {k["name"]: k["faction"] for k in load_table("keywords.yaml", "keywords")}


@lru_cache(maxsize=1)
def effect_points() -> dict[str, int]:
    return {e["name"]: int(e["points"]) for e in load_table("effects.yaml", "effects")}


@lru_cache(maxsize=1)
def status_names() -> tuple[str, ...]:
    return tuple(s["name"] for s in load_table("status-effects.yaml", "status_effects") if s["name"])


def severity(delta: int, tolerance: int = DEFAULT_TOLERANCE) -> str:
    """Two-sided: on the base side, under budget is as wrong as over -- an underspent card
    is a card that does nothing for its cost."""
    magnitude = abs(delta)
    if magnitude <= tolerance:
        return "good"
    for threshold, label in SEVERITY_BANDS:
        if magnitude <= threshold:
            return label
    return SEVERITY_WORST


def ceiling_severity(delta: int) -> str:
    """One-sided, for the ascended budget: the multiplier is a CEILING, so spending less
    than it is fine. Only overage is a problem."""
    return "good" if delta >= 0 else severity(delta, tolerance=0)


@dataclass
class Score:
    scorable: bool
    reason: str = ""
    budget: int = 0
    stats_total: int = 0
    base_keyword_points: int = 0
    base_effect_points: int = 0
    ascended_keyword_points: int = 0
    ascended_effect_points: int = 0
    unknown_names: list[str] = field(default_factory=list)

    @property
    def base_spent(self) -> int:
        return self.stats_total + self.base_keyword_points + self.base_effect_points

    @property
    def base_delta(self) -> int:
        return self.budget - self.base_spent

    @property
    def ascended_spent(self) -> int:
        return self.ascended_keyword_points + self.ascended_effect_points

    @property
    def ascended_budget(self) -> int:
        return int(self.budget * ASCENDED_BUDGET_MULTIPLIER)

    @property
    def ascended_delta(self) -> int:
        """Against the proposed rule: total spend vs base budget x 1.5. See OQ-04."""
        return self.ascended_budget - (self.base_spent + self.ascended_spent)

    def as_dict(self) -> dict:
        return {
            "scorable": self.scorable, "reason": self.reason, "budget": self.budget,
            "statsTotal": self.stats_total,
            "baseKeywordPoints": self.base_keyword_points,
            "baseEffectPoints": self.base_effect_points,
            "ascendedKeywordPoints": self.ascended_keyword_points,
            "ascendedEffectPoints": self.ascended_effect_points,
            "baseSpent": self.base_spent, "baseDelta": self.base_delta,
            "baseSeverity": severity(self.base_delta),
            "ascendedSpent": self.ascended_spent, "ascendedBudget": self.ascended_budget,
            "ascendedDelta": self.ascended_delta,
            "ascendedSeverity": ceiling_severity(self.ascended_delta),
            "unknownNames": self.unknown_names,
        }


def score(card: Card) -> Score:
    if card.meta.get("cost") is None:
        return Score(scorable=False, reason="no cost defined (stub card)")
    if not card.has_full_stats:
        return Score(scorable=False, reason="incomplete stat line")

    kw_table, ef_table = keyword_points(), effect_points()
    unknown: list[str] = []

    def total(names, table):
        running = 0
        for entry in names:
            if entry in table:
                running += table[entry]
            else:
                unknown.append(entry)
        return running

    base, ascended = card.side("base"), card.side("ascended")
    budget = (int(card.meta["cost"]) * COST_TO_BUDGET_MULTIPLIER + BUDGET_BASE_ALLOWANCE
              + (ASCENDANT_BUDGET_BONUS if card.is_ascendant else 0))

    return Score(
        scorable=True,
        budget=budget,
        stats_total=sum(int(card.stats[k]) for k in STAT_KEYS),
        base_keyword_points=total(base["keywords"], kw_table),
        base_effect_points=total(base["effects"], ef_table),
        ascended_keyword_points=total(ascended["keywords"], kw_table),
        ascended_effect_points=total(ascended["effects"], ef_table),
        unknown_names=unknown,
    )


# --------------------------------------------------------------------------- gates

def _gate_g1(card: Card, result: Score, tolerance: int) -> list[str]:
    if not result.scorable:
        return []
    failures = []
    if abs(result.base_delta) > tolerance:
        direction = "over" if result.base_delta < 0 else "under"
        failures.append(f"G1: base side {direction} budget by {abs(result.base_delta)}")
    if card.is_ascendant and result.ascended_delta < 0:
        failures.append(f"G1: ascended side exceeds base budget x{ASCENDED_BUDGET_MULTIPLIER} "
                        f"by {abs(result.ascended_delta)} (see OQ-04)")
    return failures


def _gate_g3(card: Card) -> list[str]:
    failures = []
    known = set(ABILITY_TYPES) | set(keyword_points())
    for text in (card.rules_text, card.ascended_text):
        for ability_name, declared in re.findall(r"\[([^\]]+)\]\s*(\([^)]*\))?", text):
            if ability_name in ABILITY_TYPES:
                continue
            if not declared:
                failures.append(f"G3: ability [{ability_name}] declares no ability type")
            elif declared.strip("()") not in known:
                failures.append(f"G3: ability [{ability_name}] declares unknown type "
                                f"'{declared.strip('()')}'")
    return failures


def _gate_g4(card: Card) -> list[str]:
    owners, failures = keyword_faction(), []
    for which in ("base", "ascended"):
        for keyword in card.side(which)["keywords"]:
            owner = owners.get(keyword)
            if owner is None:
                failures.append(f"G4: unknown keyword '{keyword}' on {which} side")
            elif owner != card.faction:
                failures.append(f"G4: {which} keyword '{keyword}' belongs to {owner}, "
                                f"card is {card.faction}")
    return failures


def _gate_g6(card: Card) -> list[str]:
    combined = f"{card.rules_text}\n{card.ascended_text}".lower()
    applied = [s for s in status_names() if re.search(rf"\b{re.escape(s.lower())}\b", combined)]
    if applied and not any(phrase in combined for phrase in DURATION_PHRASES):
        return [f"G6: applies status ({', '.join(applied)}) with no stated duration"]
    return []


def _gate_g8(card: Card) -> list[str]:
    failures = []
    if not card.faction:
        failures.append("G8: no faction")
    if not (card.meta.get("art") or {}).get("base"):
        failures.append("G8: no base art reference")
    if "crew" not in card.meta:
        failures.append("G8: crew key absent (use `crew: null` with a reason in Design Notes)")
    return failures


def gates(card: Card, result: Score | None = None,
          tolerance: int = DEFAULT_TOLERANCE) -> dict[str, list[str]]:
    """Return {gate_id: [failure messages]}. An empty list means the gate passed."""
    result = result if result is not None else score(card)
    return {
        "G1": _gate_g1(card, result, tolerance),
        "G3": _gate_g3(card),
        "G4": _gate_g4(card),
        "G6": _gate_g6(card),
        "G8": _gate_g8(card),
    }
