# Vendor & Competitive Landscape Module

**Family:** AI ecosystem & market
**Use when:** The question is who else is in a category, what each one claims, and how they position against each other — competitive sets, alternatives, "X vs Y", category maps.
**Do not use for:** Which is objectively better on a measurable axis (`benchmarks`), or what they charge (`pricing`).
**Siblings:** `general-web` — pair them by default here. This module finds what vendors say; `general-web` finds whether users agree.

## Sources

- **The vendor's own site**, read in this order: product pages (the claim), docs (whether it ships), changelog (whether it is maintained), customers and case studies (who actually uses it). A gap between the product page and the docs is the most useful thing you can find. Fetch `<vendor's domain>/pricing`, `/docs`, `/changelog`, `/customers` directly — there is no fixed seed list, the vendor is whichever one the task names.
- **Vendor-authored comparison pages** — "X vs Y", "alternatives to X". Structurally biased and still valuable twice over: they reveal how a company positions itself, and they name its competitive set for you. Query form: `"alternatives to <product>"` and `"<product> vs"`, then fetch what those return.
- **Review aggregators** — G2, Capterra, TrustRadius, Gartner Peer Insights. Good for who is in the category and recurring complaints; weak on recency and easily gamed. G2 and TrustRadius return 403 to a direct fetch — reach all four via `site:g2.com`, `site:capterra.com`, `site:trustradius.com`, `site:gartner.com/reviews` plus the product name; `capterra.com` also fetches directly.
- **Practitioner threads** — Hacker News and topic subreddits on the category, especially migration stories ("we moved off X"). Unfiltered and the fastest route to the failure modes no vendor page lists. Hacker News: `site:news.ycombinator.com`. See `sites/hacker-news.md`. Reddit is unreachable from this toolchain — use niche forums and Hacker News for the same signal instead. See `sites/reddit.md`.
- **Company registries** — Crunchbase, YC directories, funding coverage — when the question is who exists and at what stage, not what they do. Verified working: `https://www.crunchbase.com/`, `https://www.ycombinator.com/companies`.

## Query tactics

- **Build the competitive set from the vendors themselves.** Search `alternatives to <product>` and `<product> vs`, then harvest every name that appears on more than one vendor's comparison page. That converges faster than trying to enumerate a category from scratch.
- **Use the category term the vendors use.** They rarely agree; collect the two or three competing labels and search each, because each returns a partly different set.
- **Read the target's own positioning language before any third-party description of it.** Third-party summaries drift toward the category cliché, which is exactly the thing a positioning question is trying to see past.
- **Separate claim from evidence in the output.** Product page = claim. Docs, changelog, pricing page, public repo = evidence. Report both and mark which is which.
- **Verify claimed features actually ship**: search the docs for the feature name, check the changelog for when it landed, look for a "coming soon" or waitlist qualifier.
- Date review-site and analyst data explicitly — it skews a year or more stale and reads as current.
- When researching one client against its competitors, the same module serves both sides. Apply identical scrutiny to each, and do not let the client's framing set the category boundary.
