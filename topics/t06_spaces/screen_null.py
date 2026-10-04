"""Screen 3 -- Null space: every input the matrix squashes to zero."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

from .space_workbench import space_workbench, space_load

_INTRO = """
Some inputs x get sent by the matrix to the zero vector: A·x = (0, 0, ..., 0).
Collect ALL the inputs that get squashed to zero. That collection is the **null
space** ("null" means zero). The input x = 0 is always in it -- the matrix always
sends zero to zero. The interesting question is whether anything ELSE is in it.

Why care? The null space is exactly the FREEDOM in your answers. If A·x = b has
one solution, then adding anything from the null space to that solution gives
another solution -- because the null-space part contributes zero. One particular
answer plus the null space = every answer.
"""

_SYSTEM_LATEX = r"""
\begin{aligned}
1 \cdot x_1 + 2 \cdot x_2 &= 0 \\
2 \cdot x_1 + 4 \cdot x_2 &= 0
\end{aligned}
"""

_SYSTEM_TEXT = """
The second rule is just twice the first -- one real rule. It says x1 = −2·x2. So
pick anything for x2 and the rule hands you x1. Every choice gives an input the
matrix squashes to zero: (−2, 1), (−4, 2), (2, −1)... all of them on one line.
That line -- the line along (−2, 1) -- is this matrix's null space.
"""

_CHECK_LATEX = r"""
\begin{aligned}
A \cdot (-2, 1) &= \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}
\begin{bmatrix} -2 \\ 1 \end{bmatrix} \\
&= \begin{bmatrix} 1(-2) + 2(1) \\ 2(-2) + 4(1) \end{bmatrix}
= \begin{bmatrix} 0 \\ 0 \end{bmatrix}
\end{aligned}
"""

_SMOOTHIE_TEXT = """
On the Smoothie screen every equation was "= 0": five rules, five unknowns, and
the answer was a whole 3-dimensional space of recipe changes that all satisfied
A·x = 0. That solution space WAS a null space -- you have already computed one.
Five unknowns live in 5-dimensional space, which nobody can draw -- so for this
one the picture is the three direction vectors themselves.
"""

_SMOOTHIE_LATEX = r"""
X = f_3\begin{bmatrix} -1 \\ 0 \\ 1 \\ 0 \\ 0 \end{bmatrix}
+ f_4\begin{bmatrix} 0 \\ -1 \\ 0 \\ 1 \\ 0 \end{bmatrix}
+ f_5\begin{bmatrix} -\frac{3}{2} \\ \frac{1}{2} \\ 0 \\ 0 \\ 1 \end{bmatrix}
"""

_SMOOTHIE_LEGEND = "f1 = strawberries · f2 = bananas · f3 = yogurt · f4 = milk · f5 = honey"

_LOGISTICS_TEXT = """
On the Logistics screen the answer was one particular plan plus any multiple of
a direction vector: x1 = 50 − x5, x2 = 50 + x5, x3 = 30, x4 = 20 − x5, x5 free,
x6 = 25, x7 = 25. That direction vector -- (−1, 1, 0, −1, 1, 0, 0) -- lives in the
null space. One particular answer plus the null space = every answer. That is
the sentence from the top of this screen, working on a real problem.
"""

_CLOSING = """
Column space: what the matrix can reach. Null space: what it squashes to zero.
One more space to name, and then a counting rule connects all three.
"""


def render_null():
    # Block 0 -- interactive: reduce it yourself, then read off the answer
    st.markdown("**Reduce it yourself: find the null space.**")
    st.markdown(
        "The null space is every input x with A x = 0. Because the right-hand side is "
        "all zeros, you only need to row-reduce A itself. Reduce A below to reduced "
        "form, note which columns have pivots (the pivot variables) and which don't "
        "(the free variables), then read the null space underneath."
    )
    _NULL_A = [[1, 2, 1, 1], [1, 3, 2, 4], [2, 5, 3, 5], [0, 1, 1, 3]]
    if st.session_state.get("t06_null_wb_last") is None:
        space_load("t06_null_wb", _NULL_A)
        st.session_state["t06_null_wb_last"] = "loaded"
    space_workbench("t06_null_wb", 4, matrix_label="A")

    st.markdown("**Now read the null space off your reduced form.**")
    # color-coded RREF: pivot cols 1,2 yellow; free cols 3,4 blue
    st.latex(
        r"\begin{bmatrix}"
        r"\color{#ffd43b}{1} & \color{#ffd43b}{0} & \color{#4dabf7}{-1} & \color{#4dabf7}{-5} \\"
        r"\color{#ffd43b}{0} & \color{#ffd43b}{1} & \color{#4dabf7}{1} & \color{#4dabf7}{3} \\"
        r"\color{#ffd43b}{0} & \color{#ffd43b}{0} & \color{#4dabf7}{0} & \color{#4dabf7}{0} \\"
        r"\color{#ffd43b}{0} & \color{#ffd43b}{0} & \color{#4dabf7}{0} & \color{#4dabf7}{0}"
        r"\end{bmatrix}"
    )
    st.caption(
        "Yellow = pivot columns (x1, x2, the pivot variables). Blue = free columns "
        "(x3, x4) -- these become the blue direction vectors in the null space below."
    )
    st.markdown(
        "Reading each pivot row and moving the free variables across gives "
        "x1 = x3 + 5 x4 and x2 = -x3 - 3 x4."
    )
    st.latex(
        r"\begin{aligned} x_1 &= x_3 + 5x_4 \\ x_2 &= -x_3 - 3x_4 \\"
        r" x_3 &= x_3\ (\text{free}) \\ x_4 &= x_4\ (\text{free}) \end{aligned}"
    )
    st.latex(
        r"x = \underbrace{\begin{bmatrix} 0 \\ 0 \\ 0 \\ 0 \end{bmatrix}}_{\text{particular}}"
        r" + \underbrace{\color{#4dabf7}{x_3\begin{bmatrix} 1 \\ -1 \\ 1 \\ 0 \end{bmatrix}"
        r" + x_4\begin{bmatrix} 5 \\ -3 \\ 0 \\ 1 \end{bmatrix}}}_{\text{null space}}"
    )
    st.caption(
        "Two free variables, so the null space is 2-dimensional. Because the system "
        "equals zero, the particular part is zero -- the entire answer is the null "
        "space (the blue part)."
    )
    st.markdown("---")
    st.markdown(
        "You just found the null space of a big 4x4 by reducing it. Now take the "
        "smallest interesting example -- a 2x2 -- where the null space is a line we can "
        "actually draw and watch. Reduce it yourself, then see what 'squashed to zero' "
        "looks like."
    )

    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- new drawable example A = [[1, 2], [2, 4]]
    # The 2x2 workbench gets its own full-width row: space_workbench builds nested
    # columns internally, which can't go inside the left column below.
    st.markdown("**Reduce this 2x2 to find its null space.**")
    _NULL_A2 = [[1, 2], [2, 4]]
    if st.session_state.get("t06_null_wb2_last") is None:
        space_load("t06_null_wb2", _NULL_A2)
        st.session_state["t06_null_wb2_last"] = "loaded"
    space_workbench("t06_null_wb2", 2, matrix_label="A")
    st.markdown(
        "One step (R2 -> R2 - 2 R1) reduces it to [[1, 2], [0, 0]]: one pivot (x1), one "
        "free variable (x2). The surviving rule is x1 + 2 x2 = 0. Read a null-space "
        "vector off that rule and try it below."
    )

    # Block 2a -- fill in the blue (null-space) part of the parametric equation
    st.markdown("**Fill in the blue part of the parametric equation:**")
    # lay out  x  =  [0;0]  + x2 ·  [ box ; box ]  as one row
    eq = st.columns([0.8, 1.2, 1.2, 1.4])
    with eq[0]:
        st.latex(r"x =")
    with eq[1]:
        st.latex(r"\underbrace{\begin{bmatrix} 0 \\ 0 \end{bmatrix}}_{\text{particular}}")
    with eq[2]:
        st.latex(r"+\; x_2 \cdot")
    with eq[3]:
        b1 = st.number_input("top entry", value=0.0, step=1.0,
                             key="t06_null_fill_1", label_visibility="collapsed")
        b2 = st.number_input("bottom entry", value=0.0, step=1.0,
                             key="t06_null_fill_2", label_visibility="collapsed")
    st.caption("Type the two numbers of the null-space direction (the blue vector), "
               "then it checks whether the matrix squashes it to zero.")

    # live check (no button -- updates as they type)
    A_ = np.array([[1, 2], [2, 4]], float)
    v_ = np.array([b1, b2], float)
    Av_ = A_ @ v_
    if np.allclose(v_, 0):
        st.info("Both zero so far -- the zero vector is always in the null space, but "
                "find a NONZERO direction.")
    elif np.allclose(Av_, 0):
        st.success(f"Correct! A·({b1:g}, {b2:g}) = (0, 0) -- that vector is in the null "
                   f"space. (Any nonzero multiple of (-2, 1) works.)")
    else:
        st.error(f"Not yet: A·({b1:g}, {b2:g}) = ({Av_[0]:g}, {Av_[1]:g}), not (0, 0). "
                 f"The rule x1 + 2 x2 = 0 means x1 = -2 x2.")

    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        st.latex(_SYSTEM_LATEX)
        st.markdown(_SYSTEM_TEXT)
        st.latex(_CHECK_LATEX)
    with right:
        fig = plot.new_figure_2d(rng=8)
        plot.add_line_2d(fig, 1, 2, 0, "#4dabf7",
                         "null space -- everything squashed to zero")
        plot.add_point_2d(fig, (-2, 1), "#ffa94d", "(−2, 1)")
        plot.add_point_2d(fig, (-4, 2), "#ffa94d", "(−4, 2)")
        plot.add_point_2d(fig, (2, -1), "#ffa94d", "(2, −1)")
        plot.add_line_2d(fig, 2, -1, 0, "rgba(160,160,160,0.6)",
                         "column space (from the last screen)")
        st.plotly_chart(fig, width="stretch")

    # Block 2b -- watch the rocket get squashed (Before / After toggle)
    A2 = np.array([[1, 2], [2, 4]])
    st.markdown("**Watch the rocket get squashed.** This matrix flattens the whole "
                "plane onto the column-space line. The null-space direction (-2, 1) "
                "is the direction everything gets crushed along -- points that differ "
                "by it land on the same spot, which is how information is lost.")
    view = st.radio("View", ["Before", "After squashing"], horizontal=True,
                    key="t06_null_squash")
    # Scale 1.0 keeps the squashed nose (y = 7.92) inside the rng=8 view.
    R = plot._ROCKET * 1.0
    sq_left, sq_right = st.columns([0.5, 0.5], gap="large")
    with sq_right:
        fig_sq = plot.new_figure_2d(rng=8)
        if view == "Before":
            plot.shade_polygon(fig_sq, list(zip(R[0], R[1])),
                               "rgba(255,146,43,0.85)", "rocket",
                               line_color="#e8590c", line_width=2)
            plot.add_vector_2d(fig_sq, (0, 0), (-2, 1), "rgba(160,160,160,0.6)",
                               "null space (-2, 1): inputs along here vanish")
        else:
            R2 = A2 @ R
            plot.add_line_2d(fig_sq, 2, -1, 0, "rgba(160,160,160,0.6)",
                             "column space (1, 2): where all outputs land")
            plot.shade_polygon(fig_sq, list(zip(R2[0], R2[1])),
                               "rgba(255,146,43,0.85)", "squashed rocket = A·(rocket)",
                               line_color="#e8590c", line_width=3)
        st.plotly_chart(fig_sq, width="stretch")
    with sq_left:
        if view == "Before":
            st.caption("This arrow is the NULL SPACE -- the input directions the "
                       "matrix sends to zero. It is NOT the line the rocket flattens "
                       "onto; watch where the rocket lands, which is a different "
                       "(output) direction.")
        st.markdown("Why two different directions? The **null space (-2, 1)** is "
                    "which INPUTS vanish; the **column space (1, 2)** is where OUTPUTS "
                    "land. They point different ways because one lives in the input "
                    "space and the other in the output space -- that is the whole "
                    "point: a matrix can crush one set of directions (inputs) while "
                    "piling everything onto another (outputs).")
        for name, idx in [("nose", 0), ("right fin tip", 3),
                          ("left fin tip", 8), ("base", 5)]:
            v = R[:, idx]
            st.markdown(f"{name}:")
            st.latex(w.bmatrix(A2) + r"\cdot" + w.bmatrix(v.reshape(-1, 1))
                     + " = " + w.bmatrix((A2 @ v).reshape(-1, 1)))
        st.caption("Every vertex lands on the line (1, 2) -- the rocket is flattened "
                   "onto the column space.")
        if view == "After squashing":
            st.caption("The rocket is flattened onto the line (1, 2) -- a whole "
                       "dimension is gone. Everything along (-2, 1) was crushed to "
                       "nothing: that direction is the null space.")

    # Block 3 -- embedded smoothie recap (static, no toggle)
    left2, right2 = st.columns([0.5, 0.5], gap="large")
    with left2:
        st.markdown(_SMOOTHIE_TEXT)
    with right2:
        st.latex(_SMOOTHIE_LATEX)
        st.caption(_SMOOTHIE_LEGEND)

    # Block 4 -- embedded logistics recap (static, full width, no graph)
    st.markdown(_LOGISTICS_TEXT)

    # Block 5 -- closing text
    st.markdown(_CLOSING)
