# HTML Briefing Pattern

Use this checklist when turning a historical and Bayesian analysis into a self-contained HTML document.

## Required Sections

- **Hero / thesis**: one-line frame, headline probabilities, scope caveat.
- **Scenario selector**: mutually exclusive dominant outcomes for a stated horizon.
- **Event probabilities**: overlapping probabilities that do not sum to 100%.
- **Bayesian workbench**: formula, priors, likelihood ratios, toggles, or a visible model table.
- **Causal flow**: system map from stressor to legitimacy break, bottleneck response, and outcomes.
- **Historical analogue deck**: cases filtered by mechanism, not era or aesthetic similarity.
- **Actor map**: each faction's claim, leverage, likely tactics, and constraints.
- **Update triggers**: what new evidence would move probabilities and by how much.
- **Sources and caveats**: original sources, local notes if safe to cite, and model limitations.

## Design Direction

Prefer a distinctive context-native aesthetic: archival dossier, industrial field report, annotated map, court ledger, machine-room schematic, or war-room briefing.

Avoid:

- generic SaaS cards;
- purple/neon gradient defaults;
- excessive centered hero sections;
- external CDN dependencies unless requested;
- decorative historical references that do not carry causal meaning.

## Interaction Ideas

- Scenario buttons update a detail pane.
- Evidence toggles recalculate normalized scenario odds.
- SVG flow nodes update explanatory text.
- Case chips filter historical analogues.
- Details/summary blocks reveal update rules.
- Source cards distinguish direct claims, corroborated facts, and inference.

## Verification Checklist

- HTML file exists and is nonzero.
- Navigation anchors resolve to actual IDs.
- Required interactive IDs exist.
- No accidental external `src=` dependencies.
- External `href=` references are intentional and listed in sources.
- Local relative links point to files that exist, or are removed before publication.
- Static verification output is recorded before claiming completion.
