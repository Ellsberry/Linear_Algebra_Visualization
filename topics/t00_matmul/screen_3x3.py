"""Topic 0, Screen 2 -- the row-times-column rule, four 3x3 practice examples."""
import numpy as np
import streamlit as st

from engine.widgets import editable_matrix, set_matrix_state

EXAMPLES = [
    (np.array([[2.0, 3.0, 2.0], [4.0, 2.0, 3.0], [3.0, 4.0, 2.0]]),
     np.array([[3.0, 2.0, 4.0], [2.0, 5.0, 3.0], [4.0, 3.0, 2.0]]),
     np.array([[20.0, 25.0, 21.0], [28.0, 27.0, 28.0], [25.0, 32.0, 28.0]])),
    (np.array([[4.0, 2.0, 0.0], [3.0, 5.0, 2.0], [2.0, 3.0, 4.0]]),
     np.array([[2.0, 4.0, 3.0], [5.0, 2.0, 4.0], [3.0, 3.0, 2.0]]),
     np.array([[18.0, 20.0, 20.0], [37.0, 28.0, 33.0], [31.0, 26.0, 26.0]])),
    (np.array([[5.0, 3.0, 2.0], [2.0, 4.0, 6.0], [4.0, 2.0, 0.0]]),
     np.array([[3.0, 2.0, 5.0], [4.0, 3.0, 2.0], [2.0, 4.0, 3.0]]),
     np.array([[31.0, 27.0, 37.0], [34.0, 40.0, 36.0], [20.0, 14.0, 24.0]])),
    (np.array([[3.0, 4.0, 2.0], [5.0, 2.0, 3.0], [2.0, 3.0, 5.0]]),
     np.array([[2.0, 3.0, 4.0], [4.0, 2.0, 3.0], [3.0, 5.0, 2.0]]),
     np.array([[28.0, 27.0, 28.0], [27.0, 34.0, 32.0], [31.0, 37.0, 27.0]])),
]

_SYMBOL_STYLE = (
    "display:flex;align-items:center;justify-content:center;"
    "font-size:2em;color:#e6e6e6;height:116px;margin-top:32px"
)


def _symbol(sym: str) -> None:
    st.markdown(f'<div style="{_SYMBOL_STYLE}">{sym}</div>', unsafe_allow_html=True)


def _example_block(idx: int, A: np.ndarray, B: np.ndarray, AB: np.ndarray) -> None:
    prefix = f"t00_3x3_ex{idx + 1}"
    ans_key = f"{prefix}_ans"
    reveal_key = f"{ans_key}_reveal"

    # Show solution must set the answer cells BEFORE the number_input widgets
    # below are instantiated this run -- writing to a widget's session_state
    # key after it has already been created in the same run raises
    # StreamlitAPIException. So the button only sets this flag + reruns; the
    # actual write happens here, at the top, on the following run.
    if st.session_state.get(reveal_key):
        set_matrix_state(ans_key, AB)
        st.session_state[reveal_key] = False

    for i in range(3):
        for j in range(3):
            wkey = f"{ans_key}__{i}__{j}"
            if wkey not in st.session_state:
                st.session_state[wkey] = 0.0

    st.markdown(f"**Example {idx + 1}**")
    cols = st.columns([1.2, 0.2, 1.2, 0.2, 1.4, 3])
    with cols[0]:
        editable_matrix(f"{prefix}_A", 3, label="A", editable=False, value=A, compact=True)
    with cols[1]:
        _symbol("&middot;")
    with cols[2]:
        editable_matrix(f"{prefix}_B", 3, label="B", editable=False, value=B, compact=True)
    with cols[3]:
        _symbol("=")
    with cols[4]:
        answer = editable_matrix(ans_key, 3, label="Your answer", editable=True, compact=True)

    check_col, solve_col = st.columns(2)
    if check_col.button("Check", key=f"{prefix}_check"):
        wrong = [
            (i + 1, j + 1)
            for i in range(3)
            for j in range(3)
            if abs(answer[i, j] - AB[i, j]) > 1e-6
        ]
        if not wrong:
            st.success("Correct -- every entry matches.")
        else:
            cells = ", ".join(f"(row {i}, col {j})" for i, j in wrong)
            st.warning(f"Not quite -- check: {cells}")

    if solve_col.button("Show solution", key=f"{prefix}_solve"):
        st.session_state[reveal_key] = True
        st.rerun()

    st.divider()


def render_3x3():
    st.markdown(
        "**The rule:** entry (i, j) of the product A·B comes from row i of A "
        "dotted with column j of B -- multiply the matching pairs, then add "
        "them up. Same rule as 2×2, just one more pair to multiply and add per entry."
    )
    st.caption("Shape rule: 3×3 · 3×3 → 3×3 (inner dimensions match: 3 and 3).")
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
