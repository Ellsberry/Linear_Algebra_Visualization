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

_LOGISTICS_TEXT = """
On the Logistics (one plan) screen you developed 7 equations for 6 unknowns, and
one collapsed to the harmless row 0 = 0 -- it was already implied by the others.
Seven rows, but only six genuinely different rules: the rank is 6, not 7. The
row space is built from six rules; the seventh added nothing.
"""

_REDUCED_LATEX = r"""
\begin{bmatrix}
1 & 0 & 0 & 0 & 0 & 0 & \big| & b_1 \\
0 & 1 & 0 & 0 & 0 & 0 & \big| & b_2 \\
0 & 0 & 1 & 0 & 0 & 0 & \big| & b_3 \\
0 & 0 & 0 & 1 & 0 & 0 & \big| & b_4 \\
0 & 0 & 0 & 0 & 1 & 0 & \big| & b_5 \\
0 & 0 & 0 & 0 & 0 & 1 & \big| & b_6 \\
\color{gray}{0 & 0 & 0 & 0 & 0 & 0 & \big| & 0}
\end{bmatrix}
"""

_REDUCED_CAPTION = "Bottom row (dimmed): 0 = 0 -- added nothing."

_RULE_TEXT = """
**(number of genuinely different rules) + (number of free variables) = (number
of unknowns).**

Every unknown is either pinned down by a real rule or left free. No unknown is
both; none is neither. That is the whole rule.
"""

_CLOSING = """
Rank counts the real rules. Free variables count the freedom. Together they
always account for every unknown. The last screen puts all three spaces on one
matrix at once.
"""


def render_row():
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- embedded logistics one-plan recap (static, no graph)
    st.markdown(_LOGISTICS_TEXT)
    st.latex(_REDUCED_LATEX)
    st.caption(_REDUCED_CAPTION)

    # Block 3 -- the counting rule (full-width centerpiece)
    st.markdown(_RULE_TEXT)

    c1, c2, c3 = st.columns(3)
    with c1.container(border=True):
        st.markdown("**Smoothie**")
        st.markdown("2 real rules + 3 free = 5 unknowns ✓")
    with c2.container(border=True):
        st.markdown("**Logistics (many plans)**")
        st.markdown("6 real rules + 1 free = 7 unknowns ✓")
    with c3.container(border=True):
        st.markdown("**Circuit**")
        st.markdown("5 real rules + 0 free = 5 unknowns ✓")
        st.caption("Zero free variables is exactly why the circuit had one "
                   "definite answer.")

    # Block 4 -- closing text
    st.markdown(_CLOSING)
