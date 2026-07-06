"""
Topic 0 -- Matrix Multiplication.

Pattern: MULTI-EXAMPLE. Screens 0-4 are all built, per
specs/topic00_matrix_multiplication.md.
"""
import streamlit as st

from .screen_ops import render_ops
from .screen_2x2 import render_2x2
from .screen_3x3 import render_3x3
from .screen_rect import render_rect
from .screen_special import render_special

TITLE = "0 · Matrix multiplication"
SLUG = "matmul"

OVERVIEW = """
Every transformation, every Ax = b, every step of elimination in this app runs
on one operation: matrix multiplication. This topic teaches the mechanics
directly -- the row-times-column rule -- with hands-on practice before you
meet it inside applications.
"""


def render():
    st.markdown(OVERVIEW)

    screen = st.radio(
        "Screen",
        ["0 · Operations", "1 · Multiply 2x2", "2 · Multiply 3x3", "3 · Rectangular",
         "4 · Special matrices"],
        horizontal=True,
        key="t00_screen",
    )
    st.divider()

    if screen.startswith("0"):
        render_ops()
    elif screen.startswith("1"):
        render_2x2()
    elif screen.startswith("2"):
        render_3x3()
    elif screen.startswith("3"):
        render_rect()
    elif screen.startswith("4"):
        render_special()
