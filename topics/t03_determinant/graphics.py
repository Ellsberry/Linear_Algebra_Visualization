"""Example 4 -- Graphics (sign, collapse, and the Topic 4 cliffhanger)."""
import numpy as np
import streamlit as st

from engine import animate
from engine import plotting as plot
from engine import widgets as w

_E4_PRESETS = {
    "Mirror (reflection)": {
        "A": np.array([[-1.0, 0.0], [0.0, 1.0]]),
        "notice": (
            "Games flip sprites to draw reflections, and use the *sign* of the determinant "
            "to tell which way a surface faces — that's how an engine skips drawing the "
            "hidden back of an object (back-face culling)."
        ),
    },
    "Shadow (collapse)": {
        "A": np.array([[1.0, 0.0], [0.0, 0.0]]),
        "notice": (
            "A shadow flattens an object onto the ground. det = 0 means the area is gone — "
            "and you can't rebuild the rocket from its shadow. There is no way to undo it."
        ),
    },
}


def _example_graphics():
    from . import _det_meter

    st.markdown(
        "**Graphics.** The sign of the determinant tells you if orientation flipped; "
        "zero means the object has been collapsed to a lower dimension."
    )
    preset = st.selectbox("Preset", list(_E4_PRESETS), key="t03e4_preset")
    info = _E4_PRESETS[preset]

    if st.session_state.get("t03e4_last") != preset:
        w.set_matrix_state("t03e4_A", info["A"])
        st.session_state["t03e4_last"] = preset

    st.info(info["notice"])
    A = w.matrix_editor("t03e4_A", 2, label="Matrix A")
    t = w.scalar_slider("t03e4_t", "Morph t: identity → matrix A", 0.0, 1.0, 1.0, 0.01)

    At = animate.interpolate(A, t)
    det = float(np.linalg.det(At))

    left, right = st.columns([0.5, 0.5], gap="large")

    with left:
        at00, at01 = float(At[0, 0]), float(At[0, 1])
        at10, at11 = float(At[1, 0]), float(At[1, 1])

        st.markdown(f"**Current transform (morph t = {t:.2f}):**")
        st.latex(r"A_t = " + w.bmatrix(At))
        st.markdown("**Your matrix A (the destination at t = 1):**")
        st.latex(r"A = " + w.bmatrix(A))

        det_live = at00 * at11 - at01 * at10
        st.latex(
            r"\det A_t = a \cdot d - b \cdot c = ("
            + f"{at00:.4g}" + r")(" + f"{at11:.4g}" + r") - ("
            + f"{at01:.4g}" + r")(" + f"{at10:.4g}" + r")"
            + r" = \mathbf{" + f"{det_live:.4f}" + r"}"
        )
        st.markdown(
            "negative ⇒ orientation flipped (mirror image); 0 ⇒ area collapsed to nothing."
        )

        nose = plot._ROCKET[:, 0]
        fin_tip = plot._ROCKET[:, 3]
        window = plot._ROCKET_WINDOW

        st.markdown("**At · (rocket vertices):**")
        for label, x in [("nose", nose), ("right fin tip", fin_tip), ("window", window)]:
            xp = At @ x
            st.latex(
                r"{\small "
                + w.bmatrix(At)
                + r" \cdot \begin{pmatrix}"
                + f"{x[0]:.2f}" + r" \\ " + f"{x[1]:.2f}"
                + r"\end{pmatrix} = \begin{pmatrix}"
                + f"{xp[0]:.2f}" + r" \\ " + f"{xp[1]:.2f}"
                + r"\end{pmatrix}}"
                + r"\quad \text{(" + label + r")}"
            )
        st.markdown("Every other vertex transforms the same way.")

    with right:
        st.plotly_chart(plot.figure_2d(At, obj="rocket"), use_container_width=True)
        _det_meter(det, kind="area_sq")

    st.info(
        "det = 0 means this transform has no inverse — the flattened rocket can't "
        "be turned back. Topic 4 is about exactly which transformations can be "
        "undone, and how."
    )
