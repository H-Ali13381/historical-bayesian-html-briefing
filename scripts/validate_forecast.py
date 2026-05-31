#!/usr/bin/env python3
"""Validate a Hermes forecast ledger JSON file."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

REQUIRED = [
    "schema_version",
    "forecast_id",
    "question",
    "outcome_type",
    "horizon_start",
    "horizon_end",
    "resolution_source",
    "resolution_rule",
    "status",
    "updates",
]
REQUIRED_STRINGS = [
    "schema_version",
    "forecast_id",
    "question",
    "outcome_type",
    "horizon_start",
    "horizon_end",
    "resolution_source",
    "resolution_rule",
    "status",
]
STATUSES = {"draft", "active", "frozen", "resolved", "voided"}
OUTCOME_TYPES = {"binary", "multiway", "numeric-range"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Ledger root must be a JSON object")
    return data


def parse_date_value(value: Any) -> date | datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    s = value.replace("Z", "+00:00")
    try:
        if "T" in s:
            return datetime.fromisoformat(s)
        return date.fromisoformat(s)
    except ValueError:
        return None


def parse_date_like(value: Any) -> bool:
    return parse_date_value(value) is not None


def check_prob(name: str, value: Any, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        errors.append(f"{name} must be a number in [0,1] or null")
    elif not 0 <= float(value) <= 1:
        errors.append(f"{name}={value!r} outside [0,1]")


def check_nonempty_string(name: str, data: dict[str, Any], errors: list[str]) -> None:
    value = data.get(name)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{name} must be a nonempty string")


def validate(data: dict[str, Any], allow_unnormalized: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing required field: {key}")

    for key in REQUIRED_STRINGS:
        if key in data:
            check_nonempty_string(key, data, errors)

    if data.get("outcome_type") not in OUTCOME_TYPES:
        errors.append(f"outcome_type must be one of {sorted(OUTCOME_TYPES)}")
    if data.get("status") not in STATUSES:
        errors.append(f"status must be one of {sorted(STATUSES)}")

    parsed_dates: dict[str, date | datetime] = {}
    for key in ["horizon_start", "horizon_end"]:
        if key in data:
            parsed = parse_date_value(data.get(key))
            if parsed is None:
                errors.append(f"{key} must be ISO date/datetime")
            else:
                parsed_dates[key] = parsed
    if {"horizon_start", "horizon_end"} <= parsed_dates.keys():
        start = parsed_dates["horizon_start"]
        end = parsed_dates["horizon_end"]
        start_key = start.date() if isinstance(start, datetime) else start
        end_key = end.date() if isinstance(end, datetime) else end
        if end_key < start_key:
            errors.append("horizon_end must be on or after horizon_start")

    resolution_rule = data.get("resolution_rule")
    if isinstance(resolution_rule, str) and resolution_rule.strip().startswith("TODO"):
        warnings.append("resolution_rule is still TODO")

    resolution_source = data.get("resolution_source")
    if isinstance(resolution_source, str) and resolution_source.startswith(("http://", "https://")) and " " in resolution_source:
        errors.append("resolution_source URL must not contain spaces; split multiple sources into separate fields/notes")

    check_prob("probability_current", data.get("probability_current"), errors)

    baselines = data.get("baselines") or {}
    if isinstance(baselines, dict):
        market = baselines.get("market") or {}
        if market:
            if not isinstance(market, dict):
                errors.append("baselines.market must be an object when present")
            else:
                check_prob("baselines.market.probability", market.get("probability"), errors)
                market_url = market.get("url")
                if market_url is not None and not isinstance(market_url, str):
                    errors.append("baselines.market.url must be a string or null")
                if isinstance(market_url, str) and " " in market_url and market_url.startswith(("http://", "https://")):
                    errors.append("baselines.market.url must not contain spaces; split multiple URLs into notes/sources")
                if market_url and market.get("probability") is None:
                    warnings.append("market URL present but market probability is null")
    else:
        errors.append("baselines must be an object")

    updates = data.get("updates")
    human_approved_seen = False
    if not isinstance(updates, list):
        errors.append("updates must be a list")
    else:
        if not updates:
            warnings.append("updates is empty; public forecasts should have at least one update")
        seen_versions: set[str] = set()
        for i, upd in enumerate(updates):
            if not isinstance(upd, dict):
                errors.append(f"updates[{i}] must be an object")
                continue
            version = upd.get("version_id")
            if not version:
                warnings.append(f"updates[{i}] missing version_id")
            elif not isinstance(version, str):
                errors.append(f"updates[{i}].version_id must be a string")
            elif version in seen_versions:
                errors.append(f"duplicate update version_id: {version}")
            else:
                seen_versions.add(version)
            if not parse_date_like(upd.get("timestamp")):
                errors.append(f"updates[{i}].timestamp must be ISO datetime")
            for key in ["probability", "probability_before", "probability_after", "market_probability"]:
                if key in upd:
                    check_prob(f"updates[{i}].{key}", upd.get(key), errors)
            rationale = upd.get("rationale")
            if not isinstance(rationale, str) or not rationale.strip():
                warnings.append(f"updates[{i}] missing rationale")
            if "human_approved" in upd and not isinstance(upd.get("human_approved"), bool):
                errors.append(f"updates[{i}].human_approved must be boolean when present")
            human_approved_seen = human_approved_seen or upd.get("human_approved") is True

    if data.get("status") == "active" and not human_approved_seen:
        errors.append("active forecasts require at least one update with human_approved: true")

    scenarios = data.get("scenarios") or []
    if not isinstance(scenarios, list):
        errors.append("scenarios must be a list")
    elif scenarios:
        probs = []
        for i, scenario in enumerate(scenarios):
            if not isinstance(scenario, dict):
                errors.append(f"scenarios[{i}] must be an object")
                continue
            check_prob(f"scenarios[{i}].probability", scenario.get("probability"), errors)
            if isinstance(scenario.get("probability"), (int, float)) and not isinstance(scenario.get("probability"), bool):
                probs.append(float(scenario["probability"]))
        if probs and not allow_unnormalized and abs(sum(probs) - 1.0) > 0.01:
            errors.append(f"scenario probabilities sum to {sum(probs):.4f}, expected about 1.0")

    notes = str(data.get("public_notes", "")).lower()
    if "financial advice" not in notes and (baselines if isinstance(baselines, dict) else {}).get("market"):
        warnings.append("public_notes should include a no-financial-advice caveat for market-linked forecasts")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Hermes forecast ledger JSON file")
    parser.add_argument("json_path", help="Forecast ledger JSON path")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failure")
    parser.add_argument("--allow-unnormalized", action="store_true", help="Allow scenario probabilities that do not sum to 1")
    args = parser.parse_args()

    path = Path(args.json_path).expanduser()
    result: dict[str, Any] = {"path": str(path), "exists": path.exists(), "ok": False, "errors": [], "warnings": []}
    if not path.exists():
        result["errors"] = ["file does not exist"]
        print(json.dumps(result, indent=2))
        return 1

    try:
        data = load_json(path)
        result.update(validate(data, allow_unnormalized=args.allow_unnormalized))
    except Exception as exc:  # keep CLI diagnostics JSON-shaped
        result["errors"] = [f"failed to parse/validate: {exc}"]
        result["ok"] = False

    if args.strict and result.get("warnings"):
        result["ok"] = False
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
