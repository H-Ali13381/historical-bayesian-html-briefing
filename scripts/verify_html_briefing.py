#!/usr/bin/env python3
"""Verify a self-contained historical/Bayesian HTML briefing artifact."""

from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


PLACEHOLDER_PATTERNS = [
    "Replace this placeholder",
    "Use this section to show",
    "Describe the chain from base rate",
    "List analogues by mechanism",
    "Identify power players",
    "State evidence that would move",
    "No priors recorded yet",
    "No evidence items recorded yet",
]

FORECAST_DATA_REQUIRED_KEYS = [
    "schema_version",
    "forecast_id",
    "question",
    "outcome_type",
    "horizon_end",
    "resolution_source",
    "resolution_rule",
    "status",
    "updates",
]


class BriefingHTMLParser(HTMLParser):
    """Small HTML parser for structural checks without external dependencies."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.nav_targets: list[str] = []
        self.external_assets: list[str] = []
        self.external_links: list[str] = []
        self._in_forecast_data = False
        self._forecast_data_chunks: list[str] = []

    @property
    def forecast_data_text(self) -> str:
        return "".join(self._forecast_data_chunks).strip()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr = {name.lower(): value or "" for name, value in attrs}

        element_id = attr.get("id")
        if element_id:
            self.ids.add(element_id)

        href = attr.get("href", "")
        if tag == "a" and href.startswith("#"):
            self.nav_targets.append(href[1:])
        elif href.startswith(("http://", "https://")):
            self.external_links.append(href)

        src = attr.get("src", "")
        if src.startswith(("http://", "https://")):
            self.external_assets.append(src)

        if (
            tag == "script"
            and attr.get("id") == "forecast-data"
            and attr.get("type", "").lower() == "application/json"
        ):
            self._in_forecast_data = True
            self._forecast_data_chunks = []

    def handle_data(self, data: str) -> None:
        if self._in_forecast_data:
            self._forecast_data_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._in_forecast_data:
            self._in_forecast_data = False


def parse_forecast_data(raw: str) -> tuple[bool, dict[str, Any] | None, list[str]]:
    if not raw:
        return False, None, ["forecast-data script is empty"]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return False, None, [f"forecast-data JSON is invalid: {exc}"]
    if not isinstance(data, dict):
        return False, None, ["forecast-data JSON root must be an object"]
    missing = [key for key in FORECAST_DATA_REQUIRED_KEYS if key not in data]
    if missing:
        return False, data, [f"forecast-data missing required keys: {', '.join(missing)}"]
    return True, data, []


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify an HTML briefing artifact")
    parser.add_argument("html", help="Path to HTML file")
    parser.add_argument("--ids", default="", help="Comma-separated required element IDs")
    parser.add_argument("--allow-external-assets", action="store_true", help="Allow http(s) src references")
    parser.add_argument("--disallow-external-links", action="store_true", help="Fail on http(s) href links as well as assets")
    parser.add_argument("--require-forecast-data", action="store_true", help="Require valid <script id='forecast-data' type='application/json'>")
    parser.add_argument("--allow-placeholders", action="store_true", help="Allow generated placeholder copy to remain in the briefing")
    args = parser.parse_args()

    path = Path(args.html).expanduser()
    result: dict[str, Any] = {
        "path": str(path),
        "exists": path.exists(),
        "bytes": 0,
        "missing_ids": [],
        "nav_targets": [],
        "missing_nav_targets": [],
        "external_assets": [],
        "external_links": [],
        "forecast_data_present": False,
        "forecast_data_valid": False,
        "forecast_data_errors": [],
        "forecast_data_summary": {},
        "placeholder_hits": [],
        "ok": False,
    }

    if not path.exists() or not path.is_file():
        print(json.dumps(result, indent=2))
        return 1

    text = path.read_text(encoding="utf-8", errors="replace")
    result["bytes"] = path.stat().st_size

    html_parser = BriefingHTMLParser()
    html_parser.feed(text)
    html_parser.close()

    required_ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    result["missing_ids"] = [rid for rid in required_ids if rid not in html_parser.ids]
    result["nav_targets"] = html_parser.nav_targets
    result["missing_nav_targets"] = [target for target in html_parser.nav_targets if target not in html_parser.ids]
    result["external_assets"] = html_parser.external_assets
    result["external_links"] = html_parser.external_links

    result["forecast_data_present"] = bool(html_parser.forecast_data_text)
    if html_parser.forecast_data_text:
        valid, data, errors = parse_forecast_data(html_parser.forecast_data_text)
        result["forecast_data_valid"] = valid
        result["forecast_data_errors"] = errors
        if isinstance(data, dict):
            result["forecast_data_summary"] = {
                "forecast_id": data.get("forecast_id"),
                "status": data.get("status"),
                "probability_current": data.get("probability_current"),
                "updates": len(data.get("updates", [])) if isinstance(data.get("updates"), list) else None,
            }

    result["placeholder_hits"] = [pattern for pattern in PLACEHOLDER_PATTERNS if pattern.lower() in text.lower()]

    result["ok"] = (
        result["bytes"] > 0
        and not result["missing_ids"]
        and not result["missing_nav_targets"]
        and (args.allow_external_assets or not result["external_assets"])
        and (not args.disallow_external_links or not result["external_links"])
        and (not args.require_forecast_data or (result["forecast_data_present"] and result["forecast_data_valid"]))
        and (args.allow_placeholders or not result["placeholder_hits"])
    )

    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
