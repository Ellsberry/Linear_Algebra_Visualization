"""Screen 3 -- Why perpendicular is closest."""
import streamlit as st

_GOAL_TEXT = """
We want the best x -- call it x-hat -- so that A·x-hat is as close to b as possible.
"Closest" means the leftover r = b − A·x-hat is perpendicular to everything the
matrix can reach (the whole column space). We will turn that single sentence into
an equation you can solve.
"""

_STEP1_TEXT = """
**Step 1 -- name the leftover.** After picking x-hat, the leftover is
r = b − A·x-hat.
"""

_STEP1_LATEX = r"r = b - A\hat{x}"

_STEP2_TEXT = """
**Step 2 -- perpendicular to every column.** Closest means r is perpendicular to
each column of A. Perpendicular means dot product zero (Screen 0), so each column
of A dotted with r is zero.
"""

_STEP3_TEXT = """
**Step 3 -- stack those dot products.** Dotting every column of A with r at once is
exactly A-transpose times r. So all those "= 0" conditions become one equation:
Aᵀ r = 0.
"""

_STEP3_LATEX = r"A^T r = 0"

_STEP4_TEXT = """
**Step 4 -- substitute the leftover.** Aᵀ(b − A·x-hat) = 0.
"""

_STEP4_LATEX = r"A^T (b - A\hat{x}) = 0"

_STEP5_TEXT = """
**Step 5 -- expand.** Aᵀb − AᵀA·x-hat = 0, which rearranges to the **normal
equations**: AᵀA·x-hat = Aᵀb.
"""

_STEP5_LATEX = r"A^T b - A^T A \hat{x} = 0 \quad\Longrightarrow\quad A^T A \hat{x} = A^T b"

_STEP6_TEXT = """
**Step 6 -- solve.** When AᵀA can be inverted, x-hat = (AᵀA)⁻¹ Aᵀb. That x-hat is
the best answer -- the one whose leftover is perpendicular to everything reachable.
"""

_STEP6_LATEX = r"\hat{x} = (A^T A)^{-1} A^T b"

_NORMAL_TEXT = """
"Normal" is the old word for perpendicular -- the normal equations are the
perpendicular equations. AᵀA can be inverted as long as the columns of A are
independent (no column is a combination of the others) -- the same
independence idea from Topic 6. When that holds, there is exactly one best answer.
"""

_CLOSING = """
One formula, AᵀA·x-hat = Aᵀb, finds the closest answer for ANY over-crowded
system. The next screen turns it loose on real, messy data.
"""


def render_normal():
    # Block 1 -- the goal (text only)
    st.markdown(_GOAL_TEXT)

    # Block 2 -- the full derivation (math left, no graph)
    st.markdown(_STEP1_TEXT)
    st.latex(_STEP1_LATEX)
    st.markdown(_STEP2_TEXT)
    st.markdown(_STEP3_TEXT)
    st.latex(_STEP3_LATEX)
    st.markdown(_STEP4_TEXT)
    st.latex(_STEP4_LATEX)
    st.markdown(_STEP5_TEXT)
    st.latex(_STEP5_LATEX)
    st.markdown(_STEP6_TEXT)
    st.latex(_STEP6_LATEX)

    # Block 3 -- "normal" + when A^T A is invertible (text only)
    st.markdown(_NORMAL_TEXT)

    # Block 4 -- closing text
    st.markdown(_CLOSING)
