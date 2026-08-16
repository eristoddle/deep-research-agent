# Pricing & Availability Module

**Family:** AI ecosystem & market
**Use when:** The question is cost, rate limits, quotas, tiers, or where a model or service is available.
**Do not use for:** Whether a model is any good (`benchmarks`), or which vendor to pick overall (`vendor-landscape`).
**Siblings:** `model-releases` — the same page usually answers both; `vendor-landscape` when price is one column in a bigger comparison.

## Sources

- **The provider's own pricing page.** The only authoritative source. Everything else is a copy of it, made at an unknown date.
- **API docs: rate limits, quotas, and tiers.** Often a separate page, and often the real constraint — a cheap model you can only call twice a second is not cheap.
- **Cross-vendor aggregators** — OpenRouter's model list (per-token prices side by side), Artificial Analysis (price against latency and quality). Ideal for building a comparison set fast, then verify each figure at its source.
- **Cloud marketplace listings** — Bedrock, Vertex AI, Azure AI Foundry. The same open model is routinely served at different prices by different hosts; the marketplace page is the price that applies there.
- **Billing docs** for the units that turn a headline price into a real bill: cached-input rates, batch discounts, long-context surcharges, tool-use and reasoning-token accounting, per-image and per-page rates.

## Query tactics

- **Never quote a price from a blog post, comparison article, or another model's memory.** Fetch the pricing page. This is the single highest-error area in the whole pipeline and the errors are quotable and embarrassing.
- **Record the unit exactly**: per 1M input tokens vs output tokens, cached vs uncached, batch vs real-time, per image, per page, per second of audio. A number without its unit is not an answer.
- **Stamp the observation date.** Prices change without announcement and without a changelog entry.
- **Name the host.** "Llama 3.3 70B costs $X" is incomplete — say which provider serves it at that price, because several do at several prices.
- **Check availability alongside price**: regions, waitlists, enterprise-only tiers, and minimum commitments. A price you cannot access is not a price.
- Free tiers and credits are marketing. Note them separately from the rate, with their expiry.
- If a pricing page is unreachable, report it as unreachable with the URL. Do not substitute an aggregator's figure and present it as the provider's.
