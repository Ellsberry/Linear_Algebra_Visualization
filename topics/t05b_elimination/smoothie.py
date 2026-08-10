import streamlit as st

from .workbench import workbench, _make_aug, _load_aug, _is_upper_triangular
from engine.parametric import (
    solve_parametric,
    parametric_latex,
    solution_equations_block,
)


# ---------------------------------------------------------------------------
# Screen 7 -- Smoothie (solution space / free variables)
# ---------------------------------------------------------------------------

_A = [[1, 1, 1, 1, 1],
      [1, -1, 1, -1, 2],
      [2, 0, 2, 0, 3],
      [1, 3, 1, 3, 0],
      [7, -1, 7, -1, 11]]
_b = [0, 0, 0, 0, 0]

_INTRO = """
**Smoothie.** You sell thousands of gallons of smoothies a month, and an ingredient
shortage means you have to change a recipe -- but you must keep two things exactly
the same: the total volume and the total sweetness. The question is how much to
change each ingredient. Each change is an unknown: f1 = strawberries, f2 = bananas,
f3 = yogurt, f4 = milk, f5 = honey. Your nutrition app turns "keep volume and
sweetness fixed" into five equations -- but as you'll see, several of them say the
same thing, so there isn't one right answer. There are infinitely many, and they
form a whole space of choices.
"""

_NOTICE = """
Because a change can't add or remove total volume or sweetness, every equation is
set to 0. Run the elimination: three of the five equations turn out to be repeats of
the others, so they vanish to 0 = 0. That leaves only two real constraints on five
unknowns -- so three of the ingredients are FREE. You can pick any change for those
three, and the other two are then forced. Three free choices means the answers form
a 3-dimensional space.
"""

_CLOSING = """
Each direction vector is one "adjustment pattern" -- a way to tweak the ingredients
that keeps volume and sweetness fixed. For example, changing yogurt (f3) by +2 while
leaving milk and honey alone forces strawberries (f1) by -2 and the rest at 0. Any
mix of the three patterns is a valid new recipe. That's what a 3-dimensional solution
space means: three independent dials you can turn, each keeping every constraint
satisfied.
"""

_LEGEND = "f1 = strawberries · f2 = bananas · f3 = yogurt · f4 = milk · f5 = honey"


def render_smoothie():
    st.markdown(_INTRO)
    st.info(_NOTICE)
    st.caption(_LEGEND)

    st.radio("Preset", ["Volume + sweetness locked"], key="t05b_smoothie_preset",
              horizontal=True)

    if st.session_state.get("t05b_smoothie_last") is None:
        aug = _make_aug(_A, _b)
        _load_aug("t05b_smoothie", aug)
        st.session_state["t05b_smoothie_last"] = "loaded"

    def _render_solution():
        M = st.session_state.get("t05b_smoothie_M")
        if M is not None and _is_upper_triangular(M, 5):
            try:
                res = solve_parametric(M, 5, "f")
                st.markdown("**General solution:**")
                if res["status"] == "no_solution":
                    st.latex(parametric_latex(res, "f"))
                else:
                    st.markdown("Read each ingredient change off the reduced rows:")
                    st.latex(solution_equations_block(res, "f"))
                    st.markdown("As a single vector equation:")
                    st.latex(parametric_latex(res, "f"))
                    st.caption(f"{res['n_free']} free variables -> a {res['n_free']}-"
                               f"dimensional solution space: three independent ways to tweak "
                               f"the recipe while keeping volume and sweetness fixed.")
            except Exception:
                st.caption("Keep eliminating to see the general solution.")
        else:
            st.caption("Reach triangular form to see the general solution.")

    workbench("t05b_smoothie", 5, var_name="f", right_extra=_render_solution)

    st.markdown(_CLOSING)
