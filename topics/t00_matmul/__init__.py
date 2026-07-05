"""
Topic 0 -- Matrix Multiplication.

Pattern: MULTI-EXAMPLE. Only Screen 1 is built so far; screens 2-4 (per
specs/topic00_matrix_multiplication.md) plug into the same radio dispatch.
"""
import streamlit as st

from .screen_2x2 import render_2x2

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
        ["1 · The rule (2x2)"],
        horizontal=True,
        key="t00_screen",
    )
    st.divider()

    if screen.startswith("1"):
        render_2x2()
