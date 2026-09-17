"""Screen 5 -- Left null space: the ways the rules cancel out."""
import streamlit as st

from .space_workbench import space_workbench, space_load

_INTRO = """
You have met three collections so far: the column space (what the matrix can
reach), the null space (what it squashes to zero), and the row space (its
genuinely different rules). There is a fourth. Remember how, during elimination,
some rows collapsed to "0 = 0"? Those redundant rows didn't vanish by accident --
they happened because certain combinations of the rows themselves add up to
nothing. The collection of all those row-combinations that cancel to zero is the
**left null space**. It measures the redundancy among the rows -- exactly the
"0 = 0" leftovers, now given a name.
"""

_LEADIN = """
To find it, flip the matrix on its side -- swap its rows and columns to get
**A-transpose** (written Aᵀ) -- and then find the null space of Aᵀ using the same
recipe from the null-space screen. The vectors you get are the row-combinations
that cancel A to zero.
"""

_A_LATEX = r"""
A = \begin{bmatrix} 1 & 2 & 1 & 1 \\ 1 & 3 & 2 & 4 \\ 2 & 5 & 3 & 5 \\ 0 & 1 & 1 & 3 \end{bmatrix}
"""

_AT_LATEX = r"""
A^T = \begin{bmatrix} 1 & 1 & 2 & 0 \\ 2 & 3 & 5 & 1 \\ 1 & 2 & 3 & 1 \\ 1 & 4 & 5 & 3 \end{bmatrix}
"""

_AT_RREF_LATEX = r"""
\begin{bmatrix} 1 & 0 & 1 & -1 \\ 0 & 1 & 1 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}
"""

_PARAMETRIC_LATEX = r"""
y = \underbrace{\color{#f76707}{y_1\begin{bmatrix}-1\\-1\\1\\0\end{bmatrix}
+ y_2\begin{bmatrix}1\\-1\\0\\1\end{bmatrix}}}_{\text{left null space}}
"""

_VERIFY_TEXT = """
Check: each of these row-combinations really cancels A to zero.
"""

_VERIFY_LATEX = r"""
y^T A = (-1)\cdot\text{row}_1 + (-1)\cdot\text{row}_2 + 1\cdot\text{row}_3 + 0\cdot\text{row}_4
= \begin{bmatrix} 0 & 0 & 0 & 0 \end{bmatrix}
"""

_HOWTO_CAPTION = """
Two free variables, so the left null space is 2-dimensional --
its dimension is rows minus rank, 4 - 2 = 2. Same matrix as the other three recipes
-- now all four spaces come from one matrix.
"""

_FOUR_SPACES_TEXT = """
Now all four collections are named, and they pair up by orthogonality -- the idea
from the top of this topic. The **row space** and the **null space** are
orthogonal: one holds the rules, the other holds what those rules leave free, and
they meet at right angles. The **column space** and the **left null space** are
orthogonal in the same way. Four spaces, two orthogonal pairs -- the complete
anatomy of a matrix.
"""

_CLOSING = """
That completes the set. The next screen takes one matrix and lays all four of
these spaces out together.
"""


def render_leftnull():
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- reduce Aᵀ yourself (interactive)
    st.markdown(_LEADIN)
    st.latex(_A_LATEX)
    st.markdown(
        "**Reduce Aᵀ yourself.** Swap A's rows and columns to get Aᵀ, then row-reduce "
        "it below. The free-variable directions of its reduced form are the left null "
        "space."
    )
    _AT = [[1, 1, 2, 0], [2, 3, 5, 1], [1, 2, 3, 1], [1, 4, 5, 3]]
    if st.session_state.get("t06_leftnull_wb_last") is None:
        space_load("t06_leftnull_wb", _AT)
        st.session_state["t06_leftnull_wb_last"] = "loaded"
    space_workbench("t06_leftnull_wb", 4, matrix_label="A^{T}")
    st.markdown("**Now read the left null space off your reduced form.**")
    st.latex(
        r"\begin{bmatrix}"
        r"\color{#ffd43b}{1} & \color{#ffd43b}{0} & \color{#f76707}{1} & \color{#f76707}{-1} \\"
        r"\color{#ffd43b}{0} & \color{#ffd43b}{1} & \color{#f76707}{1} & \color{#f76707}{1} \\"
        r"\color{#ffd43b}{0} & \color{#ffd43b}{0} & \color{#f76707}{0} & \color{#f76707}{0} \\"
        r"\color{#ffd43b}{0} & \color{#ffd43b}{0} & \color{#f76707}{0} & \color{#f76707}{0}"
        r"\end{bmatrix}"
    )
    st.markdown(
        "Call the row-weights y -- the amounts you multiply each row of A by. The "
        "reduced Aᵀ has pivots in columns 1 and 2 (yellow) and free columns 3 and 4 "
        "(orange). The two free columns give the two free weights y1 and y2, and each "
        "one produces a direction vector -- exactly the null-space recipe, now applied "
        "to Aᵀ. Those direction vectors, stacked, are the left null space:"
    )
    st.latex(_PARAMETRIC_LATEX)
    st.markdown(_VERIFY_TEXT)
    st.latex(_VERIFY_LATEX)
    st.markdown(_HOWTO_CAPTION)

    # Block 3 -- the four-subspaces picture (text only)
    st.markdown(_FOUR_SPACES_TEXT)

    # Block 4 -- closing text
    st.markdown(_CLOSING)
