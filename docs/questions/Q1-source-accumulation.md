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
