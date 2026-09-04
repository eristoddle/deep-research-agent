# GitHub — github.com

**Used by:** agent-tooling, benchmarks, github-debug, model-releases
**Reachable:** yes

## Query
- Raw changelog, not a changelog site: `https://raw.githubusercontent.com/<org>/<repo>/main/CHANGELOG.md` — the real per-version list with no rendering layer. Verified on `anthropics/claude-code`.
- Issues (bugs, workarounds): `site:github.com/<org>/<repo>/issues "<exact error text>"` once the repo is known, or `site:github.com issues "<exact error text>"` when it isn't.
- Releases (SDKs, inference engines, `transformers`): `https://github.com/<org>/<repo>/releases`. Verified: `https://github.com/vllm-project/vllm/releases`.
- Benchmark methodology: several evals (SWE-bench, HELM, `lm-evaluation-harness`) publish their live table in the repo README rather than a separate site.

## Worth knowing
- The raw `CHANGELOG.md` pattern beats every changelog aggregator — it is the single best source for "what changed between versions."
- Check the last commit date before trusting any repo's doc, claim, or maintenance status.
- Open Discussions and closed Issues are where undocumented config schema and known bugs actually live.
