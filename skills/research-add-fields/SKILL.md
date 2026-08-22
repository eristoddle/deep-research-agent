---
name: research-add-fields
user-invocable: true
description: Add field definitions to existing research outline.
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---

# Research Add Fields - Supplement Research Fields

## Trigger
`/research-add-fields`

## Workflow

### Step 1: Auto-locate Fields File
Locate the run folder per `skills/research/LAYOUT.md`'s discovery rule, then read `fields.yaml` from inside it (no separate glob for `fields.yaml`).

### Step 2: Get Supplement Source
Ask user to choose:
- **A. User direct input**: User provides field names and descriptions
- **B. Web Search**: Launch agent to search common fields in this domain

### Step 3: Display and Confirm
- Display suggested new fields list
- User confirms which fields to add
- User specifies field category and detail_level

### Step 4: Save Update
Append confirmed fields to fields.yaml, save file.

## Output
Updated `{run_dir}/fields.yaml` file (in-place modification, requires user confirmation) — `{run_dir}` is the run folder located in Step 1, never a cwd-relative path
