"""
Topic 6 -- Vector Spaces (Null Space, Column Space, Row Space).

Pattern: MULTI-EXAMPLE (5 screens).
"""
import streamlit as st

from .screen_what import render_what
from .screen_column import render_column
from .screen_null import render_null
from .screen_row import render_row
from .screen_together import render_together

TITLE = "6 · Vector Spaces"
SLUG = "spaces"

OVERVIEW = """
Every matrix hides three collections of vectors inside it — one that describes
everywhere it can send you, one that describes everything it squashes to zero,
and one that describes its genuinely different rules. This topic names those
three collections, shows that you have already met each of them, and ends with
one simple counting rule that ties the whole course so far together.
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
            "5 · One matrix, all three spaces",
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
        render_together()
