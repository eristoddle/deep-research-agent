---
name: research-enumerate
user-invocable: true
description: Sweep broad and shallow to catalog what exists in a domain, writing catalog.md plus a standard outline.yaml a later /research-add-fields + /research-deep pass can descend on.
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---

# Research Enumerate - Breadth-First Catalog Sweep

## Trigger
`/research-enumerate [run-folder-name]`

Naming an existing run folder re-invokes on it as round 2 (Step 7); otherwise this creates a new run.

## Workflow

### Step 1: Locate or Create the Run Folder
A fresh sweep creates a new run folder under the research root, exactly as `/research` does: locate the root and run the discovery glob per `skills/research/LAYOUT.md` before creating anything, and ask for the root name once only if none exists yet — do not restate the discovery rule here. A round 2 invocation names an existing run folder directly and skips creation.

### Step 2: Gather the Sweep's Inputs
- **Taxonomy (required).** Ask via `AskUserQuestion` if the invocation did not supply one, and offer to propose a starting taxonomy the user edits. The run does not start without one — without categories to sweep and report coverage against, "done" is unfalsifiable.
- **Exclusion list (optional, first-class).** Accept a list of names, or a path to an existing `catalog.md` whose entries are all treated as known. This is what keeps a re-invocation to genuinely new material rather than re-deriving the register.
- **Shallow field set, 3-5 fields.** A link, a one-line description of what the thing is, and whatever terms are public. Propose a default set from the taxonomy and let the user edit it. This is not `fields.yaml`, and this sweep never writes one — `/research-add-fields` is the descend path for that.

### Step 3: The Two-Phase Sweep
**Phase 1 — aggregators. Phase 2 — one-offs.** Before enumerating leaves, look for the thing that lists the leaves: directories, marketplaces, registries, awesome-lists, category pages. One aggregator can yield dozens of items at once, so phase 1 runs first; phase 2 catches what no aggregator carries, at much lower yield per search.

**Budget is per-phase, not per-item.** This is not the `quick`/`standard`/`deep` table `/research-deep` uses — that table is per-item and already duplicated in two files, and widening it to cover sweeps would make a third copy. Each phase gets its own ceiling: **20 searches and 20 fetches**.

**Host selection rule, copied from `/research-deep`:** in GitHub Copilot, launch `Web Research Writer`; in Claude Code, launch `web-search-agent`. Launch one host-selected agent per phase with the prompt template below.

**The stopping rule is coverage, not exhaustion.** The agent reports searches and fetches used **per phase as it goes**, and stops at the ceiling rather than disclosing an overrun afterward. A phase that hits its ceiling with categories still uncovered is a successful run with an honest coverage gap, not a failure.

### Step 4: The Prompt Template

**Hard Constraint**: The following prompt must be strictly reproduced, only replacing variables in {xxx}, do not modify structure or wording.

**Prompt Template**:
```python
prompt = f"""## Task
Phase {phase} sweep of {topic}, covering categories: {categories}. {phase_focus}

## Exclusions
Treat every name in {exclusions} as already known. Do not re-report it.

## Fields
Per item found, capture: {field_list}.

## Budget
Hard limits for this phase: {searches} WebSearch calls, {fetches} fetches. Report usage as you go,
e.g. "[phase {phase}: 6/20 searches, 4/20 fetches]". Stop at the ceiling rather than continuing
past it or disclosing an overrun afterward.

## Rules
1. A blank is a result; a guess is damage. Where a value is not publicly stated, the field reads
   exactly `not public`. An inferred figure is never acceptable.
2. Every category ends in exactly one of three states: Checked, none found (searched properly,
   nothing there); Checked, inconclusive (found something, could not confirm it from a source
   that counts); Not checked — budget exhausted (never omit this silently — an unreached
   category must say so).
3. No browser automation, no downloads, no cloning, no self-written scripts.

## Output
Append to {catalog_path}: one table row per item found under its category, plus that category's
negative-state note. End the file with `## Unreachable`, `## Sources`, and `## Uncertain`.
"""
```

**One-shot Example** (assuming a phase 1 sweep of AI affiliate programs):
```
## Task
Phase 1 sweep of AI and dev-tool affiliate programs, covering categories: web scraping APIs, AI coding tools, LLM API providers, AI writing tools, PKM tools. Phase 1 is aggregators: find the directories, marketplaces, registries and category pages that list many programs at once, before enumerating individual programs.

## Exclusions
Treat every name in ['Dub'] as already known. Do not re-report it.

## Fields
Per item found, capture: name, link, what it is, commission terms.

## Budget
Hard limits for this phase: 20 WebSearch calls, 20 fetches. Report usage as you go,
e.g. "[phase 1: 6/20 searches, 4/20 fetches]". Stop at the ceiling rather than continuing
past it or disclosing an overrun afterward.

## Rules
1. A blank is a result; a guess is damage. Where a value is not publicly stated, the field reads
   exactly `not public`. An inferred figure is never acceptable.
2. Every category ends in exactly one of three states: Checked, none found (searched properly,
   nothing there); Checked, inconclusive (found something, could not confirm it from a source
   that counts); Not checked — budget exhausted (never omit this silently — an unreached
   category must say so).
3. No browser automation, no downloads, no cloning, no self-written scripts.

## Output
Append to research/ai-affiliate-programs/catalog.md: one table row per item found under its category, plus that
category's negative-state note. End the file with `## Unreachable`, `## Sources`, and `## Uncertain`.
```

### Step 5: Write `catalog.md`
One section per taxonomy category, each holding a table of found items carrying the shallow fields, plus its own **Checked, none found** / **Checked, inconclusive** / **Not checked — budget exhausted** subsection — never omit the last one silently. A blank field reads exactly `not public`; never infer. The file ends with `## Unreachable`, `## Sources`, and `## Uncertain` — the existing spellings (D11, D17, base contract), no synonyms.

The three states are per-category and mutually exclusive — a category that yielded items is not also "none found":

```
### Web scraping APIs
| Name | Link | What it is | Commission |
|---|---|---|---|
| Apify | affiliate.apify.com | Scraping/automation platform | 20% for 3 months, then 30% recurring |
| Zyte | zyte.com/affiliate | Scraping platform | not public |

### LLM API providers
Checked, none found — Together AI, Fireworks, Replicate, Groq and Modal were each checked directly; none publishes an affiliate program.

### PKM tools
Not checked — budget exhausted. Ceiling reached before this category got any coverage.
```

### Step 6: Write `outline.yaml` and Append `INDEX.md`
Write a standard `outline.yaml` in `{run_dir}`: `items[]` built from what the sweep found (name, category, and the shallow fields, in the same shape `/research` writes), plus an `execution{}` block with the package defaults (`batch_size`, `items_per_agent`, `output_dir: ./results`, `depth: standard`; omit `modules` unless the sweep pinned one). The folder now contains an `outline.yaml`, so `LAYOUT.md`'s discovery glob finds it unmodified, and `/research-add-fields` then `/research-deep` can descend on it later with no new wiring.

Append the `INDEX.md` stub exactly as `/research` does — purpose line, `date · N items · depth · status`, status **`outline`**, `Spawned from:` if applicable. Per `LAYOUT.md`, skip this step silently if the run folder has no root above it.

### Step 7: Round 2
Pointing `/research-enumerate` at an existing run folder, plus an exclusion list drawn from its own `catalog.md`, re-runs Steps 2-6 against it with a fresh per-phase budget: new findings are appended to `catalog.md`, new items to `outline.yaml`. One paragraph, no second code path.
