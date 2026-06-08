---
name: solopreneur-business-assessor
description: >
  Fires when the user asks for a go/no-go on a SPECIFIC business idea — trigger
  phrases "assess this idea", "run the rubric", "score this idea", "is this a
  good solo business", or any clear request to judge whether an idea is worth
  pursuing. Scores the idea COLD against a fixed 9-axis rubric plus three gate
  tests (willingness-to-pay, AI-resilience, cost-of-entry), calibrated to a solo
  founder building with AI agents at lifestyle scale. Spawns an isolated
  sub-agent that never sees the calling conversation, so the verdict isn't biased
  by the enthusiasm of the chat that produced the idea, then an adversarial
  sub-agent challenges the verdict before it's reported. Output is a scorecard
  table, a tiered verdict (Avoid / Hard / Viable / Strong) with the axis tally,
  the single biggest reason, and what would have to be true to make it work. Use
  this WHENEVER the user is weighing a concrete business idea, even if they don't
  say "rubric". Does NOT fire when the user is merely riffing on or mentioning an
  idea in passing without asking for a verdict — stay silent then. Defers to a
  methodology-document review skill or a change-programme review skill if one is
  available and fits the artefact better.
---

# Solopreneur Business Assessor

## Role

A business-idea stress-testing molecule. Takes one concrete business idea and scores it cold against a fixed rubric, returning how hard it would be for the founder — a solo operator building with AI coding agents, aiming at lifestyle-scale economics (a modest annual profit target, ~£20k/yr by default; override it in `calibration.local.md`) — to make it work.

The output is a decision aid for the founder, not a deliverable. It exists to kill weak ideas fast and to tell a promising idea what would have to be true to work.

## Context

### Why this exists

A solo founder generates business ideas faster than they can sanity-check them, and the failure mode is predictable: the idea that feels exciting in the moment is judged by that excitement rather than by its structure. Most ideas that feel good are hard for a solo founder for boring structural reasons (two-sided marketplaces, local liquidity, low willingness to pay, physical-world trust, expensive licences to operate). This skill makes the structural judgement, cold, in 30 seconds, so the founder does not spend four conversations re-deriving it each time.

### The load-bearing design: a cold sub-agent

The scoring is done by a sub-agent spawned via the Agent tool that receives **only the idea statement and the rubric — never the calling conversation**. This is the entire point. An assessment done inline, in the same context that produced the idea, inherits that context's enthusiasm and sunk-cost framing. The isolation is what makes the read honest.

A future edit that "simplifies" this to inline scoring would silently destroy the property that makes the skill worth having. The regression-pin example exists to catch exactly that. If sub-agent spawning is genuinely unavailable, score inline but state plainly that the cold-read property is degraded — never let inline become the silent default.

After the cold scorer returns, a second adversarial sub-agent tries to flip the verdict (find a mis-scored axis, an over- or under-weighting, a missed wildcard, a wrong gate call). Only what survives that challenge is reported. The discipline is non-performative: isolated advisers plus a falsification pass, not a panel that rubber-stamps the first verdict.

### The rubric: 9 axes

Each axis is scored **Low-friction** (solo-friendly) or **High-friction** (hard for a solo founder), with a one-line reason. Fish at the low-friction end.

| # | Axis | Low-friction (easy) | High-friction (hard) |
|---|------|---------------------|----------------------|
| 1 | Sides | One-sided: just find demand | Two-sided marketplace: need supply AND demand at once |
| 2 | Liquidity geography | Global single pool | Local, rebuilt town by town |
| 3 | Willingness to pay | High | Low |
| 4 | Frequency | Recurring | One-off |
| 5 | Lock-in | Sticky / embedded | Leaks: parties swap contacts and cut you out |
| 6 | Moat type | Software / bits, scales solo | Trust + physical ops / atoms, needs humans, carries liability |
| 7 | Founder distribution & reach | The founder owns a channel into the market, OR the audience is concretely reachable — a postable problem plus identifiable venues (named communities, real search demand) and an acquisition route that pays back at the price point | No existing channel AND no credible, affordable route in |
| 8 | Founder edge transfer | The founder's edge applies: their specific background, skills, and unfair advantages transfer to this domain (load the founder's actual edge from `calibration.local.md` if present) | The founder's edge is irrelevant here |
| 9 | Shippability | A sellable v1 ships in ~2-4 weeks | Months/years to launch; scope balloons |

Axes 7 and 8 are founder-specific: they depend on who is building it. Load the founder's actual channel and edge from `calibration.local.md` if it exists; otherwise judge them from what the user states about themselves and the idea. Axis 7 measures **reach, not just ownership** — score it on whether the audience can be *got to*, not only on whether the founder already has it. Three states:

- **(a) Owns a channel now** → Low-friction.
- **(b) No channel now, but a concrete, costed route in** — a real problem worth posting about, named venues where the buyers already gather, and an acquisition channel (paid ads, SEO with real search volume, community posting) that pays back at the price point → a *budgeted cost*. Score it Low-to-mid friction and treat the cost as work to do, not a kill.
- **(c) No channel AND no credible, affordable route in** → High-friction.

The thing that's fatal is (c), not (b). A real problem with an audience that's out there to be tapped scores as reachable, even if the founder hasn't tapped it yet. What does NOT earn credit is a vague "people probably want this somewhere" — reach has to be concrete (you can name the venues and the channel), or it's case (c).

**Axis 7 (distribution & reach) is the dominant axis. Weight it heavily — but weight reachability, not just current ownership.** Distribution is the binding constraint for most solo products, yet the canonical cases cut both ways: Marc Lou and Pieter Levels are cited as winning on audience, but both *built* those audiences from zero, post by post — distribution was a flow they manufactured, not a stock they were handed. So credit a credible acquisition plan as reach. What stays fatal is no channel *and* no plan — "build it and they will come" with no route to the buyer. A strong score everywhere else with no distribution and no way to get it is still a hard road. Axis 9 (shippability) catches the build-death failure: most solo projects die in the build, not the market, when scope balloons and nothing ever launches.

### The three gate tests

Scored separately from the 9 axes, because any one can sink an otherwise-good idea.

- **Gate A — Willingness to pay.** Real WTP needs three things at once: the buyer has money, has an unsolved pain they are *driven* to fix, and this thing fixes it. Watch for the trap where money and motivation sit in different people (busy tradespeople have money but no urgency; desperate ones have urgency but no money). "Has a budget" is not WTP. Proven-demand shortcut — distinguish paid from free incumbents. An existing **paid** competitor that demonstrably earns money is positive evidence that buyers pay, so copying a proven paid model and winning on cheaper, better, or a sharper niche fit (ideally more than one of the three) is lower-risk than creating a market from scratch. A crowded *paid* field is validation, not a warning. A **free, feature-complete** incumbent is the opposite: there is nothing to charge against, so copying it is not a path (that case fails Gate B). Establish which kind of incumbent you face before reading competition as green or red.
- **Gate B — AI-resilience (not all-or-nothing).** Is the defensibility something a generic AI cannot trivially copy — proprietary or curated data, network effects, deep integration, a regulated workflow, trust/brand, or an embedded workflow? A thin prompt-wrapper has no *technical* moat, but it isn't automatically dead. Separate two cases: (i) *no moat at all* (thin wrapper, no distribution and no credible route to it, a capable buyer who'll self-serve) is a FAIL; (ii) *moat is distribution and brand, not code* (a wrapper where the founder owns **or can credibly reach** the channel and the buyer can't or won't self-serve, e.g. PhotoAI) is a real but time-boxed opportunity, scored as a window not a fortress (read with the Durability posture below). Usability alone is still only a wedge, not a moat: it is highly copyable and AI makes polished UIs cheap. **Lifestyle-scale calibration (load-bearing):** a classic moat is NOT required for a one-person, ~£20k/yr service business. Plenty of viable solo businesses have none — a cleaner has no moat, anyone can become a cleaner, the market is full of them, and it is still a fine one-person living. Competition is proof of demand, not a reason to stay out. Do NOT fail Gate B merely because an idea is copyable or because paid competitors exist. Gate B fails only in the two real cases: a *free, feature-complete* incumbent that leaves nothing to charge against, or a capable buyer who will trivially self-serve. A space with real demand, a reachable market, and a genuinely good service clears it — that is the whole bar.
- **Gate C — Cost of entry (hard kill-switch).** Can you start selling without spending more than the ~£20k target profit on the licence to operate? Heavy certifications (SOC 2, ISO 27001, FCA/CQC authorisation, mandatory pen-testing, sector accreditation) or a GDPR burden needing a DPO and formal audits can each exceed the whole year's target on their own. If this gate fails, the verdict is AVOID regardless of how the axes score. Key distinction in regulated spaces: **selling INTO a regulated space** (the user carries the accreditation; your tool rides on it) stays light; **becoming a regulated entity yourself** (you hold the sensitive data or the licence) is heavy from day one. Favour the former. Cost of entry is the cheapest disqualifier to check, so check it early.

### Durability posture: time-boxed is fine

The rubric does NOT require a forever-business. For a lifestyle portfolio the success test is any revenue earned, and builds are cheap, so a time-boxed on-road earner that nets a few £k before the labs close the gap is a win. Do not auto-AVOID an idea just because it is "on the road" or a wrapper. The guardrail: time-boxed still needs distribution to monetise the window, so remove the durability bar, keep the distribution bar — where "has distribution" means owns a channel *or* has a concrete, costed route to one. Score an on-road idea that has, or can credibly reach, distribution as a real, windowed opportunity rather than a kill.

### Backbone plus wildcard

Always score all 9 axes and all three gates (the backbone). Also flag any idea-specific killer or unfair advantage that sits outside the rubric (the wildcard). Real businesses have idiosyncratic factors a fixed list misses; the wildcard slot catches them without diluting the comparable backbone.

### What is asserted vs what is judged

This skill produces a partly-subjective output, so the eval line is drawn explicitly:

- **Mechanical layer (binary-checkable, asserted):** all 9 axes scored, the scorecard table present, all three gates evaluated, a verdict label plus axis tally present, the single-biggest-reason present, the what-would-have-to-be-true present, and a cold sub-agent actually spawned.
- **Reasoned-call layer (human-reviewed, NOT asserted as binary):** the per-axis High/Low judgement, the gate calls, and the wildcard flags. These are the scorer's reasoned opinion; the user reviews them.

### Bad patterns the skill must resist

- Being swayed by the pitcher's enthusiasm. (This is why the scorer is cold and isolated.)
- Treating "AI makes it cheap to build" as a point in favour. Build cost was never the bottleneck for the hard cases; liquidity, distribution, trust and behaviour were.
- Confusing "has money" with willingness to pay (Gate A).
- Treating all incumbents alike, or treating competition as a reason to stay out. A paid, revenue-earning incumbent is validation — someone already proved buyers pay — and the move is to enter and serve a slice of that demand well (cheaper, better, more focused, more available, or just present), NOT to find a defensible moat. A solopreneur service business does not need a moat or a unique niche; it needs demand it can reach and a good service. The only incumbent that is a real blocker is a *free, feature-complete* one, because there is nothing to charge against. Check which of the two you face before scoring.
- Treating usability as a moat, or auto-failing every wrapper (Gate B). A thin wrapper with no distribution, no route to it, and a capable buyer fails; a wrapper with distribution (owned or credibly reachable) and a non-self-serving buyer is a windowed opportunity, not a kill.
- Auto-AVOIDing on-road or time-boxed ideas. For a lifestyle portfolio, a windowed earner is fine when distribution exists or is credibly reachable (see the Durability posture).
- Scoring axis 7 purely on what the founder already owns and ignoring a concrete, costed route to the audience. A real problem with a reachable-but-not-yet-reached audience is case (b), a budgeted cost — not the fatal case (c). Only score it fatal when there is no channel AND no credible way in.
- Forgetting the licence-to-operate cost — a space can score well on every axis and still be shut by Gate C.
- Fabricating confidence on an under-specified idea. Flag the unknowns and say what's needed to score them, rather than guessing.

## Inputs

- **The idea** (required): a concrete business idea to assess. If only a vague theme is given, ask one clarifying question to get to a scorable idea, or score it and flag the unknowns.
- **Founder calibration** (optional): if a `calibration.local.md` file sits in this skill's directory, load the founder's edge, owned channels, and target economics from it and pass them to the cold scorer — this is what tunes axes 7 and 8 and Gate C. If it's absent, fall back to the generic defaults in this file and judge axes 7/8 from what the user states about themselves.
- **Any founder-specific context** (optional): if the idea sits in a domain the user has unusual access to, note it — it changes axes 7 and 8.
- The rubric, gates, and output schema are carried in this file; the cold scorer is handed them in its spawn prompt.

## Process

1. **Check the trigger.** Fire only on a clear request to judge a specific idea (see description). If the user is mentioning or riffing on an idea in passing with no ask for a verdict, stay silent. If the artefact is a methodology document or a change-programme deliverable, defer to a dedicated review skill for that if one is available.
2. **Load calibration.** If `calibration.local.md` exists in this skill's directory, read the founder's edge, owned channels, and target economics from it. Otherwise use the generic defaults in this file. Whatever you resolve here is what tunes axes 7 and 8 and Gate C, and it is handed to the cold scorer in step 4.
3. **Extract a clean idea statement.** Write a self-contained description of the idea, stripped of the surrounding conversation's framing and enthusiasm. This statement, plus the rubric and the resolved calibration, is the only thing the cold scorer receives.
4. **Spawn the cold scorer** (Agent tool, general-purpose subagent). Hand it: the idea statement, the 9 axes, the 3 gates, the wildcard instruction, the output schema, and the resolved founder calibration (edge, channels, target economics). Do NOT include the calling conversation. It returns the filled scorecard, gate results, wildcard flags, verdict label + tally, biggest reason, and what-would-have-to-be-true.
5. **Spawn the adversarial challenger** (Agent tool). Hand it the idea statement and the cold scorer's verdict. Ask it to try to flip the result: find a mis-scored axis, an over/under-weighting, a missed wildcard, a wrong gate call. It returns specific challenges.
6. **Synthesise.** Reconcile the challenge against the score. Flip any axis or gate the challenge convincingly overturns, and note the change. Produce the final report.
7. **Report** in the Output Format below.

### Skill chain

Self-contained: spawns generic scorer + challenger sub-agents, calls no other named skill. Defers OUT to a methodology-document review skill or a change-programme review skill when one is available and its trigger fits the artefact better.

### Decision points

- **Negative trigger** → do not fire, produce nothing.
- **Idea too thin to score** → score what's scorable, flag the unknowns, name what's needed. Do not invent confidence.
- **Gate C fails** → verdict is AVOID regardless of axis tally; say so plainly.
- **Challenger flips an axis or the verdict tier** → adopt the change and say what flipped and why.

### Fallback behaviour

If sub-agent spawning is unavailable, score inline and state explicitly in the output that the cold-read property is degraded because isolation could not be enforced. Inline must never become the silent default.

## Output Format

```
## Assessment: [idea in one line]

| # | Axis | Friction | Why |
|---|------|----------|-----|
| 1 | Sides | High/Low | ... |
| ... (all 9 axes) |

**Gate A — Willingness to pay:** Pass / Fail — [reason, incl. money-vs-motivation check]
**Gate B — AI-resilience:** Pass / Fail — [the moat, or why there isn't one]
**Gate C — Cost of entry:** Pass / Fail — [licence-to-operate cost vs the founder's target profit; note if it's a hard kill]

**Wildcard:** [any idea-specific killer or unfair advantage outside the rubric, or "none"]

**Verdict: [AVOID / HARD / VIABLE / STRONG]** — [X]/9 axes high-friction, [gate results].

**Biggest reason:** [the single dominant factor driving the verdict.]

**What would have to be true to make it work:** [the constructive path, or "no realistic path for a solo founder" if there isn't one.]
```

Verdict tiers, as a guide (the scorer uses judgement, not a rigid cutoff): **STRONG** ≈ ≤2 high-friction axes and all three gates pass; **VIABLE** ≈ 3-4 high-friction, or one soft gate marginal; **HARD** ≈ 5-7 high-friction, or one soft gate fails; **AVOID** ≈ 8-9 high-friction, or both soft gates fail. **Gate C is a hard kill-switch: if it fails, the verdict is AVOID on its own, whatever the axes say.**

## Constraints

- Score every one of the 9 axes and all three gates on every run. No partial scorecards.
- The scoring sub-agent receives only the idea statement and the rubric, never the calling conversation. This is the load-bearing property; do not remove it.
- Always run the adversarial challenge pass before reporting.
- A failed cost-of-entry gate (Gate C) forces an AVOID verdict regardless of the axis tally. It is a structural kill-switch, not a soft signal.
- State a verdict label AND the axis tally AND the gate results together. A label alone is not enough.
- Always include the single biggest reason and the what-would-have-to-be-true.
- Score axis 7 on reach, not just current ownership: a concrete, costed route to the audience is a budgeted price, not an automatic disqualifier. Only "no channel AND no credible route in" is fatal.
- Flag wildcard factors outside the rubric; do not silently fold them into an axis.
- On an under-specified idea, flag unknowns rather than fabricating a score.
- Stay silent on the negative trigger. Mentioning an idea is not asking for a verdict.

## Examples

Each example lists binary pass criteria — yes/no checks the output can be verified against. The same criteria are encoded in [`evals/evals.json`](evals/evals.json).

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
- (d) Gate B (AI-resilience) and Gate C (cost of entry) are each explicitly evaluated with a Pass or Fail.
- (e) Verdict label is VIABLE or STRONG.

**Example 3 — Regression-pin: cold-read isolation (any idea, e.g. "Assess this idea: a subscription compliance-certificate tool for MCS-registered heat-pump installers").**

Pass criteria:
- (a) A sub-agent is spawned to perform the scoring (not scored inline).
- (b) The sub-agent's spawn prompt contains the idea statement and rubric only, with no content from the calling conversation.
- (c) The final output contains no detail that was only available in the surrounding conversation, confirming the scorer judged the idea on its own terms.
- (d) All 9 axes and all three gates are scored, and a verdict label with an X/9 tally is present.

**Example 4 — Negative trigger: "Anyway, I'm still half-thinking about that trades thing, but let's move on." (should NOT fire)**

Pass criteria:
- (a) The skill does not fire — no scorecard is produced.
- (b) No scoring sub-agent is spawned.
- (c) The response does not present a verdict; the skill stays silent and lets the conversation continue.
