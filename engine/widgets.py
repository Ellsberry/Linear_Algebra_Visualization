"""
Shared input widgets used by every topic.

These are the reusable building blocks of the "left panel". A topic module
calls these to render editable inputs; the engine handles Streamlit state so
presets and Reset work consistently everywhere.
"""
import numpy as np
import streamlit as st


def editable_matrix(state_key: str, dim: int, label: str = "A",
                    editable: bool = True, value=None) -> np.ndarray:
    """Render a matrix in bracket form with editable or read-only cells.

    editable=True  → number_input cells using session_state keys {state_key}__i__j
                     (same keys as matrix_editor, so presets/Reset keep working).
    editable=False → static text displaying the provided `value` array.
    Returns the matrix as a numpy array.
    """
    st.markdown(f"**{label} =**")

    if dim == 1:
        lb, rb = ["["], ["]"]
    else:
        lb = ["⎡"] + ["⎢"] * (dim - 2) + ["⎣"]
        rb = ["⎤"] + ["⎥"] * (dim - 2) + ["⎦"]

    bstyle = (
        "display:flex;align-items:center;justify-content:center;"
        "font-size:2.4em;line-height:1;color:#e6e6e6;min-height:58px"
    )
    vstyle = (
        "display:flex;align-items:center;justify-content:center;"
        "font-size:1.05em;font-weight:500;color:#e6e6e6;min-height:58px"
    )

    M = np.zeros((dim, dim))
    for i in range(dim):
        cols = st.columns([0.07] + [1] * dim + [0.07])
        cols[0].markdown(
            f'<div style="{bstyle}">{lb[i]}</div>', unsafe_allow_html=True,
        )
        for j in range(dim):
            if editable:
                wkey = f"{state_key}__{i}__{j}"
                if wkey not in st.session_state:
                    st.session_state[wkey] = 1.0 if i == j else 0.0
                M[i, j] = cols[j + 1].number_input(
                    label=wkey, key=wkey, step=0.1, format="%.2f",
                    label_visibility="collapsed",
                )
            else:
                v = float(value[i, j]) if value is not None else 0.0
                M[i, j] = v
                cols[j + 1].markdown(
                    f'<div style="{vstyle}">{v:.2f}</div>',
                    unsafe_allow_html=True,
                )
        cols[dim + 1].markdown(
            f'<div style="{bstyle}">{rb[i]}</div>', unsafe_allow_html=True,
        )
    return M


def matrix_editor(state_key: str, dim: int, label: str = "Matrix M") -> np.ndarray:
    """Render a dim x dim grid of number inputs and return the matrix.

    Cell values live in st.session_state under keys "{state_key}__i__j" so that
    presets and Reset (which write those keys) take effect automatically.
    """
    st.markdown(f"**{label}**")
    M = np.zeros((dim, dim))
    for i in range(dim):
        cols = st.columns(dim)
        for j in range(dim):
            wkey = f"{state_key}__{i}__{j}"
            if wkey not in st.session_state:
                st.session_state[wkey] = 1.0 if i == j else 0.0
            M[i, j] = cols[j].number_input(
                label=wkey,
                key=wkey,
                step=0.1,
                format="%.2f",
                label_visibility="collapsed",
            )
    return M


def vector_editor(state_key: str, dim: int, default, label: str = "Vector v") -> np.ndarray:
    """Render dim number inputs in a row and return the vector."""
    st.markdown(f"**{label}**")
    v = np.zeros(dim)
    cols = st.columns(dim)
    for i in range(dim):
        wkey = f"{state_key}__{i}"
        if wkey not in st.session_state:
            st.session_state[wkey] = float(default[i])
        v[i] = cols[i].number_input(
            label=wkey,
            key=wkey,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
        )
    return v


def scalar_slider(state_key: str, label: str, lo: float, hi: float,
                  default: float, step: float = 0.01) -> float:
    """Render a single labelled slider."""
    if state_key not in st.session_state:
        st.session_state[state_key] = default
    return st.slider(label, min_value=lo, max_value=hi, step=step, key=state_key)


def set_matrix_state(state_key: str, M: np.ndarray) -> None:
    """Write a matrix into session_state so the editor picks it up (used by presets/Reset)."""
    n = M.shape[0]
    for i in range(n):
        for j in range(n):
            st.session_state[f"{state_key}__{i}__{j}"] = float(M[i, j])


def bmatrix(M: np.ndarray) -> str:
    """Format a numpy matrix (or column vector) as a LaTeX bmatrix string."""
    M = np.atleast_2d(M)
    rows = r" \\ ".join(" & ".join(f"{val:.2f}" for val in row) for row in M)
    return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"


def set_vector_state(state_key: str, v) -> None:
    """Write a vector into session_state so vector_editor picks it up (presets/Reset)."""
    for i in range(len(v)):
        st.session_state[f"{state_key}__{i}"] = float(v[i])


def aug_array_latex(M, n_unknowns: int) -> str:
    """LaTeX string for an augmented matrix [A | b].

    M is a list of rows, each with n_unknowns + 1 floats (last entry is b).
    Produces \\left[\\begin{array}{cc...|c} ... \\end{array}\\right].
    """
    col_spec = "c" * n_unknowns + "|c"

    def _fmt(v: float) -> str:
        v = float(v)
        if abs(v) < 1e-10:
            return "0"
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.4g}"

    rows = r" \\ ".join(
        " & ".join(_fmt(M[i][j]) for j in range(n_unknowns + 1))
        for i in range(len(M))
    )
    return r"\left[\begin{array}{" + col_spec + r"}" + rows + r"\end{array}\right]"
