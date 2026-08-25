# PLAN.md

> Authoritative record of **decisions made** for deep-research-agent. Living document, built up across sessions. Read at the start of any planning/design conversation. **Append** decisions as they're made; don't rewrite.
>
> This is the **hot layer** — keep it lean. Cooled material lives in `docs/` (see below). When it grows heavy (default >15000 words), invoke the **`living-plan`** skill. That same skill's `grill` workflow is what **fills** the sections below — decisions don't have to trickle in one at a time from whatever a session happened to touch.

## Overview

An APM-installable bundle of prompts and data: the `/research*` skills, the `web-search-agent` subagent they launch by name, and the strategy modules that agent routes into. Forked from [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) (MIT, Lan Zheng) and rebuilt where it was broken — no search budget, no stop condition, a hardcoded path that broke its own validation step.

There is no build and no test suite. **Editing a file here is editing a prompt** — wording, ordering, and emphasis are the implementation, and a rewrite that reads better but drops a hard constraint is a regression. Full architecture and the failure modes worth knowing live in `CLAUDE.md`; this file records only what was *decided* and why.

## Decisions

> Whole and inline while hot. Mark load-bearing ones `🔒 foundational` so rebalancing never archives them. Cooled decisions collapse to a one-line pointer into `docs/decisions/`.

<!-- D1 — Access methods: three kinds of module -->
### D1 — Three kinds of module, three meanings of "access method" 🔒 foundational

`skills/web-search-modules/SKILL.md:36` requires every source to carry an access method — "a `site:` query, a tested search-URL pattern, a stable index page to fetch directly, or a note that it blocks fetching" — because "a name without an access method makes the agent rediscover the same thing every run." As of 2026-08-21 **`site:` appears zero times across all ten modules**; the spec and the payload disagree completely.

The requirement does not mean the same thing for every module, and treating it as uniform is what would break the retrofit:

| Kind | Modules | What "compliant" means |
|---|---|---|
| **Fixed-site** | `github-debug`, `stackoverflow`, `academic-papers`, `chinese-tech` | The source *is* a website. A literal `site:` query. Stable indefinitely; never needs accumulating. |
| **Parameterized** | `pricing`, `benchmarks`, `model-releases`, `vendor-landscape` | "The vendor's own pricing page" — which site depends on the vendor the question names. Compliance is a **URL pattern plus a seed list** of vendors that actually recur, not a fixed URL. |
| **Open-query** | `general-web`, `competitor-content` | Sources are whatever the query returned. The correct access method is an explicit **"none by design"** note — the spec's fourth form. |

**Why this is foundational:** without it a retrofit pass invents plausible URLs for the open-query modules and damages the thing they do well. `competitor-content` samples an unrefined reader-query search on purpose; pinning it to a source list would defeat it. A guessed URL is *worse* than no URL, because the agent trusts it and spends a fetch on a 404 instead of falling back to search.

**Corollary — the line budget binds.** Modules are 12–31 lines against SKILL.md's ~40-line ceiling, which exists because the file enters the agent's context whole on every routed task. Access methods must be **appended to existing source bullets**, not added as new lines. `academic-papers.md` (31 lines, 7 sources) has almost no headroom.

<!-- D2 — No speculative modules -->
### D2 — No new modules until a real project needs one

Decided 2026-08-21. The wanted modules in `ROADMAP.md` (AI writing/prompting communities, docs-and-API-reference) stay parked until a live project hits the gap.

**Why:** `/research-add-module` exists because it *discovers and tests* which sources actually hold a domain's answers rather than guessing. A module written speculatively — before a real question has been asked of it — is a hand-written source list by another name, which `CLAUDE.md:110` already names as the failure mode: "guessed sources route the agent to plausible sites that turn out to be empty." Waiting for real demand is what makes the discovery step meaningful.

This also means the module count is not a health metric. Ten well-accessed modules beat fifteen with empty source lists.

<!-- D3 — One research root per project -->
### D3 — One research root per project, discovered structurally 🔒 foundational

Decided 2026-08-22. Every run folder lives inside a single root, default `research/`, instead of scattering `{topic_slug}/` directories across the project root.

**Why:** the pipeline is used inside repos where the user is also writing code. The live consumer `writing-model-research` has `llm-writing-benchmark-landscape/` sitting next to `benchmarks/`, `harness/`, `docs/`, and `client-voice-finetuning/`, and nothing about the name says which of those is pipeline output. One root also gives the branch record (D4) somewhere to live.

The root name is a per-project choice, asked once at the first `/research` and **never written to a config file**. Discovery is structural instead: a *run folder* is any directory containing `outline.yaml`; skills glob `*/outline.yaml` **and** `*/*/outline.yaml`, and the root is simply the parent of a run folder when that parent is not the cwd. That is what keeps a renamed root and every pre-existing root-level run working with no migration, and it is why there is no `.researchrc`.

Two consequences that would otherwise break quietly:

- **`output_dir` is relative to the run folder**, not to the cwd. This was always ambiguous — `./results` read one way at the old depth and a different way once nested — so every skill now states it outright.
- **Multiple runs is the normal case, not an edge case.** `Find */outline.yaml in current working directory` assumed exactly one. Every locate step must disambiguate, which is why `/research-deep` needs `AskUserQuestion` in an allowlist that did not have it.

Migration of existing root-level runs is **offered, never automatic** — `/research` lists exactly what it would move and waits for confirmation. Moving directories in someone's repo is not a side effect of asking for research.

<!-- D4 — INDEX.md is the branch record -->
### D4 — `research/INDEX.md` is the branch record, not a directory listing

Research doesn't run once. One search indicates the next direction, which indicates the next, and the shape of that tree is currently recorded nowhere — it lives in the user's memory between sessions.

`INDEX.md` at the root records it: a `## Map` of nested bullets showing which run spawned which, then one `##` section per run carrying its purpose, status, the report's summary paragraphs and headline table, and a `**Leads**` checklist of the directions that run surfaced. A lead nobody has started is a leaf in the Map with no section of its own; when it becomes a run, its parent's checkbox is ticked and points at the new folder.

Three skills own different parts and none rewrites another's: `/research` appends the stub (purpose, date, status `outline`, parent link), `/research-deep` flips status, `/research-report` fills the summary body and asks the user which leads came out of it.

The summary body is **capped** — ≤3 paragraphs, ≤12 table rows, then a pointer into `report.md`. The index is read whole by every skill that touches it, and a 24-item table per entry (the size the live consumer's report actually is) makes the file unreadable within three runs.

<!-- D5 — Layout lives in exactly one payload file -->
### D5 — Layout and discovery live in exactly one payload file

`skills/research/LAYOUT.md`, read by every skill at its locate step — the same architecture as `ROUTING.md` being the single source of truth for module selection.

**Why not inline it in each skill:** five skills need identical discovery rules and three need identical index-writing rules. `CLAUDE.md` already records what duplication costs in this repo — the depth/budget table lives in two files and changing the numbers means changing both, which is documented as a thing that breaks quietly rather than as a design.

**Why not `CLAUDE.md`:** skills do not read it and APM does not install it. A contract the payload has to honor has to live in the payload.

<!-- D6 — Runtime-specific agent wrappers, runtime-neutral resources -->
### D6 — Keep one research prompt, add runtime-native agent entry points 🔒 foundational

Decided 2026-08-25 after mining Copilot session `56cc0499-1dd1-4148-9027-059a235aac6b` from `tpo-copilot-desktop-research`. APM 0.16 deployed the same `web-search-agent` definition into both `.claude/agents/` and `.github/agents/`; Copilot registered the duplicate name, then launched the agent with zero tools because APM passes the Claude allowlist (`WebSearch, WebFetch, Read, Write, Bash`) verbatim while Copilot expects capability categories (`read, search, web, edit, execute`). A uniquely named Copilot-native wrapper using those categories completed all three research items.

The existing `web-search-agent` name and prompt remain the Claude-compatible canonical implementation so current consumers do not break. Copilot gets the proven `Web Research Writer` wrapper, which loads and follows that canonical prompt but owns Copilot-native frontmatter. Orchestration skills select the entry point by exact registered name and host. Resource lookup is runtime-neutral: current shared `.agents/skills/` first, legacy `.claude/skills/` retained as fallback. Install docs require an explicit APM target so filesystem auto-detection cannot silently activate both harnesses.

**Why not one universal agent file:** APM's current authoring contract deploys `model` and `tools` verbatim to both Copilot and Claude. Their tool names are not portable, and removing the allowlist would restore the failure that opened roughly 100 browser tabs. Two thin entry points preserve the boundary without duplicating the research method.

## Open questions

> Each is a heading (the question) + a link to its discussion in `docs/questions/`. Thread files are append-only — a later grill adds a dated section rather than rewriting.

### Q1 — Should modules accumulate sources over time, and which kind can?

See [docs/questions/Q1-source-accumulation.md](docs/questions/Q1-source-accumulation.md).

### Q2 — What makes an access method "tested"?

See [docs/questions/Q2-tested-access-method.md](docs/questions/Q2-tested-access-method.md).

## Parking lot

> Deferred ideas. Each is a one-line hook + a link to `docs/parking-lot/`.

- **Harvest sources from completed runs into a local module** — [docs/parking-lot/harvest-from-runs.md](docs/parking-lot/harvest-from-runs.md)
- **Rewrite `stackoverflow.md`** — 12 lines, two vague source bullets, zero query tactics; a rewrite, not a retrofit — [docs/parking-lot/stackoverflow-rewrite.md](docs/parking-lot/stackoverflow-rewrite.md)
- **Non-technical families** (health, law and policy, finance) — attach when a project needs one; `competitor-content` is the worked example — [docs/parking-lot/non-technical-families.md](docs/parking-lot/non-technical-families.md)
- **Wanted modules** (AI writing communities, docs-and-API-reference) — parked under D2 until real demand — [docs/parking-lot/wanted-modules.md](docs/parking-lot/wanted-modules.md)
- **Verify the `crwl` fetch fallback** against a genuine 403 or JS-shell page — never fired in a live run — [docs/parking-lot/verify-crwl-fallback.md](docs/parking-lot/verify-crwl-fallback.md)

## Session log

> Most recent sessions inline; older sessions archived → see `docs/sessions/`.

### Session 3 — 2026-08-25

Mined the only non-empty Copilot session in `tpo-copilot-desktop-research` and traced the failed installed pipeline. The package was simultaneously active for Claude and Copilot, producing duplicate `web-search-agent` registrations; the Copilot child received no tools even though the Claude allowlist was present. A user-created `.github/agents/web-research-writer.agent.md` with Copilot-native tool categories succeeded. Decided D6 and queued the portability retrofit ahead of the untouched access-method task.

### Session 2 — 2026-08-22

Results organization. Raised from the parking lot: run folders land at the project root, which is wrong in every repo where the research sits alongside code, and nothing anywhere records that one run's findings pointed at the next.

- Decided **D3** (one root, default `research/`, discovered structurally rather than configured), **D4** (`INDEX.md` as the branch record — Map, per-run summary, Leads), and **D5** (`skills/research/LAYOUT.md` is the single source of truth, the `ROUTING.md` pattern).
- Two latent bugs surfaced while designing it: `output_dir`'s base directory was never stated (it reads differently once nested), and `research-deep`'s validator example teaches a `{project_dir}/../.claude/…` relative path that goes one level too shallow under the new layout.
- Queued the six-piece implementation ahead of the access-method retrofit, which moves to ⏸ QUEUED untouched.
- **Shipped it the same session** (`[results-root]` in `TASKS.md`). Review caught three things the implementation missed, all now fixed: the status ladder was lossy (a researched-but-unreported run read as `researching` — split into four states), legacy root-level runs have no index and every index-writing step must skip rather than create one, and `/research-report` still ran `python {topic}/generate_report.py` from the cwd, which is one level too shallow once runs nest. `{run_dir}` and `{project_dir}` are now defined at each locate step instead of being implied.

### Session 1 — 2026-08-21

Scaffolded the planning workflow. Before that, resolved a long-standing loose end: the **external task mirror**.

- Found that a bidirectional plan/vault sync (`PLAN SYNC`) had been **built** months earlier in the `vault-writer` skill and **never wired up** — zero vault notes carried `plan-repo:`, including the one the skill used as its own worked example. The design was sound (asymmetric authority: status repo→vault, new items vault→repo, priority vault-only, prose never); it was simply unreachable.
- Generalized it: `plan-file:` (defaults `TASKS.md`) so any markdown checklist works, a guard that refuses prose files outright, and a rule that new items land in an **intake section** (parking lot / backlog / `Next` tier) rather than active work — because discovering work and scheduling work are different authorities.
- Added a generic **External task mirror** pointer to `living-plan` itself (conductor-only, opaque path, zero vault vocabulary) so the mirror is named at scaffold time instead of being forgotten. Retrofitted 4 projects + this repo.
- Decided D1 and D2 above. Queued the access-method retrofit.

## Relocated (progressive disclosure)

- Decisions archive → [docs/decisions/](docs/decisions/)
- Questions detail → [docs/questions/](docs/questions/)
- Parking-lot detail → [docs/parking-lot/](docs/parking-lot/)
- Session archive → [docs/sessions/](docs/sessions/)
- Rebalance log → [docs/rebalance-log.md](docs/rebalance-log.md)
