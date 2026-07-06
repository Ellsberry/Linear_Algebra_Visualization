"""Example 2 -- Two ingredients, added (tip-to-tail / parallelogram)."""
import numpy as np
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

from . import BANANA, PEANUT, PROTEIN_AXIS, SUGAR_AXIS, VIEW


def _example_two():
    st.markdown(
        "**Combining two ingredients.** Now use both: c1 scoops of banana "
        "plus c2 scoops of peanut butter. Each scaled vector is added, and "
        "the result is one resultant vector -- your finished smoothie."
    )

    view = st.radio("View", ["Tip-to-tail", "Parallelogram"], horizontal=True,
                    key="t01e2_view")
    c1 = w.scalar_slider("t01e2_c1", "Scoops of banana (c1)", -3.0, 5.0, 3.0,
                        step=0.25)
    c2 = w.scalar_slider("t01e2_c2", "Scoops of peanut butter (c2)", -3.0, 5.0,
                        1.0, step=0.25)

    u = c1 * BANANA
    v = c2 * PEANUT
    s = u + v

    left, right = st.columns([0.5, 0.5], gap="large")

    with right:
        fig = plot.new_figure_2d(VIEW, PROTEIN_AXIS, SUGAR_AXIS)
        if view == "Tip-to-tail":
            plot.add_vector_2d(fig, [0, 0], u, "darkorange", "banana (scaled)")
            plot.add_vector_2d(fig, u, s, "sienna",
                               "peanut butter (from tip of banana)")
        else:
            plot.add_vector_2d(fig, [0, 0], u, "darkorange", "banana (scaled)")
            plot.add_vector_2d(fig, [0, 0], v, "sienna", "peanut butter (scaled)")
            plot.add_vector_2d(fig, u, s, "rgba(0,0,0,0.25)", "", arrow=False,
                               dash="dot", showlegend=False)
            plot.add_vector_2d(fig, v, s, "rgba(0,0,0,0.25)", "", arrow=False,
                               dash="dot", showlegend=False)
        plot.add_vector_2d(fig, [0, 0], s, "crimson", "resultant", width=5)
        st.plotly_chart(fig, use_container_width=True)

    with left:
        st.latex(rf"{c1:g} \cdot " + w.bmatrix(BANANA.reshape(-1, 1))
                 + " + " + rf"{c2:g} \cdot " + w.bmatrix(PEANUT.reshape(-1, 1))
                 + " = " + w.bmatrix(s.reshape(-1, 1)))
        st.caption("Scale each ingredient, then add the results component by "
                   "component -- protein with protein, sugar with sugar.")

        st.markdown(
            f"Reading it per axis: protein = {c1:g}·{BANANA[0]:g} + "
            f"{c2:g}·{PEANUT[0]:g} = {s[0]:g}, sugar = "
            f"{c1:g}·{BANANA[1]:g} + {c2:g}·{PEANUT[1]:g} = "
            f"{s[1]:g}. The resultant is ({s[0]:g}, {s[1]:g}) — a "
            "target banana alone could never reach (it's off banana's line "
            "from Screen 1). Combining two ingredients unlocks points no "
            "single ingredient can. Two vectors pointing in different "
            "directions are the start of a basis; the next screen shows "
            "the full range they reach."
        )
