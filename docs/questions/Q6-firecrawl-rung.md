# Q6 — Should firecrawl become a third fetch rung in the shipped agent?

> **Status:** open
> **Opened:** 2026-09-03 · **Last touched:** 2026-09-03

## The question

Two different uses of firecrawl are being conflated, and separating them is most of the answer.

- **As a maintainer tool** — running the Q3 re-test to find out whether Reddit is reachable. Needed now, costs one person's own API credit, ships to nobody. Not in question.
- **As a third rung inside `web-search-agent`** — after `WebFetch` and `crwl`, a shipped consumer-facing escalation. This is the open one.

## Thread

> Append-only. Each grill round adds a dated section below the existing ones.

### 2026-09-03 — opened

Raised when the user pointed out this is a public package: *"remember this is also a public skill, people can install it on their computers."*

**What makes it harder than adding a rung.** The fetch carve-out in `agents/web-search-agent.md` is written as a single narrowly-bounded exception, and `CLAUDE.md` states outright that every clause is load-bearing: already-failed, one retry, same fetch slot, stdout only, bounded output, no `--deep-crawl`, no `-O`, no install, no second helper. It ends with "no second helper" — the sentence a third rung directly contradicts. Loosening it is described as the thing that turns a narrow exception into general permission to script around blocks.

**And firecrawl is paid.** Unlike `crwl`, using it spends the consumer's money. It can never be a silent default; at minimum it is opt-in, and the consumer has to know the cost before it fires. That is a materially different contract from "use this free helper if you happen to have it."

**The cheap answer worth considering first:** firecrawl stays a maintainer tool and never ships. The package's job would then be to *record what firecrawl found* — Reddit reachable or not — into `ACCESS.md`, so consumers get the knowledge without the dependency or the bill. That fits how the access layer already works: findings are written down once, not rediscovered per install.

**The case against that:** a consumer who *has* firecrawl and *wants* to spend on it gets nothing, and `ACCESS.md`'s verdict is then wrong for them specifically — their toolchain can reach what ours cannot. The existing prompt already gestures at this: *"If the project or user has a dedicated fetch-escalation skill available locally, prefer it over calling `crwl` directly."* That sentence may already be the extension point, in which case no new rung is needed at all — `fetch-anything` is exactly such a skill, and it owns the firecrawl ladder including the Reddit handler.

### 2026-09-04 — Q3 no longer blocks this

Q3 found a public-feed path for Reddit and D15 permits the approved `reddit_feed.py` helper
to use it. Firecrawl therefore has no Reddit-access motivation: the question is solely whether
a paid, consumer-facing third fetch rung adds enough value on *other* sites to justify its
cost and a new exception to the current tool discipline.

## Blocked on

- Nothing external. This is a product and tool-discipline decision.

## Related

- `PLAN.md` **D13** — the setup-documentation rule this would trigger, including the paid-API opt-in and the referral link
- `PLAN.md` **D8** — the deferred "second tool-discipline carve-out" half, which is this question
- `CLAUDE.md` — the fetch carve-out's clause-by-clause rationale, and "no second helper"
