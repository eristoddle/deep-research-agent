---
name: research-deep
user-invocable: true
description: Read research outline, launch independent agent for each item for deep research. Disable task output.
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task
---

# Research Deep - Deep Research

## Trigger
`/research-deep [quick|standard|deep]`

The optional argument sets the per-item search depth. It overrides `execution.depth` in outline.yaml, which in turn overrides the `standard` default. Resolve `{depth}`, `{searches}`, and `{fetches}` from this table before launching anything:

| Level | Searches | Fetches | Link depth |
|---|---|---|---|
| `quick` | 3 | 4 | 1 |
| `standard` *(default)* | 8 | 12 | 1 |
| `deep` | 20 | 30 | 2 |

State the resolved level before the first batch: `Depth: deep (20 searches / 30 fetches per item).` A `deep` run over many items is expensive and slow — if the level came from outline.yaml rather than the user typing it, say so and confirm before launching.

## Workflow

### Step 1: Auto-locate Outline
Find `*/outline.yaml` file in current working directory, read items list, execution config (including items_per_agent).

### Step 2: Resume Check
- Check completed JSON files in output_dir
- Skip completed items

### Step 3: Batch Execution
- Batch by batch_size (need user approval before next batch)
- Each agent handles items_per_agent items
- Launch web-search-agent (background parallel, disable task output)

**Parameter Retrieval**:
- `{topic}`: topic field from outline.yaml
- `{item_name}`: item's name field
- `{item_related_info}`: item's complete yaml content (name + category + description etc.)
- `{output_dir}`: execution.output_dir from outline.yaml (default: ./results)
- `{fields_path}`: absolute path to {topic}/fields.yaml
- `{output_path}`: absolute path to {output_dir}/{item_name_slug}.json (slugify item_name: replace spaces with _, remove special chars)
- `{depth}` / `{searches}` / `{fetches}`: resolved from the depth table above.
- `{validator_path}`: absolute path to `validate_json.py`. Resolve it in this order and use the first that exists — do NOT assume `~/.claude`, which APM never writes to:
  1. `<project_root>/.claude/skills/research/validate_json.py`  (APM project-local install — the normal case)
  2. `~/.claude/skills/research/validate_json.py`  (global install)
  If neither exists, tell the user the skill is not fully installed and stop; do not write a replacement validator.

**Hard Constraint**: The following prompt must be strictly reproduced, only replacing variables in {xxx}, do not modify structure or wording.

**Prompt Template**:
```python
prompt = f"""## Task
Research {item_related_info}, output structured JSON to {output_path}

## Field Definitions
Read {fields_path} to get all field definitions

## Search Budget
Depth level: {depth}. Hard limits for this item: {searches} WebSearch calls, {fetches} WebFetch calls, one fetch per URL.
Use WebSearch and WebFetch only. No browser automation, no downloads, no cloning, no self-written scripts.
Stop when the fields are answered. Mark whatever is still open as [uncertain] rather than spending more budget on it.

## Output Requirements
1. Output JSON according to fields defined in fields.yaml
2. Mark uncertain field values with [uncertain]
3. Add uncertain array at the end of JSON, listing all uncertain field names
4. All field values must be in English

## Output Path
{output_path}

## Validation
After completing JSON output, run validation script to ensure complete field coverage:
python3 {validator_path} -f {fields_path} -j {output_path}
Task is complete only after validation passes.
"""
```

**One-shot Example** (assuming researching GitHub Copilot):
```
## Task
Research name: GitHub Copilot
category: International Product
description: Developed by Microsoft/GitHub, first mainstream AI coding assistant, ~40% market share, output structured JSON to {project_dir}/results/GitHub_Copilot.json

## Field Definitions
Read {project_dir}/fields.yaml to get all field definitions

## Search Budget
Depth level: standard. Hard limits for this item: 8 WebSearch calls, 12 WebFetch calls, one fetch per URL.
Use WebSearch and WebFetch only. No browser automation, no downloads, no cloning, no self-written scripts.
Stop when the fields are answered. Mark whatever is still open as [uncertain] rather than spending more budget on it.

## Output Requirements
1. Output JSON according to fields defined in fields.yaml
2. Mark uncertain field values with [uncertain]
3. Add uncertain array at the end of JSON, listing all uncertain field names
4. All field values must be in English

## Output Path
{project_dir}/results/GitHub_Copilot.json

## Validation
After completing JSON output, run validation script to ensure complete field coverage:
python3 {project_dir}/../.claude/skills/research/validate_json.py -f {project_dir}/fields.yaml -j {project_dir}/results/GitHub_Copilot.json
Task is complete only after validation passes.
```

### Step 4: Wait and Monitor
- Before launching a batch, print the plan: `Batch N/M — items X-Y of Z, depth {depth} (<={searches} searches + <={fetches} fetches per item)`
- Wait for current batch to complete
- After each batch, print cumulative progress: `Done A/Z items. Remaining: B. Failed: C.`
- Launch next batch

**Progress is mandatory, not optional.** A run with no visible progress cannot be judged as stuck versus working, and will get killed. Never let a batch run silently.

### Step 5: Summary Report
After all complete, output:
- Completion count
- Failed/uncertain marked items
- Output directory

## Agent Config
- Background execution: Yes
- Task Output: Disabled (agent has explicit output file when complete)
- Resume support: Yes
