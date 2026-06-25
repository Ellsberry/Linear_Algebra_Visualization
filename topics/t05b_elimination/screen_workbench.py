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
    "Redundant equation (infinite)": {
        "A": [[1, 1, 1], [1, 2, 3], [2, 3, 4]],
        "b": [6, 14, 20],
        "notice": "Row 3 = Row 1 + Row 2, so it vanishes during elimination — "
                  "a free variable appears and there are infinitely many solutions.",
    },
    "Contradiction (no solution)": {
        "A": [[1, 1, 1], [1, 2, 3], [2, 3, 4]],
        "b": [6, 14, 21],
        "notice": "Same coefficient equations as *Redundant*, but the last constant "
                  "differs — elimination produces a row \"0 = 1\", which is impossible.",
    },
}

_E1_NOTICE = """
Try the standard method with **Do one step**, then experiment in manual mode —
you can't break it, because every move keeps the same solution. The four presets
show the four things that can happen: a clean triangle (one solution), a forced
swap when a pivot is zero, a row that vanishes (infinitely many), and a row that
becomes "0 = something" (no solution).
"""


def _example_one():
    st.markdown(
        "**The workbench.** A 3×3 system — small enough to relate to planes "
        "and still big enough to show every scenario. Use it to learn the moves, "
        "then explore each of the four preset outcomes."
    )
    st.info(_E1_NOTICE)

    preset = st.selectbox("Preset", list(_E1_PRESETS), key="t05b_e1_preset")
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

    with st.expander("Show the math"):
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
