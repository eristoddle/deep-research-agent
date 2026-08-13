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
