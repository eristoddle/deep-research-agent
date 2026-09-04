# deep-research-agent

A structured, human-in-the-loop deep-research pipeline for Claude Code and GitHub Copilot, packaged as a single APM-installable bundle.

Contains six `/research*` skills, runtime-native research-agent entry points, and ten search-strategy modules used before searching.

## Credit

The skills, agent, and strategy modules originate in [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) by **Lan Zheng**, MIT licensed. All credit for the design of the pipeline goes there. This repository repackages that work with fixes described below; upstream's copyright is retained in `LICENSE`.

If you want the original, unmodified pipeline, install it from upstream directly.

## Install

Choose one host explicitly. For GitHub Copilot:

```sh
apm install eristoddle/deep-research-agent --target copilot
```

For Claude Code:

```sh
apm install eristoddle/deep-research-agent --target claude
```

The equivalent persistent pin belongs at the top level of `apm.yml`; use exactly one target:

```yaml
targets: [copilot] # or [claude]
dependencies:
   apm:
      - eristoddle/deep-research-agent#<commit-sha>
```

Do not omit the target when both hosts are detectable, and do not pin both for the same checkout. Auto-detecting both deploys the canonical `web-search-agent` into both agent registries, where Copilot sees duplicate agent names.

Current APM deploys agents under the selected host. Copilot uses the shared skills directory:

```
.github/agents/{web-search-agent,web-research-writer}.agent.md  # Copilot
.agents/skills/research/{SKILL.md,LAYOUT.md,validate_json.py}
.agents/skills/research-{add-items,add-fields,add-module,deep,report}/SKILL.md
.agents/skills/web-search-modules/{SKILL.md,ROUTING.md,<module>.md}
```

Claude keeps its native directories:

```
.claude/agents/{web-search-agent,web-research-writer}.md
.claude/skills/research/{SKILL.md,LAYOUT.md,validate_json.py}
.claude/skills/research-{add-items,add-fields,add-module,deep,report}/SKILL.md
.claude/skills/web-search-modules/{SKILL.md,ROUTING.md,<module>.md}
```

One dependency, no ordering constraints. Previously the skills and the agent had to be installed as six separate deps, and installing the skills without the agent produced a pipeline that failed at first use.

For an existing mixed install, choose the host you actually use, remove only this package's two generated agent files from the inactive host directory, then rerun the matching explicit install command above with `--force`. Keep the selected host's skills directory: `.agents/skills/` for Copilot or `.claude/skills/` for Claude.

## Optional: better fetching for blocked pages

The pipeline works with no setup. These two are optional, and the agent checks for them rather than requiring them — if neither is present, a page that blocks fetching is simply recorded as unreachable and the run continues.

**The agent never installs anything itself.** That is a deliberate limit on what it may do, which is exactly why setup is documented here instead: without it, the fallback below can silently never fire and there is nothing to tell you why.

### crawl4ai (`crwl`) — free

When `WebFetch` gets a 403, a bot challenge, or an empty body, the agent may retry that one URL through `crwl`. One retry, same fetch budget, output bounded, no crawling. It recovers a fair number of pages that plainly refuse `WebFetch`.

```sh
pip install crawl4ai && crawl4ai-setup
```

Nothing else is needed — the agent looks for `crwl` on `PATH` and uses it if it is there.

It does **not** recover a page whose content is rendered by client-side JavaScript; it snapshots before that content loads. For those, a JSON endpoint beside the HTML page is usually the better route, which is the kind of thing recorded in `skills/web-search-modules/ACCESS.md`.

### Firecrawl — paid, and never automatic

Firecrawl is the rung above `crwl`: a hosted API with a proxy pool, which is what makes it the one option likely to get past a block that is based on your IP address rather than your user agent.

**It costs money, so nothing in this package calls it on your behalf.** It is not wired into the agent, and installing it does not change how a research run behaves. It is here because it is the tool that answers "is this site actually unreachable, or just unreachable from my machine?" — a question worth being able to settle when a source you need keeps failing.

Sign up: **[firecrawl.link/stephan-miller](https://firecrawl.link/stephan-miller)** *(affiliate link — it costs you nothing extra and supports this project; [firecrawl.dev](https://firecrawl.dev) is the plain one if you would rather.)*

```sh
npm install -g @mendable/firecrawl-cli
export FIRECRAWL_API_KEY=fc-...        # fish: set -Ux FIRECRAWL_API_KEY fc-...
```

Use it yourself when you want to check a stubborn source. If you have a local fetch-escalation skill installed, the agent prefers that over calling any of this directly, since such a skill knows more about specific sites than a general rule can.

## Usage

```
/research <topic>        # interactive: builds outline.yaml + fields.yaml
/research-add-items      # amend the item list
/research-add-fields     # amend the field list
/research-add-module     # build a search module for a domain the existing ones miss
/research-deep           # one agent per item -> one JSON per item in results/
/research-report         # roll the JSON files up into report.md
```

`/research` and `/research-deep` select the host-native entry point: Copilot launches `Web Research Writer`; Claude launches `web-search-agent`. The skills do not work without the packaged agents, which is the reason this bundle exists.

## Changes from upstream

### Packaging

1. **Single installable package.** APM only accepts a source whose root is a package (`SKILL.md`, `apm.yml` + `.apm/`, or `plugin.json`). Upstream ships its agent as a bare `agents/` directory with none of those, so `apm install Weizhena/Deep-Research-skills/agents` fails validation and the agent — which the skills require — cannot be installed as a dependency at all.

2. **Modules live under `skills/`, not `agents/`.** APM flattens every `.md` beneath `agents/` into individual top-level agents when installing from a git source, which destroys the `web-search-modules/` directory and registers five bogus agents. A skill bundle deploys its directory intact.

### Fixes

Upstream behavior that was broken and now works.

3. **`web-search-agent` declares a `tools:` allowlist.** Upstream's agent has no `tools:` frontmatter, so it inherits every tool the host offers. Under Copilot/VS Code that includes the embedded browser and download tooling — an agent instructed to "systematically explore" ~25 source families reached for browser automation and opened roughly a hundred editor tabs in a single run, and separately wrote its own report-generator script rather than using `/research-report`. It is now restricted to `WebSearch, WebFetch, Read, Write, Bash`, with an explicit prohibition on browser automation, downloads, and self-authored research scripts.

4. **`/research-deep` no longer hardcodes `~/.claude`.** Upstream's validation step invokes `python ~/.claude/skills/research/validate_json.py`. APM installs project-locally, so that file never exists and every agent's final validation step fails. The path is now resolved across project and user installs for both `.agents/skills/` and `.claude/skills/`, with an explicit instruction not to substitute a hand-written validator when none is found.

5. **`validate_json.py` is no longer domain-locked.** Its `CATEGORY_MAPPING` was hardcoded to the categories of the topic it was first written for (AI coding assistants), so on any other research topic it failed to descend into nested category objects and misreported coverage. It now derives categories from the `fields.yaml` it is given, falling back to the original mapping.

6. **The validator no longer passes an empty field set.** `load_fields_yaml` silently returns zero fields when `fields.yaml` is missing its top-level `field_categories:` list — a malformed or wrong-shaped file, or the wrong path. Every JSON is then trivially 100% covered and every item reports `[PASS]`, while `/research-deep` treats that as "task complete". Found by running the pipeline against a hand-written `fields.yaml`. It now prints the expected schema and exits 2 rather than validating against nothing.

### Additions

Capability upstream never had, added here.

7. **The agent has a search budget, a stop condition, and a depth control.** Upstream instructs it to generate "5-10 query variations", "read beyond the first few results", and cover a merged list of ~25 source families, with no cap on searches, fetches, or link depth, and no definition of done. Runs went over an hour with no way to distinguish working from stuck. There is now a three-level depth setting, defaulting to `standard`:

   | Level | Searches | Fetches | Link depth | Modules |
   |---|---|---|---|---|
   | `quick` | 3 | 4 | 1 | 1 |
   | `standard` *(default)* | 8 | 12 | 1 | 2 |
   | `deep` | 20 | 30 | 2 | 3 |

   Set it per run with `/research-deep deep`, per project with `execution.depth` in `outline.yaml`, or ad hoc by naming explicit numbers in the task prompt — explicit numbers win, then the named level, then the outline, then the default. The agent reports budget state as it goes (`[deep: 3/20 searches, 5/30 fetches]`) and stops at the ceiling rather than quietly overspending it. Instructions that contradicted the budget were rewritten rather than left to fight it.

   Note this is unrelated to upstream's `detail_level` (`brief` / `moderate` / `detailed`) in `fields.yaml`, which controls how verbose each field's *answer* is, not how hard the agent searches. The two are independent — a `quick` run can still produce `detailed` fields, it just has less evidence behind them.

8. **Per-item budgets propagate.** The `research-deep` prompt template passes the search budget and the tool prohibitions down to each item agent, so the constraints survive the handoff instead of applying only to the top-level agent.

9. **`/research-deep` reports progress.** Batch plans and cumulative per-batch progress are now mandatory, so a long run can be told apart from a hung one. Upstream disabled task output and printed nothing between batches.

10. **Module routing is a router file, not a list in the agent prompt.** Upstream hardcodes five `trigger -> read file` lines into the agent's system prompt, with no default when nothing matches, no anti-triggers, and the same table mirrored in a second file. That works at five modules and stops working as the library grows: overlapping triggers get resolved by silently dropping one, and every module costs system-prompt context on every task whether or not it is relevant. Routing now lives in `skills/web-search-modules/ROUTING.md` — the single source of truth — which the agent reads before any search. It groups modules into **families** with a yes/no discriminating question, makes `general-web` the **explicit default** (and a valid companion to any specialist), demotes `chinese-tech` to a **modifier** layered on top of a topic module rather than competing with one, and ties module slots to the depth level. Adding a module is now one file plus one row; the agent's prompt never changes. Every module carries a `Use when` / `Do not use for` / `Siblings` header so a mis-route corrects itself at read time.

11. **Routing propagates and can be pinned.** The agent has no `AskUserQuestion`, so on ambiguity it routes to its best guess and reports it (`Routed: X + Y (Z was a close second)`) instead of stalling or hedging by loading extra modules. `/research` asks up front and records the choice in `execution.modules` in `outline.yaml`, and `/research-deep` passes it to every item agent as a `Modules:` block — the same propagation the search budget gets.

12. **Four new search modules: an AI ecosystem & market family.** Upstream's five modules assume you are debugging code or reading papers. None of them knows how to find a live leaderboard, a current model ID, a pricing page, or a competitive set — which is most of what technology-product research actually asks for. Added `benchmarks` (independent evaluators first, configuration and observation date mandatory, self-reported scores labeled as such), `model-releases` (docs and deprecation pages outrank announcement posts; model IDs, not marketing names), `pricing` (never quote a price from anything but the provider's own page, with unit, host, and date), and `vendor-landscape` (build the competitive set from vendors' own comparison pages; separate claim from evidence). They form one family in `ROUTING.md` with a disambiguation table, since they overlap deliberately.

13. **`/research-add-module` — build a search module by discovering its sources.** A module is only as good as its source list, and a guessed source list routes the agent to plausible-sounding sites that turn out to be empty. This skill runs the discovery deliberately: draft the questions the module must answer, search them as plain `general-web` queries, tally which domains actually hold the answers, then work out and **test** how to query each one — a `site:` query, the site's own search URL, a stable index page to fetch directly, or a note that it blocks fetching. It registers the result, then verifies the module beats `general-web` on the original questions and offers to discard it if it does not.

14. **Locally-created modules survive reinstalls.** Modules can live in `.agents/web-search-modules-local/`, which APM does not own. `ROUTING.md` prefers that directory, retains `.claude/web-search-modules-local/` as a legacy fallback, and lets local entries win on a name conflict, so a project can add its own modules — a client's competitive set, a niche source list — without editing any packaged file and without losing them to the next `apm install`.

15. **A bounded fetch fallback for blocked pages.** `WebFetch` returns 403s, bot challenges, and JS-only shells often enough to lose real sources. The agent may now retry **one** such URL through `crwl` (crawl4ai) if it is already installed — stdout only, output bounded with `head -c`, no `--deep-crawl`, no output-to-file, no install attempt, no second helper, no third try. It does not buy an extra fetch slot, since it is the same URL. The prompt also states why this is not a hole in the browser-automation ban: that ban is about driving a visible browser, and this is a one-shot headless fetch that prints text.

16. **A `competitor-content` module, and the first non-technical family.** Research that has to say something competitors do not needs to know what competitors already said. This module samples what is published on a topic — an unrefined search of the reader's actual query, 3-5 top pages read for *outline* rather than prose, PAA and forum questions, query variants — and reports the union of subtopics plus the gap. It states its limits rather than filling them in: `WebSearch` returns a result list, not a SERP, so ranking position, search volume, and keyword difficulty are unavailable and must never be estimated. Where the caller is doing brief-level SEO work rather than per-item pipeline research, it names `ct-seo-research` as the better instrument instead of half-reproducing it. Its family question — *what has already been written about this?* — is the first that is not about technology at all, and is the worked example for attaching non-technical families.

17. **Research results live under one root, with `INDEX.md` as the branch record.** Run folders used to land at the project root, indistinguishable from hand-written directories in a repo where the user is also writing code. Every run now lives inside a single root (default `research/`, asked once and never written to a config file — discovery is structural: any directory containing `outline.yaml` is a run folder, found by globbing one and two levels deep). Research also doesn't run once — one run's findings point at the next — so `research/INDEX.md` records that tree: a `## Map` of nested bullets showing which run spawned which, then one section per run with its purpose, status, a capped copy of its report's summary, and a `**Leads**` checklist of the directions it opened. Layout and discovery live in exactly one file, `skills/research/LAYOUT.md`, read by every skill's locate step — the `ROUTING.md` pattern applied to results instead of modules. Existing root-level runs keep working with no changes required; `/research` finds them and **offers**, never forces, a migration into the new layout.

18. **Claude and Copilot use runtime-native agent entry points.** Claude keeps the established `web-search-agent` with its exact `WebSearch, WebFetch, Read, Write, Bash` allowlist. Copilot launches the uniquely named `Web Research Writer` wrapper with `read, search, web, edit, execute`, then loads the canonical research prompt instead of duplicating it. Orchestration uses that exact registered name, packaged resources resolve through `.agents/skills/` before legacy `.claude/skills/`, and explicit one-host installs prevent duplicate canonical-agent registration.

Everything else — the pipeline design, the five original modules, the outline/fields/results/report flow — is upstream's, substantially verbatim.

## Roadmap

[`ROADMAP.md`](ROADMAP.md) tracks which search modules have been added since the fork, which ones are wanted next, and what still needs retrofitting. It lives at the repo root rather than inside the skill payload on purpose: a roadmap shipped inside a skill deploys into every install, goes stale there, and gets read as instruction by whatever loads it.

## Notes

Field counts matter more than they look. The pipeline researches every field for every item, so a 42-item outline with 96 fields is roughly 4,000 researched values and will not finish. Keep field lists to ~15-20 and prefer `items_per_agent: 1`, so each finished agent yields a complete file rather than an all-or-nothing batch.

## License

MIT. Copyright (c) 2026 Lan Zheng; modifications copyright (c) 2026 Stephan Miller. See `LICENSE`.
