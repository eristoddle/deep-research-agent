---
name: research-harvest
user-invocable: true
description: Tally which sources supported fields across research runs and write a reviewable candidate list. Hand-invoked only.
allowed-tools: Bash, Read, Write, Glob, AskUserQuestion
---

# Research Harvest - Source Promotion Candidates

## Trigger
`/research-harvest [run-folder-name]`

**Never invoked automatically** by `/research-deep` or `/research-report`. Runs routinely stop before the report step, so anything hanging off `/research-report` would never fire for them; and a prompt printed after every run is one the user learns to dismiss. This skill only runs when asked.

## Workflow

### Step 1: Locate Scope
Locate the root per `skills/research/LAYOUT.md`'s discovery rule — do not restate the rule here. With no run named, the scope is the whole root. With a run named, locate that run folder (skip disambiguation if it names one directly) and narrow the scope to it alone.

### Step 2: Resolve the Script
Resolve `harvest_sources.py` in this order and use the first that exists:
1. `<project_root>/.agents/skills/research/harvest_sources.py` (Copilot project-local install)
2. `<project_root>/.claude/skills/research/harvest_sources.py` (Claude project-local install)
3. `~/.agents/skills/research/harvest_sources.py` (Copilot user install)
4. `~/.claude/skills/research/harvest_sources.py` (Claude user install)

If none exists, tell the user the skill is not fully installed and stop — do not hand-write a substitute tally.

### Step 3: Run the Tally
`python3 {harvest_script_path} --root {root}`, or `--run {run_dir}` when a run was named. The script is read-only; it prints a bounded summary and writes nothing.

### Step 4: Report the Empty Cases Plainly
Carry the script's own distinction through to the user instead of printing "no candidates found":
- All scanned runs predate source capture -> say so in those words.
- Sources were captured and none reached the threshold -> say so in those words.
- No run has been researched yet (outline only, no results to read) -> say that. It is **not** the same as predating capture, and reporting it as such tells the user the opposite of the truth.
- A mixed scan -> say each case that applies, with the counts the script reported.

### Step 5: Write `CANDIDATES.md`
Resolve the path: prefer `.agents/web-search-modules-local/CANDIDATES.md`; use `.claude/web-search-modules-local/CANDIDATES.md` instead only when that legacy directory already exists and the `.agents` one does not — the same preference order `ROUTING.md` step 0 uses for local modules. Create the directory when neither exists.

**Read the existing file first, if one exists.** Any entry under `## Candidates` that the human has ticked (`- [x]`) or struck through (`~~like this~~`) is a disposition, not an open candidate. Move each such entry, in its ticked/struck form, into `## Dispositioned` if it is not there already. This is what stops a rejected source from returning as a fresh candidate on every later harvest — never delete a dispositioned line, on this or any later run.

Then write the file whole, in this shape:
1. A header: the date, the scope scanned (whole root or the named run), the threshold used (`--min-runs` / `--min-field-runs`), and one line noting that only **parameterized** modules (D1) can absorb a source — fixed-site and open-query modules have nothing to promote into.
2. `## Candidates` — one unticked `- [ ]` line per qualifying source from Step 3's output, with its URL, run count, field-support count, and the fields it supported. **Skip any URL that already has a disposition recorded**, even if it still qualifies this time — that is the rule the previous paragraph exists to enforce.
3. `## Dispositioned` — every disposition ever recorded (carried over from the read in this step, plus anything newly moved), never trimmed.

### Step 6: No Module Attribution
This skill never attributes a candidate to a module and never edits a module file. Discovery stays automatic; which module a source serves, and whether to promote it at all, is the human's call (D17).
