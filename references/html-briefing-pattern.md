# HTML Briefing Pattern

This compatibility note preserves the old reference path.

For new forecast artifacts, use `references/04-html-briefing-pattern.md`. The newer workflow is ledger-first: validate `forecast.json`, generate the first HTML shell with `scripts/render_forecast_html.py`, hand-polish generated placeholder sections, then verify with `scripts/verify_html_briefing.py`.

Minimum required IDs for generated pages:

```text
overview,outcomes,bayes,flow,history,actors,triggers,sources,ledger
```

Verification command:

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.hermes/skills/research/historical-bayesian-html-briefing}"
python "$SKILL_DIR/scripts/verify_html_briefing.py" forecast.html --ids overview,outcomes,bayes,flow,history,actors,triggers,sources,ledger --require-forecast-data
```
