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

# ⏭ NEXT ACTIVE TASK — `demand-signals`: build the module through discovery

**Goal:** A shipped `demand-signals` module in `skills/web-search-modules/`, built by actually running `/research-add-module`'s discovery procedure rather than by writing a plausible source list, registered in `ROUTING.md` as its own family, and verified against `general-web`.

**Why:** `PLAN.md` **D9**. D2's trigger is met and the module is approved in shape and family; what has never been done is the discovery pass that turns an approved shape into a tested source list. AGENTS.md is explicit that a hand-written source list is a guess and guessed sources route the agent to plausible sites that turn out to be empty — so the deliverable here is the *discovery*, and the module file is its output.

**Reversible if:** Step 7's comparison fails. If the module does not beat `general-web` on its own probe questions, say so and discard it rather than shipping it — a module that loses is negative value, since it consumes a routing slot and costs context on every task it matches. That outcome is a legitimate result of this task, not a failure of it.

**Read first:** `skills/research-add-module/SKILL.md` (you are executing its Steps 3-7 by hand — you have no `Skill` tool and no `AskUserQuestion`, so its two ask-the-user points are pre-answered below), `skills/web-search-modules/SKILL.md` (module shape, the three-kind access-method taxonomy, the fourth directive form), `PLAN.md` **D9** and **D1**, and `skills/web-search-modules/ACCESS.md`.

**Pre-answered (do not re-decide these):**
- **Step 2 destination — the package**, `skills/web-search-modules/demand-signals.md`. D9 approves it as general enough to ship. Not a local module.
- **Step 3.1 probe questions** — pinned below; do not redraft them.
- **Step 1** is already satisfied by D9; do not re-litigate whether the module is warranted.
- **Family** — its own row, question resolved by D9: *Is the question which problems, desires, or frustrations recur in people's own words across independent venues?*
- **Discovery budget — 12 searches, 14 fetches**, deliberately wider than the skill's stated 6/8. Every other module built this way covered one domain; this one spans five venue *classes* (niche forums, People-Also-Ask, search suggestions, review sites, Amazon Q&A), and 6 searches cannot probe five classes. Report usage as you go and stop at the ceiling.

**Design:**

## 1. Discovery pass — Steps 3 and 4 of `/research-add-module`

[x] **The trap to avoid, stated first: the module is domain-general, not about any of the probe topics.** The seven questions below are *probes* — instruments for watching which kinds of venue surface people describing problems in their own words. A module full of espresso forums and 3D-printing subreddits would be a failed run even if every link works. What you are cataloguing is **venue classes and how to query them**, transferable to a topic none of the probes mention.

Run these seven as ordinary `WebSearch` queries, the way `general-web` would, and watch what surfaces:

1. What do people repeatedly complain about when using note-taking apps for long-form writing?
2. What recurring problems do freelance writers describe about getting paid on time?
3. What do buyers keep complaining about in reviews of standing desks?
4. What questions do beginners keep asking when they start 3D printing?
5. What do people say is missing from personal budgeting apps?
6. What frustrations do small landlords repeatedly describe about managing rental properties?
7. What do home espresso owners keep saying goes wrong in their first year?

Then, per Step 3: tally the venue classes that keep producing *useful* results rather than merely frequent ones, and drop aggregators and SEO farms that repackage a source you already have — keep the source they repackage. **Target 4-8 sources.**

[x] Per Step 4, work out and **actually test** the access method for each surviving source, recording it in the form its kind calls for (D1's taxonomy: fixed-site → a literal `site:` query; parameterized → a URL pattern plus a verified seed list; open-query → an explicit "none by design" note; unreachable → a directive naming the block **and** the substitute, never a passive note that it blocks). Two things already in the record, so do not spend budget rediscovering them:
  - **Discourse forums expose JSON** — `search.json?q=` was confirmed on the Obsidian forum (`PLAN.md` D9, ROADMAP's fetch-fallback section). Confirm the pattern generalizes to at least one *other* Discourse forum and record a seed list; XenForo is untested and worth one probe.
  - **`skills/web-search-modules/sites/` already holds eight site files.** Read the relevant ones instead of rediscovering their methods, and cite them from your bullets — while keeping each bullet self-sufficient, because the agent may never open the citation.
  - **Reddit** is available through `skills/research/reddit_feed.py` and gets **at most one bullet**. D9 is explicit: it may contribute one listing-level signal alongside unrelated venues, and must never define the module or be its only evidence. `sites/reddit.md` has the method.

[x] Write your discovery notes — probe-by-probe, which venues surfaced, what each access-method test returned — to a scratchpad file, and give its path in the report. This is the evidence that discovery actually ran; the module file is too short to carry it.

## 2. Write the module

[x] `skills/web-search-modules/demand-signals.md`, **under 40 lines**, in **English** (the Chinese section headers are an upstream-module legacy, not the house style). Shape per `skills/web-search-modules/SKILL.md`:
  - Routing header — `**Family:**`, `**Use when:**`, `**Do not use for:**`, `**Siblings:**`. Write the anti-trigger honestly. The nearest neighbour is `competitor-content`, which is this module's mirror image — what has already been *published* about a topic versus what is being *asked* about it — so `Do not use for` must draw that line sharply enough that a mis-route corrects itself at read time.
  - Sources in priority order, each with what it is good for **and** its tested access method.
  - Query tactics specific to this domain. **One of them is load-bearing and comes from D9: full threads are the wrong unit.** Recurrence across venues is a listing- and title-level signal — many titles, cheaply. Full bodies matter only for verbatim vocabulary, as a narrower second pass. At `standard`'s 12 fetches, spending them on whole threads buys depth where this module needs breadth. Say that in the module, in the agent's own operational terms.

[x] Only write a `sites/<slug>.md` if one is genuinely earned — a second module now names the site, **or** what you learned overflows the bullet — and only once that content exists. A site file restating its bullet is an empty container; two were built and deleted the same day for exactly that. If nothing earns one, write none and say so.

## 3. Register it

[x] Add one family row to `skills/web-search-modules/ROUTING.md`'s step-2 table, using D9's question verbatim. Place it **after** Published-content landscape and **before** General — General is the default and must stay last. Change nothing else in the table: no existing family's question, no existing module's row.

[x] If the new family's boundary against `competitor-content` needs a sentence of disambiguation, add it in the same prose style as the existing "Between tooling & platform and AI ecosystem & market" and "Within software & debugging" notes below the table. One sentence, only if the routing genuinely needs it.

## 4. Verify it beats `general-web` — Step 7

[x] Re-run **two** of the seven probe questions, this time following the new module. Compare honestly against what plain search returned for those same questions in piece 1, and report the comparison with specifics — which venues the module reached that plain search did not, and whether the answers were actually better rather than merely different. Budget: 4 searches, 4 fetches, on top of piece 1's.

[x] **If it does not beat `general-web`, do not ship it.** It does beat it (see report) — module kept. Leave the module file and the ROUTING.md row out (or revert them), report the comparison, and say plainly that the module lost. Do not soften a losing result into a marginal win.

## 5. Documentation — only if piece 4 passes

[x] `ROADMAP.md`: one row in the "Modules added since the fork" table (`demand-signals` | its family | what it is), in the register of the existing rows. If the module opened a family by a route worth recording — the way `agent-tooling` is noted as the first to carve a family out of an existing one — add it to the prose below the table rather than the row.

[x] `README.md`: Additions entry **22**, continuing the numbering, one paragraph, in the register of 12 and 16 (which are the other module-family entries). It should say what question the module answers, why upstream's five modules could not, and name the breadth-over-depth constraint as the module's actual rule rather than a nicety.

**Files:**
- `skills/web-search-modules/demand-signals.md` (new)
- `skills/web-search-modules/ROUTING.md`
- `skills/web-search-modules/sites/<slug>.md` (new, only if genuinely earned)
- `ROADMAP.md`, `README.md`
- `TASKS.md` (piece status and run state only)

**Tests:**
1. `wc -l skills/web-search-modules/demand-signals.md` — under 40.
2. The module carries all four routing-header fields, and `Do not use for` explicitly distinguishes it from `competitor-content`.
3. Every source bullet carries an access method. `rg -n 'site:|https?://|search\.json|reddit_feed' skills/web-search-modules/demand-signals.md` — no bullet is a bare site name. Read the output rather than trusting the exit code: a grep can pass by not looking, which has now happened twice in this repo (`[access-methods]`, `[helper-firecrawl]`).
4. Every URL pattern in the module was actually fetched during piece 1. List them in the report with what each returned. An untested pattern in a module is worse than no pattern, because it will be trusted.
5. `ROUTING.md` — the new family row sits before General, the table is otherwise byte-identical to its previous state, and `general-web` is still described as the default. Confirm with `git diff skills/web-search-modules/ROUTING.md` and read it.
6. Reddit appears in at most one bullet, and the module does not depend on it.
7. The breadth-over-depth rule (listings and titles, not full threads) appears in the module's query tactics.
8. Piece 4's comparison is reported with specifics, not asserted.
9. README Additions numbering runs 1-22 with no gaps or repeats; ROADMAP's module table gained exactly one row.
10. `git diff --check`.

**Out of scope:**
- Any other module, the existing family questions, `chinese-tech`'s modifier status, or the depth/budget table.
- The two Wanted modules in ROADMAP (AI writing communities, docs-and-API-reference) — different domains, parked under D2.
- `PLAN.md` (the planning thread owns it), `AGENTS.md`, and any consumer-project pin bump.
- Building a local module, or writing anything into an installed `.agents/skills/` or `.claude/skills/` directory.
- Rewriting `competitor-content` to make room. D9 settled that the two are distinct families; nothing existing changes to admit this one.

**Report back:** Each piece completed or blocked; the scratchpad path for the discovery notes; the venue classes that survived the tally and the ones you dropped, with why; every access-method test and what it returned, including the failures; piece 4's honest comparison; whether anything earned a `sites/` file; and anything in D9 that turned out underspecified when you tried to build against it. If the module lost to `general-web`, that is the report — say so plainly.

> ▶ Run state: done 2026-09-05. All 5 pieces landed, none blocked; all 10 Tests passed. The module beat `general-web` in piece 4 and shipped. Reviewed in the planning thread — both live endpoints re-verified independently (autocomplete returns frustration-shaped completions as claimed; Trustpilot fetches on a second unrelated brand, so the pattern generalizes). One clause added there: **Trustpilot's low-star reviews skew hard toward billing, refunds, and support**, not product gaps, and the bullet now says so and points at the forum bullet for "what the product cannot do." Without it the module answers "what's missing from budgeting apps" with a page of refund complaints. Discovery notes at `<scratchpad>/demand-signals-discovery-notes.md`.

---

## ✅ Done (collapsed — full detail in the planning doc's session log)

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
