"""Example 2 -- Medical imaging."""
import numpy as np
import streamlit as st

from engine import animate
from engine import plotting as plot
from engine import widgets as w
from engine.layout import two_col

_E2_PRESETS = {
    "Calibration (rescale)": {
        "A": np.array([[1.5, 0.0], [0.0, 1.5]]),
        "notice": (
            "If a scan is rescaled, every measured area — a tumor, a vessel — scales by "
            "the determinant. Radiologists calibrate so a 2 cm lesion still measures 2 cm."
        ),
    },
    "Tilt correction (shear)": {
        "A": np.array([[1.0, 0.6], [0.0, 1.0]]),
        "notice": (
            "When software shears a tilted scan into alignment, the shape skews but the "
            "area is unchanged (det = 1) — the correction doesn't falsify any measurement."
        ),
    },
}


def _example_medical():
    from . import _det_meter

    # --- full-width description + context notice ---
    st.markdown(
        "**Medical imaging.** A scan alignment matrix rescales or shears the image. "
        "The determinant tells you how every measured area inside the scan changes."
    )
    st.info(
        "This matrix is how the scanner's image is being **stretched or skewed**. "
        "Change its entries (or pick a preset) and watch the scan region deform; the "
        "determinant tells you whether the **area** of anything you measure — a tumor, "
        "a vessel — got bigger, smaller, or stayed the same. "
        "**What to look for:** the *Calibration* preset scales everything up, so areas "
        "grow (det > 1); the *Tilt correction* shear skews the shape but "
        "**keeps the area unchanged (det = 1)** — that's the important case, because a "
        "measurement taken after it is still trustworthy."
    )

    # --- two-column body ---
    left, right = two_col()

    with left:
        preset = st.selectbox("Preset", list(_E2_PRESETS), key="t03e2_preset")
        info = _E2_PRESETS[preset]

        if st.session_state.get("t03e2_last") != preset:
            w.set_matrix_state("t03e2_A", info["A"])
            st.session_state["t03e2_last"] = preset

        st.caption(info["notice"])
        A = w.editable_matrix("t03e2_A", 2, label="Alignment matrix A")
        t = w.scalar_slider("t03e2_t", "Morph t: identity → matrix A",
                            0.0, 1.0, 1.0, 0.01)

    At = animate.interpolate(A, t)
    det = float(np.linalg.det(At))

    with left:
        _det_meter(det, kind="area_sq")

        # --- math (always visible, no expander) ---
        st.markdown(f"**Current transform (morph t = {t:.2f}):**")
        w.editable_matrix(None, 2, label="A_t", editable=False, value=At)

        st.markdown("**Your matrix A (destination at t = 1):**")
        st.latex(r"A = " + w.bmatrix(A))

        at00, at01 = float(At[0, 0]), float(At[0, 1])
        at10, at11 = float(At[1, 0]), float(At[1, 1])
        det_at = at00 * at11 - at01 * at10
        st.latex(
            r"\det A_t = ("
            + f"{at00:.4g}" + r")(" + f"{at11:.4g}" + r") - ("
            + f"{at01:.4g}" + r")(" + f"{at10:.4g}" + r")"
            + r" = \mathbf{" + f"{det_at:.4f}" + r"}"
        )
        st.markdown(
            f"**Measured area, before → after:** "
            f"region area before = 1.00 → after = |det At| × 1.00 = "
            f"**{abs(det_at):.2f}**"
        )

        st.markdown("**At · (scan region corners):**")
        for cx, cy in [(0., 0.), (1., 0.), (1., 1.), (0., 1.)]:
            x = np.array([cx, cy])
            xp = At @ x
            st.latex(
                r"A_t \cdot \begin{pmatrix}"
                + f"{cx:.0f}" + r" \\ " + f"{cy:.0f}"
                + r"\end{pmatrix} = \begin{pmatrix}"
                + f"{xp[0]:.2f}" + r" \\ " + f"{xp[1]:.2f}"
                + r"\end{pmatrix}"
            )

        st.markdown(
            "det = 1 means the area is preserved even though the shape changed "
            "(the tilt correction)."
        )

    with right:
        st.plotly_chart(plot.figure_2d(At, obj="square"),
                        use_container_width=True)

    # --- full-width closing ---
    st.markdown(
        "**Topic 4:** Actually *undoing* a distortion — turning a tilted scan back "
        "into a square one — means applying the transform's **inverse**. That's the "
        "next topic; here we're just seeing how the determinant tells us whether area "
        "was preserved."
    )
