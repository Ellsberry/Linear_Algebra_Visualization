"""Screen 4 -- Row space and the big counting rule."""
import streamlit as st

_INTRO = """
Each row of a matrix is one equation -- one rule the answer must obey. The **row
space** is the collection of every rule you can build by mixing the rows. If one
row is secretly a copy or a combination of the others, mixing it in adds nothing
new -- the row space does not get any bigger.

The number of genuinely different rules -- the rows that actually pin something
down -- is called the **rank**. You have already met it: it is the pivot count on
the workbench banner ("Pivot count = number of genuinely independent equations").
"""

_LOGISTICS_TWO_PLANS_TEXT = """
On the two Logistics screens you built shipping plans where flow in = flow out at
every node. One had a single answer; the other had a free choice. Put them side by
side and the difference is a single zero row -- the same seven-row count, but the
many-plans version leaves one route free.
"""

_ONE_PLAN_RULES_LATEX = r"""
\begin{aligned}
x_1 &= 50 \\
x_2 &= 50 \\
x_3 &= 30 \\
x_4 &= 20 \\
x_5 &= 25 \\
x_6 &= 25
\end{aligned}
"""

_ONE_PLAN_MATRIX_LATEX = r"""
\left[\begin{array}{cccccc|c}
1&0&0&0&0&0&50\\ 0&1&0&0&0&0&50\\ 0&0&1&0&0&0&30\\
0&0&0&1&0&0&20\\ 0&0&0&0&1&0&25\\ 0&0&0&0&0&1&25\\
\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0
\end{array}\right]
"""

_ONE_PLAN_CAPTION = "Six rules, six routes, no freedom -- one definite plan."

_MANY_PLANS_RULES_LATEX = r"""
\begin{aligned}
x_1 + x_5 &= 50 \\
x_2 - x_5 &= 50 \\
x_3 &= 30 \\
x_4 + x_5 &= 20 \\
x_6 &= 25 \\
x_7 &= 25
\end{aligned}
"""

_MANY_PLANS_MATRIX_LATEX = r"""
\left[\begin{array}{ccccccc|c}
1&0&0&0&1&0&0&50\\ 0&1&0&0&-1&0&0&50\\ 0&0&1&0&0&0&0&30\\
0&0&0&1&1&0&0&20\\ 0&0&0&0&0&1&0&25\\ 0&0&0&0&0&0&1&25\\
\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0
\end{array}\right]
"""

_MANY_PLANS_PARAMETRIC_LATEX = r"""
X = \begin{bmatrix}50\\50\\30\\20\\0\\25\\25\end{bmatrix}
+ x_5\begin{bmatrix}-1\\1\\0\\-1\\1\\0\\0\end{bmatrix}
"""

_MANY_PLANS_CAPTION = (
    "Six rules, seven routes -- route x5 is free, giving a whole family of plans."
)

_RULE_TEXT = """
**(number of genuinely different rules) + (number of free variables) = (number
of unknowns).**

Every unknown is either pinned down by a real rule or left free. No unknown is
both; none is neither. That is the whole rule.
"""

_SMOOTHIE_RULES_LATEX = r"""
\begin{aligned}
f_1 + f_3 + \tfrac{3}{2}f_5 &= 0 \\
f_2 + f_4 - \tfrac{1}{2}f_5 &= 0
\end{aligned}
"""

_SMOOTHIE_MATRIX_LATEX = r"""
\left[\begin{array}{ccccc|c}
1&0&1&0&\tfrac{3}{2}&0\\ 0&1&0&1&-\tfrac{1}{2}&0\\
\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0\\
\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0\\
\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0
\end{array}\right]
"""

_SMOOTHIE_CAPTION = "Two rules survive; three ingredients are free."

_SMOOTHIE_PARAMETRIC_LATEX = r"""
X = \begin{bmatrix}0\\0\\0\\0\\0\end{bmatrix}
+ f_3\begin{bmatrix}-1\\0\\1\\0\\0\end{bmatrix}
+ f_4\begin{bmatrix}0\\-1\\0\\1\\0\end{bmatrix}
+ f_5\begin{bmatrix}-\tfrac{3}{2}\\\tfrac{1}{2}\\0\\0\\1\end{bmatrix}
"""

_CIRCUIT_RULES_LATEX = r"""
\begin{aligned}
I_1 &= 6 \\
I_2 &= 2 \\
I_3 &= 3 \\
I_4 &= 3 \\
I_5 &= 1
\end{aligned}
"""

_CIRCUIT_MATRIX_LATEX = r"""
\left[\begin{array}{ccccc|c}
1&0&0&0&0&6\\ 0&1&0&0&0&2\\ 0&0&1&0&0&3\\
0&0&0&1&0&3\\ 0&0&0&0&1&1
\end{array}\right]
"""

_CIRCUIT_CAPTION = "Every current pinned down -- no free variables, one definite answer."

_CLOSING = """
Rank counts the real rules. Free variables count the freedom. Together they
always account for every unknown. The last screen puts all three spaces on one
matrix at once.
"""


def _rule_card(header, rules_latex, matrix_latex, caption, extra_latex=None):
    st.markdown(header)
    left, right = st.columns([1, 1])
    with left:
        st.latex(rules_latex)
    with right:
        st.latex(matrix_latex)
        if extra_latex is not None:
            st.latex(extra_latex)
    st.caption(caption)


def render_row():
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- embedded recap: two Logistics plans side by side
    st.markdown(_LOGISTICS_TWO_PLANS_TEXT)

    lc1, lc2 = st.columns(2)
    with lc1.container(border=True):
        _rule_card(
            "**One plan: 6 real rules + 0 free = 6 unknowns ✓**",
            _ONE_PLAN_RULES_LATEX,
            _ONE_PLAN_MATRIX_LATEX,
            _ONE_PLAN_CAPTION,
        )
    with lc2.container(border=True):
        _rule_card(
            "**Many plans: 6 real rules + 1 free = 7 unknowns ✓**",
            _MANY_PLANS_RULES_LATEX,
            _MANY_PLANS_MATRIX_LATEX,
            _MANY_PLANS_CAPTION,
            extra_latex=_MANY_PLANS_PARAMETRIC_LATEX,
        )

    # Block 3 -- the counting rule (full-width centerpiece)
    st.markdown(_RULE_TEXT)

    c1, c2 = st.columns(2)
    with c1.container(border=True):
        _rule_card(
            "**Smoothie: 2 real rules + 3 free = 5 unknowns ✓**",
            _SMOOTHIE_RULES_LATEX,
            _SMOOTHIE_MATRIX_LATEX,
            _SMOOTHIE_CAPTION,
            extra_latex=_SMOOTHIE_PARAMETRIC_LATEX,
        )
    with c2.container(border=True):
        _rule_card(
            "**Circuit: 5 real rules + 0 free = 5 unknowns ✓**",
            _CIRCUIT_RULES_LATEX,
            _CIRCUIT_MATRIX_LATEX,
            _CIRCUIT_CAPTION,
        )

    # Block 4 -- closing text
    st.markdown(_CLOSING)
