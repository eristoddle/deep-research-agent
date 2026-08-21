# PLAN.md

> Authoritative record of **decisions made** for deep-research-agent. Living document, built up across sessions. Read at the start of any planning/design conversation. **Append** decisions as they're made; don't rewrite.
>
> This is the **hot layer** — keep it lean. Cooled material lives in `docs/` (see below). When it grows heavy (default >15000 words), invoke the **`living-plan`** skill.

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

## Open questions

> Each is a heading (the question) + a link to its discussion in `docs/questions/`.

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
