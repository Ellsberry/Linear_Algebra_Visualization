"""Topic 0, Screen 7 -- outer products: AB is a sum of (col of A)(row of B)
pieces, one piece per shared-dimension index."""
import numpy as np
import streamlit as st

from engine.widgets import editable_matrix, set_matrix_state

_WORKED_A = np.array([[2.0, 1.0, 3.0], [0.0, 2.0, 1.0]])
_WORKED_B = np.array([[1.0, 4.0], [2.0, 5.0], [3.0, 1.0]])
_WORKED_C = _WORKED_A @ _WORKED_B  # [[13, 16], [7, 11]]

PRACTICE = [
    # (A, B, C, aided)
    (np.array([[2.0, 1.0], [1.0, 3.0]]),
     np.array([[1.0, 2.0], [4.0, 1.0]]),
     np.array([[6.0, 5.0], [13.0, 5.0]]),
     True),
    (np.array([[1.0, 0.0, 2.0], [3.0, 1.0, 1.0]]),
     np.array([[2.0, 1.0], [1.0, 4.0], [0.0, 2.0]]),
     np.array([[2.0, 5.0], [7.0, 9.0]]),
     False),
    (np.array([[1.0, 2.0], [0.0, 3.0], [2.0, 1.0]]),
     np.array([[3.0, 1.0, 2.0], [1.0, 0.0, 4.0]]),
     np.array([[5.0, 1.0, 10.0], [3.0, 0.0, 12.0], [7.0, 2.0, 8.0]]),
     False),
]


def _matrix_latex(M) -> str:
    rows = r" \\ ".join(" & ".join(f"{v:.0f}" for v in row) for row in M)
    return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"


def _term_latex(k: int) -> str:
    col = _WORKED_A[:, k]
    row = _WORKED_B[k, :]
    term = np.outer(col, row)
    col_latex = r"\textcolor{#4dabf7}{" + _matrix_latex(col.reshape(-1, 1)) + r"}"
    row_latex = r"\textcolor{#4dabf7}{" + _matrix_latex(row.reshape(1, -1)) + r"}"
    return (
        r"\text{Term " + str(k + 1) + r"} = " + col_latex + row_latex
        + r" = " + _matrix_latex(term)
    )


def _sum_latex() -> str:
    n = _WORKED_A.shape[1]
    terms = [np.outer(_WORKED_A[:, k], _WORKED_B[k, :]) for k in range(n)]
    total = sum(terms)
    assert np.allclose(total, _WORKED_C)
    parts = " + ".join(_matrix_latex(t) for t in terms)
    return parts + r" = " + _matrix_latex(total) + r" = C"


def _worked_combination(sel: str) -> str:
    if sel == "Sum = C":
        return _sum_latex()
    k = {"Term 1": 0, "Term 2": 1, "Term 3": 2}[sel]
    return _term_latex(k)


def _worked_example() -> None:
    st.markdown(
        "**The whole thing at once.** The row picture and the column "
        "picture are two halves of one idea. Take **column 1 of A** and "
        "**row 1 of B** and multiply them -- a column times a row gives "
        "a full 2×2 matrix (an \"outer product\"). Do the same for "
        "column 2 of A with row 2 of B, and column 3 with row 3. **Add "
        "those three matrices and you get C.** So AB is a *sum of "
        "simple pieces*, one piece per column of A paired with the "
        "matching row of B. This is the view that powers the big ideas "
        "later -- it's how PCA and SVD break a matrix into a stack of "
        "simple layers."
    )
    st.caption(
        "A is m×n, B is n×p, so C = AB is m×p -- the shared "
        "inner dimension n is what gets summed over. Here A is 2×3, B "
        "is 3×2, so C is 2×2."
    )
    st.caption(
        "The number of terms equals the shared dimension n -- one "
        "term per column of A paired with the matching row of B."
    )

    sel = st.radio("Building:", ["Term 1", "Term 2", "Term 3", "Sum = C"],
                    horizontal=True, key="t00_outer_worked")

    m, n = _WORKED_A.shape
    n2, p = _WORKED_B.shape

    cols = st.columns([1, 1, 1, 3])
    with cols[0]:
        editable_matrix(None, label="A", editable=False, value=_WORKED_A,
                         compact=True, rows=m, cols=n)
    with cols[1]:
        editable_matrix(None, label="B", editable=False, value=_WORKED_B,
                         compact=True, rows=n2, cols=p)
    with cols[2]:
        editable_matrix(None, label="C", editable=False, value=_WORKED_C,
                         compact=True, rows=m, cols=p)

    st.latex(_worked_combination(sel))
    st.divider()


def _term_check_and_solve(ans_key: str, target: np.ndarray, m: int, p: int,
                          answer: np.ndarray) -> None:
    check_col, solve_col = st.columns(2)
    if check_col.button("Check", key=f"{ans_key}_check"):
        wrong = [
            (i + 1, j + 1)
            for i in range(m)
            for j in range(p)
            if abs(answer[i, j] - target[i, j]) > 1e-6
        ]
        if not wrong:
            st.success("Correct -- every entry matches.")
        else:
            cells = ", ".join(f"(row {i}, col {j})" for i, j in wrong)
            st.warning(f"Not quite -- check: {cells}")

    if solve_col.button("Show solution", key=f"{ans_key}_solve"):
        st.session_state[f"{ans_key}_reveal"] = True
        st.rerun()


def _practice_block(idx: int, A: np.ndarray, B: np.ndarray, C: np.ndarray,
                     aided: bool) -> None:
    m, n = A.shape
    p = C.shape[1]
    prefix = f"t00_outer_p{idx + 1}"

    st.markdown(f"**Practice {idx + 1}** -- {m}x{n} . {n}x{p} = {m}x{p} ({n} terms)")
    top = st.columns([1, 1, 3])
    with top[0]:
        editable_matrix(f"{prefix}_A", label="A", editable=False, value=A,
                         compact=True, rows=m, cols=n)
    with top[1]:
        editable_matrix(f"{prefix}_B", label="B", editable=False, value=B,
                         compact=True, rows=n, cols=p)

    terms = [np.outer(A[:, k], B[k, :]) for k in range(n)]

    for k in range(n):
        term = terms[k]
        ans_key = f"{prefix}_t{k}"
        reveal_key = f"{ans_key}_reveal"

        # Show solution must set the answer cells BEFORE the number_input
        # widgets below are instantiated this run -- writing to a widget's
        # session_state key after it has already been created in the same
        # run raises StreamlitAPIException. So the button only sets this
        # flag + reruns; the actual write happens here, at the top, on the
        # following run.
        if st.session_state.get(reveal_key):
            set_matrix_state(ans_key, term)
            st.session_state[reveal_key] = False

        for i in range(m):
            for j in range(p):
                wkey = f"{ans_key}__{i}__{j}"
                if wkey not in st.session_state:
                    st.session_state[wkey] = 0.0

        if aided:
            col_str = ", ".join(f"{v:.0f}" for v in A[:, k])
            row_str = ", ".join(f"{v:.0f}" for v in B[k, :])
            rc, ac = st.columns([2, 1])
            with rc:
                st.markdown(f"Term {k + 1} = ({col_str})ᵀ · ({row_str}) = ___")
            with ac:
                answer = editable_matrix(ans_key, label=f"Term {k + 1}",
                                          editable=True, compact=True,
                                          rows=m, cols=p, hide_steppers=True)
        else:
            answer = editable_matrix(ans_key, label=f"Term {k + 1}",
                                      editable=True, compact=True,
                                      rows=m, cols=p, hide_steppers=True)

        _term_check_and_solve(ans_key, term, m, p, answer)
        st.divider()

    sum_key = f"{prefix}_sum"
    sum_reveal_key = f"{sum_key}_reveal"

    if st.session_state.get(sum_reveal_key):
        set_matrix_state(sum_key, C)
        st.session_state[sum_reveal_key] = False

    for i in range(m):
        for j in range(p):
            wkey = f"{sum_key}__{i}__{j}"
            if wkey not in st.session_state:
                st.session_state[wkey] = 0.0

    if aided:
        term_labels = " + ".join(f"Term {k + 1}" for k in range(n))
        rc, ac = st.columns([2, 1])
        with rc:
            st.markdown(f"Sum = {term_labels} = ___")
        with ac:
            sum_answer = editable_matrix(sum_key, label="Sum", editable=True,
                                          compact=True, rows=m, cols=p,
                                          hide_steppers=True)
    else:
        sum_answer = editable_matrix(sum_key, label="Sum", editable=True,
                                      compact=True, rows=m, cols=p,
                                      hide_steppers=True)

    _term_check_and_solve(sum_key, C, m, p, sum_answer)
    st.divider()


def render_outer():
    _worked_example()

    st.markdown("### Practice -- build each term, then the sum")
    for idx, (A, B, C, aided) in enumerate(PRACTICE):
        _practice_block(idx, A, B, C, aided)
