#!/usr/bin/env python3
"""Render a self-contained HTML briefing from a Hermes forecast ledger JSON file."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def h(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def pct(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{100 * float(value):.1f}%"
    return "n/a"


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("ledger root must be object")
    return data


def bar(label: str, probability: Any, body: str = "") -> str:
    p = float(probability) if isinstance(probability, (int, float)) else 0.0
    width = max(0.0, min(100.0, 100 * p))
    return f'''
      <article class="card scenario-card">
        <div class="row"><strong>{h(label)}</strong><span>{pct(probability)}</span></div>
        <div class="bar"><i style="width:{width:.1f}%"></i></div>
        <p>{h(body)}</p>
      </article>'''


def render(data: dict[str, Any]) -> str:
    title = data.get("title") or data.get("question") or "Forecast Briefing"
    p = data.get("probability_current")
    baselines = data.get("baselines") if isinstance(data.get("baselines"), dict) else {}
    market = baselines.get("market") if isinstance(baselines.get("market"), dict) else {}
    market_p = market.get("probability") if isinstance(market, dict) else None
    delta = p - market_p if isinstance(p, (int, float)) and isinstance(market_p, (int, float)) else None

    scenarios = data.get("scenarios") if isinstance(data.get("scenarios"), list) else []
    if scenarios:
        scenario_html = "\n".join(bar(s.get("name", "Scenario"), s.get("probability"), s.get("description", "")) for s in scenarios if isinstance(s, dict))
    else:
        scenario_html = bar("YES / event occurs", p, "Current binary forecast probability.") + bar("NO / event does not occur", 1 - p if isinstance(p, (int, float)) else None, "Complement probability.")

    priors = data.get("priors") if isinstance(data.get("priors"), list) else []
    evidence = data.get("evidence") if isinstance(data.get("evidence"), list) else []
    updates = data.get("updates") if isinstance(data.get("updates"), list) else []

    prior_rows = "".join(
        f"<tr><td>{h(x.get('name'))}</td><td>{h(x.get('k'))}/{h(x.get('n'))}</td><td>{pct(x.get('base_rate'))}</td><td>{h(x.get('notes'))}</td></tr>"
        for x in priors if isinstance(x, dict)
    ) or '<tr><td colspan="4">No priors recorded yet.</td></tr>'

    evidence_rows = "".join(
        f"<tr><td>{h(x.get('claim'))}</td><td>{h(x.get('direction'))}</td><td>{h(x.get('lr'))}</td><td>{h(x.get('source'))}</td></tr>"
        for x in evidence if isinstance(x, dict)
    ) or '<tr><td colspan="4">No evidence items recorded yet.</td></tr>'

    update_rows = "".join(
        f"<tr><td>{h(x.get('version_id'))}</td><td>{h(x.get('timestamp'))}</td><td>{pct(x.get('probability_after', x.get('probability')))}</td><td>{pct(x.get('market_probability'))}</td><td>{h(x.get('rationale'))}</td></tr>"
        for x in updates if isinstance(x, dict)
    ) or '<tr><td colspan="5">No updates recorded yet.</td></tr>'

    raw_source_link = data.get("resolution_source")
    source_link = raw_source_link if isinstance(raw_source_link, str) else ""
    raw_market_link = market.get("url") if isinstance(market, dict) else ""
    market_link = raw_market_link if isinstance(raw_market_link, str) else ""
    embedded = json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(title)}</title>
<style>
:root {{ --bg:#11100d; --paper:#eee5d2; --ink:#211b14; --muted:#766b5b; --line:#4a3f32; --accent:#b8792d; --red:#9a3f32; --green:#4c7a4f; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--paper); font:16px/1.55 ui-serif, Georgia, serif; }}
a {{ color:#f0b45c; }}
header {{ padding:48px 7vw 24px; border-bottom:1px solid #3a3027; background:linear-gradient(135deg,#17130f,#261d15); }}
nav {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:24px; }}
nav a {{ text-decoration:none; border:1px solid #6d573d; padding:6px 10px; border-radius:999px; }}
main {{ width:min(1180px,92vw); margin:0 auto; }}
section {{ margin:28px 0; padding:24px; background:var(--paper); color:var(--ink); border:1px solid #c8b995; box-shadow:0 10px 30px #0005; }}
h1 {{ font-size:clamp(2rem,5vw,4.8rem); line-height:.95; margin:0; }}
h2 {{ margin-top:0; font-size:1.7rem; }}
.kicker {{ color:#e2a95e; text-transform:uppercase; letter-spacing:.12em; font-size:.82rem; }}
.metrics {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:14px; margin-top:24px; }}
.metric {{ background:#1d1711; color:var(--paper); border:1px solid #584734; padding:16px; }}
.metric b {{ display:block; font-size:2rem; color:#f0b45c; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:16px; }}
.card {{ background:#fff8e9; border:1px solid #d2c29f; padding:16px; }}
.row {{ display:flex; justify-content:space-between; gap:12px; align-items:center; }}
.bar {{ height:12px; background:#d8c8a8; margin:10px 0; overflow:hidden; }}
.bar i {{ display:block; height:100%; background:linear-gradient(90deg,var(--accent),#54351c); }}
table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:.92rem; }}
th,td {{ border-bottom:1px solid #d4c5a5; text-align:left; padding:8px; vertical-align:top; }}
pre {{ white-space:pre-wrap; background:#1b1712; color:#f2e6cc; padding:16px; overflow:auto; }}
.delta-pos {{ color:var(--green); }} .delta-neg {{ color:var(--red); }}
.small {{ color:var(--muted); font-size:.92rem; }}
</style>
</head>
<body>
<header id="overview">
  <div class="kicker">Hermes Forecast Ledger</div>
  <h1>{h(title)}</h1>
  <p>{h(data.get('question'))}</p>
  <nav>
    <a href="#overview">Overview</a><a href="#outcomes">Outcomes</a><a href="#bayes">Bayes</a><a href="#flow">Flow</a><a href="#history">History</a><a href="#actors">Actors</a><a href="#triggers">Triggers</a><a href="#sources">Sources</a><a href="#ledger">Ledger</a>
  </nav>
  <div class="metrics">
    <div class="metric"><span>Hermes probability</span><b>{pct(p)}</b></div>
    <div class="metric"><span>Market baseline</span><b>{pct(market_p)}</b></div>
    <div class="metric"><span>Delta</span><b class="{'delta-pos' if isinstance(delta,(int,float)) and delta>=0 else 'delta-neg'}">{pct(delta) if isinstance(delta,(int,float)) else 'n/a'}</b></div>
    <div class="metric"><span>Horizon</span><b>{h(data.get('horizon_end'))}</b></div>
  </div>
  <p class="small">Forecasting analysis only; not financial advice. Status: {h(data.get('status'))}.</p>
</header>
<main>
<section id="outcomes"><h2>Outcomes</h2><div class="grid">{scenario_html}</div></section>
<section id="bayes"><h2>Bayesian Workbench</h2><p>Use this section to show priors, likelihood ratios, and evidence movement.</p><h3>Priors</h3><table><tr><th>Name</th><th>k/n</th><th>Base rate</th><th>Notes</th></tr>{prior_rows}</table><h3>Evidence</h3><table><tr><th>Claim</th><th>Direction</th><th>LR</th><th>Source</th></tr>{evidence_rows}</table></section>
<section id="flow"><h2>Causal Flow</h2><p>Describe the chain from base rate → new evidence → probability movement. Replace this placeholder after research.</p></section>
<section id="history"><h2>Reference Classes / Historical Analogues</h2><p>List analogues by mechanism, with what maps and what does not. Do not use analogy as proof.</p></section>
<section id="actors"><h2>Actors and Incentives</h2><p>Identify power players, institutions, constraints, and incentives that can move the outcome.</p></section>
<section id="triggers"><h2>Update Triggers</h2><p>State evidence that would move the probability upward or downward on the next update.</p></section>
<section id="sources"><h2>Sources and Caveats</h2><ul><li>Resolution source: {f'<a href="{h(source_link)}">{h(source_link)}</a>' if source_link.startswith(('http://','https://')) else h(source_link)}</li><li>Market: {f'<a href="{h(market_link)}">{h(market_link)}</a>' if isinstance(market_link,str) and market_link.startswith(('http://','https://')) else h(market_link)}</li></ul><p>{h(data.get('resolution_rule'))}</p></section>
<section id="ledger"><h2>Update Ledger</h2><table><tr><th>Version</th><th>Timestamp</th><th>Hermes</th><th>Market</th><th>Rationale</th></tr>{update_rows}</table><details><summary>Embedded JSON</summary><pre>{h(json.dumps(data, indent=2, ensure_ascii=False))}</pre></details></section>
</main>
<script id="forecast-data" type="application/json">{embedded}</script>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Render self-contained HTML from a Hermes forecast ledger JSON file")
    parser.add_argument("ledger", help="Forecast ledger JSON path")
    parser.add_argument("--output", "-o", required=True, help="HTML output path")
    args = parser.parse_args()

    data = load(Path(args.ledger).expanduser())
    html_text = render(data)
    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(out), "bytes": out.stat().st_size}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
