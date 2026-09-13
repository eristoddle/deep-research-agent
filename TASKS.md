# TASKS — deep-research-agent

> The unit of implementation work. Written by the planning thread once a decision in `PLAN.md` is concrete enough to build, executed by the `implementer` agent in its own context window.
>
> **The active task is a serial QUEUE of numbered pieces** (1, 2, 3…) — tightly-related steps of one job, or a stack of independent jobs; doesn't matter, stack as many as you want. Two rhythms this serves:
> - **Pacing** — queue a little, plan the next batch while the agent grinds.
> - **Unattended** — queue a lot and walk away; the agent chews the whole queue.
>
> **Execution (default = synchronous, one agent):** work the queue top-to-bottom. A blocked piece does **not** halt the queue — skip it and continue with any piece that doesn't depend on it (mark deps inline: `depends on #2`); halt only when nothing remaining can proceed. **Always log run-state on stop** (done or blocked): flip each piece's status box as you go and update the ▶ Run state note, so a killed/forgotten session is recoverable from this file on disk.
>
> **`Reversible if:`** — every task carries a one-line field naming any open question whose answer would undo part of the work, or `—` when none applies. Work resting on a provisional finding also gets a greppable tag in the file itself (PLAN.md **D12**), so the *what* and the *where* are both recoverable.
>
> **Contract:** fill every section before launching. Mark a section `—` only if it genuinely doesn't apply. The agent is *cold on the planning conversation* but *warm on the project* (it has `CLAUDE.md` + the codebase) — reference decisions and files by pointer; don't re-explain the repo.
>
> Completed work collapses to a one-block summary with a stable `[tag]` under **✅ Done**; the full detail lives in `PLAN.md`'s session log.

---

# ⏭ NEXT ACTIVE TASK — `/research-enumerate`: the breadth-first catalog sweep

**Goal:** A new `/research-enumerate` skill that sweeps broad and shallow to find out *what exists*, writes a `catalog.md` deliverable plus a standard `outline.yaml` into a run folder under the research root, and appends its `INDEX.md` stub — changing no existing layout, routing, or budget rule.

**Why:** `PLAN.md` **D19**. The package has exactly one shape of work — depth per item — and it is the wrong tool when the hard part is *finding the items at all* and each needs three shallow facts. The design is not speculative: it is derived from a complete worked run, `_seo/research/ai-affiliate-programs-2026-09-12/` in the `sm-static` project (four files: `providers.md`, `standalone.md`, and a round 2 of each), which both succeeded and failed in ways that settled the open questions.

**Reversible if:** — (D19 closes every question this rested on; the parked doc's "feeder mode" is decided-against, not deferred-pending-an-answer.)

**Read first:** `PLAN.md` **D19** (the whole decision — it carries the evidence and the four contributed rules), `docs/parking-lot/enumeration-pass.md` (the tactics, which remain correct), `skills/research/LAYOUT.md` (discovery, `{run_dir}`, `INDEX.md`, who-writes-what), `skills/research-harvest/SKILL.md` (the most recent skill, and the shape to match), and `skills/research-deep/SKILL.md` **lines 30-60** for the host-selection rule and the hard-constrained prompt-template convention.

**Read the four sm-static files before writing anything.** They are the specification's evidence and they are outside this repo at `/Users/eristoddle/Dropbox/xampp/htdocs/sm-static/_seo/research/ai-affiliate-programs-2026-09-12/`. Read them bounded (`sed -n`, `head`) — they total ~550 lines. Do not edit anything in that project; it is a consumer repo and out of scope per `AGENTS.md`.

**Design:**

## 1. The skill file

[ ] Create `skills/research-enumerate/SKILL.md`. Frontmatter exactly in the shape of `research-harvest`'s: `name: research-enumerate`, `user-invocable: true`, a one-line `description`, and `allowed-tools: Bash, Read, Write, Glob, AskUserQuestion`. **Target 80-110 lines** — between `research-report` (107) and `research-deep` (170); if it runs longer, the prompt template is carrying prose that belongs in the decision record.

[ ] **Locate step defers to `LAYOUT.md`.** State that the run folder is created new under the root and do not restate the discovery rule — `AGENTS.md` is explicit that layout lives in exactly one file. Ask for the root once, per the existing convention, only if none exists.

[ ] **Host selection rule, copied verbatim** from `research-deep/SKILL.md:36`: in GitHub Copilot launch `Web Research Writer`; in Claude Code launch `web-search-agent`. **No new agent is created** (D19) — this is the single most important constraint in the task. If writing the skill seems to require a new agent, stop and report rather than adding one.

## 2. Inputs the sweep takes

[ ] **A taxonomy is required, not optional.** The sweep needs an axis of categories to sweep along and to report coverage against; the affiliate run used five. Ask for it via `AskUserQuestion` if the invocation did not supply one, and offer to propose a starting taxonomy the user edits — but the run does not start without one, because without categories "done" is unfalsifiable.

[ ] **An exclusion list is a first-class input**, not an ad-hoc paragraph. The caller usually already knows part of the answer, and round 2 of the affiliate run used exactly this to keep output to genuinely new material. Accept it as a list of names, or as a path to an existing `catalog.md` whose entries are all treated as known.

[ ] **Shallow field set, 3-5 fields.** The point is a link, a one-line description of what the thing is, and whatever terms are public. This is not `fields.yaml` and the sweep does not write one — `/research-add-fields` exists for the descend path.

## 3. The two-phase sweep, with a coverage-based stopping rule

[ ] **Phase 1 — aggregators. Phase 2 — one-offs.** Before enumerating leaves, look for the thing that lists the leaves: directories, marketplaces, registries, awesome-lists, category pages. One aggregator can yield dozens of items at once, which is why it runs first and why phase 2's much lower yield per search runs second. State this as the sweep's governing tactic, in domain-independent terms — the affiliate case is the example, never the subject.

[ ] **Budget is per-phase, not per-item**, and this is the rule the worked run broke. Do **not** reuse the `quick`/`standard`/`deep` table — it is per-item and duplicated in two files already, and widening it to cover sweeps would make a third duplication. Define the enumeration budget in this skill alone: **20 searches and 20 fetches per phase**, which is what the observed runs actually consumed (17/13 and 20/17) before the one that overran.

[ ] **The stopping rule is coverage, not exhaustion.** The affiliate run's own disclosure is the evidence: 29 searches against a 20-search ceiling, caught only at compile time, and a round 1 that ran out mid-category. Require the agent to report searches and fetches used **per phase as it goes**, and to stop at the ceiling and declare the gap rather than continuing and disclosing afterward. A phase that hits its ceiling with categories still uncovered is a *successful* run with an honest coverage gap, not a failure.

## 4. The output contract

[ ] **`catalog.md`** is the deliverable, in `{run_dir}`. One section per taxonomy category, each with a table of found items carrying the shallow fields. It ends with `## Unreachable`, `## Sources`, and `## Uncertain` — **reuse those three section names exactly** (D11, D17, and the base contract, rendered as markdown because the deliverable is prose rather than `results/*.json`). Do not invent a parallel vocabulary for the same three facts.

[ ] **Three negative states, each with its own labelled subsection per category** — this is the load-bearing output rule and it is **D7** applied to enumeration:
  - *Checked, none found* — searched properly, there is nothing there. A real result.
  - *Checked, inconclusive* — found something, could not confirm it from a source that counts.
  - *Not checked — budget exhausted* — **never silently omitted.** A category the sweep never reached must say so, or its absence reads as a negative result to every later reader.

[ ] **A blank is a result; a guess is damage.** Where a value is not publicly stated, the field reads exactly `not public`. An inferred figure is worse than an empty cell, because a plausible fabricated number is indistinguishable from a real one at review time. The affiliate run held this line and said so in three of its four files — keep the rule that explicit.

[ ] **`outline.yaml`**, in the same run folder, in the standard shape: `items[]` from what the sweep found, plus an `execution{}` block with the package defaults. This is the whole of D19's no-structural-change claim — the folder contains an `outline.yaml`, so `LAYOUT.md`'s existing glob discovers it, `INDEX.md` lists it, and `/research-deep` can descend on it later with no new wiring. Do not add `catalog.md` to any discovery rule.

[ ] **Append the `INDEX.md` stub** exactly as `/research` does — purpose line, `date · N items · depth · status`, status **`outline`**, `Spawned from:` if applicable. Status `outline` is correct and is not a placeholder: items exist and nothing has been deep-researched. Per `LAYOUT.md`, if the run folder has no root above it, **skip this step silently** rather than creating an index beside it.

[ ] **Round 2 is a documented re-invocation, not a separate mode.** Point `/research-enumerate` at an existing run folder plus an exclusion list, and it appends new findings to `catalog.md` and new items to `outline.yaml` with a fresh per-phase budget. One paragraph in the skill; no second code path.

## 5. The prompt template

[ ] The sweep agent's brief is a **`Hard Constraint` prompt template**, in the established form ("strictly reproduce, only replacing `{xxx}`"). The per-phase budget, the three negative states, the `not public` rule, and the tool prohibitions must sit **inside** the template so they survive the handoff — `AGENTS.md` is explicit that restructuring a template drops these silently and the run still completes, just unbounded.

[ ] Give the template a **one-shot example directly below it**, per the house rule that every template has one and the two must change in lockstep. Keep the example short — a three-row table with one `not public`, one `Checked, none found`, and one `Not checked` line is enough to teach the format.

## 6. Documentation

[ ] `README.md`: add `/research-enumerate` to the Usage list, and one **Additions** entry **23**, continuing the numbering. One paragraph: what question it answers, why the per-item pipeline could not, and the coverage-declaration rule as its actual discipline rather than a nicety.

[ ] `ROADMAP.md`: the enumeration pass is no longer an intention. Add a short section in the register of the existing landed sections, naming the worked run as its evidence and the per-phase budget as what replaced the per-item one.

**Files:**
- `skills/research-enumerate/SKILL.md` (new)
- `README.md`, `ROADMAP.md`
- `TASKS.md` (piece status and run state only)

**Tests:**
1. `wc -l skills/research-enumerate/SKILL.md` — within 80-110.
2. Frontmatter matches `research-harvest`'s shape; `allowed-tools` is exactly `Bash, Read, Write, Glob, AskUserQuestion`.
3. **No new agent file exists.** `git status --porcelain agents/ .claude/agents/` is empty, and the skill names `web-search-agent` / `Web Research Writer` per the host-selection rule. Read the output, do not trust the exit code — a grep that passes by not looking has happened three times in this repo.
4. The skill does **not** restate `LAYOUT.md`'s discovery rule. `rg -n 'outline\.yaml' skills/research-enumerate/SKILL.md` — read every hit; the only legitimate ones are *writing* the file and the sentence explaining why writing it keeps discovery unchanged.
5. `git diff skills/research/LAYOUT.md` is **empty**. Same for `skills/web-search-modules/ROUTING.md` and the depth/budget tables in `agents/web-search-agent.md` and `skills/research-deep/SKILL.md`. D19's entire claim is that none of these move.
6. The three negative-state labels and the exact string `not public` all appear inside the hard-constrained prompt template, not only in surrounding prose. Verify by reading the template block itself.
7. `catalog.md`'s contract names `## Unreachable`, `## Sources`, `## Uncertain` — the existing spellings, no synonyms.
8. The template and its one-shot example teach the same format: same columns, same negative-state labels, same `not public` spelling.
9. README Additions numbering runs 1-23 with no gaps or repeats.
10. `git diff --check`.

**Out of scope:**
- **Any new agent**, any change to either agent's `tools:` allowlist, and any change to the `quick`/`standard`/`deep` table.
- **Feeder mode** — deriving `/research`'s Step 1 item list from a sweep. D19 decides against building it; the composition path is `/research-add-fields` then `/research-deep` on the folder the sweep already wrote.
- Any change to `LAYOUT.md`, `ROUTING.md`, `INDEX.md`'s format, or the status ladder.
- Any new module, and any edit to `skills/web-search-modules/`. Both round-2 files routed to `general-web`; directory-mining may be module-shaped later and nothing here depends on it.
- Editing anything in `sm-static` or any other consumer project — read-only evidence.
- `PLAN.md` (the planning thread owns it) and `AGENTS.md`.

**Report back:** Each piece completed or blocked; the final line count and what you cut to hit it; the exact per-phase budget numbers you wrote and whether the observed 17/13 and 20/17 figures justified them or you had reason to differ; how you worded the `Not checked — budget exhausted` state, since that is the rule most likely to be softened into something that reads better and says less; whether the template and its one-shot example genuinely teach the same format; and anything in D19 that turned out underspecified when you built against it.

> ▶ Run state: not started.

---

## ✅ Done (collapsed — full detail in the planning doc's session log)

### `[demand-signals]` D9: build the module through discovery — 2026-09-05

All 5 pieces landed, none blocked, all 10 Tests passed. `demand-signals` shipped as its own family after beating `general-web` in the piece-4 comparison, built by actually running `/research-add-module`'s discovery pass across five venue classes rather than from a guessed source list. Reviewed in the planning thread — both live endpoints re-verified independently, and one clause added there: **Trustpilot's low-star reviews skew hard toward billing, refunds, and support** rather than product gaps, so the bullet now says so and points at the forum bullet for "what the product cannot do." Without it the module answers "what's missing from budgeting apps" with a page of refund complaints. `PLAN.md` **D9**.

### `[harvest]` D17 harvest half: `/research-harvest` — 2026-09-05

All 3 pieces landed, none blocked, all 9 Tests passed against a synthetic fixture (live verification is impossible from this checkout — no run anywhere has captured sources yet, which D17's amendment settles as a separate later check). New `skills/research/harvest_sources.py` is a read-only tally: it discovers runs per LAYOUT.md, reads each run's `output_dir` relative to its run folder, and counts each source URL by runs-appeared-in and runs-where-it-supported-a-field. New `/research-harvest` is hand-invoked only, resolves the script by the same four-path lookup `/research-deep` uses for the validator, and writes `.agents/web-search-modules-local/CANDIDATES.md` — regenerated whole each run, but ticked or struck entries move to `## Dispositioned` and never return as fresh candidates. README gained `/research-harvest` in Usage plus Additions 19-21 (the list had stopped at 18 and was missing three shipped capabilities); ROADMAP's two stale sections now read as landed. `PLAN.md` **D17/D18**.

**Review found the two run states D17 named are three.** A run folder holding only an `outline.yaml` — made by `/research` and never researched — was classified `no-capture` and therefore reported as *predates source capture*, the opposite of the truth, and on the most likely first invocation of all: harvesting straight after making an outline. Fixed in the planning thread; runs are now `captured` / `no-capture` / `no-results`, the third with its own sentence in both script and skill.

Also worth keeping: the task's own justification for avoiding PyYAML ("not a dependency anywhere in this package") was **false** — `validate_json.py:9` imports it. The design was unaffected (harvest needs one scalar out of `outline.yaml`, so a line-oriented read is still right), but a task can hand the implementer a true instruction for a false reason, and the agent catching it is why the report-back asks what turned out underspecified.

### `[source-capture]` D17 capture half: record which sources answered — 2026-09-04

All 4 pieces landed, none blocked, all 6 Tests passed. `results/*.json` may now carry a top-level `sources[]` array — entries of exactly `{source, url, fields}`, where `fields` names the fields that source actually supported. The contract lives in the agent prompt (`agents/web-search-agent.md`) rather than in a `fields.yaml` convention, and is mirrored into `/research-deep`'s hard-constrained template *and* its one-shot example in lockstep. Only sources that contributed to an answer are recorded — a page opened and unused is not provenance, and a page that failed is already `unreachable[]`'s job. `validate_json.py`'s `_SKIP_KEYS` gained both `sources` and `unreachable` (the latter missed when that array shipped the same day). `/research-report` renders sources only when the invoking prompt asks, in natural language — deliberately unlike `unreachable[]`, which renders by default. `PLAN.md` **D17**.

### `[helper-firecrawl]` The approved package helper and Firecrawl's third fetch rung — 2026-09-04

All 3 pieces landed, none blocked. The fetch contract is now a three-rung ladder for a single blocked URL — `WebFetch` → `crwl` → Firecrawl — with the paid rung gated on both `command -v firecrawl` and a configured `FIRECRAWL_API_KEY`, writing to an item-specific temp file that is bounded-read at 40,000 bytes and then deleted. `skills/research/reddit_feed.py` became the one approved package helper an item agent may invoke, with a new `--max-attempts` option (default 5, nonpositive values rejected before any network call) that caps its `429` backoff at the item's remaining budget. `PLAN.md` **D15/D16**.

**The fetch budget was redefined rather than extended**: it now counts every network retrieval attempt, not just native `WebFetch` calls. Without that, the two new rungs and the helper's retries would have been free — the exact overspend the budget exists to prevent. A blocked page's whole ladder remains one logical fetch sequence; the helper's attempts each cost a slot.

Firecrawl's invocation was pinned by running it once against a control page on an opted-in machine: it writes plain Markdown to `-o` with no JSON envelope and prints only a one-line scrape ID, which is why the bounded form is temp-file-then-delete rather than a stdout pipe like `crwl`'s. That live check is what the previous session deferred for lack of a configured key.

Verified: all 6 Tests passed, including template/one-shot-example lockstep in `skills/research-deep/SKILL.md` and `git diff --check`. Reviewed in the planning thread — nothing needed reverting. **The task's own Test 5 `rg` was scoped to the eight files it edited**, so a repo-wide grep was needed to confirm no stale Reddit directive survived elsewhere; it surfaced two hits in `web-search-modules/SKILL.md` that are the authoring guidance for the fourth-form directive pattern, still correct and correctly untouched. Same shape as the case-sensitive `reddit` grep in `[access-methods]`: a test that can pass by not looking.

### `[unreachable-output]` Separate unreachable-source provenance from unanswered fields — 2026-09-04

All 3 pieces landed, none blocked. `results/*.json` can now carry an `unreachable[]` array whose entries are `{source, url, reason}`. The canonical agent and `/research-deep` handoff treat `fetch_failed` and `zero_domain_results` as provenance annotations, never as a reason to mark a field answered through a documented substitute as uncertain. `/research-report` now directs generated reports to deduplicate those entries by source, URL, and reason, then render a reader-visible `## Unreachable sources` section with affected items. The deep-research template and its one-shot example remain in lockstep. `PLAN.md` **D11**.

Verified: required contract search, template/example comparison, report semantics, `python3 -m py_compile skills/research/validate_json.py`, and `git diff --check` all passed.

### `[site-files]` A referenced site layer, earned by recurrence — 2026-09-03

All 5 pieces landed, none blocked. `skills/web-search-modules/sites/` now holds **seven** files (81 lines total) for the sites more than one module cites: GitHub, Reddit, Hugging Face, OpenRouter, Hacker News, `dev.to`, Artificial Analysis. Each carries `Used by:`, a dated `Reachable:` line, the query method, and what wastes budget. Every citing module gained a path citation while keeping its own self-sufficient access method — a bullet reduced to a bare pointer would strand the agent mid-run. `ACCESS.md` gave up its Reddit section (39 → 30 lines) and keeps only what has no site to live in. `PLAN.md` **D14**.

The `[ACCESS:reddit]` markers added earlier the same day are gone: the path citation *is* the tag, and `grep -rl "sites/reddit.md"` returns the revert list.

**The agent caught a counting error in the task's own premise**, which is the result worth keeping. D14's module counts came from a prose name-match that scored things that were not citations: routing-header cross-references to the sibling *module* `github-debug`, a "similar to Stack Overflow" comparison, and `v2ex.com` matching the substring `x.com`. Real counts are GitHub 4 (not 6), Stack Overflow 1 (not 3), Twitter/X 1 (not 2). Two files were built below their own threshold and removed after review — Twitter/X had no method written anywhere, and Stack Overflow's held only what its module bullet already said. Stack Overflow gets its file when the parked rewrite lands, which is when there is finally something to overflow.


### `[access-methods]` Access-method retrofit across the ten pre-`agent-tooling` modules — 2026-09-03

All 7 pieces landed, none blocked. Every source bullet in the ten modules now carries an access method in the form its kind calls for — literal `site:` queries for fixed-site modules, URL patterns plus verified seed lists for parameterized ones, an explicit "none by design" note for the two open-query ones. `SKILL.md` gained the three-kind taxonomy and the sharpened fourth form (a directive naming the block *and* the substitute, not a passive note). New `skills/web-search-modules/ACCESS.md` holds the venue-reachability findings. `PLAN.md` **D1/D8**.

Verified in the planning thread: validator compiles, all modules under the 40-line cap, every Reddit mention carries a substitute. Three things the review surfaced:

- **The `reddit` grep in the task's own Tests was case-sensitive** and silently skipped `competitor-content.md`, whose bullet says "Reddit" and never "reddit". A test that passes by not looking. The module was correct.
- **Two URLs went in without content verification** — `cloud.google.com/vertex-ai/pricing` (too large for the fetch summarizer) and `ycombinator.com/companies` (client-rendered SPA). Both are the right page on the right domain; neither is a guess. Recorded rather than silently accepted.
- **The Azure pricing bullet named a block with no substitute** — exactly the passive form the task had just replaced. Fixed to point at the calculator or the Bedrock/Vertex listing.

### `[runtime-portability]` Claude/Copilot portability retrofit — 2026-08-25

All 5 pieces landed, none blocked. Added the proven `Web Research Writer` Copilot wrapper while preserving the canonical `web-search-agent`; orchestration now selects each by exact registered name and host, payload lookups prefer `.agents` with `.claude` fallbacks, and install/positioning docs cover explicit single-host targets and mixed-install recovery. Validator compilation, exact frontmatter allowlists, paired fallback search, host-rule search, and `git diff --check` all passed. `PLAN.md` **D6**.

### `[results-root]` Research results live under one root, with `INDEX.md` as the branch record — 2026-08-22

All 6 pieces landed, none blocked. New `skills/research/LAYOUT.md` (60 lines) is the single source of truth for layout, discovery, `output_dir`'s base, the `INDEX.md` format, and the migration procedure; all five locate steps defer to it. `PLAN.md` **D3/D4/D5**.

Reviewed and amended in the planning thread — three gaps the implementer left:

- **Status ladder was lossy.** `/research-deep` flipping to `researching` *on queue completion* meant a fully-researched, unreported run read as in-progress. Split into `outline` → `researching` (before the first batch) → `researched` (queue done) → `complete` (report written).
- **Legacy runs have no index.** A run folder at the cwd has no root, so `{root}/INDEX.md` does not exist — every index-writing step now says to skip silently rather than create one beside the run folder.
- **cwd-relative paths survived the nesting change.** `/research-report` still said `python {topic}/generate_report.py`, which resolves one level too shallow once runs live under a root. Replaced with `{run_dir}` throughout, defined at each skill's locate step; `{project_dir}` — used in `/research-deep`'s prompt template but never defined anywhere — is now defined as the run folder's absolute path.
