"""
Topic 3 -- Determinant.

Pattern: MULTI-EXAMPLE. A top selector chooses one of four real-world screens;
only the selected screen renders. OVERVIEW pinned at top; HOWTO in a collapsed
expander. Follow the t01 structural template.
"""
import numpy as np
import streamlit as st

from engine import animate
from engine import plotting as plot
from engine import widgets as w
from engine.layout import two_col

TITLE = "3 · Determinant"
SLUG = "determinant"

OVERVIEW = """
A determinant is one number that answers a simple question: when a
transformation acts on space, **by what factor does area (in 2D) or volume (in
3D) change — and does it flip things into a mirror image?** That single number
turns out to matter to surveyors, radiologists, biologists, and game
programmers. We'll meet it in all four fields, and each time you'll see the
determinant *is* an area or a volume — not just a formula.

Here's the formula in letters (the examples fill in real numbers):
"""

HOWTO = """
The left panel sets the numbers; the right panel shows the shape. The
**determinant meter** under each picture shows the determinant and the area or
volume it equals — watch them change together. Open **Show the math** to see
the formula behind the number.
"""

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


# ----------------------------------------------------------------------------
# Shared helper: determinant meter
# ----------------------------------------------------------------------------

def _det_meter(det, kind, extra=None):
    st.metric("Determinant", f"{det:.4f}")
    if abs(det) <= 1e-9:
        st.warning("collapses — area is zero, no inverse.")
    elif det < 0:
        if kind == "area_tri":
            st.info(
                f"det is negative — you listed the corners clockwise. "
                f"Area is still ½|det| = {0.5 * abs(det):.2f} m²; "
                "surveyors keep a consistent corner order to control the sign."
            )
        else:
            st.info(f"orientation flips (det < 0); area = |det| = {abs(det):.2f}")
    else:
        if kind == "area_tri":
            st.markdown(f"area = ½ × |det| = {0.5 * abs(det):.2f} m²")
        elif kind == "area_sq":
            st.markdown(f"area scales by ×{det:.2f}")
        else:  # volume
            st.markdown(
                f"volume = det = {det:.2f}; "
                f"surface = {extra['surface']:.2f}; "
                f"surface:volume = {extra['ratio']:.2f}"
            )


# _det_meter is defined above; submodules import it via `from . import _det_meter`
from .surveying import _example_surveying
from .medical import _example_medical
from .biology import _example_biology


# ----------------------------------------------------------------------------
# Top-level render
# ----------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)
    st.latex(
        r"\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc"
        r"\qquad \text{(2D)}"
    )
    st.latex(
        r"\det \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}"
        r" = a(ei - fh) - b(di - fg) + c(dh - eg)"
        r"\qquad \text{(3D)}"
    )
    st.markdown(
        "The 3D formula looks like a lot, but notice each term is just one top-row entry "
        "times a little 2×2 determinant of what's left — it's the 2D formula used three "
        "times. And when the matrix is simple, like the diagonal one in biology, almost "
        "everything is zero and it collapses to just the diagonal multiplied together."
    )

    st.caption(
        "The left panel sets the numbers and shows the math; the right panel "
        "shows the shape. The determinant meter shows the determinant and the "
        "area or volume it equals — watch them change together."
    )

    example = st.radio(
        "Example",
        ["1 · Surveying", "2 · Medical imaging", "3 · Biology", "4 · Graphics"],
        horizontal=True,
        key="t03_example",
    )
    st.divider()

    if example.startswith("1"):
        _example_surveying()
    elif example.startswith("2"):
        _example_medical()
    elif example.startswith("3"):
        _example_biology()
    else:
        _example_graphics()


# ----------------------------------------------------------------------------
# Example 4 -- Graphics
# ----------------------------------------------------------------------------

def _example_graphics():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
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

    with right:
        st.plotly_chart(plot.figure_2d(At, obj="rocket"), use_container_width=True)
        _det_meter(det, kind="area_sq")
        st.info(
            "det = 0 means this transform has no inverse — the flattened rocket can't "
            "be turned back. Topic 4 is about exactly which transformations can be "
            "undone, and how."
        )

    with st.expander("Show the math"):
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

        st.markdown("**A · (rocket vertices):**")
        for label, x in [("nose", nose), ("right fin tip", fin_tip), ("window", window)]:
            xp = At @ x
            st.latex(
                r"A_t \cdot \begin{pmatrix}"
                + f"{x[0]:.2f}" + r" \\ " + f"{x[1]:.2f}"
                + r"\end{pmatrix} = \begin{pmatrix}"
                + f"{xp[0]:.2f}" + r" \\ " + f"{xp[1]:.2f}"
                + r"\end{pmatrix}"
                + r"\quad \text{(" + label + r")}"
            )
        st.markdown("Every other vertex transforms the same way.")
