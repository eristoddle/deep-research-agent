# Reddit — reddit.com

**Used by:** competitor-content, general-web, vendor-landscape
**Reachable:** no — niche forums on the same topic, `people also ask <query>`, search-suggestion autocomplete · 2026-09-03

## Query
- Every route inside `web-search-agent`'s tool discipline fails: `WebSearch site:reddit.com`, `WebFetch` on `www.reddit.com`/`old.reddit.com`, `curl` with a browser User-Agent on the `.json` endpoint, and the `crwl` carve-out.

## Worth knowing
- The search layer fails *silently* — ten plausible results from unrelated domains (Etsy community, SBA, slideshare), no error.
- **Settled 2026-09-03**, re-tested on a second machine and a different IP: `curl` gets a 302 to the login wall, `crwl` gets a 174-byte login page. Not an IP artifact.
- **Firecrawl refuses Reddit by policy**, not by block: *"we do not support this site."* Same on `old.` and `www.`, listing and thread. A control scrape elsewhere succeeded. A proxy pool cannot route around a vendor's refusal, so no scraper rung will help.
- **But the Atom feed is open.** `curl https://www.reddit.com/r/<sub>/.rss` returns real current listings, no auth, 200. `WebFetch` is refused on the domain by the *harness*, and `crwl` cannot parse XML — so the block is in our tooling, not at Reddit. Listings are the right unit anyway. Reopened; see Q3.
- `old.reddit.com` now 302s and is degrading. Do not prefer it.
- The `.json` endpoint exists on every view but isn't reachable by any route this toolchain has. The "JSON endpoint beside the HTML page" trick that works for Discourse forums is falsified for Reddit specifically.
