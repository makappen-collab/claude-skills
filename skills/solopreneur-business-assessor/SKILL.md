---
name: solopreneur-business-assessor
description: >
  Fires when the user asks for a go/no-go on a SPECIFIC business idea — "assess
  this idea", "run the rubric", "score this idea", "is this a good solo
  business", or any clear request to judge whether an idea is worth pursuing.
  Scores it cold against a fixed 9-axis rubric plus three gates
  (willingness-to-pay, AI-resilience, cost-of-entry), calibrated to a solo
  founder building with AI agents at lifestyle scale. A sub-agent scores in
  isolation from the calling conversation so the verdict isn't biased by the
  chat's enthusiasm; an adversarial sub-agent then challenges it. Output is a
  scorecard, a tiered verdict (Avoid / Hard / Viable / Strong) with the axis
  tally, the single biggest reason, and what would have to be true to make it
  work. Does NOT fire on idle riffing or a passing mention with no ask for a
  verdict — stay silent then. Defers to a methodology-review or change-programme
  skill if one fits the artefact better.
---

# Solopreneur Business Assessor

## Role

A business-idea stress-testing molecule. Takes one concrete idea and scores it cold against a fixed rubric, returning how hard it would be for a solo operator — building with AI agents, aiming at lifestyle-scale economics (~£20k/yr by default; override in `calibration.local.md`) — to make it work. The output is a decision aid that kills weak ideas fast and tells a promising one what would have to be true to work.

## Context

### Why this exists

A solo founder generates ideas faster than they can sanity-check them, and judges them by the excitement of the moment rather than their structure. Most ideas that feel good are hard for boring structural reasons — two-sided marketplaces, local liquidity, low willingness to pay, physical-world trust, expensive licences to operate. This skill makes that structural read cold, in seconds, so the founder doesn't re-derive it across four conversations.

### The cold sub-agent (load-bearing)

Scoring is done by a sub-agent (Agent tool) that receives **only the idea statement and the rubric — never the calling conversation**. That isolation is the whole point: an inline assessment inherits the context's enthusiasm and sunk-cost framing. A second adversarial sub-agent then tries to flip the verdict (mis-scored axis, wrong weighting, missed wildcard, wrong gate call); only what survives is reported.

A future edit that "simplifies" this to inline scoring silently destroys the property that makes the skill worth having — the regression-pin example exists to catch that. If sub-agent spawning is genuinely unavailable, score inline but state that the cold-read property is degraded; never let inline become the silent default.

### The rubric: 9 axes

Each axis is scored **Low-friction** (solo-friendly) or **High-friction** (hard), with a one-line reason. Fish at the low-friction end.

| # | Axis | Low-friction (easy) | High-friction (hard) |
|---|------|---------------------|----------------------|
| 1 | Sides | One-sided: just find demand | Two-sided marketplace: need supply AND demand at once |
| 2 | Liquidity geography | Global single pool | Local, rebuilt town by town |
| 3 | Willingness to pay | High | Low |
| 4 | Frequency | Recurring | One-off |
| 5 | Lock-in | Sticky / embedded | Leaks: parties swap contacts and cut you out |
| 6 | Moat type | Software / bits, scales solo | Trust + physical ops / atoms, needs humans, carries liability |
| 7 | Founder distribution & reach | Owns a channel into the market, OR the audience is concretely reachable (a postable problem, named venues, an acquisition route that pays back at the price point) | No channel AND no credible, affordable route in |
| 8 | Founder edge transfer | The founder's background, skills, and unfair advantages transfer to this domain | The founder's edge is irrelevant here |
| 9 | Shippability | A sellable v1 ships in ~2-4 weeks | Months/years to launch; scope balloons |

"AI makes it cheap to build" is never a point in favour — build cost was never the bottleneck for the hard cases; liquidity, distribution, trust and behaviour were.

Axes 7 and 8 are founder-specific: load the founder's channel and edge from `calibration.local.md` if present, else judge from what the user states.

**Axis 7 (distribution & reach) is the dominant axis; weight it heavily — but score reachability, not just current ownership.** Three states:

- **Owns a channel now** → Low-friction.
- **No channel, but a concrete costed route in** — a real postable problem, named venues where buyers gather, an acquisition channel (paid ads, SEO with real search volume, community posting) that pays back at the price point → score Low-to-mid; treat the cost as work to do, not a kill.
- **No channel AND no credible, affordable route** → High-friction. This is the only fatal case.

Vague "people probably want this somewhere" is the fatal case, not the reachable one. Marc Lou and Pieter Levels won on audience, but both built it from zero post by post — distribution is a flow you can manufacture, so credit a credible acquisition plan as reach. Axis 9 catches the other common death: scope balloons in the build and nothing launches.

### The three gates

Scored separately from the axes; any one can sink an otherwise-good idea.

- **Gate A — Willingness to pay.** Needs three things at once: the buyer has money, has a pain they're *driven* to fix, and this fixes it. Watch the trap where money and motivation sit in different people (tradespeople with money but no urgency; desperate ones with urgency but no money). "Has a budget" is not WTP. A paid, revenue-earning incumbent is positive evidence buyers pay — copying a proven paid model on cheaper / better / sharper-niche is lower-risk than creating a market. A crowded *paid* field is validation; a *free, feature-complete* incumbent is the opposite and fails Gate B. Establish which you face before reading competition as green or red.
- **Gate B — AI-resilience (not all-or-nothing).** Is the defensibility something a generic AI can't trivially copy? Two cases: *no moat at all* (thin wrapper, no distribution or route to it, a capable buyer who'll self-serve) = FAIL; *moat is distribution and brand, not code* (a wrapper where the founder owns or can credibly reach the channel and the buyer won't self-serve, e.g. PhotoAI) = a real but time-boxed window, not a fortress. Usability alone is a wedge, not a moat. **Lifestyle-scale calibration (load-bearing):** a classic moat is NOT required for a one-person ~£20k/yr service business — a cleaner has no moat and it's still a fine living. Do NOT fail Gate B merely because an idea is copyable or paid competitors exist; it fails only on a free feature-complete incumbent or a buyer who'll trivially self-serve.
- **Gate C — Cost of entry (hard kill-switch).** Can you start selling without spending more than the ~£20k target on the licence to operate? Heavy certifications (SOC 2, ISO 27001, FCA/CQC authorisation, mandatory pen-testing) or a GDPR burden needing a DPO can each exceed the year's target alone. Selling INTO a regulated space (the user carries the accreditation, your tool rides on it) stays light; becoming a regulated entity yourself (you hold the sensitive data or licence) is heavy from day one — favour the former. If Gate C fails, the verdict is AVOID regardless of the axes. Cheapest disqualifier to check, so check it early.

### Durability posture: time-boxed is fine

The rubric does NOT require a forever-business. For a lifestyle portfolio, any revenue earned is a win and builds are cheap, so a time-boxed earner that nets a few £k before the labs close the gap counts. Don't auto-AVOID an on-road idea or a wrapper — remove the durability bar, keep the distribution bar (owns a channel, or has a concrete costed route to one).

### Backbone plus wildcard

Always score all 9 axes and all three gates (the backbone). Also flag any idea-specific killer or unfair advantage that sits outside the rubric (the wildcard) — real businesses have idiosyncratic factors a fixed list misses.

### What's asserted vs judged

Partly-subjective output, so the eval line is explicit:

- **Mechanical (binary, asserted):** all 9 axes scored, the scorecard table present, all three gates evaluated, a verdict label + axis tally present, the single-biggest-reason present, the what-would-have-to-be-true present, and a cold sub-agent actually spawned.
- **Reasoned-call (judge / human-reviewed):** the per-axis High/Low calls, the gate calls, the wildcard flags.

## Inputs

- **The idea** (required): a concrete idea to assess. If only a vague theme is given, ask one clarifying question to get to a scorable idea, or score it and flag the unknowns.
- **Founder calibration** (optional): if `calibration.local.md` sits in this skill's directory, load the founder's edge, owned channels, and target economics from it and pass them to the cold scorer — this tunes axes 7 and 8 and Gate C. If absent, use the generic defaults here and judge axes 7/8 from what the user states.
- The rubric, gates, and output schema live in this file; the cold scorer is handed them in its spawn prompt.

## Process

1. **Check the trigger.** Fire only on a clear request to judge a specific idea. On idle riffing or a passing mention, stay silent. If the artefact is a methodology doc or change-programme deliverable, defer to a dedicated review skill if one fits.
2. **Load calibration.** Read `calibration.local.md` if present, else use the defaults here. Whatever you resolve tunes axes 7/8 and Gate C and is handed to the cold scorer.
3. **Extract a clean idea statement.** Self-contained, stripped of the conversation's framing and enthusiasm. This plus the rubric and resolved calibration is all the cold scorer receives.
4. **Spawn the cold scorer** (Agent tool, general-purpose). Hand it the idea statement, the 9 axes, the 3 gates, the wildcard instruction, the output schema, and the resolved calibration — never the calling conversation. It returns the filled scorecard, gate results, wildcard flags, verdict + tally, biggest reason, and what-would-have-to-be-true.
5. **Spawn the adversarial challenger** (Agent tool). Hand it the idea statement and the scorer's verdict; ask it to flip the result (mis-scored axis, over/under-weighting, missed wildcard, wrong gate call).
6. **Synthesise.** Flip any axis or gate the challenge convincingly overturns, and note the change. Produce the final report.
7. **Report** in the Output Format below.

### Skill chain

Self-contained: spawns generic scorer + challenger sub-agents, calls no other named skill. Defers OUT to a methodology-document or change-programme review skill when one is available and its trigger fits better.

### Decision points

- **Negative trigger** → do not fire, produce nothing.
- **Idea too thin to score** → score what's scorable, flag the unknowns, name what's needed. Don't invent confidence.
- **Gate C fails** → verdict is AVOID regardless of axis tally; say so plainly.
- **Challenger flips an axis or verdict tier** → adopt the change and say what flipped and why.

### Fallback behaviour

If sub-agent spawning is unavailable, score inline and state explicitly that the cold-read property is degraded because isolation couldn't be enforced. Inline must never become the silent default.

## Output Format

```
## Assessment: [idea in one line]

| # | Axis | Friction | Why |
|---|------|----------|-----|
| 1 | Sides | High/Low | ... |
| ... (all 9 axes) |

**Gate A — Willingness to pay:** Pass / Fail — [reason, incl. money-vs-motivation check]
**Gate B — AI-resilience:** Pass / Fail — [the moat, or why there isn't one]
**Gate C — Cost of entry:** Pass / Fail — [licence-to-operate cost vs target profit; note if a hard kill]

**Wildcard:** [any idea-specific killer or unfair advantage outside the rubric, or "none"]

**Verdict: [AVOID / HARD / VIABLE / STRONG]** — [X]/9 axes high-friction, [gate results].

**Biggest reason:** [the single dominant factor driving the verdict.]

**What would have to be true to make it work:** [the constructive path, or "no realistic path for a solo founder".]
```

Verdict tiers (a guide, not a rigid cutoff): **STRONG** ≈ ≤2 high-friction and all gates pass; **VIABLE** ≈ 3-4 high-friction, or one soft gate marginal; **HARD** ≈ 5-7 high-friction, or one soft gate fails; **AVOID** ≈ 8-9 high-friction, or both soft gates fail. **Gate C is a hard kill-switch: if it fails, the verdict is AVOID on its own.**

## Constraints

- Score every one of the 9 axes and all three gates on every run. No partial scorecards.
- The scoring sub-agent receives only the idea statement and the rubric, never the calling conversation. Load-bearing; do not remove.
- Always run the adversarial challenge pass before reporting.
- A failed Gate C forces AVOID regardless of axis tally — a structural kill-switch, not a soft signal.
- State a verdict label AND the axis tally AND the gate results together. A label alone is not enough.
- Always include the single biggest reason and the what-would-have-to-be-true.
- Score axis 7 on reach, not just current ownership: a concrete, costed route is a budgeted price, not a disqualifier. Only "no channel AND no credible route in" is fatal.
- Flag wildcard factors outside the rubric; don't silently fold them into an axis.
- On an under-specified idea, flag unknowns rather than fabricating a score.
- Stay silent on the negative trigger. Mentioning an idea is not asking for a verdict.

## Examples

Each example lists binary pass criteria the output can be verified against. The same criteria are encoded in [`evals/evals.json`](evals/evals.json).

**Example 1 — "Assess this idea: an Airtasker-style marketplace for tradespeople outside London."**

Pass criteria:
- (a) All 9 axes appear in the scorecard with a friction rating each.
- (b) Sides, Liquidity geography, and Moat type are all rated High-friction.
- (c) Verdict label is AVOID or HARD, accompanied by an X/9 tally.
- (d) The biggest reason names the two-sided / local-liquidity / marketplace dynamic.
- (e) A "what would have to be true" line is present.

**Example 2 — "Score this idea: a vertical project-management tool ('Linear for X') for a knowledge-work niche the founder already understands well."**

Pass criteria:
- (a) All 9 axes scored.
- (b) Sides and Liquidity geography are rated Low-friction.
- (c) Founder edge transfer (axis 8) is rated Low-friction, given the niche is one the founder understands.
- (d) Gate B and Gate C are each explicitly evaluated with a Pass or Fail.
- (e) Verdict label is VIABLE or STRONG.

**Example 3 — Regression-pin: cold-read isolation (any idea, e.g. "Assess this idea: a subscription compliance-certificate tool for MCS-registered heat-pump installers").**

Pass criteria:
- (a) A sub-agent is spawned to perform the scoring (not scored inline).
- (b) The sub-agent's spawn prompt contains the idea statement and rubric only, with no content from the calling conversation.
- (c) The final output contains no detail that was only available in the surrounding conversation.
- (d) All 9 axes and all three gates are scored, and a verdict label with an X/9 tally is present.

**Example 4 — Negative trigger: "Anyway, I'm still half-thinking about that trades thing, but let's move on." (should NOT fire)**

Pass criteria:
- (a) The skill does not fire — no scorecard is produced.
- (b) No scoring sub-agent is spawned.
- (c) The response does not present a verdict; the skill stays silent.
