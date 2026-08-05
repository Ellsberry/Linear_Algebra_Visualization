import streamlit as st

from .workbench import workbench, _make_aug, _load_aug


# ---------------------------------------------------------------------------
# Screen 3 -- Infinite and No Solutions
# ---------------------------------------------------------------------------

_PRESETS = {
    "No solution (0 = 3)": {
        "A": [[1, 1, 1], [2, 2, 2], [1, 2, 3]],
        "b": [6, 15, 14],
    },
    "Infinitely many (0 = 0)": {
        "A": [[1, 1, 1], [2, 2, 2], [1, 2, 3]],
        "b": [6, 12, 14],
    },
}

_INTRO = """
**Infinite and no solutions.** Not every system has a single answer. Some have
none, and some have infinitely many -- and elimination shows you which, by what
happens to the bottom row. These two systems look almost the same: the second
equation is just twice the first, and only one number on the right-hand side is
different. Run each one and watch that one number decide everything.
"""

_NOTICE = """
Eliminate row 2 against row 1 in both systems and its coefficients vanish -- you're
left with 0 = something. If that something is not zero (here 0 = 3), the equation is
impossible and the system has **no solution**. If it's 0 = 0, the equation was
always true -- it added nothing, so one unknown is free and there are **infinitely
many solutions**. Same coefficients, one different number, opposite outcomes.
"""

_CLOSING = """
"No solution" and "infinitely many" are exactly the cases where a matrix has no
inverse (det = 0, from Topic 4) -- the system can't be pinned to a single answer.
Which one you get depends on the right-hand side.
"""


def render_infinite_nosolution():
    st.markdown(_INTRO)
    st.info(_NOTICE)

    preset = st.selectbox("Preset", list(_PRESETS), key="t05b_infns_preset")
    p = _PRESETS[preset]
    if st.session_state.get("t05b_infns_last") != preset:
        aug = _make_aug(p["A"], p["b"])
        _load_aug("t05b_infns", aug)
        st.session_state["t05b_infns_last"] = preset

    workbench("t05b_infns", 3)

    st.markdown(_CLOSING)
