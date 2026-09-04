# The AUQ consumer install

**Parked** 2026-09-03, arriving from the external task mirror as three separate items. They are recorded here as one because they share a blocker: **which directory is the project root** decides where the pin lives *and* where local modules resolve from, so the scope question gates the other two.

Ordered by dependency, not by the mirror's priority marks:

1. **Decide `rough/`-level install vs per-client.** `~/Dropbox/clients/AUQ/rough` currently holds the install (pinned `#91c639f2`). Project skills resolve from the project root, so opening `rough/DeepInfra/` directly does **not** see them — the skills are invisible from exactly the directory the work happens in. Either the install moves down to each client folder (N installs, N pins to bump) or the work moves up to `rough/` (one install, but every client's research shares one research root and one `INDEX.md`). D3's structural discovery makes the second less painful than it would have been: a run folder is found by globbing for `outline.yaml`, so multiple clients under one root already works. **This is a real decision and belongs in a grill, not in a task queue.**

2. **Bump the AUQ pin.** It sits at `#91c639f2`, which predates the validator fix and `competitor-content`, and by now also the `[results-root]` and `[runtime-portability]` retrofits and everything the access-method retrofit lands. A consumer does not get any of it until the pin moves and `apm install` re-runs. Mechanical once (1) is settled — pointless before, since the answer may change how many pins there are.

3. **Build local modules for DeepInfra and OCR/LlamaIndex** via `/research-add-module`. Source maps, **not positioning briefs** — fixed source sets plus competitor sets. **D2 does not block this**: D2 governs new *package* modules shipped to every consumer, and these are project-owned modules under `.agents/web-search-modules-local/`, built by the discovery step for a project that actually has the question. That is D2's satisfied case, not an exception to it. Depends on (1) for where they land.

Nothing here is queued. (2) becomes mechanical the moment (1) is answered; (3) is authoring work that should run through `/research-add-module` rather than by hand.
