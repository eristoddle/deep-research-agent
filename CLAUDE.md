# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

An APM-installable bundle of prompts and data. There is no application here — every `.md` file is either a skill Claude Code invokes or a reference file an agent reads at runtime. The single piece of executable code is `skills/research/validate_json.py`.

Consequences worth internalizing before editing anything:

- **There is no build and no test suite.** Correctness is judged by whether the installed pipeline behaves, not by anything runnable in this checkout.
- **Editing a file here is editing a prompt.** Wording, ordering, and emphasis are the implementation. A rewrite that reads better but drops a hard constraint is a regression.
- The package originates in [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) (Lan Zheng, MIT). Attribution in `README.md` and `LICENSE` stays.

## Development workflow — planning vs implementation

Planning and implementation run in two layers by design.

- **Planning (the main thread).** Question/answer and exploration, landing on decisions recorded in `PLAN.md`. Makes design calls, owns judgment about whether a module's routing or wording is right.
- **Implementation (the `implementer` agent).** Once a decision is concrete enough to build, the planning thread writes the active task into `TASKS.md` and launches the `implementer` agent. It runs in its own context window (keeping planning context clean) and can run in the background while planning continues. On return, the planning thread reviews the diff. **The agent is defined at `.claude/agents/implementer.md`, deliberately not in `agents/`** — APM flattens every `.md` beneath `agents/` into a separate top-level agent on install, so an agent written there would install itself into every consumer project.

`TASKS.md` is the handoff contract. The active task is a **serial queue of numbered pieces** — stack as few or as many as you like, which serves both **pacing** (queue a little, plan ahead while the agent grinds) and **unattended** (queue a lot and walk away). The default is synchronous: one agent works the queue top-to-bottom and reports once at the end; a blocked piece is skipped (not halted on) so the run finishes everything it legitimately can, and the agent **logs run-state into `TASKS.md` on every stop** (per-piece status + a ▶ Run state note) so a killed or forgotten session is recoverable from the file on disk. Standing "how we implement here" knowledge lives in the **agent definition**, not in every task. Only fully-specified, mechanical work is delegable; design decisions, open questions, and judgment calls stay in the planning thread.

**Verification here is not a test suite — there isn't one.** Each task's Tests section lists the concrete checks that stand in for one. Because editing a file in this repo is editing a prompt, a change that reads better but drops a hard constraint is a regression that nothing will catch; that is what the per-task checks and the tight Out-of-scope sections exist to contain.

**External task mirror — `~/Dropbox/Apps/remotely-save/Writing/10 Reference/10.06 Ideas/Software-Website-Business/🔎 Deep Research Agent.md`.** A second copy of this project's task list lives outside the repo, so items can be captured away from the machine and read back here. **Reconcile it before starting a queue and again after finishing one** — otherwise it drifts silently and gets forgotten, which is the failure this line exists to prevent. An item present on one side and missing from the other is **not** a decision to delete it: absence means "not yet mirrored," never "dropped." A mirrored item arrives as a *proposal* — it lands in the parking lot, never straight into the active queue. Nothing in `PLAN.md` or `TASKS.md` exists to serve the mirror; the mirror side owns the pointer and the reconciliation, and these docs stay standalone without it.

`PLAN.md` is the **hot** decision record — keep it lean. Cooled material (old session logs, settled/superseded decisions, deferred ideas) is progressively disclosed into `docs/` with one-line pointers left behind. When `PLAN.md` grows heavy to read each session, invoke the **`living-plan`** skill — it detects what has cooled and relocates it, propose-then-confirm.

Note that `ROADMAP.md` is **not** a task list — it is rationale, deliberately kept at the repo root rather than in the skill payload. Intentions live there; what is actually queued lives in `TASKS.md`.

## Verification

```sh
python3 -m py_compile skills/research/validate_json.py

# Exercise the validator against a real pipeline output (nothing in this repo has fields.yaml/results)
python3 skills/research/validate_json.py -f <project>/fields.yaml -j <project>/results/<item>.json
python3 skills/research/validate_json.py -f <project>/fields.yaml -d <project>/results   # whole directory
```

End-to-end verification means installing into a consumer project and running the pipeline there. Consumers pin a commit SHA:

```yaml
# consumer apm.yml
dependencies:
  apm:
  - eristoddle/deep-research-agent#<sha>
```

So a change is not live for a consumer until the pin is bumped and `apm install` re-run. `/Users/eristoddle/Dropbox/Writing/writing-model-research` is the live consumer; its `llm-writing-benchmark-landscape/` is a real completed run (outline, fields, results, report) and the best fixture for testing changes against.

## Architecture

Three layers, coupled by literal names and paths rather than imports:

```
/research, /research-deep …   skills/*/SKILL.md      user-invoked, orchestrate
        │ Task(subagent_type: "web-search-agent")
        ▼
web-search-agent              agents/web-search-agent.md   does all retrieval
        │ Read(.claude/skills/web-search-modules/<domain>.md)
        ▼
strategy modules              skills/web-search-modules/*.md   data only
```

**The skills launch the agent by name.** Installing the skills without the agent yields a pipeline that fails at first use — that is the entire reason this is one package rather than six.

**Modules live under `skills/`, never `agents/`.** APM flattens every `.md` beneath `agents/` into separate top-level agents when installing from a git source, which would destroy the `web-search-modules/` directory and register five bogus agents.

### Data contract of a research run

```
{topic_slug}/
  outline.yaml    # items[] + execution{batch_size, items_per_agent, output_dir, depth, modules}
  fields.yaml     # field categories, descriptions, detail_level (brief|moderate|detailed)
  results/*.json  # one file per item; values marked [uncertain]; trailing uncertain[] array
  report.md       # produced by a generate_report.py the report skill writes per project
```

`/research` builds the first two, `/research-deep` fans out one agent per item into `results/`, `/research-report` rolls them up. `detail_level` in `fields.yaml` controls answer verbosity; it is unrelated to the search-depth budget below.

## Things that break quietly

**Routing lives in exactly one file: `skills/web-search-modules/ROUTING.md`.** The agent's prompt names no modules — it only knows to read the router — so adding a module means writing `<domain>.md` and adding one row to `ROUTING.md`. Nothing else. Do not reintroduce a module list into `agents/web-search-agent.md` or `skills/web-search-modules/SKILL.md`; that duplication is what the router replaced.

The router distinguishes three kinds of entry, and new modules must pick one:

- **Topic modules**, grouped into *families* with a yes/no discriminating question. Pick one family, one module.
- **`general-web` is the explicit default** and doubles as a valid second module alongside any specialist. Routing to it is a correct answer, not a fallback failure.
- **Modifiers** (`chinese-tech`) are axes — language, region, recency — layered on a topic module. They never replace one and never consume a topic slot.

Module slots are set by depth: 1 at `quick`, 2 at `standard`, 3 at `deep`. Every module file carries a `Use when` / `Do not use for` / `Siblings` header so a mis-route corrects itself at read time.

**Modules live in two places.** `skills/web-search-modules/` is package-owned and APM overwrites it on every install — only edit it in this repo. `.claude/web-search-modules-local/` is project-owned and APM never touches it; `ROUTING.md` step 0 reads its router first and local entries win on a name conflict. Never write a project's own module into an installed `.claude/skills/web-search-modules/`; the next install deletes it. `/research-add-module` builds either kind.

**The agent cannot ask the user** — it is a subagent with no `AskUserQuestion`. On ambiguous routing it loads `general-web` plus its best guess and prints `Routed: X + Y (Z was a close second)`. Callers that *can* ask (`/research`, Step 2b) resolve routing up front and pin it to `execution.modules` in `outline.yaml`, which `/research-deep` passes to every item agent as `Modules:`.

**The depth/budget table is duplicated too** — `agents/web-search-agent.md` and `skills/research-deep/SKILL.md`. Changing the numbers means changing both.

| Level | Searches | Fetches | Link depth | Modules |
|---|---|---|---|---|
| `quick` | 3 | 4 | 1 | 1 |
| `standard` *(default)* | 8 | 12 | 1 | 2 |
| `deep` | 20 | 30 | 2 | 3 |

Precedence: explicit numbers in the task prompt > level named in the prompt > `execution.depth` in `outline.yaml` > `standard`.

**Prompt templates are marked `Hard Constraint` in `skills/research/SKILL.md` and `skills/research-deep/SKILL.md`** ("strictly reproduce, only replacing `{xxx}`"). The per-item budget, the tool prohibitions, and the `## Modules` routing block are injected *inside* those templates so the constraints survive the handoff to each item agent. Each template has a one-shot example directly below it — change one and you must change the other, or they teach contradictory formats. Restructuring a template drops them silently — the run still completes, just unbounded.

**Never hardcode `~/.claude`.** APM installs project-locally. Both lookups resolve project-local first, global second: modules at `.claude/skills/web-search-modules/` then `~/.claude/agents/web-search-modules/`; the validator at `<project>/.claude/skills/research/validate_json.py` then `~/.claude/skills/research/validate_json.py`. When neither exists the skill must stop and say so rather than hand-write a substitute validator.

**The agent's `tools:` allowlist is load-bearing.** `WebSearch, WebFetch, Read, Write, Bash` plus explicit prohibitions on browser automation, downloads, and self-authored research scripts. Without it the agent inherits every host tool; under Copilot/VS Code that produced ~100 opened editor tabs in one run. Do not widen it casually.

There is exactly one carve-out: a `WebFetch` that fails on a URL may be retried once via `crwl crawl "<url>" -o markdown | head -c 40000`, only if `crwl` is already installed. Every clause of that rule is doing work — already-failed, one retry, same fetch slot, stdout only, bounded output, no `--deep-crawl`, no `-O`, no install, no second helper. Loosen any one and it becomes general permission to script around blocks, which is the behavior the allowlist exists to stop. The prompt also explains why this is not browser automation (headless, one-shot, opens nothing) — keep that reasoning, or the agent refuses its own exception.

**`validate_json.py` derives categories from the `fields.yaml` it is given**, falling back to `CATEGORY_MAPPING` for the original AI-coding-assistants topic. Keep it topic-agnostic — hardcoding categories re-breaks every other research topic.

It expects a top-level `field_categories:` list (`- category: X` / `fields: - name: y`). Any other shape parses to zero fields, which used to make every JSON trivially 100% covered and report `[PASS]`; it now exits 2 instead. Do not relax that guard — `/research-deep` gates task completion on this exit code, so a false pass silently accepts unresearched output.

## Authoring a search module

Prefer `/research-add-module` over writing one by hand: it searches to discover which sources actually hold a domain's answers, tests how to query each one, and verifies the result beats `general-web` before keeping it. A hand-written source list is a guess, and guessed sources route the agent to plausible sites that turn out to be empty. Modules do not self-update by design — re-run the skill or edit by hand.

Reference files, not code. Under ~40 lines: a one-line trigger description, a prioritized source list noting what each source is good for, and query tactics that actually work in that domain. Length is a real cost — the file enters the agent's context on every routed task, and the agent loads at most two per task, so each module must cover a coherent domain rather than a grab bag.

Every module needs the routing header (`Family` / `Use when` / `Do not use for` / `Siblings`), a prioritized source list, and query tactics specific to the domain. The five upstream modules retain Chinese section headers (`## 搜索源`, `## 查询策略`); new modules should be written in English. `skills/web-search-modules/SKILL.md` keeps a **Wanted** list of modules judged worth adding — check it before inventing a new domain.

Non-technical families attach the same way as technical ones: one new family row with its own question. Nothing in the existing routing changes to make room for them.

## README conventions

`README.md` documents divergence from upstream under **Changes from upstream**, currently split into *Packaging* and *Fixes*. New capability (search modules, new pipeline features) belongs under an **Additions** heading rather than being filed as a fix — a fix repairs upstream behavior that was broken, an addition is behavior upstream never had. Keep the numbering continuous and the Credit section intact.
