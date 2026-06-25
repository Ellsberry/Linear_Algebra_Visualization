"""Example 1 -- One ingredient (a vector is already a recipe)."""
import numpy as np
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

from . import BANANA, PROTEIN_AXIS, SUGAR_AXIS, VIEW

_E1_PRESETS = {
    "More scoops": ("The arrow keeps its direction and just gets longer. "
                    "Scaling a vector stretches it without turning it.", 3.0, False),
    "Half a scoop": ("You land halfway out. Scaling works with fractions, "
                     "not just whole steps.", 0.5, False),
    "Read the recipe": ("banana = (1, 4) means 1 step along the protein axis plus "
                        "4 along the sugar axis. So even a single vector is a "
                        "combination of those two axis directions — that's where "
                        "\"basis\" comes from.", 1.0, True),
}


def _example_one():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**One ingredient.** Start with one ingredient — banana, at (1, 4): "
            "one gram of protein and four of sugar per scoop. The slider is how "
            "many scoops. Watch the arrow grow as you add scoops and shrink back "
            "toward the origin as you take them away."
        )
        preset = st.selectbox("Example", list(_E1_PRESETS), key="t01e1_preset")
        notice, c_default, brk_default = _E1_PRESETS[preset]

        if st.session_state.get("t01e1_last") != preset:
            st.session_state["t01e1_c"] = c_default
            st.session_state["t01e1_break"] = brk_default
            st.session_state["t01e1_last"] = preset

        st.info(notice, icon="💡")
        c = w.scalar_slider("t01e1_c", "Scoops of banana", -3.0, 5.0, c_default, step=0.25)
        show_break = st.checkbox("Show the recipe breakdown", key="t01e1_break")

    end = c * BANANA
    with right:
        fig = plot.new_figure_2d(VIEW, PROTEIN_AXIS, SUGAR_AXIS)
        plot.add_vector_2d(fig, [0, 0], BANANA, "rgba(180,140,0,0.45)",
                           "banana (1 scoop)", dash="dot")
        plot.add_vector_2d(fig, [0, 0], end, "darkorange", f"{c:g} scoops")
        if show_break:
            plot.add_vector_2d(fig, [0, 0], [end[0], 0], "crimson",
                               "protein part", dash="dash", arrow=False)
            plot.add_vector_2d(fig, [end[0], 0], end, "royalblue",
                               "sugar part", dash="dash", arrow=False)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show the math"):
        st.latex(rf"{c:g} \cdot " + w.bmatrix(BANANA.reshape(-1, 1))
                 + " = " + w.bmatrix(end.reshape(-1, 1)))
        st.caption("Scaling multiplies every component by the same number.")
