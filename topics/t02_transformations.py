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
A matrix is a **function that transforms space**. Feed it a vector, it hands
back a new vector. The columns of the matrix tell you exactly where the basis
vectors (**î**, **ĵ**, and in 3D **ẑ**) land — and everything else follows,
because every vector is a combination of those.

Watch the grid deform. Edit the matrix cells, or pick an example, and slide the
**Morph** control to see the identity turn into your matrix.
"""

# Each preset returns the target matrix for the given dimension, plus a "notice".
_NOTICE = {
    "Identity": "Nothing moves — every vector maps to itself.",
    "Shear": "Layers slide sideways; the area is unchanged (det = 1).",
    "Rotation 45°": "The whole space spins. Lengths and angles are preserved.",
    "Reflection": "Space is flipped across an axis — orientation reverses (det < 0).",
    "Scale ×2": "Everything stretches away from the origin; area/volume grows.",
    "Collapse (singular)": "Space is squashed flat — this transform can't be undone (det = 0).",
    "Custom": "Edit the matrix cells yourself and watch the effect.",
}
PRESET_NAMES = list(_NOTICE.keys())


def _build_preset(name: str, dim: int):
    """Return the matrix for a preset, or None for 'Custom' (leave cells as-is)."""
    if name == "Custom":
        return None
    M = np.eye(dim)
    if name == "Identity":
        return M
    if name == "Shear":
        M[0, 1] = 1.0
        return M
    if name == "Rotation 45°":
        a = np.pi / 4
        c, s = np.cos(a), np.sin(a)
        M[0, 0], M[0, 1], M[1, 0], M[1, 1] = c, -s, s, c
        return M
    if name == "Reflection":
        M[1, 1] = -1.0
        return M
    if name == "Scale ×2":
        return 2.0 * np.eye(dim)
    if name == "Collapse (singular)":
        M[1, 1] = 0.0
        return M
    return M


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

        preset = st.selectbox("Example", PRESET_NAMES, key="t02_preset")

        # Apply a preset only when the (preset, dim) selection changes, so manual
        # cell edits are preserved afterwards.
        signature = (preset, dim)
        if st.session_state.get("t02_last") != signature:
            M_preset = _build_preset(preset, dim)
            if M_preset is not None:
                w.set_matrix_state("t02_A", M_preset)
            st.session_state["t02_last"] = signature

        st.info(_NOTICE[preset], icon="💡")

        M = w.matrix_editor("t02_A", dim, label="Matrix M (its columns = where the basis lands)")

        t = w.scalar_slider("t02_t", "Morph: identity → matrix", 0.0, 1.0, 1.0, step=0.01)

        show_vec = st.checkbox("Show a sample vector v", value=False, key="t02_showvec")
        v = None
        if show_vec:
            default_v = [1.0, 1.0] if dim == 2 else [1.0, 1.0, 1.0]
            v = w.vector_editor("t02_v", dim, default_v, label="Vector v")

        st.button("↺ Reset to identity", on_click=_reset)

    Mt = interpolate(M, t)
    vt = (Mt @ v) if (show_vec and v is not None) else None

    with right:
        if dim == 2:
            st.plotly_chart(plot.figure_2d(Mt, show_vec, v, vt), use_container_width=True)
        else:
            st.caption("Drag to rotate · scroll to zoom")
            st.plotly_chart(plot.figure_3d(Mt, show_vec, v, vt), use_container_width=True)

    with st.expander("Show the math"):
        det = float(np.linalg.det(M))
        st.latex(r"M = " + w.bmatrix(M))
        st.markdown(
            f"**Determinant** = `{det:.3f}` — the factor by which "
            f"{'area' if dim == 2 else 'volume'} is scaled."
            + (" Negative ⇒ orientation flips." if det < 0 else "")
            + (" **Zero ⇒ space collapses and M has no inverse.**" if abs(det) < 1e-9 else "")
        )
        st.markdown("The basis vectors land on the **columns** of M:")
        cols_latex = " ,\\quad ".join(
            (["\\hat{i}", "\\hat{j}", "\\hat{z}"][k] + r" \to " + w.bmatrix(M[:, k]))
            for k in range(dim)
        )
        st.latex(cols_latex)
        if show_vec and v is not None:
            st.latex(r"M\,v = " + w.bmatrix(M) + w.bmatrix(v.reshape(-1, 1))
                     + r" = " + w.bmatrix((M @ v).reshape(-1, 1)))

    with st.expander("Try this"):
        st.markdown(
            "- Make a matrix whose **determinant is negative**. What happens to the square/cube?\n"
            "- Find a non-identity matrix that leaves the sample vector **v pointing the same way** "
            "(only its length changes). You've just found an *eigenvector* — Topic 8.\n"
            "- Set a column equal to another column. Why does the area collapse to zero?"
        )
