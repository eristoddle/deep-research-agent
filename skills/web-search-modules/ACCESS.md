# Access — known-unreachable venues

Shared record of venues confirmed unreachable from this toolchain: what fails, what was tried,
and the substitute. Not a module, not routed to — a module's fourth-form directive cites a
section here rather than restating the finding inline. Hand-authored only; nothing writes to
this file at runtime.

**This is a maintenance index, not a runtime file.** Nothing loads it during a run and nothing
should — the substitute already lives inline in the module bullet, which is what the agent acts
on. Do not wire it into an agent prompt. Every verdict here is dated and expected to expire; the
bullets resting on one carry its tag (e.g. `[ACCESS:reddit]`), so `grep -rl "ACCESS:reddit"`
prints everything to revert when it flips.

## Reddit `[ACCESS:reddit]`

**Fails:** every route inside `web-search-agent`'s tool discipline — `WebSearch
site:reddit.com`, `WebFetch` on `www.reddit.com`/`old.reddit.com`, `curl` with a browser
User-Agent on the `.json` endpoint, and the `crwl` carve-out. The search layer fails *silently*:
ten plausible results from other domains (Etsy community, SBA, slideshare), no error.
**Tried:** all five routes above, together, on one run. **Substitute:** niche forums on the same
topic, `people also ask <query>`, search-suggestion autocomplete.
**2026-09-03.** One machine, one IP, one harness build; firecrawl untested and is the one rung
with a proxy pool. Not settled — see [Q3](../../docs/questions/Q3-reddit-reachability.md).

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
reachable by any route this toolchain has (see Reddit, above).
**2026-09-03.** Cite `docs/parking-lot/search-layer-refusals.md`.
