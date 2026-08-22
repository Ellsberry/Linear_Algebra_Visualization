import numpy as np
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
**Smoothie.** You sell one thousand gallons of smoothies a month, and an ingredient
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

_DIR_F3 = r"\begin{bmatrix}-1\\0\\1\\0\\0\end{bmatrix}"
_DIR_F4 = r"\begin{bmatrix}0\\-1\\0\\1\\0\end{bmatrix}"
_DIR_F5 = r"\begin{bmatrix}-\tfrac{3}{2}\\\tfrac{1}{2}\\0\\0\\1\end{bmatrix}"


def _fmt_scalar(v):
    if abs(v) < 1e-9:
        v = 0.0
    return f"{v:.2f}"


def _col_latex(vals):
    return r"\begin{bmatrix}" + r"\\".join(_fmt_scalar(v) for v in vals) + r"\end{bmatrix}"


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
                    vc_left, vc_right = st.columns([1, 2], gap="medium")
                    with vc_left:
                        st.markdown(
                            "f1 = strawberries  \n"
                            "f2 = bananas  \n"
                            "f3 = yogurt  \n"
                            "f4 = milk  \n"
                            "f5 = honey"
                        )
                    with vc_right:
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

    st.markdown("**Try it yourself: fix any three, the recipe fills in the rest.**")
    st.markdown(
        "The recipe has three free choices and two forced ones. Pick any THREE "
        "ingredients to set yourself (check their boxes and type a change: positive = "
        "add, negative = remove). The other two are then computed for you so that the "
        "total volume and total sweetness both stay at zero. For example, set "
        "strawberries to -10 (short by 10) and watch the recipe work out how to "
        "compensate."
    )

    def _parse_val(raw):
        try:
            return float(raw)
        except (TypeError, ValueError):
            return 0.0

    _fix_labels = ["f1 strawberries", "f2 bananas", "f3 yogurt", "f4 milk", "f5 honey"]
    _fix_default_checked = [True, True, True, False, False]
    _fix_default_values = ["-10", "0", "0", "0", "0"]

    C = np.array([[1, 1, 1, 1, 1], [1, -1, 1, -1, 2]], float)

    fixed = []
    fix_cols = st.columns(5)
    for i, col in enumerate(fix_cols):
        with col:
            checked = st.checkbox(
                "set this one",
                value=_fix_default_checked[i],
                key=f"t05b_smoothie_fix_f{i + 1}",
            )
            raw = st.text_input(
                _fix_labels[i],
                value=_fix_default_values[i],
                key=f"t05b_smoothie_val_f{i + 1}",
            )
        if checked:
            fixed.append((i, _parse_val(raw)))

    if len(fixed) != 3:
        st.warning("Pick exactly 3 ingredients to set -- the other 2 are forced.")
    else:
        fix_idx = [i for i, _ in fixed]
        fix_vals = np.array([v for _, v in fixed], float)
        dep_idx = [i for i in range(5) if i not in fix_idx]

        Cdep = C[:, dep_idx]
        Cfix = C[:, fix_idx]
        if abs(np.linalg.det(Cdep)) < 1e-9:
            st.warning(
                "Those three don't pin down a unique fix -- try setting a different "
                "combination (for example, swap one for another ingredient)."
            )
        else:
            dep_vals = np.linalg.solve(Cdep, -Cfix @ fix_vals)

            x = [0.0] * 5
            for i, v in fixed:
                x[i] = v
            for i, v in zip(dep_idx, dep_vals):
                x[i] = v

            result_cols = st.columns(5)
            for i, col in enumerate(result_cols):
                with col:
                    tag = " (computed for you)" if i in dep_idx else ""
                    st.markdown(f"{_fix_labels[i]}{tag}")
                    st.markdown(f"{x[i]:g}")

            st.markdown("**The parametric formula with your numbers:**")
            f3v, f4v, f5v = x[2], x[3], x[4]
            formula = (
                "X = " + _fmt_scalar(f3v) + r"\," + _DIR_F3
                + " + " + _fmt_scalar(f4v) + r"\," + _DIR_F4
                + " + " + _fmt_scalar(f5v) + r"\," + _DIR_F5
                + " = " + _col_latex(x)
            )
            st.latex(formula)

            volume = sum(x)
            sweetness = x[0] - x[1] + x[2] - x[3] + 2 * x[4]
            if abs(volume) < 1e-9:
                volume = 0.0
            if abs(sweetness) < 1e-9:
                sweetness = 0.0

            m_left, m_right = st.columns(2)
            with m_left:
                st.metric("Total volume", f"{volume:g}")
            with m_right:
                st.metric("Total sweetness", f"{sweetness:g}")

            st.success(
                "Valid swap -- the two free ingredients were adjusted to keep volume "
                "and sweetness locked."
            )
