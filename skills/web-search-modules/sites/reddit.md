# Reddit — reddit.com

**Used by:** competitor-content, general-web, vendor-landscape
**Reachable:** no — niche forums on the same topic, `people also ask <query>`, search-suggestion autocomplete · 2026-09-03

## Query
- Every route inside `web-search-agent`'s tool discipline fails: `WebSearch site:reddit.com`, `WebFetch` on `www.reddit.com`/`old.reddit.com`, `curl` with a browser User-Agent on the `.json` endpoint, and the `crwl` carve-out.

## Worth knowing
- The search layer fails *silently* — ten plausible results from unrelated domains (Etsy community, SBA, slideshare), no error.
- All five routes were tried together on one run, one machine, one IP, one harness build. Firecrawl was untested — the one rung with a proxy pool. Not settled; see Q3.
- The `.json` endpoint exists on every view but isn't reachable by any route this toolchain has. The "JSON endpoint beside the HTML page" trick that works for Discourse forums is falsified for Reddit specifically.
