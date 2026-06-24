"""Example 4 -- Business / economics (production and resources)."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

from . import _inv_meter

_E4_PRESETS = {
    "Two distinct products":            np.array([[2.0, 1.0], [1.0, 3.0]]),
    "Proportional products (singular)": np.array([[2.0, 4.0], [1.0, 2.0]]),
}


def _example_business():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Business.** Matrix A maps production → resources used. "
            "The inverse answers: \"I have these resources — how much of each product "
            "can I make?\""
        )
        preset = st.selectbox("Preset", list(_E4_PRESETS), key="t04e4_preset")
        if st.session_state.get("t04e4_last") != preset:
            w.set_matrix_state("t04e4_A", _E4_PRESETS[preset])
            st.session_state["t04e4_last"] = preset

        A = w.matrix_editor("t04e4_A", 2,
                            label="Resource-usage matrix A (column j = resources for product j)")
        x = w.vector_editor("t04e4_x", 2, (4.0, 2.0), label="Production x (units of each product)")

    det = float(np.linalg.det(A))
    invertible = abs(det) > 1e-9
    r = A @ x

    with right:
        fig = plot.new_figure_2d(rng=14, x_title="resource 1", y_title="resource 2")
        plot.add_vector_2d(fig, [0, 0], r, "seagreen", f"resources r = ({r[0]:.1f}, {r[1]:.1f})")
        plot.add_point_2d(fig, r, "seagreen", "r = Ax", size=14)
        if invertible:
            x_back = np.linalg.inv(A) @ r
            plot.add_point_2d(fig, x_back, "crimson", "A⁻¹r (round-trip)", size=10, symbol="x")
        st.plotly_chart(fig, use_container_width=True)

    # ---- The algebra block (shown openly, not in expander) ----
    st.markdown("#### The algebra, step by step")

    a11, a12 = float(A[0, 0]), float(A[0, 1])
    a21, a22 = float(A[1, 0]), float(A[1, 1])
    x1, x2   = float(x[0]), float(x[1])
    r1, r2   = float(r[0]), float(r[1])

    # Step 1 — forward, general
    st.markdown("**1. Forward map (general)**")
    st.latex(
        r"r = Ax = "
        r"\begin{bmatrix}a_{11}&a_{12}\\a_{21}&a_{22}\end{bmatrix}"
        r"\begin{bmatrix}x_1\\x_2\end{bmatrix}"
        r"= \begin{bmatrix}a_{11}x_1+a_{12}x_2\\a_{21}x_1+a_{22}x_2\end{bmatrix}"
    )

    # Step 2 — forward, live numbers
    st.markdown("**2. Forward map (your numbers)**")
    st.latex(
        r"r = " + w.bmatrix(A)
        + w.bmatrix(x.reshape(-1, 1))
        + " = " + w.bmatrix(r.reshape(-1, 1))
    )

    # Step 3 — inverse formula, emphasise det in denominator
    st.markdown("**3. Inverse formula** — det in the denominator is the key")
    if invertible:
        st.latex(
            r"A^{-1} = \frac{1}{\det A}"
            r"\begin{bmatrix}a_{22}&-a_{12}\\-a_{21}&a_{11}\end{bmatrix}"
            + r"\qquad \det A = a_{11}a_{22} - a_{12}a_{21} = " + f"{det:.4f}"
        )
    else:
        st.latex(
            r"A^{-1} = \frac{1}{\det A}"
            r"\begin{bmatrix}a_{22}&-a_{12}\\-a_{21}&a_{11}\end{bmatrix}"
            r"\quad \det A = " + f"{det:.4f}"
            r"\implies \frac{1}{\det A} = \frac{1}{0} \text{ — undefined}"
        )
        st.caption(
            "These two products use resources in the same proportion, so from the "
            "resources alone you can't tell how much of each you made. There's no way "
            "to work backwards — the inverse doesn't exist."
        )

    if invertible:
        Ainv = np.linalg.inv(A)
        x_back = Ainv @ r

        # Step 4 — inverse, live numbers
        st.markdown("**4. Inverse (your numbers)**")
        st.latex(r"A^{-1} = " + w.bmatrix(Ainv))

        # Step 5 — recover and verify
        st.markdown("**5. Recover production from resources**")
        st.latex(
            r"x = A^{-1}r = "
            + w.bmatrix(Ainv)
            + w.bmatrix(r.reshape(-1, 1))
            + " = " + w.bmatrix(x_back.reshape(-1, 1))
        )
        st.success(f"Round trip returns x = ({x_back[0]:.3f}, {x_back[1]:.3f}) ✓")

    # ---- Optional target solver ----
    with st.expander("Solve for a resource target"):
        rt = w.vector_editor("t04e4_rt", 2, (8.0, 6.0), label="Resource target r")
        if invertible:
            xt = Ainv @ rt
            st.latex(r"x = A^{-1}r = " + w.bmatrix(xt.reshape(-1, 1)))
            if any(xt < 0):
                st.info(
                    "The algebra returns a negative number of products — mathematically "
                    "valid, physically impossible. The model is more permissive than a "
                    "real factory."
                )
        else:
            st.warning("No inverse — can't solve for a resource target.")

    # ---- Inverse meter ----
    st.markdown("**Inverse meter**")
    _inv_meter(A)

    st.info(
        "Run the matrix forward and it tells you resources used; run it backward (the "
        "inverse) and it tells you how much to produce to use exactly what you have. This "
        "\"solve A x = r for x\" is the exact question of the next topic — linear systems."
    )
