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

# ⏭ NEXT ACTIVE TASK — Build the nine site files

## Goal

The nine sites that more than one module names each get one small file at `skills/web-search-modules/sites/<slug>.md`, holding the querying method that is currently either duplicated across modules or written well in exactly one of them and missing from the rest. Done means: a maintainer editing how we query GitHub edits one file, not six; every module bullet naming one of the nine cites its site file by path; and no module bullet has become dependent on that file to function.

## Why (pointer)

`PLAN.md` **D14**. GitHub is named by **six** modules, and the method that actually works — fetching `https://raw.githubusercontent.com/<org>/<repo>/main/CHANGELOG.md` instead of a changelog aggregator, checking the last commit date before trusting a repo — exists in `agent-tooling.md` and nowhere else. Five modules point at GitHub with no method at all. That is the shape this fixes.

**The citation is the tag** (D12(a), amended). A module referencing `sites/reddit.md` is what makes `grep -rl "sites/reddit.md"` produce the revert list when Reddit's status changes. There is no separate marker: **delete the `[ACCESS:reddit]` tags** currently in `general-web.md`, `competitor-content.md`, `vendor-landscape.md`, and `ACCESS.md` — the path citation replaces them.

**Reversible if:** [Q3](docs/questions/Q3-reddit-reachability.md) flips Reddit to reachable — that changes one line in `sites/reddit.md` and nothing else, which is the point. [Q5](docs/questions/Q5-site-references.md) and [Q6](docs/questions/Q6-firecrawl-rung.md) are open but do not reverse this work.

### ▶ Run state (the agent keeps this current on every stop)
_<done · all 5 pieces landed, none blocked · nothing remains · see implementer report for the github/stackoverflow/twitter-x citation-count discrepancy against D14's counts>_

## Size

**~50 minutes.** This is **consolidation, not research.** Every method you write already exists somewhere in this repo — in a module bullet, in `ACCESS.md`, or in `agent-tooling.md`, and the URLs in them were verified in the previous task. **Do not search. Do not fetch. Do not verify URLs.** If a site file would need a method nobody has written down yet, write what is known and leave the gap explicit rather than inventing one.

## The format — all nine files use it exactly

```markdown
# <Site name> — <domain>

**Used by:** <comma-separated module names that reference this file>
**Reachable:** yes | no — <substitute, if no> · <date, only when a verdict was actually tested>

## Query
- <the access method: `site:` query, URL pattern, or JSON endpoint>

## Worth knowing
- <2-5 bullets: what works, what wastes budget. Omit the section entirely rather than padding it.>
```

**Hard cap 20 lines per site file.** These are small on purpose. `Reachable:` carries a date **only** where a verdict was actually tested — Reddit and nothing else. For the other eight write `**Reachable:** yes` with no date; do not invent test results.

`Used by:` is a hint, verified by `grep`, not a contract. List the modules you actually edited in piece 3.

## Design — numbered pieces (status: `[ ]` not started · `[x]` done · `[!]` blocked)

- [x] **1.** `[S]` **Create `skills/web-search-modules/sites/` and write the four multi-module files**: `github.md` (6 modules), `stackoverflow.md` (3 — name it `stackoverflow.md`; it is a *site* file and is unrelated to the topic module of the same name, which stays where it is), `reddit.md` (3), `huggingface.md` (3). Source the content from what already exists: GitHub's method from `agent-tooling.md`, Reddit's verdict and substitute from `ACCESS.md`'s Reddit section, the rest from the bullets in the modules that name them.
- [x] **2.** `[S]` **Write the five two-module files**: `openrouter.md`, `hacker-news.md`, `devto.md`, `artificial-analysis.md`, `twitter-x.md`. _(depends on #1 for the established format)_ Same rule — consolidate what the modules already say. `twitter-x.md` will be thin; that is a correct outcome, not a reason to pad it.
- [x] **3.** `[M]` **Add the path citation to every module bullet that names one of the nine.** _(depends on #1, #2)_ The bullet keeps its own self-sufficient one-line access method and gains `See \`sites/<slug>.md\`.` **The bullet must still work if nobody opens the site file** — do not move the access method out of the bullet and into the file. Line counts stay under 40; `academic-papers.md` is at 31 and `general-web.md` at 33, so append inline.
- [x] **4.** `[S]` **Strip the `[ACCESS:reddit]` markers** from `general-web.md`, `competitor-content.md`, `vendor-landscape.md`, and `ACCESS.md`. _(depends on #3)_ The path citation added in #3 replaces them entirely.
- [x] **5.** `[S]` **Move Reddit out of `ACCESS.md`.** _(depends on #1)_ Its verdict and substitute become `sites/reddit.md`'s `Reachable:` line. Replace the section with a one-line pointer. `ACCESS.md` keeps "JS-shell pages" and the JSON-endpoint scope note, which have no site to live in. Update its header paragraph so it describes what it actually still holds.

## Files

- `skills/web-search-modules/sites/*.md` — pieces 1, 2 (new directory, 9 new files)
- `skills/web-search-modules/*.md` — pieces 3, 4 (citations; bullets otherwise untouched)
- `skills/web-search-modules/ACCESS.md` — pieces 4, 5

## Tests (add; keep the suite green)

1. `python3 -m py_compile skills/research/validate_json.py` still passes (should be untouched).
2. **Every site file is ≤20 lines** and every module stays **<40**. Report before/after for each module touched.
3. **`grep -rl "sites/reddit.md" skills/`** returns every module that names Reddit — this is the revert-list mechanism working. Same spot-check for `sites/github.md`.
4. **`grep -rn "ACCESS:reddit" skills/` returns nothing.**
5. **Every module bullet you edited still names its own access method.** Read them back: a bullet reduced to only a pointer is a regression, not a simplification.

## Out of scope (do NOT do)

- **Do not search, fetch, or verify any URL.** Consolidation only. A method nobody has written down stays unwritten — say so in the report.
- **Do not wire site files into any agent or skill prompt.** D14: nothing loads them at runtime. No `Read` instruction, no mention in `ROUTING.md`, `SKILL.md`, or `agents/`.
- **Do not touch `ROUTING.md`** or any routing header. No module changes family, and site files are not routed to.
- **Do not rewrite the `stackoverflow.md` *module*.** That rewrite is still parked. `sites/stackoverflow.md` is a different file; creating it does not unpark the other.
- **Do not create a site file for a site named by only one module.** The threshold is two. Nine files, no tenth.
- **Do not create any file under `agents/`.**
- **Do not "improve" prose** in a module you are otherwise editing.
- Do not commit.

## Report back

Per site file: its line count and where its content came from. Per module: before/after line count and the citation added. Then, separately: **any site file that came out thin because the method was never written down anywhere** — that is the list that tells the planning thread what still needs discovering.
## ✅ Done (collapsed — full detail in the planning doc's session log)

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
