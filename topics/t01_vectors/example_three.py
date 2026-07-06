"""Example 3 -- The smoothie mixer (combinations, span, basis)."""
import numpy as np
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

from . import BANANA, PEANUT, PROTEIN_AXIS, SUGAR_AXIS, VIEW

TARGET = np.array([14.0, 11.0])


def _example_three():
    st.markdown(
        "**Every combination at once.** Scale and add both ingredients "
        "freely: c1·(1,4) + c2·(8,2). As you vary the two "
        "sliders, the resultant sweeps out a whole region."
    )

    allow_neg = st.checkbox("Allow negative scoops", key="t01e3_neg")
    lo = -5.0 if allow_neg else 0.0

    # clamp any already-stored slider value into the new bounds so the
    # slider widget doesn't raise when switching from negatives back to
    # non-negative-only
    for key in ("t01e3_c1", "t01e3_c2"):
        if key in st.session_state and st.session_state[key] < lo:
            st.session_state[key] = lo

    c1 = w.scalar_slider("t01e3_c1", "Scoops of banana (c1)", lo, 5.0, 2.0,
                        step=0.25)
    c2 = w.scalar_slider("t01e3_c2", "Scoops of peanut butter (c2)", lo, 5.0,
                        1.5, step=0.25)

    u = c1 * BANANA
    v = c2 * PEANUT
    result = u + v

    det = float(BANANA[0] * PEANUT[1] - BANANA[1] * PEANUT[0])
    A = np.column_stack([BANANA, PEANUT])
    c1_hit, c2_hit = np.linalg.solve(A, TARGET)
    u_hit, v_hit = c1_hit * BANANA, c2_hit * PEANUT
    sum_hit = u_hit + v_hit
    dist = float(np.linalg.norm(result - TARGET))

    left, right = st.columns([0.5, 0.5], gap="large")

    with right:
        fig = plot.new_figure_2d(VIEW, PROTEIN_AXIS, SUGAR_AXIS)
        if allow_neg:
            R = VIEW
            plot.shade_polygon(fig, [(-R, -R), (R, -R), (R, R), (-R, R)],
                               "rgba(0,150,136,0.13)", "span (whole plane)")
        else:
            B = 14
            plot.shade_polygon(fig, [(0, 0), B * BANANA, B * (BANANA + PEANUT),
                                     B * PEANUT],
                               "rgba(0,150,136,0.13)", "reachable smoothies")
        plot.add_vector_2d(fig, [0, 0], u, "darkorange", "banana (scaled)")
        plot.add_vector_2d(fig, [0, 0], v, "sienna", "peanut butter (scaled)")
        plot.add_vector_2d(fig, [0, 0], result, "crimson", "resultant", width=5)
        plot.add_point_2d(fig, TARGET, "gold", "target (14, 11)", size=15,
                          symbol="star")
        plot.add_point_2d(fig, result, "navy", "your smoothie", size=13)
        st.plotly_chart(fig, use_container_width=True)
        if dist < 0.3:
            st.success("You hit the target smoothie!")

    with left:
        st.latex(rf"{c1:g} \cdot " + w.bmatrix(BANANA.reshape(-1, 1))
                 + rf" + {c2:g} \cdot " + w.bmatrix(PEANUT.reshape(-1, 1))
                 + " = " + w.bmatrix(result.reshape(-1, 1)))
        st.caption("Per axis, to hit the target (14, 11):")
        st.latex(rf"\text{{Protein: }} {BANANA[0]:g}c_1 + {PEANUT[0]:g}c_2 "
                 rf"= {TARGET[0]:g}")
        st.latex(rf"\text{{Sugar: }} {BANANA[1]:g}c_1 + {PEANUT[1]:g}c_2 "
                 rf"= {TARGET[1]:g}")

        lead = (
            "Real smoothies use non-negative scoops. Combining banana and "
            "peanut butter this way reaches the wedge between them -- the "
            "smoothies you can actually make. "
        ) if not allow_neg else ""
        lead += (
            "Mathematically, allowing any coefficients (including "
            "negative) these two independent vectors span the entire "
            "plane -- that is what makes them a basis. Toggle 'Allow "
            "negative scoops' to see the full span. "
        )

        st.markdown(
            lead +
            "Because banana and peanut "
            "butter point in different directions, their combinations "
            "reach every point. Check independence with the determinant: "
            f"det[({BANANA[0]:g},{BANANA[1]:g}),({PEANUT[0]:g},"
            f"{PEANUT[1]:g})] = {BANANA[0]:g}·{PEANUT[1]:g} − "
            f"{BANANA[1]:g}·{PEANUT[0]:g} = {det:g} ≠ 0. Non-zero "
            "means independent means they form a basis: two building-block "
            "vectors that reach every target, each with exactly one "
            f"recipe. For target ({TARGET[0]:g}, {TARGET[1]:g}) the one "
            f"solution is c1 = {c1_hit:g} scoops banana, c2 = {c2_hit:g} "
            f"scoops peanut butter. Check: {c1_hit:g}·({BANANA[0]:g},"
            f"{BANANA[1]:g}) + {c2_hit:g}·({PEANUT[0]:g},"
            f"{PEANUT[1]:g}) = ({u_hit[0]:g},{u_hit[1]:g}) + "
            f"({v_hit[0]:g},{v_hit[1]:g}) = ({sum_hit[0]:g},{sum_hit[1]:g}). "
            "Contrast Screen 1, where one vector spanned only a line -- "
            "two independent vectors span the whole plane. That is a "
            "basis."
        )
