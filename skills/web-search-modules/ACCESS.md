# Access — known-unreachable venues

Shared record of what has no site to live in: venue reachability that isn't tied to one named
site, and the scope of the JSON-endpoint tactic. Not a module, not routed to — a module's
fourth-form directive cites a section here rather than restating the finding inline.
Hand-authored only; nothing writes to this file at runtime.

**This is a maintenance index, not a runtime file.** Nothing loads it during a run and nothing
should — the substitute already lives inline in the module bullet, which is what the agent acts
on. Do not wire it into an agent prompt. Every verdict here is dated and expected to expire.

**Reddit's reachability verdict moved to `sites/reddit.md`'s `Reachable:` line** — it has its own
site file now, so it no longer lives here. `grep -rl "sites/reddit.md"` is the revert-list
mechanism for it.

## JS-shell pages

**Fails:** a page whose content arrives via client-side JS render (e.g.
`forum.obsidian.md/search?q=`). The `crwl` fallback escalates cleanly and its `head -c 40000`
bound holds, but it snapshots before the async content loads. **Tried:** `WebFetch`
(placeholder page), then `crwl` (result count rendered, no actual results).
**Substitute:** look for a JSON endpoint beside the HTML page before escalating to `crwl` at all.
**2026-08-29.** Cite `docs/parking-lot/verify-crwl-fallback.md`.

## "JSON endpoint beside the HTML page" — scope

Not a general fix. **Holds** for Discourse forums — confirmed on the Obsidian forum's
`search.json`. **Falsified** for Reddit: the `.json` endpoint exists on every view but is not
reachable by any route this toolchain has — see `sites/reddit.md`.
**2026-09-03.** Cite `docs/parking-lot/search-layer-refusals.md`.
