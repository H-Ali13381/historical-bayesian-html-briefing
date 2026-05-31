# Step 04 — HTML Briefing Pattern

Use this for the default forecast package. For serious/open-ended forecasts, render and verify a self-contained HTML page unless the requester explicitly asked for a quick answer or no artifact.

## Preferred Flow

1. Start from a validated forecast JSON ledger.
2. Generate the first HTML shell with code.
3. Replace placeholder language in `flow`, `history`, `actors`, and `triggers` with forecast-specific content. The renderer's generic text is scaffolding, not a finished briefing.
4. Hand-polish the copy/design only after the machine-readable structure exists.
5. Verify anchors, required sections, embedded forecast data, and external dependencies.

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.hermes/skills/research/historical-bayesian-html-briefing}"
python "$SKILL_DIR/scripts/validate_forecast.py" forecast.json
python "$SKILL_DIR/scripts/render_forecast_html.py" forecast.json --output forecast.html
# Hand-polish forecast.html and replace generated placeholder copy before final verification.
python "$SKILL_DIR/scripts/verify_html_briefing.py" forecast.html --ids overview,outcomes,bayes,flow,history,actors,triggers,sources,ledger --require-forecast-data
```

## Required Sections

- `overview`: thesis, exact question, current probability, market baseline, no-advice caveat.
- `outcomes`: dominant mutually exclusive scenarios and/or binary forecast.
- `bayes`: base rates, likelihood ratios, model notes, and calculation trail.
- `flow`: causal chain from evidence to probability movement.
- `history`: historical analogues / reference classes with mapping limits.
- `actors`: power players, institutions, incentives, and constraints.
- `triggers`: evidence that would move probability up/down.
- `sources`: resolution source, research sources, market URL, caveats.
- `ledger`: embedded JSON or table of updates so the page is auditable.

## Design Direction

Prefer context-native editorial design: archival dossier, industrial field report, annotated map, court ledger, machine-room schematic, market terminal, or war-room briefing.

Avoid:
- generic SaaS card piles;
- neon/purple gradient defaults;
- excessive centered hero sections;
- CDN fonts/scripts unless the requester explicitly asks;
- visual drama that hides resolution criteria;
- leaving generated placeholder prose in the briefing.

## Interaction Ideas

- Scenario cards update a detail pane.
- Evidence toggles reveal how probabilities moved.
- Market-vs-Hermes delta is visually prominent.
- Update history can expand/collapse.
- Sources and caveats remain visible, not buried.

## Synthetic Example

The bundled public fixture is useful for structural validation:

`examples/minimal-briefing.html`

Use bundled examples only as synthetic structure checks. Do not publish private briefings without clearing sources, names, paths, claims, and licensing.
