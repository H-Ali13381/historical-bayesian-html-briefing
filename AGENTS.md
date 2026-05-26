# Agent Notes

This repository publishes one agent skill: `historical-bayesian-html-briefing`.

Canonical files:

- `SKILL.md` is the source of truth for the skill.
- `references/html-briefing-pattern.md` is the public checklist referenced by the skill.
- `scripts/verify_html_briefing.py` is the deterministic verifier referenced by the skill.
- `.agents/skills/historical-bayesian-html-briefing/` is a cross-client discovery mirror.

When editing the skill, update the root files first, then refresh the mirror:

```bash
mkdir -p .agents/skills/historical-bayesian-html-briefing
cp SKILL.md .agents/skills/historical-bayesian-html-briefing/
rm -rf .agents/skills/historical-bayesian-html-briefing/references .agents/skills/historical-bayesian-html-briefing/scripts
cp -R references scripts .agents/skills/historical-bayesian-html-briefing/
```

Validation checks:

```bash
python3 -m py_compile scripts/verify_html_briefing.py
python3 scripts/verify_html_briefing.py examples/minimal-briefing.html --ids outcomes,bayes,flow,history,actors,triggers,sources
```

Public hygiene checks:

Run your preferred repository secret scanner and a separate local-path scan before publishing. Keep scanner configuration outside this file or exclude this file from simple grep-style audits so the audit rules do not match themselves.

Do not add private paths, secrets, local debug notes, raw session logs, unpublished source transcripts, or client/employer-specific examples to this public package.
