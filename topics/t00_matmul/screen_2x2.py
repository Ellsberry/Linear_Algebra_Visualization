"""Topic 0, Screen 1 -- the row-times-column rule, four 2x2 practice examples."""
import numpy as np
import streamlit as st

from engine.widgets import editable_matrix, set_matrix_state

EXAMPLES = [
    (np.array([[6.0, 4.0], [7.0, 5.0]]),
     np.array([[3.0, 8.0], [9.0, 2.0]]),
     np.array([[54.0, 56.0], [66.0, 66.0]])),
    (np.array([[8.0, 0.0], [5.0, 7.0]]),
     np.array([[6.0, 3.0], [4.0, 9.0]]),
     np.array([[48.0, 24.0], [58.0, 78.0]])),
    (np.array([[7.0, 3.0], [9.0, 0.0]]),
     np.array([[5.0, 6.0], [8.0, 4.0]]),
     np.array([[59.0, 54.0], [45.0, 54.0]])),
    (np.array([[4.0, 7.0], [6.0, 5.0]]),
     np.array([[9.0, 3.0], [2.0, 8.0]]),
     np.array([[50.0, 68.0], [64.0, 58.0]])),
]

_SYMBOL_STYLE = (
    "display:flex;align-items:center;justify-content:center;"
    "font-size:2em;color:#e6e6e6;height:116px;margin-top:32px"
)


def _symbol(sym: str) -> None:
    st.markdown(f'<div style="{_SYMBOL_STYLE}">{sym}</div>', unsafe_allow_html=True)


def _example_block(idx: int, A: np.ndarray, B: np.ndarray, AB: np.ndarray) -> None:
    prefix = f"t00_2x2_ex{idx + 1}"
    ans_key = f"{prefix}_ans"

    for i in range(2):
        for j in range(2):
            wkey = f"{ans_key}__{i}__{j}"
            if wkey not in st.session_state:
                st.session_state[wkey] = 0.0

    st.markdown(f"**Example {idx + 1}**")
    cols = st.columns([1.2, 0.2, 1.2, 0.2, 1.4, 3])
    with cols[0]:
        editable_matrix(f"{prefix}_A", 2, label="A", editable=False, value=A, compact=True)
    with cols[1]:
        _symbol("&middot;")
    with cols[2]:
        editable_matrix(f"{prefix}_B", 2, label="B", editable=False, value=B, compact=True)
    with cols[3]:
        _symbol("=")
    with cols[4]:
        answer = editable_matrix(ans_key, 2, label="Your answer", editable=True, compact=True)

    check_col, solve_col = st.columns(2)
    if check_col.button("Check", key=f"{prefix}_check"):
        wrong = [
            (i + 1, j + 1)
            for i in range(2)
            for j in range(2)
            if abs(answer[i, j] - AB[i, j]) > 1e-6
        ]
        if not wrong:
            st.success("Correct -- every entry matches.")
        else:
            cells = ", ".join(f"(row {i}, col {j})" for i, j in wrong)
            st.warning(f"Not quite -- check: {cells}")

    if solve_col.button("Show solution", key=f"{prefix}_solve"):
        set_matrix_state(ans_key, AB)
        st.rerun()

    st.divider()


def render_2x2():
    st.markdown(
        "**The rule:** entry (i, j) of the product A·B comes from row i of A "
        "dotted with column j of B -- multiply the matching pairs, then add "
        "them up."
    )
    st.caption("Shape rule: 2×2 · 2×2 → 2×2 (inner dimensions match: 2 and 2).")
    st.divider()

    top_left, top_right = st.columns(2)
    with top_left:
        _example_block(0, *EXAMPLES[0])
    with top_right:
        _example_block(1, *EXAMPLES[1])

    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        _example_block(2, *EXAMPLES[2])
    with bottom_right:
        _example_block(3, *EXAMPLES[3])
