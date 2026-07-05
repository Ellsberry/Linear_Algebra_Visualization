"""Topic 0, Screen 1 -- the row-times-column rule, four 2x2 practice examples."""
import numpy as np
import streamlit as st

from engine.widgets import editable_matrix, set_matrix_state

EXAMPLES = [
    (np.array([[1.0, 2.0], [0.0, 1.0]]),
     np.array([[2.0, 0.0], [1.0, 3.0]]),
     np.array([[4.0, 6.0], [1.0, 3.0]])),
    (np.array([[2.0, 1.0], [1.0, 2.0]]),
     np.array([[1.0, 0.0], [2.0, 1.0]]),
     np.array([[4.0, 1.0], [5.0, 2.0]])),
    (np.array([[0.0, 1.0], [1.0, 0.0]]),
     np.array([[3.0, 2.0], [1.0, 4.0]]),
     np.array([[1.0, 4.0], [3.0, 2.0]])),
    (np.array([[2.0, 0.0], [0.0, 3.0]]),
     np.array([[1.0, 2.0], [2.0, 1.0]]),
     np.array([[2.0, 4.0], [6.0, 3.0]])),
]


def render_2x2():
    st.markdown(
        "**The rule:** entry (i, j) of the product A·B comes from row i of A "
        "dotted with column j of B -- multiply the matching pairs, then add "
        "them up."
    )
    st.caption("Shape rule: 2×2 · 2×2 → 2×2 (inner dimensions match: 2 and 2).")

    labels = [f"Example {i + 1}" for i in range(len(EXAMPLES))]
    choice = st.radio("Pick an example", labels, horizontal=True, key="t00_2x2_choice")
    idx = labels.index(choice)
    A, B, AB = EXAMPLES[idx]
    prefix = f"t00_2x2_ex{idx + 1}"
    ans_key = f"{prefix}_ans"

    for i in range(2):
        for j in range(2):
            wkey = f"{ans_key}__{i}__{j}"
            if wkey not in st.session_state:
                st.session_state[wkey] = 0.0

    st.divider()

    cols = st.columns(3)
    with cols[0]:
        editable_matrix(f"{prefix}_A", 2, label="A", editable=False, value=A)
    with cols[1]:
        editable_matrix(f"{prefix}_B", 2, label="B", editable=False, value=B)
    with cols[2]:
        answer = editable_matrix(ans_key, 2, label="A · B (your answer)", editable=True)

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
