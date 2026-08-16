"""Screen 2 -- Column space: every place the matrix can send you."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

_HOWTO_STEP1_TEXT = """
**Step 1 -- Write the matrix and look at its columns.** The column space
is every output A can produce, which is every combination of its columns. So start
with the columns themselves.
"""

_HOWTO_STEP1_LATEX = r"""
A = \begin{bmatrix} 1 & 2 & 1 & 1 \\ 1 & 3 & 2 & 4 \\ 2 & 5 & 3 & 5 \\ 0 & 1 & 1 & 3 \end{bmatrix}
"""

_HOWTO_STEP2_TEXT = """
**Step 2 -- Row-reduce to find the pivot columns.** Row-reduce to the
reduced form (Reduced Row Echelon Form) and see which columns get a pivot (a leading
1).
"""

_HOWTO_STEP2_LATEX = r"""
\begin{bmatrix}
\color{#ffd43b}{1} & 0 & -1 & -5 \\
0 & \color{#ffd43b}{1} & 1 & 3 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0
\end{bmatrix}
"""

_HOWTO_STEP3_TEXT = """
**Step 3 -- The pivot columns of the ORIGINAL matrix are the answer.**
Columns 1 and 2 hold the pivots, so they are the independent ones -- columns 3 and 4
are just combinations of them and add nothing new. IMPORTANT: take these columns
from the ORIGINAL matrix A, not from the reduced form. The reduced form only tells
you WHICH columns to pick.
"""

_HOWTO_STEP3_LATEX = r"""
\begin{bmatrix} 1 \\ 1 \\ 2 \\ 0 \end{bmatrix}
\qquad
\begin{bmatrix} 2 \\ 3 \\ 5 \\ 1 \end{bmatrix}
"""

_HOWTO_STEP4_TEXT = """
**Step 4 -- Write the column space in parametric form.** Every vector in
the column space is some amount of the first pivot column plus some amount of the
second. Call those amounts c1 and c2.
"""

_HOWTO_STEP4_LATEX = r"""
\text{any output} = \underbrace{\color{#37b24d}{c_1\begin{bmatrix} 1 \\ 1 \\ 2 \\ 0 \end{bmatrix}
+ c_2\begin{bmatrix} 2 \\ 3 \\ 5 \\ 1 \end{bmatrix}}}_{\text{column space}}
"""

_HOWTO_CAPTION = """
Two pivot columns, so the column space is 2-dimensional -- its
dimension is the rank, 2. Those two columns are a basis for it. (This is the SAME
matrix whose null space you compute on the next screen -- one matrix, two spaces.)
"""

_INTRO = """
The **column space** is all possible outputs of the matrix, and its **dimension**
is the **rank** -- which determines solvability, uniqueness of solutions, and how
much information the matrix preserves. It determines whether a system A·x = b has
a solution, because a vector b is solvable only if it lies in the column space of
A. If b is in the column space of A then at least one solution exists; if b is not
in the column space of A then no solution exists.

Take a matrix A. Feed it every possible input x and collect every output A·x.
That collection of all possible outputs is called the **column space**. It gets
that name because every output is a mix of A's columns — so the collection of
outputs and the collection of column-mixes are the same thing.

Here is the sentence that makes this whole topic matter: **the equation A·x = b
has a solution exactly when the target b sits inside the column space** — when b
is somewhere the matrix can actually reach. If b is outside, no input can get
there: no solution.
"""

_REACHABLE_A = [[1.5, 0.5], [0.0, 1.0]]
_SINGULAR_A = [[1.0, 1.0], [1.0, 1.0]]

_REACHABLE_TEXT = """
The two actuator columns point different ways. Mixing them reaches
the entire plane — the column space is the whole plane, so EVERY target b is
reachable.
"""

_SINGULAR_TEXT = """
Both actuator columns point the same way. Mixing them only slides
along one line — the column space is just that line, so any target off the line
is unreachable. You saw this in Topic 4; that line WAS a column space.
"""

_REACHABLE_CAPTION = """
Two different inputs, and their outputs land in different
quadrants — all over the plane. That is why this matrix's column space is the whole
plane: it can reach anywhere.
"""

_WORKED_TEXT = """
Column 2 is exactly 2 × column 1 — they point the same way. Every mix of them
lands on the line along (1, 2). That line is this matrix's column space. A
target like b = (3, 6) is ON the line — reachable. A target like b = (3, 5) is
OFF the line — no solution exists, no matter what x you try.
"""

_CLOSING = """
The column space answers "can we get there?" The next screen asks the opposite
question: what does the matrix squash to nothing?
"""


def render_column():
    # Block 0 -- how to compute a column space, step by step (math, no graph)
    st.markdown("**How to compute the column space of a matrix, step by step.**")
    st.markdown(_HOWTO_STEP1_TEXT)
    st.latex(_HOWTO_STEP1_LATEX)
    st.markdown(_HOWTO_STEP2_TEXT)
    st.latex(_HOWTO_STEP2_LATEX)
    st.markdown(_HOWTO_STEP3_TEXT)
    st.latex(_HOWTO_STEP3_LATEX)
    st.markdown(_HOWTO_STEP4_TEXT)
    st.latex(_HOWTO_STEP4_LATEX)
    st.markdown(_HOWTO_CAPTION)
    st.markdown("---")

    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- embedded robotics recap (the one allowed toggle)
    pose = st.radio("Pose", ["Reachable pose", "Singular pose"],
                    horizontal=True, key="t06_cs_pose")
    reachable = pose == "Reachable pose"
    A = np.array(_REACHABLE_A if reachable else _SINGULAR_A)

    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        w.editable_matrix("t06_cs_A", 2, label="A", editable=False, value=A,
                          compact=True)
        col1, col2 = A[:, 0], A[:, 1]
        st.markdown(f"Column 1 (actuator 1): ({col1[0]:g}, {col1[1]:g})  \n"
                    f"Column 2 (actuator 2): ({col2[0]:g}, {col2[1]:g})")
        st.markdown(_REACHABLE_TEXT if reachable else _SINGULAR_TEXT)
        if reachable:
            rx1, rx2 = np.array([3.0, -3.0]), np.array([-2.0, 3.0])
            rb1, rb2 = A @ rx1, A @ rx2
            st.latex(
                w.bmatrix(A) + r"\cdot" + w.bmatrix(rx1.reshape(-1, 1))
                + " = " + w.bmatrix(rb1.reshape(-1, 1))
                + r"\qquad" + w.bmatrix(A) + r"\cdot" + w.bmatrix(rx2.reshape(-1, 1))
                + " = " + w.bmatrix(rb2.reshape(-1, 1))
            )
            st.markdown(_REACHABLE_CAPTION)
    with right:
        fig = plot.new_figure_2d(rng=8)
        plot.add_vector_2d(fig, (0, 0), A[:, 0], "#ff6b6b", "actuator 1 (column 1)")
        plot.add_vector_2d(fig, (0, 0), A[:, 1], "#4dabf7", "actuator 2 (column 2)")
        if reachable:
            plot.shade_polygon(fig, [(-8, -8), (8, -8), (8, 8), (-8, 8)],
                               "rgba(32,201,151,0.12)", "column space = the whole plane")
            plot.add_point_2d(fig, (3, -3), "#ffa94d", "A·(3, -3)")
            plot.add_point_2d(fig, (-1.5, 3), "#ffa94d", "A·(-2, 3)")
        else:
            plot.add_line_2d(fig, 1, -1, 0, "#20c997", "column space = this line")
            plot.add_point_2d(fig, (4, 2), "#ff6b6b",
                              "b = (4, 2) -- unreachable, outside the column space")
        st.plotly_chart(fig, use_container_width=True)

    # Block 3 -- new worked example A = [[1, 2], [2, 4]]
    A2 = np.array([[1, 2], [2, 4]])
    left2, right2 = st.columns([0.5, 0.5], gap="large")
    with left2:
        w.editable_matrix("t06_cs_A2", 2, label="A", editable=False, value=A2,
                          compact=True)
        st.markdown("Column 1: (1, 2)  \nColumn 2: (2, 4)")
        st.markdown(_WORKED_TEXT)
        x1, x2 = np.array([3.0, -3.0]), np.array([-2.0, 3.0])
        p1, p2 = A2 @ x1, A2 @ x2
        st.latex(
            w.bmatrix(A2) + r"\cdot" + w.bmatrix(x1.reshape(-1, 1)) + " = " + w.bmatrix(p1.reshape(-1, 1))
            + r"\qquad" + w.bmatrix(A2) + r"\cdot" + w.bmatrix(x2.reshape(-1, 1)) + " = " + w.bmatrix(p2.reshape(-1, 1))
        )
    with right2:
        fig2 = plot.new_figure_2d(rng=10)
        plot.add_line_2d(fig2, 2, -1, 0, "#4dabf7", "column space: line along (1, 2)", rng=10)
        plot.add_point_2d(fig2, (3, 6), "#51cf66", "b = (3, 6) -- reachable")
        plot.add_point_2d(fig2, (3, 5), "#ff6b6b", "b = (3, 5) -- unreachable")
        plot.add_point_2d(fig2, (-3, -6), "#ffa94d", "A·(3, -3)")
        plot.add_point_2d(fig2, (4, 8), "#ffa94d", "A·(-2, 3)")
        st.plotly_chart(fig2, use_container_width=True)

    # Block 4 -- closing text
    st.markdown(_CLOSING)
