# Rebalance log

Ledger for the `living-plan` skill. One entry per run.

## Config

- **planning doc:** `PLAN.md` (repo root)
- **task doc:** `TASKS.md` (repo root)
- **conductor:** `CLAUDE.md` (real file, not a symlink; no `AGENTS.md`)
- **agent dir:** `.claude/agents/` — **not** `agents/`
- **threshold:** 15000 words (default)
- **external task mirror:** the project's Obsidian note (path in `CLAUDE.md`); reconciled by `vault-writer`'s PLAN SYNC

> **Two repo-specific hazards for any future run.**
>
> 1. **`agents/` at the repo root is shipped APM payload, not a dev agent dir.** APM flattens every `.md` beneath `agents/` into a separate top-level agent when installing from a git source. A planning or implementer agent written there would install itself into every consumer project. The implementer lives in `.claude/agents/` for this reason.
> 2. **This repo is prompts, not code.** There is no build and no test suite, so a rebalance that "tidies" wording in a skill or module can silently drop a hard constraint with nothing to catch it. Relocating a whole section is safe; rewriting sentences is not.

## Runs

### 2026-08-21 — scaffold

Greenfield. Created `PLAN.md`, `TASKS.md`, `.claude/agents/implementer.md`, the `docs/` tree, and this log. Appended the planning blurb + external-task-mirror pointer to `CLAUDE.md`, replacing the interim § *Where the task list lives*.

Seeded with two decisions (D1 access-method kinds 🔒, D2 no speculative modules), two open questions (Q1 source accumulation, Q2 what "tested" means), five parking-lot items, and one active task (the access-method retrofit, 6 pieces).

Deviations from the template, both deliberate: the implementer carries `WebFetch, WebSearch` beyond the template's tool list (verifying an access method *is* fetching the URL), and "keep the suite green" was rewritten into three concrete checks since no suite exists.

### 2026-09-03 — grill (round 1)

Mode B, continuing. Entry: user asked for planning after a design conversation about supporting a web-clip article's research process. Planning-only session, nothing built.

**Seeded** from 6 decisions, 2 open questions, 5 parking-lot items. Three parked items reactivated by new material: `search-layer-refusals` (its proposed fix falsified), `wanted-modules` (D2 trigger supplied), `harvest-from-runs` (sibling of the new ledger idea).

**One round, 6 questions, all answered.**

- **Decided → D7 🔒** (no silent substitution), **D8 🔨** (access methods in one shared file; fourth form becomes a directive), **D9 🔨** (`demand-signals`, research stage, Reddit-free), **D10 🔨** (fetch-outcome ledger, failures-only negative cache).
- **Opened → Q3** (is Reddit reachable, and from where — firecrawl untested), **Q4** (ledger mechanics: location, write carve-out, expiry).
- **Amended** `docs/parking-lot/search-layer-refusals.md` (all four of its open questions dispositioned) and `docs/questions/Q2-tested-access-method.md` (its staleness half may close via D10).
- **Nothing queued** to `TASKS.md`; the access-method retrofit remains active and untouched.

**Facts gathered during the round** rather than asked of the user: five reachability routes tested live (WebSearch `site:`, WebFetch on two hosts, `curl` + UA to `.json`, `crwl`).

**Correction from the user, worth carrying into future runs:** the agent stated reachability in absolute terms from single-machine evidence. The plan is destined for a different computer, and two of five failing routes are IP-scoped while one is harness-scoped. Q3 was written to carry the **procedure**, not the conclusion. Watch for this whenever a grill turns a live test into a decision.
