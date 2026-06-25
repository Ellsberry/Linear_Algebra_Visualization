"""Example 1 -- The three outcomes."""
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

from . import _classify, _render_outcome, _E1_PRESETS


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
