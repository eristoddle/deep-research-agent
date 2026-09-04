# Q5 — Should sites be their own structure, referenced by topic modules?

> **Status:** ✅ Resolved by `PLAN.md` D14. Reopen only if a real run shows that the module's inline access method is insufficient.
> **Opened:** 2026-09-03 · **Last touched:** 2026-09-03

## The question

Modules are organized by **topic** — `pricing`, `benchmarks`, `general-web`. But the same **sites** show up across many of them, and each site has its own querying quirks that are currently rediscovered on every run. The proposal is not topic-*versus*-site: topic modules stay. The question is whether the **sites named inside them** should become their own referenced structure — one file per site — that topic modules point at.

The worked example is Stack Overflow. `stackoverflow.md` is already parked for a rewrite whose whole content is *how to query that one site* — the closed/duplicate signal, score-vs-recency on old accepted answers, `[tag]` syntax, when the answer is in a comment. That is site knowledge sitting inside a topic module, and nothing else can reach it.

## Thread

> Append-only. Each grill round adds a dated section below the existing ones.

### 2026-09-03 — opened

Raised while answering the rollback question in D12, after seeing the same Reddit sentence written into four files. The user had discussed topic-vs-site framing in an earlier session elsewhere and did not recall where it landed.

**The case for it:** a site's querying method is stable and reusable, while a topic module's membership is not. Reddit appears in three modules, Stack Overflow in one that is mostly about it, and the SEO skip-list in `agent-tooling` is site knowledge too. Written once per site, every topic module that names it gets the method for free — and the rediscovery cost the access-method retrofit exists to eliminate goes away for the *method*, not just the URL.

**`ACCESS.md` is the first instance of this shape, accidentally.** It is keyed by venue (Reddit, JS-shell pages), not by topic, and three modules already cite it. So the structure being proposed here partly exists; the open part is whether it grows into a per-site set or stays one small maintenance file. D12(b) deliberately fixed it as a maintenance index for now, which is a decision that would be revisited, not contradicted, if this question resolves toward per-site files.

**The user's own hesitation, recorded as stated:** "maybe that's just too much, maybe that's a lot of files, I don't know, I'll think about that." That is the real tension — every file in this payload enters an agent's context when loaded, and the module cap exists because length is a live cost. A per-site set only pays off if a topic module can reference a site file *without* loading all of them.

**Not answerable yet** because it depends on something unmeasured: how many sites actually recur across modules. If it is five, this is a small reference set. If it is forty, it is a directory nobody maintains and the module set rots around it. Counting the distinct named sites across all eleven modules is the cheap next step, and it is a fact-finding job, not a decision.

### 2026-09-03 — counted, and it splits the question in two

The blocker below was a number, so it was measured rather than asked.

**75 distinct domains are named across the eleven modules. Only 6 appear in more than one module, and none appears in more than three:** `platform.claude.com` (3), `github.com` (3), `openrouter.ai`, `developers.openai.com`, `artificialanalysis.ai`, `ai.google.dev` (2 each). Reddit is a 3.

That result separates two motivations that were being treated as one:

- **Sharing a site across modules** — the weak half. Six domains is not a directory, it is a footnote, and building a per-site reference layer to serve six entries would cost more than it saves. Reddit only *felt* like a strong case because its verdict is long and got restated three times; the tag from D12 already solves that at a fraction of the cost.
- **Giving one site more room than a module can spare** — the strong half, and it is a different problem. `stackoverflow.md` needs the closed/duplicate signal, score-vs-recency, `[tag]` syntax, and comment-vs-answer. That is not knowledge shared with other modules; it is knowledge that does not fit in a module that also has to cover the rest of Stack Exchange, under a ~40-line cap that exists because modules load whole into context.

**So the useful version of this question is probably not "should sites be a structure" but "what happens when one site's method outgrows its module's line budget."** A site file would then be an *overflow* mechanism loaded on demand for that one site, not a parallel taxonomy — which is a much smaller thing to build and does not touch routing at all.

Still open, still the user's call; the counting just moved where the weight sits.

### 2026-09-03 — recounted, then promoted to D14

**The count above was wrong, and wrong in the direction that mattered.** It matched *domain strings* (`reddit.com`), but modules name sites in prose — `**Reddit**`, `Hacker News`, `Stack Overflow`. Counting by name instead of by domain gives **9 sites in more than one module**, not 6:

| Site | Modules |
|---|---|
| GitHub | 6 |
| Stack Overflow / Stack Exchange | 3 |
| Reddit | 3 |
| Hugging Face | 3 |
| OpenRouter · Hacker News · `dev.to` · Artificial Analysis · Twitter/X | 2 each |

GitHub at 6 is what turned the question. The method that actually works on it — the raw `CHANGELOG.md` URL, checking the last commit date before trusting a repo — is written in `agent-tooling.md` and in no other module, while five others name GitHub with no method at all. That is not a hypothetical duplication cost; it is five modules currently shipping a worse answer than one of their siblings already has.

**The user's rule, which is what made this decidable:** a site earns a file when a *second* module names it. Recurrence is the threshold, so nothing is written speculatively and the set only grows when the payload itself demonstrates the need — D2's logic one level down.

**The user also collapsed the tagging question into this one.** A module has to reference its site file anyway, and *that reference is the tag*: `grep -rl "sites/reddit.md"` produces the same revert list a `[ACCESS:reddit]` marker would, with no second syntax to keep in sync. The markers added earlier the same session were removed.

**→ promoted to D14.** What stays open is narrow: whether a site file is ever loaded at runtime. D14 says no for now — the module bullet keeps its own self-sufficient access method, so nothing needs loading — and that gets revisited only if a real run shows the inline bullet was not enough.

## Blocked on

- Nothing. D14 established the recurrence and overflow triggers; runtime loading remains explicitly deferred until a real run proves the inline method insufficient.

## Related

- `PLAN.md` **D12** — tagging provisional findings; `ACCESS.md` as a maintenance index, the decision this would revisit
- `PLAN.md` **D8** — access methods in one shared file, the architecture this extends
- [P — rewrite `stackoverflow.md`](../parking-lot/stackoverflow-rewrite.md) — the worked example: a topic module that is really site knowledge
