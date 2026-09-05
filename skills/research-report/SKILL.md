---
name: research-report
user-invocable: true
description: Summarize deep research results into markdown report, cover all fields, skip uncertain values.
allowed-tools: Read, Write, Glob, Bash, AskUserQuestion
---

# Research Report - Summary Report

## Trigger
`/research-report`

## Workflow

### Step 1: Locate Results Directory
Locate the run folder per `skills/research/LAYOUT.md`'s discovery rule, read topic and output_dir config. `{run_dir}` below is the absolute path to that folder — every path in this skill hangs off it, never off the cwd, which is one level up once runs live under a root.

### Step 2: Scan Optional Summary Fields
Read all JSON results, extract fields suitable for TOC display (numeric, short metrics), e.g.:
- github_stars
- google_scholar_cites
- swe_bench_score
- user_scale
- valuation
- release_date

Use AskUserQuestion to ask user:
- Which fields to display in TOC besides item name?
- Provide dynamic options list (based on actual fields in JSON)

### Step 3: Generate Python Conversion Script
Generate `generate_report.py` in `{run_dir}/`, script requirements:
- Read all JSON from output_dir
- Read fields.yaml to get field structure
- Cover all field values from each JSON
- Skip fields with values containing [uncertain]
- Skip fields listed in uncertain array
- Treat unreachable as an internal JSON field during ordinary field and category traversal, not as an uncertain field
- Collect unreachable entries from all item results, deduplicate them by the full source + url + reason tuple, and emit a reader-visible `## Unreachable sources` section with each entry's source, URL, reason, and affected item names
- Treat sources as an internal JSON field during ordinary field and category traversal, not as an uncertain field. Unlike unreachable, do **not** emit a sources section by default — only add one, reading the sources array across item results, if the user's invoking prompt asks for sources or citations in natural language. There is no flag or config key for this; it is decided by what the prompt says, per run
- Generate markdown report format: Table of contents (with anchor links + user-selected summary fields) + Detailed content (by field category)
- Save to `{run_dir}/report.md`

**TOC Format Requirements**:
- Must include every item
- Each item displays: number, name (anchor link), user-selected summary fields
- Example: `1. [GitHub Copilot](#github-copilot) - Stars: 10k | Score: 85%`

#### Script Technical Requirements (Must Follow)

**1. JSON Structure Compatibility**
Support two JSON structures:
- Flat structure: Fields directly at top level `{"name": "xxx", "release_date": "xxx"}`
- Nested structure: Fields in category sub-dict `{"basic_info": {"name": "xxx"}, "technical_features": {...}}`

Field lookup order: Top level -> category mapping key -> Traverse all nested dicts

**2. Category Multi-language Mapping**
fields.yaml category names and JSON keys can be any combination (CN-CN, CN-EN, EN-CN, EN-EN). Must establish bidirectional mapping:
```python
CATEGORY_MAPPING = {
    "Basic Info": ["basic_info", "Basic Info"],
    "Technical Features": ["technical_features", "technical_characteristics", "Technical Features"],
    "Performance Metrics": ["performance_metrics", "performance", "Performance Metrics"],
    "Milestone Significance": ["milestone_significance", "milestones", "Milestone Significance"],
    "Business Info": ["business_info", "commercial_info", "Business Info"],
    "Competition & Ecosystem": ["competition_ecosystem", "competition", "Competition & Ecosystem"],
    "History": ["history", "History"],
    "Market Positioning": ["market_positioning", "market", "Market Positioning"],
}
```

**3. Complex Value Formatting**
- list of dicts (e.g., key_events, funding_history): Format each dict as one line, separate kv with ` | `
- Normal list: Short lists joined with comma, long lists displayed with line breaks
- Nested dict: Recursive formatting, display with semicolon or line breaks
- Long text strings (over 100 chars): Add line breaks `<br>` or use blockquote format for readability

**4. Extra Fields Collection**
Collect fields that exist in JSON but not defined in fields.yaml, put in "Other Info" category. Note to filter:
- Internal fields: `_source_file`, `uncertain`, `unreachable`, `sources`
- Nested structure top-level keys: `basic_info`, `technical_features` etc.
- `uncertain` array: Display each field name on separate line, don't compress into one line

**5. Uncertain Value Skipping**
Skip conditions:
- Field value contains `[uncertain]` string
- Field name is in `uncertain` array
- Field value is None or empty string

`unreachable` entries are not uncertain values and must not be skipped entirely: render the dedicated, deduplicated `## Unreachable sources` section after ordinary field/category traversal.

`sources` entries are likewise not uncertain values, but unlike `unreachable` they do **not** render by default. Render a sources section only when the user's prompt for this report asked for sources or citations, in natural language — never introduce a flag or option to control this.

### Step 4: Execute Script
Run `python {run_dir}/generate_report.py`

### Step 5: Update the Index
Fill this run's entry in `{root}/INDEX.md` per `skills/research/LAYOUT.md`'s format and summary cap:
- Copy the report's intro paragraphs and headline table into the entry's summary body, capped at ≤3 paragraphs and ≤12 table rows, then `… N more rows in report.md` — `report.md` itself is untouched and stays the full record
- Flip this run's status from `researched` to `complete`
- Use `AskUserQuestion` to ask which directions this run surfaced; write the answers as the entry's `**Leads**` checklist, and add each as a new `lead` leaf under this run in the `## Map`

## Output
- `{run_dir}/generate_report.py` - Conversion script
- `{run_dir}/report.md` - Summary report
- `{root}/INDEX.md` - this run's entry filled in (summary, status, Leads); a legacy run with no root has no index, so this step is skipped silently
