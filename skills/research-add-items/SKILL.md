---
name: research-add-items
user-invocable: true
description: Add items (research objects) to existing research outline.
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---

# Research Add Items - Supplement Research Objects

## Trigger
`/research-add-items`

## Workflow

### Step 1: Auto-locate Outline
Locate the run folder per `skills/research/LAYOUT.md`'s discovery rule, auto-read `outline.yaml`.

### Step 2: Get Supplement Sources in Parallel
Simultaneously:
- **A. Ask user**: What items to supplement? Any specific names?
- **B. Ask if Web Search needed**: Launch agent to search for more items?

### Step 3: Merge and Update
- Append new items to outline.yaml
- Display to user for confirmation
- Avoid duplicates
- Save updated outline

## Output
Updated `{run_dir}/outline.yaml` file (in-place modification) — `{run_dir}` is the run folder located in Step 1, never a cwd-relative path
