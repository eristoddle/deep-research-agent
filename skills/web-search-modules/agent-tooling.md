# Agent Tooling Module

**Family:** Tooling & platform
**Use when:** The subject is something you *install and run* — an agent CLI or IDE, an MCP server, a skill or plugin — and the question is its current feature set, config format, version history, permission model, or ecosystem.
**Do not use for:** A model you *call* over an API — its scores (`benchmarks`), version and deprecation dates (`model-releases`), token prices (`pricing`), or vendor positioning (`vendor-landscape`). Not for a bug in a named repo either (`github-debug`).
**Siblings:** `github-debug` — pair them when a config question may turn out to be a bug; `general-web` when you need what practitioners hit rather than what the docs claim.

## Sources

- **The tool's own docs site, fetched directly by URL.** The authoritative answer for config formats, directory layouts, and permission models. Do not reach it via `site:` search — see the impostor-domain tactic below. Verified working: `https://cursor.com/docs/skills`, `https://opencode.ai/docs/config/`, `https://code.claude.com/docs/en/changelog`.
- **The raw `CHANGELOG.md` on GitHub**, not a changelog site. `https://raw.githubusercontent.com/<org>/<repo>/main/CHANGELOG.md` returns the real per-version list with no rendering layer. Verified on `anthropics/claude-code`. This is the single best source for "what changed between versions" and it beats every changelog aggregator.
- **`agentskills.io`** — the vendor-neutral spec for the `SKILL.md` format, and the answer to any portability question. **Fetch the `.md` variants**, not the HTML: `https://agentskills.io/specification.md` and `https://agentskills.io/clients.md`. The bare HTML pages return raw MDX with a multi-thousand-line embedded client array. `https://agentskills.io/llms.txt` is the link index. `clients.md` is the highest-value page in this module: it maps ~45 agent tools to their own canonical skills-doc URL, which is how you find a tool's real docs domain without searching.
- **The project's GitHub repo** — for anything the docs omit: actual config schema, open Discussions, and whether the thing is maintained. Check the last commit date before trusting any tool doc.
- **`mcpservers.org`** — browsable registry for MCP servers and agent skills, entries linked to source repos. Use it to enumerate what exists; then verify each candidate at its repo.
- **`dev.to`** — the one community source that consistently outperformed here, specifically for *undocumented* failure modes (hook exit-code semantics, case-sensitive matchers, hooks that silently no-op in headless mode). Weak for facts, strong for gotchas.

## Query tactics

- **This domain is the most SEO-farmed one in the module set.** A plain search for any agent tool returns a wall of sites that repackage one changelog. Skip on sight: `gradually.ai`, `claudelog.com`, `claudefa.st`, `claude-world.com`, `releasebot.io`, `techsy.io`, `codersera.com`, `thepromptshelf.dev`, `vibehackers.io`, `mcpdirectory.io`, `mcp.so`, `agensi.io`, `skillsclaude.org`, `agentskill.sh`, `agent-skills.cc`, `claudeskil.com`. Go to the primary source instead; you already know its URL.
- **Watch for impostor docs domains.** `open-code.ai` and `opencode.asia` both mirror opencode's documentation and both outrank the real `opencode.ai` on some queries. Confirm a docs domain against `agentskills.io/clients.md` or the GitHub repo's stated homepage before quoting anything from it. Assume every popular agent tool has at least one clone.
- **Never quote a marketplace's inventory count.** Observed on one afternoon: 275,000+, 7,200+, 4,558, and ~3,000 for overlapping catalogs. These are marketing numbers. If a count matters, say the registries disagree and name the range.
- **Stamp the version and the date on every behavioral claim.** These tools ship multiple times a week — Claude Code was at 2.1.251 on 2026-08-28. A config format answer without a version is not an answer, and last month's is routinely wrong.
- **Config questions are directory questions.** The useful answer names the exact file and every path searched, in precedence order. Cursor reads skills from four (`.agents/skills/`, `.cursor/skills/`, and the `~` variants); opencode uses `opencode.json`/`opencode.jsonc`. Half of what looks like a broken tool is a file in the wrong directory.
- **`platform.claude.com/docs/en/release-notes/overview` is ~95KB.** Fetch it only with a narrow prompt, and prefer the raw CHANGELOG for Claude Code specifically — that page covers the API and SDKs, not the CLI.
