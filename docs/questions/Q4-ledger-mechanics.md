# Q4 — Where does the fetch-outcome ledger live, and who is allowed to write it?

> **Status:** open
> **Opened:** 2026-09-03 · **Last touched:** 2026-09-04

## The question

`PLAN.md` **D10** settles *what* the ledger is (a failures-only negative cache) and *why*. It
does not settle three mechanics, each of which can sink it independently: where the file lives,
how an agent is permitted to append to it, and when an entry expires.

## Thread

> Append-only. Each grill round adds a dated section below the existing ones.

### 2026-09-03 — opened

Grill round 1 decided the ledger's shape (D10) and deferred its mechanics. Three unresolved:

**1. Where it lives.** The ownership split from D1 applies, and none of the three options is
free:

| Location | Survives `apm install`? | Scope |
|---|---|---|
| `skills/web-search-modules/` | **No — overwritten every install.** Fatal for an accumulating file. | — |
| `.agents/web-search-modules-local/` | Yes | One project. Every new project re-learns the same blocks from scratch. |
| `~/.agents/…` (user level) | Yes | All projects — but then it is not in this repo at all, and nothing ships to other consumers. |

The tension is real: the knowledge is **user-and-machine-scoped** (Q3 shows the same domain can
behave differently per IP and per harness), which argues for user level. But a package that
ships no ledger ships nothing — each consumer starts empty. A seeded-but-overridable split may
be the answer and has not been designed.

**2. The write carve-out.** `agents/web-search-agent.md` states *"`Write` is for your designated
output file only — do not create scratch files, caches, or notes."* A ledger **is** a cache, by
name. An item agent appending to it needs an explicit exception, and this repo's own `CLAUDE.md`
warns that every clause of the existing `crwl` carve-out is load-bearing and that loosening one
turns it into general permission to script around blocks.

Options not yet weighed: the item agent writes directly; the item agent *reports* blocks in its
output and the orchestrating skill (which already has `Write`) records them; or the ledger is
only ever written by a human / `/research-add-module`.

The middle option looks cheapest — it needs no change to the agent's allowlist at all, and the
orchestrator already aggregates item results. It has not been checked against what an item
agent's output format can carry.

**3. Expiry.** A block observed once may lift; a ledger that never forgets eventually stops the
agent from trying things that would now work. Dating every entry is the obvious move and
connects to Q2's unresolved staleness half — see below.

### 2026-09-03 — interaction with Q2 noted

Q2 ("what makes an access method tested") lists *stamp an observation date* as an option and
rejects it as too expensive: module files are capped at ~40 lines and `academic-papers.md` is
already at 31.

**The ledger may dissolve that constraint.** It is a dated observation store that lives outside
the module line budget, so dates cost nothing there. If the ledger ships, Q2's follow-on may
close as a side effect rather than needing its own answer.

Not promoted to a decision — it depends on where the ledger lands (mechanic 1 above), since a
per-project ledger cannot carry dates for a package-shipped module's sources.

### 2026-09-04 — deferred with a concrete revisit trigger

Do not build the ledger before it has demonstrated a repeated job. D11's `unreachable[]` records
and the final report's `## Unreachable sources` section now retain the necessary evidence without
adding a cache or a new write exception.

Reopen this question only when two completed reports in the same consumer project contain the same
`source` + `reason` failure tuple. That is the threshold at which manual maintenance of a module or
site-file directive has demonstrably started repeating; then decide location, writer, and expiry
against real evidence rather than a hypothetical store.

## Blocked on

- Nothing external. This is designable now; it was deferred for round length, not for missing facts.

## Related

- `PLAN.md` **D10** (the ledger's shape) · **D1 🔒** (the ownership split this inherits)
- [Q1 — source accumulation](Q1-source-accumulation.md) — the sibling mechanism; same "accumulate
  observed evidence from runs" shape, blocked on judgment where the ledger is not
- [Q2 — tested access methods](Q2-tested-access-method.md) — its staleness half may close here
