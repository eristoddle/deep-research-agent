# Public-package hygiene — no owner name, local paths, or private projects in what ships

**Parked** 2026-10-01. This is a public package that other people install. Nothing a consumer receives should name the maintainer, point at a path on the maintainer's machine, or lean on one of the maintainer's own projects as if every reader knew it. That reads as unprofessional, and a hard-coded path is also a bug, because the path doesn't exist on anyone else's machine.

## Two zones, two standards

- **What ships (strict):** everything under `skills/` and `agents/`. APM installs this into other people's projects, and the model reads it as instructions. No personal name, no `/Users/...` or `~/Dropbox/...` path, no `sm-static`, `writing-model-research`, Veneer or other private project used as a reference the reader is expected to know. Examples should be generic or clearly hypothetical.
- **What's public but not installed (looser):** `README.md`, `LICENSE`, `plugin.json`, `AGENTS.md`, `PLAN.md`, `TASKS.md`, `ROADMAP.md`, `docs/`. Anyone can read these on GitHub. The author line, copyright, repo URLs (`eristoddle/...`) and the disclosed affiliate link are correct and stay. The question there is narrower: should absolute local paths (the external task mirror in `AGENTS.md`, the live-consumer path) and run evidence naming private repos be reworded or made relative?

## First scan (2026-10-01, grep only, not a full read)

- `skills/` and `agents/`: **no hits** for the name, the GitHub handle, `/Users/`, `Dropbox`, `sm-static` or `writing-model-research`. The one thing close to the line is the one-shot example in `skills/research-enumerate/SKILL.md` (AI affiliate programs), which comes from a real private run. It reads as a generic example, but it's worth a second look.
- Planning docs: a handful of hits each in `AGENTS.md` (2), `PLAN.md` (5), `ROADMAP.md` (1), and seven `docs/` files, mostly `sm-static` and Dropbox paths cited as run evidence.
- A grep only catches the words it's told to look for. Wording like "the user's blog", a project nickname, or a personal habit written as if it were a rule won't show up, so the real check is a read-through.

## What closing this looks like

1. Read every file under `skills/` and `agents/` by eye and fix anything personal.
2. Decide the planning-docs question above and apply it.
3. Add a standing rule to `AGENTS.md` (and the implementer agent's definition) so new skill text stays clean: shipped files use generic examples and relative paths, and a quick grep for the name, handle, `/Users/` and `Dropbox` across `skills/` and `agents/` becomes a check on every task that touches them.
