"""Screen 6 -- One matrix, all four spaces."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

_A = np.array([[1, 2], [2, 4]])

_ELIM_LATEX = r"""
\begin{aligned}
A &= \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix} \\
R_2 &\to R_2 - 2 \cdot R_1 \\
&= \begin{bmatrix} 1 & 2 \\ 0 & 0 \end{bmatrix}
\end{aligned}
"""

_ELIM_CAPTION = """
One elimination and everything is visible: one pivot row (one real rule), one
zero row (one redundant rule), one free variable.
"""

_SPACES_HEADING = "**Read all four spaces off the reduced form.**"

_SPACES_TEXT = """
**Column space** -- what it can reach: the line along (1, 2). Targets on it are
solvable; targets off it are not.

**Null space** -- what it squashes to zero: the line along (−2, 1). This is the
freedom: add any multiple of (−2, 1) to a solution and it is still a solution.

**Row space** -- its genuinely different rules: one rule, x1 + 2·x2 (rank 1),
which points along (1, 2).

**Left null space** -- the ways the rows cancel: the line along (−2, 1) (row 2
minus 2·row 1 gives all zeros).

Counting rule check: 1 real rule + 1 free variable = 2 unknowns. ✓

Notice the **orthogonal pairs**: the row space (1, 2) is perpendicular to the null
space (−2, 1) -- their dot product 1·(−2) + 2·1 = 0. The column space (1, 2) is
perpendicular to the left null space (−2, 1) the same way. Two perpendicular
pairs, all on one little 2 by 2.
"""

_SPACES_CAPTION = """
The two lines drawn above ARE all four spaces: column space and row space share
the (1, 2) line; null space and left null space share the (−2, 1) line -- and the
two lines are perpendicular.
"""

_SYM_2X2 = (
    "<p style='font-weight:700;color:#f76707;'>A note on the transpose: to get the "
    "left null space you normally flip the matrix to A-transpose (Aᵀ) and reduce "
    "that. But this matrix is <u>symmetric</u> -- flip it across its diagonal and "
    "it looks identical, so Aᵀ = A. When a matrix is symmetric, transposing changes "
    "nothing, and its left null space is exactly the same as its null space -- here, "
    "both are the line along (−2, 1). (The next screen uses a matrix that is NOT "
    "symmetric, where the transpose really matters.)</p>"
)

_BANNER_TEXT = """
**Now let's go bigger.** The example above lived in 2D, so each space was a line.
Next, a 3-by-3 matrix in 3D -- the same three spaces, but now they're planes and
lines. Watch the ideas scale up one dimension.
"""

_A2 = np.array([[2, 1, 3], [1, 1, 2], [3, 2, 5]])

_RREF2_LATEX = r"""
\left[\begin{array}{ccc|c}
1&0&1&0\\ 0&1&1&0\\
\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0
\end{array}\right]
"""

_RREF2_CAPTION = """
This time the matrix is 3 by 3, and row 3 is just row 1 plus row 2 -- a redundant
rule that collapses to a zero row. Two real rules survive out of three, so the
spaces are now two-dimensional: not lines, but whole PLANES.
"""

_SPACES2_TEXT = """
**Column space** -- a plane: everything the matrix can reach is the flat sheet
spanned by the two surviving columns (2, 1, 3) and (1, 1, 2). Two independent
directions, so a plane, not a line.

**Null space** -- a line: everything squashed to zero runs along (-1, -1, 1). One
free variable, so a single line -- and it points straight through the plane.

**Row space** -- a plane: the two surviving reduced rows, rank 2.

**Left null space** -- a line: the row-combination that cancels is along (-1, -1, 1)
(row 3 minus row 1 minus row 2 gives all zeros). It is perpendicular to the
column-space plane -- it is exactly the line poking through it in the picture.

**Counting rule check:** 2 real rules + 1 free variable = 3 unknowns. ✓ The line
(1 dimension) and the plane (2 dimensions) add up to all of 3D space.
"""

_SYM_3X3 = (
    "<p style='font-weight:700;color:#f76707;'>This 3 by 3 is symmetric too "
    "(Aᵀ = A), so again the left null space matches the null space -- both are the "
    "line along (−1, −1, 1). That is why the left-null line in the picture is the "
    "same line poking through the plane. Symmetry is the special case; when a "
    "matrix is not symmetric, the left null space is genuinely its own space.</p>"
)

_PLANE_CAPTION = """
One matrix, in 3D: the column space is a plane, the null space is a line
through it. Rotate to see the line pierce the plane.
"""

_CLOSING = """
Two more words make this vocabulary complete. The **dimension** of a space is
how many independent directions it has -- a line has dimension 1, a plane 2, the
smoothie's null space 3. A **basis** is the smallest set of vectors that builds
the whole space -- the direction vectors you have been reading off the reduced
form are exactly a basis for the null space. Topic 7 asks a new kind of
question: when the target b is OUTSIDE the column space and there is no exact
answer, what is the CLOSEST we can get? That single question is how line-of-best-
fit, GPS, and camera apps all work.
"""


def render_together():
    # Block 1 -- eliminate once (math left, graph right)
    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        w.editable_matrix("t06_together_A", 2, label="A", editable=False, value=_A,
                          compact=True)
        st.latex(_ELIM_LATEX)
        st.markdown(_ELIM_CAPTION)
    with right:
        fig = plot.new_figure_2d(rng=8)
        plot.add_line_2d(fig, 2, -1, 0, "#4dabf7", "column space: line along (1, 2)")
        plot.add_line_2d(fig, 1, 2, 0, "#ffa94d", "null space: line along (−2, 1)")
        st.plotly_chart(fig, width="stretch")
        st.caption("one matrix, two different lines")

    # Block 2 -- read all four spaces off the reduced form
    st.markdown(_SPACES_HEADING)
    st.markdown(_SPACES_TEXT)
    st.markdown(_SYM_2X2, unsafe_allow_html=True)
    st.latex(r"A^{T} = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix} = A")
    st.caption(_SPACES_CAPTION)

    # Banner -- between the 1D and 2D examples
    st.info(_BANNER_TEXT)

    # Block 3 -- a bigger matrix: spaces become planes (2-dimensional example)
    left2, right2 = st.columns([0.5, 0.5], gap="large")
    with left2:
        w.editable_matrix("t06_together_A2", 3, label="A", editable=False,
                          value=_A2, compact=True)
        st.markdown("Row 3 = row 1 + row 2.")
        st.latex(_RREF2_LATEX)
        st.markdown(_RREF2_CAPTION)
        st.markdown(_SPACES2_TEXT)
        st.markdown(_SYM_3X3, unsafe_allow_html=True)
        st.latex(r"A^{T} = \begin{bmatrix} 2 & 1 & 3 \\ 1 & 1 & 2 \\ 3 & 2 & 5 \end{bmatrix} = A")
    with right2:
        fig2 = plot.new_figure_3d(rng=6)
        plot.add_plane_3d(fig2, -1, -1, 1, 0, "#4dabf7", "column space (a plane)")
        plot._arrow3d(fig2, np.array([2.0, 1.0, 3.0]), "#ff6b6b", "column 1: (2, 1, 3)")
        plot._arrow3d(fig2, np.array([1.0, 1.0, 2.0]), "#51cf66", "column 2: (1, 1, 2)")
        fig2.add_trace(go.Scatter3d(
            x=[2, -2], y=[2, -2], z=[-2, 2], mode="lines",
            line=dict(color="#ffa94d", width=7), name="null space (a line)",
        ))
        st.plotly_chart(fig2, width="stretch")
        st.caption(_PLANE_CAPTION)

    # Block 4 -- closing bridge (text only)
    st.markdown(_CLOSING)
