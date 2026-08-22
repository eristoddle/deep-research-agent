# Layout

Single source of truth for where research lives and how skills find it — the same role `ROUTING.md` plays for module selection. Every skill's locate step reads this file instead of carrying its own copy of the rule.

Resolve this file project-local first, global second — do NOT assume `~/.claude`:
1. `<project_root>/.claude/skills/research/LAYOUT.md` (APM project-local install)
2. `~/.claude/skills/research/LAYOUT.md` (global install)

## Definitions

- **Run folder** — any directory containing `outline.yaml`.
- **Root** — the run folder's parent directory, when that parent is not the cwd. A run folder sitting directly at the cwd (the legacy layout) has no root, and therefore no index: a skill whose step writes `INDEX.md` **skips that step silently** rather than creating one beside the run folder.
- **`{run_dir}`** — the absolute path to the located run folder. Every path inside a run (`fields.yaml`, `results/`, `report.md`, `generate_report.py`) hangs off it, never off the cwd.

## Tree

```
{root}/                # default name `research/`, asked once at first /research, never configured
  INDEX.md             # the branch record, see below
  {topic_slug}/        # a run folder
    outline.yaml
    fields.yaml
    results/*.json
    report.md
    generate_report.py
```

`outline.yaml`, `fields.yaml`, `results/`, `report.md`, `generate_report.py` are unchanged inside the run folder.

## Discovery

Glob **both** `*/outline.yaml` and `*/*/outline.yaml` from the cwd. The first form finds a legacy root-level run with no migration required; the second finds one nested under a root.

**More than one match is the normal case, not an edge case.** Present the matches, most recently modified first, and ask which one via `AskUserQuestion` — unless the caller already named a run folder, in which case use that one. Never guess when more than one match exists.

## `output_dir`

`execution.output_dir` in `outline.yaml` is relative to the **run folder**, never the cwd. This was always ambiguous; state it explicitly wherever `output_dir` is read.

## INDEX.md

Lives at `{root}/INDEX.md`.

- `## Map` — nested bullets, one per run, showing which run spawned which. A lead nobody has started is a leaf with no `##` section of its own.
- One `##` section per run: purpose line (one sentence); italic meta line `date · N items · depth · status`, status one of `outline` -> `researching` -> `researched` -> `complete`, or `lead` for a Map leaf with no section; optional `Spawned from:` link to the parent run's section; summary body (cap below); `**Leads**` checklist of directions this run surfaced, ticked once a lead becomes its own run.

## Who writes what

Each skill owns its own part; none rewrites another's.
- `/research` appends the stub — purpose, date, status `outline`, `Spawned from:` if applicable.
- `/research-deep` flips status `outline` -> `researching` before the first batch, and `researching` -> `researched` on queue completion. The two are distinct on purpose: a run whose items are all researched but whose report has not been written is neither in progress nor finished, and an index that cannot say so is not worth reading.
- `/research-report` fills the summary body and the `**Leads**` checklist, then flips status `researched` -> `complete`.

## Summary cap

The summary body is capped at **≤3 paragraphs, ≤12 table rows**, then `… N more rows in report.md`. INDEX.md is read whole by every skill that touches it — an uncapped per-entry table (the live consumer's report has 24 rows) makes the whole file unreadable within three runs.

## Migration (offered, never automatic)

When discovery finds run folders at the cwd root with no `{root}/` above them, `/research` **offers** to move them: list exactly what would move, move only on explicit confirmation, then backfill one `INDEX.md` entry per moved run from its `outline.yaml` (purpose, date, item count) and `report.md` if present (summary body), status inferred as `report.md` present -> `complete`, `results/` populated -> `researched`, neither -> `outline`. No other skill triggers migration.
