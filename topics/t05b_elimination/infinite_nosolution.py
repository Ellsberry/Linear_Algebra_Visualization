import streamlit as st

from .workbench import workbench, _make_aug, _load_aug, _is_upper_triangular
from engine.parametric import (
    solve_parametric,
    parametric_latex,
    solution_equations_block,
)


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
**Infinite and no solutions.** Not every system has a single answer. Some have none,
and some have infinitely many. Elimination to triangular form shows you which, by what
happens to the bottom row.

Each equation is a rule the answer has to obey. When the rules all point to one spot,
you get a single solution. But rules can overlap or clash. If two rules secretly say
the exact same thing, one of them is wasted -- it pins nothing down, and you're left
with extra freedom (infinitely many answers). If two rules flatly contradict each
other, nothing can satisfy them both (no answer at all). This works the same whether
you have 2 unknowns, 3, or 20.

The two systems below are built to show this. Their coefficients are identical -- the
second equation is just twice the first -- and only one number on the right-hand side
is different. Run each one and watch that single number flip the answer.
"""

_NOTICE = """
Here's the tell. Look at the two equations before you start: the second is just the
first multiplied by 2 -- every coefficient is doubled. They're not two different rules,
they're the same rule written twice. So when you eliminate row 2 against row 1,
everything in it cancels and you're left with a bottom row reading **0 = something**.

- If that something is **not zero** (here 0 = 3), it's impossible -- zero can't equal
  three -- so the system has **no solution**.
- If it's **0 = 0**, the equation is always true. It added nothing, so one unknown is
  free to be anything, giving **infinitely many solutions**.

Same coefficients, one different number, opposite outcomes.
"""

_CLOSING = """
"No solution" and "infinitely many" are exactly the cases where a matrix has no
inverse (det = 0, from Topic 4) -- the system can't be pinned to a single answer.
Which one you get depends on the right-hand side.
"""


def render_infinite_nosolution():
    st.markdown(_INTRO)
    st.info(_NOTICE)

    preset = st.radio("Preset", list(_PRESETS), key="t05b_infns_preset", horizontal=True)
    p = _PRESETS[preset]
    if st.session_state.get("t05b_infns_last") != preset:
        aug = _make_aug(p["A"], p["b"])
        _load_aug("t05b_infns", aug)
        st.session_state["t05b_infns_last"] = preset

    def _render_solution():
        M = st.session_state.get("t05b_infns_M")
        if M is not None and _is_upper_triangular(M, 3):
            try:
                res = solve_parametric(M, 3, "x")
                st.markdown("**General solution:**")
                if res["status"] == "no_solution":
                    st.latex(parametric_latex(res, "x"))
                    st.caption(
                        "The bottom row became 0 = a nonzero number, so no values "
                        "of x satisfy all three equations."
                    )
                elif res["status"] == "unique":
                    st.latex(solution_equations_block(res, "x"))
                    st.latex(parametric_latex(res, "x"))
                    st.caption("Elimination pinned down every unknown -- exactly one solution.")
                else:  # infinite
                    st.markdown("Read each variable off the reduced rows:")
                    st.latex(solution_equations_block(res, "x"))
                    st.markdown("Written as a single vector equation:")
                    st.latex(parametric_latex(res, "x"))
                    st.caption(
                        f"{res['n_free']} free variable(s): each can be any value, "
                        f"and the rest are then determined. Every choice gives a "
                        f"valid solution -- infinitely many."
                    )
            except Exception:
                st.caption("Keep eliminating to see the general solution.")
        else:
            st.caption("Reach triangular form to see the general solution.")

    workbench("t05b_infns", 3, right_extra=_render_solution)

    st.markdown(_CLOSING)
