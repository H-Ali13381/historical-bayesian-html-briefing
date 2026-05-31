# Step 05 — Updates, Scoring, and Calibration

Use this when maintaining daily forecasts or resolving old forecasts.

## Update Discipline

A daily update appends a new entry. It never silently rewrites the old number.

Each update should include:
- timestamp;
- version id;
- probability before and after;
- market probability at the same timestamp, if available;
- sources checked;
- evidence delta;
- reason for movement;
- model/skill version when relevant;
- human override / approval flag.

## Freeze and Resolve

Before outcome resolution:
- freeze if the market closes, source stops updating, or the cutoff passes;
- record final pre-resolution probability;
- preserve initial and time-weighted views separately.

After resolution:
- record outcome: `0`, `1`, or void/ambiguous;
- score Brier and log score with `forecast_math.py`;
- score the market baseline at comparable timestamps;
- write a short post-mortem for large misses or strong deltas.

## Scoring Commands

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.hermes/skills/research/historical-bayesian-html-briefing}"
python "$SKILL_DIR/scripts/forecast_math.py" brier --p 0.42 --outcome 1
python "$SKILL_DIR/scripts/forecast_math.py" log-score --p 0.42 --outcome 1
```

## Recommended Public Scorecard

Show:
- initial forecast score;
- final pre-resolution score;
- time-weighted score, when available;
- market baseline score;
- naive 50% baseline;
- Brier score;
- log score;
- calibration by bucket;
- performance by topic and horizon;
- voided/ambiguous count.

## ELO-Like Rating

If the site shows an ELO-like public score, derive it from proper scoring rules and baseline comparisons. Do not treat ELO as the underlying truth.

## Post-Mortem Template

```text
Question:
Outcome:
Initial probability:
Final probability:
Market baseline:
Score delta:
What was right:
What was wrong:
Evidence missed:
Calibration lesson:
Pipeline change:
```

## Common Failures

- Scoring only final forecasts and hiding early overconfidence.
- Voiding awkward misses without a public ambiguity policy.
- Comparing Hermes to market prices from different timestamps.
- Publishing an ELO number without underlying Brier/log/calibration data.
