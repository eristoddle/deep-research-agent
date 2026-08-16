# Model Releases & Changelogs Module

**Family:** AI ecosystem & market
**Use when:** The question is what shipped, what changed, what a model is called, or whether it still exists — versions, release dates, deprecations, migrations.
**Do not use for:** How a model *scores* (`benchmarks`), what it *costs* (`pricing`), or a bug in code that calls it (`github-debug`).
**Siblings:** `pricing` — a new model release and its price nearly always land on the same day, from the same page.

## Sources

- **API docs "models" page** — the authoritative list of currently served model IDs. Outranks every announcement post: blogs say what launched, docs say what is live right now.
- **Deprecation, sunset, and migration pages** — usually a separate page from the model list, and the only place that tells you a model is going away. Check it explicitly; nothing else surfaces it.
- **Provider newsrooms and engineering blogs** — Anthropic, OpenAI, Google DeepMind, Meta AI, Mistral, DeepSeek, Qwen, and the inference hosts. Good for intent and capability claims, weak for exact identifiers.
- **Hugging Face model repos** for open weights — commit history, revision tags, and README diffs are ground truth on what actually changed, including silent re-uploads that never got an announcement.
- **GitHub releases** for the surrounding stack — SDKs, inference engines (vLLM, SGLang), and `transformers`. Support for a new architecture often lands here before the model is announced.

## Query tactics

- **Run `date +%Y-%m-%d` first and anchor every query to it.** This is the module where the model's own training-cutoff knowledge is most likely to be confidently wrong.
- **Model IDs are the reliable key, not marketing names.** Search the exact identifier string; marketing names get reused across generations and pull in coverage of the wrong version.
- **Read the docs/changelog before any news article.** News coverage lags, misstates IDs, and repeats other coverage rather than the source.
- **Ask "is it still served," not just "was it released."** A model with a launch post may already be deprecated; only the models page and the sunset notice settle it.
- **Distinguish preview / experimental / GA.** Preview endpoints change under you and are frequently what a benchmark number was actually measured on.
- For open weights, prefer the repo commit log over the announcement — weights get quietly re-uploaded and the README is edited in place.
- Note the *last updated* timestamp of every page you cite. A changelog with no visible date is a weak source.
