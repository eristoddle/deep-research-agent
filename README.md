# deep-research-agent

A structured, human-in-the-loop deep-research pipeline for Claude Code, packaged as a single APM-installable bundle.

Contains the five `/research*` skills, the `web-search-agent` subagent that does the actual searching, and the five search-strategy modules the agent reads before it searches.

## Credit

The skills, agent, and strategy modules originate in [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) by **Lan Zheng**, MIT licensed. All credit for the design of the pipeline goes there. This repository repackages that work with fixes described below; upstream's copyright is retained in `LICENSE`.

If you want the original, unmodified pipeline, install it from upstream directly.

## Install

```sh
apm install eristoddle/deep-research-agent --target claude
```

Deploys to:

```
.claude/agents/web-search-agent.md
.claude/skills/research/{SKILL.md,validate_json.py}
.claude/skills/research-add-items/SKILL.md
.claude/skills/research-add-fields/SKILL.md
.claude/skills/research-deep/SKILL.md
.claude/skills/research-report/SKILL.md
.claude/skills/web-search-modules/{academic-papers,chinese-tech,general-web,github-debug,stackoverflow}.md
```

One dependency, no ordering constraints. Previously the skills and the agent had to be installed as six separate deps, and installing the skills without the agent produced a pipeline that failed at first use.

## Usage

```
/research <topic>        # interactive: builds outline.yaml + fields.yaml
/research-add-items      # amend the item list
/research-add-fields     # amend the field list
/research-deep           # one agent per item -> one JSON per item in results/
/research-report         # roll the JSON files up into report.md
```

`/research` and `/research-deep` launch `web-search-agent` by name via Task, so the skills do not work without the agent — which is the reason this bundle exists.

## Changes from upstream

### Packaging

1. **Single installable package.** APM only accepts a source whose root is a package (`SKILL.md`, `apm.yml` + `.apm/`, or `plugin.json`). Upstream ships its agent as a bare `agents/` directory with none of those, so `apm install Weizhena/Deep-Research-skills/agents` fails validation and the agent — which the skills require — cannot be installed as a dependency at all.
2. **Modules live under `skills/`, not `agents/`.** APM flattens every `.md` beneath `agents/` into individual top-level agents when installing from a git source, which destroys the `web-search-modules/` directory and registers five bogus agents. A skill bundle deploys its directory intact.

### Fixes

3. **`web-search-agent` declares a `tools:` allowlist.** Upstream's agent has no `tools:` frontmatter, so it inherits every tool the host offers. Under Copilot/VS Code that includes the embedded browser and download tooling — an agent instructed to "systematically explore" ~25 source families reached for browser automation and opened roughly a hundred editor tabs in a single run, and separately wrote its own report-generator script rather than using `/research-report`. It is now restricted to `WebSearch, WebFetch, Read, Write, Bash`, with an explicit prohibition on browser automation, downloads, and self-authored research scripts.

4. **The agent has a search budget, a stop condition, and a depth control.** Upstream instructs it to generate "5-10 query variations", "read beyond the first few results", and cover a merged list of ~25 source families, with no cap on searches, fetches, or link depth, and no definition of done. Runs went over an hour with no way to distinguish working from stuck. There is now a three-level depth setting, defaulting to `standard`:

   | Level | Searches | Fetches | Link depth | Modules |
   |---|---|---|---|---|
   | `quick` | 3 | 4 | 1 | 1 |
   | `standard` *(default)* | 8 | 12 | 1 | 2 |
   | `deep` | 20 | 30 | 2 | 3 |

   Set it per run with `/research-deep deep`, per project with `execution.depth` in `outline.yaml`, or ad hoc by naming explicit numbers in the task prompt — explicit numbers win, then the named level, then the outline, then the default. The agent reports budget state as it goes (`[deep: 3/20 searches, 5/30 fetches]`) and stops at the ceiling rather than quietly overspending it. Instructions that contradicted the budget were rewritten rather than left to fight it.

   Note this is unrelated to upstream's `detail_level` (`brief` / `moderate` / `detailed`) in `fields.yaml`, which controls how verbose each field's *answer* is, not how hard the agent searches. The two are independent — a `quick` run can still produce `detailed` fields, it just has less evidence behind them.

5. **`/research-deep` no longer hardcodes `~/.claude`.** Upstream's validation step invokes `python ~/.claude/skills/research/validate_json.py`. APM installs project-locally, so that file never exists and every agent's final validation step fails. The path is now resolved project-local first, global second, with an explicit instruction not to substitute a hand-written validator when neither is found.

6. **`validate_json.py` is no longer domain-locked.** Its `CATEGORY_MAPPING` was hardcoded to the categories of the topic it was first written for (AI coding assistants), so on any other research topic it failed to descend into nested category objects and misreported coverage. It now derives categories from the `fields.yaml` it is given, falling back to the original mapping.

7. **`/research-deep` reports progress.** Batch plans and cumulative per-batch progress are now mandatory, so a long run can be told apart from a hung one. Upstream disabled task output and printed nothing between batches.

8. **Per-item budgets propagate.** The `research-deep` prompt template passes the search budget and the tool prohibitions down to each item agent, so the constraints survive the handoff instead of applying only to the top-level agent.

Everything else — the pipeline design, the module contents, the outline/fields/results/report flow — is upstream's, substantially verbatim.

## Notes

Field counts matter more than they look. The pipeline researches every field for every item, so a 42-item outline with 96 fields is roughly 4,000 researched values and will not finish. Keep field lists to ~15-20 and prefer `items_per_agent: 1`, so each finished agent yields a complete file rather than an all-or-nothing batch.

## License

MIT. Copyright (c) 2026 Lan Zheng; modifications copyright (c) 2026 Stephan Miller. See `LICENSE`.
