# Competitor Content Module

**Family:** Published-content landscape
**Use when:** The question is what has already been published on a topic and what those pages cover — coverage gaps, the shape of what ranks, the questions readers ask that nothing answers.
**Do not use for:** Whether the claims in those pages are *true* (route to the topic's own family), or keyword volume, difficulty, and ranking position — see the limits below.
**Siblings:** `general-web` — pair them when you need both what competitors say and what practitioners report.

## Sources

**None by design.** The result list *is* the source — see the first bullet below. Pinning a fixed set of sites would defeat the sampling this module exists to do.

- **A plain, unrefined `WebSearch` of the query a reader would actually type.** The result list is the sample. Resist improving the query: a better query returns a better answer and a *worse* sample of what the reader will see.
- **The top-ranking pages themselves**, 3-5 of them, fetched and read for **structure** — H2/H3 outline, what gets defined, what gets compared, what gets cited, roughly how long. Not for prose.
- **`people also ask <query>` as its own search** — surfaces the question set around the topic.
- **Query variants** — the same topic phrased as a beginner, a buyer, and a practitioner would phrase it. Each returns a partly different set, and the union is the real landscape.
- **Reddit and forum threads on the query** — where the questions that no ranking page answers get asked out loud. Usually the richest source of a genuine gap. Read Reddit through the approved Atom-feed listing reader (titles and permalinks, not full threads) and pair it with niche forums and `people also ask` for the same signal in more depth. See `sites/reddit.md`.
- **The commissioning site's own existing content**, when the project has a list of it. Prevents re-covering ground and surfaces internal link targets.

## Query tactics

- **Fetch for the outline, report the outline.** The useful output is a union of subtopics across competitors, then the short list of what your material covers that none of them do. Prose summaries of competitor articles are not worth their context cost.
- **Note the dominant format** — listicle, glossary entry, tutorial, comparison table. What ranks tells you the shape the topic is expected to arrive in, which is a decision input even when you break it deliberately.
- **Date every page you read.** A topic where everything ranking is two years old is an opening; a topic refreshed last month is not.
- **Look for the question nobody answers.** Cross the PAA and forum questions against the competitor outlines. Anything asked often and answered nowhere is the gap worth writing.

## Limits — state these rather than filling them in

`WebSearch` returns a result list, not a SERP. You cannot see ranking positions, search volume, keyword difficulty, or the live PAA box, and no amount of querying will produce them. Never estimate them; say the tooling does not provide them. Anyone who needs those numbers needs a keyword tool.

If the caller is doing brief-level SEO work rather than per-item research inside a pipeline run, the `ct-seo-research` skill is the better instrument — it runs a fuller SERP scan, extracts competitor pages with `defuddle`, and writes a structured SEO block into the brief. Say so instead of half-reproducing it.
