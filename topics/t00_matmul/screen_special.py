"""Topic 0, Screen 4 -- special matrices: identity, upper-triangular, RREF.
Exposition only (definitions + why + read-only examples); no practice."""
import numpy as np
import streamlit as st

from engine.widgets import editable_matrix

IDENTITY_3 = np.eye(3)
DEMO_A = np.array([[2.0, 5.0, 1.0], [3.0, 4.0, 6.0], [1.0, 2.0, 3.0]])

UPPER_TRIANGULAR = np.array([[2.0, 3.0, 1.0], [0.0, 4.0, 2.0], [0.0, 0.0, 5.0]])

RREF_GOOD = np.array([[1.0, 0.0, 2.0], [0.0, 1.0, 3.0], [0.0, 0.0, 0.0]])
RREF_BAD = np.array([[2.0, 0.0, 3.0], [0.0, 1.0, 4.0], [0.0, 0.0, 0.0]])

_SYMBOL_STYLE = (
    "display:flex;align-items:center;justify-content:center;"
    "font-size:2em;color:#e6e6e6;height:116px;margin-top:32px"
)


def _symbol(sym: str) -> None:
    st.markdown(f'<div style="{_SYMBOL_STYLE}">{sym}</div>', unsafe_allow_html=True)


def _identity_section() -> None:
    st.markdown("### Identity matrix (I)")
    st.markdown(
        "1's on the diagonal, 0 everywhere else. It is the \"1\" of matrix "
        "multiplication: multiplying by I leaves a matrix or vector "
        "completely unchanged, since I . A = A and A . I = A for any A that "
        "fits."
    )
    cols = st.columns([1, 0.2, 1, 0.2, 1, 3])
    with cols[0]:
        editable_matrix("t00_special_I", label="I", editable=False,
                         value=IDENTITY_3, compact=True, rows=3, cols=3)
    with cols[1]:
        _symbol("&middot;")
    with cols[2]:
        editable_matrix("t00_special_IA_A", label="A", editable=False,
                         value=DEMO_A, compact=True, rows=3, cols=3)
    with cols[3]:
        _symbol("=")
    with cols[4]:
        editable_matrix("t00_special_IA_result", label="A", editable=False,
                         value=IDENTITY_3 @ DEMO_A, compact=True, rows=3, cols=3)
    st.divider()


def _upper_triangular_section() -> None:
    st.markdown("### Upper-triangular")
    st.markdown(
        "Every entry below the diagonal is 0. A system in this form solves "
        "instantly by back-substitution -- the last row already gives one "
        "unknown directly, and each row above plugs it in to find the next. "
        "This is exactly the shape elimination is aiming for in Topic 5.5."
    )
    cols = st.columns([1, 5])
    with cols[0]:
        editable_matrix("t00_special_upper", label="U", editable=False,
                         value=UPPER_TRIANGULAR, compact=True, rows=3, cols=3)
    st.divider()


def _rref_section() -> None:
    st.markdown("### Reduced row echelon form (RREF)")
    st.markdown(
        "The end state of full elimination: the leading (first nonzero) "
        "entry in every nonzero row is a 1, that 1 is the only nonzero "
        "entry in its column, and any all-zero rows sit at the bottom. Once "
        "a matrix is in RREF, solutions can be read straight off it -- and "
        "running [A | I] all the way to RREF is exactly how Topic 5.5 reads "
        "off A's inverse."
    )
    cols = st.columns([1, 5])
    with cols[0]:
        editable_matrix("t00_special_rref_good", label="RREF", editable=False,
                         value=RREF_GOOD, compact=True, rows=3, cols=3)
    st.markdown(
        "For contrast, the matrix below is NOT in RREF -- it has the same "
        "shape and the same zero pattern, but row 1's leading entry is 2, "
        "not 1:"
    )
    cols2 = st.columns([1, 5])
    with cols2[0]:
        editable_matrix("t00_special_rref_bad", label="Not RREF", editable=False,
                         value=RREF_BAD, compact=True, rows=3, cols=3)


def render_special():
    st.markdown(
        "A few matrix shapes come up often enough to name. No practice here "
        "-- just what each one is, why it matters, and what it looks like."
    )
    st.divider()

    _identity_section()
    _upper_triangular_section()
    _rref_section()
