# Q3 — Is Reddit reachable at all, and from where?

> **Status:** ✅ **ANSWERED — Reddit is reachable.** `skills/research/reddit_feed.py` reads the public Atom feeds. Built and tested 2026-09-03
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

### 2026-09-03 — corrected: not blocked, and never was on this machine

Two errors in the entry above, both mine, both recorded here rather than edited away.

**"Access to the other computer" had it backwards.** The machine where the five routes failed is the *work* computer, which is the one that is hard to get to. This machine — where the plan lives and where the work happens — is the accessible one. There was never a hardware blocker.

**The firecrawl API key is already here.** Checked directly: `FIRECRAWL_API_KEY` is set in the environment (35 characters), the `firecrawl` CLI is installed, and `crwl` is installed. `fetch-anything`'s `SKILL.md:64` names that variable as where the key is read from, and its Reddit handler escalates to firecrawl with `--proxy auto` specifically for IP-based blocks.

**So the re-test is runnable now**, and the five-row table above should be re-run here before any of it is treated as settled — the original run was on the *other* machine, so even the harness-scoped `WebFetch` refusal may read differently. The user has stated the firecrawl test will happen, timing open.

**What flips if firecrawl reaches Reddit** — the revert set, so it does not have to be rediscovered. Every bullet resting on this verdict is tagged `[ACCESS:reddit]` per D12(a); `grep -rl "ACCESS:reddit"` prints the current list. As of this writing that is `skills/web-search-modules/{general-web,competitor-content,vendor-landscape}.md` plus the Reddit section of `skills/web-search-modules/ACCESS.md`. A positive result also reopens D8's deferred venue half (a Reddit *modifier*, never a topic module) and changes what `demand-signals` (D9) can be built on, since that module is currently Reddit-free by construction rather than by preference.

### 2026-09-03 — resolved: tested here, and firecrawl refuses Reddit outright

Run on this machine, second IP, current harness build.

| Route | Result |
|---|---|
| `curl` + browser UA → `.json` | **302** to the login wall (was 403 on the other machine — same family) |
| `crwl` (the carve-out) | **174-byte login page** (was 238 bytes) |
| `firecrawl scrape` — `old.reddit.com` listing | **refused**: *"We apologize for the inconvenience but we do not support this site."* |
| `firecrawl scrape` — `www.reddit.com` listing | same refusal |
| `firecrawl scrape` — `old.reddit.com/r/…/top/` | same refusal |
| `firecrawl scrape` — `news.ycombinator.com` (control) | **succeeded**, 15KB |

**The IP hypothesis is dead.** Two machines, two IPs, the same wall. The rows that were labelled IP-scoped in the original entry are not.

**And firecrawl's failure is a different kind entirely.** It is not a block, a rate limit, or a challenge — it is a vendor policy refusal naming the site, returned identically for every URL shape, while a control scrape on another domain worked fine. **A proxy pool cannot route around a scraper's own decision not to serve a domain.** That was the one mechanism left that could have changed the answer, which is what makes this resolved rather than merely re-tested.

**What this settles elsewhere:** D9's `demand-signals` module is Reddit-free **by necessity, not by choice** — that scoping decision is now confirmed rather than provisional, and it will not need revisiting. [Q6](Q6-firecrawl-rung.md) loses its Reddit motivation entirely, though firecrawl remains capable on other sites. The revert list below stays accurate but is unlikely to ever be used.

### 2026-09-03 — reopened: the feeds were never tested, and one of them works

**The previous entry's "there is no route left to try" was wrong.** Every route tested to that point was a *scraper* aimed at HTML. Reddit's Atom feeds were never tried. One works.

| Route | Result |
|---|---|
| `curl` → `www.reddit.com/r/<sub>/.rss` | **HTTP 200, 73,649 bytes, real current post titles** (feed `<updated>` matched the test date) |
| `curl` → `www.reddit.com/r/<sub>/search.rss?q=…` | **429** — rate limited, *not* refused. Untested with backoff. |
| `curl` → `old.reddit.com/r/<sub>/.rss` | 302. Consistent with the user's report that `old.reddit.com` is degrading generally; stop treating it as the preferred host. |
| `WebFetch` → the working `.rss` URL | *"Claude Code is unable to fetch from www.reddit.com"* — a **harness** refusal, not Reddit's |
| `crwl` → the working `.rss` URL | `'NoneType' object has no attribute 'raw_markdown'` — a **format** failure on XML, not a block. Possibly a flag away. |

**So the wall is not Reddit's.** Reddit serves this content to an ordinary client with no auth. The two tools the agent is allowed to use cannot take it: one is blocked by the harness at the domain level, the other cannot parse XML.

**Why this matters more than "a workaround exists":** the feed returns **listings** — many post titles, cheaply, in one request. D9 states outright that listings are the correct unit for demand signals and that full threads are the wrong one. This is not a degraded substitute for the blocked route; it is closer to what the module actually wants than scraping threads would have been.

**Open, and now the real question:** what mechanism reaches it. A `curl` of a known feed URL is one-shot, stdout, bounded, opens nothing, and needs no auth — the same shape as the existing `crwl` carve-out and arguably narrower, since it is a fixed URL pattern rather than an arbitrary page. Whether that becomes a second carve-out, an extension of the existing one, or something the user builds separately is undecided. See [Q6](Q6-firecrawl-rung.md), which is the same class of question.

**Not yet tested:** `search.rss` with spacing to clear the 429, per-subreddit `.rss` sort variants (`/top/.rss`, `/new/.rss`), and the multi-subreddit form (`/r/a+b+c/.rss`).

**The official OAuth API is NOT a candidate — struck on first-hand evidence.** It was suggested here as "the supported path"; the user has already tried to sign up for it and could not get a token at all. Their words: *"it seemed broken as fuck… I've dealt with issues on websites before and figured out workarounds and all this. I gave up trying to sign up."* That is someone who routes around broken signup flows for a living failing to complete this one. Do not re-propose it without new evidence that the registration flow works — it has already cost one attempt.

**Which promotes the feed from fallback to primary.** The `.rss` route's real advantage is not that it happens to work, it is that **there is nothing to sign up for**: no account, no client ID, no token to expire, revoke, or re-authorize, and no terms tier to fall out of. Every other route considered — firecrawl, the OAuth API — failed at a *vendor gate* rather than at a technical wall. The feed has no gate.

### 2026-09-03 — answered: we wrote the tool

The user's call, and it was the right one: *every* failure had been somebody's permission gate, so the answer was to stop asking permission and write the reader. `skills/research/reddit_feed.py` — stdlib only, no dependencies, no account, no key.

**No new permission was needed.** `web-search-agent`'s allowlist is `WebSearch, WebFetch, Read, Write, Bash`. It already has `Bash`. The `crwl` carve-out was never a permission — it is a *rule* about what may run through a permission the agent already holds. A bounded script is the same shape.

**Verified working:** subreddit listings (`r/SideProject`), merged multi-subreddit feeds (`r/Entrepreneur+smallbusiness+freelance` — one request, several communities), and site-wide search. Output is title + permalink + date + subreddit, text or `--json`.

**Three things the testing caught that a naive version would have shipped broken:**

- **The rate limit is cumulative by IP, not per-request.** A burst of feeds trips a 429 even though each one alone is fine. It clears with patient backoff — the script retries 5 times starting at 5s and doubling. A 429 is a rate limit, never a refusal.
- **`sort=new` on a site-wide search returns near-random posts.** Only `relevance` respects the query, so search defaults to it regardless of the listing default.
- **Reddit's search mixes matching *subreddits* in with matching *posts*.** Unfiltered, a search for "is there a tool that" returned `r/Tools` and `r/todayilearned` — 200 OK, plausible-looking, not results. Only post permalinks carry `/comments/`, which is the filter. **This is D7's silent substitution appearing inside our own tool**, and it would have been invisible without reading the output.

**Still open (small):** whether the module invokes this directly, and the wording of the tool-discipline rule that permits it — the same class of question as [Q6](Q6-firecrawl-rung.md). The access problem is solved; what remains is prompt wording.

### 2026-09-04 — execution policy resolved

The agent may invoke `reddit_feed.py` as an approved package helper. It is reviewed,
versioned, reusable across consumer projects, and performs deterministic listing extraction
more cheaply than asking a model to parse the same feed. This is not permission to generate
arbitrary scripts during research: a one-off helper belongs in its own run folder, while a
project-specific reusable helper earns a project-owned location only once there is a real
repeat use. See `PLAN.md` **D15**.

The remaining implementation detail is to state the reader's exact bounded invocation and
fetch accounting in the agent prompt. That is a build task, not an unresolved access question.

## Blocked on

- Nothing. Answered.

## Related

- `PLAN.md` **D7** (no silent substitution) — the requirement that holds regardless of the answer here
- `PLAN.md` **D8** (access methods in one shared file) — where the answer gets written down
- [P — search-layer refusals](../parking-lot/search-layer-refusals.md) — the run evidence that raised it
