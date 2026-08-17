"""
Topic 8 -- Eigenvalues & Eigenvectors.

Pattern: MULTI-EXAMPLE (6 screens).
"""
import streamlit as st

from .screen_special import render_special
from .screen_defined import render_defined
from .screen_eigenvalues import render_eigenvalues
from .screen_eigenvectors import render_eigenvectors
from .screen_reading import render_reading
from .screen_markov import render_markov

TITLE = "8 · Eigenvalues & Eigenvectors"
SLUG = "eigen"

OVERVIEW = """
Multiply a vector by a matrix and it usually swings onto a new direction. But
every matrix has a few special directions that don't swing at all -- the vector
comes out pointing the same way, just longer, shorter, or flipped. Those special
directions are eigenvectors, and the amount of stretch is the eigenvalue. They are
the hidden skeleton of a matrix, and they explain everything from vibrating bridges
to how weather settles into a climate.
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)

    screen = st.radio(
        "Screen",
        [
            "0 · The special directions",
            "1 · Eigenvector & eigenvalue defined",
            "2 · Finding eigenvalues",
            "3 · Finding eigenvectors",
            "4 · What eigenvalues tell you",
            "5 · Why it matters: Markov chains",
        ],
        horizontal=True,
        key="t08_screen",
    )

    st.divider()

    if screen.startswith("0 "):
        render_special()
    elif screen.startswith("1 "):
        render_defined()
    elif screen.startswith("2 "):
        render_eigenvalues()
    elif screen.startswith("3 "):
        render_eigenvectors()
    elif screen.startswith("4 "):
        render_reading()
    elif screen.startswith("5 "):
        render_markov()
