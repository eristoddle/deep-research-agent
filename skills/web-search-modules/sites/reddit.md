# Reddit — reddit.com

**Used by:** competitor-content, general-web, vendor-landscape
**Reachable:** yes — public Atom feeds only, via `skills/research/reddit_feed.py` · 2026-09-04

## Query
- Every scraper route into Reddit still fails: `WebFetch` is refused by the harness at the domain level, `crwl` cannot parse the feed XML anyway, and Firecrawl refuses the domain by vendor policy (*"we do not support this site"*, tested on both `old.` and `www.`, listing and thread).
- **The public Atom feeds are the one open route.** `skills/research/reddit_feed.py` reads `/r/<sub>/.rss` and `/r/<sub>/search.rss` with the stdlib — no account, no token, no API registration. Invoke it with `--json --limit 25 --max-attempts <remaining-fetch-budget>`; each attempt, including a `429` backoff retry, is a real network request and counts against the caller's fetch budget.
- `www.reddit.com` only. `old.reddit.com` now 302s and is degrading; never prefer it.

## Worth knowing
- **Listings only.** Output is title, permalink, date, and subreddit per entry — the reader never returns a post's body or its comments. That is a narrower, cheaper unit than a full thread and the right one for a repetition/listing-level signal; full bodies are a separate, later job this helper does not do.
- The `WebSearch` layer fails *silently* on Reddit — ten plausible results from unrelated domains (Etsy community, SBA, slideshare), no error. Use the feed reader instead of relying on `site:reddit.com` search results.
- The search feed (`search.rss`) mixes matching *subreddits* into results alongside matching *posts*; the reader already filters to permalinks containing `/comments/`, so this is handled for you rather than something a caller needs to re-check.
- The `.json` endpoint exists on every view but is not reachable by any route this toolchain has; it is not a substitute for the Atom feed.
