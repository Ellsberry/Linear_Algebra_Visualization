import streamlit as st

from .workbench import workbench, _make_aug


# ---------------------------------------------------------------------------
# Screen 1 — The workbench
# ---------------------------------------------------------------------------

_E1_PRESETS = {
    "One solution": {
        "A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
        "b": [8, -11, -3],
        "notice": "A clean 3×3 — three nonzero pivots appear after elimination. "
                  "Back-substitute to reach x = (2, 3, −1).",
    },
    "Needs a row swap": {
        "A": [[0, 2, 1], [1, 1, 1], [2, 1, 3]],
        "b": [5, 6, 11],
        "notice": "The top-left entry is 0 — **Do one step** immediately triggers a swap. "
                  "After that, elimination proceeds normally to x = (3, 2, 1).",
    },
}


def _example_one():
    st.markdown(
        "This screen works with 3 variables and 3 unknowns. Using the elimination method, you "
        "will start with an AUGMENTED matrix that contains the coefficients of the functions in "
        "a system of equations and tack on or augment the answers to the functions. You will "
        "then use the 3 allowable operations: swap rows, scale a row, add a multiple of one row "
        "to transform the matrix into its upper triangular form. You then can use back "
        "substitution to obtain the values of x.\n\n"
        "The upper triangle form has non-zero values on the long diagonal and zeros below the "
        "diagonal. The values on the diagonal are called \"PIVOTS\". To get to a completed "
        "upper triangular form in this exercise, no pivot can be zero. If a zero appears in the "
        "pivot position, use the swap row operation."
    )

    preset = st.radio(
        "Preset",
        ["One solution", "Needs a row swap"],
        horizontal=True,
        key="t05b_e1_preset",
    )
    p = _E1_PRESETS[preset]
    if st.session_state.get("t05b_e1_last") != preset:
        aug = _make_aug(p["A"], p["b"])
        st.session_state["t05b_e1_M"] = aug
        st.session_state["t05b_e1_orig"] = [row[:] for row in aug]
        st.session_state["t05b_e1_log"] = []
        st.session_state["t05b_e1_history"] = []
        st.session_state.pop("t05b_e1_solution", None)
        st.session_state["t05b_e1_last"] = preset
    st.caption(p["notice"])

    workbench("t05b_e1", 3)

    st.markdown(
        "The three legal moves — add a multiple, swap, scale — are the "
        "**elementary row operations**. Each can be undone, so they never "
        "change the solution set.\n\n"
        "Once the matrix is upper triangular, its determinant equals the "
        "**product of the diagonal pivots**. If any pivot is zero, the "
        "determinant is zero — exactly the *singular* / \"no unique solution\" "
        "case from Topic 3. The number of nonzero pivots is the *rank* of A, "
        "a preview of Topic 6."
    )
