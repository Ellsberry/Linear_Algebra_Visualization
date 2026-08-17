"""
Topic 7 -- Projection & Least Squares.

Pattern: MULTI-EXAMPLE (6 screens).
"""
import streamlit as st

from .screen_perp import render_perp
from .screen_line import render_line
from .screen_plane import render_plane
from .screen_normal import render_normal
from .screen_fit import render_fit
from .screen_world import render_world

TITLE = "7 · Projection & Least Squares"
SLUG = "projection"

OVERVIEW = """
Sometimes there is no exact answer — the target sits outside everything a matrix
can reach, and no input hits it exactly. This topic is about the next best thing:
the CLOSEST answer. The closest point turns out to be a perpendicular shadow, and
that one idea powers line-of-best-fit, GPS, and the computer vision in your camera.
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)

    screen = st.radio(
        "Screen",
        [
            "0 · Perpendicular means dot product zero",
            "1 · Projecting onto a line",
            "2 · Projecting onto a plane",
            "3 · Why perpendicular is closest",
            "4 · Line of best fit",
            "5 · Where this lives in the real world",
        ],
        horizontal=True,
        key="t07_screen",
    )

    st.divider()

    if screen.startswith("0 "):
        render_perp()
    elif screen.startswith("1 "):
        render_line()
    elif screen.startswith("2 "):
        render_plane()
    elif screen.startswith("3 "):
        render_normal()
    elif screen.startswith("4 "):
        render_fit()
    elif screen.startswith("5 "):
        render_world()
