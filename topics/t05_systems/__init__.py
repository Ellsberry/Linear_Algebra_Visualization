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


# ── Example 3: Engineering — metal mixing ─────────────────────────────────────

def _example_three():
    left, right = st.columns([1, 1.4], gap="large")

    with left:
        st.markdown(
            "**Metal mixing.** You have two metal alloys. Each alloy, per unit you add, "
            "contributes a known amount of **copper** and **zinc** — that pair of numbers "
            "is the alloy's \"makeup vector.\" You want to combine some amount **x₁** of "
            "alloy 1 and **x₂** of alloy 2 to hit an exact target. "
            "\"How much of each alloy?\" is the system x₁·c₁ + x₂·c₂ = b, where c₁, c₂ "
            "are the alloys' makeup vectors (the columns of A) and b is the target. "
            "**You are solving for x₁ and x₂ — how many units of each alloy to add.** "
            "This is the *column picture*: build the target out of the column vectors. "
            "(Direct callback to Topic 1's smoothies — same idea, now solved exactly.)"
        )
        preset = st.selectbox("Preset", list(_E3_PRESETS), key="t05e3_preset")
        if st.session_state.get("t05e3_last") != preset:
            A_p, b_p = _E3_PRESETS[preset]
            w.set_matrix_state("t05e3_A", A_p)
            w.set_vector_state("t05e3_b", b_p)
            st.session_state["t05e3_last"] = preset

        A = w.matrix_editor("t05e3_A", 2,
                            label="Alloy makeup — column 1 = alloy 1 (copper, zinc), column 2 = alloy 2 (copper, zinc)")
        b = w.vector_editor("t05e3_b", 2, (8., 9.), label="Target (copper, zinc)")

    kind, x, det_val = _classify(A, b)

    with right:
        fig = plot.new_figure_2d(rng=12, x_title="copper", y_title="zinc", height=420)
        c1, c2 = A[:, 0], A[:, 1]
        plot.add_vector_2d(fig, [0, 0], c1, "royalblue",
                           f"alloy 1 ({c1[0]:.2g} Cu, {c1[1]:.2g} Zn)")
        plot.add_vector_2d(fig, [0, 0], c2, "crimson",
                           f"alloy 2 ({c2[0]:.2g} Cu, {c2[1]:.2g} Zn)")
        plot.add_point_2d(fig, b, "#e6e6e6", f"target ({b[0]:.2g}, {b[1]:.2g})",
                          size=13, symbol="diamond")
        if kind == "unique":
            mid = x[0] * c1
            plot.add_vector_2d(fig, [0, 0], mid, "rgba(0,128,0,0.5)",
                               f"x₁ × alloy 1", dash="dash")
            plot.add_vector_2d(fig, mid, b, "seagreen",
                               f"x₂ × alloy 2", dash="dash")
        st.plotly_chart(fig, use_container_width=True)

        if kind == "unique":
            st.success(f"Blend: **{x[0]:.3g} units of alloy 1** + **{x[1]:.3g} units of alloy 2**")
        elif kind == "none":
            st.warning("No blend of these two alloys reaches the target.")
        else:
            st.info("Many blends work (the alloys are redundant).")

    st.markdown(
        "> Metallurgists, chemists, and chefs solve linear systems to hit a target blend "
        "from the ingredients on hand. You're solving for *how much of each alloy* to add. "
        "If the two alloys aren't truly different — one is just a scaled copy of the other "
        "— then every blend lands on a single line, and any target off that line is "
        "impossible to make: no solution."
    )

    with st.expander("Show the math"):
        st.latex(r"A\,x = b \;\Longrightarrow\; " + w.bmatrix(A)
                 + r"\begin{bmatrix}x_1\\x_2\end{bmatrix} = " + w.bmatrix(b.reshape(-1, 1)))
        if kind == "unique":
            st.latex(r"x = " + w.bmatrix(x.reshape(-1, 1)))
            st.markdown(f"Use **{x[0]:.3g} kg of alloy 1** and **{x[1]:.3g} kg of alloy 2**.")
        elif kind == "none":
            st.markdown("The two alloys are proportional — the target is off their line. No blend works.")
        else:
            st.markdown("The target lies on the alloys' shared line — infinitely many blends work.")


# ── Example 5: 3D — three planes ─────────────────────────────────────────────

def _example_five():
    left, right = st.columns([1, 1.6], gap="large")

    with left:
        st.markdown(
            "**Three planes in space.** Each row of Ax = b is one equation — one plane. "
            "Three planes can meet at a point (one solution), along a line (infinitely "
            "many), or share no common point (none).\n\n"
            "Framed as: three foods, three nutrients — find amounts to hit exact targets."
        )
        preset = st.selectbox("Preset", list(_E5_PRESETS), key="t05e5_preset")
        if st.session_state.get("t05e5_last") != preset:
            A_p, b_p = _E5_PRESETS[preset]
            w.set_matrix_state("t05e5_A", A_p)
            w.set_vector_state("t05e5_b", b_p)
            st.session_state["t05e5_last"] = preset

        A = w.matrix_editor("t05e5_A", 3,
                            label="Nutrient content — row i = nutrient i, column j = food j")
        b = w.vector_editor("t05e5_b", 3, (5., 8., 7.), label="Nutrient targets (one per row)")

    kind, x, det_val = _classify(A, b)

    with right:
        fig = plot.new_figure_3d(rng=6, titles=("food 1", "food 2", "food 3"))
        for i in range(3):
            plot.add_plane_3d(fig, A[i, 0], A[i, 1], A[i, 2], b[i],
                              _PLANE_COLORS[i], f"plane {i + 1}")
        if kind == "unique":
            fig.add_trace(go.Scatter3d(
                x=[x[0]], y=[x[1]], z=[x[2]], mode="markers",
                marker=dict(color="gold", size=10, line=dict(color="#e6e6e6", width=2)),
                name=f"solution ({x[0]:.2g}, {x[1]:.2g}, {x[2]:.2g})",
            ))
        st.caption("drag to rotate · scroll to zoom — the solution is where all three planes cross.")
        st.plotly_chart(fig, use_container_width=True)

        if kind == "unique":
            st.success(
                f"Plan: **{x[0]:.3g} unit{'s' if abs(x[0])!=1 else ''} food 1**, "
                f"**{x[1]:.3g} food 2**, **{x[2]:.3g} food 3**"
            )
        elif kind == "none":
            st.warning("No plan hits all three targets.")
        else:
            st.info("Many plans work (a redundant food).")

    st.markdown(
        "> A dietician hitting exact nutrient targets from three foods is solving three "
        "equations in three unknowns — three planes in space. They meet at one point (one "
        "plan), along a line (many plans), or nowhere (impossible). You're solving for "
        "how much of each food to use."
    )

    st.info(
        "This is the biggest system we can still *picture* — three unknowns, three planes. "
        "Real problems have six, or six thousand, unknowns, and there's no drawing for "
        "that. The next topic introduces the systematic method — elimination to "
        "**triangular form** — that solves a system of any size, the same algorithm every "
        "engineering simulation runs internally."
    )

    with st.expander("Show the math"):
        st.latex(r"A = " + w.bmatrix(A) + r"\;,\quad b = " + w.bmatrix(b.reshape(-1, 1)))
        st.markdown(f"**det(A)** = `{det_val:.3g}`")
        if kind == "unique":
            st.latex(r"x = " + w.bmatrix(x.reshape(-1, 1)))
        elif kind == "none":
            st.markdown("rank(A) < rank([A | b]) → **no solution**.")
        else:
            st.markdown("rank(A) = rank([A | b]) < n → **infinitely many solutions** (free variable).")


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
