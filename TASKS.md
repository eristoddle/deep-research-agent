# TASKS — deep-research-agent

> The unit of implementation work. Written by the planning thread once a decision in `PLAN.md` is concrete enough to build, executed by the `implementer` agent in its own context window.
>
> **The active task is a serial QUEUE of numbered pieces** (1, 2, 3…) — tightly-related steps of one job, or a stack of independent jobs; doesn't matter, stack as many as you want. Two rhythms this serves:
> - **Pacing** — queue a little, plan the next batch while the agent grinds.
> - **Unattended** — queue a lot and walk away; the agent chews the whole queue.
>
> **Execution (default = synchronous, one agent):** work the queue top-to-bottom. A blocked piece does **not** halt the queue — skip it and continue with any piece that doesn't depend on it (mark deps inline: `depends on #2`); halt only when nothing remaining can proceed. **Always log run-state on stop** (done or blocked): flip each piece's status box as you go and update the ▶ Run state note, so a killed/forgotten session is recoverable from this file on disk.
>
> **Contract:** fill every section before launching. Mark a section `—` only if it genuinely doesn't apply. The agent is *cold on the planning conversation* but *warm on the project* (it has `CLAUDE.md` + the codebase) — reference decisions and files by pointer; don't re-explain the repo.
>
> Completed work collapses to a one-block summary with a stable `[tag]` under **✅ Done**; the full detail lives in `PLAN.md`'s session log.

---

# ⏭ NEXT ACTIVE TASK — Access-method retrofit across all ten search modules

## Goal

Every source bullet in every module says **how to reach that source**, in the form appropriate to its module's kind (PLAN.md D1). Done means: a reader of any module can query its sources without first searching to find out where they live, and no bullet names a URL that has not been confirmed to resolve.

## Why (pointer)

`PLAN.md` **D1 🔒** — the spec at `skills/web-search-modules/SKILL.md:36` has required an access method since before these modules were written, and `site:` currently appears **zero** times across all ten. Spec and payload disagree. The cost is concrete: a `standard` run gets 8 searches and 12 fetches total, so searches spent rediscovering *where* a named source lives are searches not spent on the question — and rediscovery is non-deterministic, which is how a price ends up quoted from a blog copy instead of the provider's page.

### ▶ Run state (the agent keeps this current on every stop)
_<not started · nothing done · nothing blocked · all 6 pieces remain · resume from #1>_

## Design — numbered pieces (status: `[ ]` not started · `[x]` done · `[!]` blocked)

- [ ] **1.** **Write the three-kind taxonomy into `skills/web-search-modules/SKILL.md`**, at/near line 36. The current sentence implies every source takes a URL. Add the distinction from D1 — fixed-site → literal `site:` query; parameterized → URL pattern + seed list; open-query → an explicit "none by design" note — and state that a **guessed URL is worse than none**, because the agent trusts it and spends a fetch on a 404 instead of falling back to search. This piece gates every other piece: it is what stops #4 from inventing sources.
- [ ] **2.** **Parameterized batch** — `pricing.md`, `benchmarks.md`, `model-releases.md`, `vendor-landscape.md`. _(depends on #1)_ Each source bullet gains a URL **pattern** plus a short seed list of the vendors/leaderboards that actually recur. Verify every seed URL resolves and contains what the bullet claims. `pricing` and `benchmarks` first — ROADMAP ranks them highest because provider pricing pages and leaderboard URLs are stable and worth naming outright.
- [ ] **3.** **Fixed-site batch** — `github-debug.md`, `academic-papers.md`, `chinese-tech.md`. _(depends on #1)_ Literal `site:` queries appended to existing bullets. `academic-papers` already carries bare domains (`arxiv.org`, `scholar.google.com`) but no query method — it is partially compliant, so add the method to the domains already there rather than restating them. It has 31 of 40 lines used: append inline, add no new lines.
- [ ] **4.** **Open-query batch** — `general-web.md`, `competitor-content.md`. _(depends on #1)_ Write the explicit **"none by design"** note and one line on why. Do **not** invent a source list for either. `competitor-content` samples an unrefined reader-query search deliberately; a pinned source list would defeat the module.
- [ ] **5.** **`stackoverflow.md` access methods only.** _(depends on #1)_ Add `site:stackoverflow.com` / Stack Exchange query methods to its two source bullets. **The rewrite is parked** — do not add query tactics, do not restructure it, do not lengthen it beyond the access methods. That work is a separate parking-lot item.
- [ ] **6.** **Update `ROADMAP.md`.** _(depends on #2, #3, #4, #5)_ Retire the "Retrofit: access methods" section — replace it with a one-line record that it landed and what the three-kind rule is, pointing at `PLAN.md` D1. Leave every other roadmap section alone.

## Files

- `skills/web-search-modules/SKILL.md` — piece 1
- `skills/web-search-modules/{pricing,benchmarks,model-releases,vendor-landscape}.md` — piece 2
- `skills/web-search-modules/{github-debug,academic-papers,chinese-tech}.md` — piece 3
- `skills/web-search-modules/{general-web,competitor-content}.md` — piece 4
- `skills/web-search-modules/stackoverflow.md` — piece 5
- `ROADMAP.md` — piece 6

## Tests (add; keep the suite green)

There is no test suite — correctness here is judged by three checks, all of which must hold when the queue finishes:

1. `python3 -m py_compile skills/research/validate_json.py` still passes (it should be untouched; this catches an accidental edit).
2. **Every URL you write resolves and contains what the bullet claims.** Fetch it. A URL you could not verify does not go in the file — say so in the report instead. This is the whole point of the task.
3. **`wc -l` on every module stays under 40.** Append access methods to existing bullets; do not add new lines. Report the before/after line count for each file you touch.

## Out of scope (do NOT do)

- **Do not add a new module.** PLAN.md D2 — no new modules until a real project needs one.
- **Do not touch `ROUTING.md`**, its families, or any routing header. No module changes family here.
- **Do not rewrite `stackoverflow.md`'s tactics** — access methods only (piece 5).
- **Do not create any file under `agents/` or `skills/`.** `agents/` is shipped APM payload; a stray `.md` there is flattened into a top-level agent in every consumer install.
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
