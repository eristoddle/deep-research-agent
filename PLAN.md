# PLAN.md

> Authoritative record of **decisions made** for deep-research-agent. Living document, built up across sessions. Read at the start of any planning/design conversation. **Append** decisions as they're made; don't rewrite.
>
> This is the **hot layer** — keep it lean. Cooled material lives in `docs/` (see below). When it grows heavy (default >15000 words), invoke the **`living-plan`** skill. That same skill's `grill` workflow is what **fills** the sections below — decisions don't have to trickle in one at a time from whatever a session happened to touch.

## Overview

An APM-installable bundle of prompts and data: the `/research*` skills, the `web-search-agent` subagent they launch by name, and the strategy modules that agent routes into. Forked from [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) (MIT, Lan Zheng) and rebuilt where it was broken — no search budget, no stop condition, a hardcoded path that broke its own validation step.

There is no build and no test suite. **Editing a file here is editing a prompt** — wording, ordering, and emphasis are the implementation, and a rewrite that reads better but drops a hard constraint is a regression. Full architecture and the failure modes worth knowing live in `CLAUDE.md`; this file records only what was *decided* and why.

## Decisions

> Whole and inline while hot. Mark load-bearing ones `🔒 foundational` so rebalancing never archives them. Cooled decisions collapse to a one-line pointer into `docs/decisions/`.

<!-- D1 — Access methods: three kinds of module -->
### D1 — Three kinds of module, three meanings of "access method" 🔒 foundational

`skills/web-search-modules/SKILL.md:36` requires every source to carry an access method — "a `site:` query, a tested search-URL pattern, a stable index page to fetch directly, or a note that it blocks fetching" — because "a name without an access method makes the agent rediscover the same thing every run." As of 2026-08-21 **`site:` appears zero times across all ten modules**; the spec and the payload disagree completely.

The requirement does not mean the same thing for every module, and treating it as uniform is what would break the retrofit:

| Kind | Modules | What "compliant" means |
|---|---|---|
| **Fixed-site** | `github-debug`, `stackoverflow`, `academic-papers`, `chinese-tech` | The source *is* a website. A literal `site:` query. Stable indefinitely; never needs accumulating. |
| **Parameterized** | `pricing`, `benchmarks`, `model-releases`, `vendor-landscape` | "The vendor's own pricing page" — which site depends on the vendor the question names. Compliance is a **URL pattern plus a seed list** of vendors that actually recur, not a fixed URL. |
| **Open-query** | `general-web`, `competitor-content` | Sources are whatever the query returned. The correct access method is an explicit **"none by design"** note — the spec's fourth form. |

**Why this is foundational:** without it a retrofit pass invents plausible URLs for the open-query modules and damages the thing they do well. `competitor-content` samples an unrefined reader-query search on purpose; pinning it to a source list would defeat it. A guessed URL is *worse* than no URL, because the agent trusts it and spends a fetch on a 404 instead of falling back to search.

**Corollary — the line budget binds.** Modules are 12–31 lines against SKILL.md's ~40-line ceiling, which exists because the file enters the agent's context whole on every routed task. Access methods must be **appended to existing source bullets**, not added as new lines. `academic-papers.md` (31 lines, 7 sources) has almost no headroom.

<!-- D2 — No speculative modules -->
### D2 — No new modules until a real project needs one

Decided 2026-08-21. The wanted modules in `ROADMAP.md` (AI writing/prompting communities, docs-and-API-reference) stay parked until a live project hits the gap.

**Why:** `/research-add-module` exists because it *discovers and tests* which sources actually hold a domain's answers rather than guessing. A module written speculatively — before a real question has been asked of it — is a hand-written source list by another name, which `CLAUDE.md:110` already names as the failure mode: "guessed sources route the agent to plausible sites that turn out to be empty." Waiting for real demand is what makes the discovery step meaningful.

This also means the module count is not a health metric. Ten well-accessed modules beat fifteen with empty source lists.

<!-- D3 — One research root per project -->
### D3 — One research root per project, discovered structurally 🔒 foundational

Decided 2026-08-22. Every run folder lives inside a single root, default `research/`, instead of scattering `{topic_slug}/` directories across the project root.

**Why:** the pipeline is used inside repos where the user is also writing code. The live consumer `writing-model-research` has `llm-writing-benchmark-landscape/` sitting next to `benchmarks/`, `harness/`, `docs/`, and `client-voice-finetuning/`, and nothing about the name says which of those is pipeline output. One root also gives the branch record (D4) somewhere to live.

The root name is a per-project choice, asked once at the first `/research` and **never written to a config file**. Discovery is structural instead: a *run folder* is any directory containing `outline.yaml`; skills glob `*/outline.yaml` **and** `*/*/outline.yaml`, and the root is simply the parent of a run folder when that parent is not the cwd. That is what keeps a renamed root and every pre-existing root-level run working with no migration, and it is why there is no `.researchrc`.

Two consequences that would otherwise break quietly:

- **`output_dir` is relative to the run folder**, not to the cwd. This was always ambiguous — `./results` read one way at the old depth and a different way once nested — so every skill now states it outright.
- **Multiple runs is the normal case, not an edge case.** `Find */outline.yaml in current working directory` assumed exactly one. Every locate step must disambiguate, which is why `/research-deep` needs `AskUserQuestion` in an allowlist that did not have it.

Migration of existing root-level runs is **offered, never automatic** — `/research` lists exactly what it would move and waits for confirmation. Moving directories in someone's repo is not a side effect of asking for research.

<!-- D4 — INDEX.md is the branch record -->
### D4 — `research/INDEX.md` is the branch record, not a directory listing

Research doesn't run once. One search indicates the next direction, which indicates the next, and the shape of that tree is currently recorded nowhere — it lives in the user's memory between sessions.

`INDEX.md` at the root records it: a `## Map` of nested bullets showing which run spawned which, then one `##` section per run carrying its purpose, status, the report's summary paragraphs and headline table, and a `**Leads**` checklist of the directions that run surfaced. A lead nobody has started is a leaf in the Map with no section of its own; when it becomes a run, its parent's checkbox is ticked and points at the new folder.

Three skills own different parts and none rewrites another's: `/research` appends the stub (purpose, date, status `outline`, parent link), `/research-deep` flips status, `/research-report` fills the summary body and asks the user which leads came out of it.

The summary body is **capped** — ≤3 paragraphs, ≤12 table rows, then a pointer into `report.md`. The index is read whole by every skill that touches it, and a 24-item table per entry (the size the live consumer's report actually is) makes the file unreadable within three runs.

<!-- D5 — Layout lives in exactly one payload file -->
### D5 — Layout and discovery live in exactly one payload file

`skills/research/LAYOUT.md`, read by every skill at its locate step — the same architecture as `ROUTING.md` being the single source of truth for module selection.

**Why not inline it in each skill:** five skills need identical discovery rules and three need identical index-writing rules. `CLAUDE.md` already records what duplication costs in this repo — the depth/budget table lives in two files and changing the numbers means changing both, which is documented as a thing that breaks quietly rather than as a design.

**Why not `CLAUDE.md`:** skills do not read it and APM does not install it. A contract the payload has to honor has to live in the payload.

<!-- D6 — Runtime-specific agent wrappers, runtime-neutral resources -->
### D6 — Keep one research prompt, add runtime-native agent entry points 🔒 foundational

Decided 2026-08-25 after mining Copilot session `56cc0499-1dd1-4148-9027-059a235aac6b` from `tpo-copilot-desktop-research`. APM 0.16 deployed the same `web-search-agent` definition into both `.claude/agents/` and `.github/agents/`; Copilot registered the duplicate name, then launched the agent with zero tools because APM passes the Claude allowlist (`WebSearch, WebFetch, Read, Write, Bash`) verbatim while Copilot expects capability categories (`read, search, web, edit, execute`). A uniquely named Copilot-native wrapper using those categories completed all three research items.

The existing `web-search-agent` name and prompt remain the Claude-compatible canonical implementation so current consumers do not break. Copilot gets the proven `Web Research Writer` wrapper, which loads and follows that canonical prompt but owns Copilot-native frontmatter. Orchestration skills select the entry point by exact registered name and host. Resource lookup is runtime-neutral: current shared `.agents/skills/` first, legacy `.claude/skills/` retained as fallback. Install docs require an explicit APM target so filesystem auto-detection cannot silently activate both harnesses.

**Why not one universal agent file:** APM's current authoring contract deploys `model` and `tools` verbatim to both Copilot and Claude. Their tool names are not portable, and removing the allowlist would restore the failure that opened roughly 100 browser tabs. Two thin entry points preserve the boundary without duplicating the research method.

<!-- D7 — No silent substitution -->
### D7 — No silent substitution 🔒 foundational

Decided 2026-09-03. **When a named source cannot be reached, the run says so. It never proceeds silently on whatever the tool returned instead.**

**Why:** a `site:reddit.com` search returned ten clean, plausible results from *other domains* (Etsy community, SBA, slideshare) and **no error at all**. That is not a refusal, it is a substitution — and a run that names Reddit as its primary source while reporting success on Etsy forums is worse than a run that fails, because the failure is invisible to whoever reads the report. It retroactively explains `vocabulary-ladder-price-monitoring` "falling back to eBay/Amazon/Shopify community forums": that was very likely not the agent's judgment, it is what the search tool handed it.

Three places it binds:

- **A search that returns zero results from a named domain is a finding**, not an empty set. Report it.
- **`results/*.json` and the report must distinguish "no answer exists" from "the source was unreachable."** The `uncertain[]` array is already the mechanism; this is what it is for.
- **A module that names a source it cannot reach is a bug in the module** — which is what D8 fixes.

This is about *behavior*, not about Reddit. It holds for any source, and it holds regardless of how [Q3](docs/questions/Q3-reddit-reachability.md) resolves.

**Mechanism superseded by D11** — `uncertain[]` is the wrong channel, and had no implementation in any case. Everything above stands.

<!-- D8 — Access methods in one shared file; the fourth form is a directive -->
### D8 — Access methods live in one shared file, and the fourth form is a directive 🔨

Decided 2026-09-03. Two parts, both about the **access** layer and neither about routing.

**(a) One shared file.** Reddit is named as a source in `general-web`, `competitor-content`, and `vendor-landscape` with zero access methods between them. Whatever gets learned about reaching a venue lands in **one** file that modules cite by name — the same architecture as `ROUTING.md` for routing and `LAYOUT.md` for layout. Deliberately *not* a new router entry: how to reach a source is not a routing question, and the router has exactly three kinds of entry today.

**(b) The spec's fourth form becomes a directive.** `SKILL.md` allows "a note that it blocks fetching." That is passive — it tells the agent to give up, which under D7 beats substituting but still ends the line of inquiry. Sharpen it to name **the block and the substitute**: "unreachable from this toolchain — use niche forums and PAA for the same signal." **No fifth kind.** The parked doc proposed one for API/JSON-replaced sources; Reddit is not API-replaced, so that was never the gap.

**Deferred — the venue half.** If a Reddit venue layer is ever built it is a **modifier** (the `chinese-tech` precedent: an axis layered on a topic module, never consuming a topic slot), not a topic module, which would compete with `pricing`/`general-web` and lose. It is worth little while [Q3](docs/questions/Q3-reddit-reachability.md) is open.

**Amended 2026-09-04 by Q3/D15.** Reddit's public Atom feeds are reachable through the approved package helper, so Reddit is no longer an example of the fourth access-method form. That form still applies when a source is genuinely unreachable; its directive remains valid. A future implementation task must replace the stale Reddit substitute directives with its bounded feed-reader method. The venue conclusion is unchanged: a Reddit-specific layer, if it earns one, is a modifier rather than a topic module.

<!-- D9 — demand-signals module -->
### D9 — `demand-signals`: build the research stage, without Reddit 🔨

Decided 2026-09-03. **D2's trigger is met** and the module is approved in shape. Not queued this session.

**Scope** is Day 1–3 of the source article (`10.05 Web Clips/I Gave AI 30 Days…`): *find a problem people repeatedly describe, in their own words, across unrelated places.* Not the product, funnel, or content stages — this repo does the research stage.

**Reddit-free by construction** — and as of Q3's resolution the same day, by *necessity* rather than by choice, so this scoping will not need revisiting: niche forums (Discourse/XenForo expose JSON — confirmed on the Obsidian forum), People-Also-Ask, search suggestions, review sites, Amazon Q&A. The article's own requirement is *the same problem appearing in different places* — that is breadth, so no single venue is load-bearing, and building around the blocked one is a scoping choice rather than a compromise.

**Amended 2026-09-04 by Q3/D15.** Reddit listings are now an available source through `reddit_feed.py`, not a forbidden or mandatory dependency. The breadth rule stands: it may contribute one listing-level signal alongside unrelated venues, never consume the module's research budget or define the module around one platform.

**Why D2 is satisfied rather than waived:** explicit demand, plus two prior runs of exactly this shape (`obstacle-corpus-inverted`, `vocabulary-ladder-price-monitoring`) that came back under-sampled, plus `/research-add-module`'s discovery step having effectively already run — its finding is that the marquee source is a wall. A module written now is *tested*, not guessed, which is the whole point of D2.

**Family is undecided.** It may extend Published-content landscape — `competitor-content` is its mirror image (what has been *published* vs. what is being *asked*) — or open its own row. Per `wanted-modules`, test the discriminating question before assuming the family.

**Resolved 2026-09-04.** `demand-signals` opens its own family: *Is the question which problems, desires, or frustrations recur in people's own words across independent venues?* This is distinct from Published-content landscape's question — *what has already been written about the topic, and what do those pages cover?* — so combining them would make routing less accurate. Reddit listings may be one source when the package reader is available, but never the family definition or its only evidence.

One design constraint worth carrying: **full threads are the wrong unit.** Repetition across places is a listing/search-level signal — many titles, cheaply. Full bodies matter only for verbatim vocabulary, a narrower second pass. At `standard`'s 12 fetches, spending them on whole threads buys depth where this needs breadth.

<!-- D10 — Fetch-outcome ledger -->
### D10 — Fetch-outcome ledger: failures-only, a negative cache 🔨

Decided 2026-09-03 in shape; mechanics deferred to [Q4](docs/questions/Q4-ledger-mechanics.md). Not queued this session.

Origin is `fetch-anything`'s handler registry, **inverted**. There, a ledger records which rung won so the ladder is not re-climbed — which works because three rungs exist. Here, `web-search-agent`'s ladder is two rungs (`WebFetch` → `crwl`) with no crawl4ai-Python and no firecrawl, so a row saying *"firecrawl worked for reddit.com"* is advice this agent cannot act on.

**So the actionable class is the one the idea called "nothing worked."** Don't retry, don't trust a search that quietly returns other domains, here is the substitute. That makes the ledger the **enforcement mechanism for D7** and the **content source for D8's directives**, rather than a rung-router.

**Why this can ship where [harvest-from-runs](docs/parking-lot/harvest-from-runs.md) is stuck:** access outcomes are binary and observed; source *quality* needs judgment, which is exactly [Q1](docs/questions/Q1-source-accumulation.md)'s blocker. Same "accumulate observed evidence from runs" shape, different payload, and only one of them needs a human in the loop.

**Amended 2026-09-04 by D15.** The approved Reddit reader is a named source method, not a generic fetch rung. It does not change this ledger's failures-only purpose or make Firecrawl outcomes actionable to the generic agent.

**Deferred with a revisit pin, 2026-09-04.** Do not build an automatic ledger yet. `unreachable[]` and the report section now preserve the evidence needed to decide whether one pays for itself. Reopen Q4 only when two completed reports from the same consumer project record the same `source` + `reason` failure tuple; until then, manual maintenance of module and site access methods is cheaper than another accumulating store.

<!-- D11 — Unreachable is a separate channel from unanswered -->
### D11 — "Unreachable" is a separate output channel from "unanswered" 🔨

Decided 2026-09-03. **Supersedes D7's mechanism clause** — D7 said "the `uncertain[]` array is already the mechanism; this is what it is for." It is not, and D7's requirement stands unchanged on everything else.

**Two defects found while looking for the implementation, because there is none:**

- **"Record it as unreachable" has no destination.** `agents/web-search-agent.md` says it four times (the exception preamble, and lines 50, 55, 61) and never once names a field, an array, or an output slot. The instruction dead-ends: the agent is told to record something with nowhere to put it.
- **`uncertain[]`'s display is self-contradictory.** `skills/research-report/SKILL.md:78` lists `uncertain` among internal fields to *filter out*; line 80, in the same block, gives it *display formatting*. Section 5 then skips every field named in it. Whether an unanswered field is visible at all depends on which instruction the script-generating agent follows that run.

**Why a separate array rather than overloading `uncertain[]`:** the two facts have different audiences — a *reader* needs to know a named source was a wall, the *pipeline* needs to know a field is blank — and different lifetimes. An unanswered field dies with the run; a wall persists across runs and is exactly the content that feeds `ACCESS.md` and D10's ledger. Overloading would force `generate_report.py` to partially un-skip by parsing the string inside an entry, which is the class of implicit contract this repo already breaks on.

The shape:

| | |
|---|---|
| **Channel** | `unreachable[]` in `results/*.json`, sibling to `uncertain[]` |
| **Placement** | Per-item, deduplicated by `/research-report` into one section. The item agent is the only thing that observes the failure and it writes exactly one file — its own. A run-level file would need N parallel agents writing one path: a concurrency problem and a new `Write` target in a deliberately narrow allowlist. The redundancy is not pure: item 3 may reach a page item 7 could not, and that difference is signal. |
| **Scope** | Both hard fetch failure *and* silent substitution. |
| **Severity** | **Annotates provenance, never blocks a field.** If D8's substitute answered the question, the field is answered — `unreachable[]` records that the answer did not come from the named source. Blocking would make the pipeline fail loudly on a wall it has a documented workaround for, which fights D8's design. |
| **Report** | Keep skipping the unanswered *cell* — an empty cell in a comparison table teaches nothing. Resolve the 78/80 contradiction toward disclosure so coverage is stated rather than silently shrunk. |

**The detection rule, which is what makes the substitution half enforceable:** *if you constrained a search to a domain and no returned URL is on that domain, that is a zero-result finding, not a result set.* Mechanical, no judgment, and the URLs needed to evaluate it are already in the agent's hands. Without that sentence the agent has no reason to look, because nothing errored — which is the whole of D7.

<!-- D12 — Temporary findings must be findable again -->
### D12 — A finding that will expire has to be findable when it does 🔨

Decided 2026-09-03, from a live example. The access-method retrofit typed the sentence *"unreachable from this toolchain — use niche forums and Hacker News instead"* into `general-web.md`, `competitor-content.md`, `vendor-landscape.md`, and `ACCESS.md`. Four copies of a claim that is **expected to become false** — Q3 is open and the whole point of testing firecrawl is to make Reddit reachable. Nothing recorded where those four copies were.

Three parts:

**(a) The citation is the tag.** Anything resting on a finding that can expire must **cite the file that holds it**, by path. That reference is what makes it findable — `grep -rl "sites/reddit.md"` prints the exact revert list — so there is no separate marker syntax to invent, remember, or keep in sync with the thing it marks.

A first pass used a distinct `[ACCESS:reddit]` marker alongside the citation. The user's correction retired it the same session: a module has to reference the site file anyway, and *that reference already is the tag*. Two mechanisms where one does the job is the duplication this decision exists to stop, so the marker was removed rather than kept "just in case."

The substitute still has to appear **inline** in the module bullet — one line, self-sufficient — because the agent must be able to act without opening a second file mid-run. So the goal is not to eliminate the restatement but to make every restatement point at its source.

**(b) `ACCESS.md` is a maintenance index, not a runtime file.** Nothing loads it during a run and nothing should. D8 described it on the `ROUTING.md` model, but `ROUTING.md` is read by the agent on every task and this is not — the substitute already lives in the module bullet. Stated in the file itself so nobody later "fixes" it by wiring it into the agent prompt.

**(c) The task contract gains a `Reversible if:` line.** One line per task naming any open question whose answer would undo part of the work. Q3 was open for the entire retrofit and nothing in the task said the Reddit bullets were provisional, which is how four copies of an expiring claim got written without a trace. Pairs with (a): the line says *what* could reverse it, the tag says *where*.

<!-- D13 — A public package must tell the human how to enable its optional rungs -->
### D13 — If a capability is gated on something the consumer must install, the package says how 🔨

Decided 2026-09-03. This is an APM package other people install, and it currently ships a feature that can silently never work.

**The existing gap:** `README.md:123` documents the `crwl` fetch fallback, and `agents/web-search-agent.md` correctly tells the agent to check `command -v crwl`, stop if absent, and **never install anything**. That agent rule is right and stays. But no file anywhere tells the *human* how to install `crwl`. A consumer installs the package, the fallback never fires, and nothing explains why — the capability reads as broken rather than as unconfigured.

**The rule:** any capability gated on a binary, an API key, or an account gets a short setup note in `README.md` — what it is, what it buys, that it is optional, and how to get it. The agent prompt keeps saying "never install"; the README is where a person is told. Those are different audiences and the current docs only serve one.

**Applies now to `crwl`, and to firecrawl if it is ever added** ([Q6](docs/questions/Q6-firecrawl-rung.md)). Firecrawl carries an extra obligation the others do not: it is a **paid API**, so it can never be a silent default — a consumer must opt in knowing it costs them money. Its signup link is `https://firecrawl.link/stephan-miller`, and because that is a referral link it should be labeled as one where it appears. Disclosing it costs nothing and is the norm; an undisclosed one in a public repo is the kind of thing that gets noticed later.

<!-- D14 — Site files, earned by recurrence -->
### D14 — A site earns its own file when a second module names it 🔨

Decided 2026-09-03; **seven** files built the same day. Modules stay organized by **topic**; the **sites** inside them become a small referenced layer at `skills/web-search-modules/sites/<slug>.md`.

**The threshold is recurrence, not judgment.** A site gets a file when it is named by two or more modules — the same logic as D2's "no module until a real project needs one," applied one level down. Nothing is written speculatively, and the set grows only when the payload itself demonstrates the need.

**Measured — after two bad counts, which are recorded because the method mattered more than the number.** Counting by *domain string* (`reddit.com`) found 6 recurring sites, but modules name sites in prose, so it undercounted. Counting by *prose name* found 9, but it overcounted: it matched routing-header cross-references (`academic-papers.md` names `github-debug` in its `Siblings:` line — a pointer to a sibling **module**, not a citation of github.com), comparisons (`chinese-tech.md` calls SegmentFault "similar to Stack Overflow"), and a substring (`v2ex.com` contains `x.com`).

**The number that counts is citations in a `## Sources` bullet with an access method attached** — the only kind of mention a site file can serve:

| Site | Modules citing it |
|---|---|
| GitHub | **4** — `agent-tooling`, `benchmarks`, `github-debug`, `model-releases` |
| Reddit · Hugging Face | 3 |
| OpenRouter · Hacker News · `dev.to` · Artificial Analysis | 2 |
| Stack Overflow · Twitter/X | **1 each — below threshold** |

GitHub at 4 still proves the point: the raw `CHANGELOG.md` pattern and the check-the-last-commit-date rule live in `agent-tooling` and nowhere else, while three other modules cite GitHub without them.

**Two triggers, not one.** The threshold above is *recurrence*. The second is *overflow* — one module whose site knowledge already exceeds what the module can hold. Both are earned by something that **exists**: a site file is never created for content someone intends to write. Stack Overflow clarified this. It is cited by exactly one module, so it fails recurrence; it is the textbook overflow case *once the parked rewrite exists*, but until then there is nothing to overflow, and a file holding only what the module bullet already says is an empty container inviting speculative filling. It gets its file the day the rewrite lands. Twitter/X fails both triggers and has no written method anywhere.

**Division of labor, and why the module bullet cannot just be a pointer:**

| | Holds | Why |
|---|---|---|
| **Site file** | the deep, durable method for one site; a dated one-line reachability verdict | Written once. This is what the six GitHub bullets are currently missing. |
| **Module bullet** | one self-sufficient line of access method, plus a path citation | The agent must be able to act **without opening a second file mid-run**. A bullet that only says "see the site file" strands the agent if nothing loaded it. |

**Two motivations, and only one of them was real.** Sharing a site across modules is the weak case on its own — nine files is a footnote, not a library. The strong case is **overflow**: `stackoverflow.md` needs the closed/duplicate signal, score-vs-recency, `[tag]` syntax, and comment-vs-answer, none of which fit in a module that also has to cover the rest of Stack Exchange under a ~40-line cap. Site files are an overflow mechanism that happens to also deduplicate, not a parallel taxonomy. Nothing about routing changes.

**These are author-and-maintainer reference for now — nothing loads them at runtime**, same standing as `ACCESS.md` under D12(b). Wire one into the agent only if a real run shows the inline bullet was not enough. That keeps the context cost at zero until there is evidence it is needed.

**`ACCESS.md` gives up its site-keyed entries.** Reddit's section becomes `sites/reddit.md`'s `Reachable:` line. `ACCESS.md` keeps only what has no site to live in — "JS-shell pages," and the note on how far the JSON-endpoint trick generalizes.

<!-- D15 — Scripts belong to their reuse scope -->
### D15 — Scripts belong to their reuse scope; approved scripts are part of research 🔨

Decided 2026-09-04. The concern is not scripting. A deterministic script that extracts or normalizes a known source avoids spending model tokens on work code can perform more cheaply and consistently. The constraint is **lifetime and ownership**, so throwaway helpers do not accumulate in a global area.

| Reuse | Location | Rule |
|---|---|---|
| One run | That run's `{run_dir}` | A task may create it only at its designated path. It is output for that research process, not package infrastructure. |
| One consumer project | A project-owned location, named only when a real repeated use earns one | Do not create an empty global helper directory speculatively. It survives package updates because the project owns it. |
| Multiple package consumers | The package payload | A reviewed, versioned helper is installed with the skill and may be invoked as part of the research method. |

`skills/research/reddit_feed.py` is the third case: it is a reusable reader for Reddit's public Atom listings, not a per-run convenience script. The research agent may invoke an **approved existing** helper by its resolved package path; this is distinct from authoring arbitrary scripts while researching. The eventual invocation rule must keep its existing boundaries explicit: a named helper and documented arguments, stdout only with a bounded result, no downloads or browser automation, and each network request counted against the item's fetch budget.

For the Reddit helper, a `429` retry is another network request and consumes another fetch slot. Its invocation must cap retry attempts at the item's remaining fetch budget rather than allowing the helper's backoff to overspend it.

**Why this distinction matters:** the old "do not write your own scripts" sentence was guarding against an agent improvising crawlers, report generators, and caches to evade retrieval limits. It does not prohibit a maintained helper whose purpose, inputs, and bounds are already reviewed. The general rule stays: generated one-off scripts live with their run; reusable helpers earn a durable home only through actual repeat use.

**Shipped 2026-09-04** — see `TASKS.md` `[helper-firecrawl]`. The helper carve-out is written as an allowlist of exactly one: the prompt names `reddit_feed.py` and forbids every other helper in the same breath, so it does not read as general permission to invoke scripts. `--max-attempts` is what keeps the helper's own `429` backoff inside the item's fetch budget instead of quietly outspending it.

<!-- D16 — Firecrawl is an optional shipped fallback -->
### D16 — Firecrawl is an optional third fetch rung 🔨

Decided 2026-09-04. The shipped ladder is `WebFetch` -> `crwl` -> Firecrawl for the same URL, climbing only after the prior rung fails. A dedicated project fetch-escalation skill still takes precedence when available; the bundled ladder is the ready-to-use fallback that avoids reworking an active research project just because a consumer did not install that separate skill beforehand.

Firecrawl is optional and paid. The agent never installs it. A consumer opts in by configuring `FIRECRAWL_API_KEY` and making the Firecrawl CLI available; when either is absent, the agent records the URL as unreachable after the available rungs rather than prompting, installing, or spending money. When Firecrawl runs, the agent states that it used the paid rung and treats that call as the current URL's bounded fallback, never a route into crawling or browser automation.

This supersedes Q6's decision question. **Shipped 2026-09-04** — see `TASKS.md` `[helper-firecrawl]`. The bounded invocation is `firecrawl scrape "<url>" -f markdown -o "<item-specific temp path>.md"`, then `head -c 40000` on that file, then delete it. That shape came from a live scrape on an opted-in machine rather than from the docs: Firecrawl writes plain Markdown to the `-o` path with no JSON envelope and keeps stdout to a one-line scrape ID, which is why the temp-file-and-delete form is the bounded one rather than a stdout pipe like `crwl`'s.

## Open questions

> Each is a heading (the question) + a link to its discussion in `docs/questions/`. Thread files are append-only — a later grill adds a dated section rather than rewriting.

### Q1 — Should modules accumulate sources over time, and which kind can?

See [docs/questions/Q1-source-accumulation.md](docs/questions/Q1-source-accumulation.md).

### Q2 — What makes an access method "tested"? — ✅ resolved 2026-09-04

See [docs/questions/Q2-tested-access-method.md](docs/questions/Q2-tested-access-method.md).

### Q3 — Is Reddit reachable at all, and from where? — ✅ **answered 2026-09-03: yes, via the public Atom feeds**

Every *scraper* route failed at a permission gate — the harness blocks the domain for `WebFetch`, firecrawl refuses it by vendor policy, and the OAuth API's signup could not be completed. **The feeds were never tested, and they are open.** `skills/research/reddit_feed.py` reads them with the stdlib: no account, no key, no dependency. It needed no new permission, because `Bash` was already in the allowlist and the `crwl` carve-out was always a *rule*, not a permission. Listings are also the right unit for D9. See [docs/questions/Q3-reddit-reachability.md](docs/questions/Q3-reddit-reachability.md).

### Q4 — Where does the fetch-outcome ledger live, and who may write it? — deferred; reopen on D10's repeat-failure pin

D10 settles the ledger's shape, not its mechanics: location (the `apm install` overwrite problem), the `Write` carve-out an item agent would need, and expiry. See [docs/questions/Q4-ledger-mechanics.md](docs/questions/Q4-ledger-mechanics.md).

### Q5 — Should sites be their own structure, referenced by topic modules? — ✅ resolved by D14

Modules are organized by topic. Sites recur across them and each one has its own querying quirks, which are currently rediscovered every run. See [docs/questions/Q5-site-references.md](docs/questions/Q5-site-references.md).

### Q6 — Should firecrawl become a third fetch rung in the shipped agent? — ✅ resolved by D16

Needed *now* as a maintainer tool to answer Q3. Whether it ships inside `web-search-agent` is a separate and larger question, because it is paid and the carve-out is deliberately narrow. See [docs/questions/Q6-firecrawl-rung.md](docs/questions/Q6-firecrawl-rung.md).

## Parking lot

> Deferred ideas. Each is a one-line hook + a link to `docs/parking-lot/`.

- **Harvest sources from completed runs into a local module** — [docs/parking-lot/harvest-from-runs.md](docs/parking-lot/harvest-from-runs.md)
- **Rewrite `stackoverflow.md`** — 12 lines, two vague source bullets, zero query tactics; a rewrite, not a retrofit — [docs/parking-lot/stackoverflow-rewrite.md](docs/parking-lot/stackoverflow-rewrite.md)
- **Non-technical families** (health, law and policy, finance) — attach when a project needs one; `competitor-content` is the worked example — [docs/parking-lot/non-technical-families.md](docs/parking-lot/non-technical-families.md)
- **Wanted modules** (AI writing communities, docs-and-API-reference) — parked under D2 until real demand — [docs/parking-lot/wanted-modules.md](docs/parking-lot/wanted-modules.md)
- **The AUQ consumer install** — pin bump, `rough/`-level vs per-client scope, and DeepInfra/OCR local modules; one cluster because the scope question gates the other two — [docs/parking-lot/auq-consumer-install.md](docs/parking-lot/auq-consumer-install.md)
- **Verify the `crwl` fetch fallback** — ✅ **tested 2026-08-29**: escalation runs clean and the `head -c` bound holds, but it does *not* recover a JS-shell page. Rule kept; prefer a JSON endpoint beside the HTML page instead — [docs/parking-lot/verify-crwl-fallback.md](docs/parking-lot/verify-crwl-fallback.md)

## Session log

> Most recent sessions inline; older sessions archived → see `docs/sessions/`.

### Session 7 — 2026-09-04

- **D15 and D16 shipped together** — the fetch contract is now a three-rung ladder (`WebFetch` → `crwl` → Firecrawl) for one URL, and `reddit_feed.py` is the one approved package helper an item agent may invoke. Both landed in the same task because they are the same edit to the same two prompts; splitting them would have meant rewriting the Tool Discipline section twice.
- **The fetch budget was redefined, not just extended.** It now counts every network retrieval attempt rather than only native `WebFetch` calls — otherwise the two new rungs and the helper's `429` retries would have been free, which is exactly the overspend the budget exists to prevent. A blocked page's whole ladder is still one logical fetch sequence for that URL; the helper's individual attempts each cost a slot.
- **Firecrawl's CLI shape was settled by running it, not by reading about it.** A single control scrape on this opted-in machine showed it writes plain Markdown to `-o` and prints only a scrape ID — so the bounded form is temp-file-then-delete, not a stdout pipe. This is what the previous session deferred for lack of a configured key.
- Review caught nothing that had to be reverted. One thing worth recording: the task's own Test 5 `rg` was scoped to the eight files it edited, so a repo-wide grep was needed to confirm no stale Reddit directive survived elsewhere. It found two hits in `web-search-modules/SKILL.md` that are the *authoring guidance* for the fourth-form directive pattern — still correct, correctly untouched. Same shape as the case-sensitive `reddit` grep in the `[access-methods]` task: a test that can pass by not looking.

### Session 6 — 2026-09-04

- **D11 shipped** — `unreachable[]` is now a structured per-item provenance channel, separate from unanswered `uncertain[]`. Each entry is `{source, url, reason}`, with `fetch_failed` for an inaccessible page and `zero_domain_results` for a named-domain search that returned no matching-domain URLs. The report contract deduplicates entries and renders a visible `## Unreachable sources` section with affected items, while fields answered through a documented substitute remain answered.
- The canonical research-agent prompt and `/research-deep` hard-constrained prompt template now carry the same detection and output rules; its one-shot example was changed in lockstep. Validator compilation, targeted contract checks, and `git diff --check` passed.

### Session 5 — 2026-09-03

Two implementer queues shipped and a two-round grill, interleaved. Opened by reviewing the returned access-method retrofit, which is what surfaced the session's real finding.

- **The retrofit landed** — all 7 pieces, ten modules now carry access methods, `ACCESS.md` created. Review caught three things: a case-sensitive `grep` in the task's own Tests that passed by skipping a file, two URLs written without content verification (both the right page, neither a guess), and one bullet that named a block with no substitute — the exact passive form the task had just replaced.
- **D7 named a mechanism that does not exist.** Looking for its implementation found none: the agent prompt says "record it as unreachable" four times and never names a destination, and `research-report/SKILL.md` contradicts itself two lines apart about whether `uncertain[]` is displayed or filtered. **D11** gives "unreachable" its own channel, annotating provenance rather than blocking a field, and supersedes D7's mechanism clause while leaving the rest of D7 standing.
- **D12** came from the user asking the right question about the diff: the retrofit had typed an expiring claim into four files with no record of where. The answer went through one revision — the agent's `[ACCESS:reddit]` marker was retired when the user pointed out that a module must cite its site file anyway, and *that citation is already the tag*.
- **D13** from the user noting this is a package other people install: the `crwl` fallback is documented as a feature with install instructions nowhere, so it can silently never fire. Any capability gated on a binary, key, or account now gets a README setup note. Firecrawl carries the extra condition that it is paid, so never a default, with a labeled referral link.
- **D14** unifies the session's structural thread. Sites become a small referenced layer, earned at two modules. Counting settled it: GitHub is named by six modules and only one of them knows how to query it properly.
- **Q3's blockers were both false** — the inaccessible machine is the work computer, not this one, and the firecrawl key and CLI are already installed here. The re-test is runnable now, and Q3 now carries the revert list beside the procedure.
- **Q6** opened rather than decided: whether firecrawl ships inside the agent is a different question from using it to answer Q3, because the fetch carve-out ends with the words "no second helper" and firecrawl spends the consumer's money.

Mirror reconciled both directions; its three repo-less items landed as one parking-lot cluster, since the install-scope question gates the other two.

### Session 4 — 2026-09-03

Planning only, no code. Opened on whether the pipeline can support the research process in a web-clip article (*I Gave AI 30 Days…*), whose Day 1–3 is: find a problem people repeatedly describe in their own words across unrelated places. That process leans on Reddit, so the session tested whether Reddit is reachable at all.

- **It is not, from this machine** — all five routes inside the agent's tool discipline failed, and the search layer fails **silently**, returning ten plausible results from other domains with no error. That produced **D7 (no silent substitution)**, the session's one 🔒 decision, and it is about behavior rather than about Reddit.
- The parked `search-layer-refusals` doc proposed "look for a JSON endpoint beside the HTML page" as the fix. **Falsified for Reddit** — the endpoint exists and is unreachable. The heuristic stays correct for Discourse; it is not general. Amended in place.
- **D8** splits venue from access — the two things "topic vs source" was conflating. Access moves to one shared file (the `ROUTING.md`/`LAYOUT.md` pattern), the router is untouched, and the spec's fourth access-method form is sharpened from a passive note into a directive naming a substitute. A Reddit *modifier* (the `chinese-tech` shape) is the right venue answer if one is ever needed, and waits on Q3.
- **D9** unparks a `demand-signals` module — D2's trigger met by explicit demand plus two prior under-sampled runs — scoped to the research stage and built Reddit-free.
- **D10** takes the session's new idea, a per-domain fetch-outcome ledger modeled on `fetch-anything`'s handler registry, and **inverts it**: this agent has two rungs and no firecrawl, so "which rung won" is unactionable and "nothing worked" is the whole value. It becomes D7's enforcement mechanism and D8's content source.
- Correction taken mid-round: the evidence is **one machine, one IP, one harness build**, and this plan is destined for a different computer. Firecrawl was never tested. **Q3** therefore carries the re-test procedure, not the conclusion.

Nothing queued to `TASKS.md` — the access-method retrofit remains the active task, untouched.

### Session 3 — 2026-08-25

Mined the only non-empty Copilot session in `tpo-copilot-desktop-research` and traced the failed installed pipeline. The package was simultaneously active for Claude and Copilot, producing duplicate `web-search-agent` registrations; the Copilot child received no tools even though the Claude allowlist was present. A user-created `.github/agents/web-research-writer.agent.md` with Copilot-native tool categories succeeded. Decided D6 and queued the portability retrofit ahead of the untouched access-method task.

### Session 2 — 2026-08-22

Results organization. Raised from the parking lot: run folders land at the project root, which is wrong in every repo where the research sits alongside code, and nothing anywhere records that one run's findings pointed at the next.

- Decided **D3** (one root, default `research/`, discovered structurally rather than configured), **D4** (`INDEX.md` as the branch record — Map, per-run summary, Leads), and **D5** (`skills/research/LAYOUT.md` is the single source of truth, the `ROUTING.md` pattern).
- Two latent bugs surfaced while designing it: `output_dir`'s base directory was never stated (it reads differently once nested), and `research-deep`'s validator example teaches a `{project_dir}/../.claude/…` relative path that goes one level too shallow under the new layout.
- Queued the six-piece implementation ahead of the access-method retrofit, which moves to ⏸ QUEUED untouched.
- **Shipped it the same session** (`[results-root]` in `TASKS.md`). Review caught three things the implementation missed, all now fixed: the status ladder was lossy (a researched-but-unreported run read as `researching` — split into four states), legacy root-level runs have no index and every index-writing step must skip rather than create one, and `/research-report` still ran `python {topic}/generate_report.py` from the cwd, which is one level too shallow once runs nest. `{run_dir}` and `{project_dir}` are now defined at each locate step instead of being implied.

### Session 1 — 2026-08-21

Scaffolded the planning workflow. Before that, resolved a long-standing loose end: the **external task mirror**.

- Found that a bidirectional plan/vault sync (`PLAN SYNC`) had been **built** months earlier in the `vault-writer` skill and **never wired up** — zero vault notes carried `plan-repo:`, including the one the skill used as its own worked example. The design was sound (asymmetric authority: status repo→vault, new items vault→repo, priority vault-only, prose never); it was simply unreachable.
- Generalized it: `plan-file:` (defaults `TASKS.md`) so any markdown checklist works, a guard that refuses prose files outright, and a rule that new items land in an **intake section** (parking lot / backlog / `Next` tier) rather than active work — because discovering work and scheduling work are different authorities.
- Added a generic **External task mirror** pointer to `living-plan` itself (conductor-only, opaque path, zero vault vocabulary) so the mirror is named at scaffold time instead of being forgotten. Retrofitted 4 projects + this repo.
- Decided D1 and D2 above. Queued the access-method retrofit.

## Relocated (progressive disclosure)

- Decisions archive → [docs/decisions/](docs/decisions/)
- Questions detail → [docs/questions/](docs/questions/)
- Parking-lot detail → [docs/parking-lot/](docs/parking-lot/)
- Session archive → [docs/sessions/](docs/sessions/)
- Rebalance log → [docs/rebalance-log.md](docs/rebalance-log.md)
