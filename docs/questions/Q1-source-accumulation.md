# Q1 — Should modules accumulate sources over time, and which kind can?

**Status:** open. Raised 2026-08-21.

## The question

Modules are static reference files. `CLAUDE.md:110` states the current stance outright: *"Modules do not self-update by design — re-run the skill or edit by hand."* Should that hold?

The intuition against it: a site-based module like `github-debug` never needs to change — the source *is* github.com, and that URL will be the same in five years. But a module whose sources depend on the topic has no fixed list, and every research run discovers sources that the module didn't know about and then throws them away.

## What D1 settles, and what it doesn't

The three-kind taxonomy (PLAN.md D1) answers *where* accumulation could even apply:

- **Fixed-site** — nothing to accumulate. The site list is stable by construction.
- **Parameterized** — **this is the only kind where accumulation pays.** The seed list of vendors/leaderboards is exactly the thing that grows as more of them get researched. A `pricing` module that has seen forty providers is genuinely better than one that has seen four.
- **Open-query** — cannot accumulate. Sources are whatever the query returned; that is the design.

So the question narrows to: should parameterized modules grow their seed lists automatically?

## What makes it feasible

Two pieces already exist:

- **A completed run leaves the evidence.** `{topic_slug}/results/*.json` records the URLs each item agent actually used. The sources that answered a question are already on disk after every run.
- **There is a home that survives installs.** `.claude/web-search-modules-local/` is project-owned and APM never touches it, unlike `skills/web-search-modules/` which is overwritten on every install. An accumulated, project-specific source list belongs in the local tree by construction — writing one into the package tree would be deleted by the next `apm install`.

## The tension

Automatic accumulation fights the reason `/research-add-module` exists. That skill *tests* whether a source actually holds a domain's answers and whether the module beats `general-web` before keeping it. A URL harvested from a run is only evidence that an agent fetched it once — not that it was load-bearing, not that it was correct, and not that it will still be there next month. Harvesting uncritically would refill modules with exactly the guessed-quality sources the skill was built to prevent.

Possible middle ground worth thinking about: harvest into a *candidate* list that a human or `/research-add-module` promotes, rather than into the source list directly. That keeps discovery automatic and keeps judgment manual — the same split D2 relies on.

## What would need deciding

1. Candidates-only, or direct into the seed list?
2. What evidence justifies promotion — appeared in N runs? was quoted in the final report? survived a fetch check?
3. Does this live in the pipeline (a step after `/research-deep`) or as a separate skill invoked on demand?
4. Does it change `CLAUDE.md:110`, or is a candidate list narrow enough that "modules do not self-update" stays true as written?

## Related

- PLAN.md **D1** (kinds), **D2** (no speculative modules)
- Parking lot: [harvest-from-runs](../parking-lot/harvest-from-runs.md)

---

## 2026-09-04 — grill round 1; the capture half is settled, and its premise was wrong

**This page's central factual claim was false.** It stated that "`{topic_slug}/results/*.json` records the URLs each item agent actually used" and built the whole harvest idea on that. Verified against a real run (`AUQ/rough/DeepInfra/research/inference-speed-cost`): each result file contains **exactly one URL**, and only because that project's `fields.yaml` happened to declare a `pricing_source_url` field. The results record *answers*, not where the answers came from. Nothing is accumulating today.

So harvesting was never the first problem — **capture** is. Whatever gets built can only see runs from the day capture is turned on; existing runs are not recoverable.

Five questions answered this round, all confirming the recommended option:

1. **The capture rule lives in the agent prompt, not in `fields.yaml` convention.** A convention you must remember is one that gets forgotten on the run that mattered — which is exactly how the one-URL-per-item state arose. Same home as `unreachable[]`.
2. **Only URLs that contributed to an answer** are recorded, not every page opened. Dead ends are already `unreachable[]`'s job, and a list of everything opened is noise that would make any promotion threshold meaningless.
3. **Each entry takes the same three-key shape as `unreachable[]`** — URL, source name, and the fields it supported. The field list is what proves a source was load-bearing rather than merely fetched, which is the entire basis for promoting it later.
4. **The harvest writes a candidate list, never straight into a module.** Direct writes would refill modules with the guessed-quality sources `/research-add-module` exists to filter out. Discovery automatic, judgment manual — the same split D2 relies on.
5. **A new skill, `/research-harvest`, invoked manually.** Not after every run: two of three runs in the live AUQ project stopped at `findings.md` and never reached the report step, so anything hanging off `/research-report` would never fire there. A separate skill also keeps it out of context until wanted.

**Still open:** what earns a candidate promotion into a module's source list (depends on 2 and 3, so it was deferred to round 2), where the candidate file lives, and what `/research-harvest` scans.

**Incidental finding, not a design question:** `skills/research/validate_json.py:22` has `_SKIP_KEYS = {"_source_file", "uncertain"}` — `"unreachable"` was never added when that shipped earlier the same day, so it prints under "Extra fields". Tested: cosmetic only, no false pass, because the walker never descends into the array. A `sources[]` array will need the same one-word addition.

## 2026-09-04 — grill round 2; the harvest half settles, frontier empty

1. **Promotion threshold: a candidate needs at least 3 separate runs, and must have supported a field in at least 2 of them.** One appearance is an accident. The second clause is what round 1's answers bought — without the per-entry field list, this would collapse back into counting fetches.
2. **One candidate file per project**, at `.agents/web-search-modules-local/CANDIDATES.md`. Not one per module: which module a source serves is part of what the human is reviewing, so splitting by module up front forces that judgment too early.
3. **`/research-harvest` scans every run under the research root by default**, with an option to name a single run. Recurrence across runs is the entire signal and is invisible from inside one run; `INDEX.md` already enumerates them.
4. **`/research-report` does not render sources by default; it renders them on request.** "On request" means **asked for in the prompt, not a formal flag** — the user's own use of the pipeline varies run to run (sometimes a readable report, sometimes only raw material for an article), and that flexibility through prompting is a property worth preserving rather than formalizing into an option.
5. **Existing runs get nothing.** They have no captured sources and cannot acquire them retroactively; reconstructing which URL answered which field would mean re-running paid research against data that never recorded it. Let them age out.

**Frontier empty.** Every branch visited. The remaining work is mechanical and belongs in the task queue, not here.
