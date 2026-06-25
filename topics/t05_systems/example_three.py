"""Example 3 -- Engineering (metal mixing)."""
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

from . import _classify, _E3_PRESETS


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
