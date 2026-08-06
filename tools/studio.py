#!/usr/bin/env python3
"""Card Studio -- a local design workbench for the card files.

Serves a single-page workbench on localhost that reads and writes cards/**/*.md directly.
Change a stat, watch the budget meter move, hit save, and the markdown file updates in
place so `git diff` shows exactly what you changed.

    python tools/studio.py              # serve on 127.0.0.1:8765 and open a browser
    python tools/studio.py --port 9000
    python tools/studio.py --no-browser

Binds to loopback only -- nothing on your network can reach it.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import re
import sys
import threading
import webbrowser
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote, unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))

import card_io  # noqa: E402
import generate  # noqa: E402
import rules  # noqa: E402
import scoring  # noqa: E402

import yaml  # noqa: E402

PLAYTEST_LOG = card_io.REPO_ROOT / "playtests.yaml"
SNAPSHOT_DIR = card_io.REPO_ROOT / ".snapshots"

STUDIO_HTML = Path(__file__).resolve().parent / "studio.html"
FONT_DIR = Path(__file__).resolve().parent / "fonts"
MAX_BODY_BYTES = 1_000_000


def faction_briefs() -> dict:
    """Faction identity, keyed by the name cards actually use.

    Reads data/factions.yaml directly. It used to scrape docs/rulebook/03-factions.md, which
    broke the moment that document became generated -- data should never be recovered from a
    rendering of itself.
    """
    briefs = {}
    for faction in rules.load_world().factions:
        briefs[faction["name"]] = {
            "identity": (faction.get("identity") or "").strip(),
            "weakness": (faction.get("weakness") or "").strip(),
            "windows": faction.get("windows") or {},
            "windowNotes": faction.get("window_notes") or {},
            "emoji": faction.get("emoji", ""),
            "reviewed": bool(faction.get("reviewed")),
            "unique": faction.get("unique") or {},
            "never": faction.get("never") or {},
        }
    return briefs


def art_urls(card: card_io.Card) -> dict:
    """Resolved, URL-encoded links to this card's artwork, or None where nothing matched."""
    art = card.meta.get("art") or {}
    urls = {}
    for side in ("base", "ascended"):
        resolved = card_io.resolve_art(art.get(side))
        urls[side] = {
            "path": resolved,
            # /art/ is rooted at the art directory, so strip the repo-relative prefix
            "url": "/art/" + quote(resolved.removeprefix("art/")) if resolved else None,
            "ref": art.get(side),
        }
    return urls


def card_payload(card: card_io.Card) -> dict:
    return {
        "relPath": card.rel_path,
        "art": art_urls(card),
        "meta": card.meta,
        "rulesText": card.rules_text,
        "levelupCondition": card.levelup_condition,
        "ascendedText": card.ascended_text,
        "lore": card.lore,
        "designNotes": card.design_notes,
        "score": scoring.score(card).as_dict(),
    }


def write_table(filename: str, key: str, rows: list) -> None:
    path = card_io.REPO_ROOT / "data" / filename
    header = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or not line.strip():
                header.append(line)
            else:
                break
    body = yaml.safe_dump({key: rows}, sort_keys=False, allow_unicode=True, width=100)
    path.write_text("\n".join(header) + "\n" + body, encoding="utf-8")
    rules.load_world.cache_clear()
    scoring.plan_config.cache_clear()


def rule_docs() -> dict:
    """code -> what that rule checks, read straight off the rule functions.

    Every rule is named for the code it emits (f4_over_ceiling -> F4), so the Studio's
    tooltips are the code's own docstrings. Write the explanation once, in rules.py, and
    it can never drift from what the checker actually does.
    """
    docs = {}
    for rule in rules.HARD + rules.SOFT:
        text = " ".join((rule.__doc__ or "").split())
        if not text:
            continue
        # leading name parts that look like codes -- f6_f7_card_gates emits both F6 and F7
        for part in rule.__name__.split("_"):
            if not re.fullmatch(r"[fw]\d+", part):
                break
            docs[part.upper()] = text
    docs.setdefault("GAP", "A hole in the pool: something the design needs that no card fills yet.")
    docs.setdefault("RULE", "A validation rule crashed. This is a bug in tools/rules.py.")
    return docs


def findings_payload() -> list[dict]:
    rules.load_world.cache_clear()
    return [f.as_dict() for f in rules.worklist(rules.run_all())]


def playtests() -> list:
    if not PLAYTEST_LOG.exists():
        return []
    return (yaml.safe_load(PLAYTEST_LOG.read_text(encoding="utf-8")) or {}).get("games", []) or []


def bootstrap() -> dict:
    # plan_config is lru_cached and was only ever invalidated when the Studio itself wrote a
    # table, so a hand edit to data/plan-credits.yaml was invisible until the server restarted --
    # and silently so, because the stale config still answers every question asked of it.
    scoring.plan_config.cache_clear()
    world = rules.load_world()
    return {
        "cards": [card_payload(c) for c in card_io.load_all()],
        "factionData": world.factions,
        "crews": world.crews,
        "jobs": world.jobs,
        "formations": world.formations,
        "states": world.states,
        "windowKeys": list(rules.WINDOW_KEYS),
        "windowLabels": rules.WINDOW_LABELS,
        "findings": findings_payload(),
        "ruleDocs": rule_docs(),
        "playtests": playtests(),
        "usage": library_usage(),
        "keywords": card_io.load_table("keywords.yaml", "keywords"),
        "effects": card_io.load_table("effects.yaml", "effects"),
        "statuses": card_io.load_table("status-effects.yaml", "status_effects"),
        "factions": faction_briefs(),
        "lorePacketFields": list(card_io.LORE_PACKET_FIELDS),
        "statKeys": list(card_io.STAT_KEYS),
        "abilityTypes": list(scoring.ABILITY_TYPES),
        "durationPhrases": list(scoring.DURATION_PHRASES),
        "humanGates": scoring.HUMAN_ONLY_GATES,
        "plan": scoring.plan_config(),
        "constants": {
            "costMultiplier": scoring.COST_TO_BUDGET_MULTIPLIER,
            "baseAllowance": scoring.BUDGET_BASE_ALLOWANCE,
            "ascendantBonus": scoring.ASCENDANT_BUDGET_BONUS,
            "ascendedMultiplier": scoring.ASCENDED_BUDGET_MULTIPLIER,
            "tolerance": scoring.DEFAULT_TOLERANCE,
            "severityBands": list(scoring.SEVERITY_BANDS),
            "severityWorst": scoring.SEVERITY_WORST,
        },
    }


def apply_edit(payload: dict) -> dict:
    """Write an edited card back to disk and return the server's authoritative score."""
    relative = payload.get("relPath", "")
    target = (card_io.REPO_ROOT / relative).resolve()
    if not target.is_relative_to(card_io.CARDS_DIR.resolve()) or not target.is_file():
        raise ValueError(f"refusing to write outside cards/: {relative}")

    card = card_io.load(target)
    card.meta.update(payload.get("meta") or {})
    card.rules_text = payload.get("rulesText", card.rules_text)
    card.levelup_condition = payload.get("levelupCondition", card.levelup_condition)
    card.ascended_text = payload.get("ascendedText", card.ascended_text)
    card.lore = payload.get("lore", card.lore)
    card_io.save(card)
    return card_payload(card_io.load(target))


def save_faction(payload: dict) -> dict:
    world = rules.load_world()
    rows = [dict(f) for f in world.factions]
    incoming = payload.get("faction") or {}
    for index, faction in enumerate(rows):
        if faction.get("key") == incoming.get("key"):
            rows[index] = incoming
            break
    else:
        rows.append(incoming)
    write_table("factions.yaml", "factions", rows)
    run_generate()
    return {"ok": True, "factions": rows, "findings": findings_payload()}


def save_crew(payload: dict) -> dict:
    world = rules.load_world()
    rows = [dict(c) for c in world.crews]
    incoming = payload.get("crew") or {}
    for index, crew in enumerate(rows):
        if crew.get("key") == incoming.get("key"):
            rows[index] = incoming
            break
    else:
        rows.append(incoming)
    write_table("crews.yaml", "crews", rows)
    run_generate()
    return {"ok": True, "crews": rows, "findings": findings_payload()}


LIBRARY = {
    "keywords": ("keywords.yaml", "keywords"),
    "effects": ("effects.yaml", "effects"),
    "statuses": ("status-effects.yaml", "status_effects"),
}


def library_rows(kind: str) -> list:
    filename, key = LIBRARY[kind]
    path = card_io.REPO_ROOT / "data" / filename
    if not path.exists():
        return []
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get(key, []) or []


def library_usage() -> dict:
    """name -> [card names that use it]. Answers 'can I safely change this?'"""
    usage: dict[str, list] = {}
    for card in card_io.load_all():
        for side in ("base", "ascended"):
            block = card.side(side)
            for name in block["keywords"] + block["effects"]:
                usage.setdefault(name, [])
                if card.name not in usage[name]:
                    usage[name].append(card.name)
    # statuses are referenced in prose, not in frontmatter
    for status in library_rows("statuses"):
        name = status.get("name")
        if not name:
            continue
        hits = [c.name for c in card_io.load_all()
                if re.search(rf"\b{re.escape(name)}\b", f"{c.rules_text}\n{c.ascended_text}",
                             re.IGNORECASE)]
        if hits:
            usage.setdefault(name, [])
            usage[name] = sorted(set(usage[name]) | set(hits))
    return usage


def save_library_entry(payload: dict) -> dict:
    kind = payload["kind"]
    entry = payload["entry"]
    original = payload.get("originalName") or entry.get("name")
    filename, key = LIBRARY[kind]
    rows = [dict(r) for r in library_rows(kind)]
    for index, row in enumerate(rows):
        if row.get("name") == original:
            rows[index] = entry
            break
    else:
        rows.append(entry)
    write_table(filename, key, rows)
    run_generate()
    return {"ok": True, "rows": rows, "usage": library_usage(),
            "findings": findings_payload()}


def delete_library_entry(payload: dict) -> dict:
    kind, name = payload["kind"], payload["name"]
    used_by = library_usage().get(name, [])
    if used_by and not payload.get("force"):
        return {"ok": False, "blocked": True, "usedBy": used_by,
                "error": f"{len(used_by)} card(s) still use '{name}'."}
    filename, key = LIBRARY[kind]
    rows = [r for r in library_rows(kind) if r.get("name") != name]
    write_table(filename, key, rows)
    run_generate()
    return {"ok": True, "rows": rows, "usage": library_usage(),
            "findings": findings_payload()}


def rename_library_entry(payload: dict) -> dict:
    """Rename everywhere at once -- data, cards and docs. Same engine as tools/rename.py."""
    kind, old, new = payload["kind"], payload["old"], payload["new"]
    import rename as rename_tool
    pattern = re.compile(re.escape(old))
    singular = {"keywords": "keyword", "effects": "effect", "statuses": "status"}[kind]
    changed = 0
    for path in rename_tool.targets(singular):
        text = path.read_text(encoding="utf-8")
        if pattern.search(text):
            path.write_text(pattern.sub(new, text), encoding="utf-8")
            changed += 1
    rules.load_world.cache_clear()
    scoring.plan_config.cache_clear()
    scoring.keyword_points.cache_clear()
    scoring.effect_points.cache_clear()
    scoring.keyword_faction.cache_clear()
    scoring.status_names.cache_clear()
    run_generate()
    return {"ok": True, "files": changed, "rows": library_rows(kind),
            "usage": library_usage(), "findings": findings_payload()}


def create_card(payload: dict) -> dict:
    card = card_io.new_card(
        name=(payload.get("name") or "").strip(),
        faction=payload.get("faction"),
        crew=payload.get("crew") or None,
        subtype=payload.get("subtype") or "Descendant",
        cost=payload.get("cost"),
    )
    return {"ok": True, "card": card_payload(card_io.load(card.path)),
            "findings": findings_payload()}


def clone_card(payload: dict) -> dict:
    """Copy an existing card's mechanics under a new name. Lore is deliberately NOT copied --
    the Lore Packet is about a specific real person and must never be inherited."""
    source = card_io.load((card_io.REPO_ROOT / payload["relPath"]).resolve())
    clone = card_io.new_card(
        name=(payload.get("name") or f"{source.name} copy").strip(),
        faction=source.faction, crew=source.meta.get("crew"),
        subtype=source.meta.get("subtype") or "Descendant", cost=source.meta.get("cost"))
    for key in ("stats", "base", "ascended", "plan"):
        if source.meta.get(key) is not None:
            clone.meta[key] = json.loads(json.dumps(source.meta[key]))
    clone.rules_text = source.rules_text
    clone.levelup_condition = source.levelup_condition
    clone.ascended_text = source.ascended_text
    card_io.save(clone)
    return {"ok": True, "card": card_payload(card_io.load(clone.path)),
            "findings": findings_payload()}


def log_playtest(payload: dict) -> dict:
    games = playtests()
    entry = {k: payload.get(k) for k in ("when", "players", "winner", "cards", "felt_bad", "notes")}
    entry["id"] = len(games) + 1
    games.append(entry)
    PLAYTEST_LOG.write_text(
        "# Playtest log. Append-only. Written by tools/studio.py.\n"
        "# felt_bad is the important field -- it is the only data the documents cannot produce.\n\n"
        + yaml.safe_dump({"games": games}, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8")
    return {"ok": True, "playtests": games}


def take_snapshot(payload: dict) -> dict:
    """A named point-in-time record of every card's numbers, for diffing across playtests."""
    SNAPSHOT_DIR.mkdir(exist_ok=True)
    label = re.sub(r"[^\w-]+", "-", (payload.get("label") or "snapshot")).strip("-")
    state = {}
    for card in card_io.load_all():
        result = scoring.score(card)
        state[card.meta.get("slug") or card.name] = {
            "name": card.name, "cost": card.meta.get("cost"),
            "stats": card.meta.get("stats"), "impact": result.base_spent + result.ascended_spent,
            "ceiling": result.ceiling, "reach": result.reach,
        }
    path = SNAPSHOT_DIR / f"{label}.yaml"
    path.write_text(yaml.safe_dump({"label": label, "cards": state},
                                   sort_keys=False, allow_unicode=True), encoding="utf-8")
    return {"ok": True, "label": label, "cards": len(state),
            "snapshots": sorted(p.stem for p in SNAPSHOT_DIR.glob("*.yaml"))}


def run_generate() -> list[str]:
    world = rules.load_world()
    written = []
    for relative, builder in generate.TARGETS.items():
        path = card_io.REPO_ROOT / relative
        fresh = builder(world)
        if not path.exists() or path.read_text(encoding="utf-8") != fresh:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(fresh, encoding="utf-8")
            written.append(relative)
    return written


class StudioHandler(BaseHTTPRequestHandler):
    server_version = "CardStudio/1.0"
    # Chrome opens speculative connections and then sends nothing on some of them. Without a
    # timeout those sockets hold a worker thread open until the browser gives up.
    timeout = 30

    def log_message(self, fmt, *args):  # quieter than the default access log
        # args[0] is the request line for an access log, but an HTTPStatus for an error log --
        # assuming it was always a string crashed the handler on any request the base class
        # rejected, which is exactly what a browser's preconnect probe produces.
        first = str(args[0]) if args else ""
        if "api" in first:
            sys.stderr.write(f"  {first}\n")

    def handle_one_request(self) -> None:
        # Navigating away mid-response drops the socket. That is normal browser behaviour,
        # not a server fault, so it should not spray a traceback across the console.
        try:
            super().handle_one_request()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, TimeoutError):
            self.close_connection = True

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict) -> None:
        self._send(status, json.dumps(payload).encode("utf-8"), "application/json")

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            if not STUDIO_HTML.exists():
                self._send(500, b"studio.html is missing", "text/plain")
                return
            self._send(200, STUDIO_HTML.read_bytes(), "text/html; charset=utf-8")
        elif self.path.startswith("/art/"):
            self._send_art(unquote(self.path[len("/art/"):]))
        elif self.path.startswith("/fonts/"):
            self._send_font(unquote(self.path[len("/fonts/"):]))
        elif self.path == "/api/check":
            self._send_json(200, {"findings": findings_payload()})
        elif self.path == "/api/bootstrap":
            try:
                self._send_json(200, bootstrap())
            except Exception as exc:  # surface data errors in the UI, don't 500 silently
                self._send_json(500, {"error": f"{type(exc).__name__}: {exc}"})
        else:
            self._send(404, b"not found", "text/plain")

    def _send_font(self, relative: str) -> None:
        """The 20 Moves faces, self-hosted. The design system loads them from Google Fonts;
        a local workbench should not need the internet to look like itself."""
        target = (FONT_DIR / relative).resolve()
        if not target.is_relative_to(FONT_DIR.resolve()) or not target.is_file():
            self._send(404, b"no such font", "text/plain")
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "font/woff2")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "private, max-age=86400")
        self.end_headers()
        self.wfile.write(body)

    def _send_art(self, relative: str) -> None:
        target = (card_io.ART_DIR / relative).resolve()
        if not target.is_relative_to(card_io.ART_DIR.resolve()) or not target.is_file():
            self._send(404, b"no such artwork", "text/plain")
            return
        body = target.read_bytes()
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        # These are multi-megabyte photos and the editor re-renders on every keystroke --
        # without a cache header the browser would re-fetch them constantly.
        self.send_header("Cache-Control", "private, max-age=3600")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        routes = {
            "/api/card": apply_edit,
            "/api/faction": save_faction,
            "/api/crew": save_crew,
            "/api/playtest": log_playtest,
            "/api/snapshot": take_snapshot,
            "/api/library": save_library_entry,
            "/api/library/delete": delete_library_entry,
            "/api/library/rename": rename_library_entry,
            "/api/newcard": create_card,
            "/api/clonecard": clone_card,
            "/api/generate": lambda _: {"generated": generate.main.__doc__ and run_generate()},
        }
        handler = routes.get(self.path)
        if handler is None:
            self._send(404, b"not found", "text/plain")
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY_BYTES:
            self._send_json(413, {"error": "payload too large"})
            return
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            self._send_json(200, handler(payload))
        except Exception as exc:
            self._send_json(400, {"error": f"{type(exc).__name__}: {exc}"})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    try:
        cards = card_io.load_all()
    except Exception as exc:
        print(f"Could not read cards/: {exc}", file=sys.stderr)
        return 1

    url = f"http://127.0.0.1:{args.port}/"
    # Threaded, because a single-threaded server serialises every connection: one browser
    # preconnect that never sends a request blocks the page load behind it, which is the
    # "spins forever and never paints" failure. A card screen also pulls two multi-megabyte
    # images, and those should not queue behind each other either.
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(StudioHandler))
    server.daemon_threads = True
    print(f"Card Studio — {len(cards)} cards loaded")
    print(f"  {url}")
    print("  Edits save straight to cards/**/*.md. Ctrl-C to stop.\n")
    if not args.no_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
