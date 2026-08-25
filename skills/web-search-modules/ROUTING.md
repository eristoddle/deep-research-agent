# Module Routing

Read this file before any `WebSearch` or `WebFetch`. Pick modules here, read them, then search. Never search before reading at least one module.

Module files live beside this router. Resolve the packaged directory in order and use the first that exists: `.agents/skills/web-search-modules/` in the current project, `.claude/skills/web-search-modules/` in the current project, `~/.agents/skills/web-search-modules/`, then `~/.claude/skills/web-search-modules/`. Module names below are bare — `github-debug` means the file `github-debug.md` in that directory.

## 0. Check for local modules

Before using the table below, check `.agents/web-search-modules-local/ROUTING.md` in the current project, then the legacy `.claude/web-search-modules-local/ROUTING.md`. Read the first one that exists — the project has search modules of its own, and they are usually sharper for that project's work than anything packaged here.

Local families and modules merge with the ones below. On a name conflict the local one wins. Local module files live beside that local router, not in this directory.

Each `Read` that fails *is* the check — do not hunt for the file, and do not spend a `Bash` call on it. If neither router is there, ignore this step; that is the normal case.

## 1. Caller override wins

If the task prompt names modules explicitly — `Modules: benchmarks, general-web` — load exactly those and skip to step 5. If it names a mode in prose ("just a general web search", "papers only"), honor that the same way. The caller knows the topic; you know the source map.

## 2. Pick one topic module

Work down the families in order and stop at the first whose question is a yes. Read **one** module from it.

| Family | Ask yourself | Modules |
|---|---|---|
| Software & debugging | Is something broken, erroring, failing to build, or version-specific? | `github-debug`, `stackoverflow` |
| Literature | Does the answer live in a paper, preprint, or citation trail? | `academic-papers` |
| AI ecosystem & market | Is it a fact about a shipped AI product — its scores, its versions, its price, or who competes with it? | `benchmarks`, `model-releases`, `pricing`, `vendor-landscape` |
| Published-content landscape | Is the question what has already been *written* about this topic, and what those pages cover? | `competitor-content` |
| General *(default)* | Nothing above fits — opinion, practice, comparison, product, news, or anything unclassified | `general-web` |

Within **software & debugging**: `github-debug` when the artifact is a specific project (an error from a named library, a regression, a known bug); `stackoverflow` when the question is how to use a language or API correctly.

Within **AI ecosystem & market**, pick by what the answer *is*:

| The answer is… | Module |
|---|---|
| a published number — score, rank, throughput | `benchmarks` |
| a version, a date, a model ID, a deprecation | `model-releases` |
| a cost, a rate limit, a region | `pricing` |
| a competitive set, a claim, a positioning | `vendor-landscape` |

These four overlap by design — a question about a new model's price and scores is genuinely two of them. Take two only if the task actually asks for both; otherwise take the one the caller's *question* is about and let the other go.

**General is a real answer, not a failure.** Most questions are general-web questions. Routing to it because nothing sharper fits is the system working.

## 3. Optionally add a second module

One more, only if it earns its slot. Valid seconds:

- **A module from a second family**, when the task genuinely spans two — "attention papers and their open-source implementations" is `academic-papers` + `github-debug`.
- **`general-web`**, alongside any topic module. It is the cheap generalist and pairs with almost anything: a specialist module tells you where authoritative answers live, general-web tells you what practitioners actually report. Default to adding it when the task asks for comparison, tradeoffs, real-world experience, or "what should I use".

Never a third topic module. If a task looks like it needs three families, it should have been split into separate tasks by the caller — say so in your output rather than trying to cover them all.

## 4. Modifiers

Modifiers are not topics. They are axes — language, region, recency — layered on top of a topic module, and they answer *where else to look*, not *what the question is about*.

| Modifier | Layer it on when |
|---|---|
| `chinese-tech` | The subject is open-weight models, Chinese vendors, or work likely published on Chinese platforms first — or English results came back thin on a topic where they plausibly wouldn't be |

At most one modifier. A modifier never replaces a topic module.

## 5. Budget

Module slots come from the run's depth level. These are the same numbers as the search budget — do not exceed them.

| Depth | Slots | What fills them |
|---|---|---|
| `quick` | 1 | One topic module. No modifier. |
| `standard` | 2 | Topic module + one of: second topic module, `general-web`, or a modifier. |
| `deep` | 3 | Up to two topic modules + one of: `general-web` or a modifier. |

## 6. When routing is ambiguous

You cannot ask the user — you are a subagent with no interactive tools. So do not stall and do not hedge by loading more modules. Instead:

1. Load `general-web` plus your best-guess topic module and proceed.
2. **State the routing decision in your output**, with the runner-up: `Routed: general-web + stackoverflow (github-debug was a close second).`

That line is the mechanism. It tells the caller to re-run with an explicit `Modules:` override when you guessed wrong, which is cheaper than guessing well.

Callers that *can* ask — the `/research` skills, which have `AskUserQuestion` — should resolve this up front and pass `Modules:` in the task prompt.
