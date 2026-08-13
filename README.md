# deep-research-agent

The `web-search-agent` subagent and its five strategy modules from
[Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills),
wrapped in a `plugin.json` so APM can install them.

## Why this exists

APM only accepts a source whose root is a package — `SKILL.md`, `apm.yml` + `.apm/`,
or `plugin.json`. Upstream ships its agent as a bare `agents/` directory with none of
those, so `apm install Weizhena/Deep-Research-skills/agents` fails validation and the
agent can't be installed as a dependency. The five research skills each have a
`SKILL.md` at their root and install fine on their own.

`/research` and `/research-deep` launch `web-search-agent` by name via Task, so the
skills are non-functional without it. This repo closes that gap.

## Install

```sh
apm install eristoddle/deep-research-agent --target claude
```

Deploys to:

```
.claude/agents/web-search-agent.md
.claude/skills/web-search-modules/{academic-papers,chinese-tech,general-web,github-debug,stackoverflow}.md
```

The modules live under `skills/` rather than `agents/` on purpose. APM flattens
every `.md` beneath `agents/` into individual top-level agents when installing from
a git source, which destroys the `web-search-modules/` directory and registers five
bogus agents. A skill bundle deploys its directory intact, so the modules stay
together and stay readable at a stable path.

Pair it with the skills:

```sh
apm install Weizhena/Deep-Research-skills/skills/research-en/research --target claude
# ...and research-add-items, research-add-fields, research-deep, research-report
```

## Changes from upstream

1. Upstream's agent hardcodes its module directory as
   `~/.claude/agents/web-search-modules/`, which assumes the documented `cp` install
   into the home directory. APM deploys project-locally, so the reference now prefers
   `.claude/skills/web-search-modules/` and falls back to the global path.
2. The modules moved from `agents/` to `skills/web-search-modules/` (see above), with
   a `SKILL.md` added to describe the bundle.

The module contents and the rest of the agent are verbatim.

## License

MIT, from upstream — see `LICENSE`. Copyright (c) 2026 Lan Zheng.
All credit for the agent and modules goes to
[Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills).
