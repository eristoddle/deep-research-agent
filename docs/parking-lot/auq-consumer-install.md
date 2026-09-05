# AUQ local modules — DeepInfra and OCR/LlamaIndex

**Parked** 2026-09-03. Two of the three items this file used to hold are closed; only the module-building remains.

**Closed 2026-09-04 — where the install lives.** `rough/` is the right level and is not an open question. The research spans DeepInfra *and* OCR/LlamaIndex together, so one install covering both is the point, not a compromise. Do not reopen this as a "root vs per-client" decision; it was answered by what the work actually is.

**Closed 2026-09-04 — the installed copy is current.** Updated to `#d178d2c` and re-installed; 7 skills and both agents verified in place.

## What remains

**Build local modules for DeepInfra and OCR/LlamaIndex** via `/research-add-module`. Source maps, **not positioning briefs** — fixed source sets plus competitor sets. They land in `rough/.agents/web-search-modules-local/`, which APM does not own, so they survive reinstalls.

**D2 does not block this.** D2 governs new *package* modules shipped to every consumer; these are project-owned modules for a project that actually has the question. That is D2's satisfied case, not an exception to it.

Run it through `/research-add-module` rather than writing the source lists by hand — the discovery step is the whole value, and a guessed source list routes the agent at plausible sites that turn out to be empty.
