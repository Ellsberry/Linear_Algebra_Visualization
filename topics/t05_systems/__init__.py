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


# ── Example 1: The three outcomes ────────────────────────────────────────────

def _example_one():
    left, right = st.columns([1, 2.2], gap="large")

    with left:
        preset = st.selectbox("Preset", list(_E1_PRESETS), key="t05e1_preset")
        if st.session_state.get("t05e1_last") != preset:
            A_p, b_p = _E1_PRESETS[preset]
            w.set_matrix_state("t05e1_A", A_p)
            w.set_vector_state("t05e1_b", b_p)
            st.session_state["t05e1_last"] = preset

        A = w.matrix_editor("t05e1_A", 2, label="Coefficients A")
        b = w.vector_editor("t05e1_b", 2, (3., 1.), label="Right side b")

    kind, x, det_val = _classify(A, b)

    with right:
        row_col, col_col = st.columns(2)
        with row_col:
            st.markdown("**Row picture** — where do the lines cross?")
            fig_r = plot.new_figure_2d(rng=5, x_title="x₁", y_title="x₂", height=380)
            plot.add_line_2d(fig_r, A[0, 0], A[0, 1], b[0], "royalblue", "row 1", rng=5)
            plot.add_line_2d(fig_r, A[1, 0], A[1, 1], b[1], "crimson",   "row 2", rng=5)
            if kind == "unique":
                plot.add_point_2d(fig_r, x, "seagreen",
                                  f"solution ({x[0]:.2g}, {x[1]:.2g})", size=14)
            st.plotly_chart(fig_r, use_container_width=True)

        with col_col:
            st.markdown("**Column picture** — what mix of columns reaches b?")
            fig_c = plot.new_figure_2d(rng=5, x_title="", y_title="", height=380)
            c1, c2 = A[:, 0], A[:, 1]
            plot.add_vector_2d(fig_c, [0, 0], c1, "royalblue", "col 1")
            plot.add_vector_2d(fig_c, [0, 0], c2, "crimson",   "col 2")
            plot.add_point_2d(fig_c, b, "#e6e6e6", "target b", size=12, symbol="diamond")
            if kind == "unique":
                mid = x[0] * c1
                plot.add_vector_2d(fig_c, [0, 0], mid, "rgba(0,128,0,0.5)",
                                   "x₁·col1", dash="dash")
                plot.add_vector_2d(fig_c, mid, b, "seagreen",
                                   "x₂·col2 → b", dash="dash")
            st.plotly_chart(fig_c, use_container_width=True)

        _render_outcome(kind, x, det_val)

    st.markdown(
        "> Same system, two views. The row picture asks \"where do the lines cross?\"; the "
        "column picture asks \"what mix of these two arrows reaches the target?\" They "
        "always agree — one crossing point matches one mix; parallel lines match a target "
        "you can't reach; one repeated line matches a target with many mixes."
    )

    with st.expander("Show the math"):
        st.latex(r"A = " + w.bmatrix(A) + r"\;,\quad b = " + w.bmatrix(b.reshape(-1, 1)))
        st.markdown(f"**det(A)** = `{det_val:.3g}`")
        if kind == "unique":
            st.latex(r"x = A^{-1}b = " + w.bmatrix(x.reshape(-1, 1)))
        elif kind == "none":
            st.markdown("rank(A) < rank([A | b]) → **no solution** (inconsistent).")
        else:
            st.markdown("rank(A) = rank([A | b]) < n → **free variable** → infinitely many solutions.")


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
