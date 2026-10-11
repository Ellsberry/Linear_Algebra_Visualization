"""Screen 2 -- The transpose A^T (flip rows and columns)."""
import numpy as np
import streamlit as st

from engine import widgets as w

from .screen_inverse import _cbmatrix

_GREEN = "#37b24d"
_BLUE = "#4dabf7"

_DEFAULT_A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

_INTRO = """
The **transpose** of a matrix, written **Aᵀ**, is the matrix you get by flipping
it across its diagonal — every **row** of A becomes a **column** of Aᵀ. If A is
2 rows by 3 columns, Aᵀ is 3 rows by 2 columns. The entry in row i, column j of
A lands in row j, column i of Aᵀ. That's the whole definition. Unlike the
inverse, the transpose **always exists and the matrix does not have to be
square.**
"""

_FLIP_CAPTION = "2×3 becomes 3×2. Row 1 of A — (1, 2, 3) — is now column 1 of Aᵀ."

_SYM_LEAD = "A symmetric matrix is one that equals its own transpose: A = Aᵀ."

_SYM_REST = """That can
only happen for a square matrix, and it means the matrix is a mirror image
across its diagonal — the entry in row i, column j equals the entry in row j,
column i."""

_BRIDGE = """
Here's why the transpose is the last tool we needed before projection. Take any
matrix A — any shape — and multiply it by its own transpose to form **AᵀA**.
That product is always **square** and always **symmetric**, no matter what shape
A started as. In the next topic, when a system `Ax = b` has no exact answer,
we'll multiply both sides by Aᵀ to turn it into a square, solvable system —
`AᵀA x̂ = Aᵀb` — and read the closest answer off of it. You don't need that
formula yet. Just remember: **Aᵀ is what makes a tall, unsolvable system square.**
"""


def render_transpose():
    # Load the spec default once; manual edits persist after that.
    if st.session_state.get("t06b_tr_last") is None:
        w.set_matrix_state("t06b_tr_A", _DEFAULT_A)
        st.session_state["t06b_tr_last"] = "loaded"

    # --- Block 1 -- What the transpose is ------------------------------------
    st.markdown(_INTRO)

    st.divider()

    # --- Block 2 -- Flip it yourself -----------------------------------------
    left, right = st.columns([0.5, 0.5])

    with left:
        A = w.editable_matrix("t06b_tr_A", rows=2, cols=3, label="A")
        m, n = A.shape
        st.markdown(f"A is m×n = **{m}×{n}**")

    with right:
        w.editable_matrix("t06b_tr_AT", editable=False, value=A.T,
                          rows=3, cols=2, label="$A^{T}$")
        st.markdown(f"Aᵀ is n×m = **{n}×{m}**")
        st.caption(_FLIP_CAPTION)

    st.divider()

    # --- Block 3 -- Symmetry, and why the transpose matters next ------------
    st.markdown(
        f"<span style='color:{_GREEN};font-weight:700;'>{_SYM_LEAD}</span> "
        f"{_SYM_REST}",
        unsafe_allow_html=True,
    )
    st.markdown(_BRIDGE)

    # Live confirm: A^T A from the Block-2 matrix is square and symmetric.
    AtA = A.T @ A
    k = AtA.shape[0]
    symmetric = bool(np.allclose(AtA, AtA.T))
    st.latex(
        r"A^{T}A = " + w.bmatrix(A.T) + w.bmatrix(A)
        + " = " + _cbmatrix(AtA, _BLUE)
    )
    st.caption(
        f"AᵀA comes out {k}×{k} — square — and "
        + ("equals its own transpose — symmetric ✓"
           if symmetric else "is NOT symmetric (this should never happen)")
        + " — whatever shape A was."
    )
