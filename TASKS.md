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

# ⏭ NEXT ACTIVE TASK — none queued

Nothing is ready to hand off. The next work is the remaining nine BMAD deep-recon items (`docs/parking-lot/bmad-deep-recon-lessons.md`), and every one needs a grill first — start with **#8** (one agent per question across all subjects). See `PLAN.md` Session 8.

---

## ✅ Done (collapsed — full detail in the planning doc's session log)

### `[bmad-trust-1-5]` BMAD lessons #1 and #5: source-trace warning and source-quality card — 2026-09-26

All 3 pieces landed, none blocked, all 8 Tests passed. `validate_json.py` warns `[WARN] Answered fields with no source (N): …` when an answered field is missing from every `sources[].fields` — **advisory only**, `valid` and the exit code untouched, and a file with no `sources` key prints one skip line instead. `agents/web-search-agent.md` step 3 gained a 5-line **Source Quality** block. README: BMAD credit line and Additions 24. Review fix: a field counts as uncertain whether marked inline (`[uncertain]` in the value) or in `uncertain[]`, since the template asks for both and an agent missing one would otherwise draw a false warning. `PLAN.md` Session 8.

### `[enumerate]` D19: `/research-enumerate`, the breadth-first catalog sweep — 2026-09-12

All 6 pieces landed, none blocked, all 10 Tests passed. New `skills/research-enumerate/SKILL.md` sweeps aggregators then one-offs against a per-phase 20-search/20-fetch ceiling (not the per-item depth table), writes `catalog.md` plus a standard `outline.yaml` so `/research-deep` can descend with no new wiring, and declares unreached categories as `Not checked — budget exhausted` rather than omitting them. No new agent. Review in the planning thread fixed three things: the task's `allowed-tools` was copied from the wrong skill (`research-harvest` launches nothing), so Test 2 pinned a defect; the one-shot example was changed to a filled rendering of the prompt, per house convention; and the negative-state label was normalized to the em dash. Final 124 lines, over the 80-110 target by two required examples. README Additions 23. `PLAN.md` **D19**.

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
