"""Screen 3 -- Null space: every input the matrix squashes to zero."""
import streamlit as st

from engine import plotting as plot

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
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- new drawable example A = [[1, 2], [2, 4]]
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
        st.plotly_chart(fig, use_container_width=True)

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
