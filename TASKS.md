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

# ⏭ NEXT ACTIVE TASK — D17 capture half: record which sources answered

**Goal:** Every `results/*.json` records the sources that actually answered its fields, so that recurrence across runs becomes measurable later.

**Why:** `PLAN.md` **D17**. Verified 2026-09-04 against a live consumer run: result files record *answers*, not provenance — one URL per item, and only because that project's `fields.yaml` happened to declare a URL field. Nothing accumulates today, so the harvest skill D17 also describes would have nothing to read. Capture must ship first and can only see runs from the day it lands.

**Reversible if:** Nothing open. D17 settled every branch; the harvest half is deliberately not in this task.

**Design:**

1. [x] Add the `sources[]` contract to `agents/web-search-agent.md`, beside the existing `unreachable[]` rules. It is a top-level array, sibling to `uncertain[]` and `unreachable[]`. Each entry has exactly three keys: `source` (the site or publication name), `url`, and `fields` (an array of the field names that source supported). **Record only sources that contributed to an answer** — a page that was opened and did not inform any field is not recorded, and a page that failed is already `unreachable[]`'s job. A source that supported several fields is one entry with several names in `fields`, never repeated entries. Do not add a new tool, permission, fetch, or search to produce this: it is written from what the agent already has in hand at output time.

2. [x] Mirror the same contract into `skills/research-deep/SKILL.md` — both the hard-constrained prompt template **and** its one-shot example, in lockstep. The example must show a populated `sources` array with at least two entries, one of which supports more than one field, so the multi-field shape is demonstrated rather than described. Follow the numbered-output-rules format already used there for `unreachable`.

3. [x] `skills/research/validate_json.py:22` — `_SKIP_KEYS` is `{"_source_file", "uncertain"}`. Add both `"unreachable"` (missed when that array shipped 2026-09-04) and `"sources"`. Without this they are counted as unexpected top-level keys and printed under "Extra fields". Confirmed cosmetic, not a false pass — the walker never descends into these arrays — so do not restructure the walker; this is a one-line set addition.

4. [x] `skills/research-report/SKILL.md` — a generated report **does not render sources by default**. It renders them only when the invoking prompt asks for sources or citations, in natural language; do not add a flag, an option, or a config key. State this explicitly so the default stays quiet and the behavior stays promptable. This is deliberately unlike `unreachable[]`, which does render by default.

**Files:**
- `agents/web-search-agent.md`
- `skills/research-deep/SKILL.md`
- `skills/research/validate_json.py`
- `skills/research-report/SKILL.md`
- `TASKS.md` (piece status and run state only)

**Tests:**
1. `python3 -m py_compile skills/research/validate_json.py`.
2. Build a throwaway `fields.yaml` + item JSON in the scratchpad containing populated `uncertain`, `unreachable`, and `sources` arrays. Run the validator and confirm none of the three appears under "Extra fields", and that coverage is unchanged from the same file with those arrays removed.
3. Compare the prompt template and the one-shot example in `skills/research-deep/SKILL.md` after variable substitution. Their output-rules and `sources` instructions must match exactly. This is the regression nothing else here catches.
4. Confirm the one-shot example's `sources` array is syntactically valid JSON and contains an entry whose `fields` array has more than one name.
5. `rg -n 'sources' agents/web-search-agent.md skills/research-deep/SKILL.md skills/research-report/SKILL.md` — confirm the report file states the not-by-default rule and that no flag or option was introduced.
6. `git diff --check`.

**Out of scope:**
- The `/research-harvest` skill, `CANDIDATES.md`, the promotion threshold, and anything reading across runs. That is D17's harvest half and is deliberately later.
- Backfilling existing runs; D17 settled that they get nothing.
- Changing either agent's `tools:` allowlist, the fetch-escalation ladder, the depth/budget table, or `unreachable[]`'s existing render-by-default behavior.

**Report back:** Each piece completed or blocked, files changed, every test result, and whether the template and its one-shot example needed any wording to differ. Update every piece status and the run-state note before stopping.

> ▶ Run state: done 2026-09-04. All 4 pieces landed, none blocked. All 6 Tests passed.

---

## ✅ Done (collapsed — full detail in the planning doc's session log)

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
