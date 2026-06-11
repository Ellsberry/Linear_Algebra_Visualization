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
from engine.animate import interpolate

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
- A **vertex** is a corner of the shape — a specific point, like the nose of the
  rocket or the (1,1) corner of the square. "Vertex" is the geometry word.
- A **vector** is the arrow from the origin to that point — the column of numbers
  you actually multiply by A. "Vector" is the algebra word.

These are two views of the same thing: **every corner of a shape is described by
a vector**, and that's exactly why a matrix can transform a shape — it multiplies
the vector of each corner, and the corners move.

The columns of A tell you where the basis vectors (î, ĵ, and in 3D ẑ) land. Watch
the grid deform: edit the cells of A or pick an example, and drag the **Morph**
slider to see the identity turn into your matrix A.
"""

# Each preset returns the target matrix for the given dimension, plus a "notice"
# that ends with where this transformation shows up in the real world.
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


def _build_preset(name: str, dim: int):
    """Return the matrix for a preset, or None for 'Custom' (leave cells as-is)."""
    if name == "Custom":
        return None
    A = np.eye(dim)
    if name == "Identity":
        return A
    if name == "Shear":
        A[0, 1] = 1.0
        return A
    if name == "Rotation 45°":
        a = np.pi / 4
        c, s = np.cos(a), np.sin(a)
        A[0, 0], A[0, 1], A[1, 0], A[1, 1] = c, -s, s, c
        return A
    if name == "Reflection":
        A[1, 1] = -1.0
        return A
    if name == "Scale ×2":
        return 2.0 * np.eye(dim)
    if name == "Non-uniform scale":
        factors = [2.0, 1.0] if dim == 2 else [2.0, 1.0, 0.5]
        return np.diag(factors)
    if name == "General warp":
        A[0, 0], A[0, 1], A[1, 0], A[1, 1] = 2.0, 1.0, 1.0, 3.0
        return A  # in 3D the z-axis is left alone, so the warp acts on the xy-plane
    if name == "Collapse (singular)":
        A[1, 1] = 0.0
        return A
    return A


def _corner_latex(T: np.ndarray, v: np.ndarray) -> str:
    """Return LaTeX showing the live numeric matrix T times v equals result."""
    result = T @ v
    return w.bmatrix(T) + w.bmatrix(v.reshape(-1, 1)) + r" = " + w.bmatrix(result.reshape(-1, 1))


def _reset():
    """Reset callback: jump back to Identity. Runs before the rerun."""
    st.session_state["t02_preset"] = "Identity"
    st.session_state["t02_last"] = None


def render():
    st.markdown(INTRO)

    left, right = st.columns([1.05, 1.35], gap="large")

    with left:
        dim = 3 if st.radio("Space", ["2D", "3D"], horizontal=True,
                            key="t02_dim") == "3D" else 2

        obj = "square"
        if dim == 2:
            obj = "rocket" if st.radio(
                "Object", ["Unit square", "Rocket 🚀"], horizontal=True,
                key="t02_obj") == "Rocket 🚀" else "square"

        preset = st.selectbox("Example", PRESET_NAMES, key="t02_preset")

        # Apply a preset only when the (preset, dim) selection changes, so manual
        # cell edits are preserved afterwards.
        signature = (preset, dim)
        if st.session_state.get("t02_last") != signature:
            A_preset = _build_preset(preset, dim)
            if A_preset is not None:
                w.set_matrix_state("t02_A", A_preset)
            # The eigenvector hunt only makes sense with the sample vector shown.
            if preset == "General warp":
                st.session_state["t02_showvec"] = True
            st.session_state["t02_last"] = signature

        st.info(_NOTICE[preset], icon="💡")

        A = w.matrix_editor("t02_A", dim, label="Matrix A (its columns = where the basis lands)")

        t = w.scalar_slider("t02_t", "Morph t: identity → matrix A", 0.0, 1.0, 1.0, step=0.01)

        show_vec = st.checkbox("Show a sample vector x", value=False, key="t02_showvec")
        x = None
        if show_vec:
            default_x = [1.0, 1.0] if dim == 2 else [1.0, 1.0, 1.0]
            x = w.vector_editor("t02_v", dim, default_x, label="Vector x")

        st.button("↺ Reset to identity", on_click=_reset)

    At = interpolate(A, t)
    xt = (At @ x) if (show_vec and x is not None) else None

    with right:
        if dim == 2:
            st.plotly_chart(plot.figure_2d(At, show_vec, x, xt, obj=obj),
                            use_container_width=True)
        else:
            st.caption("Drag to rotate · scroll to zoom")
            st.plotly_chart(plot.figure_3d(At, show_vec, x, xt), use_container_width=True)

    with st.expander("Show the math"):
        det_final = float(np.linalg.det(A))
        det_live = float(np.linalg.det(At))
        dim_word = "area" if dim == 2 else "volume"
        st.latex(r"A = " + w.bmatrix(A))
        det_msg = (
            f"**Determinant now:** `{det_live:.3f}` "
            f"· **final (your matrix A):** `{det_final:.3f}`"
        )
        if det_final < 0:
            det_msg += " Negative final value ⇒ orientation flips."
        if abs(det_final) < 1e-9:
            det_msg += " **Zero final value ⇒ space collapses and A has no inverse.**"
        st.markdown(det_msg)
        st.markdown(
            f"**Meaning:** The determinant tells you how the transform scales "
            f"{dim_word}: {dim_word} is multiplied by **|det|**, and the **sign** of the "
            f"determinant tells you whether orientation flipped (negative = mirror image)."
        )
        mid_morph = (
            "(Mid-morph the shape isn't a pure rotation yet, so its determinant dips "
            "below 1; at t = 1 it's exactly 1."
        )
        if det_final < 0:
            mid_morph += (
                " For a reflection the live determinant likewise dips through 0 "
                "before reaching its final negative value."
            )
        mid_morph += ")"
        st.markdown(mid_morph)
        st.markdown("The basis vectors land on the **columns** of A:")
        cols_latex = " ,\\quad ".join(
            (["\\hat{i}", "\\hat{j}", "\\hat{z}"][k] + r" \to " + w.bmatrix(A[:, k]))
            for k in range(dim)
        )
        st.latex(cols_latex)
        if show_vec and x is not None:
            st.latex(r"A\,x = " + w.bmatrix(A) + w.bmatrix(x.reshape(-1, 1))
                     + r" = " + w.bmatrix((A @ x).reshape(-1, 1)))

        st.markdown("---")
        st.markdown("**Where each corner lands**")
        if abs(t) < 0.01:
            t_word = "the identity — nothing moves"
        elif abs(t - 1.0) < 0.01:
            t_word = "your full matrix A"
        else:
            t_word = "part-way from the identity to A"
        st.markdown(
            f"These are the matrix's numbers right now "
            f"(morph **t = {t:.2f}** — {t_word}). "
            f"Drag t to 1 to reach A."
        )

        if dim == 2:
            if obj == "square":
                for v_col in [np.array([0.0, 0.0]), np.array([1.0, 0.0]),
                               np.array([1.0, 1.0]), np.array([0.0, 1.0])]:
                    st.latex(_corner_latex(At, v_col))
            else:  # rocket
                nose = plot._ROCKET[:, 0]
                fin_tip = plot._ROCKET[:, 3]
                window = plot._ROCKET_WINDOW
                for v_col, label in [(nose, "nose"), (fin_tip, "fin tip"), (window, "window")]:
                    st.markdown(f"*{label}*")
                    st.latex(_corner_latex(At, v_col))
                st.markdown("Every other vertex transforms the same way.")
        else:  # 3D
            for v_col in [np.array([1.0, 0.0, 0.0]),
                           np.array([0.0, 1.0, 0.0]),
                           np.array([0.0, 0.0, 1.0])]:
                st.latex(_corner_latex(At, v_col))

        st.markdown(
            "> Two of these corners are special. The corner **(1,0)** is the basis vector **î**,"
            " and **(0,1)** is **ĵ**. Look at where they land: **A · (1,0)** is the **first"
            " column of A**, and **A · (0,1)** is the **second column**. That's the rule from"
            " the top of this topic — \"the columns of A are where the basis vectors go\" — and"
            " you can check it right here."
            " *(Check it with the Morph slider all the way over at t = 1; mid-morph the numbers"
            " above are the columns of the in-between transform, not yet your final A.)*"
        )

    with st.expander("Try this"):
        st.markdown(
            "- Make a matrix whose **determinant is negative**. What happens to the square/cube?\n"
            "- Find a non-identity matrix that leaves the sample vector **x pointing the same way** "
            "(only its length changes). You've just found an *eigenvector* — Topic 8.\n"
            "- Set a column equal to another column. Why does the area collapse to zero?"
        )
