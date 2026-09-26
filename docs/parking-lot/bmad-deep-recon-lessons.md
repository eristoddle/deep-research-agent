# Lessons from BMAD deep-recon

**Parked** 2026-09-25, from a read of [bmad-code-org/BMAD-METHOD `skills/bmad-deep-recon`](https://github.com/bmad-code-org/BMAD-METHOD/tree/5e33d3c03ba53187a40ab679d5479cdd4b6ac2fb/skills/bmad-deep-recon) (pinned commit `5e33d3c`), after Stephan used it for a plugin-API teardown of VS Code and Obsidian and found it good. It is listed in `ALTERNATIVES.md`.

Items 1–6 came from reading the skill, and are about trust: proving each answer is true and current. Items 7–11 came from reading the actual Veneer run output, and are about what made that run *good* — they matter more. None is decided — each still has to ripen through a grill into a decision before it becomes a task.

## Flexibility rule — applies to every item below

The package's standard pipeline is one shape among several uses. It has also been driven ad hoc for a specific task, where no report is wanted and the findings feed straight into the work (e.g. building software). Every addition here must be **opt-in or additive**: a run that asks for none of it behaves exactly as it does today, nothing new becomes a required step, and nothing forces a report. New features widen what the package can do; they never narrow the default. A proposal that fails this test gets reshaped, not shipped.

## Credit rule — applies to every item below

**When any of these ships, credit BMAD deep-recon in `README.md` in the same change.** The pipeline itself originates in Weizhena/Deep-Research-skills and the Credit section says so; ideas taken from a second repo get the same treatment. Add a line to the Credit section naming BMAD Method (bmad-code-org) and linking the skill, and name the specific idea in the README's **Additions** entry for the feature. Once the first item ships, later items only add to the Additions entry.

## 1. Every answered field must trace to a source — checked by script

Deep-recon's first rule is "never conclude from training data alone": prior knowledge proposes queries, only evidence retrieved this run concludes. This is a real risk for a field matrix — an agent filling "VS Code extension API: activation events" already knows a plausible answer and may never search for it.

D17 already gives every `results/*.json` a `sources[]` array with a `fields` key. So `validate_json.py` can check mechanically: every answered (non-`[uncertain]`) field must appear in at least one `sources[].fields`. An answered field with no backing source is flagged. Enforced by the script rather than by prompt wording, and it builds on what exists. Open: warn or fail the exit code, given `/research-deep` gates completion on it.

## 2. Freshness windows per field, and a re-check list

Each deep-recon research type sets how old a claim of each class may be (pricing & features ≤ 3 mo, versions/compatibility ≤ 1 mo, landscape ≤ 12 mo) and the report ends with a computed staleness map: re-check dates per claim, earliest first.

Here a field already *is* a claim class, so the window belongs in `fields.yaml` (e.g. `fresh_for: 3mo`), possibly with a default in a module. Requires `sources[]` entries to gain a publication date and an access date, which they do not carry today — that touches the hard-constrained templates in `skills/research-deep/SKILL.md` and their one-shot examples in lockstep. `/research-report` would render the re-check list. Distinct from D12, which is about expiring *access* findings in modules, not expiring *answers*.

## 3. A `disputed` marker, separate from `uncertain`

`[uncertain]` currently covers both "could not confirm" and "sources disagree". Deep-recon separates them and never averages: a disputed value reports both figures, both cited. Its definition of an **independent** source is worth copying verbatim in spirit: a different publisher with different underlying data — not a syndication or quote of the first, and not the same vendor's marketing in two places. Also a hard-constrained template change, and `validate_json.py` would need to know the new marker.

## 4. Draft then Process — let an outside deep-research product do the gathering

Deep-recon can skip searching entirely: draft a prompt for a deep-research product the user already pays for (ChatGPT, Gemini, Perplexity), then process the returned report into its own cited format. For this package: a skill that turns a pasted external report into `results/<item>.json` against the run's `fields.yaml`, or that drafts the per-item prompt from `outline.yaml` + `fields.yaml`. Saves heavy token spend on large runs. The largest item here — a new skill. Note deep-recon's rule for imports: an imported report counts as one publisher however many sources it cites internally.

## 5. A source-quality card in the agent prompt

About five lines for `agents/web-search-agent.md`. Prefer primary sources. Downgrade on sight: speculative language presented as findings, marketing register, unnamed sources, unsourced numbers, and many domains recycling one upstream report (that is one publisher). Answer engines (Perplexity and kin) are aggregators — chase and cite their citations, never the engine. Conflicts resolve by recency, consistency with established facts, and publisher quality, never by averaging.

## 6. A "pick one" mode for the report

Deep-recon's select shape: split requirements into hard gates and weighted preferences, agreed *before* research runs; screen to finalists recording what was cut and why; show a weighted matrix with the scoring visible so the reader can re-weight it; name the pick, the runner-up and the conditions under which it wins, the strongest argument against the pick, and the cheapest way to reverse the choice. For this package: an optional `/research-report` mode that applies weights over `fields.yaml` fields. Would have fit the plugin-API research had the goal been choosing a model to copy.

## What made the Veneer run good — evidence

Read 2026-09-25 from the run folder `veneer/_bmad-output/planning-artifacts/research/technical-vs-code-and-obsidian-plugin-apis-2026-09-25/` (`.memlog.md`, `research.md` headings, the D2 actions digest in full). Preset `standard`, 8 dimensions, validation `normal`, red team off.

**Not the driver: lead-following rounds.** All 8 dimensions logged `Stopped: coverage` after round 1; no round-2 digest exists. The trust layer (items 1–3) ran after the research and corrected details — 12 claims verified, 1 disputed, 6 partial citations fixed — without changing what was found. Worth having, but not why the output was good.

## 7. A decision line that every agent receives

The run's first log line is the decision: "which plugin mechanics/APIs Veneer borrows, builds now, or keeps as future candidates." Every digest ends in a **Design lessons** list answering it — "copy VS Code's declaration/implementation split", "do not let plugins ship default hotkeys silently", "auto-namespace command IDs as Obsidian does". This package gathers facts and leaves the so-what to the human. Shape here: an optional `decision:` in `outline.yaml`, injected into the item-agent template, and an optional lessons section in each result when it is set. Template change — lockstep with the one-shot example.

## 8. Question-major runs: one agent per question, across all subjects

The biggest driver. Each of the 8 agents owned a *question* (lifecycle, actions, UI surfaces, editor, files/events, theming, security, AI APIs) and researched it for **both** VS Code and Obsidian, so every comparison and lesson came from an agent holding both sides. This package's unit is one agent per *item*: with VS Code and Obsidian as items, two agents each research one product and nothing compares them. For a compare-then-decide task the item×field grid is the wrong shape. Shape here: a new run shape, probably its own stage alongside `/research-enumerate` rather than a flag on `/research-deep`. A real design change — grill it, do not quick-edit it.

## 9. An open inventory field instead of predeclared fields only

Each digest's core was an ~40-row inventory table (system, API, what it does, gotchas, source) — a list of what exists, which could not have been written as `fields.yaml` entries in advance because discovering the API surface was the point. Shape here: an optional field type whose value is an open table with declared columns, so an item agent can enumerate. `validate_json.py` must understand it. Related to `/research-enumerate`'s breadth pass, but inside an item.

## 10. Reconcile against the project's own spec — after research, never during

The Veneer spec and plugin lists were kept out of research on purpose (`veneer-inventory.md` opens "project context — NOT research evidence") and used only afterward to mark each API row built / needed / future. That produced a gap list against the user's own software instead of a general survey. Deep-recon calls the rule the *research firewall*: project context shapes what to ask, never what is true. Shape here: an optional post-research step (in `/research-report`, or standalone when no report is wanted) that takes named project files and annotates results against them.

## 11. Leads and gaps per result

Every digest ends in **Leads & gaps**: claims still unconfirmed, sources seen only as search snippets, topics not covered, budget overruns. `[uncertain]` records *that* a value is shaky, not what to chase next. Shape here: an optional `leads[]` array beside `uncertain[]` / `unreachable[]` / `sources[]`, which also gives a later run or `/research-harvest` something to pick up.

## Considered and not taken

- **Red-team pass** (a fresh-context skeptic hunting disconfirming evidence per major conclusion) — suits a decision brief, weak fit for a grid of facts.
- **The `customize.toml` override layer** — heavy and BMAD-specific.
- Files-first persistence, depth presets and stop-when-answered — already equivalent here.
