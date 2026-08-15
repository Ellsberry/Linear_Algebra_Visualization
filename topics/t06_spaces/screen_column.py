"""Screen 2 -- Column space: every place the matrix can send you."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

_INTRO = """
Take a matrix A. Feed it every possible input x and collect every output A·x.
That collection of all possible outputs is called the **column space**. It gets
that name because every output is a mix of A's columns -- so the collection of
outputs and the collection of column-mixes are the same thing.

Here is the sentence that makes this whole topic matter: **the equation A·x = b
has a solution exactly when the target b sits inside the column space** -- when b
is somewhere the matrix can actually reach. If b is outside, no input can get
there: no solution.
"""

_REACHABLE_A = [[1.5, 0.5], [0.0, 1.0]]
_SINGULAR_A = [[1.0, 1.0], [1.0, 1.0]]

_REACHABLE_TEXT = """
The two actuator columns point different ways. Mixing them reaches
the entire plane -- the column space is the whole plane, so EVERY target b is
reachable.
"""

_SINGULAR_TEXT = """
Both actuator columns point the same way. Mixing them only slides
along one line -- the column space is just that line, so any target off the line
is unreachable. You saw this in Topic 4; that line WAS a column space.
"""

_WORKED_TEXT = """
Column 2 is exactly 2 × column 1 -- they point the same way. Every mix of them
lands on the line along (1, 2). That line is this matrix's column space. A
target like b = (3, 6) is ON the line -- reachable. A target like b = (3, 5) is
OFF the line -- no solution exists, no matter what x you try.
"""

_CLOSING = """
The column space answers "can we get there?" The next screen asks the opposite
question: what does the matrix squash to nothing?
"""


def render_column():
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
    with right:
        fig = plot.new_figure_2d(rng=8)
        plot.add_vector_2d(fig, (0, 0), A[:, 0], "#ff6b6b", "actuator 1 (column 1)")
        plot.add_vector_2d(fig, (0, 0), A[:, 1], "#4dabf7", "actuator 2 (column 2)")
        if reachable:
            plot.shade_polygon(fig, [(-8, -8), (8, -8), (8, 8), (-8, 8)],
                               "rgba(32,201,151,0.12)", "column space = the whole plane")
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
    with right2:
        fig2 = plot.new_figure_2d(rng=8)
        plot.add_line_2d(fig2, 2, -1, 0, "#4dabf7", "column space: line along (1, 2)")
        plot.add_point_2d(fig2, (3, 6), "#51cf66", "b = (3, 6) -- reachable")
        plot.add_point_2d(fig2, (3, 5), "#ff6b6b", "b = (3, 5) -- unreachable")
        st.plotly_chart(fig2, use_container_width=True)

    # Block 4 -- closing text
    st.markdown(_CLOSING)
