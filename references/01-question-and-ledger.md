# Step 01 — Question and Ledger

Use this before generating any public prediction.

## Goal

Turn a vague topic into a forecastable object that can be updated, audited, scored, and rendered.

## Forecastability Gate

A question is forecastable only if it has:
- a clear event or outcome set;
- a horizon/cutoff date;
- a named resolution source;
- a resolution rule that handles ambiguity;
- a probability target: binary, multiway, or numeric range;
- a reason to forecast rather than abstain.

Reject or rewrite questions that are purely vibes, open-ended essays, unresolvable rumors, or markets whose resolution criteria do not match the intended question.

## Tetlock-Style Rewrite Pattern

Convert:

> Will AI regulation get worse?

Into:

> Will [specific regulator/institution] enact [specific rule/action] affecting [specific target] by [date], according to [resolution source]?

## Ledger First

Create the machine-readable ledger before writing prose or HTML:

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.hermes/skills/research/historical-bayesian-html-briefing}"
python "$SKILL_DIR/scripts/scaffold_forecast.py" \
  --question "Will ... by YYYY-MM-DD?" \
  --horizon-end YYYY-MM-DD \
  --resolution-source "https://..." \
  --resolution-rule "Exact rule for YES/NO/VOID" \
  --market-url "https://polymarket.com/event/..." \
  --output forecast.json
```

Then fill the JSON fields rather than improvising structure.

## Required Ledger Fields

- `forecast_id`: stable slug.
- `question`: exact public question.
- `outcome_type`: `binary`, `multiway`, or `numeric-range`.
- `horizon_start`, `horizon_end`: ISO dates.
- `resolution_source`: URL or named institution.
- `resolution_rule`: exact rule for true/false/void.
- `status`: `draft`, `active`, `frozen`, `resolved`, or `voided`.
- `probability_current`: current binary probability, if binary.
- `baselines.market`: market probability and URL when applicable.
- `priors`: reference classes and base-rate estimates.
- `evidence`: evidence items with direction and likelihood ratio when used.
- `updates`: timestamped probability history.
- `scoring`: Brier/log score fields after resolution.

## Human Approval Gate

For public forecast sites, new forecasts should require explicit human approval before becoming active. Scheduled updates can run automatically after approval when the publication workflow supports it.

Use:
- `status: draft` before approval;
- `status: active` after approval;
- `human_approved: true` in the activating update.

## Common Failures

- Forecast page is beautiful but unscorable.
- Forecast answer stops at prose and never creates a ledger or HTML artifact.
- Polymarket market question differs from the forecast question.
- Resolution source is a social-media claim instead of an authoritative source.
- Probability updates overwrite history.
- A viral market is included despite ambiguous resolution.
