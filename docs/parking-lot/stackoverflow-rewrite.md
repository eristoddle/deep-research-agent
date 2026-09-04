# Rewrite `stackoverflow.md`

**Parked** 2026-08-21. Distinct from the access-method retrofit, which covers this file at piece 6.

`skills/web-search-modules/stackoverflow.md` is **12 lines** — the shortest module by a wide margin. It has a correct routing header, two vague source bullets ("Stack Overflow and other Stack Exchange sites", "Technical forums and discussion boards"), and **zero query tactics**. Every other module carries a tactics section; this one carries none, so it contributes almost nothing beyond its routing decision.

It routes on real traffic — the Software & debugging family is the most-hit family — so it should earn its slot rather than coasting on a sibling relationship with `github-debug`.

The retrofit adds access methods only. A rewrite means writing the tactics that actually work on Stack Exchange: the closed/duplicate signal, score-vs-recency tension on old accepted answers, `[tag]` search syntax, and when the answer is in a comment rather than the accepted post. That is authoring work, not a mechanical pass, and it is a good candidate for `/research-add-module` rather than hand-writing.
