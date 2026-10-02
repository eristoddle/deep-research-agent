# Grill prep for the BMAD deep-recon lessons

**What this file is.** Fact-finding gathered ahead of the grill sessions (the round-by-round design interviews) for the open items in [bmad-deep-recon-lessons.md](bmad-deep-recon-lessons.md): #2, #3, #4, #6, #7, #9, #10, #11, plus the remaining questions on #8 ([Q7](../questions/Q7-question-major-details.md), items 3–7). **It decides nothing.** Every "Suggested answer" below is a starting point for Stephan to accept, change or throw out. Written 2026-10-01.

**Sources used.**

- **BMAD deep-recon, local copy:** `/Users/eristoddle/Dropbox/node/veneer/.claude/skills/bmad-deep-recon/` (BMAD version 6.12.0 per `veneer/_bmad/_config/manifest.yaml`). Checked against the pinned GitHub commit [`5e33d3c`](https://github.com/bmad-code-org/BMAD-METHOD/tree/5e33d3c03ba53187a40ab679d5479cdd4b6ac2fb/skills/bmad-deep-recon): `references/run.md`, `verification.md`, `process.md`, `selection.md` and `types/technical.md` are byte-identical. `SKILL.md` and `references/synthesis.md` differ only in setup and output-language wording, nothing that touches these items. File paths below are relative to the skill folder.
- **The Veneer run:** `veneer/_bmad-output/planning-artifacts/research/technical-vs-code-and-obsidian-plugin-apis-2026-09-25/` (called "the run folder" below), plus the reconciliation output it produced at `veneer/docs/plugin-api-reference.md`.
- **This repo** at commit `6e30d89`. Line numbers are as of that commit.
- **Live consumer fixture:** `writing-model-research/research/llm-writing-benchmark-landscape/` (spot-checked only).

**Two rules every item is measured against** (from the lessons file): the *flexibility rule* (everything opt-in or additive; a run that uses none of it behaves exactly as today; nothing forces a report) and the *credit rule* (when an item ships, credit BMAD in `README.md` in the same change). The credit line already exists at `README.md:11`, but it reads "Some **trust features** are adapted from…". Items #7–#11 are not trust features, so the first of them to ship probably has to widen that sentence, not just add an Additions entry.

**A finding that cuts across several items:** the Veneer run's best-known sections, **API inventory**, **Design lessons** and **Leads & gaps**, are *not prescribed by the BMAD skill*. The skill's return contract for a researcher (`references/run.md`, "The fan-out") asks only for "findings as claims, each with `{claim, source, publisher, pub_date, accessed, confidence, class}`, plus leads worth chasing and what it looked for and could not find." The inventory table and the design-lessons list were shaped by the brief the lead agent wrote for that run, and that brief was not saved anywhere in the run folder. So for #7 and #9 there is no BMAD wording to copy, only the run's output to imitate.

---

## #2 — Freshness windows per field, and a re-check list

### How BMAD does it

- **Windows live per research type, per claim class**, not per question. Each type pack has one line, e.g. `types/technical.md`: "**Freshness:** versions & compatibility ≤ 1 mo · ecosystem signals ≤ 6 mo · landscape ≤ 12 mo (AI-adjacent ≤ 3 mo) · patterns ≤ 2 yr." `types/market.md` and `types/competitive.md` carry "pricing & feature claims ≤ 3 mo". (The lessons file's example list mixes lines from two different packs; that's fine as an example, but no single pack says all three.)
- **A "class" is a label the lead puts on each claim**, logged one line per claim in `.memlog.md` (the run's append-only log) in a machine-readable shape: `ref=[n] status=<…> class=<class> pub=<YYYY-MM> — <claim>` (`references/run.md`, "Synthesize the dimension", step 3).
- **The re-check list is computed by a script**, never written by hand: `scripts/recon_kit.py staleness <claims.json> --windows '<map>'` takes `[{claim, class, pub_date}]` plus a months-per-class map, returns each claim's re-check date, a `stale` flag, `earliest_recheck`, and the classes that had no window (`recon_kit.py:173-209`). It exits 1 if anything is already stale. `references/synthesis.md` item 8 renders the result as the report's last section, the **Staleness map**, "closing by noting the earliest."
- **The Veneer run did not follow the rule as written.** Its `.memlog.md` line 40: "(assumption) Staleness dated from verification date (2026-09-25) rather than source pub dates, since version facts are historical and the question is when to re-check current docs." Most sources had no publication date anyway: in digest `d2-actions-r1-1.md`, 13 of 14 sources are listed as `undated` (official docs pages rarely carry one). The rendered map (`research.md:214-239`) shows the result: "**Earliest re-check: 2026-10-01**, covering the Obsidian and VS Code version facts", with rows like `| 2026-10-01 | version | [2] VS Code 1.74 contributions imply activation events |`. That re-check date is today.

### What it would touch here

- `skills/research-deep/SKILL.md` — the hard-constrained item template (lines 59-102) and its one-shot example (104-149), in lockstep. Output Requirement 8 (line 85, and 133 in the example) says each `sources` entry has "**exactly** source, url, and fields keys"; adding a date breaks "exactly". The sample `sources` array (88-92 and 136-140) would need dates too, or it teaches the old shape.
- `agents/web-search-agent.md:78` repeats the "exactly `source`, `url`, and `fields` keys" rule. It must change in the same edit or the two prompts contradict each other.
- `skills/research/SKILL.md:145-149` defines what `fields.yaml` holds (name, description, detail_level). A per-field window (e.g. `fresh_for: 3mo`) would be added here. `validate_json.py`'s `load_fields_yaml` (lines 25-40) ignores unknown keys, so an extra key does no harm to the gate.
- `skills/research-report/SKILL.md` Step 3 (lines 31-93) is where a re-check list would be rendered. Note that the report is generated by a script the report skill writes per run (`generate_report.py`), so date arithmetic belongs in that script, which is deterministic and fine for it.
- Existing nearby concept: `/research` Step 2 already asks the user for a **time range** for the search ("last 6 months, since 2024, unlimited", `skills/research/SKILL.md:25`). That is a filter on what to search, not an expiry on answers. Different job, easy to confuse in the grill.
- `validate_json.py` exit code: nothing here needs to touch it. A missing date should not fail a run (the gate is for missing required fields, line 154).
- Distinct from **D12** (`PLAN.md:177`), which is about expiring *access findings inside modules*, not expiring *answers*.

### Overlaps

- **#3 and #11** change the same Output Requirements list and the same agent lines; doing #2's source-date piece in the same edit saves one lockstep pass.
- **#4 (Process):** BMAD's import step records "when (ask if not evident — production date drives staleness)". An imported report needs the same date field.
- **#8 digests:** a digest's `## Sources` section could carry dates in prose with no JSON change.

### Questions the grill needs

1. Which date should the re-check count from: the source's publication date, the date the agent read it, or whichever exists? Suggested answer: the access date, always recorded, with the publication date as optional. The Veneer run had to fall back to the access date because docs pages are undated, so building on publication date alone would leave most rows blank.
2. Where should the window live: on each field in `fields.yaml`, as a default in a search module, or both? Suggested answer: on the field, optional, no module default for now. A module default adds a second place to look and the lessons file only says "possibly".
3. Should the dates go inside each `sources[]` entry (one more key) or somewhere else? Suggested answer: inside the entry, since `sources[].fields` already ties a source to fields, so a field's age is derivable from its sources without a new structure.
4. Is the re-check list part of the default report, or only when asked? Suggested answer: only when the run's `fields.yaml` declares at least one window, which keeps every existing run's report unchanged (flexibility rule).
5. Does anything ever act on a stale flag (a "refresh" that re-runs only stale fields), or is the list just for the reader? Suggested answer: list only for now; BMAD's Refresh intent is a separate feature and nothing here asked for it.
6. Should the window use BMAD's unit style (`1mo`, `2yr`) or a plain number of months? Suggested answer: months as a number, which is what `recon_kit.py` itself converts to.

### Facts I could not establish

- No result file on this machine that I checked carries `sources[]` yet: the live fixture's 24 results predate source capture (0 files with `"sources"` or `"unreachable"`), so there is no real data to test a date field against.
- How often the item agent can actually find a publication date for typical sources here. Only the Veneer sample (13 of 14 undated) exists.

---

## #3 — A `disputed` marker, separate from `uncertain`

### How BMAD does it

- **"Disputed" is a verification outcome, assigned after research by a separate checker**, not something the researcher writes. `references/verification.md` defines four outcomes per claim: verified, "**disputed** (independent sources materially disagree — report both figures, both cited; never average)", unverified, overturned. The checker is "fresh-context verifier subagents reading digest files". At the default `normal` level it only spot-checks the few load-bearing claims per dimension.
- **The independence definition** (`references/verification.md`, Levels): "**Independent** means a different publisher with different underlying data or reporting — not a syndication, quote, or republication of the first source, and not the same vendor's marketing in two places. An imported report counts as one publisher regardless of how many sources it cites internally; two imports from different tools agreeing is genuine confirmation, and their disagreement is a finding."
- **The Veneer example:** one disputed claim. `.memlog.md:23`: `ref=[46] status=disputed class=version pub=2026-01 — Obsidian SecretStorage backend: OS keychain vs local storage`. In the report (`research.md:115`, under Open questions): "**Obsidian SecretStorage backend (disputed):** one reading of the docs says OS keychain, another says local storage keyed to the vault [46][98]. Matters only if Veneer copies its shared-secret model." Note the run is internally inconsistent: `digests/verification-r1.md:5` says "0 disputed", while the memlog and the report frontmatter (`claims_disputed: 1`) say 1. The dispute was found during the verification pass, not by the researcher.

### What it would touch here

- **There is no separate verification pass in this package.** The item agent would have to mark its own disputes while researching. That is a different mechanism from BMAD's, and worth saying out loud in the grill.
- `agents/web-search-agent.md:132` (shipped in #5): "Resolve conflicts by recency, consistency with established facts, and publisher quality — never by averaging; report both values and mark the field `[uncertain]`." This line is exactly what #3 would change: today a dispute is deliberately routed into `[uncertain]`.
- `agents/web-search-agent.md:130` already has half of the independence rule ("Many domains repeating one upstream report count as one publisher"). Missing: "not the same vendor's marketing in two places" and the import rule (which only matters if #4 ships).
- `skills/research-deep/SKILL.md` item template Output Requirements 2-3 (lines 79-80) and the example (126-128), in lockstep.
- `skills/research/validate_json.py`: `_is_answered` (lines 86-92) treats any string containing `[uncertain]` as unanswered. A `[disputed]` value would count as **answered**, which means the source-trace warning from #1 would then demand a source for it. That is arguably correct (both sides should be cited). The PASS/FAIL gate (line 154) only checks that required fields are present, so a disputed marker cannot flip the exit code unless someone makes it. It should stay that way.
- If disputes get their own array (like `uncertain[]`), it must join `_SKIP_KEYS` at `validate_json.py:22`, or the validator will list it as an "extra field" (an `[INFO]` line, not a failure, but noise).
- `skills/research-report/SKILL.md`: the description (line 4) says "skip uncertain values", and the skip rules (lines 87-88) key on `[uncertain]`. A disputed value would need its own rendering rule (show both values), and a new array would join the "internal fields" list (line 81).

### Overlaps

- **#11 (leads):** BMAD gives contradictions priority as leads to chase next ("Contradictions get priority", `references/run.md`, Rounds). A disputed field is a natural lead.
- **#2 and #11:** same template list, same agent lines, same `_SKIP_KEYS`. One lockstep edit could carry all three.
- **#4:** the import-counts-as-one-publisher rule only becomes live if Process ships.

### Questions the grill needs

1. Should the item agent mark disputes itself, given there is no verification pass here? Suggested answer: yes; the agent already sees both values when it hits a conflict, and adding a verifier is a much larger change no one has asked for.
2. Inline marker in the value (`[disputed]`), a separate `disputed[]` array, or both, the way `uncertain` works today? Suggested answer: both, mirroring `uncertain` exactly, because the validator and report already honor "inline or in the array" for uncertain (`validate_json.py:87-89`), and a parallel shape is least surprising.
3. What does a disputed value look like? Suggested answer: both values in the field text, each with its own source in `sources[]` listing that field, so the existing source trace checks both sides are cited.
4. Is a disputed field "answered" for the source-trace warning? Suggested answer: yes (see the validator note above); the warning is advisory, so nothing gates on it.
5. Does `agents/web-search-agent.md:132` change from "mark the field `[uncertain]`" to "mark it `[disputed]`", and does that change apply to non-JSON (prose) output too? Suggested answer: change it for JSON output; for prose output say "report both values, both cited" without a marker.
6. Copy the full independence definition into the agent now, or only the vendor-marketing clause? Suggested answer: only the vendor-marketing clause now; the import clause waits for #4.
7. Does an old run without the marker read differently after this ships? Suggested answer: no; old disputes stay `[uncertain]`, which is still true, just less specific.

### Facts I could not establish

- How often disputes actually happen in this package's runs. No run here records them separately, so I cannot say whether the new marker would see real use.

---

## #4 — Draft then Process: an outside deep-research product does the gathering

### How BMAD does it

- **Draft** (`references/draft.md`): ask which outside tool the prompt is for, then compose "the dimensions as explicit research questions pruned to the decision, the freshness bars as recency requirements, the two-source expectation for its critical claim classes, the audience, the source policy" plus "a **non-negotiable citation demand**: every claim with source URL and publication date, contrary evidence reported, gaps admitted rather than padded. Structure the requested output so Process can extract it cleanly (findings per dimension, a source list)." The prompt is saved as `brief.md` in the run folder, whose name is computed deterministically (`recon_kit.py slug`) so the returned report lands in the same folder.
- **Process** (`references/process.md`): (1) copy the original report into `imports/` untouched; (2) record provenance, "what produced it (which tool or firm), when (ask if not evident — production date drives staleness)"; (3) a fresh-context subagent extracts "every claim bearing on the decision into digest files", in the same claim shape as a native run, "keeping the original's citations (the cited source is the publisher; the import is the via)"; (4) check which dimensions are covered and which are open; (5) write the summary; open dimensions get "a one-line route: draft a follow-up prompt, or a targeted Run on the gap."
- `SKILL.md` On Activation step 4 offers the choice up front: "**Run** it here now, or **Draft** a prompt for a deep-research tool they subscribe to — often cheaper and a strong gatherer… State the trade honestly (tokens and minutes here vs. one manual round-trip there)."
- **No Veneer example:** the run's `imports/` folder is empty; it used Run mode.

### What it would touch here

- A new skill under `skills/` (README Additions entry, credit line). It reuses `outline.yaml` and `fields.yaml` as inputs; nothing in the existing item template needs to change if the new skill writes `results/<item>.json` itself.
- **The validator gate:** results written by Process must pass `validate_json.py` like any other result. The gate must not be relaxed for imports; a field the import did not cover becomes `[uncertain]`, same as a native run.
- **`sources[]` shape** (`skills/research-deep/SKILL.md:85`, `agents/web-search-agent.md:78`): "exactly source, url, fields". BMAD's "the import is the via" has nowhere to go without a fourth key, or the import has to be recorded elsewhere (e.g. a file note).
- **`unreachable[]`** has no meaning for an import (nothing was fetched). The skill would write it empty or omit it; `validate_json.py` does not require it.
- **`skills/research/LAYOUT.md:30`** lists what lives inside a run folder. An `imports/` folder and a `brief.md` would be new entries.
- **Index status:** `LAYOUT.md:53` gives the `outline` → `researching` → `researched` flips to `/research-deep` only. A Process run would need the same flips, or `/research-report` will not see the run as ready.
- **Context discipline:** an outside deep-research report can be very long. If the main conversation reads it whole to extract fields, that is exactly the unbounded payload the global rules warn about. BMAD sends extraction to a fresh subagent for this reason. Here the only packaged agent is `web-search-agent`, whose allowlist (`WebSearch, WebFetch, Read, Write, Bash`) does allow reading a file and writing JSON, but whose prompt is about searching.
- **Budget table:** not involved; no searching happens in Process.

### Overlaps

- **#8 (question-major):** outside deep-research products naturally write by *question* across subjects ("compare X and Y on Z"), not one subject at a time. A drafted prompt per question, processed into a digest, may fit the D20 shape better than one prompt per item.
- **#2:** the import's production date is the obvious freshness anchor.
- **#3:** BMAD's rule that an import counts as one publisher.
- **#9:** an external report often contains inventory-like lists.

### Questions the grill needs

1. Is this one skill with two modes (draft a prompt; process a report), or two skills? Suggested answer: one skill, two modes, matching BMAD's loop and keeping the skill count down.
2. One external report per item, or one report for the whole run that the skill splits into per-item results? Suggested answer: allow both, but default to one per run; twenty copy-paste round trips for a twenty-item run defeats the point of saving effort.
3. Who does the extraction: the main conversation, or a subagent? Suggested answer: a subagent via `web-search-agent` with a Process-specific task prompt, so a long report never enters the planning context. This needs a check that the agent's prompt does not push it to start searching.
4. Where does the provenance (which tool, when) live? Suggested answer: a small file in the run folder (e.g. next to the copied original), not a fourth `sources[]` key, so the hard-constrained source shape stays as is.
5. Should the drafted prompt demand output in the shape of `fields.yaml` (field-by-field), or in free prose? Suggested answer: field-by-field per item with a URL per claim, as BMAD does for its dimensions, which makes extraction mechanical.
6. Does Process run `validate_json.py` and flip index status the same way `/research-deep` does? Suggested answer: yes on both; otherwise the downstream report and harvest steps treat the run as unresearched.
7. Do gaps left by an import get a route, like BMAD's "draft a follow-up prompt, or a targeted Run on the gap"? Suggested answer: yes; the route here is `/research-deep` on the same run folder, which skips completed items already (Step 2, Resume Check).

### Facts I could not establish

- No worked example of BMAD's Process in the Veneer run (empty `imports/`).
- What a typical ChatGPT/Gemini/Perplexity deep-research report looks like for a field-matrix prompt; I did not run one.
- Whether `/research-deep`'s Resume Check would treat imported results as "completed" — it checks for existing JSON files, so probably yes, but unverified.

---

## #6 — A "pick one" mode for the report

### How BMAD does it

`references/selection.md` (13 lines), layered over any research type when the decision is "choose between candidates":

1. **Requirements frame.** "Split hard gates from weighted preferences and set the weights. Sources: the project itself (brief, PRD, spine, …, codebase) and the user — web research does not set requirements. **Agree the frame before any candidate research runs**."
2. **Candidate screen.** "Screen to 3–5 finalists; record the cuts and why. Screening sources ≤ 6 months old."
3. **Evidence per criterion.** "Cite every contested cell; where vendor claims and independent experience diverge, the divergence is a finding."
4. **Cost & lock-in.** Total cost and "the cost of leaving".
5. **Verdict.** "The weighted decision matrix — show the scoring, not just totals; a matrix the user can re-weight is worth more than a verdict they must trust. Then: the pick; the named runner-up and the conditions under which it wins instead; the strongest argument against the pick…; the cheapest reversibility hedge."

Plus extra two-source classes (pricing, performance numbers, "any cell that decides between the top two finalists") and "a selection report older than two quarters should be refreshed."

**No Veneer example:** that run used the default "explore" shape, not select. Its closest output is the Recommendations table (`research.md:97-110`, columns `# | Recommendation | Feeds | Confidence basis`).

### What it would touch here

- `skills/research-report/SKILL.md`. Today the report skill writes a **deterministic conversion script** (`generate_report.py`, Step 3, lines 31-93) and asks one question (which fields go in the table of contents, Step 2, lines 18-29). Scoring prose cells against criteria is *judgment*, which a conversion script cannot do. A select mode therefore adds an agent judgment step the report skill does not have now.
- Many fields are prose (`detail_level: moderate|detailed`), not numbers, so "weights over fields" means someone (the model) turns prose into scores. That is where the grill should spend time.
- BMAD sets gates and weights **before** research. Here that would touch `/research` (`skills/research/SKILL.md` Step 4, lines 133-149, where `outline.yaml` and `fields.yaml` are written), not only the report. A report-only version would set weights after the fact, which BMAD explicitly avoids.
- The live fixture shows a per-item stand-in already exists: `llm-writing-benchmark-landscape/fields.yaml:99-102` declares a required `verdict` field ("Direct recommendation: include in the comparison portfolio, check occasionally, or skip — and one sentence of why"). Per-item verdicts are not a cross-item pick, but they show the pull.
- Flexibility rule: fine if it is an optional mode of `/research-report`; nothing else changes. "Nothing forces a report" means the select logic must not become the only way to get a pick (e.g. a task-driven run might want the matrix without a full report).

### Overlaps

- **#7:** a pick answers a decision; without a stated decision there is nothing to weigh against.
- **#10:** BMAD's requirements come from project files, which is the same "named project files" input #10 needs. Both obey the firewall: project files set the criteria, never the facts.
- **#8:** comparison digests already hold every subject side by side; a pick over digests may be easier than over grid cells.
- **#3:** a disputed cell between the top two finalists is exactly what BMAD asks to double-source.

### Questions the grill needs

1. Are gates and weights set before research (in `/research`), after (in `/research-report`), or either? Suggested answer: either, recorded in `outline.yaml` when set early, asked at report time when not; the early path is better but the late path keeps it usable on existing runs.
2. Who turns prose cells into scores? Suggested answer: the model, with every score shown next to the cell text and its source, so the reader can disagree cell by cell. That is BMAD's "show the scoring, not just totals."
3. Do gates cut items from the report or only mark them? Suggested answer: mark and keep a "cut, and why" list, as BMAD's screen step does; nothing silently disappears.
4. Is the verdict section (pick, runner-up and when it wins, strongest argument against, cheapest way to reverse) copied whole? Suggested answer: yes, it is short and every line answers a question a reader would ask.
5. Does the pick live in `report.md` or in its own file? Suggested answer: its own file (e.g. `pick.md`), so it exists even when no report is wanted, which serves the task-driven use the flexibility rule protects.
6. Is a "select" shape worth building before a real project asks for it? Suggested answer: worth asking honestly; D2's spirit (no new modules until a real project needs one) may apply to features too.

### Facts I could not establish

- No select-shape run exists in the Veneer folder or in this package's consumers that I checked, so there is no worked example of a matrix from either side.

---

## #7 — A decision line that every agent receives

### How BMAD does it

- **The decision is the centre of the skill.** `SKILL.md` Overview: "Every engagement serves a **decision** — enter a market, pick a stack, scope a product, commit to a domain — and is shaped by it from the first question to the final artifact."
- **It is written into the run** three ways: the report template frontmatter `decision: '{decision}'` and a body line "**Decision this research serves:** {decision}" (`assets/research.template.md`); the memlog init (`--field decision="<decision>"`, `references/run.md`, plan gate); and every researcher's brief contains "the questions it owns, the decision they serve, and the topic" (`references/run.md`, "The fan-out").
- **The report binds recommendations to it** (`references/synthesis.md` item 5): "each bound to the decision and… to the downstream artifact that consumes it".
- **"Design lessons" is not in the skill.** No BMAD file mentions a lessons section. In the Veneer run it appears in every digest (e.g. `digests/d2-actions-r1-1.md:70-77`): "Copy VS Code's declaration/implementation split…", "Do not let plugins ship default hotkeys silently…", "Auto-namespace command IDs by plugin ID as Obsidian does [8]; VS Code relies on convention." Each lesson carries citations. The run's decision line (`.memlog.md` frontmatter): "Which plugin mechanics/APIs Veneer borrows, builds now, or keeps as future candidates".

### What it would touch here

- `outline.yaml` gains an optional `decision:` key. Written by `/research` Step 4 (`skills/research/SKILL.md:136-143`); could also be asked in Step 1.
- `skills/research-deep/SKILL.md`: the item template (59-102) and one-shot example (104-149), in lockstep, plus a new line in Parameter Retrieval (39-54).
- **A hard-constrained template has no "if" blocks.** "Strictly reproduce, only replacing `{xxx}`" (line 56) means an unset decision still renders the section. The existing precedent is `Modules: {modules}`, which renders the literal `auto` when unset (line 48) and the agent is told what `auto` means (line 74). A `Decision: none` sentinel would follow that precedent. But strictly, the flexibility rule says a run without a decision "behaves exactly as today", and a prompt with an extra "Decision: none" block is not byte-identical. The grill should decide whether "behaves the same" is good enough.
- **Where the lessons go in the JSON.** Two routes: (a) a new top-level array beside `uncertain[]`, which needs `_SKIP_KEYS` in `validate_json.py:22` and the report's internal-fields list (`skills/research-report/SKILL.md:81`); or (b) the decision is injected but lessons are just a normal **declared field** in `fields.yaml`. Route (b) changes nothing in the validator or report, and the live fixture's `verdict` field shows users already do this by hand.
- The lessons would need sources; with route (b) the #1 source-trace warning already covers it.
- `/research-report` would decide whether to render lessons; with route (b) it already does, as an ordinary field.

### Overlaps

- **#2, #3, #11** change the same template; bundling saves lockstep passes.
- **#8:** D20's digests come from the same `outline.yaml`, so one `decision:` key serves both run shapes. Q7 item 3 asks whether digests absorb #7.
- **#6 and #10** both need a decision to exist; #7 is upstream of them.

### Questions the grill needs

1. Where is the decision captured: a new question in `/research`, an optional line the user adds by hand to `outline.yaml`, or both? Suggested answer: both; `/research` asks once ("what will you decide with this? skip if none"), and hand-editing works for existing runs.
2. Is a `Decision: none` sentinel in the template acceptable under the flexibility rule, or must the template render byte-identically when no decision is set? Suggested answer: the sentinel, following the `Modules: auto` precedent; the rule is about behaviour, and an agent told "none" does exactly what it does today.
3. Are lessons a new array (route a) or a declared field (route b)? Suggested answer: a new optional array, filled only when a decision is set, because route (b) forces the user to know to add the field, and the whole point is that it follows from the decision automatically. But route (b) is the zero-risk fallback.
4. What does one lesson look like: a plain sentence, or sentence plus source? Suggested answer: a sentence with source references in the same style as fields, so the source trace can check it.
5. Does the report render lessons by default when present? Suggested answer: yes when present, since present means the user set a decision; nothing renders for runs without one.
6. Should lessons be per item (item-major) at all, given that the Veneer lessons came from comparing two products? Suggested answer: genuinely open. A lesson from one product alone ("Obsidian auto-namespaces command IDs") is still useful, but the best Veneer lessons were comparative, which is #8's territory.

### Facts I could not establish

- The exact brief the Veneer lead gave its researchers (the source of the Design lessons format). It was not saved in the run folder.

---

## #9 — An open inventory field instead of predeclared fields only

### How BMAD does it

- **Not prescribed by the skill.** No BMAD file mentions an inventory. The return contract is a list of claims.
- **The Veneer run's version** (`digests/d2-actions-r1-1.md:5-46`): a section `## API inventory` with columns `| System | API / mechanism | What it does | Notes (version, gotchas) | Src |`, about 38 rows. Example row: `| VS Code | commands.registerCommand(id, handler) | Binds a command ID to a handler at runtime | Declaration (manifest) and implementation (code) are separate halves | [2] |`. A separate `## Claims` section (lines 48-69) lists the load-bearing claims in the shape `claim — [refs] — confidence — class`.
- **The inventory went on to be the main deliverable.** `veneer/docs/plugin-api-reference.md` (637 lines) is a capability map built from the inventories, with columns `| Capability | VS Code | Obsidian | Veneer | Notes / what to borrow |`. That is where #10's reconciliation landed.
- **It cost budget.** The D2 digest's own leads section: "Budget note: 14 sources used (cap 12) because two issue sources came as search-result snippets."

### What it would touch here

- `fields.yaml` schema (`skills/research/SKILL.md:145-149`): a field would gain something like a type (table) and declared columns. `detail_level` (brief/moderate/detailed) means nothing for a table.
- `skills/research/validate_json.py`:
  - `load_fields_yaml` (25-40) ignores unknown keys, so declaring `columns:` is harmless.
  - `extract_json_fields` (43-61) adds a field's name and does not descend into a list value, so table rows will not be miscounted as extra fields. Good.
  - `_is_answered` (86-92) counts any non-empty list as answered; it only detects `[uncertain]` in strings, so an uncertain row inside a table goes unnoticed.
  - The source trace (95-119) works per field name: one `sources[]` entry naming the table field covers all 40 rows. Per-row sources (the run's `Src` column) are a different, finer mechanism the validator does not know.
  - Nothing checks that rows have the declared columns. Adding that check as a **warning** is safe; making it fail the exit code would be a gate change the grill should decide on deliberately, because `/research-deep` gates completion on that code (`skills/research-deep/SKILL.md:100`).
- `skills/research-deep/SKILL.md`: the agent reads fields from `fields.yaml` and Output Requirement 1 says "Output JSON according to fields defined in fields.yaml" (line 78). If the field's own definition explains the table shape, the template may need **no** change. If a template line is added, the example changes with it.
- `skills/research-report/SKILL.md` Step 3: `generate_report.py` needs a rule to render a list-of-objects value as a markdown table.
- **Budget:** the per-item table (`skills/research-deep/SKILL.md:15-19`, duplicated in `agents/web-search-agent.md:17-19`) assumes answering a fixed set of fields. D19 (`PLAN.md:310`) already proved that a sweep blows a per-item budget ("29 WebSearch calls against a 20-search `deep` ceiling"). An inventory is a sweep inside an item.

### Overlaps

- **`/research-enumerate` (D19):** its `catalog.md` is already "an open table with declared columns" across a whole domain: a required taxonomy (the axis to sweep along, `skills/research-enumerate/SKILL.md:21`), 3-5 shallow fields per row (line 23), and three honest negative states, "Checked, none found / Checked, inconclusive / Not checked — budget exhausted" (line 59). An inventory field is that pattern shrunk to one item. Its vocabulary already exists and D19 says "do not invent a parallel vocabulary".
- **#8 / Q7 item 3:** D20's digests may absorb the inventory for question-major runs. In Veneer the inventory was per *question* across both products (a `System` column), not per item.
- **#10:** inventory rows are what gets reconciled (built / needed / future).
- **#11:** "Not checked — budget exhausted" is a lead.

### Questions the grill needs

1. Is an inventory a field type inside an item, or is it really "run `/research-enumerate` scoped to one item"? Suggested answer: a field type, but borrowing enumerate's three negative states word for word, so the two features speak the same language.
2. How are columns declared? Suggested answer: a list of column names on the field in `fields.yaml`, each with a one-line description, the same way fields themselves are declared.
3. Do rows carry their own sources, or does the field carry one source list? Suggested answer: per-row source URLs, because a 40-row table backed by one `sources[]` entry hides which row came from where; the field-level `sources[]` entry still exists so the validator trace keeps working.
4. Does the validator check row shape, and does a bad row fail the run? Suggested answer: warn only, matching how #1 shipped; the exit code stays about required fields.
5. Does an inventory field get its own budget? Suggested answer: needs a decision. D19's lesson argues yes; the simplest version is "an inventory field may use up to N extra fetches", stated in the field so the template does not change.
6. Is this worth building for item-major runs if Q7 puts the inventory in question-major digests anyway? Suggested answer: decide Q7 item 3 first; if the inventory lives in digests, the item-major version may not have a user yet.

### Facts I could not establish

- Whether any existing consumer `fields.yaml` already fakes an inventory with a long prose field. I spot-checked one fixture (no), not all.
- Per-row source columns in the Veneer run cite `[n]` numbers into a per-digest list; how those were renumbered for the global report (the `digests-global/` copies) is not documented in the run.

---

## #10 — Reconcile against the project's own spec, after research, never during

### How BMAD does it

- **BMAD has the rule but not the step.** `SKILL.md` Epistemics rule 2, "**The research firewall.** Project context — briefs, PRDs, code, memory… — shapes *what to ask*, never *what is true*. It is inadmissible as evidence… Research subagents receive only their brief — no project files, no ambient context — unless the plan explicitly grants a named document." There is no "reconcile" reference file; the nearest prescribed pieces are `references/selection.md`'s requirements frame (sourced from the project) and `references/synthesis.md`'s recommendations bound to downstream artifacts ("Feeds").
- **The Veneer run did reconciliation by hand, planned at the plan gate.** `.memlog.md:9`: "Reconciliation inputs (post-research only): docs/current-spec.md, docs/FUTURE_PLUGIN_APIS.md, reconciliation-digest s3, vault note plugin lists. Deliverables: research.md + docs/plugin-api-reference.md + deprecated-plugin shortlist."
- **Project files were copied into the run folder and labelled.** `veneer-inventory.md:1`: "Veneer plugin API inventory (project context — NOT research evidence)", "Used only in the reconciliation step to mark catalog rows **built / needed / future**." `planned-plugins.md` carries the same label.
- **The output used five states, not three.** `veneer/docs/plugin-api-reference.md:11`: "✅ built in Veneer · 🔨 needed (the shell or a current planned plugin requires it) · 🆕 Veneer-original (neither VS Code nor Obsidian has it) · 🅿️ future candidate (parked; kept for reference) · ⛔ don't copy (a documented mistake)." The lessons file says built / needed / future; the shipped output added "Veneer-original" and "don't copy".

### What it would touch here

- **The item agent already obeys the firewall by construction:** the item template (`skills/research-deep/SKILL.md:59-102`) passes only the item and `fields.yaml`, never project files. Nothing to change there; the grill only needs to make sure the new step never leaks project files back into it.
- **Where it would live:** `/research-report` Step 3 writes a *deterministic* script; annotating results against a spec is *judgment*, so it cannot live inside `generate_report.py`. It would be an agent step in the report skill, or a standalone skill. "Standalone when no report is wanted" (lessons file) matches the flexibility rule.
- **Output location:** writing annotations back into `results/*.json` would add new keys the validator would see (`_SKIP_KEYS`, `validate_json.py:22`) and would mix project opinion into research evidence, which is the firewall's whole point. A separate file keeps them apart.
- **Context discipline:** the step reads every result plus the project files. On a large run that is unbounded; it may need to work per item or per category.
- `skills/research/LAYOUT.md:30` (run folder contents) if a new file such as `reconcile.md` lands in the run folder.

### Overlaps

- **#9:** the Veneer reconciliation marked inventory rows. Without an inventory, reconciliation marks fields, which is coarser.
- **#7:** the decision says what to reconcile *for*. Veneer's decision line literally names the states ("borrows, builds now, or keeps as future candidates").
- **#6:** BMAD's requirements frame comes from the same project files.
- **#8:** in Veneer, reconciliation ran over the per-question digests, not per-product results.

### Questions the grill needs

1. A step inside `/research-report`, a standalone skill, or both? Suggested answer: a standalone skill the report can call, so a task-driven run with no report can still reconcile.
2. Who names the project files, and when? Suggested answer: the user, at the time of reconciling (not at `/research`), so research never sees them; BMAD's Veneer run named them at the plan gate but used them only afterward.
3. Fixed status vocabulary or user-defined? Suggested answer: a default set (built / needed / future / not for us), overridable per run; Veneer needed five states, which shows a fixed three would not have fit.
4. Annotate the results files, or write a separate file? Suggested answer: a separate file in the run folder, so results stay pure evidence and the validator is untouched.
5. Copy project files into the run folder with a "NOT research evidence" label, as Veneer did? Suggested answer: no copy, just name them by path in the output file's header; copies go stale and the label only matters if something might mistake them for evidence.
6. Does the firewall rule get written into the package somewhere explicit (agent prompt or `LAYOUT.md`)? Suggested answer: yes, one sentence where the reconcile step is defined; the item agent already never sees project files, so it needs no change.

### Facts I could not establish

- Whether a "reconciliation-digest s3" file exists (named in `.memlog.md:9`). It is not in the run folder; it may be elsewhere in the Veneer repo. I did not search for it.
- How much of `plugin-api-reference.md`'s status column was the agent versus Stephan.

---

## #11 — Leads and gaps per result

### How BMAD does it

- **The return contract** (`references/run.md`, "The fan-out"): "plus leads worth chasing and what it looked for and could not find."
- **Leads drive the next round** (`references/run.md`, Rounds): "After each round, harvest the leads: new entities worth chasing, unexpected connections, contradictions between sources, and questions the round opened. Contradictions get priority. Promising leads become the next round's brief." A dimension stops on coverage or "novelty exhaustion".
- **The report's Open questions** (`references/synthesis.md` item 6): "what the research could not answer, and what it would take to answer each."
- **The Veneer example** (`digests/d2-actions-r1-1.md:79-86`, `## Leads & gaps`) has four kinds of entry: unconfirmed claims ("Unverified: exact allowed `StatusBarItem.backgroundColor` values"), snippet-only sources ("VS Code issues #108142 and #33745 were seen only as search snippets; fetch to confirm status and dates"), uncovered topics ("Not covered: … VS Code Quick Pick API vs Obsidian `SuggestModal`"), and a budget note ("14 sources used (cap 12)").
- **In Veneer the leads were never followed:** every dimension logged `Stopped: coverage` after round 1 (lessons file, and `.memlog.md` source lines). They surfaced in the report's Open questions instead.

### What it would touch here

- **Name collision: "Leads" already means something here.** `skills/research/LAYOUT.md:46-47`: each run's `INDEX.md` entry has a "`**Leads**` checklist of directions this run surfaced", and a Map leaf with status `lead` is "a lead nobody has started". `skills/research-report/SKILL.md:102`: the report step uses AskUserQuestion "to ask which directions this run surfaced; write the answers as the entry's `**Leads**` checklist". So a per-item `leads[]` would sit next to an existing run-level Leads concept with a different grain.
- **That is also an opportunity:** today the report asks the user cold. Aggregated per-item leads could become the proposed options for that question.
- `skills/research-deep/SKILL.md` Output Requirements (77-92) and the example (125-140), in lockstep.
- `skills/research/validate_json.py:22`: a new top-level array must join `_SKIP_KEYS`, or it is reported as an "extra field" (`[INFO]` line, not a failure). Exit code untouched.
- `skills/research-report/SKILL.md:81`: the internal-fields list (`_source_file`, `uncertain`, `unreachable`, `sources`) needs the new key, or `generate_report.py` may render it as an ordinary field.
- `agents/web-search-agent.md:76-78` (the `unreachable` and `sources` rules for JSON output) would gain a sibling rule, and line 154 ("If insufficient info found: State what was searched…") already asks for something close in prose output.
- **`/research-harvest` cannot pick these up as is.** The lessons file says leads give "`/research-harvest` something to pick up", but `skills/research/harvest_sources.py` reads only `sources[]` and exists to promote sources into modules (D17, D18). Leads are a different kind of thing; the natural consumer is the INDEX Leads checklist, not harvest.
- Overlap with existing channels: "seen only as a snippet" is close to `unreachable[]`; "unconfirmed" is close to `uncertain[]`. The grill should draw the lines so the agent is not unsure which array to use.

### Overlaps

- **#2, #3, #7:** same template list, same `_SKIP_KEYS`, same report internal-fields list. One lockstep edit.
- **#3:** BMAD ranks contradictions first among leads.
- **#9:** "Not checked — budget exhausted" rows are leads.
- **#8 / Q7 item 3:** D20 digests end in `## Unreachable` / `## Sources` / `## Uncertain`; a `## Leads` section would be a fourth.

### Questions the grill needs

1. What name, given `INDEX.md` already has a run-level **Leads** checklist? Suggested answer: keep "leads" so the item-level list visibly feeds the run-level one, and state in `LAYOUT.md` that item leads are raw material for the index's Leads checklist.
2. Plain strings or small objects (kind + note)? Suggested answer: small objects with a `kind` from a short fixed list (unconfirmed, snippet-only, not covered, over budget, contradiction), because the four Veneer kinds were all distinct and a kind lets the report group them.
3. Where is the line between a lead and `uncertain[]` / `unreachable[]`? Suggested answer: `uncertain[]` names a field that is shaky, `unreachable[]` names a source that was a wall, a lead names *what to do next*; the same problem may appear in two of them and that is fine.
4. Does `/research-report` use aggregated leads to propose the index's Leads checklist instead of asking cold? Suggested answer: yes, as suggested options in the existing AskUserQuestion; the user still chooses.
5. Is the array optional for the agent, or always present (possibly empty)? Suggested answer: always present, empty when nothing to report, matching `unreachable[]`, so the report never has to guess whether an old run had none or never recorded them. Old runs simply lack the key.
6. Is "over budget" a lead or something the agent should never do? Suggested answer: record it if it happens; the D2 digest's overrun was honest disclosure, and hiding it would be worse than the overrun.

### Facts I could not establish

- None material. Whether the item agent in this package actually overruns its budget often enough for an over-budget kind to matter is unknown; no run here records it.

---

## #8 — remaining questions (Q7)

D20 (`PLAN.md:335-346`) decides: a new skill (working name `/research-compare`), one prose digest per question across all subjects, reusing `web-search-agent` unmodified, reading the existing `outline.yaml` (items = subjects) and `fields.yaml` (each field category = one question; its fields are the sub-points), digests ending in `## Unreachable` / `## Sources` / `## Uncertain` as `catalog.md` does (D19). Q7 items 1–2 (subject ceiling, budget formula) are awaiting Stephan's confirmation and are not covered here. Not yet built: there is no `skills/research-compare/`, and `TASKS.md:21` says nothing is ready to hand off.

### Q7 item 3 — what goes in a digest

**BMAD / Veneer facts.** The Veneer D2 digest's sections, in order: `## API inventory`, `## Claims`, `## Design lessons`, `## Leads & gaps`, `## Sources` (`digests/d2-actions-r1-1.md`, headings at lines 5, 48, 70, 79, 88). It has no separate Unreachable or Uncertain section: unconfirmed items sat inside Leads & gaps, marked "Unverified:". A one-line scope header opens it: "All claims trace to sources retrieved 2026-09-25. Items marked "unverified" are hypotheses from prior knowledge that this run did not confirm." Sources are listed as `[n] Title — Publisher — date or "undated" — URL — accessed date`. BMAD's own contract (`references/run.md`) asks only for claims, leads, and what was not found.

**Here.** D20 already fixes the three trailing sections. Adding Inventory, Lessons and Leads means a digest is: comparison body, optional inventory, optional lessons (only when `decision:` is set), leads, then the D20 trailing sections. Digests are prose, so none of this touches `validate_json.py` or the item template.

**Question:** Do digests carry comparison + inventory + lessons + leads, with the item-major versions of #7/#9/#11 left to their own grills? Suggested answer: yes; prose digests cost nothing to extend, and settling the section names here gives #7/#9/#11 a vocabulary to reuse. Lessons only when `decision:` is set, so a digest without a decision is not padded.

### Q7 item 4 — does `/research-report` read digests

**Facts.** `/research-report` writes `generate_report.py`, which reads `results/*.json` (Step 3). It has nothing to read in a digests-only run. Veneer's `research.md` was a judgment synthesis over digests: executive summary first, one section per question, **cross-dimension insights** ("what only the combination shows… if there are no cross-dimension insights, say so rather than manufacture them", `references/synthesis.md` item 3), recommendations, open questions, source appendix, staleness map. That is model work, not a conversion script. `LAYOUT.md:54` makes `/research-report` the only skill that flips `researched` → `complete`.

**Question:** Does a question-major run stop at the digests, or does `/research-report` learn a digest mode? Suggested answer: stop at the digests by default (they already are the comparison, and nothing forces a report), with an optional synthesis step later if a run actually wants one. Then decide separately who flips the index to `complete` for such a run.

### Q7 item 5 — module routing per question

**Facts.** Today routing is one list per run: `/research` Step 2b pins `execution.modules` in `outline.yaml` (`skills/research/SKILL.md:120-128`, written at 143), and `/research-deep` passes it as `Modules:` to every item agent (`skills/research-deep/SKILL.md:48`). Module slots per agent depend on depth: 1 / 2 / 3 (`agents/web-search-agent.md:17-19`). BMAD has no module concept; its per-dimension equivalent is "its search surfaces" in each researcher's brief (`references/run.md`). In Veneer, the security and AI-API questions plainly needed different sources (security advisories vs. model-API docs).

**Question:** Route per question at plan time and pin it, or reuse the single run-level list? Suggested answer: allow an optional per-category module list in `fields.yaml` (next to the category name), falling back to `execution.modules`, then to `auto`. `validate_json.py` ignores unknown keys, so this is safe for item-major runs on the same folder. The cost is a second place modules can be pinned, which the grill should weigh against `ROUTING.md` being the single source of truth for routing rules (the pin is a choice, not a rule, so it may not conflict).

### Q7 item 6 — where digests live, and index status

**Facts.** BMAD writes `digests/<dimension>-r<round>-<n>.md` (`references/run.md`). Here, `LAYOUT.md:30` lists run-folder contents (`outline.yaml`, `fields.yaml`, `results/`, `report.md`, `generate_report.py`); `/research-enumerate` already added `catalog.md` at the folder's top level. The status ladder is `outline` → `researching` → `researched` → `complete` (`LAYOUT.md:47`), flipped by `/research-deep` (line 53). **A real collision:** `/research-harvest`'s script classifies a run folder with no `results/*.json` as `no-results` and reports it as "never researched" (D18, `PLAN.md:297-308`). A digests-only run would be misreported. Digests' `## Sources` are markdown, so harvest cannot count them either (the same is true of `catalog.md` today).

**Question:** Where do digests go, and what status does a digests-only run carry? Suggested answer: a `digests/` folder in the run folder, one file per question (named after the category slug); the compare skill flips `outline` → `researching` → `researched` exactly as `/research-deep` does, so no new status is invented. Separately decide whether `/research-harvest` learns a fourth run state ("digests only") or is left alone for now.

### Q7 item 7 — the skill's name

**Facts.** Existing names: `research`, `research-deep`, `research-report`, `research-add-items`, `research-add-fields`, `research-add-module`, `research-enumerate`, `research-harvest`. BMAD calls the unit a "dimension"; D20 and Q7 call it a "question" and the items "subjects" (round 1 tripped on "products").

**Question:** Is `/research-compare` the name? Suggested answer: keep it if the skill is always run with two or more subjects; it says what the user gets. If single-subject runs are allowed (one agent per question for one subject), a name like `/research-by-question` describes the shape more honestly. Decide the single-subject case first and the name follows.

### Facts I could not establish

- Whether the duplicated depth/budget table becomes a third copy in the compare skill. The two existing copies already differ in shape: `skills/research-deep/SKILL.md:15-19` has no Modules column, `agents/web-search-agent.md:17-19` has Modules plus a description column. Q7 item 2's formula would need to land somewhere; that belongs to items 1–2.

---

## Suggested grill order

1. **#8 Q7 items 3–7 (with 1–2 confirmed in the same sitting).** D20 is the only item already decided and the "biggest driver"; settling the digest sections here names the vocabulary (lessons, inventory, leads) that #7, #9 and #11 then reuse for item-major runs.
2. **#7 decision line.** Upstream of #6 and #10 (both need a decision to exist), and it settles the "optional variable in a hard-constrained template" pattern (`Decision: none`, like `Modules: auto`) that the next bundle reuses.
3. **Bundle #11 + #3 + #2's source-date half.** All three change the same Output Requirements list in the item template and its one-shot example, the same agent lines (76-78, 132), `_SKIP_KEYS`, and the report's internal-fields list; one lockstep edit instead of three.
4. **#2's windows and re-check list.** Can follow once dates exist in `sources[]`; it is the report-side half and depends on the anchor-date answer from step 3.
5. **#9 inventory field.** After Q7 item 3, because if the inventory lives in question-major digests the item-major version may not have a user yet; and it should borrow `/research-enumerate`'s vocabulary.
6. **#10 reconcile.** After #7 (what to reconcile for) and #9 (what rows to mark); independent of the template, so it never collides with the bundle.
7. **#6 pick-one.** After #7 and #10, since its requirements frame is #10's project-file input applied before research, and its verdict answers #7's decision.
8. **#4 Draft then Process.** Last: the largest item, a whole new skill, independent of the others, and its best target shape (per-item results vs. question-major digests) is clearer once #8 is built.
