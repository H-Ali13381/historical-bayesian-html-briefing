#!/usr/bin/env python3
"""Verify a self-contained historical/Bayesian HTML briefing artifact."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify an HTML briefing artifact")
    parser.add_argument("html", help="Path to HTML file")
    parser.add_argument("--ids", default="", help="Comma-separated required element IDs")
    parser.add_argument("--allow-external", action="store_true", help="Allow http(s) src/href references")
    args = parser.parse_args()

    path = Path(args.html).expanduser()
    result = {
        "path": str(path),
        "exists": path.exists(),
        "bytes": 0,
        "missing_ids": [],
        "nav_targets": [],
        "missing_nav_targets": [],
        "external_refs": [],
        "ok": False,
    }

    if not path.exists() or not path.is_file():
        print(json.dumps(result, indent=2))
        return 1

    text = path.read_text(encoding="utf-8", errors="replace")
    result["bytes"] = path.stat().st_size

    required_ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    result["missing_ids"] = [
        rid
        for rid in required_ids
        if f'id="{rid}"' not in text and f"id='{rid}'" not in text
    ]

    nav_targets = re.findall(r'<a\s+[^>]*href=["\']#([^"\']+)["\']', text, flags=re.I)
    result["nav_targets"] = nav_targets
    result["missing_nav_targets"] = [
        target
        for target in nav_targets
        if f'id="{target}"' not in text and f"id='{target}'" not in text
    ]

    external_refs = re.findall(r'(?:src|href)=["\'](https?://[^"\']+)["\']', text, flags=re.I)
    result["external_refs"] = external_refs

    result["ok"] = (
        result["bytes"] > 0
        and not result["missing_ids"]
        and not result["missing_nav_targets"]
        and (args.allow_external or not result["external_refs"])
    )

    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
