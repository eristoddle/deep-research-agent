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

# ⏭ NEXT ACTIVE TASK — Access-method retrofit across all ten search modules

## Goal

Every source bullet in every module says **how to reach that source**, in the form appropriate to its module's kind (PLAN.md D1), and a source that *cannot* be reached says so and names what to use instead (PLAN.md D8). Done means: a reader of any module can query its sources without first searching to find out where they live, no bullet names a URL that has not been confirmed to resolve, and no bullet names an unreachable source without a substitute.

## Why (pointer)

`PLAN.md` **D1 🔒** — the spec at `skills/web-search-modules/SKILL.md:36` has required an access method since before these modules were written, and `site:` currently appears **zero** times across the ten in scope. Spec and payload disagree. The cost is concrete: a `standard` run gets 8 searches and 12 fetches total, so searches spent rediscovering *where* a named source lives are searches not spent on the question — and rediscovery is non-deterministic, which is how a price ends up quoted from a blog copy instead of the provider's page.

`PLAN.md` **D8** sharpens the fourth form of access method. The spec currently allows "a note that it blocks fetching," which is passive — it tells the agent to give up. Under **D7** giving up already beats the real failure mode (silently proceeding on whatever the search tool substituted), but it still ends the line of inquiry. The fourth form becomes a **directive naming the block and the substitute**, and what is known about reaching a venue lands in one shared file rather than being restated in each module that names it.

**The worked example is already in the repo.** `skills/web-search-modules/agent-tooling.md` was built access-method-first through `/research-add-module` and is excluded from this retrofit (`ROADMAP.md:24`) precisely because it is the reference shape. Read it before touching anything else. It demonstrates all three kinds in one file: `Verified working: <url>, <url>` seed lists, an explicit "do not reach it via `site:` search — fetch the URL directly" instruction, and blocked/wrong sources named alongside what to use instead (the impostor-domain and SEO-skip-list tactics). Match that shape rather than inventing one.

### ▶ Run state (the agent keeps this current on every stop)
_<done · all 7 pieces landed, none blocked · four checks in Tests section all pass (py_compile, URL verification with unresolved URLs reported below, all modules + ACCESS.md under 40 lines, reddit grep clean) · nothing remains>_

## Size — where the time actually goes

**~2.5 to 3 hours total.** Counted, not guessed: the ten modules carry **52 source bullets**, and they are not equal work.

| Piece | Modules | Bullets | Size |
|---|---|---|---|
| 5 | `general-web`, `competitor-content` | 14 | `[S]` ~10 min — these get **no** URLs by design; one "none by design" note each |
| 4 + 6 | `github-debug`, `academic-papers`, `chinese-tech`, `stackoverflow` | 18 | `[M]` ~25 min — a literal `site:` query appended per bullet; a query form, so nothing to verify |
| 3 | `pricing`, `benchmarks`, `model-releases`, `vendor-landscape` | 20 | `[L]` ~90 min — **the entire cost of this task** |
| 1 + 2 + 7 | `SKILL.md`, `ACCESS.md`, `ROADMAP.md` | — | `[S]` ~45 min combined |

Piece 3 dominates because **one bullet is not one URL**. "The provider's own pricing page" is really Anthropic, OpenAI, Google, Mistral, DeepSeek, and xAI; "leaderboards" is another five or six. Twenty bullets expand into roughly **60–100 actual URLs**, and each one gets fetched to confirm it resolves *and* contains what the bullet claims. That is 30–50 minutes of pure network wait, plus reading each result, plus refitting bullets to stay under the 40-line cap rather than appending to it.

### The one real decision

**The verification is the cost, not the writing.** Drop "confirm every seed URL resolves" and the whole task is ~45 minutes instead of ~3 hours.

The rule exists because a **guessed URL is worse than none** (PLAN.md D1): the agent trusts it and spends a fetch on a 404 instead of falling back to search. Recommendation is to keep it for piece 3 specifically, since provider pricing pages are exactly where a stale URL causes a wrong number to get published. If the budget has to give, drop verification on the *leaderboard* seeds in `benchmarks` before the *pricing* seeds.

## Design — numbered pieces (status: `[ ]` not started · `[x]` done · `[!]` blocked)

- [x] **1.** `[S]` **Write the three-kind taxonomy and the fourth-form directive into `skills/web-search-modules/SKILL.md`**, at/near line 36. The current sentence implies every source takes a URL. Two changes, both to that bullet: (a) add the distinction from D1 — fixed-site → literal `site:` query; parameterized → URL pattern + seed list; open-query → an explicit "none by design" note — and state that a **guessed URL is worse than none**, because the agent trusts it and spends a fetch on a 404 instead of falling back to search. (b) Per D8, rewrite the existing fourth form: "a note that it blocks fetching" becomes a **directive that names the block *and* the substitute** — the shape is "unreachable from this toolchain — use X for the same signal," not "this site blocks fetching." A passive note ends the line of inquiry; a directive redirects it. This piece gates every other piece: it is what stops #5 from inventing sources.
- [x] **2.** `[S]` **Create `skills/web-search-modules/ACCESS.md`** — the one shared file D8(a) calls for, the same architecture as `ROUTING.md` for routing and `LAYOUT.md` for layout. _(depends on #1)_ **This is a data file, not a router entry** — do not add it to `ROUTING.md`, do not give it a family, and do not touch routing in any way; how to reach a source is not a routing question. Shape: one section per venue, each carrying **what fails**, **what was tried**, **the substitute**, and **the date + a one-line caveat naming the evidence's scope**. Seed it with exactly three entries, all already observed and recorded — do not research new ones, do not speculate:
  - **Reddit** — every route inside the agent's tool discipline failed 2026-09-03; the search layer fails *silently*, returning plausible results from other domains with no error. Substitute: niche forums, People-Also-Ask, search suggestions. Caveat: **one machine, one IP, one harness build; firecrawl untested** — cite [Q3](docs/questions/Q3-reddit-reachability.md) and do not state it as settled.
  - **JS-shell pages** — the `crwl` fallback escalates cleanly and the `head -c` bound holds, but it does *not* recover a page whose content arrives via JS. Substitute: prefer a JSON endpoint beside the HTML page. Cite `docs/parking-lot/verify-crwl-fallback.md`.
  - **"JSON endpoint beside the HTML page" is not general** — it holds for Discourse (confirmed on the Obsidian forum) and is falsified for Reddit, where the endpoint exists and is unreachable. Cite `docs/parking-lot/search-layer-refusals.md`.

  Add one line to `SKILL.md` pointing at it, next to the piece-1 edit. Keep the whole file under ~40 lines — it is read the same way a module is. **Hand-authored only:** D10's runtime-accumulated ledger is a different thing whose mechanics are still open ([Q4](docs/questions/Q4-ledger-mechanics.md)); nothing in this piece writes at runtime, and no skill or agent prompt gains a `Write` permission.
- [x] **3.** `[L]` **Parameterized batch** — `pricing.md`, `benchmarks.md`, `model-releases.md`, `vendor-landscape.md`. _(depends on #1, #2)_ Each source bullet gains a URL **pattern** plus a short seed list of the vendors/leaderboards that actually recur — the `Verified working:` shape from `agent-tooling.md`. Verify every seed URL resolves and contains what the bullet claims. `pricing` and `benchmarks` first — ROADMAP ranks them highest because provider pricing pages and leaderboard URLs are stable and worth naming outright. `vendor-landscape` names Reddit as a source: give it the D8 directive form and cite `ACCESS.md` rather than restating the finding inline.
- [x] **4.** `[M]` **Fixed-site batch** — `github-debug.md`, `academic-papers.md`, `chinese-tech.md`. _(depends on #1, #2)_ Literal `site:` queries appended to existing bullets. `academic-papers` already carries bare domains (`arxiv.org`, `scholar.google.com`) but no query method — it is partially compliant, so add the method to the domains already there rather than restating them. It has 31 of 40 lines used: append inline, add no new lines.
- [x] **5.** `[S]` **Open-query batch** — `general-web.md`, `competitor-content.md`. _(depends on #1, #2)_ Write the explicit **"none by design"** note and one line on why. Do **not** invent a source list for either. `competitor-content` samples an unrefined reader-query search deliberately; a pinned source list would defeat the module. Both name Reddit: that bullet gets the D8 directive form citing `ACCESS.md` — which is the one case where an open-query module does carry an access method, because "unreachable, use X instead" is exactly what the agent needs and is not a source list.
- [x] **6.** `[S]` **`stackoverflow.md` access methods only.** _(depends on #1, #2)_ Add `site:stackoverflow.com` / Stack Exchange query methods to its two source bullets. **The rewrite is parked** — do not add query tactics, do not restructure it, do not lengthen it beyond the access methods. That work is a separate parking-lot item.
- [x] **7.** `[S]` **Update `ROADMAP.md`.** _(depends on #3, #4, #5, #6)_ Retire the "Retrofit: access methods" section — replace it with a one-line record that it landed, what the three-kind rule is, and that the fourth form is now a directive backed by `ACCESS.md`, pointing at `PLAN.md` D1 and D8. Leave every other roadmap section alone, including the `agent-tooling` paragraph that names it the reference shape.

## Files

- `skills/web-search-modules/SKILL.md` — pieces 1, 2
- `skills/web-search-modules/ACCESS.md` — piece 2 (new file)
- `skills/web-search-modules/{pricing,benchmarks,model-releases,vendor-landscape}.md` — piece 3
- `skills/web-search-modules/{github-debug,academic-papers,chinese-tech}.md` — piece 4
- `skills/web-search-modules/{general-web,competitor-content}.md` — piece 5
- `skills/web-search-modules/stackoverflow.md` — piece 6
- `ROADMAP.md` — piece 7
- `skills/web-search-modules/agent-tooling.md` — **read-only reference shape. Do not edit it.**

## Tests (add; keep the suite green)

There is no test suite — correctness here is judged by four checks, all of which must hold when the queue finishes:

1. `python3 -m py_compile skills/research/validate_json.py` still passes (it should be untouched; this catches an accidental edit).
2. **Every URL you write resolves and contains what the bullet claims.** Fetch it. A URL you could not verify does not go in the file — say so in the report instead. This is the whole point of the task.
3. **`wc -l` on every module stays under 40**, `ACCESS.md` included. Append access methods to existing bullets; do not add new lines. Report the before/after line count for each file you touch.
4. **`grep -n "reddit" skills/web-search-modules/*.md`** — every remaining hit sits in a bullet that names a substitute and cites `ACCESS.md`. A bare mention of Reddit with no directive is the exact failure D7 and D8 exist to close.

## Out of scope (do NOT do)

- **Do not add a new module.** PLAN.md D2 — no new modules until a real project needs one. `ACCESS.md` is a shared data file, not a module: no routing header, no `ROUTING.md` row.
- **Do not touch `ROUTING.md`**, its families, or any routing header. No module changes family here.
- **Do not edit `agent-tooling.md`.** It is out of scope by ROADMAP decision and is the reference shape; changing it moves the target.
- **Do not build D10's fetch-outcome ledger.** Q4 is open — location, the `Write` carve-out, and expiry are all undecided. `ACCESS.md` is hand-authored and nothing writes to it at runtime.
- **Do not re-test Reddit reachability.** Q3 carries the re-test procedure and it is a planning-thread call on different hardware. Record what is already known, with its caveat, and move on.
- **Do not rewrite `stackoverflow.md`'s tactics** — access methods only (piece 6).
- **Do not create any file under `agents/`.** `agents/` is shipped APM payload; a stray `.md` there is flattened into a top-level agent in every consumer install.
- **Do not "improve" prose** in a module you're otherwise editing. Wording is the implementation; a nicer sentence that drops a constraint is a regression.
- Do not commit.

## Report back

Per file: before/after line count, the access method added to each source bullet, and — separately — **every URL you could not verify**, with what happened when you fetched it. List blocked pieces with reasons. Do not bury an unverified URL in a summary; it is the one result that changes what the planning thread does next.
---

## ✅ Done (collapsed — full detail in the planning doc's session log)

### `[runtime-portability]` Claude/Copilot portability retrofit — 2026-08-25

All 5 pieces landed, none blocked. Added the proven `Web Research Writer` Copilot wrapper while preserving the canonical `web-search-agent`; orchestration now selects each by exact registered name and host, payload lookups prefer `.agents` with `.claude` fallbacks, and install/positioning docs cover explicit single-host targets and mixed-install recovery. Validator compilation, exact frontmatter allowlists, paired fallback search, host-rule search, and `git diff --check` all passed. `PLAN.md` **D6**.

### `[results-root]` Research results live under one root, with `INDEX.md` as the branch record — 2026-08-22

All 6 pieces landed, none blocked. New `skills/research/LAYOUT.md` (60 lines) is the single source of truth for layout, discovery, `output_dir`'s base, the `INDEX.md` format, and the migration procedure; all five locate steps defer to it. `PLAN.md` **D3/D4/D5**.

Reviewed and amended in the planning thread — three gaps the implementer left:

- **Status ladder was lossy.** `/research-deep` flipping to `researching` *on queue completion* meant a fully-researched, unreported run read as in-progress. Split into `outline` → `researching` (before the first batch) → `researched` (queue done) → `complete` (report written).
- **Legacy runs have no index.** A run folder at the cwd has no root, so `{root}/INDEX.md` does not exist — every index-writing step now says to skip silently rather than create one beside the run folder.
- **cwd-relative paths survived the nesting change.** `/research-report` still said `python {topic}/generate_report.py`, which resolves one level too shallow once runs live under a root. Replaced with `{run_dir}` throughout, defined at each skill's locate step; `{project_dir}` — used in `/research-deep`'s prompt template but never defined anywhere — is now defined as the run folder's absolute path.
