"""
Topic 2 -- Linear Transformations: a matrix is a function that moves space.

This module is the template for every other topic. To add a new topic, copy
this file, change TITLE / SLUG / INTRO, the PRESETS, and the body of render().
Reuse engine.widgets and engine.plotting so the look and behaviour stay
consistent.
"""
import numpy as np
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

TITLE = "2 · Linear Transformations"
SLUG = "transformations"

INTRO = """
Throughout this course we'll keep meeting the equation **Ax = b**. Here's the
first piece of it. The matrix **A** is a function that transforms space. Apply it
to a vector **x** — written **A·x**, the matrix on the left acting on x — and out
comes a new vector, the result **b**. So **Ax = b** just says "apply A to x, and
you land on b." Right now we're exploring that forward action — *what A does to
x*. Later we'll turn it around and ask the harder question: given b, which x gets
you there?

Two words we'll use a lot:
- A **vertex** is a corner of the shape — a specific point, like a corner of the
  parallelogram below. "Vertex" is the geometry word.
- A **vector** is the arrow from the origin to that point — the column of numbers
  you actually multiply by A. "Vector" is the algebra word.

These are two views of the same thing: **every corner of a shape is described by
a vector**, and that's exactly why a matrix can transform a shape — it multiplies
the vector of each corner, and the corners move.

The columns of A tell you where the basis vectors (î, ĵ) land. Pick a preset
below (or choose Custom to set the four entries yourself) and watch the
parallelogram transform.
"""

# Each preset's notice ends with where this transformation shows up in the
# real world.
_NOTICE = {
    "Identity": "Nothing moves — every vector maps to itself. It's the "
                "\"do nothing\" transform that every animation morphs out of.",
    "Shear": "Layers slide sideways; the area is unchanged (det = 1). Italic "
             "fonts are a shear of upright letters, and so is the slanted look "
             "of a 2.5D game.",
    "Rotation 45°": "The whole space spins; lengths and angles are preserved. "
                    "This happens every time a game rotates your character or "
                    "your phone re-orients a photo.",
    "Reflection": "Space is flipped across an axis — orientation reverses "
                  "(det < 0). Mirror modes in art programs, and reflections "
                  "across water in games, are exactly this matrix.",
    "Scale ×2": "Everything stretches away from the origin; area/volume grows. "
                "Zooming in, and resizing any image or sprite, is this.",
    "Non-uniform scale": "Each axis is stretched by a different amount. It's how "
                         "you squash a sprite into a 'short and wide' cartoon "
                         "look — the axes scaled unequally.",
    "General warp": "A general transformation that stretches and skews at once. "
                    "'Liquify' and image-morphing filters bend a picture like "
                    "this. When A acts on most vectors it swings them to point a "
                    "new way — but a few special vectors come out pointing along "
                    "the *same line* they started on (same direction or exactly "
                    "opposite, just longer or shorter). Turn on the sample vector, "
                    "type different values into **x**, and compare its arrow (x) "
                    "with its image (A·x): for most x they point different ways. "
                    "Find a direction where A·x lies right along x — then look for "
                    "a *second* one. Those are **eigenvectors** (Topic 8), and most "
                    "2D transforms have two.",
    "Collapse (singular)": "Space is squashed flat — this transform can't be "
                           "undone (det = 0). It's the math of a shadow: a flat "
                           "shadow is 3D squashed down, and you can't rebuild the "
                           "object from its shadow alone.",
    "Custom": "Edit the matrix cells yourself and watch the effect.",
}
PRESET_NAMES = list(_NOTICE.keys())

# Fixed matrices for every preset except "Custom" (built live from the four
# number_inputs instead).
_PRESET_MATRICES = {
    "Identity": np.array([[1.0, 0.0], [0.0, 1.0]]),
    "Shear": np.array([[1.0, 1.0], [0.0, 1.0]]),
    "Rotation 45°": np.array([[0.707, -0.707], [0.707, 0.707]]),
    "Reflection": np.array([[1.0, 0.0], [0.0, -1.0]]),
    "Scale ×2": np.array([[2.0, 0.0], [0.0, 2.0]]),
    "Non-uniform scale": np.array([[2.0, 0.0], [0.0, 0.5]]),
    "General warp": np.array([[1.0, 0.5], [-0.5, 1.2]]),
    "Collapse (singular)": np.array([[1.0, 2.0], [2.0, 4.0]]),
}

# An asymmetric parallelogram, one corner in each quadrant, no 0s or 1s so no
# corner is mistakable for a basis vector. Columns are the four corners.
CORNERS = np.array([
    [-3.0, 4.0, 3.0, -4.0],
    [-2.0, -1.0, 4.0, 3.0],
])

VIEW = 14


def _corner_latex(A: np.ndarray, v: np.ndarray) -> str:
    """Return LaTeX showing the numeric matrix A times corner v equals result."""
    result = A @ v
    return w.bmatrix(A) + w.bmatrix(v.reshape(-1, 1)) + r" = " + w.bmatrix(result.reshape(-1, 1))


def render():
    st.markdown(INTRO)

    if "t02_preset" not in st.session_state:
        st.session_state["t02_preset"] = "Identity"

    # --- control band: Matrix A + notice left, preset buttons right ---
    band_left, band_right = st.columns([0.5, 0.5], gap="large")

    with band_right:
        st.markdown("**Choose a transformation**")
        rows = [PRESET_NAMES[i:i + 3] for i in range(0, len(PRESET_NAMES), 3)]
        for row in rows:
            btn_cols = st.columns(3)
            for btn_col, name in zip(btn_cols, row):
                with btn_col:
                    if st.button(name, key=f"t02_btn_{name}", use_container_width=True):
                        st.session_state["t02_preset"] = name
        preset = st.session_state["t02_preset"]

        if preset == "Custom":
            st.caption("Set the four entries of A:")
            r1c1, r1c2 = st.columns(2)
            with r1c1:
                a11 = st.number_input("a11", value=1.0, step=0.1, format="%.2f",
                                      key="t02_custom_a11")
            with r1c2:
                a12 = st.number_input("a12", value=0.0, step=0.1, format="%.2f",
                                      key="t02_custom_a12")
            r2c1, r2c2 = st.columns(2)
            with r2c1:
                a21 = st.number_input("a21", value=0.0, step=0.1, format="%.2f",
                                      key="t02_custom_a21")
            with r2c2:
                a22 = st.number_input("a22", value=1.0, step=0.1, format="%.2f",
                                      key="t02_custom_a22")
            A = np.array([[a11, a12], [a21, a22]])
        else:
            A = _PRESET_MATRICES[preset]

    with band_left:
        st.latex(r"A = " + w.bmatrix(A))
        st.caption("Columns = where î and ĵ land.")
        st.markdown("The basis vectors land on the **columns** of A:")
        st.latex(r"\hat{i} \to " + w.bmatrix(A[:, 0]) + r" \quad \hat{j} \to " + w.bmatrix(A[:, 1]))

    # --- two-column row: corner math/determinant/meaning/notice left, graph right ---
    left, right = st.columns([0.5, 0.5], gap="large")

    with left:
        st.markdown("**Where each corner lands**")
        for i in range(CORNERS.shape[1]):
            st.latex(r"{\small " + _corner_latex(A, CORNERS[:, i]) + r"}")

        det = float(np.linalg.det(A))
        st.markdown(f"**Determinant:** `{det:.3f}`")
        meaning = f"Area is multiplied by **|det|** = `{abs(det):.3f}`."
        if det < 0:
            meaning += " The **negative sign** means orientation flips (a mirror image)."
        if abs(det) < 1e-9:
            meaning += " **det = 0 means the transform collapses space** — A has no inverse."
        st.markdown(meaning)
        st.info(_NOTICE[preset], icon="💡")

    with right:
        fig = plot.new_figure_2d(VIEW)
        before_pts = [tuple(CORNERS[:, i]) for i in range(CORNERS.shape[1])]
        after = A @ CORNERS
        after_pts = [tuple(after[:, i]) for i in range(after.shape[1])]
        plot.shade_polygon(fig, before_pts, "rgba(0,0,0,0)", "before (original)",
                           line_color="rgba(190,190,190,0.55)", line_width=1.5)
        plot.shade_polygon(fig, after_pts, "rgba(255,140,0,0.35)", "after (A applied)",
                           line_color="#ff8c00", line_width=3)
        st.plotly_chart(fig, use_container_width=True)
