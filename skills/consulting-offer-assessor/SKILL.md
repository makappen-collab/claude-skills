---
name: consulting-offer-assessor
description: >
  Fires when the user asks for a readiness call on a SPECIFIC consulting offering —
  a methodology, solution, productised service, or fixed-price consulting package —
  before they write a product brief or build the deliverables. Trigger phrases:
  "assess this offering", "is this offer ready", "score this methodology / consulting
  offer", "run the offer assessor", "is this ready for a product brief",
  "/consulting-offer-assessor". Scores the offering cold against a fixed 9-element
  rubric (problem, deliverables, price, timeline, phases, structure, metrics, target
  buyer, proof) plus two gates (coherence, buyer-willingness). A sub-agent scores in
  isolation from the calling conversation so the verdict isn't biased by the chat's
  enthusiasm; an adversarial sub-agent then challenges it. Output is a scorecard, a
  tiered verdict (Not-ready / Refine / Ready / Strong) with the element tally, the
  single biggest gap, and what would have to be true to move forward. It is the
  consulting-offering sibling of a lifestyle-business idea assessor, and it runs
  BEFORE a product-brief gate. Does NOT fire on idle riffing with no ask for a
  verdict; on a lifestyle or consumer product idea (that's a business-idea assessor);
  on stress-testing a FINISHED methodology doc against a buying committee (that's a
  buyer-council review); on BUILDING the methodology artefacts (that's a methodology
  builder); or on a change-programme artefact (that's a change-council review).
---

# Consulting Offer Assessor

## Role

A readiness gate for consulting offerings. Takes one concrete offering — a methodology, solution, productised service, or fixed-price consulting package — and scores it cold against a fixed rubric, returning whether the offering is coherent and complete enough to take forward. It is the **Assess** stage of a product lifecycle: it runs BEFORE the product-brief gate, and its whole job is to stop a half-formed offering from consuming a brief and a build before its core pieces exist. The output kills a thin offering fast and tells a promising one exactly what to fix before the brief.

## Context

### Why this exists

A consulting offering feels ready long before it is. Enthusiasm in a design conversation hides missing pieces — no stated price, deliverables that don't map to the phases, metrics that don't measure the stated problem, no named buyer who would actually pay. This skill makes that completeness read cold, in seconds, so the consultant doesn't carry a contradictory offering all the way into a product brief before noticing the gap.

### The cold sub-agent (load-bearing)

Scoring is done by a sub-agent (Agent tool) that receives **only the offering statement, the rubric, and the resolved calibration — never the calling conversation**. That isolation is the whole point: an inline assessment inherits the design chat's optimism and fills gaps the offering hasn't actually closed. A second adversarial sub-agent then tries to flip the verdict (over-credited element, missed contradiction, wrong gate call); only what survives is reported.

A future edit that "simplifies" this to inline scoring silently destroys the property that makes the skill worth having — the regression-pin example exists to catch that. If sub-agent spawning is genuinely unavailable, score inline but state that the cold-read property is degraded; never let inline become the silent default.

### The rubric: 9 elements

Each element is rated **Solid** (present and sharp), **Thin** (gestured at, not nailed down), or **Absent** (missing), with a one-line reason. These are the pieces any consulting offering must have before it's worth a brief.

| # | Element | Solid looks like | Absent looks like |
|---|---------|------------------|-------------------|
| 1 | Problem definition | A crisp statement of the client's problem and our read of it | "Companies struggle with change" — no specific pain |
| 2 | Deliverables | A clear breakdown of what the client actually receives | "Some advice and a workshop" — no artefact list |
| 3 | Price / model | A stated price or a defined pricing model | No number, no model |
| 4 | Timeline | How long the engagement takes | Open-ended |
| 5 | Phases | The staged structure of the engagement | One undifferentiated blob of work |
| 6 | Offering structure | How the offering itself is organised — its logical spine (modules, workstreams, the shape of the thing) | No spine; a list of activities |
| 7 | Metrics | How success is measured | "They'll be happier" — nothing measurable |
| 8 | Target buyer & fit | A specific buyer (role, org type, situation) and why it fits them | A whole function named in general — no named buyer |
| 9 | Proof / why this provider | Evidence the outcome lands and why a buyer should believe this provider delivers it | Asserted authority, no basis |

Elements 8 and 9 are the two most commonly missing: an offering can have a price, deliverables, and a timeline yet have no buyer who'd pay it and no reason to believe this provider over anyone else. Score those as hard as the rest.

### The two gates

Scored separately from the elements; either can cap an otherwise-complete offering. A checklist where all 9 boxes are ticked still fails if the pieces don't add up or no one will buy it — the gates catch that.

- **Gate A — Coherence.** Do the pieces add up? Price ↔ scope ↔ timeline ↔ phases must be internally consistent. A low fixed price against weeks of senior delivery, deliverables that don't map to any phase, metrics that don't measure the stated problem — each is a coherence failure even when every element is individually "present". Where a calibration day-rate band is supplied, check the price implies a sane day-rate against it.
- **Gate B — Buyer-willingness.** Is there a *named* buyer who would pay this price for this outcome — with the budget authority and a live enough pain to act now? A function "in general" is not a buyer; a specific role in a specific situation is. Money and motivation must sit in the same person.

A gate failure caps the verdict at **Refine** (or **Not-ready** if it fails hard). Both gates are reasoned-calls, not box-ticks.

### Backbone plus wildcard

Always score all 9 elements and both gates (the backbone). Also flag any offering-specific killer or unfair advantage outside the rubric (the wildcard) — a regulated-buyer constraint, a standout proof asset, a timing edge. Real offerings have idiosyncratic factors a fixed list misses.

### What's asserted vs judged

Partly-subjective output, so the eval line is explicit:

- **Mechanical (binary, asserted):** all 9 elements rated, the scorecard table present, both gates evaluated, a verdict label + element tally present, the single-biggest-gap present, the what-would-have-to-be-true present, and a cold sub-agent actually spawned.
- **Reasoned-call (judge / human-reviewed):** the per-element Solid/Thin/Absent ratings, the gate calls, the wildcard flags.

## Inputs

- **The offering** (required): a concrete consulting offering to assess. If only a vague theme is given, ask one clarifying question to get to a scorable offering, or score it and flag the unknowns.
- **Calibration** (optional): if `calibration.local.md` sits in this skill's directory, load the consultant's price bands, target buyers, proof base, and routing from it and pass them to the cold scorer — this tunes Gate A (coherence/day-rate sanity), element 8 (buyer), and element 9 (proof). If absent, use the generic defaults here and judge from what the user states.
- The rubric, gates, and output schema live in this file; the cold scorer is handed them in its spawn prompt.

## Process

1. **Check the trigger.** Fire only on a clear request to judge a specific consulting offering's readiness. On idle riffing or a passing mention, stay silent. Route a lifestyle/consumer product idea to a business-idea assessor; a finished methodology doc for committee review to a buyer-council review; a build request to a methodology builder; a change-programme artefact to a change-council review. Where `calibration.local.md` names the specific sibling skills, use those names.
2. **Load calibration.** Read `calibration.local.md` if present, else use the defaults here. Whatever you resolve tunes Gate A and elements 8/9 and is handed to the cold scorer.
3. **Extract a clean offering statement.** Self-contained, stripped of the conversation's framing and enthusiasm. This plus the rubric and resolved calibration is all the cold scorer receives.
4. **Spawn the cold scorer** (Agent tool, general-purpose). Hand it the offering statement, the 9 elements, the 2 gates, the wildcard instruction, the output schema, and the resolved calibration — never the calling conversation. It returns the filled scorecard, gate results, wildcard flags, verdict + tally, biggest gap, and what-would-have-to-be-true.
5. **Spawn the adversarial challenger** (Agent tool). Hand it the offering statement and the scorer's verdict; ask it to flip the result (over-credited element, missed contradiction, wrong gate call, missed wildcard).
6. **Synthesise.** Flip any element or gate the challenge convincingly overturns, and note the change. Produce the final report.
7. **Report** in the Output Format below. On **Ready** or **Strong**, recommend the product-brief gate as the next stage. On **Refine** or **Not-ready**, name the gaps and stop — no brief yet.

### Skill chain

Self-contained: spawns generic scorer + challenger sub-agents, calls no other named skill in this file. Defers OUT to a business-idea assessor (a lifestyle/consumer idea), a buyer-council review (a finished methodology doc), a methodology builder (a build), or a change-council review (a change artefact) when one fits better; the specific sibling-skill names live in `calibration.local.md`. Hands FORWARD to a product-brief gate on a Ready/Strong verdict.

### Decision points

- **Negative trigger** → do not fire, produce nothing.
- **Offering too thin to score** → score what's scorable, flag the unknowns, name what's needed. Don't invent confidence.
- **A gate fails** → cap the verdict at Refine (Not-ready if it fails hard); say so plainly.
- **Challenger flips an element or verdict tier** → adopt the change and say what flipped and why.

### Fallback behaviour

If sub-agent spawning is unavailable, score inline and state explicitly that the cold-read property is degraded because isolation couldn't be enforced. Inline must never become the silent default.

## Output Format

```
## Readiness assessment: [offering in one line]

| # | Element | Rating | Why |
|---|---------|--------|-----|
| 1 | Problem definition | Solid/Thin/Absent | ... |
| ... (all 9 elements) |

**Gate A — Coherence:** Pass / Fail — [do price ↔ scope ↔ timeline ↔ phases add up]
**Gate B — Buyer willingness:** Pass / Fail — [the named buyer who'd pay this, or why there isn't one]

**Wildcard:** [any offering-specific killer or unfair advantage outside the rubric, or "none"]

**Verdict: [NOT-READY / REFINE / READY / STRONG]** — [X] solid / [Y] thin / [Z] absent of 9; gates [results].

**Biggest gap:** [the single dominant thing holding it back, or for Strong, the one thing to watch.]

**What would have to be true to move forward:** [the constructive path to the next tier, or to the product brief.]
```

Verdict tiers (a guide, not a rigid cutoff): **STRONG** ≈ all 9 Solid and both gates pass; **READY** ≈ all 9 at least Thin with problem/deliverables/price/buyer Solid and both gates pass; **REFINE** ≈ 1-2 Absent or several Thin, or one gate marginal/failed; **NOT-READY** ≈ 3+ Absent, or a gate fails hard. **A gate failure caps the verdict at Refine or below regardless of the element tally.** Only Ready and Strong proceed to the product-brief gate.

## Constraints

- Rate every one of the 9 elements and both gates on every run. No partial scorecards.
- The scoring sub-agent receives only the offering statement, the rubric, and the resolved calibration — never the calling conversation. Load-bearing; do not remove.
- Always run the adversarial challenge pass before reporting.
- A gate failure caps the verdict — a structural cap, not a soft signal.
- State a verdict label AND the element tally AND the gate results together. A label alone is not enough.
- Always include the single biggest gap and the what-would-have-to-be-true.
- Flag wildcard factors outside the rubric; don't silently fold them into an element.
- On an under-specified offering, flag unknowns rather than fabricating a rating.
- Stay silent on the negative trigger. Mentioning an offering is not asking for a verdict.

## Examples

Each example lists binary pass criteria the output can be verified against. The same criteria are encoded in [`evals/evals.json`](evals/evals.json).

**Example 1 — "Assess this offering: a fixed-price 'HRIS readiness' diagnostic. I know it's a Workday pre-implementation health-check but I haven't set a price, a timeline, or how we'd measure success yet."**

Pass criteria:
- (a) All 9 elements appear in the scorecard with a Solid/Thin/Absent rating each.
- (b) Price, Timeline, and Metrics are each rated Absent.
- (c) Verdict label is NOT-READY or REFINE, accompanied by a solid/thin/absent-of-9 tally.
- (d) The biggest gap names the missing price / timeline / metrics, not a peripheral element.
- (e) A "what would have to be true to move forward" line is present and no product-brief handoff is recommended.

**Example 2 — "Score this methodology offer: a 3-phase, 15-day fixed-price change-adoption programme for CHROs at mid-market firms going live on Workday. £36k. Deliverables, phases, metrics and the proof base from past Workday programmes are all written up."**

Pass criteria:
- (a) All 9 elements rated.
- (b) Problem definition, Deliverables, Price, Timeline, Phases, Target buyer, and Proof are each rated Solid or Thin (none Absent).
- (c) Gate A (coherence) and Gate B (buyer-willingness) are each explicitly evaluated with a Pass or Fail.
- (d) Verdict label is READY or STRONG.
- (e) The product-brief gate is recommended as the next stage.

**Example 3 — Regression-pin: cold-read isolation (any offering, e.g. "Assess this offering: a quarterly retained 'HR-AI operating model' advisory for People Directors").**

Pass criteria:
- (a) A sub-agent is spawned to perform the scoring (not scored inline).
- (b) The sub-agent's spawn prompt contains the offering statement, the rubric, and the calibration only, with no content from the calling conversation.
- (c) The final output contains no detail that was only available in the surrounding conversation.
- (d) All 9 elements and both gates are scored, and a verdict label with a solid/thin/absent tally is present.

**Example 4 — Negative trigger: "I might productise that change-adoption thing one day, but anyway — back to the deck." (should NOT fire)**

Pass criteria:
- (a) The skill does not fire — no scorecard is produced.
- (b) No scoring sub-agent is spawned.
- (c) The response does not present a verdict; the skill stays silent.
