# Package-First Skill Optimization Notes

Use when maintaining, auditing, or optimizing this forecasting skill itself.

## Objective function that worked

For serious/open-ended forecasting questions, optimize for completion rate of verified forecast packages, not merely helpful prose.

A successful run produces:
- JSON forecast ledger saved to disk;
- probability calculations performed with code/tooling;
- ledger validation passing;
- self-contained HTML briefing generated;
- HTML verification passing, including no placeholder copy;
- final user summary with headline odds, artifact paths, and validation status.

Prose-only forecasts are failure states unless the requester explicitly opts out of artifacts or asks for a quick gut check.

## SkillOpt / optimizer pattern

When improving this skill:
1. Build an eval set that includes both positive triggers and near-miss negatives.
2. Score package-first behavior explicitly: JSON, math tooling, validation, HTML, verifier, final paths/status.
3. Keep wall-clock time as diagnostic metadata only unless the requester explicitly asks to optimize for speed.
4. Compare old/current/candidate versions against the same rubric before applying changes.
5. Apply the candidate only if it improves held-out behavior or fixes a concrete failure mode.
6. Preserve optimizer artifacts under a workspace/reference path so future agents can inspect the scoring logic.

## Trigger precision examples

Positive triggers should include:
- broad strategic questions: "what is going to happen with X?";
- explicit probabilities or odds;
- Bayesian/Tetlock/superforecasting language;
- market-resolution or scenario-odds questions;
- requests for shareable forecast briefings.

Near-miss negatives should include:
- simple factual explanations with no forecast horizon;
- historical summaries;
- requests for definitions;
- quick non-artifact answers when the requester explicitly opts out.

## Pitfall

Do not let a successful prose answer mask a package failure. The package contract is the behavior being optimized.