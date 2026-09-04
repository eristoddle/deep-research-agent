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

# ⏭ NEXT ACTIVE TASK — D15/D16: Approved helper and Firecrawl integration

**Goal:** Make the existing Reddit Atom-feed reader and optional Firecrawl fallback available to item agents without weakening the bounded-research contract.

**Why:** D15 approves reusable, reviewed helpers as a token-efficient part of research and requires their network activity to remain budgeted. D16 makes Firecrawl a ready, optional paid fallback so an opted-in consumer does not have to modify the package mid-project. The current prompts still prohibit every script, describe only two fetch rungs, and tell agents that Reddit is unreachable even though `reddit_feed.py` works.

**Reversible if:** A live opted-in Firecrawl check shows the documented CLI behavior or cost model is materially different; keep the Reddit helper integration and revise only the Firecrawl piece.

**Design:**

1. [ ] Update `skills/research/reddit_feed.py`, `agents/web-search-agent.md`, and the hard-constrained template plus one-shot example in `skills/research-deep/SKILL.md` to allow only the approved package helper. Add a positive `--max-attempts` CLI option to `reddit_feed.py`, defaulting to its existing five attempts. The agent command must use `--json --limit 25 --max-attempts <remaining-fetch-budget>` and bounded stdout (`head -c 40000`). A `429` retry is a separate network request and consumes a fetch slot; do not begin another attempt when no slots remain. Redefine prompt wording consistently so the fetch budget covers every network retrieval attempt, not just native `WebFetch` calls, while retaining one logical fetch sequence per URL. Agents may not author arbitrary scripts, invoke an unlisted helper, download artifacts, or use browser automation.

2. [ ] Extend the same canonical agent prompt and `research-deep` template/example with the optional Firecrawl third rung. After `WebFetch` and the existing one `crwl` retry fail on the same URL, run Firecrawl only when both `command -v firecrawl` succeeds and `FIRECRAWL_API_KEY` is configured; otherwise record the URL as unreachable and continue. The configured key is the consumer's opt-in; no install, interactive prompt, or extra per-run confirmation. Treat the paid scrape as one bounded retrieval attempt, state in the item output that the paid rung ran, and never crawl multiple URLs. Firecrawl must write only to an item-specific temporary Markdown path beside that item's JSON output, read no more than 40,000 bytes, then delete that temporary file. A dedicated project fetch-escalation skill remains preferred when available. Update README setup/behavior so it accurately says Firecrawl is an optional configured fallback rather than "never automatic"; retain the paid disclosure and affiliate disclosure.

3. [ ] Update `skills/web-search-modules/sites/reddit.md`, `general-web.md`, `competitor-content.md`, and `vendor-landscape.md` to replace their stale Reddit-unreachable directive with the approved listing-reader method. Each module bullet remains self-sufficient and cites `sites/reddit.md`; it must say that the Atom reader yields listings, not full post bodies, and name its own non-Reddit companion sources so the breadth rule remains intact. The site file becomes the detailed source of the reader's limits: only public Atom feeds, no `old.reddit.com`, and title/permalink/date/subreddit listing results. Do not create a Reddit modifier or the `demand-signals` module in this task.

**Files:**
- `skills/research/reddit_feed.py`
- `agents/web-search-agent.md`
- `skills/research-deep/SKILL.md`
- `README.md`
- `skills/web-search-modules/sites/reddit.md`
- `skills/web-search-modules/general-web.md`
- `skills/web-search-modules/competitor-content.md`
- `skills/web-search-modules/vendor-landscape.md`
- `TASKS.md` (piece status and run state only)

**Tests:**
1. Run `python3 -m py_compile skills/research/reddit_feed.py skills/research/validate_json.py` and `python3 skills/research/reddit_feed.py --help`; confirm `--max-attempts` is documented.
2. Compare `skills/research-deep/SKILL.md`'s prompt template and one-shot example after variable substitution. Their Search Budget and helper/escalation instructions must match exactly.
3. Run a normal public-listing command with `--json --limit 25 --max-attempts 1`; verify it emits only post entries and no more than 25. Run it again with an intentionally nonpositive `--max-attempts` and verify it exits as bad arguments without a network request.
4. On an opted-in machine only, run Firecrawl against a known reachable control page and verify its temporary item-specific file is bounded-read then removed. Confirm the agent's missing-key path skips Firecrawl and records the URL unreachable; never supply a key through chat or commit one.
5. Run `rg -n 'reddit_feed|max-attempts|Firecrawl|FIRECRAWL_API_KEY|unreachable from this toolchain' agents/web-search-agent.md skills/research-deep/SKILL.md README.md skills/web-search-modules/{general-web,competitor-content,vendor-landscape}.md skills/web-search-modules/sites/reddit.md` and confirm no stale Reddit-unreachable directive remains.
6. Run `git diff --check`.

**Out of scope:**
- Building or routing the `demand-signals` module, a Reddit modifier, a fetch-outcome ledger, or project-local reusable helpers.
- Changing agent tool allowlists, Firecrawl's package/CLI dependency, package installation behavior, `fetch-anything`, or any source unrelated to Reddit.
- Any live research run beyond the focused helper and Firecrawl checks listed above.

**Report back:** List each completed or blocked piece, all files changed, every test result, the actual Firecrawl CLI behavior observed in the opted-in environment, and whether any instruction had to differ between Claude and Copilot. Update every piece status and the run-state note before stopping.

> ▶ Run state: queued 2026-09-04. Planned only; do not launch in this session. Resume from piece 1 in the later implementation/testing session.

---

## ✅ Done (collapsed — full detail in the planning doc's session log)

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
