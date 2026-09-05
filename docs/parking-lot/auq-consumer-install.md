# The AUQ consumer install

**Parked** 2026-09-03, arriving from the external task mirror as three separate items. They are recorded here as one because they share a blocker: **which directory is the project root** decides where the pin lives *and* where local modules resolve from, so the scope question gates the other two.

Ordered by dependency, not by the mirror's priority marks:

1. **Decide `rough/`-level install vs per-client.** `~/Dropbox/clients/AUQ/rough` holds the install (updated to `#d178d2c` on 2026-09-04). Project skills resolve from the project root, so opening `rough/DeepInfra/` directly does **not** see them — the skills are invisible from exactly the directory the work happens in. Either the install moves down to each client folder (N installs, N pins to bump) or the work moves up to `rough/` (one install, but every client's research shares one research root and one `INDEX.md`). D3's structural discovery makes the second less painful than it would have been: a run folder is found by globbing for `outline.yaml`, so multiple clients under one root already works. **This is a real decision and belongs in a grill, not in a task queue.**

2. **Update the installed copy of the skills in AUQ.** ✅ **Done 2026-09-04** — updated to `#d178d2c` and `apm install` re-run; 7 skills and both agents verified in place. Note the earlier claim here was wrong twice over: the pin was at `#f7a9707d` (not `#91c639f2`, which had already been superseded), and this was described as blocked on (1) when it never was. (1) decides whether there should *also* be an install in each client folder; it does not stop the existing `rough/` install from being updated. Leaving a client on months-old files to await a design decision was the wrong call.

3. **Build local modules for DeepInfra and OCR/LlamaIndex** via `/research-add-module`. Source maps, **not positioning briefs** — fixed source sets plus competitor sets. **D2 does not block this**: D2 governs new *package* modules shipped to every consumer, and these are project-owned modules under `.agents/web-search-modules-local/`, built by the discovery step for a project that actually has the question. That is D2's satisfied case, not an exception to it. Depends on (1) for where they land.

Nothing here is queued. (2) is done; (1) remains a real design decision for a grill, and (3) is authoring work that should run through `/research-add-module` rather than by hand once (1) says where the modules land.
