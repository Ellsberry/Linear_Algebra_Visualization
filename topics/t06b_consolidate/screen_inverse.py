"""Screen 1 -- The inverse A^-1 ("matrix division" that isn't)."""
import numpy as np
import streamlit as st

from engine import widgets as w

_GREEN = "#37b24d"
_YELLOW = "#ffd43b"
_BLUE = "#4dabf7"

_DEFAULT_A = np.array([[2.0, 1.0], [1.0, 3.0]])
_DEFAULT_B = np.array([[3.0], [5.0]])

_INTRO = """
**You can't divide by a matrix.** To solve `Ax = b` with ordinary numbers you'd
divide both sides by A. But there is no such thing as `b / A` — matrix division
is not defined. Instead we build a matrix that *undoes* A, called the
**inverse** and written **A⁻¹**. It's defined by one property: `A⁻¹A = I`, the
identity matrix, which does nothing — the matrix version of multiplying by 1.
"""

_CHAIN_LATEX = r"""
\begin{aligned}
Ax &= b \\
A^{-1}(Ax) &= A^{-1}b \\
(A^{-1}A)\,x &= A^{-1}b \\
Ix &= A^{-1}b \\
x &= A^{-1}b
\end{aligned}
"""

_LEFT_NOTE = """
**Multiply on the LEFT, both sides.** Matrix multiplication does not commute:
`A⁻¹b` is not the same as `bA⁻¹` (the second one may not even be a legal size).
With numbers the order never matters; with matrices it always does. So A⁻¹ goes
on the *left* of both sides, and the order can't be swapped.
"""

_BREAK_MSG = """
**det A = 0 — there is no inverse.** When the determinant is zero, no matrix can
undo A: there is nothing to multiply by, so `x = A⁻¹b` can't even be written.
This is the same "squashed" case as the singular rockets in Vector Spaces — A
collapses the plane, and you can't un-collapse it.
"""

_RULE = """
An inverse exists only when **A is square** (same number of rows and columns)
**and** its **determinant is not zero**. Square is required because A⁻¹ has to
undo A from both sides (`A⁻¹A = AA⁻¹ = I`), and only a square matrix can do
that. Nonzero determinant is required because a zero determinant means A crushes
space flat, and nothing can bring it back. We'll see in the final table that
"square and det ≠ 0" is the same as "full rank."
"""


def _cbmatrix(M, color) -> str:
    """bmatrix with each ENTRY colored (never \\color around the whole bmatrix)."""
    M = np.round(np.atleast_2d(M), 2) + 0.0  # avoid "-0.00"
    rows = r" \\ ".join(
        " & ".join(rf"\color{{{color}}}{{{v:.2f}}}" for v in row) for row in M
    )
    return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"


def render_inverse():
    # Load the spec defaults once; manual edits persist after that.
    if st.session_state.get("t06b_inv_last") is None:
        w.set_matrix_state("t06b_inv_A", _DEFAULT_A)
        w.set_matrix_state("t06b_inv_b", _DEFAULT_B)
        st.session_state["t06b_inv_last"] = "loaded"

    # --- Block 1 -- There is no matrix division -----------------------------
    st.markdown(_INTRO)
    st.latex(_CHAIN_LATEX)
    st.markdown(
        f"<div style='color:{_GREEN};font-weight:700;'>\n\n{_LEFT_NOTE}\n\n</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # --- Block 2 -- Watch it solve, and watch it break ----------------------
    left, right = st.columns([0.5, 0.5])

    with left:
        A = w.editable_matrix("t06b_inv_A", dim=2, label="A")
        b = w.editable_matrix("t06b_inv_b", rows=2, cols=1, label="b")

        det = float(np.linalg.det(A))
        singular = abs(det) < 1e-9
        if singular:
            det = 0.0
        st.latex(rf"\det A = {det:.2f}")

        if singular:
            A_inv = None
        else:
            A_inv = np.linalg.inv(A)
            x = A_inv @ b
            st.latex(r"A^{-1} = " + _cbmatrix(A_inv, _YELLOW))
            st.latex(
                r"x = A^{-1}b = " + _cbmatrix(A_inv, _YELLOW) + w.bmatrix(b)
                + " = " + _cbmatrix(x, _GREEN)
            )
            st.latex(
                r"A\,x = " + w.bmatrix(A) + _cbmatrix(x, _GREEN)
                + " = " + w.bmatrix(A @ x) + r" = b \;\checkmark"
            )

    with right:
        st.markdown("**Check: does A⁻¹ really undo A?**")
        if singular:
            st.markdown("No A⁻¹ exists, so there is nothing to check.")
        else:
            st.latex(
                r"A^{-1}A = " + _cbmatrix(A_inv, _YELLOW) + w.bmatrix(A)
                + " = " + _cbmatrix(A_inv @ A, _BLUE) + r" = I \;\checkmark"
            )

    if singular:
        st.error(_BREAK_MSG)

    st.divider()

    # --- Block 3 -- The rule for the inverse ---------------------------------
    st.markdown(_RULE)
