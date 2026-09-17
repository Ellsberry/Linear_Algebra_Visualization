"""
Topic 6 -- Vector Spaces (Null Space, Column Space, Row Space).

Pattern: MULTI-EXAMPLE (5 screens).
"""
import streamlit as st

from .screen_what import render_what
from .screen_column import render_column
from .screen_null import render_null
from .screen_row import render_row
from .screen_leftnull import render_leftnull
from .screen_together import render_together
from .screen_bigmatrix import render_bigmatrix
from .screen_transforms import render_transforms

TITLE = "6 · Vector Spaces"
SLUG = "spaces"

OVERVIEW = """
Every matrix hides four collections of vectors inside it — one that describes
everywhere it can send you (the **column space**), one that describes everything
it crushes to zero (the **null space**), one that captures its genuinely different
rules (the **row space**), and one that reveals all the ways those rules can
cancel out (the **left null space**). This topic names those four collections,
shows that you have already met the first three, and ends with the counting rule
and the fourth space that tie the whole picture together.

**Orthogonal: the math word for perpendicular.** You already know
**perpendicular** — two arrows meeting at a right angle. **Orthogonal** is just
the mathematician's word for the same thing, and it means exactly perpendicular
when you're talking about two arrows in 2D or 3D: they're orthogonal when they
meet at 90 degrees, which is exactly when their dot product is zero.

So why have a second word? Because "orthogonal" keeps working in places where
"perpendicular" stops making sense. You can picture two arrows at a right angle,
but what about two functions, like sin(x) and cos(x)? You can't draw them meeting
at 90 degrees — yet there's a version of the dot product for functions, and by
that measure sin(x) and cos(x) come out to zero, so we say they are
**orthogonal**. Same idea — "their product cancels to zero" — stretched to things
you can't draw as arrows.

This matters here because the four collections inside a matrix come in
**orthogonal pairs**: the row space is orthogonal to the null space, and the
column space is orthogonal to the left null space. Orthogonality is the thread
that ties the four spaces together.
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)

    screen = st.radio(
        "Screen",
        [
            "1 · What a vector space is",
            "2 · Column space",
            "3 · Null space",
            "4 · Row space and the counting rule",
            "5 · Left null space",
            "6 · One matrix, all four spaces",
            "7 · Work it yourself: all four spaces of a big matrix",
            "8 · The four spaces of a transformation",
        ],
        horizontal=True,
        key="t06_screen",
    )

    st.divider()

    if screen.startswith("1 "):
        render_what()
    elif screen.startswith("2 "):
        render_column()
    elif screen.startswith("3 "):
        render_null()
    elif screen.startswith("4 "):
        render_row()
    elif screen.startswith("5 "):
        render_leftnull()
    elif screen.startswith("6 "):
        render_together()
    elif screen.startswith("7 "):
        render_bigmatrix()
    elif screen.startswith("8 "):
        render_transforms()
