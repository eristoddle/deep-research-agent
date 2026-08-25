---
name: research
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, WebSearch, Task, AskUserQuestion
description: Conduct preliminary research on a topic and generate research outline. For academic research, benchmark research, technology selection, etc.
---

# Research Skill - Preliminary Research

## Trigger
`/research <topic>`

## Workflow

### Step 1: Generate Initial Framework from Model Knowledge
Based on topic, use model's existing knowledge to generate:
- Main research objects/items list in this domain
- Suggested research field framework

Output {step1_output}, use AskUserQuestion to confirm:
- Need to add/remove items?
- Does field framework meet requirements?

### Step 2: Web Search Supplement
Use AskUserQuestion to ask for time range (e.g., last 6 months, since 2024, unlimited).

**Parameter Retrieval**:
- `{topic}`: User input research topic
- `{YYYY-MM-DD}`: Current date
- `{step1_output}`: Complete output from Step 1
- `{time_range}`: User specified time range

**Hard Constraint**: The following prompt must be strictly reproduced, only replacing variables in {xxx}, do not modify structure or wording.

**Host selection rule:** In GitHub Copilot, launch `Web Research Writer`; in Claude Code, launch `web-search-agent`.

Launch 1 host-selected agent (background), **Prompt Template**:
```python
prompt = f"""## Task
Research topic: {topic}
Current date: {YYYY-MM-DD}

Based on the following initial framework, supplement latest items and recommended research fields.

## Existing Framework
{step1_output}

## Goals
1. Verify if existing items are missing important objects
2. Supplement items based on missing objects
3. Continue searching for {topic} related items within {time_range} and supplement
4. Supplement new fields

## Modules
Modules: auto
Read `web-search-modules/ROUTING.md` before any search and route per that file. State the modules you loaded in your output.

## Output Requirements
Return structured results directly (do not write files):

### Supplementary Items
- item_name: Brief explanation (why it should be added)
...

### Recommended Supplementary Fields
- field_name: Field description (why this dimension is needed)
...

### Sources
- [Source1](url1)
- [Source2](url2)
"""
```

**One-shot Example** (assuming researching AI Coding History):
```
## Task
Research topic: AI Coding History
Current date: 2025-12-30

Based on the following initial framework, supplement latest items and recommended research fields.

## Existing Framework
### Items List
1. GitHub Copilot: Developed by Microsoft/GitHub, first mainstream AI coding assistant
2. Cursor: AI-first IDE, based on VSCode
...

### Field Framework
- Basic Info: name, release_date, company
- Technical Features: underlying_model, context_window
...

## Goals
1. Verify if existing items are missing important objects
2. Supplement items based on missing objects
3. Continue searching for AI Coding History related items within since 2024 and supplement
4. Supplement new fields

## Modules
Modules: auto
Read `web-search-modules/ROUTING.md` before any search and route per that file. State the modules you loaded in your output.

## Output Requirements
Return structured results directly (do not write files):

### Supplementary Items
- item_name: Brief explanation (why it should be added)
...

### Recommended Supplementary Fields
- field_name: Field description (why this dimension is needed)
...

### Sources
- [Source1](url1)
- [Source2](url2)
```

### Step 2b: Pin Search Modules (optional)
Read `web-search-modules/ROUTING.md` and propose the module routing for this whole project — the same topic is about to be researched for every item, so routing once here beats every item agent re-deciding it.

Use AskUserQuestion, offering:
- **Auto** *(default)* — each item agent routes itself per ROUTING.md. Correct when items are heterogeneous.
- **Your proposed routing** — name the modules and say in one line why, e.g. `benchmarks, general-web — every item is a model with published eval results`.
- **General web only** — the user just wants a broad sweep.

Only ask when the topic plausibly has a sharper home than `general-web`. Write the answer to `execution.modules` in outline.yaml; omit the key for Auto.

### Step 3: Ask User for Existing Fields
Use AskUserQuestion to ask if user has existing field definition file, if so read and merge.

### Step 4: Generate Outline (Separate Files)
Merge {step1_output}, {step2_output} and user's existing fields, generate two files:

**outline.yaml** (items + config):
- topic: Research topic
- items: Research objects list
- execution:
  - batch_size: Number of parallel agents (confirm with AskUserQuestion)
  - items_per_agent: Items per agent (confirm with AskUserQuestion)
  - output_dir: Results output directory (default: ./results)
  - modules: Search modules pinned for this project, from Step 2b (omit the key entirely to let each agent route itself)

**fields.yaml** (field definitions):
- Field categories and definitions
- Each field's name, description, detail_level
- detail_level hierarchy: brief -> moderate -> detailed
- uncertain: Uncertain fields list (reserved field, auto-filled in deep phase)

### Step 5: Output and Confirm
Locate the root and run the discovery glob per `skills/research/LAYOUT.md` before creating anything.

- If no root exists **and** discovery finds no run folders at all, this is the first `/research` in this project: use `AskUserQuestion` to ask the root name once, default `research/`. If a root already exists, use it silently — never ask again.
- If discovery finds run folders sitting at the cwd root (outside any root), offer to migrate them per LAYOUT.md's migration procedure: list exactly what would move, and move only on explicit confirmation, backfilling one `INDEX.md` entry per moved run from its `outline.yaml` and `report.md`. Declining leaves them in place; either way, continue with this run.
- If `{root}/INDEX.md` already has run entries, ask whether this run descends from one of the open leads (a Map leaf with no `##` section yet). If so, record `Spawned from:` in the new entry and tick that lead's checkbox.
- Create directory: `{root}/{topic_slug}/`
- Save: `outline.yaml` and `fields.yaml` inside it
- Append this run's stub entry to `{root}/INDEX.md` (creating the file if this root has no index yet) — purpose, date, status `outline`, `Spawned from:` if applicable, per LAYOUT.md's format
- Show to user for confirmation

## Output Path
```
{root}/
  INDEX.md
  {topic_slug}/
    ├── outline.yaml    # items list + execution config
    └── fields.yaml     # field definitions
```

## Follow-up Commands
- `/research-add-items` - Supplement items
- `/research-add-fields` - Supplement fields
- `/research-deep` - Start deep research
