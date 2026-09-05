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

# ⏭ NEXT ACTIVE TASK — D17 harvest half: `/research-harvest`

**Goal:** A hand-invoked `/research-harvest` skill that scans every run under the research root, tallies which sources supported fields across runs, and writes a reviewable candidate list — plus the shipped script that does the counting.

**Why:** `PLAN.md` **D17** (harvest half) and **D18** (its implementation shape). Capture shipped 2026-09-04, so results files can now carry `sources[]`; nothing reads them yet. D17's amendment settles that this ships now rather than waiting for data to accumulate — "wait for several runs" described one consumer's situation and is not a condition this repo can observe.

**Reversible if:** Nothing open. The promotion threshold (3 runs / field-support in 2) is D17-settled; if it later proves wrong only the two constants in the script change.

**Design:**

## 1. `skills/research/harvest_sources.py` — the read-only tally helper

[x] New file, beside `validate_json.py` and `reddit_feed.py` in `skills/research/`. Match `validate_json.py`'s house style: stdlib only (no PyYAML — see below), `argparse`, exit `2` on usage/input error, bounded output.

- **Arguments:** `--root <path>` (the research root; scan every run beneath it) and `--run <path>` (one run folder), mutually exclusive, at least one required. Optional `--min-runs` (default `3`) and `--min-field-runs` (default `2`) so the D17 threshold is visible and adjustable, not buried in a literal.
- **Discovery:** a run folder is any directory containing `outline.yaml`. Under `--root`, glob one and two levels deep, matching `skills/research/LAYOUT.md`'s rule — do not invent a third depth or a recursive walk.
- **Results location:** read `execution.output_dir` from `outline.yaml`, **resolved relative to the run folder, never the cwd** (LAYOUT.md); default `results` when absent or unparseable. `outline.yaml` is YAML but PyYAML is not a dependency anywhere in this package — do not add one. A line-oriented read for the single `output_dir:` key under `execution:` is sufficient and must fail soft to `results`.
- **Scan:** every `*.json` directly in that directory. A file that is not valid JSON, or not a JSON object, is counted as skipped and named in the summary — never a traceback, never a silent drop.
- **Per-run classification, which is the point of the whole script (D17 amendment):** a run is `no-capture` when **no** result file in it has a `sources` key, and `captured` when at least one does. Report the two counts separately.
- **Tally key is the URL**, normalized only by stripping a trailing `/` and lowercasing the scheme+host (leave the path case alone). Carry the `source` name(s) seen for that URL for display. Per URL, count: number of distinct runs it appears in, and number of distinct runs where its `fields` array was non-empty. An entry missing `fields`, or with an empty one, still counts toward run appearances but never toward field-support.
- **Malformed `sources` entries** (not an object, missing `url`, `fields` not a list) are counted and reported as a single "N malformed source entries skipped" line, not enumerated.
- **Output is bounded — this is load-bearing, the script's stdout enters an agent's context.** Print, in order: a one-line scan summary (runs scanned, of which captured / no-capture / skipped files); the qualifying candidates in full, one block each with url, source name(s), run count, field-support run count, the run names, and the distinct field names; then near-misses (appeared in >1 run but below threshold) capped at **20** with a `… and N more` line; then nothing else. Cap the field-name list per entry at 12 names plus a count. No raw JSON dumps, no per-file logging.
- **When there are no candidates**, print which case it is, explicitly, in the words D17 asks for: all runs `no-capture` → these runs predate source capture; otherwise → sources were captured and none reached the threshold. A mixed scan says both, with counts.
- Add `--json` **only if** it falls out for free; if it complicates the output-bounding, skip it. The skill consumes the text.

## 2. `skills/research-harvest/SKILL.md` — the skill

[x] New directory + `SKILL.md`, frontmatter in the same shape as the other skills (`name`, `user-invocable: true`, `description`, `allowed-tools`). Allowed tools: `Bash, Read, Write, Glob, AskUserQuestion` — no `WebSearch`, no `WebFetch`, no `Task`. Harvest reads what runs already recorded; it does no research and launches no agent. Keep it under ~70 lines.

- **Trigger** `/research-harvest`, optionally naming one run. **Never invoked automatically** by `/research-deep` or `/research-report` — state this (D17's reasoning: runs routinely stop before the report step, and a prompt after every run gets trained away).
- **Locate step defers to `skills/research/LAYOUT.md`**, like every other skill — do not restate the discovery rule. Default scope is the whole root; a named run narrows it.
- **Resolve the script** with the same four-path lookup and same ordering `skills/research-deep/SKILL.md` uses for `{validator_path}` (`.agents` project, `.claude` project, `~/.agents`, `~/.claude`). When none exists, **stop and say so** — do not hand-write a substitute tally.
- **Report the empty cases in plain words**, carrying the script's distinction through to the user rather than printing "no candidates found."
- **Write `.agents/web-search-modules-local/CANDIDATES.md`.** Prefer that path; write to `.claude/web-search-modules-local/CANDIDATES.md` instead only when that legacy directory already exists and the `.agents` one does not — the same preference order `ROUTING.md` step 0 uses for local modules. Create the directory when neither exists.
- **File shape:** a header naming the date, the scope scanned, the threshold used, and one line noting that only **parameterized** modules (D1) can absorb a source; then `## Candidates`, one unticked `- [ ]` per source with its URL, run count, field-support count, and the fields it supported; then `## Dispositioned`.
- **Regeneration rule (D18):** the file is rewritten whole on every harvest, but read it first — any entry the human has **ticked (`- [x]`) or struck (`~~…~~`)** moves to (or stays in) `## Dispositioned` and is **excluded from `## Candidates`** even if it still qualifies. State plainly that this is what stops a rejected source returning as new every harvest. Never delete a dispositioned line.
- **No module attribution and no module edits.** The skill never writes into a module file — D17: discovery stays automatic, judgment stays manual.

## 3. Documentation — README and ROADMAP

[x] `README.md`: add `/research-harvest` to the **Usage** block (one line, matching the existing comment style). Then backfill the **Additions** list, which stops at 18 and is missing three shipped capabilities — continue the numbering, match the existing entries' register (what it is, why upstream's absence was a problem, what the rule actually is), and keep them to one paragraph each:
  - **19** — `unreachable[]` as an output channel separate from unanswered `uncertain[]`, and the deduplicated `## Unreachable sources` report section (`PLAN.md` D11, `TASKS.md` `[unreachable-output]`).
  - **20** — the one approved package helper (`reddit_feed.py`, its `--max-attempts` cap) and the fetch budget's redefinition to count *every* network retrieval attempt rather than only native `WebFetch` calls (D15, `[helper-firecrawl]`). Note that entry 15 already covers the Firecrawl rung — do not duplicate it, reference it.
  - **21** — source capture and harvest together: `sources[]` on every result file, and `/research-harvest`'s candidate list with its 3-runs/2-field-support threshold (D17, D18).

[x] `ROADMAP.md`: two sections are stale and read as open work.
  - **"Fill in `stackoverflow.md`"** — landed 2026-09-04, and the finding is worth keeping rather than deleting: `site:stackoverflow.com` returns **zero** SO URLs and fills with answer-scraping farms, `WebFetch` is refused at both the site and its API, and the working route is the Stack Exchange API through the existing `crwl` escalation (keyless, 300/day, `filter=withbody` returns the accepted answer's text with no page fetch). Rewrite it as a landed section in the register of "Retrofit: access methods — landed".
  - **"Verify the fetch fallback"** — the parking lot records this as tested 2026-08-29: the escalation runs clean and the `head -c` bound holds, but it does **not** recover a JS-shell page; prefer a JSON endpoint beside the HTML page. The section still says "has never fired in a real run." Reconcile it to what was actually found; keep the Obsidian forum observation, which is the worked example.
  - Do **not** touch the module table, the `chinese-tech` section, or the Wanted modules list.

**Files:**
- `skills/research/harvest_sources.py` (new)
- `skills/research-harvest/SKILL.md` (new)
- `README.md`
- `ROADMAP.md`
- `TASKS.md` (piece status and run state only)

**Tests:**
1. `python3 -m py_compile skills/research/harvest_sources.py` and `python3 -m py_compile skills/research/validate_json.py` (the latter must still compile; you are not editing it).
2. **Build a synthetic fixture in the scratchpad** — D17's amendment says live verification is impossible here, so the fixture *is* the test. A root with four run folders: one whose results have no `sources` key at all (predates capture); three that carry `sources`, arranged so that exactly one URL appears in 3 runs with a non-empty `fields` in 2 of them (a candidate), one appears in 3 runs but has field support in only 1 (a near-miss), and one appears in a single run. Include one result file with `output_dir` set to something other than `results`, one unparseable `.json`, and one malformed `sources` entry.
3. Run `--root` against that fixture. Confirm: exactly one candidate is reported; the near-miss appears under near-misses, not candidates; the unparseable file is named as skipped and does not crash the run; the non-default `output_dir` run was scanned; the scan summary counts 1 no-capture and 3 captured.
4. Run `--run` against the single no-capture run alone. Confirm the output says these runs predate source capture, in those terms, and does **not** say sources were captured but nothing met the threshold.
5. Delete the `sources` arrays from the fixture's captured runs and re-run `--root`; confirm the message flips to the predates-capture case. Then restore them, lower `--min-runs 2`, and confirm the near-miss is still excluded (it fails the *field-support* clause, not the run-count one) — this is the check that proves the two-clause threshold is really two clauses.
6. Pipe the fixture's `--root` output through `wc -l` and confirm it is bounded; then synthesize 60 qualifying-ish URLs and confirm near-misses cap at 20 with the `… and N more` line.
7. Exercise the `CANDIDATES.md` regeneration rule by hand: write a `CANDIDATES.md` containing one ticked and one struck entry, then follow the skill's own written steps against the fixture and confirm those two land under `## Dispositioned` and appear nowhere under `## Candidates`. If the skill's wording does not make that mechanically followable, the wording is the bug — fix it.
8. `rg -n 'research-harvest' README.md skills/research-harvest/SKILL.md` and confirm the skill is in the Usage block; confirm the Additions numbering runs 1–21 with no gaps or repeats.
9. `git diff --check`.

**Out of scope:**
- Writing into any module file, or attributing a candidate to a module. D17 keeps promotion manual.
- Backfilling existing runs with sources, or any migration.
- Changing either agent's `tools:` allowlist, the depth/budget table, the fetch ladder, `validate_json.py`, or `unreachable[]`'s render-by-default behavior.
- Live verification against a consumer project — D17 names that a separate later check, and it cannot be done from this checkout.
- `PLAN.md` (the planning thread owns it) and any consumer-project pin bump.

**Report back:** Each piece completed or blocked, files changed, every test result with the actual output line that proves it (especially Tests 4, 5, and 7), the fixture's scratchpad path so the planning thread can re-run it, and anything in the D17/D18 spec that turned out underspecified when you tried to build against it.

> ▶ Run state: **done**, all 3 pieces landed, none blocked. All 9 Tests passed, including Tests 4/5/7 (the ones the report-back calls out specifically). Fixture built at `/private/tmp/claude-501/-Users-eristoddle-Dropbox-Writing-deep-research-agent/c5cbdd7b-99b6-40ad-8bea-dbbf17214da5/scratchpad/harvest-fixture` (a backup pre-edit copy sits alongside it at `harvest-fixture-backup`, and a second disposable fixture for the 60-URL near-miss cap check at `harvest-fixture-nearmiss-cap`) — re-runnable, see the implementer's report for the exact commands. Nothing left in the queue; see the full report in the session transcript for underspecified points raised (PyYAML's parenthetical justification, and the "named in the summary" vs "one-line summary" wording tension, both resolved by implementation choice rather than blocking).

---

## ✅ Done (collapsed — full detail in the planning doc's session log)

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
