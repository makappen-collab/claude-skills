# Claude Code skills

A small, curated set of [Claude Code](https://claude.com/claude-code) skills,
shared publicly. Each skill is a self-contained folder with a `SKILL.md` that
tells Claude when to fire and how to behave.

> This repo is auto-generated. The skills are mirrored from a private source on
> every update, so direct pushes here may be overwritten — open an issue for
> bugs or suggestions rather than a PR.

## Install a skill

Copy any skill folder into your Claude Code skills directory:

```bash
# global (all projects)
cp -r skills/<skill-name> ~/.claude/skills/<skill-name>

# or per-project
cp -r skills/<skill-name> .claude/skills/<skill-name>
```

Start (or restart) Claude Code and it will pick the skill up.

## Skills in this repo

### `solopreneur-business-assessor`

Scores a concrete business idea cold against a fixed 9-axis rubric plus three
gate tests (willingness-to-pay, AI-resilience, cost-of-entry), tuned for a solo
founder building with AI agents at lifestyle scale. It spawns an isolated
sub-agent that never sees the chat that produced the idea, so the verdict isn't
swayed by your enthusiasm, then runs an adversarial pass that tries to flip the
result before reporting. Output is a scorecard, a tiered verdict (Avoid / Hard /
Viable / Strong), the single biggest reason, and what would have to be true to
make it work.

Optional: drop a `calibration.local.md` in the skill folder with your own edge,
channels and target economics to tune axes 7-8 and the cost gate to you.

### `pptx-render-safe`

Production discipline for PowerPoint decks built in code with `python-pptx`. It
encodes the trap where "shrink text to fit" (autofit) previews cleanly in
LibreOffice but silently overflows its boxes in real PowerPoint and Keynote, and
fixes it by baking explicit font sizes. Ships a reusable text-fitting helper
(`scripts/fit_text.py`) and a render-to-images verification workflow so you prove
the deck is clean before handing it over.

Optional: drop a `brand.local.md` in the skill folder pointing at your default
brand-template folder so the skill resolves your palette and fonts automatically.

## Licence

[MIT](LICENSE).
