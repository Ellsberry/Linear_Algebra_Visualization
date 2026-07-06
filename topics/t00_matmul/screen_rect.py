"""Topic 0, Screen 3 -- rectangular multiplication: shape rule, three verified
practice examples of different shapes, and one non-conformable pair."""
import numpy as np
import streamlit as st

from engine.widgets import editable_matrix, set_matrix_state

EXAMPLES = [
    # 2x3 . 3x2 = 2x2
    (np.array([[2.0, 3.0, 4.0], [5.0, 2.0, 3.0]]),
     np.array([[2.0, 4.0], [3.0, 2.0], [4.0, 3.0]]),
     np.array([[29.0, 26.0], [28.0, 33.0]])),
    # 5x3 . 3x2 = 5x2
    (np.array([[2.0, 3.0, 2.0], [4.0, 2.0, 3.0], [3.0, 3.0, 2.0],
               [2.0, 4.0, 3.0], [3.0, 2.0, 4.0]]),
     np.array([[3.0, 2.0], [2.0, 4.0], [4.0, 2.0]]),
     np.array([[20.0, 20.0], [28.0, 22.0], [23.0, 22.0], [26.0, 26.0], [29.0, 22.0]])),
    # 3x3 . 3x1 = 3x1
    (np.array([[2.0, 3.0, 4.0], [3.0, 2.0, 5.0], [4.0, 3.0, 2.0]]),
     np.array([[3.0], [2.0], [4.0]]),
     np.array([[28.0], [33.0], [26.0]])),
]

NONCONF_A = np.array([[1.0, 2.0], [3.0, 4.0]])
NONCONF_B = np.array([[1.0, 2.0, 3.0], [3.0, 1.0, 2.0], [2.0, 3.0, 1.0]])

_SYMBOL_STYLE = (
    "display:flex;align-items:center;justify-content:center;"
    "font-size:2em;color:#e6e6e6;height:116px;margin-top:32px"
)


def _symbol(sym: str) -> None:
    st.markdown(f'<div style="{_SYMBOL_STYLE}">{sym}</div>', unsafe_allow_html=True)


def _example_block(idx: int, A: np.ndarray, B: np.ndarray, AB: np.ndarray) -> None:
    m, n = A.shape
    n2, q = B.shape
    prefix = f"t00_rect_ex{idx + 1}"
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

    for i in range(m):
        for j in range(q):
            wkey = f"{ans_key}__{i}__{j}"
            if wkey not in st.session_state:
                st.session_state[wkey] = 0.0

    st.markdown(f"**Example {idx + 1}** -- {m}x{n} . {n2}x{q} = {m}x{q}")
    cols = st.columns([1.2, 0.2, 1.2, 0.2, 1.4, 3])
    with cols[0]:
        editable_matrix(f"{prefix}_A", label="A", editable=False, value=A,
                         compact=True, rows=m, cols=n)
    with cols[1]:
        _symbol("&middot;")
    with cols[2]:
        editable_matrix(f"{prefix}_B", label="B", editable=False, value=B,
                         compact=True, rows=n2, cols=q)
    with cols[3]:
        _symbol("=")
    with cols[4]:
        answer = editable_matrix(ans_key, label="Your answer", editable=True,
                                  compact=True, rows=m, cols=q)

    check_col, solve_col = st.columns(2)
    if check_col.button("Check", key=f"{prefix}_check"):
        wrong = [
            (i + 1, j + 1)
            for i in range(m)
            for j in range(q)
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


def _nonconformable_block() -> None:
    st.markdown("**Fourth example -- non-conformable**")
    cols = st.columns([1.2, 0.2, 1.2, 4])
    with cols[0]:
        editable_matrix("t00_rect_bad_A", label="A", editable=False,
                         value=NONCONF_A, compact=True, rows=2, cols=2)
    with cols[1]:
        _symbol("&middot;")
    with cols[2]:
        editable_matrix("t00_rect_bad_B", label="B", editable=False,
                         value=NONCONF_B, compact=True, rows=3, cols=3)

    st.error(
        "These can't be multiplied -- A has 2 columns but B has 3 rows; "
        "inner dimensions must match."
    )


def render_rect():
    st.markdown(
        "**The shape rule:** for A(m x n) . B(p x q), the inner dimensions "
        "must match -- n must equal p. Multiplying only works when A's "
        "column count equals B's row count; the result is m x q."
    )
    st.divider()

    for idx, (A, B, AB) in enumerate(EXAMPLES):
        _example_block(idx, A, B, AB)

    _nonconformable_block()
