---
name: historical-bayesian-html-briefing
description: "Use when a user wants a serious historically grounded probabilistic forecast, Bayesian/Tetlock-style scenario odds, market deltas, forecast ledgers, crisis/strategy forecasts, or a shareable self-contained HTML briefing for complex social, technical, economic, geopolitical, market-resolution, or personal-strategy questions."
version: 1.2.0
author: Skill package maintainers
license: Apache-2.0
metadata:
  hermes:
    tags: [research, synthesis, forecasting, superforecasting, bayesian-analysis, prediction-markets, forecast-ledger, html-artifact]
    category: research
    related_skills: [research, academic-research-synthesis, polymarket, frontend-design]
---

# Historical Bayesian HTML Briefing

Use this for serious prediction work: resolvable questions, explicit probabilities, visible base rates, evidence updates, market comparisons, versioned ledgers, and a complete forecast package.

## Default Deliverable Contract

For any serious or open-ended forecast, produce the full package by default unless the requester explicitly asks for a quick answer, no artifact, or no HTML. Do not decide on your own to skip the artifact because the question is broad.

A complete package means:
- a forecastable question or scenario set with horizon and resolution rule;
- a machine-readable JSON ledger saved to disk;
- outside-view/base-rate evidence and current sources;
- probabilities computed or normalized with `scripts/forecast_math.py` or another tool, never mentally;
- `scripts/validate_forecast.py` run successfully on the ledger;
- a self-contained HTML briefing rendered with `scripts/render_forecast_html.py`, hand-polished if needed, then verified with `scripts/verify_html_briefing.py`;
- a final terminal summary that includes headline probabilities, validation status, and exact file paths.

If the requester explicitly opts out of HTML or wants only a quick gut check, say that the full package was intentionally skipped and do not pretend the forecast is ledger-backed.

## Workflow

Follow the steps in order; load only the reference needed for the current step. The workflow is not complete until the ledger and HTML verification commands have succeeded, unless the requester explicitly opted out.

For strategic/product competition forecasts ("what are my odds against X?", "what if I achieve every goal?"), also use `references/strategic-competition-forecasting.md` to split head-to-head, diagonal wedge, reputation, startup, and personal-only outcomes.

When maintaining or auditing this skill's default artifact behavior, consult `references/strict-html-default-lesson.md`; it captures the failure mode where a serious forecast stopped at prose and the corrected objective function for package-first delivery.

When optimizing this skill itself, consult `references/package-first-skill-optimization.md`; it defines the package-first objective function, trigger eval shape, score-only selection rule, and the pitfall that prose success can hide artifact failure.

1. Define the forecast question and ledger object: `references/01-question-and-ledger.md`.
2. Gather outside-view/base-rate evidence: `references/02-research-and-base-rates.md`.
3. Compute probabilities with code: `references/03-probability-modeling.md` and `scripts/forecast_math.py`.
4. Validate the machine-readable ledger: `scripts/validate_forecast.py`.
5. Render the HTML artifact: `references/04-html-briefing-pattern.md`, `scripts/render_forecast_html.py`, then hand-polish any placeholder sections.
6. Verify the final HTML with `scripts/verify_html_briefing.py` and confirm there are no accidental external assets.
7. Update, score, and post-mortem resolved forecasts: `references/05-updates-scoring-and-calibration.md`.

For “what happens if I compete with X?” strategy questions, also use `references/competitive-strategy-forecast.md`: split head-to-head, diagonal/niche, and reputational outcomes instead of collapsing them into one success probability.

## Hard Rules

- Use tools/scripts for arithmetic, Bayesian updates, normalization, Brier/log scores, and market deltas. Do not do forecast math mentally.
- Preserve forecast history. New evidence creates a new update entry; it does not overwrite the old belief state.
- Treat prediction-market prices as baselines and attention signals, not truth.
- Keep overlapping event probabilities separate from mutually exclusive scenario probabilities.
- Label outputs as forecasting/analysis, not financial advice.
- Do not stop after a prose forecast for serious/open-ended questions. Prose is the summary of the package, not the deliverable.
- HTML is default, not optional, when this skill is invoked for serious forecasting. The requester may opt out; the agent may not silently opt out.
- Keep new forecasts in `status: draft` with `human_approved: false` unless the requester explicitly asks to publish/activate the forecast. Do not infer approval just because the requester requested a forecast package.
- After any post-render ledger edit, either re-render the HTML from the ledger or explicitly synchronize the embedded `<script id="forecast-data">` JSON and visible status fields before verification. A verified page can still be semantically stale if the embedded ledger was not updated.
- When an evidence item depends on multiple URLs, do not put a human phrase like `url1 and url2` inside one `href`. Split into separate links in the polished HTML or store separate source fields/notes so verification does not bless malformed links.
- If the rendered HTML still contains generator placeholders, hand-polish those sections before verification and final delivery.
- Before claiming completion, run both ledger validation and HTML verification and report the real results.

## Script Quick Start

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.hermes/skills/research/historical-bayesian-html-briefing}"
python "$SKILL_DIR/scripts/scaffold_forecast.py" --question "Will ... by YYYY-MM-DD?" --horizon-end YYYY-MM-DD --resolution-source URL --output forecast.json
python "$SKILL_DIR/scripts/forecast_math.py" bayes --prior 0.35 --lr 1.2 --lr 0.8
python "$SKILL_DIR/scripts/validate_forecast.py" forecast.json
python "$SKILL_DIR/scripts/render_forecast_html.py" forecast.json --output forecast.html
# Hand-polish forecast.html so flow/history/actors/triggers contain forecast-specific content.
python "$SKILL_DIR/scripts/verify_html_briefing.py" forecast.html --ids overview,outcomes,bayes,flow,history,actors,triggers,sources,ledger --require-forecast-data
```

## Verification

Before claiming completion: validate the ledger, verify generated HTML, confirm no accidental external assets, check that no placeholder copy remains in required sections, and if saved in a private knowledge base, update and read back that knowledge base's index/log according to its convention.

Completion line should include:
- JSON ledger path and validation `ok` result;
- HTML path and verification `ok` result;
- required IDs present: `overview,outcomes,bayes,flow,history,actors,triggers,sources,ledger`;
- whether the forecast is `draft`, `active`, `frozen`, `resolved`, or intentionally quick/no-artifact.
