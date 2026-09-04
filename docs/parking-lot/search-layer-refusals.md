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

---

## 2026-09-03 — retested; the proposed fix is falsified for Reddit

Grill round 1. This page's four open questions are now partly answered, and its **central
proposal does not survive contact with Reddit.**

**Q3 above ("does the refusal reproduce, or was it transient?") — it reproduces, and it is worse
than recorded here.** This page logged it as `400 — not accessible to our user agent`. What a
`site:reddit.com` search actually returned was ten clean, plausible results from *other domains*
(Etsy community, SBA, slideshare) and no error at all. That is **silent substitution**, not a
refusal: the run looks like it succeeded. It also explains the fallback logged above —
`vocabulary-ladder-price-monitoring` "falling back to eBay/Amazon/Shopify community forums" was
very likely not the agent's judgment, it is what the search tool handed it.

This is what became `PLAN.md` **D7**.

**The "JSON endpoint first" fix is falsified for Reddit.** This page proposed it as the answer,
carried over from the Discourse win in `verify-crwl-fallback.md`, on the reasoning that "Reddit
exposes JSON on essentially every view." The endpoint exists; it is not reachable:

- `WebFetch` on `www.reddit.com` **and** `old.reddit.com` → `Claude Code is unable to fetch from
  <host>`. A harness-level refusal, not a Reddit 403 — so the URL form is irrelevant.
- `curl` + browser User-Agent → `.json` → `403`.
- `crwl` on `old.reddit.com` → login wall, 238 bytes.

The heuristic remains correct for Discourse and other server-rendered forums. It is **not** the
general rule this page reads as. Narrow it.

**Scope this evidence, do not universalize it.** All of the above is one machine, one IP, one
harness build, on one day. Two rows are IP-scoped (the `curl` 403, the `crwl` login wall) and one
is harness-scoped (the `WebFetch` refusal names Claude Code, not Reddit). **Firecrawl was never
tested** — the one rung with a proxy pool, and the rung `fetch-anything`'s Reddit handler reaches
for precisely because Reddit rate-limits by IP. The re-test procedure now lives in
[Q3](../questions/Q3-reddit-reachability.md); treat that as the deliverable rather than the table.

### Disposition of this page's four open questions

1. **Fifth access-method kind for API/JSON-replaced sources?** — **No.** Reddit is not
   API-replaced, so that was never the gap. The existing fourth form is instead sharpened from a
   passive note into a directive that names a substitute. → `PLAN.md` **D8**.
2. **Reddit module under D2?** — **Deferred**, and for a better reason than D2. A venue layer is
   worth little while the venue may be unreachable; it waits on [Q3](../questions/Q3-reddit-reachability.md).
   The routing shape, if it is ever built, is a **modifier** (the `chinese-tech` precedent), not a
   topic module.
3. **Does it reproduce?** — **Yes**, silently. Answered above.
4. **Route fetches through `fetch-anything`?** — **Still open.** Its Reddit handler's three rungs
   are each outside this agent's tool discipline: `.json` (confirmed dead), crawl4ai's *Python
   API* (more than the `crwl` CLI carve-out permits, and banned as agent-authored scripting), and
   firecrawl (paid, "no second helper"). Carried into [Q3](../questions/Q3-reddit-reachability.md)
   and [Q4](../questions/Q4-ledger-mechanics.md).

**Still parked**, but no longer for lack of evidence — the demand-signals work (`PLAN.md` **D9**)
was deliberately scoped to not need Reddit, which is what unblocks progress without resolving this.
