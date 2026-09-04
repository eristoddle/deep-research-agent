# Q3 — Is Reddit reachable at all, and from where?

> **Status:** open
> **Opened:** 2026-09-03 · **Last touched:** 2026-09-03

## The question

Every route inside `web-search-agent`'s current tool discipline failed against Reddit when
tested from one machine on 2026-09-03. **Firecrawl was never tested**, and it is the one rung
with a proxy pool — precisely the mechanism that would defeat an IP-based block. Until it is
tested, "Reddit is unreachable" is not a fact, it is a result scoped to one environment.

What depends on it: whether a Reddit venue module or modifier is ever worth writing (Q2's
deferred half), and whether `web-search-agent` needs a second tool-discipline carve-out (D8's
deferred half).

## Thread

> Append-only. Each grill round adds a dated section below the existing ones.

### 2026-09-03 — opened

Grill round 1. Five routes tested from **one machine, one IP, one harness build**, all failing:

| Route | Result |
|---|---|
| `WebSearch "site:reddit.com …"` | zero reddit URLs; ten results from Etsy community / SBA / slideshare |
| `WebFetch www.reddit.com/…/search.json` | `Claude Code is unable to fetch from www.reddit.com` — harness-level refusal |
| `WebFetch old.reddit.com/…` | same harness-level refusal |
| `curl` + browser User-Agent → `.json` | `403` |
| `crwl crawl old.reddit.com/…` (the carve-out) | login wall, 238 bytes |

**Not tested: firecrawl.** `fetch-anything`'s Reddit handler escalates to it with `--proxy auto`
for exactly this failure mode, and its own note says Reddit rate-limits by IP, so this rung is
"more likely to pay off here than on a typical site."

Two of these five results are environment-scoped in different ways, and the distinction matters
for a re-test:

- **IP-scoped** — the `curl` 403 and the `crwl` login wall. A different IP, a VPN, or a proxy
  pool may not see them at all.
- **Harness-scoped** — the `WebFetch` refusal names Claude Code itself, not Reddit. A different
  host (Copilot, per D6) may not carry the same block, and it may change between builds.
- The `WebSearch` substitution is the one that looks environment-independent, but it has been
  observed on exactly two days by one user.

**The user's correction, and why it stands:** absolute statements about reachability are not
earned by this evidence. The plan is destined to be executed on a different computer, where at
minimum the IP-scoped rows may come back differently.

**So the deliverable here is a procedure, not a conclusion.** Re-run all five rows above on the
target machine, plus firecrawl, before treating any Reddit source as unreachable there. That
procedure is the thing worth carrying; the table above is one machine's answer to it.

## Blocked on

- Access to the other computer, and a firecrawl API key on it.

## Related

- `PLAN.md` **D7** (no silent substitution) — the requirement that holds regardless of the answer here
- `PLAN.md` **D8** (access methods in one shared file) — where the answer gets written down
- [P — search-layer refusals](../parking-lot/search-layer-refusals.md) — the run evidence that raised it
