# Search-layer refusals — the failure no fetch escalation can fix

**Parked** 2026-09-02, from evidence in four live `/research-deep` runs (a Firecrawl cookbook in the `sm-static` blog repo). Full row-by-row log lives there: `research/FETCH-BLOCKING-LOG.md`.

## The distinction

Two failures look alike in a run report and need opposite fixes:

| Layer | What happens | What fixes it |
|---|---|---|
| **Fetch** | URL is in hand; `WebFetch` returns 403 / 429 / binary | escalate the fetcher — the `crwl` carve-out, now live-fire validated at 6/7 (see `verify-crwl-fallback.md`) |
| **Search** | `WebSearch` will not return the domain at all: `400 — not accessible to our user agent` | **nothing at the fetch layer** — there is no URL to escalate to |

The second kind is invisible in the current model, because every tool we have for reaching a blocked source assumes a URL already exists.

## What it cost, concretely

Two runs named Reddit as their **primary** source and got nothing from it:

- `obstacle-corpus-inverted` — mining r/webscraping for people describing sites they fought to reach. Fell back to Hacker News and GitHub; the run reported itself **under-sampled relative to what exists**.
- `vocabulary-ladder-price-monitoring` — collecting how sellers phrase a problem in their own words, from r/ecommerce, r/smallbusiness, r/Flipping, r/AmazonSeller. Fell back to eBay/Amazon/Shopify community forums, which did yield verbatim language, but the run's search-phrasing fields are reconstructed from forum prose rather than observed and are marked uncertain.

Stack Overflow refused identically in the first of those. That is notable given `stackoverflow.md` is a shipped module routing on the most-hit family — **the module routes to a source the toolchain cannot currently reach**, which is a sharper problem than the thinness already recorded in `stackoverflow-rewrite.md`.

## The likely fix, and why it is already this repo's answer

`verify-crwl-fallback.md` reached it independently: **look for a JSON endpoint beside the HTML page.** Discourse `search.json` beat both `WebFetch` and `crwl` on the Obsidian forum.

Both blocked sources here have the same property:

- **Reddit** exposes JSON on essentially every view — append `.json` to a listing, thread, or search URL.
- **Stack Exchange** has a documented public API (`api.stackexchange.com`), which is a better source than scraped question pages regardless of blocking.

So this is not a new mechanism. It is the existing "JSON endpoint first" finding, applied to two sources where the HTML route is not merely worse but **entirely unavailable** — which is what promotes it from a tactic to an access method.

## Shape of the work, if it ripens

Access-method-shaped, which means it may belong inside the active retrofit rather than beside it:

- `SKILL.md` already allows "a note that it blocks fetching" as a valid access method. That form is **necessary but not sufficient** here — a note tells the agent to give up, where a JSON endpoint would let it succeed. Worth deciding whether the taxonomy needs a fifth form: *an API or JSON endpoint that replaces the HTML route*.
- `stackoverflow.md` would gain `api.stackexchange.com` as its real access method. Note the active task's piece 5 explicitly scopes that file to `site:` queries only, so **this must not be smuggled into that piece.**
- Reddit has no module today. Whether it needs one, or belongs as sources inside an existing family, is undecided — and `PLAN.md` D2 bars new modules until a real project needs one. Two runs losing their primary source is arguably that trigger; that is a judgment call for the planning thread, not something to assume here.

## Open questions

1. Does the three-kind access-method taxonomy need a fourth kind for API/JSON-replaced sources, or does that collapse into *parameterized*?
2. Is a Reddit module justified under D2, or is this two source bullets in existing modules?
3. Does the search-layer refusal reproduce, or was it transient? Worth one cheap check before building on it — the evidence is four runs on two days, all with the same tooling.
4. Would routing fetches through the blog repo's `fetch-anything` skill (which already owns a defuddle → crawl4ai → firecrawl ladder plus per-domain handlers including Reddit) be a cheaper answer than reimplementing handlers here? It centralises domain knowledge but crosses a repo boundary and may not survive the agent's fetch-budget accounting.
