# Step 03 — Probability Modeling

Use this when converting priors and evidence into probabilities.

## Rule

Do all math with tools. Never calculate forecast probabilities, normalization, Brier scores, log scores, or deltas mentally.

## Core Commands

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.hermes/skills/research/historical-bayesian-html-briefing}"

# Smooth a base rate: (k + alpha) / (n + alpha + beta)
python "$SKILL_DIR/scripts/forecast_math.py" beta-prior --k 3 --n 12

# Apply likelihood ratios to a prior
python "$SKILL_DIR/scripts/forecast_math.py" bayes --prior 0.2857 --lr 1.3 --lr 0.85

# Normalize mutually exclusive scenario weights
python "$SKILL_DIR/scripts/forecast_math.py" normalize --weights 0.4 0.35 0.25 --labels containment reform disruption

# Compare Hermes probability to a market baseline
python "$SKILL_DIR/scripts/forecast_math.py" delta --forecast 0.42 --market 0.31

# Score after resolution
python "$SKILL_DIR/scripts/forecast_math.py" brier --p 0.42 --outcome 1
python "$SKILL_DIR/scripts/forecast_math.py" log-score --p 0.42 --outcome 1
```

## Prior / Posterior Pattern

For binary forecasts:

```text
prior p = (k + 1) / (n + 2)
odds = p / (1 - p)
posterior odds = prior odds × LR1 × LR2 × ...
posterior p = posterior odds / (1 + posterior odds)
```

Use likelihood ratios as disciplined nudges, not fake certainty.

Suggested scale:
- `0.7–0.9`: weak/moderate negative evidence.
- `1.1–1.4`: weak/moderate positive evidence.
- `1.5–2.5`: strong evidence.
- `3+`: rare, direct, high-reliability evidence.

## Scenario Probabilities

Keep these separate:
- **Event probabilities** may overlap and do not need to sum to 100%.
- **Dominant scenarios** must be mutually exclusive and should sum to 100% over a stated horizon.

Use `normalize` for scenario weights and store the normalized results in `scenarios`.

## Market Delta Discipline

A Hermes-vs-market spread is a hypothesis, not proof of edge. Record:
- market probability at timestamp;
- Hermes probability at same timestamp;
- absolute delta;
- reason for disagreement;
- liquidity caveat;
- resolution-rule mismatch, if any.

## Common Failures

- Precise percentages with no prior/evidence trail.
- Scenarios summing to 100% when they are actually overlapping events.
- Over-extremizing against Polymarket without independent evidence.
- Hiding the calculation in prose.
- Updating the number but not the ledger.
