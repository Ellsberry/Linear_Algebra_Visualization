"""Example 4 -- Business / economics (bakery: recipes and resources)."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

from . import _inv_meter

_E4_PRESETS = {
    "Two different recipes":                np.array([[2.0, 1.0], [1.0, 3.0]]),
    "Recipes in the same ratio (singular)": np.array([[2.0, 4.0], [1.0, 2.0]]),
}


def _example_business():
    st.markdown(
        "**Business.** A bakery makes cakes and cookies out of flour and sugar. The recipe "
        "matrix A has one column per product: column 1 is a cake's recipe (flour, sugar), "
        "column 2 is a cookie's recipe. Multiply A by how many of each you bake and it tells "
        "you the total flour and sugar used. The inverse runs it backward: given the flour "
        "and sugar you have, it finds how many cakes and cookies that makes."
    )
    preset = st.selectbox("Preset", list(_E4_PRESETS), key="t04e4_preset")
    if st.session_state.get("t04e4_last") != preset:
        w.set_matrix_state("t04e4_A", _E4_PRESETS[preset])
        st.session_state["t04e4_last"] = preset

    ac, _ = st.columns([0.5, 0.5])
    with ac:
        A = w.editable_matrix("t04e4_A", 2, compact=True,
              label="Recipe matrix A (col 1 = cake, col 2 = cookie; rows = flour, sugar)")
    xc, _ = st.columns([0.5, 0.5])
    with xc:
        x = w.vector_editor("t04e4_x", 2, (4.0, 2.0),
              label="How many you bake (cakes, cookies)")
    det = float(np.linalg.det(A))
    invertible = abs(det) > 1e-9
    r = A @ x

    left, right = st.columns([0.6, 0.4], gap="large")

    with right:
        fig = plot.new_figure_2d(rng=14, x_title="flour used", y_title="sugar used")
        plot.add_vector_2d(fig, [0, 0], r, "seagreen",
                           f"resources ({r[0]:.1f} flour, {r[1]:.1f} sugar)")
        plot.add_point_2d(fig, r, "seagreen", "resources used", size=14)
        if invertible:
            Ainv = np.linalg.inv(A)
            x_back = Ainv @ r
            plot.add_point_2d(fig, x_back, "crimson", "round-trip", size=10, symbol="x")
        st.plotly_chart(fig, use_container_width=True)
        _inv_meter(A)

    with left:
        st.markdown("#### The algebra, step by step")

        st.markdown("**1. How the resources add up (in general).** Each product uses some "
                    "flour and some sugar; the total used is A times how many you bake.")
        st.latex(r"{\small r = Ax = "
                 r"\begin{bmatrix}a_{11}&a_{12}\\a_{21}&a_{22}\end{bmatrix}"
                 r"\begin{bmatrix}x_1\\x_2\end{bmatrix}"
                 r"= \begin{bmatrix}a_{11}x_1+a_{12}x_2\\a_{21}x_1+a_{22}x_2\end{bmatrix}}")

        st.markdown("**2. With your recipes and batch.**")
        st.latex(r"{\small r = " + w.bmatrix(A) + w.bmatrix(x.reshape(-1, 1))
                 + " = " + w.bmatrix(r.reshape(-1, 1)) + r"}")
        st.markdown(f"So this batch uses **{r[0]:.1f} flour** and **{r[1]:.1f} sugar**.")

        st.markdown("**3. To work backward, we need A⁻¹.**")
        if invertible:
            st.latex(r"{\small A^{-1} = \frac{1}{\det A}"
                     r"\begin{bmatrix}a_{22}&-a_{12}\\-a_{21}&a_{11}\end{bmatrix}"
                     + rf"\qquad \det A = {det:.4f}" + r"}")
        else:
            st.latex(r"{\small A^{-1} = \frac{1}{\det A}"
                     r"\begin{bmatrix}a_{22}&-a_{12}\\-a_{21}&a_{11}\end{bmatrix}"
                     + rf"\quad \det A = {det:.4f} \implies \tfrac{{1}}{{0}}"
                     + r"\text{ — undefined}}")
        st.markdown(
            "For a 2×2 you build the inverse by a fixed recipe: swap the two diagonal "
            "numbers, flip the sign of the other two, and divide everything by the "
            "determinant. The determinant sits in the denominator — so if it's zero, "
            "you're dividing by zero and there is no inverse."
        )
        if not invertible:
            st.caption(
                "These two recipes use flour and sugar in the very same ratio — the cookie "
                "is just a double cake. So from the flour and sugar totals alone you can't "
                "tell how many of each you made. There's no way to work backward, and the "
                "inverse doesn't exist (dividing by det A = 0)."
            )

        if invertible:
            Ainv = np.linalg.inv(A)
            x_back = Ainv @ r

            st.markdown("**4. Your A⁻¹ (with numbers).**")
            st.latex(r"{\small A^{-1} = " + w.bmatrix(Ainv) + r"}")

            st.markdown("**5. How many of each product the resources make.**")
            st.latex(r"{\small x = A^{-1}r = " + w.bmatrix(Ainv)
                     + w.bmatrix(r.reshape(-1, 1)) + " = "
                     + w.bmatrix(x_back.reshape(-1, 1)) + r"}")
            st.success(f"Round trip returns {x_back[0]:.1f} cakes and {x_back[1]:.1f} cookies ✓")

    with st.expander("Solve for a resource target"):
        rt = w.vector_editor("t04e4_rt", 2, (8.0, 6.0), label="Flour and sugar on hand")
        if invertible:
            xt = np.linalg.inv(A) @ rt
            st.latex(r"x = A^{-1}r = " + w.bmatrix(xt.reshape(-1, 1)))
            if any(xt < 0):
                st.info(
                    "The algebra returns a negative number of cakes or cookies — "
                    "mathematically valid, physically impossible. The model is more "
                    "permissive than a real bakery."
                )
        else:
            st.warning("No inverse — can't solve for a flour/sugar target.")

    st.info(
        "Run the recipe matrix forward and it tells you the resources a batch uses; run it "
        "backward (the inverse) and it tells you how much to bake to use exactly the flour "
        "and sugar you have. This \"solve A x = r for x\" is the exact question of the next "
        "topic — linear systems."
    )
