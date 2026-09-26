# Alternative research agents

This repo is not the only way to do agent-driven research, and it is not the best fit for every job. This page is a map of the other options, so that someone who lands here can pick the right tool even when the right tool is not this one.

Everything listed runs **inside a coding agent** or as something an agent can drive: a skill, an MCP server, a CLI, or a library. Hosted SaaS research products are deliberately excluded, because their output lives in someone else's UI and the whole point of running research from an agent is that the findings land in your own files.

## Pick by shape, not by depth

The instinct is to rank these tools by how deep they go. That turns out to be the wrong axis. Depth is a dial almost all of them have. The two properties that actually decide which one you want are:

**Answer shape.** A run either produces a *narrative document* (chapters, prose, citations), a *matrix* (N subjects by M attributes, which is a comparison table), an *annotated source list* (findings with provenance, synthesis left to you), or a *knowledge base* (a growing corpus rather than a deliverable). A tool built for one shape is awkward at the others. Wanting a book out of a matrix engine feels like death by a thousand cuts; wanting a comparison table out of a report writer means reading 30,000 words to fill in a grid.

**Persistence.** A run is either ephemeral, where the findings exist once and the next run starts cold, or accumulating, where a store is consulted before fetching and each session starts smarter than the last. This matters more than run length. An accumulating tool used for twenty minutes a week beats an ephemeral one used for eight hours once, if the topic is something you will keep returning to.

Two secondary axes worth checking:

- **Source routing** — does it search the open web generically, or does it know where the answers for a given kind of question actually live? Generic width sweeps do badly on topics where vendor marketing and programmatic SEO dominate the first hundred results.
- **Provider lock** — is it tied to one model vendor, or can it run on whatever you have, including local models?

## The landscape

Stars and last-push months verified against the GitHub API on 2026-09-18 (BMAD deep-recon on 2026-09-25).

| Tool | Form | Answer shape | Persistence | Stars | Last push |
|---|---|---|---|---|---|
| [local-deep-research](https://github.com/LearningCircuit/local-deep-research) | MCP + lib + CLI | Narrative report | Encrypted SQLite history + your own docs | 9.1k | 2026-09 |
| [hyperresearch](https://github.com/jordan-gibbs/hyperresearch) | Claude Code skill + MCP + CLI | Narrative, chaptered | Markdown vault + SQLite index | 3.4k | 2026-09 |
| [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | Python lib (+ [MCP](https://github.com/assafelovic/gptr-mcp)) | Narrative report | None | 29.5k | 2026-08 |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | Claude Code skill | Ranked brief | SQLite archive of past briefs | 62.3k | 2026-09 |
| [paper-qa](https://github.com/Future-House/paper-qa) | Python lib + CLI | Cited answer | Reusable index under `~/.pqa/` | 9.2k | 2026-09 |
| [local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) | LangGraph app | Summary + sources | None | 9.4k | 2026-09 |
| [deep-searcher](https://github.com/zilliztech/deep-searcher) | Python lib + CLI | Narrative report | Milvus vector DB | 8.3k | 2025-11 |
| [DeepGit](https://github.com/zamalali/DeepGit) | MCP + CLI + lib | Ranked matrix | LanceDB vector index | 913 | 2026-08 |
| [hoolulu/deep-research](https://github.com/hoolulu/deep-research) | Cross-platform skill | Narrative, chaptered | Folder of dated reports | 580 | 2026-08 |
| [reddit-research-mcp](https://github.com/dialog-tools/reddit-research-mcp) | MCP server | Cited findings | Saved feeds | 245 | 2026-09 |
| [RivalSearchMCP](https://github.com/damionrashford/RivalSearchMCP) | MCP server | Structured JSON | None | 128 | 2026-09 |
| [BMAD deep-recon](https://github.com/bmad-code-org/BMAD-METHOD/tree/main/skills/bmad-deep-recon) | Skill in the BMAD Method | Decision brief; weighted matrix when choosing | Run folder + claims ledger, refreshable | 53.5k\* | 2026-09 |

\* Stars are for the whole BMAD-METHOD repository, of which deep-recon is one skill.

## What each one is uniquely good at

**[local-deep-research](https://github.com/LearningCircuit/local-deep-research)** — the most complete package here. Per-domain engines (arXiv, PubMed, Semantic Scholar, NASA ADS, GitHub, SearXNG, Wayback), an encrypted SQLCipher history of every past run, and a personal document library indexed and searched alongside live results. Runs fully offline on Ollama or llama.cpp if you want it to. Reach for it when the corpus is the asset and you will be returning to the same subject for months.

**[hyperresearch](https://github.com/jordan-gibbs/hyperresearch)** — a 16-step pipeline with three tiers, the largest of which partitions a topic into chapters and loops the pipeline per chapter to produce a very long document. Markdown is the source of truth and SQLite is the cache, so the vault stays portable. Claude-only, with Opus on the synthesis and critique roles, so long runs are not cheap. Reach for it when you want one large chaptered document out the other end.

**[gpt-researcher](https://github.com/assafelovic/gpt-researcher)** — the mature, widely deployed baseline, and the one most likely to already be supported by whatever you are building on. Its MCP surface is the interesting part for agent use: `get_research_context` and `get_research_sources` hand back the raw material separately from the written report, so your agent can do the writing. Note that the MCP wrapper is less actively maintained than the core library, and a paid search API is effectively required to get good results.

**[last30days-skill](https://github.com/mvanhorn/last30days-skill)** — recency-windowed research over social and forum sources (Reddit, X, Hacker News, YouTube transcripts, Bluesky, Polymarket odds), ranked by actual engagement rather than by search position. Answers "what are people saying about this right now", which no report writer does well. The accumulated briefs become a searchable offline archive.

**[paper-qa](https://github.com/Future-House/paper-qa)** — academic literature with citations traceable to page ranges, over your own PDFs plus Semantic Scholar, Crossref and Unpaywall. Reach for it when a claim has to be defensible down to where it came from.

**[local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher)** — the smallest readable implementation of the reflect-then-fill-the-gap loop. More useful as a component to embed in something of your own than as a finished tool.

**[deep-searcher](https://github.com/zilliztech/deep-searcher)** — research over *your* private corpus with the web as the optional supplement, which is the inverse of everything else here. The only entry that has gone quiet, so check its state before committing to it.

**[DeepGit](https://github.com/zamalali/DeepGit)** — GitHub-only tool discovery that returns a scored, reasoned comparison table instead of prose. The right shape for "find me the N projects that do X", which is the question this very page answers.

**[hoolulu/deep-research](https://github.com/hoolulu/deep-research)** — the same chaptered-report shape as hyperresearch, but portable across Claude Code, Codex, Cursor, OpenCode, Windsurf and Cline, and multilingual. The one to choose if you do not want to be tied to a single host agent.

**[reddit-research-mcp](https://github.com/dialog-tools/reddit-research-mcp)** — semantic search across Reddit with every finding citing a real post or comment, upvotes included. Demand signals and pain points in people's own words, which generic web search flattens into blog posts about the topic.

**[RivalSearchMCP](https://github.com/damionrashford/RivalSearchMCP)** — no LLM inside the server. It returns per-URL trust scores and detects conflicts between sources, flagging numeric, date and polarity disagreements with confidence weights. An auditing layer rather than a research tool, and it composes with any of the others.

**[BMAD deep-recon](https://github.com/bmad-code-org/BMAD-METHOD/tree/main/skills/bmad-deep-recon)** — research framed around a *decision* rather than a topic, with the strongest evidence discipline of anything on this page. Every claim carries a publisher, publication date and access date; load-bearing claims are checked against an independent publisher (syndication and the same vendor twice do not count); disagreements are reported with both sides rather than averaged; and each research type sets how old a claim of each kind may be before it is stale, so the report ends with a dated re-check list. It can also skip running the search itself: draft a prompt for a deep-research product you already pay for, then process the report that comes back into the same cited summary. When the decision is "pick one of these", it produces a weighted matrix you can re-weight, plus a named runner-up and the conditions under which it wins. It is the closest neighbor to this repo in answer shape, but built for a handful of finalists rather than dozens of items. It expects the BMAD Method's setup and scripts to be installed, so it is not a drop-in standalone skill. Reach for it when research feeds a concrete choice and you need to defend every number in it.

Also worth knowing about, though it did not make the table: **[STORM](https://github.com/stanford-oval/storm)** (Stanford) is the only project in this space whose output shape is genuinely a wiki article, built by simulating multi-perspective interviews. Last pushed 2025-09, so treat it as a reference design rather than something to depend on.

## Where this repo fits

This one produces a **matrix**. You define items (the subjects) and fields (the attributes), it researches every field for every item with one agent per item, and the report rolls those values up. That makes it a good fit for questions with a shape like "these twelve models, across these fifteen attributes" and a poor fit for "write me a long document about this topic". If you want a narrative, one of the report writers above will serve you better and there is no reason to force this one into that job.

The part that is genuinely different here is the [search-strategy modules](skills/web-search-modules): per-domain routing that decides where to look *before* searching, with an access method per source, an ordering rule for which sources outrank which, and documented workarounds for sources that block agent fetching. Most tools in the table search the open web generically and scale by adding sources. This one tries to search fewer, better places. That approach earns the most on topics where the first page of generic results is vendor marketing.

It is also human-in-the-loop by design. The outline is reviewed and amended before any research runs, which costs you a step and buys you the ability to fix a bad research plan before spending an hour on it.

## Caveats on this page

Star counts and last-push dates were verified. Run times, source counts, benchmark placements and claims like "no API keys required" are taken from each project's own documentation and have not been independently reproduced here. Treat them as claims.

Corrections and additions are welcome. If something in this space fits the brief at the top and is missing, open an issue.
