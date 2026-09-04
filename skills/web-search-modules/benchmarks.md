# Benchmarks & Leaderboards Module

**Family:** AI ecosystem & market
**Use when:** The answer is a published evaluation number — how a model scores, how fast it runs, how it ranks against others.
**Do not use for:** Numbers reported *inside a paper* (`academic-papers`), or "which should I actually use" as a practitioner question (`general-web`).
**Siblings:** `model-releases` — pair them when a score belongs to a specific version and you must confirm which one was evaluated.

## Sources

In descending order of independence, which is the axis that matters here:

- **Independent evaluators** — LMArena and similar human-preference arenas (Elo, not accuracy); Artificial Analysis (latency, throughput, cost-per-token, quality index in one table). Best starting point because the evaluator has no stake in the result. Verified working: `https://arena.ai/leaderboard` (LMArena's own domain now redirects here), `https://artificialanalysis.ai/models`. See `sites/artificial-analysis.md`.
- **The benchmark's own home** — its repo, docs site, or hosted leaderboard. SWE-bench, HELM, `lm-evaluation-harness`, and coding/agentic evals mostly publish a live table in the repo README or a project site. This is where the *methodology* lives, and methodology is what makes two numbers comparable or not. Verified working: `https://www.swebench.com/` (Verified/Lite/Multilingual leaderboards), `https://github.com/stanford-crfm/helm` (HELM's hosted leaderboard pages render client-side; the repo README links the current ones), `https://github.com/EleutherAI/lm-evaluation-harness`. See `sites/github.md`.
- **Hugging Face** — Spaces hosting leaderboards, model cards with an eval table, and collections that gather a benchmark's submissions. Leaderboard aggregation has largely consolidated here as standalone trackers shut down — the original Open LLM Leaderboard itself retired in 2026. Verified working: `https://huggingface.co/spaces?category=model-benchmarking`, `https://huggingface.co/spaces/ArtificialAnalysis/LLM-Performance-Leaderboard`. See `sites/huggingface.md`.
- **Vendor announcements and model cards** — the fastest source and the least neutral. Always usable, always labeled as self-reported. Same provider blog/newsroom URLs as `model-releases`' newsroom bullet.
- **OpenRouter rankings** — actual usage share by model, which answers "what do people really run" in a way no benchmark does. Verified working: `https://openrouter.ai/rankings`. See `sites/openrouter.md`.

## Query tactics

- **Search the benchmark, not the model.** `SWE-bench leaderboard` finds the live table; `<model> benchmark results` finds twelve blog posts quoting a stale copy of it.
- **Prefer a live leaderboard page over any article citing one.** Articles freeze a snapshot and rarely date it.
- **Capture the configuration or the number is meaningless**: shot count, chain-of-thought on/off, subset (`SWE-bench Verified` ≠ `SWE-bench full`), harness version, temperature, and the exact model ID evaluated.
- **Date every score.** Leaderboards are overwritten in place; a number without an observation date cannot be reproduced or defended later.
- **Separate self-reported from independently run**, and say which in the output. A vendor's own eval is evidence, just weaker evidence.
- **Look for the dispute.** Search `<benchmark> contamination`, `<benchmark> disputed`, or `<model> <benchmark> criticism` — headline scores on popular benchmarks are contested often enough that it is worth one query.
- Performance benchmarks (tokens/sec, time-to-first-token) are host-dependent, not model-dependent. Record which provider served the model.
