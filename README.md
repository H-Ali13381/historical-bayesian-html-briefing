# Historical Bayesian HTML Briefing

A shareable Hermes agent skill for serious historically grounded probabilistic forecasting: forecast ledgers, Bayesian/Tetlock-style updates, market deltas, scenario odds, and self-contained HTML briefing artifacts.

It is designed for analyses that need:

- forecastable questions with horizons and resolution rules;
- mechanism-based historical analogies rather than decorative metaphors;
- explicit Bayesian/probabilistic calculation with tool-backed math;
- clear separation between overlapping event probabilities and mutually exclusive scenarios;
- update triggers that say what evidence would move the odds;
- a machine-readable JSON ledger plus a polished HTML dossier by default for serious forecasts unless the requester explicitly opts out.

## What's included

```text
.
├── SKILL.md
├── references/
│   ├── 01-question-and-ledger.md
│   ├── 02-research-and-base-rates.md
│   ├── 03-probability-modeling.md
│   ├── 04-html-briefing-pattern.md
│   ├── 05-updates-scoring-and-calibration.md
│   ├── competitive-strategy-forecast.md
│   ├── html-briefing-pattern.md
│   ├── package-first-skill-optimization.md
│   ├── strategic-competition-forecasting.md
│   └── strict-html-default-lesson.md
├── scripts/
│   ├── forecast_math.py
│   ├── render_forecast_html.py
│   ├── scaffold_forecast.py
│   ├── validate_forecast.py
│   └── verify_html_briefing.py
├── templates/
│   ├── forecast-ledger.example.json
│   └── forecast-ledger.schema.json
├── examples/
│   ├── minimal-forecast.json
│   └── minimal-briefing.html
├── .agents/skills/historical-bayesian-html-briefing/
│   ├── SKILL.md
│   ├── references/
│   ├── scripts/
│   └── templates/
├── AGENTS.md
├── LICENSE
└── README.md
```

The root `SKILL.md` is canonical. The `.agents/skills/...` copy is a mirror for clients that discover skills from that layout.

## Install in Hermes

From the repository root:

```bash
TARGET="$HOME/.hermes/skills/research/historical-bayesian-html-briefing"
mkdir -p "$TARGET"
cp SKILL.md "$TARGET/"
cp -R references scripts templates "$TARGET/"
```

Then start a fresh Hermes session or refresh the skill index according to your local setup.

## Basic workflow

```bash
SKILL_DIR="$HOME/.hermes/skills/research/historical-bayesian-html-briefing"
python "$SKILL_DIR/scripts/scaffold_forecast.py" \
  --question "Will the specified event happen by YYYY-MM-DD?" \
  --horizon-end YYYY-MM-DD \
  --resolution-source "https://example.com/resolution-source" \
  --resolution-rule "Exact YES/NO/VOID rule" \
  --probability 42% \
  --output forecast.json
python "$SKILL_DIR/scripts/validate_forecast.py" forecast.json
python "$SKILL_DIR/scripts/render_forecast_html.py" forecast.json --output forecast.html
# Hand-polish placeholder sections, then:
python "$SKILL_DIR/scripts/verify_html_briefing.py" forecast.html \
  --ids overview,outcomes,bayes,flow,history,actors,triggers,sources,ledger \
  --require-forecast-data
```

## Validate the package

Run syntax checks:

```bash
python3 -m py_compile scripts/forecast_math.py scripts/render_forecast_html.py scripts/scaffold_forecast.py scripts/validate_forecast.py scripts/verify_html_briefing.py
```

Run deterministic smoke checks:

```bash
python3 scripts/forecast_math.py bayes --prior 0.42 --lr 1.35 --lr 0.85
python3 scripts/validate_forecast.py examples/minimal-forecast.json
python3 scripts/verify_html_briefing.py examples/minimal-briefing.html \
  --ids overview,outcomes,bayes,flow,history,actors,triggers,sources,ledger \
  --require-forecast-data
```

The bundled HTML example is hand-polished and should return JSON with `"ok": true`. Fresh renderer output is a scaffold; either hand-polish the generated placeholder sections or run the verifier with `--allow-placeholders` only for a scaffold smoke test.

## Public hygiene

This package is sanitized for public sharing:

- no personal home-directory paths;
- no private wiki paths;
- no source transcripts or session logs;
- no client, employer, or unpublished project details;
- no API keys, credentials, or live local configuration;
- only synthetic examples are included.

Before publishing changes, run a path/secret scan and inspect the diff manually. Treat generated forecast artifacts as potentially sensitive until sources, names, paths, and claims are cleared for public release.

## License

Apache-2.0. See `LICENSE`.
