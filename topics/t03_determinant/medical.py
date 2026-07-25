"""Example 2 -- Medical imaging."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w


def _scale(s):
    return np.array([[s, 0.0], [0.0, s]])


def _rot(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


_E2_PRESETS = {
    "Wrong pixel size (rescale)": {
        "A": np.array([[1.2, 0.0], [0.0, 1.2]]),
        "sweep": lambda t: _scale(1.0 + 0.2 * t),
        "notice": (
            "The image was captured at the wrong pixel size, so the transform scales "
            "everything up by 1.2×. The phantom's area comes out 1.44× its true size: "
            "det = 1.44 ≠ 1. That mismatch is how the error is caught — the scan is "
            "rejected and reshot, not \"corrected\" by multiplying."
        ),
    },
    "Tilt correction (rotation)": {
        "A": _rot(np.radians(20)),
        "sweep": lambda t: _rot(np.radians(20) * t),
        "notice": (
            "The transform is a pure 20° rotation to line the scan up. Rotation moves the "
            "phantom without stretching it, so its area is unchanged: det = 1. The scan "
            "passes — a tumor measured afterward is still its true size."
        ),
    },
}


def _example_medical():
    # --- full-width description + context notice ---
    st.markdown(
        "**Medical imaging.** Before anyone measures a tumor or a vessel, the software "
        "rotates and squares up the raw image — maybe the patient was tilted, or this "
        "scan has to match one from last month. But first it runs a calibration test. "
        "A CT or MRI scanner is checked against a **phantom** — a physical object of "
        "precisely known dimensions (a grid, circles, or in our example a red square of "
        "exact size) scanned as part of the session. The software multiplies the "
        "phantom by the transform A. If det(A) = 1, the area came through unchanged and "
        "the scan is trustworthy. If det(A) ≠ 1, the transform distorted the size — the "
        "scan is rejected and another is made."
    )

    preset = st.selectbox("Preset", list(_E2_PRESETS), key="t03e2_preset")
    info = _E2_PRESETS[preset]

    st.caption(info["notice"])
    A = info["A"]

    sc, _ = st.columns([0.5, 0.5])
    with sc:
        t = w.scalar_slider("t03e2_t", "Morph t: raw scan → aligned",
                            0.0, 1.0, 1.0, 0.01)

    At = info["sweep"](t)
    det = float(np.linalg.det(At))

    left, right = st.columns([0.5, 0.5], gap="large")

    with left:
        mcol1, mcol2 = st.columns(2)
        with mcol1:
            st.markdown(f"**Current transform (t = {t:.2f}):**")
            w.editable_matrix(None, 2, label="A_t", editable=False, value=At,
                              compact=True)
        with mcol2:
            st.markdown("**Destination A (t = 1):**")
            w.editable_matrix(None, 2, label="A", editable=False, value=A,
                              compact=True)
        st.caption("A_t shows how the scan transforms as the image is repositioned.")

        at00, at01 = float(At[0, 0]), float(At[0, 1])
        at10, at11 = float(At[1, 0]), float(At[1, 1])
        det_at = at00 * at11 - at01 * at10
        st.latex(
            r"\det A_t = ("
            + f"{at00:.2f}" + r")(" + f"{at11:.2f}" + r") - ("
            + f"{at01:.2f}" + r")(" + f"{at10:.2f}" + r")"
            + r" = \mathbf{" + f"{det_at:.2f}" + r"}"
        )
        st.markdown(
            f"**Measured area, before → after:** "
            f"region area before = 1.00 → after = |det At| × 1.00 = "
            f"**{abs(det):.2f}**"
        )

        st.markdown("**A · (phantom corners):**")
        for cx, cy in [(0., 0.), (1., 0.), (1., 1.), (0., 1.)]:
            x = np.array([cx, cy])
            xp = At @ x
            st.latex(
                r"{\small "
                + w.bmatrix(At)
                + r" \cdot \begin{pmatrix}"
                + f"{cx:.0f}" + r" \\ " + f"{cy:.0f}"
                + r"\end{pmatrix} = \begin{pmatrix}"
                + f"{xp[0]:.2f}" + r" \\ " + f"{xp[1]:.2f}"
                + r"\end{pmatrix}}"
            )

        st.markdown(
            "A rotation keeps det = 1: it moves the scan without changing any area."
        )

    with right:
        # asymmetric scan outline (wider than tall) and its 1 cm^2 lesion --
        # the same four corners the "At . (lesion corners)" math above lists,
        # so the shaded area the student watches IS the measured-area number.
        SCAN = [np.array(p) for p in [(-2, -1.5), (3, -1), (2.5, 2), (-1.5, 1.5)]]
        LESION = [np.array(p) for p in [(0, 0), (1, 0), (1, 1), (0, 1)]]
        MARK = np.array([3, -1])  # one scan corner, doubles as an orientation mark

        fig = plot.new_figure_2d(rng=5, x_title="cm →", y_title="cm ↑")
        # ghost = before (identity position), faint:
        plot.shade_polygon(fig, SCAN, "rgba(120,144,156,0.18)", "raw scan (before)",
                           line_color="rgba(160,170,180,0.7)", line_width=2)
        plot.shade_polygon(fig, LESION, "rgba(120,144,156,0.30)",
                           line_color="rgba(160,170,180,0.7)", line_width=1)
        # solid = after (At applied), bold:
        plot.shade_polygon(fig, [At @ p for p in SCAN], "rgba(32,201,151,0.15)",
                           "aligned scan (after)", line_color="#20c997", line_width=2)
        plot.shade_polygon(fig, [At @ p for p in LESION], "rgba(255,107,107,0.40)",
                           "phantom (known size)", line_color="#ff6b6b", line_width=2)
        # orientation mark on both positions so a rotation is unmistakable:
        plot.add_point_2d(fig, MARK, "#adb5bd", "orientation mark (before)")
        plot.add_point_2d(fig, At @ MARK, "#ff6b6b", "orientation mark (after)")
        st.plotly_chart(fig, use_container_width=True)

        from . import _det_meter
        _det_meter(det, kind="area_sq")

    # --- full-width closing ---
    st.markdown(
        "**Topic 4:** Actually *undoing* a distortion — turning a tilted "
        "scan back into a square one — means applying the transform's "
        "**inverse**. That's the next topic; here we're just seeing how the "
        "determinant tells us whether area was preserved."
    )
