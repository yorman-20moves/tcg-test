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
import sys
import threading
import webbrowser
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import quote, unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))

import card_io  # noqa: E402
import scoring  # noqa: E402

STUDIO_HTML = Path(__file__).resolve().parent / "studio.html"
MAX_BODY_BYTES = 1_000_000


def faction_briefs() -> dict[str, dict]:
    """Pull each faction's identity and printed weakness out of the rulebook so the
    workbench shows the canonical text rather than a second copy of it."""
    source = card_io.REPO_ROOT / "docs" / "rulebook" / "03-factions.md"
    briefs: dict[str, dict] = {}
    if not source.exists():
        return briefs

    current = None
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            heading = line.split("—")[-1].strip().removeprefix("The ").strip()
            # "Assholes / Pwners" -> "Assholes": card frontmatter uses the first name only.
            current = heading.split("/")[0].strip()
            briefs[current] = {"identity": [], "weakness": ""}
        elif current and line.startswith("> **The printed weakness:**"):
            briefs[current]["weakness"] = (line.split("*", 4)[-1]
                                           .strip(" *_>").replace("*", "").strip())
        elif current and line.startswith("> "):
            if briefs[current]["weakness"]:
                briefs[current]["weakness"] += " " + line.lstrip("> ").strip(" *_")
        elif current and line.strip() and not line.startswith(("---", "#", "|", ">")):
            briefs[current]["identity"].append(line.strip())

    for brief in briefs.values():
        brief["identity"] = " ".join(brief["identity"]).replace("**", "")
        brief["weakness"] = brief["weakness"].replace("*", "").strip()
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


def bootstrap() -> dict:
    return {
        "cards": [card_payload(c) for c in card_io.load_all()],
        "keywords": card_io.load_table("keywords.yaml", "keywords"),
        "effects": card_io.load_table("effects.yaml", "effects"),
        "statuses": card_io.load_table("status-effects.yaml", "status_effects"),
        "factions": faction_briefs(),
        "lorePacketFields": list(card_io.LORE_PACKET_FIELDS),
        "statKeys": list(card_io.STAT_KEYS),
        "abilityTypes": list(scoring.ABILITY_TYPES),
        "durationPhrases": list(scoring.DURATION_PHRASES),
        "humanGates": scoring.HUMAN_ONLY_GATES,
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


class StudioHandler(BaseHTTPRequestHandler):
    server_version = "CardStudio/1.0"

    def log_message(self, fmt, *args):  # quieter than the default access log
        if "api" in (args[0] if args else ""):
            sys.stderr.write(f"  {args[0]}\n")

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
        elif self.path == "/api/bootstrap":
            try:
                self._send_json(200, bootstrap())
            except Exception as exc:  # surface data errors in the UI, don't 500 silently
                self._send_json(500, {"error": f"{type(exc).__name__}: {exc}"})
        else:
            self._send(404, b"not found", "text/plain")

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
        if self.path != "/api/card":
            self._send(404, b"not found", "text/plain")
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY_BYTES:
            self._send_json(413, {"error": "payload too large"})
            return
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            self._send_json(200, apply_edit(payload))
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
    server = HTTPServer(("127.0.0.1", args.port), partial(StudioHandler))
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
