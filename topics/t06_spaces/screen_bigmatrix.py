"""Screen 7 -- Work it yourself: all four spaces of a big matrix."""
import streamlit as st

from .space_workbench import space_workbench, space_load

_A = [
    [-1, -1, 0, 0, 0, 0, 0],
    [1, 0, -1, -1, 0, 0, 0],
    [0, 1, 0, 0, -1, -1, -1],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1],
]

_AT = [
    [-1, 1, 0, 0, 0, 0, 0],
    [-1, 0, 1, 0, 0, 0, 0],
    [0, -1, 0, 1, 0, 0, 0],
    [0, -1, 0, 0, 1, 0, 0],
    [0, 0, -1, 0, 1, 0, 0],
    [0, 0, -1, 0, 0, 1, 0],
    [0, 0, -1, 0, 0, 0, 1],
]

_INTRO = """
This is the shipping network from Topic 5.5 -- seven routes, seven balance rules --
stripped down to its 7-by-7 matrix. This time YOU find all four of its spaces. It
is bigger than anything you've reduced by hand, so here's the plan: do the first
few row operations yourself to get the feel, then let **Do one step** finish the
job (or jump straight to the answer with **Run to reduced form**). Watch the
pivots appear, then read each space off the result.
"""

_STEP1_HEADING = (
    "**Step 1 -- reduce A to find the column space, null space, and row space.**"
)

_STEP1_CAPTION = (
    "Try a few manual row operations first, then use Do one step to finish."
)

_STEP1_READOFF = """
**Column space** (green) -- 6 pivots appear, in columns 1, 2, 3, 4, 6, and 7. So
the column space is spanned by those 6 columns of the ORIGINAL A. It is
6-dimensional -- too big to draw, but its dimension is the rank, 6.

**Null space** (blue) -- only column 5 has no pivot, so there is one free variable
(route x5). Reading it off gives the single direction (-1, 1, 0, -1, 1, 0, 0) -- the
exact free shipping-plan direction from Topic 5.5. The null space is a line.

**Row space** (purple) -- the 6 nonzero reduced rows, a 6-dimensional space.
"""

_A_PLAIN_LATEX = r"""
A = \begin{bmatrix}
-1 & -1 & 0 & 0 & 0 & 0 & 0 \\
1 & 0 & -1 & -1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & -1 & -1 & -1 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 1
\end{bmatrix}
"""

_AT_PLAIN_LATEX = r"""
A^{T} = \begin{bmatrix}
-1 & 1 & 0 & 0 & 0 & 0 & 0 \\
-1 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & -1 & 0 & 1 & 0 & 0 & 0 \\
0 & -1 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & -1 & 0 & 1 & 0 & 0 \\
0 & 0 & -1 & 0 & 0 & 1 & 0 \\
0 & 0 & -1 & 0 & 0 & 0 & 1
\end{bmatrix}
"""

_COLSPACE_PARAMETRIC_LATEX = r"""
\text{column space} =
c_1 \begin{bmatrix} \color{#37b24d}{-1}\\ \color{#37b24d}{1}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0} \end{bmatrix}
+ c_2 \begin{bmatrix} \color{#37b24d}{-1}\\ \color{#37b24d}{0}\\ \color{#37b24d}{1}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0} \end{bmatrix}
+ c_3 \begin{bmatrix} \color{#37b24d}{0}\\ \color{#37b24d}{-1}\\ \color{#37b24d}{0}\\ \color{#37b24d}{1}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0} \end{bmatrix}
+ c_4 \begin{bmatrix} \color{#37b24d}{0}\\ \color{#37b24d}{-1}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{1}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0} \end{bmatrix}
+ c_5 \begin{bmatrix} \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{-1}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{1}\\ \color{#37b24d}{0} \end{bmatrix}
+ c_6 \begin{bmatrix} \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{-1}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{0}\\ \color{#37b24d}{1} \end{bmatrix}
"""

_NULL_LATEX = r"""
\text{null space} = x_5 \begin{bmatrix}
\color{#4dabf7}{-1}\\ \color{#4dabf7}{1}\\ \color{#4dabf7}{0}\\
\color{#4dabf7}{-1}\\ \color{#4dabf7}{1}\\ \color{#4dabf7}{0}\\
\color{#4dabf7}{0} \end{bmatrix}
"""

_ROWSPACE_PARAMETRIC_LATEX = r"""
\begin{aligned}
\text{row space} = \ & r_1 \begin{bmatrix} \color{#9775fa}{1} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{1} & \color{#9775fa}{0} & \color{#9775fa}{0} \end{bmatrix}
+ r_2 \begin{bmatrix} \color{#9775fa}{0} & \color{#9775fa}{1} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{-1} & \color{#9775fa}{0} & \color{#9775fa}{0} \end{bmatrix} \\
& + r_3 \begin{bmatrix} \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{1} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} \end{bmatrix}
+ r_4 \begin{bmatrix} \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{1} & \color{#9775fa}{1} & \color{#9775fa}{0} & \color{#9775fa}{0} \end{bmatrix} \\
& + r_5 \begin{bmatrix} \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{1} & \color{#9775fa}{0} \end{bmatrix}
+ r_6 \begin{bmatrix} \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{0} & \color{#9775fa}{1} \end{bmatrix}
\end{aligned}
"""

_STEP2_HEADING = "**Step 2 -- reduce Aᵀ to find the left null space.**"

_STEP2_LEADIN = """
The last space needs the transpose. Unlike the neat matrices on the last screen,
this one is NOT symmetric -- Aᵀ is genuinely different from A, so this step really
does new work. Flip A to Aᵀ (swap rows and columns) and reduce it below.
"""

_STEP2_READOFF = """
**Left null space** (orange) -- reducing Aᵀ leaves one free variable, giving the
single direction (1, 1, 1, 1, 1, 1, 1). This one has a beautiful meaning: it says
"add up all seven balance equations" -- and they cancel to zero, because across the
whole network total flow in equals total flow out. The left null space is the
conservation law itself. It is a line.
"""

_LEFTNULL_LATEX = r"""
\text{left null space} = y_1 \begin{bmatrix}
\color{#f76707}{1}\\ \color{#f76707}{1}\\ \color{#f76707}{1}\\
\color{#f76707}{1}\\ \color{#f76707}{1}\\ \color{#f76707}{1}\\
\color{#f76707}{1} \end{bmatrix}
"""

_SUMMARY = """
**All four spaces of the 7-by-7:**
- Column space: 6-dimensional (what the network can produce).
- Row space: 6-dimensional (its genuinely different rules).
- Null space: 1-dimensional, the line along (-1, 1, 0, -1, 1, 0, 0).
- Left null space: 1-dimensional, the line along (1, 1, 1, 1, 1, 1, 1).

Counting rule: 6 real rules + 1 free variable = 7 unknowns. ✓ And because this
matrix is NOT symmetric, the null space and the left null space are genuinely
different directions -- not the same line, the way they were on the symmetric
examples last screen. That is the normal situation; symmetry was the special case.
"""

_CLOSING = """
You just found all four fundamental spaces of a real 7-by-7 system by hand. Every
matrix, no matter how big, has exactly these four -- two that live in the input
space (row space and null space) and two in the output space (column space and
left null space), each pair orthogonal. That is the complete anatomy of a matrix,
and you can now dissect any one you meet.
"""


def render_bigmatrix():
    # Block 1 -- intro (text only)
    st.markdown(_INTRO)

    # Block 2 -- reduce A yourself (interactive)
    st.markdown(_STEP1_HEADING)
    st.markdown("You start with A:")
    st.latex(_A_PLAIN_LATEX)
    if st.session_state.get("t06_big_A_last") is None:
        space_load("t06_big_A", _A)
        st.session_state["t06_big_A_last"] = "loaded"
    space_workbench("t06_big_A", 7, matrix_label="A")
    st.caption(_STEP1_CAPTION)
    st.markdown(_STEP1_READOFF)
    st.markdown("The column space is the span of the 6 pivot columns of the ORIGINAL "
                "A (all but column 5):")
    st.latex(_COLSPACE_PARAMETRIC_LATEX)
    st.latex(_NULL_LATEX)
    st.markdown("The row space is the span of the 6 nonzero reduced rows:")
    st.latex(_ROWSPACE_PARAMETRIC_LATEX)

    # Block 3 -- reduce Aᵀ yourself (interactive)
    st.markdown(_STEP2_HEADING)
    st.markdown(_STEP2_LEADIN)
    st.markdown("You start with Aᵀ:")
    st.latex(_AT_PLAIN_LATEX)
    if st.session_state.get("t06_big_AT_last") is None:
        space_load("t06_big_AT", _AT)
        st.session_state["t06_big_AT_last"] = "loaded"
    space_workbench("t06_big_AT", 7, matrix_label="A^{T}")
    st.markdown(_STEP2_READOFF)
    st.latex(_LEFTNULL_LATEX)

    # Block 4 -- the four-space summary + counting (text only)
    st.markdown(_SUMMARY)

    # Block 5 -- closing text
    st.markdown(_CLOSING)
