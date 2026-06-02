"""
Shared input widgets used by every topic.

These are the reusable building blocks of the "left panel". A topic module
calls these to render editable inputs; the engine handles Streamlit state so
presets and Reset work consistently everywhere.
"""
import numpy as np
import streamlit as st


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
