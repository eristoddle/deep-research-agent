# Stack Overflow Module

> 从 web-search-agent.md 提取的技术问答专用策略

**Family:** Software & debugging
**Use when:** The question is how to use a language, API, or tool correctly — implementation, syntax, idiom — and nothing is necessarily broken.
**Do not use for:** A confirmed bug in a specific project (`github-debug`), or architecture and tool-selection questions (`general-web`).
**Siblings:** `github-debug` — pair them when a usage question may turn out to be a bug.

## 搜索源
- **Stack Overflow, through the Stack Exchange API.** `site:stackoverflow.com` returns zero SO URLs and a page of answer-scraping farms instead, and `WebFetch` is refused on both `stackoverflow.com` and `api.stackexchange.com` — so reach the API through the escalation ladder (`WebFetch` fails, then `crwl`). Keyless, 300 requests/day. Search: `https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=votes&q=<terms>&site=stackoverflow&pagesize=5`. Then read answers for one `question_id`: `.../2.3/questions/<id>/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody&pagesize=3`. See `sites/stackoverflow.md`.
- **Other Stack Exchange sites** — same API, change `&site=`: `serverfault` (ops and deployment), `superuser` (desktop and shell), `dba` (databases), `unix`, `security`. Pick by whose practitioners own the question; `stackoverflow` is the wrong site for an nginx or systemd question.
- **The language or library's own docs**, fetched directly by URL, whenever the API's top answers disagree or all predate the current major version. An idiom question with a stale accepted answer is a docs question.
- **Technical forums and discussion boards** — Discourse forums expose JSON beside the HTML (`<thread-url>.json`), which is usually the cheapest route once a relevant forum surfaces in general results. Query `site:<forum domain> <terms>`.

## 查询策略
- **Two calls, not a page fetch.** One `search/advanced` call ranks the whole field — it returns `score`, `accepted_answer_id`, `answer_count`, `creation_date`, `last_activity_date`, and `tags` per question. Pick the right question from that, then spend one `/answers` call with `filter=withbody` to get the text. Fetching question pages is both blocked and unnecessary.
- **Search the error string, not a description of it.** Paste the literal exception line minus the parts unique to the caller — file paths, line numbers, memory addresses, variable names. Those are what make a query return nothing.
- **Filter by tag, not by adding words.** `&tagged=python;python-asyncio` narrows far more precisely than appending "python" to `q`, because tags are curated and prose is not. Semicolons are AND.
- **Score is lifetime; recency is a separate axis.** A 400-score accepted answer from 2014 outranks everything and may document a removed API. Compare `creation_date` against `last_activity_date`, and state which version an answer applies to rather than presenting it as current.
- **Read past the accepted answer.** Acceptance is the asker's one-time judgment, often years stale; `sort=votes` surfaces the later answer that reflects the current idiom. Fetch two or three and say when they disagree.
- **A closed or duplicate question is still a signal.** "Closed as opinion-based" usually means the real answer is a tradeoff, not a fact — report it as one instead of picking a side. A duplicate's target is the canonical thread; follow `link` there.
- **Never cite an answer farm.** `bobbyhadz.com`, `techoverflow.net`, `itsourcecode.com`, and Medium mirrors republish SO answers and rank above the original. If one is the only thing a general search returned, find the source question through the API and cite that instead.
