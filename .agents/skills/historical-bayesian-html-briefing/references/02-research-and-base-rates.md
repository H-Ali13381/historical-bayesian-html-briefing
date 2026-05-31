# Step 02 — Research and Base Rates

Use this after the ledger exists and before assigning the headline probability.

## Goal

Build an outside-view-first evidence packet. The narrative should explain the probability, not invent it.

## Source Stack

Use sources in this order when relevant:

1. **Resolution source** — the institution or rule that will determine outcome.
2. **Market source** — Polymarket/Gamma/CLOB price, liquidity, volume, and exact market wording.
3. **Base-rate sources** — historical frequency, analogous events, prior market families, prior institutional cycles.
4. **Current evidence** — recent news, filings, official statements, data releases.
5. **Opposing-view evidence** — strongest evidence against the preferred direction.
6. **Meta evidence** — incentives, selection effects, market microstructure, source reliability.

## CHAMPS KNOW Checklist

Use the Tetlock-derived checklist explicitly:

- **C — Comparison classes:** What is the reference class and base rate?
- **H — Hunt:** What high-signal evidence was checked?
- **A — Adjust:** What evidence moves probability up/down?
- **M — Models:** What do markets, simple models, polls, or historical rates imply?
- **P — Post-mortem hook:** What would make this forecast wrong?
- **S — Select effort:** Is this question worth public forecasting?
- **K — Power players:** Who can directly change the outcome?
- **N — Norms/institutions:** Which procedures and rules matter?
- **O — Other views:** What is the strongest counter-case?
- **W — Wildcards:** What low-probability breakpoints matter?

## Base-Rate Notes

For every base rate, record:
- numerator and denominator, if available;
- source and date;
- why the reference class is relevant;
- what does not map;
- whether the rate is likely stale, selected, or noisy.

If no defensible base rate exists, state that directly and use a wider uncertainty range.

## Polymarket-Specific Checks

Before using a market price as a baseline:
- verify exact market wording;
- parse outcome prices correctly;
- record timestamp;
- record liquidity/volume/open interest when available;
- compare resolution source/rule to the Hermes forecast question;
- flag thin, stale, or manipulable markets.

## Output Packet

Add compact entries to the ledger:

```json
"priors": [
  {"name": "reference class", "k": 3, "n": 12, "base_rate": 0.2857, "notes": "..."}
],
"evidence": [
  {"claim": "...", "direction": "up", "lr": 1.25, "source": "...", "notes": "..."}
]
```

## Common Failures

- Starting from the news hook instead of the outside view.
- Using market price as the forecast without independent reasoning.
- Treating a historical analogy as proof rather than a reference class.
- Omitting disconfirming evidence.
- Letting a pretty story dominate a weak base rate.
