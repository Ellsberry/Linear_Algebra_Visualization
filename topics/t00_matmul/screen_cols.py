"""Topic 0, Screen 6 -- column picture: columns of C are combinations of
columns of A."""
import numpy as np
import streamlit as st

from engine.widgets import editable_matrix, set_matrix_state

_WORKED_A = np.array([[2.0, 1.0, 3.0], [0.0, 2.0, 1.0]])
_WORKED_B = np.array([[1.0, 4.0], [2.0, 5.0], [3.0, 1.0]])
_WORKED_C = _WORKED_A @ _WORKED_B  # [[13, 16], [7, 11]]

_WORKED2_A = np.array([[2.0, 1.0, 3.0], [4.0, 2.0, 5.0]])
_WORKED2_B = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
_WORKED2_C = _WORKED2_A @ _WORKED2_B  # [[1, 2, 3], [2, 4, 5]]

_WORKED3_A = _WORKED2_A
_WORKED3_B = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
_WORKED3_C = _WORKED3_A @ _WORKED3_B  # [[2, 1, 6], [4, 2, 10]]

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


def _worked_combination(j: int) -> str:
    weights = _WORKED_B[:, j]
    terms = " + ".join(
        r"\textcolor{#4dabf7}{" + f"{w:.0f}" + r"}\,("
        + ", ".join(f"{v:.0f}" for v in _WORKED_A[:, k]) + r")"
        for k, w in enumerate(weights)
    )
    result = (
        r"\begin{bmatrix}"
        + r" \\ ".join(f"{v:.0f}" for v in _WORKED_C[:, j])
        + r"\end{bmatrix}"
    )
    return r"\text{Column " + str(j + 1) + r" of C} = " + terms + r" = " + result


def _worked_example() -> None:
    st.markdown(
        "**Column picture.** Now look at one column of C at a time. The "
        "**first column of C** is built entirely from the **columns of "
        "A** -- you take *1 of column 1, 2 of column 2, and 3 of column "
        "3* of A and add them up. Those weights (1, 2, 3) are exactly "
        "the **first column of B**. So each column of B is a recipe, "
        "and it mixes the columns of A to make the matching column of "
        "C. **Column j of C = (column j of B) used as weights on the "
        "columns of A.**"
    )
    st.caption(
        "A is m×n, B is n×p, so C = AB is m×p -- the shared "
        "inner dimension n is what gets summed over. Here A is 2×3, B "
        "is 3×2, so C is 2×2."
    )

    sel = st.radio("Building:", ["Column 1 of C", "Column 2 of C"],
                    horizontal=True, key="t00_cols_worked")
    j = 0 if sel == "Column 1 of C" else 1

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

    st.latex(_worked_combination(j))
    st.divider()


def _worked2_combination(j: int) -> str:
    weights = _WORKED2_B[:, j]
    terms = " + ".join(
        r"\textcolor{#4dabf7}{" + f"{w:.0f}" + r"}\,("
        + ", ".join(f"{v:.0f}" for v in _WORKED2_A[:, k]) + r")"
        for k, w in enumerate(weights)
    )
    result = (
        r"\begin{bmatrix}"
        + r" \\ ".join(f"{v:.0f}" for v in _WORKED2_C[:, j])
        + r"\end{bmatrix}"
    )
    return r"\text{Column " + str(j + 1) + r" of C} = " + terms + r" = " + result


def _worked_example2() -> None:
    st.markdown("**Worked Example 2 -- a column permutation.**")

    sel = st.radio("Building:", ["Column 1 of C", "Column 2 of C", "Column 3 of C"],
                    horizontal=True, key="t00_cols_worked2")
    j = ["Column 1 of C", "Column 2 of C", "Column 3 of C"].index(sel)

    m, n = _WORKED2_A.shape
    n2, p = _WORKED2_B.shape

    cols = st.columns([1, 1, 1, 3])
    with cols[0]:
        editable_matrix(None, label="A", editable=False, value=_WORKED2_A,
                         compact=True, rows=m, cols=n)
    with cols[1]:
        editable_matrix(None, label="B", editable=False, value=_WORKED2_B,
                         compact=True, rows=n2, cols=p)
    with cols[2]:
        editable_matrix(None, label="C", editable=False, value=_WORKED2_C,
                         compact=True, rows=m, cols=p)

    st.latex(_worked2_combination(j))
    st.caption(
        "This B is a permutation matrix -- each column of C picks exactly "
        "one column of A (weight 1), so multiplying reorders A's columns. "
        "Here columns 1 and 2 of A swap."
    )
    st.divider()


def _worked3_combination(j: int) -> str:
    weights = _WORKED3_B[:, j]
    terms = " + ".join(
        r"\textcolor{#4dabf7}{" + f"{w:.0f}" + r"}\,("
        + ", ".join(f"{v:.0f}" for v in _WORKED3_A[:, k]) + r")"
        for k, w in enumerate(weights)
    )
    result = (
        r"\begin{bmatrix}"
        + r" \\ ".join(f"{v:.0f}" for v in _WORKED3_C[:, j])
        + r"\end{bmatrix}"
    )
    return r"\text{Column " + str(j + 1) + r" of C} = " + terms + r" = " + result


def _worked_example3() -> None:
    st.markdown("**Worked Example 3 -- a diagonal scale.**")

    sel = st.radio("Building:", ["Column 1 of C", "Column 2 of C", "Column 3 of C"],
                    horizontal=True, key="t00_cols_worked3")
    j = ["Column 1 of C", "Column 2 of C", "Column 3 of C"].index(sel)

    m, n = _WORKED3_A.shape
    n2, p = _WORKED3_B.shape

    cols = st.columns([1, 1, 1, 3])
    with cols[0]:
        editable_matrix(None, label="A", editable=False, value=_WORKED3_A,
                         compact=True, rows=m, cols=n)
    with cols[1]:
        editable_matrix(None, label="B", editable=False, value=_WORKED3_B,
                         compact=True, rows=n2, cols=p)
    with cols[2]:
        editable_matrix(None, label="C", editable=False, value=_WORKED3_C,
                         compact=True, rows=m, cols=p)

    st.latex(_worked3_combination(j))
    st.caption(
        "This B is diagonal, so each column of C is just one column of A "
        "scaled: column 1 unchanged, column 2 unchanged, column 3 doubled "
        "(weight 2). A diagonal B scales each column independently."
    )
    st.divider()


def _answer_matrix_html(prefix: str, m: int, p: int) -> str:
    """Live read-only C display assembled from the student's per-column
    answer boxes. Column j renders blank until f"{prefix}_c{j}_touched" is
    True (set when that column's Check or Show solution is clicked); once
    touched, every cell in that column shows its current entered value,
    including a genuine 0."""
    if m == 1:
        lb, rb = ["["], ["]"]
    else:
        lb = ["⎡"] + ["⎢"] * (m - 2) + ["⎣"]
        rb = ["⎤"] + ["⎥"] * (m - 2) + ["⎦"]

    row_bstyle = (
        "display:flex;align-items:center;justify-content:center;"
        "font-size:2.4em;line-height:1;color:#e6e6e6;"
    )
    row_style = (
        "display:flex;align-items:center;gap:0.35em;"
        "font-size:1.05em;font-weight:500;color:#e6e6e6;min-height:40px"
    )

    rows_html = []
    for i in range(m):
        cells = []
        for j in range(p):
            touched = st.session_state.get(f"{prefix}_c{j}_touched", False)
            if not touched:
                text = ""
            else:
                fv = float(st.session_state.get(f"{prefix}_c{j}__{i}__0", 0.0))
                text = f"{fv:.0f}" if abs(fv - round(fv)) < 1e-9 else f"{fv:.2f}"
            cells.append(
                f'<span style="min-width:1.6em;text-align:right;">{text}</span>'
            )
        rows_html.append(
            f'<div style="display:flex;align-items:center;gap:0.3em;">'
            f'<div style="{row_bstyle}">{lb[i]}</div>'
            f'<div style="{row_style}">{"".join(cells)}</div>'
            f'<div style="{row_bstyle}">{rb[i]}</div>'
            f'</div>'
        )
    return "".join(rows_html)


def _practice_block(idx: int, A: np.ndarray, B: np.ndarray, C: np.ndarray,
                     aided: bool) -> None:
    m, n = A.shape
    p = C.shape[1]
    prefix = f"t00_cols_p{idx + 1}"

    st.markdown(f"**Practice {idx + 1}** -- {m}x{n} . {n}x{p} = {m}x{p}")

    # Show-solution write + default-seed pass for every column, done BEFORE
    # any widget this run (including the live C display below) reads
    # session_state -- same reveal-flag mechanism as before, just hoisted
    # above the top row so C reflects a just-revealed column immediately.
    #
    # Show solution must set the answer cells BEFORE the number_input
    # widgets below are instantiated this run -- writing to a widget's
    # session_state key after it has already been created in the same
    # run raises StreamlitAPIException. So the button only sets this
    # flag + reruns; the actual write happens here, at the top, on the
    # following run.
    for j in range(p):
        ans_key = f"{prefix}_c{j}"
        reveal_key = f"{ans_key}_reveal"
        touched_key = f"{ans_key}_touched"
        if st.session_state.get(reveal_key):
            set_matrix_state(ans_key, C[:, j:j + 1])
            st.session_state[reveal_key] = False
        for i in range(m):
            wkey = f"{ans_key}__{i}__0"
            if wkey not in st.session_state:
                st.session_state[wkey] = 0.0
        if touched_key not in st.session_state:
            st.session_state[touched_key] = False

    op_style = (
        "display:flex;align-items:center;justify-content:center;"
        "font-size:1.8em;line-height:1;color:#e6e6e6;min-height:58px"
    )

    top = st.columns([1, 0.3, 1, 0.3, 1.2])
    with top[0]:
        editable_matrix(f"{prefix}_A", label="A", editable=False, value=A,
                         compact=True, rows=m, cols=n)
    with top[1]:
        st.markdown("&nbsp;")
        st.markdown(f'<div style="{op_style}">·</div>', unsafe_allow_html=True)
    with top[2]:
        editable_matrix(f"{prefix}_B", label="B", editable=False, value=B,
                         compact=True, rows=n, cols=p)
    with top[3]:
        st.markdown("&nbsp;")
        st.markdown(f'<div style="{op_style}">=</div>', unsafe_allow_html=True)
    with top[4]:
        st.markdown("**C =**")
        st.markdown(_answer_matrix_html(prefix, m, p), unsafe_allow_html=True)

    cols_row = st.columns(p)
    for j in range(p):
        ans_key = f"{prefix}_c{j}"
        reveal_key = f"{ans_key}_reveal"
        touched_key = f"{ans_key}_touched"

        with cols_row[j]:
            if aided:
                weights = B[:, j]
                recipe = " + ".join(
                    f"{w:.0f}·({', '.join(f'{v:.0f}' for v in A[:, k])})"
                    for k, w in enumerate(weights)
                )
                st.markdown(f"Col {j + 1} = {recipe} = ___")

            answer = editable_matrix(ans_key, label=f"Col {j + 1}",
                                      editable=True, compact=True,
                                      rows=m, cols=1, hide_steppers=True)

            check_col, solve_col = st.columns(2)
            if check_col.button("Check", key=f"{ans_key}_check"):
                st.session_state[touched_key] = True
                wrong = [
                    i + 1 for i in range(m)
                    if abs(answer[i, 0] - C[i, j]) > 1e-6
                ]
                if not wrong:
                    st.success("Correct -- every entry matches.")
                else:
                    cells = ", ".join(f"row {i}" for i in wrong)
                    st.warning(f"Not quite -- check: {cells}")

            if solve_col.button("Show solution", key=f"{ans_key}_solve"):
                st.session_state[reveal_key] = True
                st.session_state[touched_key] = True
                st.rerun()

    st.divider()


def render_cols():
    _worked_example()
    _worked_example2()
    _worked_example3()

    st.markdown("### Practice -- build the whole of C, one column at a time")
    for idx, (A, B, C, aided) in enumerate(PRACTICE):
        _practice_block(idx, A, B, C, aided)
