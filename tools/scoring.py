#!/usr/bin/env python3
"""Budget arithmetic and the machine-checkable rubric gates.

One implementation, consumed by balance.py, validate.py and studio.py, so the number
shown in the design workbench is by construction the same number the CLI reports.

See docs/rubrics/gameplay-rubric.md for what the gates mean.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from card_io import STAT_KEYS, Card, ability_type_names, cached_on, load_table

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


@cached_on("data/keywords.yaml")
def keyword_points() -> dict[str, int]:
    return {k["name"]: int(k["points"]) for k in load_table("keywords.yaml", "keywords")}


@cached_on("data/keywords.yaml")
def keyword_faction() -> dict[str, str]:
    return {k["name"]: k["faction"] for k in load_table("keywords.yaml", "keywords")}


@cached_on("data/effects.yaml")
def effect_points() -> dict[str, int]:
    return {e["name"]: int(e["points"]) for e in load_table("effects.yaml", "effects")}


@cached_on("data/plan-credits.yaml")
def plan_config() -> dict:
    """The Score's credit table and window multiplier. See docs/design/balance-philosophy.md."""
    import yaml
    from card_io import REPO_ROOT
    path = REPO_ROOT / "data" / "plan-credits.yaml"
    if not path.exists():
        return {"window_step": 0.25, "max_windows": 5, "narrowness_cap": 4,
                "credits": [], "windows": [], "prohibitions": []}
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@cached_on("data/status-effects.yaml")
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
class Plan:
    """What the card pays beyond Energy, and who can answer it.

    Allowance = base budget + credits
    Ceiling   = min(Allowance, base budget x reach cap)

    Credits earn power. Reach decides whether you are allowed to collect it. A card that
    pays nothing has Allowance == base budget, i.e. the original rule, unchanged.

    Each cost carries up to three discounts (see balance-philosophy.md Part Two):
      bite    -- does paying it make you worse at what the card wants to do?
      timing  -- before the payoff (full), at it (half), after it (nothing)
      enabler -- does another card, especially in the same crew, hand it to you free?
    """
    credits_paid: dict = field(default_factory=dict)
    windows: list = field(default_factory=list)
    reach: int | None = None
    tests: dict = field(default_factory=dict)   # {cost_key: {"bite": "...", ...}}

    def _discount(self, cost_key: str) -> tuple[float, list[str]]:
        """Multiplier from the three tests. Absent tests default to full credit."""
        scales = plan_config().get("cost_tests", {})
        chosen = (self.tests or {}).get(cost_key, {})
        factor, notes = 1.0, []
        for test_name, options in scales.items():
            answer = chosen.get(test_name)
            if answer is None:
                continue
            value = options.get(answer)
            if value is None:
                continue
            factor *= float(value)
            if value != 1.0:
                notes.append(f"{test_name}={answer}")
        return factor, notes

    def credit_points(self) -> tuple[int, list[str]]:
        config = plan_config()
        table = {c["key"]: c for c in config.get("credits", [])}
        narrowness_cap = config.get("narrowness_cap", 4)
        total, breakdown = 0, []
        for key, quantity in (self.credits_paid or {}).items():
            entry = table.get(key)
            if not entry or not quantity:
                continue
            raw = int(entry["points"]) * int(quantity)
            if key == "narrowness":
                raw = min(raw, narrowness_cap)
            factor, notes = self._discount(key)
            points = int(raw * factor)
            total += points
            label = f"{entry['label']} x{quantity} = {raw}"
            if factor != 1.0:
                label += f"  ->  {points}  ({', '.join(notes) or 'discounted'})"
            breakdown.append(label)
        return total, breakdown

    @property
    def declared(self) -> bool:
        """True once the designer has actually described a plan. An undeclared card is not
        'Reach 0 / unprintable' -- it is simply an ordinary card held to the base budget."""
        return bool(self.credits_paid or self.windows or self.reach is not None)

    def reach_value(self, faction: str | None = None) -> int | None:
        """Explicit override wins; otherwise compute from the faction window map.

        Computed Reach = how many factions are STRONG in at least one window this card
        declares. That is the whole point of data/factions.yaml: the softest number in the
        balance system stops being a guess.
        """
        if self.reach is not None:
            return max(0, min(4, int(self.reach)))
        if not self.windows:
            return None
        computed = self.computed_reach()
        return computed if computed is not None else min(4, self.window_count())

    def computed_reach(self) -> int | None:
        """None when factions.yaml has no window profiles to compute from."""
        return None if self._answering() is None else len(self._answering())

    def answering_factions(self) -> list[str]:
        return self._answering() or []

    def _answering(self) -> list[str] | None:
        try:
            import yaml
            from card_io import REPO_ROOT
            path = REPO_ROOT / "data" / "factions.yaml"
            if not path.exists():
                return None
            factions = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("factions") or []
        except Exception:
            return None
        if not factions:
            return None
        declared = set(self.windows or [])
        return [f["name"] for f in factions
                if any((f.get("windows") or {}).get(w) == "strong" for w in declared)]

    def window_count(self) -> int:
        valid = {w["key"] for w in plan_config().get("windows", [])}
        return len([w for w in (self.windows or []) if w in valid])


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
    plan: Plan = field(default_factory=Plan)

    # ---- The Score -------------------------------------------------------------------
    @property
    def credits(self) -> int:
        return self.plan.credit_points()[0]

    @property
    def allowance(self) -> int:
        """Base budget plus everything the card pays in non-Energy currencies."""
        return self.budget + self.credits

    # kept as an alias so older callers keep working
    @property
    def earned(self) -> int:
        return self.allowance

    @property
    def reach(self) -> int | None:
        return self.plan.reach_value()

    @property
    def reach_cap(self) -> int | None:
        """None means Reach 0: nobody can answer it, so the card is not printable.
        An undeclared plan is capped at the base budget -- the original rule."""
        if self.reach is None:
            return self.budget
        caps = plan_config().get("reach_caps", {}) or {}
        multiple = caps.get(self.reach, caps.get(str(self.reach)))
        return None if multiple is None else int(self.budget * float(multiple))

    @property
    def ceiling(self) -> int:
        cap = self.reach_cap
        return 0 if cap is None else min(self.allowance, cap)

    @property
    def headroom(self) -> int:
        """Points of power still available. Negative means the card is over its Ceiling."""
        return self.ceiling - (self.base_spent + self.ascended_spent)

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
            "credits": self.credits,
            "creditBreakdown": self.plan.credit_points()[1],
            "windowCount": self.plan.window_count(),
            "reach": self.reach,
            "reachCap": self.reach_cap,
            "reachComputed": self.plan.computed_reach(),
            "reachOverridden": self.plan.reach is not None,
            "answeringFactions": self.plan.answering_factions(),
            "allowance": self.allowance,
            "earned": self.allowance,
            "ceiling": self.ceiling,
            "totalSpent": self.base_spent + self.ascended_spent,
            "headroom": self.headroom,
            "headroomSeverity": ceiling_severity(self.headroom),
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

    plan_block = card.meta.get("plan") or {}
    return Score(
        scorable=True,
        budget=budget,
        plan=Plan(credits_paid=plan_block.get("pays") or {},
                  windows=plan_block.get("windows") or [],
                  reach=plan_block.get("reach"),
                  tests=plan_block.get("tests") or {}),
        stats_total=sum(int(card.stats[k]) for k in STAT_KEYS),
        base_keyword_points=total(base["keywords"], kw_table),
        base_effect_points=total(base["effects"], ef_table),
        ascended_keyword_points=total(ascended["keywords"], kw_table),
        ascended_effect_points=total(ascended["effects"], ef_table),
        unknown_names=unknown,
    )


# --------------------------------------------------------------------------- gates

def _gate_g1(card: Card, result: Score, tolerance: int) -> list[str]:
    """G1 under The Score: total spend must not exceed the earned Ceiling.

    A card that pays nothing and claims no windows has ceiling == base budget, so this
    reduces exactly to the old rule for every card that has not opted into a plan.
    """
    if not result.scorable:
        return []
    failures = []
    has_plan = result.plan.declared

    if has_plan:
        # The Ceiling covers BOTH sides of the card -- that is what the plan bought.
        if result.reach_cap is None:
            failures.append("G1: Reach 0 — no faction can answer this card. Not printable.")
        elif result.headroom < 0:
            over = abs(result.headroom)
            capped = result.allowance > result.ceiling
            note = (f"; capped by Reach {result.reach} at {result.ceiling} "
                    f"(earned {result.allowance})") if capped else ""
            failures.append(f"G1: Impact {result.base_spent + result.ascended_spent} exceeds "
                            f"Ceiling {result.ceiling} — over by {over}{note}")
        return failures

    # No plan declared: the old two-sided budget check, unchanged.
    if abs(result.base_delta) > tolerance:
        direction = "over" if result.base_delta < 0 else "under"
        failures.append(f"G1: base side {direction} budget by {abs(result.base_delta)}")
    if card.is_ascendant and result.ascended_delta < 0:
        failures.append(f"G1: ascended side exceeds base budget x{ASCENDED_BUDGET_MULTIPLIER} "
                        f"by {abs(result.ascended_delta)} (see OQ-04)")
    return failures


def _gate_g3(card: Card) -> list[str]:
    """Ability type declared, and the keyword it claims is one the side actually has.

    This reads FIELDS. It used to regex the prose, which is how it once told Decoy that
    `[Improved Sangre Por Sangre]` "declares no ability type" while the card plainly read
    `(Fast Ability)` -- one stray colon defeated the pattern and the gate then asserted absence
    from its own failure to parse. A false negative is now structurally impossible: there is no
    sentence to misread.
    """
    failures = []
    known_types = set(ability_type_names())
    for side in ("base", "ascended"):
        face = card.side(side)
        for ability in face["abilities"]:
            name = ability.get("name") or "(unnamed)"
            declared = (ability.get("type") or "").strip()
            if not declared:
                failures.append(f"G3: ability [{name}] has no type")
            elif declared not in known_types:
                failures.append(f"G3: ability [{name}] declares unknown type '{declared}'")

            claimed = (ability.get("keyword") or "").strip()
            if claimed and claimed not in face["keywords"]:
                failures.append(f"G3: ability [{name}] claims keyword '{claimed}' but the "
                                f"{side} side does not declare it")
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
