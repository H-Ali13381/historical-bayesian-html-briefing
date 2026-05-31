# Competitive Strategy Forecasts

Use this reference when the requester asks questions like “what happens if I compete with X?”, “can my project beat Y?”, or “what is the expected outcome if I pursue this wedge?”

## Frame the forecast as conditional strategy, not vibes

Split the vague competitive question into at least two forecastable claims:

1. **Head-to-head outcome** — can the challenger beat the incumbent/lab/company on the incumbent’s strongest axis?
2. **Diagonal/niche outcome** — can the challenger win a differentiated wedge adjacent to the incumbent?
3. **Personal/reputational outcome** — even if the company/product outcome fails, does the attempt produce career capital, proof-of-work, collaborators, or a job/funding path?

These are usually different probabilities. Do not collapse them into one “will I succeed?” number.

## Useful ledger shape

For a non-market strategic forecast, the resolution source can be “project public artifacts and observable adoption metrics” if there is no market or institution. Define concrete success criteria, for example:

- recurring external users or paid/pilot users;
- GitHub stars/forks/downloads plus evidence of non-user installs;
- revenue, partnership, grant, acquisition, or job-offer outcome directly attributable to the project;
- public demos that generate inbound interest from credible users/builders.

Keep `status: draft` unless the requester explicitly wants to publish or track it as an active forecast.

## Scenario pattern

Use mutually exclusive scenario buckets such as:

- stalls / remains personal-only;
- strong personal or OSS tool, modest attention;
- niche product wedge;
- reputational/career win;
- serious startup win;
- true head-to-head competitor.

Normalize these with `forecast_math.py normalize` and keep them separate from binary event probabilities.

## Evidence checklist

Positive evidence:

- already-working substrate or prototype;
- differentiated wedge the incumbent is unlikely to prioritize;
- user-owned/local/sovereign angle;
- existing demos that are hard for generic products to fake;
- compounding procedural knowledge, skills, or workflow library.

Negative evidence:

- incumbent’s capital, talent, distribution, and model access;
- product polish/latency gaps;
- crowded developer-tool market;
- lack of external users or public proof;
- execution risk from solo/small-team scope.

## Output style

Be blunt about the losing axis. Then identify the winnable axis.

Good structure:

- “Head-to-head on X: very unlikely.”
- “Diagonal wedge on Y: plausible.”
- “Expected value: mostly proof-of-work/reputation unless external adoption appears.”
- “Strategic recommendation: avoid competing on the incumbent’s strength; compete where the challenger has asymmetric substrate/context.”

Label the result as forecasting/strategic analysis, not financial advice.