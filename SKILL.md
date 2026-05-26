---
name: historical-bayesian-html-briefing
description: Use when a user wants a historically grounded deep dive that combines mechanism-based analogies, explicit probabilistic outcome forecasting, Bayesian updates, scenario odds, or a self-contained interactive HTML briefing for a complex social, technical, economic, or geopolitical system.
version: 1.0.0
author: Skill package maintainers
license: Apache-2.0
metadata:
  hermes:
    tags: [research, synthesis, forecasting, bayesian-analysis, historical-analogy, html-artifact, visualization]
    category: research
    related_skills: [research, academic-research-synthesis, frontend-design, obsidian]
---

# Historical Bayesian HTML Briefing

Use this skill when an analysis needs more than a summary: mechanism-based historical analogies, explicit uncertainty, visible Bayesian updates, scenario probabilities, and optionally a self-contained interactive HTML dossier.

The goal is not fake precision. The goal is disciplined uncertainty: expose base rates, evidence, likelihood ratios, scenario assumptions, caveats, and update triggers clearly enough that a reader can challenge the model.

## When to Use

Use for prompts like:

- "What happens historically in this kind of situation?"
- "Give me possible outcomes with percent chances."
- "Use Bayesian updating."
- "Compare this modern technical, economic, political, or organizational problem to older historical cases."
- "Turn this research into an interactive HTML briefing, dossier, field report, or map."

Do not use this for simple summaries, one-off current-fact lookups, or narrow code tasks that do not need historical comparison or probabilistic forecasting.

## Prerequisites

- Access to the source material being analyzed: article, transcript, paper, policy, market event, interview, notes, or dataset.
- A way to calculate probabilities with code or a calculator. Do not do Bayesian arithmetic by mental math.
- Optional: a user-selected notes or wiki directory for saving source notes, raw transcripts, analysis markdown, and HTML artifacts.
- Optional: a browser or HTML preview tool if the deliverable is interactive.

Load companion skills/tools as needed:

- `research` for source gathering and synthesis.
- `academic-research-synthesis` when papers or scholarly fields matter.
- `frontend-design` when producing polished HTML.
- `obsidian` or the user's preferred note system skill when writing into a local knowledge base.

## Procedure

### 1. Define the system, not just the topic

Identify the moving parts before choosing analogies:

- the surplus, scarce resource, or bottleneck flow;
- the ruling or allocation center;
- bottleneck actors with leverage;
- excluded, lower-status, or under-rewarded actors;
- capital owners, customers, shareholders, or dependents;
- state, legal, regulatory, or coercive actors;
- competitors, outside raiders, substitutes, or alternative supply paths.

For historical analogy, compare functions rather than aesthetics. A modern supply-chain choke point is not literally a grain route, guild, mine, port, railroad, or arsenal, but it may share the same causal role: concentrated leverage over a strategic flow.

### 2. Capture sources and caveats

Before forecasting, separate:

- what the source explicitly claims;
- what is corroborated elsewhere;
- what is inferred;
- what remains uncertain or contested;
- which actors have incentives to exaggerate, minimize, or obscure the facts.

If creating durable notes, keep raw source notes separate from analysis so later readers can audit the chain from source to interpretation.

### 3. Build a historical analogue set

Use a compact but diverse case set. Include old history when it shares the mechanism:

- royal, state, temple, or military workshops;
- guild cities and protected craft monopolies;
- mines, extraction camps, and frontier labor systems;
- peasant, artisan, or skilled-labor scarcity conflicts;
- navies, armies, arsenals, and strategic labor corps;
- ports, rail, coal, telecom, power, logistics, semiconductors, or other network chokepoints;
- conglomerate, chaebol, keiretsu, national-champion, or state-capital restructuring.

For each analogue capture:

- chokepoint;
- grievance or stressor;
- ruling-center response;
- outcome;
- what maps to the present system;
- what does not map.

### 4. Separate event probabilities from dominant scenarios

Events can overlap, so they do not need to sum to 100%. Examples:

- selective concessions;
- legal, state, or managerial containment;
- institutional reform;
- automation, substitution, redundancy, or de-chokepointing;
- structural breakup, firewalling, or reallocation;
- major disruption, strike, conflict, default, or system failure.

Dominant scenarios should be mutually exclusive over a stated horizon, such as 0-6 months, 0-24 months, or 2-5 years. Normalize only the mutually exclusive scenario set.

### 5. Use explicit Bayesian math

Use code, a spreadsheet, or a calculator for arithmetic.

Recommended base-rate smoothing:

```text
prior p = (k + 1) / (n + 2)
odds = p / (1 - p)
posterior odds = prior odds * LR1 * LR2 * ...
posterior p = posterior odds / (1 + posterior odds)
```

Where:

- `n` = analogue cases considered;
- `k` = cases where the event appeared;
- `LR` = likelihood ratio for modern evidence.

Use small, legible likelihood ratios unless evidence is unusually strong:

- 0.7-0.9: weak negative evidence;
- 1.1-1.4: weak or moderate positive evidence;
- 1.5-2.5: strong positive evidence;
- 3.0+: direct, high-quality, outcome-specific evidence.

Always label the result as a transparent toy calibration, not a proven factual forecast.

### 6. Explain the outcome logic plainly

For each scenario include:

- percent chance;
- what it looks like in concrete terms;
- historical pattern;
- why it is plausible here;
- why it may fail;
- what new evidence would update probability upward or downward.

The output should feel like a map a reader can reason with, not an oracle.

### 7. Build the HTML briefing when requested

When asked for HTML, create a self-contained local file. Avoid external asset dependencies unless the user explicitly wants them.

Prefer a context-native aesthetic over generic software-dashboard styling: archival dossier, industrial field report, annotated map, court ledger, machine-room schematic, war-room notebook, or institutional case file.

Useful interactive sections:

- scenario selector cards;
- probability bars;
- Bayesian workbench with evidence toggles;
- causal flow diagram;
- historical analogue filter deck;
- actor map;
- update-trigger section;
- source and caveat appendix.

Use `references/html-briefing-pattern.md` as the checklist.

### 8. Verify before completion

For HTML artifacts:

- verify the file exists and has nonzero size;
- check required section IDs and navigation anchors;
- check for unintended external `src=` or `href=` dependencies;
- confirm scenario and evidence data exist if JavaScript interactivity is expected;
- if saving into a knowledge base, update its index/log according to that knowledge base's convention and read back the updates.

From the skill directory, run the bundled verifier when practical:

```bash
python3 scripts/verify_html_briefing.py /path/to/briefing.html --ids outcomes,bayes,flow,history,actors,triggers,sources
```

## Pitfalls

- Do not flatten history into a cute metaphor. State what maps and what does not.
- Do not let overlapping event probabilities sum to 100 unless they are explicitly mutually exclusive.
- Do not use precise percentages without showing model inputs.
- Do not confuse event probability with dominant-scenario probability.
- Do not treat source claims as verified facts; preserve caveats and source incentives.
- Do not bury the conclusion under methodology. Give the answer first, then show the math.
- Do not make an HTML artifact depend on external fonts, scripts, or CDNs unless requested.
- Do not include private local paths, raw personal notes, secrets, unpublished client/employer context, or session transcripts in a public briefing package.

## Verification Checklist

Before claiming the work is complete:

- The historical analogue set is mechanism-based, not aesthetic.
- Sources, caveats, and assumptions are visible.
- Bayesian arithmetic was performed with a tool, spreadsheet, or code.
- Event probabilities and mutually exclusive scenarios are clearly separated.
- Update triggers are concrete enough to change future odds.
- Any HTML artifact passes static checks for required IDs, anchors, file size, and external dependencies.
