# Stack Overflow — stackoverflow.com

**Used by:** stackoverflow
**Reachable:** yes — the Stack Exchange API only, through the fetch-escalation ladder · 2026-09-04

## Query
- **`site:stackoverflow.com <terms>` fails silently.** It returns zero `stackoverflow.com` URLs and fills the page with sites that republish SO answers — `bobbyhadz.com`, `techoverflow.net`, `itsourcecode.com`, Medium mirrors. No error, just plausible wrong sources. Do not use it.
- **`WebFetch` is refused at the domain level** on both `stackoverflow.com` and `api.stackexchange.com`, so a question page cannot be read directly.
- **The API is the route, reached through the escalation ladder** — `WebFetch` fails, then `crwl` returns the JSON verbatim. Keyless, no registration; quota is 300 requests/day per IP.
  - Find questions: `https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=votes&q=<terms>&site=stackoverflow&pagesize=5`
  - Read answers: `https://api.stackexchange.com/2.3/questions/<question_id>/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody&pagesize=3`
  - Narrow by tag with `&tagged=python;python-asyncio`, or search one Stack Exchange site by changing `&site=` (`serverfault`, `superuser`, `dba`).

## Worth knowing
- **One search call ranks the field without fetching anything.** Each item carries `score`, `accepted_answer_id`, `answer_count`, `creation_date`, `last_activity_date`, `tags`, and `link` — enough to pick the right question before spending a second call on its answers.
- **`filter=withbody` returns the answer text itself** (HTML), so the accepted answer arrives without ever loading a page. Verified 2026-09-04: a 1,195-character accepted answer came back in one call.
- **`score` is lifetime, `last_activity_date` is not.** A 400-score accepted answer from 2014 outranks everything and may document an API that no longer exists. Compare the two dates before trusting a high score, and say which version an answer applies to.
- **The answer is often not the accepted one.** `sort=votes` surfaces the later, higher-scoring answer that the accepted one predates; fetch two or three, not just `accepted_answer_id`.
- Never cite the content farms above, even when one is correct. The real SO URL is in the API response's `link` field — cite that.
