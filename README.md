# Historical Bayesian HTML Briefing

A shareable agent skill for turning complex events into historically grounded, probabilistic, source-caveated briefings.

It is designed for analyses that need:

- mechanism-based historical analogies rather than decorative metaphors;
- explicit Bayesian or probabilistic forecasting;
- clear separation between overlapping event probabilities and mutually exclusive scenarios;
- update triggers that say what evidence would move the odds;
- optional self-contained interactive HTML dossiers.

## What's included

```text
.
├── SKILL.md
├── references/
│   └── html-briefing-pattern.md
├── scripts/
│   └── verify_html_briefing.py
├── examples/
│   └── minimal-briefing.html
├── .agents/
│   └── skills/historical-bayesian-html-briefing/
│       ├── SKILL.md
│       ├── references/html-briefing-pattern.md
│       └── scripts/verify_html_briefing.py
├── AGENTS.md
├── LICENSE
└── README.md
```

The root `SKILL.md` is the canonical skill. The `.agents/skills/...` copy is a mirror for clients that discover skills from that layout.

## Install in Hermes

From the repository root:

```bash
TARGET="$HOME/.hermes/skills/research/historical-bayesian-html-briefing"
mkdir -p "$TARGET"
cp SKILL.md "$TARGET/"
cp -R references scripts "$TARGET/"
```

Then start a fresh Hermes session or refresh the skill index according to your local setup.

## Validate the package

Run the script syntax check:

```bash
python3 -m py_compile scripts/verify_html_briefing.py
```

Run the bundled verifier against the synthetic example:

```bash
python3 scripts/verify_html_briefing.py   examples/minimal-briefing.html   --ids outcomes,bayes,flow,history,actors,triggers,sources
```

Expected result: JSON with `"ok": true`.

## Public hygiene

This package was sanitized for public sharing:

- no personal home-directory paths;
- no private wiki paths;
- no source transcripts or session logs;
- no client, employer, or unpublished project details;
- no API keys, credentials, or live local configuration;
- only a synthetic HTML example is included.

Before publishing changes, run a path/secret scan and inspect the diff manually. Treat generated briefings as potentially sensitive until sources, names, paths, and claims are cleared for public release.

## License

Apache-2.0. See `LICENSE`.
