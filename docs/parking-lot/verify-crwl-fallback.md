# Verify the `crwl` fetch fallback against a real block

**Parked** 2026-08-21 — needed a genuine failing page to test against, which could not be manufactured on demand.

**Unblocked 2026-08-29.** A standing, reproducible JS-shell page exists: `https://forum.obsidian.md/search?q=<terms>` renders a placeholder ("this is not the content you are looking for") to any `WebFetch`, every time. `crwl` is installed locally. Both missing preconditions are now met, so this is testable whenever someone wants to run it.

`agents/web-search-agent.md` carries exactly one carve-out from its tool allowlist: a `WebFetch` that fails on a URL may be retried once via `crwl crawl "<url>" -o markdown | head -c 40000`, only if `crwl` is already installed. Every clause is load-bearing — already-failed, one retry, same fetch slot, stdout only, bounded output, no `--deep-crawl`, no `-O`, no install, no second helper.

**It has never fired in a live run.** Both failures in the first live test were a 404 and a page that simply lacked the data — both correctly handled by searching instead, neither one a block. Still true as of 2026-08-29: the Obsidian forum block was hit while building a project-local module, but `crwl` was never reached, because that site's Discourse `search.json` endpoint answered directly and better. That is itself a finding — **check for a JSON endpoint beside the HTML page before escalating**, since it is cheaper and returns structured fields.

What is unverified: that the escalation triggers on a genuine 403 or JS-shell page, that the `head -c 40000` bound actually holds on a large page, and that the agent does not talk itself out of its own exception (the prompt explains why this is not browser automation — headless, one-shot, opens nothing — precisely because an earlier version refused it).

Connects to the retrofit: if a source turns out to block fetching, the spec's fourth access-method form ("a note that it blocks fetching") is the correct thing to write, and such a source is also a ready-made test case for this fallback.
