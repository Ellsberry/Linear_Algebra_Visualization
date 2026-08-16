"""Screen 3 -- Null space: every input the matrix squashes to zero."""
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

_HOWTO_STEP1_TEXT = """
**Step 1 -- Set up A·x = 0.** The null space is every input x the matrix
sends to zero. So we solve A·x = 0.
"""

_HOWTO_STEP1_LATEX = r"""
A\,x = \begin{bmatrix} 1 & 2 & 1 & 1 \\ 1 & 3 & 2 & 4 \\ 2 & 5 & 3 & 5 \\ 0 & 1 & 1 & 3 \end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ x_4 \end{bmatrix}
= \begin{bmatrix} 0 \\ 0 \\ 0 \\ 0 \end{bmatrix}
"""

_HOWTO_STEP2_TEXT = """
**Step 2 -- Form the augmented matrix [A | 0] and row-reduce.** Attach a
column of zeros and row-reduce to the reduced form (Reduced Row Echelon
Form).
"""

_HOWTO_AUG = [[1, 2, 1, 1, 0], [1, 3, 2, 4, 0], [2, 5, 3, 5, 0], [0, 1, 1, 3, 0]]
_HOWTO_RREF = [[1, 0, -1, -5, 0], [0, 1, 1, 3, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

_HOWTO_STEP3_TEXT = """
**Step 3 -- Identify pivot and free variables.** The reduced form has
pivots (leading 1s) in columns 1 and 2, so x1 and x2 are the pivot
variables. Columns 3 and 4 have no pivot, so x3 and x4 are free -- you may
choose them to be anything.
"""

_HOWTO_STEP3_LATEX = r"""
\left[\begin{array}{cccc|c}
\color{#ffd43b}{1} & 0 & -1 & -5 & 0 \\
0 & \color{#ffd43b}{1} & 1 & 3 & 0 \\
0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0
\end{array}\right]
"""

_HOWTO_STEP4_TEXT = """
**Step 4 -- Solve the pivot variables in terms of the free variables.**
First read each pivot row straight off the reduced form, then move the
free variables to the right side.
"""

_HOWTO_STEP4_BEFORE_LATEX = r"""
\begin{aligned}
x_1 - x_3 - 5x_4 &= 0 \\
x_2 + x_3 + 3x_4 &= 0
\end{aligned}
"""

_HOWTO_STEP4_AFTER_LATEX = r"""
\begin{aligned}
x_1 &= x_3 + 5x_4 \\
x_2 &= -x_3 - 3x_4 \\
x_3 &= x_3\ (\text{free}) \\
x_4 &= x_4\ (\text{free})
\end{aligned}
"""

_HOWTO_STEP5_TEXT = """
**Step 5 -- Write the null space in parametric form.** To turn those
equations into vectors, do what you learned earlier: set one free
variable to 1 and the rest to 0, and read off the column. Setting
(x3, x4) = (1, 0) gives the first direction; (0, 1) gives the second.
"""

_HOWTO_STEP5_LATEX = r"""
x = \underbrace{\begin{bmatrix} 0 \\ 0 \\ 0 \\ 0 \end{bmatrix}}_{\text{particular}}
+ \underbrace{\color{#4dabf7}{x_3\begin{bmatrix} 1 \\ -1 \\ 1 \\ 0 \end{bmatrix}
+ x_4\begin{bmatrix} 5 \\ -3 \\ 0 \\ 1 \end{bmatrix}}}_{\text{null space}}
"""

_HOWTO_CAPTION = """
Because the system equals zero, the particular part is zero -- so the
ENTIRE answer is the null space (the blue part). Two free variables, so
it is 2-dimensional; those two vectors are a basis for it.
"""

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
    # Block 0 -- how to compute a null space, step by step (math, no graph)
    st.markdown("**How to compute the null space of a matrix, step by step.**")
    st.markdown(_HOWTO_STEP1_TEXT)
    st.latex(_HOWTO_STEP1_LATEX)
    st.markdown(_HOWTO_STEP2_TEXT)
    st.latex(w.aug_array_latex(_HOWTO_AUG, 4) + r"\;\to\;" + w.aug_array_latex(_HOWTO_RREF, 4))
    st.markdown(_HOWTO_STEP3_TEXT)
    st.latex(_HOWTO_STEP3_LATEX)
    st.markdown(_HOWTO_STEP4_TEXT)
    st.latex(_HOWTO_STEP4_BEFORE_LATEX)
    st.latex(_HOWTO_STEP4_AFTER_LATEX)
    st.markdown(_HOWTO_STEP5_TEXT)
    st.latex(_HOWTO_STEP5_LATEX)
    st.markdown(_HOWTO_CAPTION)
    st.markdown("---")

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
