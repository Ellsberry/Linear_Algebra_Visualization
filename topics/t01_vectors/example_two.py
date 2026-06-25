"""Example 2 -- Two ingredients, added (tip-to-tail / parallelogram)."""
import numpy as np
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

from . import BANANA, PEANUT, PROTEIN_AXIS, SUGAR_AXIS, VIEW

_E2_PRESETS = {
    "Tip-to-tail": ("The sum is simply where you land after following one arrow "
                    "and then the other.", BANANA, PEANUT),
    "Same direction": ("Two ingredients pointing the same way just give a longer "
                       "arrow in that direction — nothing new about where you can go.",
                       np.array([2.0, 1.0]), np.array([4.0, 2.0])),
    "Opposite directions": ("Pointing against each other, they partly cancel, and "
                            "the sum comes out shorter than either one.",
                            np.array([3.0, 2.0]), np.array([-2.0, -1.0])),
}


def _example_two():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Two ingredients, added.** Add a second ingredient: peanut butter at "
            "(4, 1). One scoop of each gives a smoothie of banana + peanut butter. "
            "The result is the two arrows laid **tip-to-tail** — walk out along "
            "banana, then keep going along peanut butter, and where you end up is "
            "the sum. Flip to the **parallelogram** view to see the same answer a "
            "second way."
        )
        preset = st.selectbox("Example", list(_E2_PRESETS), key="t01e2_preset")
        notice, u_def, v_def = _E2_PRESETS[preset]

        if st.session_state.get("t01e2_last") != preset:
            w.set_vector_state("t01e2_u", u_def)
            w.set_vector_state("t01e2_v", v_def)
            st.session_state["t01e2_last"] = preset

        st.info(notice, icon="💡")
        view = st.radio("View", ["Tip-to-tail", "Parallelogram"], horizontal=True,
                        key="t01e2_view")
        u = w.vector_editor("t01e2_u", 2, u_def, label="banana (u)")
        v = w.vector_editor("t01e2_v", 2, v_def, label="peanut butter (v)")

    s = u + v
    with right:
        fig = plot.new_figure_2d(VIEW, PROTEIN_AXIS, SUGAR_AXIS)
        if view == "Tip-to-tail":
            plot.add_vector_2d(fig, [0, 0], u, "darkorange", "u")
            plot.add_vector_2d(fig, u, s, "seagreen", "v (from tip of u)")
        else:
            plot.add_vector_2d(fig, [0, 0], u, "darkorange", "u")
            plot.add_vector_2d(fig, [0, 0], v, "seagreen", "v")
            plot.add_vector_2d(fig, u, s, "rgba(0,0,0,0.25)", "", arrow=False,
                               dash="dot", showlegend=False)
            plot.add_vector_2d(fig, v, s, "rgba(0,0,0,0.25)", "", arrow=False,
                               dash="dot", showlegend=False)
        plot.add_vector_2d(fig, [0, 0], s, "crimson", "u + v", width=5)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show the math"):
        st.latex(w.bmatrix(u.reshape(-1, 1)) + " + " + w.bmatrix(v.reshape(-1, 1))
                 + " = " + w.bmatrix(s.reshape(-1, 1)))
        st.caption("Add vectors component by component — protein with protein, "
                   "sugar with sugar.")
