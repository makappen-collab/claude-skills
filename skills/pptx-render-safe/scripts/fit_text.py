"""Deterministic text fitting for python-pptx decks.

python-pptx's "shrink text to fit" (MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE) writes an
OOXML <a:normAutofit/> element WITHOUT a computed fontScale. PowerPoint and
Keynote then render the text at full size and it overflows its box -- they only
recompute the scale when a human edits the box. LibreOffice is the only common
renderer that recomputes it on load, which is why a LibreOffice-exported PDF
preview looks correct while the real .pptx overflows in PowerPoint.

The fix is to never use autofit and instead bake an explicit font size that
genuinely fits. `fit_size` estimates the wrapped line count from character
counts and returns the largest size (stepping down from max_size to min_size)
whose estimated height fits the box. Set it explicitly:

    from fit_text import fit_size
    from pptx.util import Pt
    size = fit_size(body_text, width_in=4.97, height_in=1.1, max_size=14)
    run.font.size = Pt(size)

The calibration constants are load-bearing -- tuned against real Manrope decks
rendered and eyeballed for overflow. Changing them re-opens the overflow bug, so
keep them unless you re-calibrate against rendered output (build the deck, render
pptx -> PDF -> images, and confirm no box clips).

    CHAR_W  = 0.66   mean glyph advance as a fraction of the em
    SAFETY  = 0.94   fraction of the box height used as the line budget

Pure python; depends only on the standard library `math`.
"""
from __future__ import annotations

import math

CHAR_W = 0.66   # mean glyph advance as a fraction of the em (Manrope, a wide face)
SAFETY = 0.94   # use 94% of the box height as the budget, leaving breathing room


def fit_size(items, width_in, height_in, *, max_size, min_size=9.0,
             line_spacing=1.3, space_after_pt=0.0, char_w=CHAR_W, safety=SAFETY):
    """Largest font in pt (max_size down to min_size in 0.5 steps) that fits the box.

    Args:
        items: a single string, or a list of strings (one per paragraph). A "\\n"
            inside an item is treated as a hard line break.
        width_in, height_in: the text box's usable width and height in inches.
        max_size: the design font size; returned unchanged when the text fits.
        min_size: the floor. The function never returns below this -- if even the
            floor overflows, give the box more height rather than shrinking past
            readability.
        line_spacing: paragraph line-spacing multiple, matching what you set on
            the paragraph.
        space_after_pt: space-after between paragraphs in points (for multi-item
            lists), matching the paragraph setting.
        char_w, safety: calibration constants. Load-bearing; see module docstring.

    Returns:
        A float font size in points. Equal to max_size when the text already fits.
    """
    if isinstance(items, str):
        items = [items]
    items = [str(it) for it in items if str(it) != ""]
    if not items:
        return max_size
    width_pt = max(1.0, width_in * 72.0)
    budget = height_in * safety
    size = max_size
    while size >= min_size - 1e-9:
        cpl = max(1.0, width_pt / (size * char_w))       # estimated chars per line
        lines = 0
        for it in items:
            for para in it.split("\n"):
                lines += max(1, math.ceil(len(para) / cpl))
        line_h = size * line_spacing / 72.0
        gaps = max(0, len(items) - 1) * (space_after_pt / 72.0)
        if lines * line_h + gaps <= budget:
            return round(size, 1)
        size -= 0.5
    return min_size
