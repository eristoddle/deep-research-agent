# Roadmap

Intentions, not instructions. Nothing here is read at runtime — the operational rules live in `skills/web-search-modules/SKILL.md` and `ROUTING.md`, and a roadmap shipped inside a skill payload goes stale in every install that has it.

## Modules added since the fork

Upstream shipped five: `github-debug`, `stackoverflow`, `academic-papers`, `chinese-tech`, `general-web`. Everything below was written here.

| Module | Family | What it is |
|---|---|---|
| `benchmarks` | AI ecosystem & market | Published evaluation numbers — arenas, leaderboards, harness repos, model cards. Sources ordered by *independence*; the run configuration and an observation date are mandatory, and self-reported scores are labeled as such. |
| `model-releases` | AI ecosystem & market | What shipped, what changed, what it is called, whether it still exists. Docs model-lists and deprecation pages outrank announcement posts; model IDs over marketing names. |
| `pricing` | AI ecosystem & market | Cost, rate limits, quotas, regional availability. The provider's own page is the only quotable source, and every figure carries its unit, its host, and the date it was read. |
| `vendor-landscape` | AI ecosystem & market | Who else is in a category and what each claims. Builds the competitive set from vendors' own comparison pages, and separates claim (product page) from evidence (docs, changelog, pricing). |
| `competitor-content` | Published-content landscape | What has already been published on a topic and what it covers. Samples an unrefined reader-query search, reads top pages for *outline* rather than prose, and returns the coverage gap. States its SERP limits instead of inventing volumes or positions. |

The first four landed together as one family because they overlap deliberately; `ROUTING.md` disambiguates them by what the answer *is*. `competitor-content` is the first family question that is not about technology at all.

## Retrofit: access methods

`SKILL.md` requires every source in a module to carry an access method — a `site:` query, a tested search-URL pattern, a stable index page to fetch directly, or a note that it blocks fetching. **None of the ten current modules has one.** The requirement was added after they were written, so the spec and the payload disagree. `/research-add-module` produces modules that comply; the existing ten need a pass. `pricing` and `benchmarks` are the highest value (provider pricing pages and leaderboard URLs are stable and worth naming outright), `competitor-content` the lowest (its sources are by definition whatever the query returns).

## Fill in `stackoverflow.md`

Twelve lines, two source bullets, no query tactics at all — the weakest module in the set and the only one still carrying nothing but upstream's source list. It routes on real traffic, so it should earn its slot.

## Wanted modules

- **AI writing and prompting communities** — where practitioners compare model output: r/LocalLLaMA, r/WritingWithAI, Discord digests, practitioner blogs. Distinct from `general-web.md`, which is aimed at software best practices. The gap that shows up when a question is "is this model any good at writing", which currently routes to bare `general-web`.
- **Docs and API reference** — reading a product's own documentation as a primary source, as distinct from `vendor-landscape`'s reading of its marketing.

Extend the AI ecosystem & market family rather than adding near-duplicates beside it. Non-technical families (health, law and policy, finance, history) attach the same way: one new family row in `ROUTING.md` with its own yes/no question. `competitor-content` is the worked example — its family question is not about technology at all.

## Verify the fetch fallback

The `crwl` escalation has never fired in a real run. Both failures in the first live test were a 404 and a page that simply lacked the data, both correctly handled by searching instead. It needs one genuine 403 or JS-shell page to confirm the rule works and the `head -c` bound holds.

## Why `chinese-tech` stays

A large share of open-weight model work and evaluation happens on Chinese platforms, and those results are often published there first and sometimes only there. It is a genuine coverage advantage, not dead weight. The mistake to avoid is letting it pull a project's *framing* toward Chinese models when that was not the question — which is why it was demoted to a modifier rather than a topic module, and why that warning is in the module's own `Do not use for` line where the agent actually reads it.
