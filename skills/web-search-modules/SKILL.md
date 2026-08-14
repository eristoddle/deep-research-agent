---
name: web-search-modules
description: Reference library of search-strategy modules for the web-search-agent subagent. Not invoked directly — web-search-agent reads the relevant module files from this directory before running any search. Contains per-domain source lists and query tactics for GitHub debugging, general web, academic papers, Chinese tech communities, and Stack Overflow.
---

# Web Search Strategy Modules

This directory is a data bundle, not a workflow. It exists so the
`web-search-agent` subagent has a stable place to read its strategy modules from.

`web-search-agent` selects one or more of these before executing any search:

| File | Use for | Sources |
|------|---------|---------|
| `github-debug.md` | Debugging, error messages, GitHub Issues | GitHub Issues (open/closed) |
| `general-web.md` | Best practices, comparative research | Reddit, official docs, blogs, Hacker News, Dev.to, Medium, Discord, X |
| `academic-papers.md` | Paper and literature search | Google Scholar, arXiv, HuggingFace Papers, bioRxiv, ResearchGate, Semantic Scholar, ACM DL, IEEE Xplore |
| `chinese-tech.md` | Chinese-language technical sources | CSDN, Juejin, SegmentFault, Zhihu, Cnblogs, OSChina, V2EX, Tencent/Alibaba Cloud |
| `stackoverflow.md` | Technical Q&A | Stack Overflow, Stack Exchange, technical forums |

Read the module files directly. Nothing here should be executed.

## Adding a module

Modules are plain reference files, not code. The agent reads at most two per task, so each one should cover a coherent domain rather than a grab bag.

To add one:

1. Write `<domain>.md` in this directory. Follow the shape of the existing files: a one-line trigger description, a prioritized **source list** with a note on what each source is good for, and a **query tactics** section with the search patterns that actually work in that domain. Keep it under ~40 lines — it is read into the agent's context on every routed task, so length is a real cost.
2. Add a row to the table in this file.
3. Add a routing line to `agents/web-search-agent.md` under "Scenario-Specific Query Strategies", naming the trigger condition and the file.

Both steps 2 and 3 matter: the agent routes from the list in its own prompt, so a module that exists but is not listed there will never be loaded.

### Wanted

Modules that would earn their place, roughly in priority order:

- **Benchmarks and leaderboards** — where evaluation results actually live: leaderboard sites, Hugging Face spaces and collections, Papers-with-Code-style trackers, model cards, eval harness repos. The existing modules all assume you are debugging or reading papers; none of them know how to find a live results page.
- **Model releases and changelogs** — provider blogs, release notes, model card diffs, pricing pages, deprecation notices. Fast-moving and badly served by general search.
- **AI writing and prompting communities** — where practitioners compare model output: r/LocalLLaMA, r/WritingWithAI, Discord digests, practitioner blogs. Distinct from `general-web.md`, which is aimed at software best practices.
- **Pricing and availability** — API pricing pages, rate limits, regional availability, aggregator comparisons.

`chinese-tech.md` is worth keeping. A large share of open-weight model work and evaluation happens on Chinese platforms, and those results are often published there first and sometimes only there. It is a genuine coverage advantage, not dead weight — the mistake to avoid is letting it pull a project's *framing* toward Chinese models when that was not the question.
