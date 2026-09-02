import streamlit as st

from .det_workbench import det_workbench, _det_load


# ---------------------------------------------------------------------------
# Screen 3 -- Determinant Calculation
# ---------------------------------------------------------------------------

_BLOCK1 = """
**Determinant Calculation.** The determinant is a single number you can compute
from a square matrix, and it tells you whether the matrix can be undone. When the
determinant is zero, the matrix squashes space flat and has no inverse; when it is
not zero, the matrix can be reversed. You met determinants back in Topic 3 -- this
screen is about how to actually calculate one, especially for big matrices.
"""

_BLOCK2_INTRO = """
Here are the formulas again from Topic 3. For a 2 by 2 matrix, multiply the two
numbers on the main diagonal and subtract the product of the other two. For a 3 by
3, there is a longer formula built from three smaller 2 by 2 determinants combined
with alternating plus and minus signs.
"""

_BLOCK2_OUTRO = """
The 3 by 3 formula is really just the 2 by 2 formula used three times. It works --
but notice it is already getting complicated, and this is only a 3 by 3.
"""

_BLOCK3 = """
The formula for the 3 by 3 came from a method called **cofactor expansion**: to
find the determinant, you break the matrix into smaller matrices, find their
determinants, and combine them. Those smaller matrices break into even smaller
ones, and so on. It always works -- but the amount of work explodes as the matrix
grows.

Here is how fast it explodes. A 3 by 3 needs about 6 steps. A 4 by 4 needs about
24. A 10 by 10 needs over 3 million. And a 20 by 20 matrix -- still small by
real-world standards -- needs about 2,400,000,000,000,000,000 steps (that is 2.4
quintillion). Even a computer doing a billion steps every second would take about
77 years to finish. Cofactor expansion is simply not usable for matrices of any
real size.
"""

_BLOCK4 = """
There is a far better way, and you already know most of it: **elimination** -- the
same row operations you used to solve systems. If you use elimination to turn the
matrix into upper-triangular form (all zeros below the diagonal), the determinant
is the product of the numbers left on the diagonal, with two small adjustments you
keep track of as you go. That same 20 by 20 matrix takes only about 2,600 steps
this way -- done instantly instead of in 77 years.

The two adjustments come from the row operations. Two of the three operations
change the determinant, so you track them:

- **Adding a multiple of one row to another does not change the determinant at
  all.** This is the workhorse move, and it is free.
- **Swapping two rows flips the sign of the determinant.** Every swap multiplies
  your answer by −1, so you count the swaps: an even number leaves the sign alone,
  an odd number flips it.
- **Multiplying a row by a number k multiplies the determinant by that same k.** So
  if you scale a row by k along the way, you divide your final answer by k to undo
  it.

Keep those three rules in mind and elimination gives you the determinant quickly,
even for enormous matrices.
"""

_BLOCK5_INTRO = """
**Try it: eliminate this 4 by 4 yourself.** The top-left entry is 0, so you
will need a row swap before you can clear the first column. Watch the
determinant tracker on the right: it counts your swaps and scaling, and when
you reach triangular form it multiplies the diagonal and applies the sign to
give the determinant. Reduce it to upper-triangular form and read off det = 8.
"""

_DET_A = [[0, 1, 1, 2], [1, 2, 3, 1], [2, 1, 1, 0], [1, 1, 2, 3]]

_BLOCK6 = """
So the determinant of a big matrix is not found by the textbook formula -- it is
found by elimination, reading the answer off the diagonal and adjusting for any
swaps and scaling. It is the same elimination you already know, doing a second job.
"""


def _bmat(rows, highlight_diag=False):
    """Bracketed LaTeX matrix from a grid of scalars/strings.

    highlight_diag: color the (i, i) diagonal entries amber, to match the
    pivot-highlight color used elsewhere.
    """
    line_strs = []
    for i, row in enumerate(rows):
        cells = []
        for j, v in enumerate(row):
            s = str(v)
            if highlight_diag and i == j:
                s = r"\color{#ffd43b}{" + s + "}"
            cells.append(s)
        line_strs.append(" & ".join(cells))
    return r"\begin{bmatrix}" + r" \\ ".join(line_strs) + r"\end{bmatrix}"


def render_determinant():
    st.markdown(_BLOCK1)

    st.markdown(_BLOCK2_INTRO)
    st.latex(
        r"\det" + _bmat([["a", "b"], ["c", "d"]])
        + r" = ad - bc \quad \text{(2D)}"
    )
    st.latex(
        r"\det" + _bmat([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]])
        + r" = a(ei - fh) - b(di - fg) + c(dh - eg) \quad \text{(3D)}"
    )
    st.markdown(_BLOCK2_OUTRO)

    st.markdown(_BLOCK3)
    st.markdown(
        "| Matrix size | Cofactor-expansion steps |\n"
        "|---|---|\n"
        "| 3x3 | ~6 |\n"
        "| 4x4 | ~24 |\n"
        "| 10x10 | ~3,600,000 |\n"
        "| 20x20 | ~2.4 quintillion (~77 years at 1B/sec) |"
    )

    st.markdown(_BLOCK4)

    st.markdown(_BLOCK5_INTRO)
    if st.session_state.get("t05b_det_last") is None:
        _det_load("t05b_det", _DET_A)
        st.session_state["t05b_det_last"] = "loaded"
    det_workbench("t05b_det", 4)

    st.markdown(_BLOCK6)
