---
name: research-add-module
user-invocable: true
allowed-tools: Read, Write, Glob, Bash, WebSearch, WebFetch, AskUserQuestion
description: Build a new web-search strategy module for a domain the existing modules do not cover. Discovers where that domain's answers actually live by searching for them, records how to query each source, and registers the module locally so it survives reinstalls.
---

# Research Add Module - Build a Search Module

## Trigger
`/research-add-module <domain or research question>`

## Why this exists

Every named-source module started as a general web search. `general-web` is the jumping-off point: you search normally, notice the same four sites keep holding the real answers, and from then on you go straight to them. This skill does that deliberately instead of by accident — and writes down *how* to query each source, not just its name.

A module built without that discovery pass is a guess about where answers live. Guessed source lists route the agent to plausible-sounding sites that turn out to be empty.

## Workflow

### Step 1: Check that it is warranted

Read `web-search-modules/ROUTING.md` (and the local router, if one exists — see Step 2). If an existing module already covers this domain, say so and stop. Module sprawl is the failure mode here: every module competes for the same one-to-three slots per task, so a near-duplicate makes routing *worse*, not better.

Proceed only if you can name a question the current modules would route to `general-web` and answer badly.

### Step 2: Choose the destination

Use AskUserQuestion:

- **Project-local** *(default)* — `.claude/web-search-modules-local/` in the current project. For client work, one-off deep dives, or anything whose source list is specific to this project. Read automatically by the router, and **not** owned by APM, so it survives `apm install`.
- **The package** — `skills/web-search-modules/` in the `deep-research-agent` repo itself. Only when you are working in that repo and the module is general enough to ship to everyone.

**Never write a module into an APM-installed `.claude/skills/web-search-modules/`.** That directory is package-owned; the next `apm install` overwrites it and the module is gone.

### Step 3: Discovery pass

Budget: **6 searches, 8 fetches.** Report usage as you go.

1. Draft 5-8 representative questions this module must be able to answer. Show them to the user and confirm before searching — wrong questions produce a wrong source list.
2. Run them as ordinary `WebSearch` queries. This is deliberately the `general-web` behavior; you are watching what it surfaces.
3. Tally the domains that keep producing *useful* results, not merely frequent ones. A site that appears in every result set while only restating a primary source is noise.
4. Drop aggregators and SEO farms that repackage a source you already have. Keep the source they repackage.

Target **4-8 sources**. Fewer is not a coherent module; more is an unroutable grab bag.

### Step 4: Work out how to query each source

For each surviving source, determine and record the access method — this is what makes the module worth more than a list of names:

- **`site:` query** — `site:example.com <terms>` returns useful results. The default; note it and move on.
- **The site's own search** — many sites have a search URL that `WebFetch` can hit directly and that returns better results than a `site:` query. Find the exact pattern by searching the site once and reading the resulting URL, then **fetch it once to confirm it works**. Record it verbatim, e.g. `https://example.com/search?q={terms}`.
- **A stable index page** — a changelog, a leaderboard, a pricing page, a model list. Record the URL directly; these are worth fetching without searching at all.
- **Blocked** — `WebFetch` gets a 403 or an empty body. Note it, and note whether `crwl` gets through (see the agent's fetch-fallback rule). A source that cannot be read is still worth listing *with that warning* so the next run does not rediscover it.

Record only patterns you actually tested. An untested URL pattern in a module is worse than no pattern, because it will be trusted.

### Step 5: Write the module

`<domain>.md` in the chosen directory, under ~40 lines, following the shape in `web-search-modules/SKILL.md`:

- Routing header: `**Family:**`, `**Use when:**`, `**Do not use for:**`, `**Siblings:**`. Write the anti-trigger honestly — it is what lets a mis-route correct itself.
- **Sources**, in priority order, each with what it is good for **and its access method from Step 4**.
- **Query tactics** — what you learned in Step 3 about phrasing that works in this domain. Not generic search advice; only what is specific to these sources.

### Step 6: Register it

Add a row to the router for the chosen destination.

For a project-local module, that is `.claude/web-search-modules-local/ROUTING.md`. If it does not exist, create it with this shape:

```markdown
# Local Modules

Project-specific search modules. The packaged router reads this file if it exists; entries here take precedence over packaged modules of the same name.

| Family | Ask yourself | Modules |
|---|---|---|
| <family> | <yes/no question about the task> | `<module>` |
```

Attach to an existing family where one fits; create a new family row only when the discriminating question is genuinely different.

### Step 7: Verify it beats general-web

Re-run two of the Step 3 questions, this time following the new module. Compare against what plain search returned in Step 3, and report the comparison honestly.

If the module did not do better, say so and offer to discard it. A module that does not beat `general-web` is negative value: it consumes a routing slot and adds context on every task it matches.

## Notes

Modules do not update themselves. When a source dies or a better one appears, re-run this skill on the same domain, or edit the file by hand — both are normal. Deliberate hand-editing is the intended maintenance path, not an escape hatch from one.
