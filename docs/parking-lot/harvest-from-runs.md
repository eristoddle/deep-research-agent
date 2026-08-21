# Harvest sources from completed runs into a local module

**Parked** 2026-08-21. Depends on [Q1](../questions/Q1-source-accumulation.md) being decided first.

Every completed run leaves `{topic_slug}/results/*.json`, which records the URLs each item agent actually used. Today that evidence is discarded. The idea: pull recurring URLs out of finished runs and fold them into a **local** module in `.claude/web-search-modules-local/` — project-owned, never overwritten by `apm install`, which is the only tree where an accumulating source list can safely live.

Applies only to **parameterized** modules (PLAN.md D1); fixed-site modules have nothing to accumulate and open-query modules cannot.

Not started because the hard part is not extraction, it is **what justifies keeping a URL** — see Q1. Harvesting uncritically refills modules with the guessed-quality sources `/research-add-module` exists to filter out.
