# Strict HTML Default Lesson

Use this reference when maintaining or auditing the `historical-bayesian-html-briefing` workflow after a session where the agent answered a serious forecast in prose and only created the HTML artifact after the requester challenged it.

## Objective Function

For serious/open-ended forecasts, optimize for a complete forecast package by default:
1. forecastable question or scenario set;
2. machine-readable JSON ledger saved to disk;
3. outside-view/base-rate evidence and current sources;
4. tool-backed probability math or normalization;
5. successful ledger validation;
6. self-contained HTML briefing rendered, hand-polished, and verified;
7. concise terminal summary with real file paths and verification results.

Penalty should be high for prose-only answers, skipped validation, or treating HTML as optional when the skill was invoked for serious forecasting.

## Opt-Out Rule

Only skip the ledger/HTML package when the requester explicitly asks for a quick answer, gut check, no artifact, or no HTML. In that case, say the full package was intentionally skipped and do not imply the forecast is ledger-backed.

## Verification Lesson

A renderer that creates required IDs is not enough. The verifier should fail if generated placeholder copy remains in sections such as `flow`, `history`, `actors`, or `triggers`. The agent must hand-polish those sections before final delivery.

## Good Final Report Shape

Keep the final terminal response compact:
- top-line probabilities or scenario odds;
- JSON ledger path + validation `ok` result;
- HTML path + verification `ok` result;
- required section IDs present;
- artifact status (`draft`, `active`, etc.) or explicit quick/no-artifact opt-out.
