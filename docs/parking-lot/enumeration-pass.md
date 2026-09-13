# Enumeration pass — breadth before depth

**Parked** 2026-09-12, raised by a live task in the `sm-static` project: catalogue affiliate programs in the AI space.

## The gap

The package has one shape of work: `/research` builds an outline, `/research-deep` launches an independent agent per item to fill a rich field schema. That is depth per item, and it is the right tool when each item genuinely needs investigating.

It is the wrong tool when the hard part is **finding the items at all** and each one needs three shallow facts. The affiliate task is the worked example: per program all that is wanted is a link, a one-line description of the product, and commission terms if they are public. Running a deep agent per program would pay per-item investigation cost to retrieve what is printed on the program's own page, while the actual difficulty, which is enumeration, goes unaddressed.

So there is a missing stage, and it sits *before* `/research-deep` rather than beside it.

## Why this is not just "a shallow mode"

**The name stops being accurate and that is fine, because the two compose.** Stephan's framing: some deep research *starts* with this pass. Sweep broad and shallow to find out what exists, then pick the paths worth descending and run `/research-deep` on only those. The enumeration pass is stage one, the deep pass is stage two, and the selection between them is a human decision informed by stage one's output.

That makes this a **terminal-or-feeder** stage:

- **Terminal** when a catalog is the deliverable. The affiliate register wants a list, not a monograph per program.
- **Feeder** when the catalog is reconnaissance. The outline that `/research` currently asks a human to supply from model knowledge could instead be *derived* from a real sweep, which would make the item list evidence-based rather than recalled.

The second use is the more interesting one, because it attacks a known soft spot: `/research` Step 1 generates the initial item list from the model's existing knowledge, which is exactly where a stale or partial list enters and then silently shapes everything downstream.

## Tactics that generalize beyond the affiliate case

Recorded now because they were learned on a real task and would otherwise have to be rediscovered:

- **Find the aggregator, harvest the roster.** The affiliate insight was that Dub is not a program, it is a *provider* hosting dozens. One provider found yields many items at once. The general form: before enumerating leaves, look for the thing that lists the leaves. Directories, marketplaces, registries, awesome-lists, category pages. This is the single highest-leverage move in a breadth sweep and it has nothing to do with affiliates.
- **Two-phase sweep, dense first.** Phase one hits aggregators, phase two hits one-offs that no aggregator carries. Phase two has much lower yield per search, so it runs second and stops when it stops paying.
- **Take an exclusion list as an input.** The caller usually already knows some of the answer. Feeding known items in and instructing the sweep to skip them keeps the output to genuinely new material and stops the register being re-derived every run. Worth a first-class slot in the prompt shape, not an ad-hoc paragraph.
- **A blank is a result; a guess is damage.** Shallow catalog fields are often gated behind signup (commission terms are the canonical case). The instruction has to be explicit that "not public" is the correct value and an inferred rate is worse than an empty cell, because a plausible fabricated number is indistinguishable from a real one at review time.
- **Record the negatives.** "Checked, no program found" is worth keeping, or the same dead ends get re-searched on every future run.

## The trigger to unpark

Per D2's spirit: build it when a second live project wants the same shape. The affiliate task is the first. Stephan expects this kind of request to recur ("I see doing this type of thing pretty often"), and specifically noted it needs a real process rather than a one-sentence prompt, which is the argument for it being package machinery instead of an improvised subagent brief each time.

What the affiliate run should produce as evidence for that decision: whether the two-phase sweep actually outperformed a naive flat search, and how much of the output needed human triage before it was usable.
