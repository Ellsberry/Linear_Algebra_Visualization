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

try:
    from .infinite_nosolution import render_infinite_nosolution
except ImportError:
    render_infinite_nosolution = None

try:
    from .smoothie import render_smoothie
except ImportError:
    render_smoothie = None

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
        [
            "1 · Augmented Matrix",
            "2 · Inverse by elimination",
            "3 · Infinite and No Solutions",
            "4 · Logistics (one plan)",
            "5 · Logistics (many plans)",
            "6 · Smoothie",
            "7 · Circuit",
        ],
        horizontal=True,
        key="t05b_example",
    )

    # Clear equation-builder state when entering a screen fresh (so typed boxes
    # don't persist across visits).
    _eb_keys = {
        "4 · Logistics (one plan)":   ("t05b_e2a", 7),
        "5 · Logistics (many plans)": ("t05b_e2", 7),
        "7 · Circuit":                ("t05b_e3", 5),
    }
    _prev = st.session_state.get("t05b_prev_example")
    if _prev != example:
        # entering a (possibly different) screen: clear the one we're entering
        if example in _eb_keys:
            k, nrows = _eb_keys[example]
            for i in range(nrows):
                st.session_state.pop(f"{k}_eq__{i}", None)
            for suffix in ("_check_result", "_parse_errors", "_ready", "_M",
                           "_orig", "_log", "_history", "_solution"):
                st.session_state.pop(f"{k}{suffix}", None)
        st.session_state["t05b_prev_example"] = example

    st.divider()

    if example.startswith("1 "):
        _example_one()
    elif example.startswith("2 "):
        render_inverse_elim()
    elif example.startswith("3 "):
        if render_infinite_nosolution is not None:
            render_infinite_nosolution()
        else:
            st.info("Coming soon.")
    elif example.startswith("4 "):
        _example_two_a()
    elif example.startswith("5 "):
        _example_two()
    elif example.startswith("6 "):
        if render_smoothie is not None:
            render_smoothie()
        else:
            st.info("Smoothie: coming soon")
    elif example.startswith("7 "):
        _example_three()
