# Verify the `crwl` fetch fallback against a real block

**Tested 2026-08-29 synthetically. Fired for the first time in live runs 2026-09-02: 7 retries, 6 recoveries.**

## Live-fire evidence, 2026-09-02

The standing unknown on this page — *"It has never fired in a live run"* — is now closed. Four `/research-deep` runs for an outside project (a Firecrawl cookbook in the `sm-static` blog repo) exercised the escalation seven times across three of the four runs:

| Source | Failure | `crwl` result |
|---|---|---|
| `ropesgray.com` | 403 | **recovered** — became the highest-yield source in that run |
| `fbm.com` | 403 | **recovered** |
| `ico.org.uk` (×3) | 403 / failed | **recovered, all three** |
| `autoriteitpersoonsgegevens.nl` | failed | **recovered** |
| `news.ycombinator.com` (item 44973222) | 429 | **not recovered** — same rate limit |

Every clause of the carve-out held: already-failed URL, one retry, same fetch slot, bounded output. No agent talked itself out of the exception — the last open behavioural unknown on this page, and it resolved in the rule's favour across three independent agents.

## The refined rule

Combining this with the 2026-08-29 synthetic test:

| Failure mode | Does `crwl` rescue it? |
|---|---|
| 403 / bot user-agent block on a server-rendered page | **Yes** — 6/6 observed |
| 429 rate limit | **No** — the limit applies to it too |
| JS-shell async render | **No** — partial render, and the fragment is misleadingly plausible |

**So the escalation earns its slot, and the 2026-08-29 conclusion should be narrowed rather than kept as written.** "Does not rescue a JS-shell page" was right but read as a general discouragement. The accurate version: it is *reliable* against the most common block — a server-rendered page refusing a bot user-agent — and useless against the two cases where the content is not in the HTML at all, or is rate-gated.

That is a stronger case for keeping it than the original test produced, and it means the "check for a JSON endpoint first" advice below is a complement, not a replacement: the JSON endpoint is the better move for JS-shell sites specifically, which is exactly where `crwl` fails.

## Prior conclusion, 2026-08-29 — superseded above, retained for the reasoning

Two runs, both `exit 0` with empty stderr, so the escalation itself works and needs no change.

| Unknown | Result |
|---|---|
| Does it trigger and run on a genuine block? | **Yes.** Ran clean against `https://forum.obsidian.md/search?q=...`, the standing JS-shell page. |
| Does it recover the content? | **No — partial render only.** Returned 464 bytes: site chrome, and the line `16 results for syncthing conflict android`. Zero thread titles, zero `/t/{slug}/{id}` links. It renders enough JS to produce the result *count* but snapshots before the results themselves load. |
| Does `head -c 40000` hold on a large page? | **Yes.** `platform.claude.com/docs/en/release-notes/overview` returned 116,328 bytes raw, clipped to exactly 40,000. |
| Does the agent talk itself out of its own exception? | **Still open.** Behavioral, not mechanical — cannot be settled by running the command. |

**What this means for the rule.** Keep it: it costs one retry, it is bounded, and it is confirmed not to error. But stop expecting it to be the answer for JS-heavy sites. For an async-rendering app it returns a plausible-looking fragment with the real content missing, which is worse than an obvious failure, because the fragment can be mistaken for a thin page.

**The better first move, when a fetch comes back empty: look for a JSON endpoint beside the HTML page.** Discourse forums expose `search.json?q=`, which returned 16 structured results with `title`, `slug`, `id`, `posts_count`, and dates where both `WebFetch` and `crwl` failed. Cheaper than the retry and strictly better output. This is now recorded in the blog repo's local `obsidian` module.

Original parked notes follow.

---
**Parked** 2026-08-21 — needed a genuine failing page to test against, which could not be manufactured on demand.

**Unblocked 2026-08-29.** A standing, reproducible JS-shell page exists: `https://forum.obsidian.md/search?q=<terms>` renders a placeholder ("this is not the content you are looking for") to any `WebFetch`, every time. `crwl` is installed locally. Both missing preconditions are now met, so this is testable whenever someone wants to run it.

`agents/web-search-agent.md` carries exactly one carve-out from its tool allowlist: a `WebFetch` that fails on a URL may be retried once via `crwl crawl "<url>" -o markdown | head -c 40000`, only if `crwl` is already installed. Every clause is load-bearing — already-failed, one retry, same fetch slot, stdout only, bounded output, no `--deep-crawl`, no `-O`, no install, no second helper.

**It has never fired in a live run.** Both failures in the first live test were a 404 and a page that simply lacked the data — both correctly handled by searching instead, neither one a block. Still true as of 2026-08-29: the Obsidian forum block was hit while building a project-local module, but `crwl` was never reached, because that site's Discourse `search.json` endpoint answered directly and better. That is itself a finding — **check for a JSON endpoint beside the HTML page before escalating**, since it is cheaper and returns structured fields.

What is unverified: that the escalation triggers on a genuine 403 or JS-shell page, that the `head -c 40000` bound actually holds on a large page, and that the agent does not talk itself out of its own exception (the prompt explains why this is not browser automation — headless, one-shot, opens nothing — precisely because an earlier version refused it).

Connects to the retrofit: if a source turns out to block fetching, the spec's fourth access-method form ("a note that it blocks fetching") is the correct thing to write, and such a source is also a ready-made test case for this fallback.
