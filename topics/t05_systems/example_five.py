"""Example 5 -- 3D: three planes."""
import plotly.graph_objects as go
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

from . import _classify, _E5_PRESETS, _PLANE_COLORS


def _example_five():
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

    A = w.editable_matrix("t05e5_A", 3,
                          label="Nutrient content — row i = nutrient i, column j = food j")
    b = w.vector_editor("t05e5_b", 3, (5., 8., 7.), label="Nutrient targets (one per row)")

    kind, x, det_val = _classify(A, b)

    left, right = st.columns([0.5, 0.5], gap="large")

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

    with left:
        st.latex(r"{\small A = " + w.bmatrix(A) + r"\;,\quad b = " + w.bmatrix(b.reshape(-1, 1)) + r"}")
        st.markdown(f"**det(A)** = `{det_val:.3g}`")
        if kind == "unique":
            st.latex(r"{\small x = " + w.bmatrix(x.reshape(-1, 1)) + r"}")
        elif kind == "none":
            st.markdown("rank(A) < rank([A | b]) → **no solution**.")
        else:
            st.markdown("rank(A) = rank([A | b]) < n → **infinitely many solutions** (free variable).")

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
