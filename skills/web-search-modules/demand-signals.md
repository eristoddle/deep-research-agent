# Demand Signals Module

**Family:** Demand signals
**Use when:** The task is to find what people repeatedly want, struggle with, or complain about, in their own words, across places that don't talk to each other — the repetition itself is the evidence (a product-gap search, a frustration audit, "what do people keep asking/complaining about X").
**Do not use for:** Whether existing published content already covers a topic, or what ranks for a query — that is `competitor-content`'s job. It reads the same forum layer but as *contrast against ranked pages*; here the forum layer is the evidence itself, not context for a coverage gap. "What's missing from what's written" routes there; "what people keep saying is wrong" routes here.
**Siblings:** `competitor-content` (mirror image), `general-web` (pairs for corroboration).

## Sources

- **The domain's own niche forum, found by search, not guessed.** If it runs Discourse — test `<forum-root>/search.json?q=<terms>`, returns JSON directly — use that; confirmed on `forum.obsidian.md` and `community.home-assistant.io`. If not (XenForo, vBulletin, phpBB — XenForo's own community confirms search is POST-only with no public GET route; direct fetch 403'd on `forums.macrumors.com`), fall back to `site:<forum-domain> <terms>` as an ordinary WebSearch — confirmed returning specific, on-topic threads.
- **`people also ask <query>` as its own separate WebSearch**, not a refinement of the main query — surfaces the adjacent-question set people actually type. Same tactic `competitor-content` uses; here the questions are the signal, not context for a gap.
- **Search-suggestion completion** — `https://suggestqueries.google.com/complete/search?client=firefox&q=<partial phrase>` returns raw autocomplete strings for a partial phrase; confirmed live 2026-09-05. Unofficial and undocumented — if it 404s or empties, drop it rather than guessing a replacement.
- **Review sites** — `https://www.trustpilot.com/review/<company-domain>` fetches cleanly and surfaces recent 1-2 star reviews directly; confirmed on `fezibo.com` and `notion.so` 2026-09-05. Find `<company-domain>` with one WebSearch (`<brand> trustpilot`) first — a guessed domain is as bad as a guessed URL. **Know what this venue skews toward:** its low-star reviews are dominated by billing, refunds, and support grievances, which are a real recurring frustration but not a product gap. Use it for *how a company treats people*; go to the forum bullet for *what the product cannot do*. Do not report a page of refund complaints as evidence that a feature is missing.
- **Amazon product Q&A — unreachable.** `/ask/questions/<id>/` pages return 503 on every product tested, on both `amazon.com` and `us.amazon.com`; WebSearch does not surface the Q&A content as a snippet either. Use the review-site bullet above, or a vendor's own on-site reviews, for the same buyer-voice signal instead.
- **Reddit — at most one listing-level pass, never this module's only evidence.** Read via the approved Atom-feed reader; see `sites/reddit.md`.

## Query tactics

- **Full threads are the wrong unit.** Recurrence across venues is a listing/title-level signal — many titles cheaply beats a few threads read deeply. At `standard`'s 12 fetches, spend them opening listings and search hits across venues; open a full thread only for verbatim wording, once the same complaint has already recurred elsewhere.
- **Phrase it like the frustrated user, not the marketer** — "keeps happening", "first year", "why does X always", "what's missing from" — not the product-category term a vendor would use.
- **A pattern needs two independent venues before it counts.** The same complaint in a forum, a review site, and a PAA result is the signal; the same complaint appearing only across SEO listicles is one source repackaged, not repetition — drop those, per the general module-authoring rule.
