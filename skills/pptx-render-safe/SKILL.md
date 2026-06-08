---
name: pptx-render-safe
description: >
  Use whenever you build, generate, template, or repair a PowerPoint (.pptx) deck
  in code with python-pptx (branded methodology decks, any script that
  emits slides from data), or verify such a generated deck before handing it over.
  It encodes the hard-won rule that python-pptx "shrink text to fit" (autofit)
  silently overflows in PowerPoint and Keynote, so font sizes must be baked
  explicitly; it requires sourcing the deck's palette, type and layout from the
  project's brand template; and it
  carries the render-to-images verification workflow plus a reusable text-fitting
  helper. Fire it even when the user only says "build the
  slide deck", "generate the pptx", "the text is overflowing the boxes",
  "regenerate the deck", or "render the deck" — anytime python-pptx is in play.
  Do NOT fire for reading or extracting text/thumbnails from an existing .pptx
  (use the built-in pptx skill), for HTML / Canva / Google Slides decks, or for a
  purely manual edit made in the PowerPoint app with no code involved.
---

# pptx-render-safe

## Role

You are the production discipline for PowerPoint decks built in code with
python-pptx. Your single job: make the generated `.pptx` render identically, with
no text overflow, in PowerPoint, Keynote, Quick Look and the exported PDF — and
prove it before the deck is handed over. You do not judge visual taste; you
guarantee the mechanics.

## Context

### The failure this skill exists to prevent

A python-pptx deck that uses "shrink text to fit" looks perfect in the PDF
preview and overflows its boxes in the real PowerPoint file. Here is why.

| Step | What happens |
|---|---|
| You set `tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE` | python-pptx writes an OOXML `<a:normAutofit/>` element with **no `fontScale`** attribute. It records the *intent* to shrink, not the *amount*. |
| PowerPoint / Keynote open the file | They render the text at **full size**. They only compute and apply the shrink when a human clicks into and edits the box — not on load. So the text overflows. |
| LibreOffice opens the file (incl. `soffice --convert-to pdf`) | It **does** recompute the scale on load. So the PDF, and any images made from it, look correct. |

The trap: the renderer you use to preview (LibreOffice) is the one renderer that
hides the bug. The renderer the client uses (PowerPoint) is the one that shows
it. A clean preview means nothing while autofit is still in the generator.

### The fix: bake explicit sizes, never autofit

Remove autofit entirely and set an explicit font size that genuinely fits the
box. Then every renderer agrees — there is no scale left to compute — and the
preview becomes faithful.

The bundled helper does the sizing: [`scripts/fit_text.py`](scripts/fit_text.py)
exposes `fit_size(items, width_in, height_in, *, max_size, min_size=9.0,
line_spacing=1.3, space_after_pt=0.0)`. It estimates the wrapped line count from
character counts and returns the largest size (stepping down from `max_size`)
that fits; it returns `max_size` unchanged when the text already fits. Use it:

```python
from fit_text import fit_size          # scripts/fit_text.py on sys.path
from pptx.util import Pt
size = fit_size(body_text, width_in=4.97, height_in=1.1, max_size=14)
run.font.size = Pt(size)               # explicit. No tf.auto_size anywhere.
```

Its calibration constants `CHAR_W = 0.66` and `SAFETY = 0.94` are load-bearing,
tuned against real rendered decks. Treat them as fixed unless you re-calibrate
against rendered output and document it; nudging them re-opens the overflow bug.

When a fixed-height card holds variable text, give the card enough height that
the floor font stays readable. Two side-by-side cards with very different text
lengths will land on different sizes (the fuller one smaller) — that is correct
and by design, not an inconsistency to "fix" by forcing one size.

### Brand fidelity — build from the project's brand template

A deck is only "produced correctly" if it is on-brand. The palette, typography,
wordmark/logo and layout must come from the canonical brand template that governs
the project you are working in — sourced and verified against it, never invented
or eyeballed.

- **Find the governing brand first — always resolve the latest, never pin a
  version.** The source of truth is the project's brand-template folder. Point at
  the folder, not a fixed version: templates get revised over time, and superseded
  versions typically move to an `Archive/`, so resolve the highest-numbered file at
  build time rather than naming one in the generator. Resolve it deterministically:

  ```bash
  BRAND_DIR="/path/to/your project's brand template folder"   # the folder, not a pinned file
  TEMPLATE=$(ls "$BRAND_DIR"/*\ Deck\ Template\ v*.pptx | sort -V | tail -1)
  GUIDE=$(ls "$BRAND_DIR"/*\ Brand\ Guidelines\ v*.pdf  | sort -V | tail -1)
  ```

  The template carries layouts, slide masters and theme; the guidelines carry
  palette hex, type scale, spacing and wordmark rules. If a `brand.local.md` file
  sits in this skill's directory, it names your default brand-template folder —
  use it when the project doesn't specify its own. If no governing template is
  findable, ask which brand applies — do not guess a palette.
- **Two ways to honour it, both valid.** Either build on the resolved template
  `.pptx` as the base (`Presentation(template_path)`) so masters, theme colours
  and fonts carry through; or lift the exact tokens (hex, font names, spacing)
  from the resolved guidelines into the generator's constants. Either way, read
  the values fresh from the latest file each build; if you cache tokens as
  constants, record which guidelines version they came from (a comment) so a
  later reviewer can spot when the brand has moved on and refresh them. The
  non-negotiable: every colour and font traces to the current canonical source,
  not to memory or a stale copy.
- **Verify against it.** In the render sweep, check the palette, fonts and
  wordmark match the template — a wrong coral or a substituted font is a defect,
  the same as overflow. Note the font-substitution gotcha: LibreOffice may swap
  the brand fonts (e.g. Manrope, JetBrains Mono) for look-alikes in the PDF, so
  confirm fonts in PowerPoint/Keynote, not only in the PDF preview.

### Editability — these stay native PowerPoint files

A python-pptx-generated `.pptx` is a fully native, hand-editable PowerPoint file:
every text box, shape and colour is real and editable, nothing is flattened or
locked. Two tradeoffs to state plainly to whoever owns the deck:

- **The code is the source of truth.** Re-running the generator overwrites manual
  edits. Make durable changes in the source (the YAML/script), and treat any
  hand-edits in PowerPoint as one-off final touches you will not regenerate over.
- **Baked sizes don't auto-shrink.** If someone later types a lot more text into a
  box by hand, it will not auto-shrink — they resize it, or PowerPoint recomputes
  that one box when they click into it. This is an acceptable trade, because
  autofit was broken in generated files anyway.

### What is asserted vs reviewed by a human

The checks here are **mechanical and binary**: autofit absent, sizes explicit,
the overflow sweep run and clean, helper constants intact, and the brand values
(palette hex, fonts, wordmark) traceable to the project's canonical template.
What stays a human judgement is composition and taste — visual hierarchy, whether
a slide *reads well*, whether the design lands. Assert the mechanics; leave the
aesthetics to review.

## Inputs

- The project's brand template/guidelines — the one current file of each type in
  the project's brand folder (superseded versions archived). Resolve them by
  listing the folder, never by a version-pinned filename. A `brand.local.md` in
  this skill's directory, if present, names your default brand folder.
- A python-pptx generator (a script that builds the `.pptx`), or a generated deck
  to verify.
- `scripts/fit_text.py` importable by the generator (add its dir to `sys.path`).
- For verification: LibreOffice (`soffice`) for `pptx -> pdf`, and `pdftoppm`
  (Poppler) for `pdf -> images`.

## Process

### 1. Establish the governing brand template

Identify the brand that governs the project before building — its own brand kit
or template folder (resolve the current file of each type by listing the folder,
never a version-pinned name; superseded versions usually live in an `Archive/`).
If a `brand.local.md` is present in this skill's directory, it names your default
brand folder to fall back on. If there's no findable template, ask which brand
applies. Source the palette, fonts, wordmark and layout from it: build on the
template `.pptx`, or pin exact tokens lifted from the guidelines. Never
approximate a brand colour.

### 2. Build (or repair) the generator without autofit

- Set every wrapped text box's size explicitly via `fit_size(...)` and
  `run.font.size = Pt(size)`. Do not set `tf.auto_size` to `TEXT_TO_FIT_SHAPE`
  (or any autofit) anywhere.
- Confirm it: grep the generator for `TEXT_TO_FIT_SHAPE`, `normAutofit`, and
  `auto_size` — the result must be empty. (`MSO_AUTO_SIZE` may then be an unused
  import; drop it.)
- Size fixed-height cards so the floor font is readable; raise card height rather
  than let `fit_size` floor out and overflow.

### 3. Verify — render to images and sweep (faithful only after autofit is gone)

```bash
soffice --headless --convert-to pdf --outdir /tmp/deckqa "deck.pptx"
cd /tmp/deckqa && pdftoppm -jpeg -r 110 *.pdf slide      # -> slide-NN.jpg
```

- Inspect every slide. Use a fresh-eyes subagent for anything past a few slides —
  you will read past overflow you have been staring at. Tell it to flag only
  genuine defects: text **clipped** at a box edge, text **overlapping** another
  element, or text **colliding with the footer**. Text that merely ends with
  empty space below it inside its box is fine, and two cards at different font
  sizes is fine.
- Because autofit is gone, these images are faithful to what PowerPoint shows.
  Only now is a clean preview meaningful.
- Fix any flagged box (give it more height, or let `fit_size` step it down) and
  re-render. One fix can shift another box, so re-sweep after fixing.

### 4. State the editability tradeoff on handover

When delivering, say which artefact is canonical (the generator vs the `.pptx`),
and that baked text will not auto-shrink on manual edits. If the deck is open in
PowerPoint when you regenerate it, the owner must close and reopen — PowerPoint
will not reload a file changed underneath it.

## Constraints

- Never use python-pptx autofit (`MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE` / any
  `normAutofit`). Bake an explicit `Pt(size)` instead.
- Never declare a generated deck correct on the strength of a LibreOffice / PDF
  preview while any autofit remains — that preview hides the overflow. Trust a
  preview only after the generator is autofit-free.
- Do not change `CHAR_W` (0.66) or `SAFETY` (0.94) in `fit_text.py` without
  re-calibrating against freshly rendered output and noting it.
- Source the brand from the project's canonical template — palette, fonts,
  wordmark and layout — resolving the current file by listing the brand folder
  (a `brand.local.md` in this skill's directory names your default). Never invent
  or approximate brand colours; if no governing template is findable, ask which
  brand applies before building.
- Verify before handover: render `pptx -> pdf -> images` and sweep every slide.
  Distinguish clipped/overlapping (a bug) from near-an-edge-with-space (fine), and
  check palette/fonts/wordmark against the template.
- Assert the mechanics (autofit absent, sizes baked, brand values traced to the
  template); leave composition and taste — hierarchy, whether it reads well — to
  human review.
- Do not fire for reading/extracting from an existing `.pptx` (built-in pptx
  skill), or for HTML / Canva / Google Slides decks, or a purely manual in-app
  edit.

## Examples

Each example's pass criteria are binary yes/no checks the behaviour can be
verified against. The same KPIs are encoded in
[`evals/evals.json`](evals/evals.json).

**1 — Generate / repair a deck (positive trigger).**
"The text is overflowing the cards in the workshop deck the script builds —
sort it out and regenerate."
Pass criteria:
- (a) Grepping the generator for `TEXT_TO_FIT_SHAPE`, `normAutofit`, and
  `auto_size` returns nothing.
- (b) Every wrapped body text box gets an explicit `Pt(size)` whose value comes
  from `fit_size` (or an equivalent baked size), not autofit.
- (c) The deck was rendered `pptx -> pdf -> images` and an overflow sweep was run
  across all slides.
- (d) The sweep reports zero clipped / overlapping / footer-colliding boxes.

**2 — Preview trust (regression-pin).**
The agent renders a PDF preview after a build and it looks clean.
Pass criteria:
- (a) The reasoning states LibreOffice recomputes the autofit scale but
  PowerPoint and Keynote do not.
- (b) The agent does NOT declare the deck correct from that preview while any
  autofit remains in the generator.
- (c) A preview is treated as faithful only after the generator is confirmed
  autofit-free.

**3 — On-brand for the project (brand fidelity).**
Building a branded methodology deck in code.
Pass criteria:
- (a) The palette (hex), fonts and wordmark are sourced from the project's current
  brand template/masters (resolved by listing the brand folder), not invented or
  remembered.
- (b) Every brand colour and font in the generator traces to that template /
  guidelines at a stated version — no approximated values.
- (c) If the project has no findable brand template, the agent asks which brand
  applies rather than guessing a palette.
- (d) The render sweep checks palette, fonts and wordmark against the template and
  treats a wrong colour or a substituted font as a defect.

**4 — Helper constants (regression-pin).**
Someone edits `scripts/fit_text.py`.
Pass criteria:
- (a) `fit_size` returns `max_size` unchanged when the text already fits the box.
- (b) `fit_size` returns a smaller size for text that overflows at `max_size`.
- (c) `fit_size` never returns below `min_size`.
- (d) `CHAR_W == 0.66` and `SAFETY == 0.94` are preserved (or a re-calibration
  against rendered output is documented in the change).

**5 — Extract from an existing deck (negative trigger, must NOT fire).**
"Pull the text out of /path/to/board-deck.pptx into a one-page
summary" — or "build me this deck in Canva."
Pass criteria:
- (a) pptx-render-safe does NOT fire.
- (b) No autofit / `fit_size` / generator changes are proposed.
- (c) The agent defers — to the built-in `pptx` skill for extraction, or notes
  that Canva / Google Slides / HTML decks are out of this skill's scope.
