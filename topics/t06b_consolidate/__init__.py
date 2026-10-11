"""
Topic 6.5 -- Putting It Together (Inverse, Transpose, Complete Solution).

Pattern: MULTI-EXAMPLE (4 screens). Built from specs/topic6b_consolidate.md.
"""
import streamlit as st

from .screen_inverse import render_inverse
from .screen_transpose import render_transpose
from .screen_complete import render_complete
from .screen_rules import render_rules

TITLE = "6.5 · Putting It Together"
SLUG = "consolidate"

OVERVIEW = """
You now know the four spaces hiding inside a matrix. This short topic names
three tools you've been using without a clean definition — the **inverse**, the
**transpose**, and the **complete solution** of a system — and ends with one
table that tells you exactly when each one is allowed. That table is also the
doorway to the next topic: it shows you the cases where a system has **no exact
answer at all**, which is precisely the problem projection is built to solve.
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)

    screen = st.radio(
        "Screen",
        [
            "1 · The inverse A⁻¹",
            "2 · The transpose Aᵀ",
            "3 · The complete solution",
            "4 · The rules, and what's next",
        ],
        horizontal=True,
        key="t06b_screen",
    )

    st.divider()

    if screen.startswith("1 "):
        render_inverse()
    elif screen.startswith("2 "):
        render_transpose()
    elif screen.startswith("3 "):
        render_complete()
    elif screen.startswith("4 "):
        render_rules()
