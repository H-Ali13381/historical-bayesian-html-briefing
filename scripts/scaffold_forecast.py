#!/usr/bin/env python3
"""Create a machine-readable Hermes forecast ledger JSON file."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:80] or "forecast"


def parse_probability(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    raw = value.strip()
    if raw.endswith("%"):
        p = float(raw[:-1]) / 100.0
    else:
        p = float(raw)
        if p > 1 and p <= 100:
            p = p / 100.0
    if not 0 <= p <= 1:
        raise argparse.ArgumentTypeError(f"probability must be in [0,1] or [0,100%], got {value!r}")
    return p


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_ledger(args: argparse.Namespace) -> dict[str, Any]:
    title = args.title or args.question
    forecast_id = args.forecast_id or slugify(title)
    p = parse_probability(args.probability)
    market_p = parse_probability(args.market_probability)
    timestamp = args.timestamp or now_utc()

    updates: list[dict[str, Any]] = []
    if p is not None:
        updates.append(
            {
                "version_id": "v001",
                "timestamp": timestamp,
                "probability": p,
                "probability_before": None,
                "probability_after": p,
                "market_probability": market_p,
                "rationale": args.rationale or "Initial scaffold forecast; replace with evidence-backed rationale.",
                "sources_checked": [],
                "evidence_delta": [],
                "model": args.model,
                "human_approved": args.human_approved,
            }
        )

    return {
        "schema_version": "1.0",
        "forecast_id": forecast_id,
        "title": title,
        "question": args.question,
        "outcome_type": args.outcome_type,
        "horizon_start": args.horizon_start or date.today().isoformat(),
        "horizon_end": args.horizon_end,
        "resolution_source": args.resolution_source,
        "resolution_rule": args.resolution_rule or "TODO: specify exact YES/NO/VOID rule before publication.",
        "status": args.status,
        "probability_current": p,
        "baselines": {
            "market": {
                "platform": args.market_platform,
                "url": args.market_url,
                "probability": market_p,
                "timestamp": timestamp if market_p is not None else None,
                "liquidity": None,
                "volume": None,
                "notes": "Verify market wording, liquidity, and resolution criteria before treating as a baseline.",
            },
            "naive": {"probability": 0.5},
            "base_rate": {"probability": None, "notes": "Fill after outside-view/base-rate pass."},
        },
        "priors": [],
        "evidence": [],
        "scenarios": [],
        "updates": updates,
        "scoring": {
            "primary": "brier",
            "secondary": "log_score",
            "baselines": ["market", "base_rate", "naive_50"],
            "outcome": None,
            "resolved_at": None,
            "brier": None,
            "log_score": None,
        },
        "public_notes": args.public_notes or "Forecasting analysis only; not financial advice.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a Hermes forecast ledger JSON file")
    parser.add_argument("--question", required=True, help="Exact forecast question")
    parser.add_argument("--horizon-end", required=True, help="ISO date cutoff/resolution horizon")
    parser.add_argument("--resolution-source", required=True, help="URL or institution used for resolution")
    parser.add_argument("--resolution-rule", default="", help="Exact YES/NO/VOID rule")
    parser.add_argument("--title", default="", help="Display title; defaults to question")
    parser.add_argument("--forecast-id", default="", help="Stable slug; defaults from title/question")
    parser.add_argument("--outcome-type", default="binary", choices=["binary", "multiway", "numeric-range"])
    parser.add_argument("--horizon-start", default="", help="ISO date; defaults to today")
    parser.add_argument("--status", default="draft", choices=["draft", "active", "frozen", "resolved", "voided"])
    parser.add_argument("--probability", default=None, help="Current probability as 0-1 or percent")
    parser.add_argument("--market-probability", default=None, help="Market baseline probability as 0-1 or percent")
    parser.add_argument("--market-url", default=None, help="Prediction-market URL, if any")
    parser.add_argument("--market-platform", default="Polymarket", help="Market platform name")
    parser.add_argument("--timestamp", default="", help="ISO timestamp for initial update; defaults to now UTC")
    parser.add_argument("--rationale", default="", help="Initial update rationale")
    parser.add_argument("--model", default=None, help="Model or method name")
    parser.add_argument("--human-approved", action="store_true", help="Mark initial update as human-approved")
    parser.add_argument("--public-notes", default="", help="Public caveat/notes")
    parser.add_argument("--output", "-o", default="", help="Write JSON to this path; stdout if omitted")
    parser.add_argument("--dry-run", action="store_true", help="Print JSON but do not write output file")
    args = parser.parse_args()

    ledger = build_ledger(args)
    text = json.dumps(ledger, indent=2, ensure_ascii=False) + "\n"

    if args.output and not args.dry_run:
        path = Path(args.output).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(json.dumps({"ok": True, "path": str(path), "forecast_id": ledger["forecast_id"]}, indent=2))
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
