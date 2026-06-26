"""
Topic 5.5 -- Elimination & Triangular Form.

Pattern: MULTI-EXAMPLE (3 screens).
"""
import streamlit as st

from .circuit import _example_three
from .inverse_elim import render_inverse_elim
from .logistics import _example_two
from .logistics_one import _example_two_a
from .screen_workbench import _example_one

TITLE = "5.5 · Elimination & Triangular Form"
SLUG = "elimination"

OVERVIEW = """
Topic 5 ended at the edge of what we can draw — three unknowns, three planes.
This topic is the method that goes further. We simplify the system's augmented
matrix `[A | b]` with three reversible moves — swap rows, scale a row, add a
multiple of one row to another — until it's **upper triangular** (zeros below
the diagonal). Then we read the answer off from the bottom row up
(**back-substitution**). The moves never change the answer, so it's always safe
to experiment. First on a 3×3 you can still relate to planes, then on a
six-variable shipping network and a circuit you *can't* picture — where the
procedure is the only way through.
"""

HOWTO = """
Use **Do one step** / **Run to triangular form** to watch the standard method,
or compose your own row operations in **manual** mode. The banner tells you when
you've hit a special case (no solution, or infinitely many). Once the matrix is
triangular, **back-substitute** to solve. **Undo** and **Reset** make
experimenting safe.
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)
    st.caption(HOWTO)

    example = st.radio(
        "Example",
        ["1 · The workbench", "2a · Logistics (one plan)", "2b · Logistics (many plans)", "3 · Circuit", "4 · Inverse by elimination"],
        horizontal=True,
        key="t05b_example",
    )
    st.divider()

    if example.startswith("1"):
        _example_one()
    elif example.startswith("2a"):
        _example_two_a()
    elif example.startswith("2b"):
        _example_two()
    elif example.startswith("3"):
        _example_three()
    else:
        render_inverse_elim()
