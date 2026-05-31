# Agent Notes

This repository publishes one agent skill: `historical-bayesian-html-briefing`.

Canonical files:

- `SKILL.md` is the source of truth for the skill.
- `references/` contains public workflow checklists and lessons referenced by the skill.
- `scripts/` contains deterministic helpers for forecast math, ledger scaffolding, ledger validation, HTML rendering, and HTML verification.
- `templates/` contains public forecast-ledger schema/example files.
- `.agents/skills/historical-bayesian-html-briefing/` is a cross-client discovery mirror.

When editing the skill, update the root files first, then refresh the mirror:

```bash
mkdir -p .agents/skills/historical-bayesian-html-briefing
cp SKILL.md .agents/skills/historical-bayesian-html-briefing/
rm -rf .agents/skills/historical-bayesian-html-briefing/references .agents/skills/historical-bayesian-html-briefing/scripts .agents/skills/historical-bayesian-html-briefing/templates
cp -R references scripts templates .agents/skills/historical-bayesian-html-briefing/
```

Validation checks:

```bash
python3 -m py_compile scripts/forecast_math.py scripts/render_forecast_html.py scripts/scaffold_forecast.py scripts/validate_forecast.py scripts/verify_html_briefing.py
python3 scripts/forecast_math.py bayes --prior 0.42 --lr 1.35 --lr 0.85
python3 scripts/validate_forecast.py examples/minimal-forecast.json
python3 scripts/verify_html_briefing.py examples/minimal-briefing.html --ids overview,outcomes,bayes,flow,history,actors,triggers,sources,ledger --require-forecast-data
```

Public hygiene checks:

Run a repository secret scanner and a separate local-path scan before publishing. Keep scanner configuration outside this file or exclude this file from simple grep-style audits so the audit rules do not match themselves.

Do not add private paths, secrets, local debug notes, raw session logs, unpublished source transcripts, or client/employer-specific examples to this public package. Examples must remain synthetic or explicitly cleared for publication.
