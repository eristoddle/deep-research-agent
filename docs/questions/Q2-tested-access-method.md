# Q2 — What makes an access method "tested"?

**Status:** open. Raised 2026-08-21. **Gates the retrofit's cost.**

## The question

`skills/web-search-modules/SKILL.md:36` calls for "a **tested** search-URL pattern." It does not say what testing means, and the answer decides whether the access-method retrofit is a two-hour text pass or a much longer verification pass.

The strong reason to care: a guessed URL is worse than no URL. With no URL the agent searches and finds the page. With a wrong URL it spends a fetch on a 404, and under a `standard` budget of 12 fetches that is real damage. So "tested" has to mean something, or the retrofit reintroduces the failure it exists to fix.

## Candidate standards, weakest to strongest

1. **It resolves.** Fetch returns 200. Cheap, catches typos and dead domains, proves nothing about content.
2. **It resolves and contains what the bullet claims.** Fetch and confirm the page is actually the pricing table / the leaderboard / the model list. Catches the common real failure: a vendor reorganizes and the old URL now redirects to a marketing page.
3. **It answers a real question better than `general-web` would.** The bar `/research-add-module` already applies to a whole module. Strongest, and far too expensive to apply per-URL across forty bullets.

The retrofit task currently assumes **(2)**. That is a judgment call, not a settled decision.

## The follow-on nobody has answered

Whatever standard is chosen, a URL verified today can rot. Nothing in the repo records *when* an access method was last confirmed, so a module cannot tell a fresh URL from a three-year-old one.

Options, none chosen:

- Record nothing; accept rot and fix on failure. Cheapest, and consistent with "modules do not self-update."
- Stamp an observation date per access method — but this costs lines, and the ~40-line budget is already tight (`academic-papers.md` is at 31).
- Stamp one date per module in its header. Cheap in lines, coarse in meaning.

Note the precedent: `pricing.md` **already requires an observation date for every figure it reports**. Requiring one for the module's own sources would be consistent — but the cost lands in context budget, not in the report.

## What would need deciding

1. Is standard (2) the bar? Confirm or move it.
2. Is a date recorded at all, and at what granularity?
3. What does the implementer do with a URL that fails verification — omit the bullet, keep the bullet without a URL, or mark it "blocks fetching"? (The third is a real category in the spec and may be the right answer for sources that 403.)

## Related

- PLAN.md **D1** (the line budget corollary)
- `TASKS.md` active task, Tests section — currently encodes standard (2)

---

### 2026-09-03 — the staleness half may close elsewhere

Grill round 1. This page's *follow-on nobody has answered* — "a URL verified today can rot, and
nothing records when an access method was last confirmed" — listed three options and rejected
per-source dating as too expensive against the ~40-line module cap.

**`PLAN.md` D10 (the fetch-outcome ledger) may dissolve that cost.** A ledger is a dated
observation store living *outside* the module line budget, so dates there are free. If it ships,
this follow-on may close as a side effect rather than needing its own answer.

Not decided — it depends on where the ledger lands, since a per-project ledger cannot carry dates
for a package-shipped module's sources. Tracked as mechanic 1 in
[Q4](Q4-ledger-mechanics.md).

Note also that D8 sharpens the spec's fourth access-method form ("a note that it blocks fetching")
into a **directive** that must name a substitute. That changes the answer to this page's third
"what would need deciding" item: a URL that fails verification is not simply omitted or marked
blocked — it must be replaced with what to use instead.
