"""Screen 5 -- One matrix, all three spaces."""
import numpy as np
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

_SPACES_TEXT = """
**Column space** -- what it can reach: the line along (1, 2). Targets on it are
solvable; targets off it are not.

**Null space** -- what it squashes to zero: the line along (−2, 1). This is the
freedom: add any multiple of (−2, 1) to a solution and it is still a solution.

**Row space** -- its genuinely different rules: one rule, x1 + 2·x2 (rank 1).

Counting rule check: 1 real rule + 1 free variable = 2 unknowns. ✓
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
        st.plotly_chart(fig, use_container_width=True)
        st.caption("one matrix, two different lines")

    # Block 2 -- read all three spaces off the reduced form
    st.markdown(_SPACES_TEXT)

    # Block 3 -- closing bridge (text only)
    st.markdown(_CLOSING)
