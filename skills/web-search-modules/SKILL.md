---
name: web-search-modules
description: Reference library of search-strategy modules for the web-search-agent subagent. Not invoked directly — web-search-agent reads ROUTING.md from this directory before running any search, then reads the module files that routing selects. Contains per-domain source lists and query tactics.
---

# Web Search Strategy Modules

This directory is a data bundle, not a workflow. It exists so the `web-search-agent` subagent has a stable place to read its routing table and strategy modules from. Nothing here should be executed.

## Layout

| File | Role |
|------|------|
| `ROUTING.md` | **The router.** Families, defaults, modifiers, per-depth module slots, ambiguity rule. The agent reads this first, every task. |
| `<domain>.md` | A strategy module: where to look in one domain and how to query it. Read only when routing selects it. |

`ROUTING.md` is the single source of truth for which modules exist. The agent's own prompt names no modules — it only knows to read the router — so the module list can grow without touching `agents/web-search-agent.md`.

## Two places modules can live

| Location | Owner | Use for |
|---|---|---|
| `skills/web-search-modules/` (this directory) | The package. **APM overwrites it on every install.** | General modules worth shipping to everyone. Edit here only in the `deep-research-agent` repo itself. |
| `.claude/web-search-modules-local/` | The project. APM never touches it. | Project-specific modules — client work, one-off deep dives, a source list only this project cares about. |

`ROUTING.md` reads the local router first, so a locally-created module needs no change to any packaged file to take effect. That is the point: a module you add to a project survives the next `apm install`, and a package upgrade never clobbers your work.

`/research-add-module` builds either kind — it discovers the sources by searching for them rather than guessing, records how to query each one, registers the module, and verifies it actually beats `general-web` before keeping it.

## Adding a module

Modules are plain reference files, not code. The agent loads at most one to three per task depending on depth, so each one should cover a coherent domain rather than a grab bag.

1. **Write `<domain>.md`.** Follow the shape of the existing files:
   - A routing header: `**Family:**`, `**Use when:**`, `**Do not use for:**`, `**Siblings:**`. The anti-trigger matters as much as the trigger — it is what lets a mis-route correct itself at read time.
   - A prioritized **source list**, noting what each source is actually good for **and how to query it** — a `site:` query, a tested search-URL pattern, a stable index page to fetch directly, or a note that it blocks fetching. A name without an access method makes the agent rediscover the same thing every run.
   - **Query tactics** — the search patterns that work in that domain, not generic advice.

   Keep it under ~40 lines. It enters the agent's context whole on every routed task, so length is a real cost.

2. **Add it to `ROUTING.md`** — a row in an existing family, or a new family row with its own discriminating question. That is the only registration step; nothing else needs editing.

Families should stay few and answerable by a yes/no question about the task. When a family's module list grows past three or four, that is the signal to split the family, not to lengthen the row.

### Modifiers

A module that describes *where else to look* rather than *what the question is about* — a language, a region, a time window — is a **modifier**, and belongs in the modifier table in `ROUTING.md` instead of a family. Modifiers layer on top of a topic module and never replace one. `chinese-tech.md` is the worked example.

## Wanted

Modules that would earn their place, roughly in priority order:

- **AI writing and prompting communities** — where practitioners compare model output: r/LocalLLaMA, r/WritingWithAI, Discord digests, practitioner blogs. Distinct from `general-web.md`, which is aimed at software best practices.
- **Docs and API reference** — reading a product's own documentation as a primary source, as distinct from `vendor-landscape`'s reading of its marketing.

The AI ecosystem & market family (`benchmarks`, `model-releases`, `pricing`, `vendor-landscape`) landed together and covers most technology-product research. Extend that family rather than adding near-duplicates beside it.

Non-technical families (health, law and policy, finance, history) attach the same way: a new family row in `ROUTING.md` with its own question. Nothing in the tech routing needs to change to make room for them.

`chinese-tech.md` is worth keeping. A large share of open-weight model work and evaluation happens on Chinese platforms, and those results are often published there first and sometimes only there. It is a genuine coverage advantage, not dead weight — the mistake to avoid is letting it pull a project's *framing* toward Chinese models when that was not the question.
