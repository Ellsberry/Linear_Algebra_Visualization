"""
Topic 5 -- Linear Systems (Ax = b).

Pattern: multi-example selector (see t01_vectors.py).
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

TITLE = "5 · Linear Systems (Ax = b)"
SLUG = "systems"

OVERVIEW = """
In Topic 4's business screen you solved Ax = r for x. That's a **linear
system**: a set of equations bundled into Ax = b, asking "what input x produces
the output b?" A system can have exactly one solution, none, or infinitely many
— and you can see why two ways: the **row picture** (each equation is a line or
plane; solutions are where they meet) and the **column picture** (which
combination of A's columns builds b?). We'll see both, then meet linear systems
in business, engineering, chemistry, and nutrition.

*(We can picture systems with up to 3 unknowns. For bigger ones — six, or six
thousand — there's a systematic method that doesn't rely on a drawing. That's
the next topic.)*
"""

HOWTO = """
The left panel sets the equations; the right panel shows the picture. The
**outcome meter** tells you whether there's one solution, none, or infinitely
many — and why. On the core screen you'll see the row picture and the column
picture of the *same* system side by side.
"""

_E1_PRESETS = {
    "One solution":    (np.array([[1., 1.], [1., -1.]]), np.array([3., 1.])),
    "No solution":     (np.array([[1., 1.], [1.,  1.]]), np.array([2., 5.])),
    "Infinitely many": (np.array([[1., 1.], [2.,  2.]]), np.array([2., 4.])),
}

_E3_PRESETS = {
    "Reachable target":   (np.array([[2., 1.], [1., 3.]]), np.array([8., 9.])),
    "Unreachable target": (np.array([[2., 4.], [1., 2.]]), np.array([8., 9.])),
    "Redundant alloys":   (np.array([[2., 4.], [1., 2.]]), np.array([8., 4.])),
}

_E5_PRESETS = {
    "Unique plan":               (np.array([[2.,1.,1.],[1.,3.,1.],[1.,1.,4.]]), np.array([5.,8.,7.])),
    "Redundant foods (infinite)":(np.array([[1.,1.,1.],[1.,2.,3.],[2.,3.,4.]]), np.array([6.,14.,20.])),
    "Impossible targets (none)": (np.array([[1.,1.,1.],[1.,2.,3.],[2.,3.,4.]]), np.array([6.,14.,21.])),
}


# ----------------------------------------------------------------------------
# Shared helpers
# ----------------------------------------------------------------------------

def _classify(A, b):
    """Returns (kind, x_or_None, det_val) without rendering."""
    square = A.shape[0] == A.shape[1]
    det_val = float(np.linalg.det(A)) if square else 0.0
    if square and abs(det_val) > 1e-9:
        return "unique", np.linalg.solve(A, b), det_val
    Ab = np.column_stack([A, b.reshape(-1)])
    kind = "none" if np.linalg.matrix_rank(A) < np.linalg.matrix_rank(Ab) else "infinite"
    return kind, None, det_val


def _render_outcome(kind, x, det_val):
    """Render the colored outcome meter."""
    det_str = f"det = {det_val:.3g}"
    if kind == "unique":
        parts = "  ·  ".join(f"x{i+1} = {xi:.3g}" for i, xi in enumerate(x))
        st.info(f"**One solution** ({det_str} ≠ 0)  ·  {parts}", icon="✅")
    elif kind == "none":
        st.warning(
            f"**No solution** ({det_str} = 0) — equations are inconsistent: "
            "parallel lines/planes that never share a point.",
            icon="⚠️",
        )
    else:
        st.info(
            f"**Infinitely many solutions** ({det_str} = 0) — one equation is "
            "redundant; a free variable means a line/plane of solutions.",
            icon="♾️",
        )


_PLANE_COLORS = ["royalblue", "tomato", "seagreen"]


# Shared helpers and preset dicts are defined above; submodules import them
# via `from . import _classify, _render_outcome, _E1_PRESETS` etc.
from .example_four import _example_four
from .example_two import _example_two
from .example_three import _example_three
from .example_five import _example_five
from .example_one import _example_one


# ----------------------------------------------------------------------------
# Top-level render
# ----------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)
    with st.expander("How to use this screen"):
        st.markdown(HOWTO)

    example = st.radio(
        "Example",
        ["1 · The three outcomes", "2 · Business", "3 · Engineering",
         "4 · Chemistry", "5 · 3D: three planes"],
        horizontal=True, key="t05_example",
    )
    st.divider()

    if example.startswith("1"):
        _example_one()
    elif example.startswith("2"):
        _example_two()
    elif example.startswith("3"):
        _example_three()
    elif example.startswith("4"):
        _example_four()
    else:
        _example_five()
