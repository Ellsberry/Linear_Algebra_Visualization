"""Screen 8 -- The four spaces of a transformation."""
import streamlit as st

from engine import plotting as plot

_INTRO = """
Back in Topic 2 you watched matrices transform space -- rotating, shearing,
scaling, or flattening it. Now you can ask a sharp question about each one: does it
LOSE any information? The four spaces answer it. If a transformation can be undone,
nothing is lost: it reaches the whole plane (its column space is everything) and
only the zero vector maps to zero (its null space is just the origin). If it
flattens space, information is lost: a whole line of inputs gets crushed to zero.
Here are five transformations from Topic 2, sorted by that question.
"""

_INVERTIBLE_LEADIN = """
**Four that lose nothing: identity, rotation, shear, and scale.** Each of these can
be undone (each has an inverse), and all four tell the same four-space story:
- **Column space = the whole plane.** Their two columns point in different
  directions, so mixing them reaches every point in 2D. Every target is reachable.
- **Null space = just the origin.** Nothing except the zero vector gets sent to
  zero -- no information is crushed.
- **Row space = the whole plane** as well, and the **left null space = just the
  origin**. Full rank (2), zero free variables: 2 + 0 = 2.
"""

_INVERTIBLE_CAPTION = (
    "All four fill the plane and crush nothing -- that is exactly what makes them "
    "invertible."
)

_TRANSFORMS = [
    ("Identity", r"\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}", (1, 0), (0, 1)),
    ("Rotation 90", r"\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}", (0, 1), (-1, 0)),
    ("Shear", r"\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}", (1, 0), (1, 1)),
    ("Scale x2", r"\begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}", (2, 0), (0, 2)),
]

_COLLAPSE_TEXT = """
**One that loses information: the collapse.** The matrix [[1,2],[2,4]] has a second
column that is just twice the first, so it flattens the whole plane onto a single
line. Watch what happens to its four spaces:
- **Column space = a line** (along (1, 2)). Everything the matrix produces lands on
  this one line -- most of the plane is now unreachable.
- **Null space = a line** (along (-2, 1)). A WHOLE line of inputs gets crushed to
  zero -- that is the information being lost. (This is why a singular matrix has no
  inverse: once a line is crushed to a point, you cannot undo it.)
- Rank 1, one free variable: 1 + 1 = 2. The column space (1 dimension) plus the
  null space (1 dimension) still account for all of 2D.
"""

_LESSON = """
Here is the whole point, tying three topics together: a transformation is
**invertible** exactly when it loses nothing -- when its column space is the whole
space and its null space is just the origin (Topic 4's "the determinant is not
zero" is the same fact). The moment a transformation crushes even one line to zero,
its null space grows, its column space shrinks, and it can no longer be undone. The
four spaces are the complete report card on what a matrix does -- and whether you
can get back what you started with.
"""


def render_transforms():
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- the invertible four (grouped; small graphs)
    st.markdown(_INVERTIBLE_LEADIN)
    cols = st.columns(4)
    for col, (label, latex, c1, c2) in zip(cols, _TRANSFORMS):
        with col:
            st.markdown(f"**{label}**")
            st.latex(latex)
            fig = plot.new_figure_2d(rng=3, height=260)
            plot.shade_polygon(fig, [(-3, -3), (3, -3), (3, 3), (-3, 3)],
                               "rgba(32,201,151,0.12)")
            plot.add_vector_2d(fig, (0, 0), c1, "#ff6b6b", "column 1", showlegend=False)
            plot.add_vector_2d(fig, (0, 0), c2, "#4dabf7", "column 2", showlegend=False)
            plot.add_point_2d(fig, (0, 0), "#ffd43b", "null space = just this point")
            st.plotly_chart(fig, width="stretch")
    st.caption(_INVERTIBLE_CAPTION)

    # Block 3 -- the collapse (singular; full treatment, graph)
    st.markdown("---")
    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        st.markdown(_COLLAPSE_TEXT)
    with right:
        fig2 = plot.new_figure_2d(rng=8)
        plot.add_line_2d(fig2, 2, -1, 0, "#4dabf7", "column space -- everything lands here")
        plot.add_line_2d(fig2, 1, 2, 0, "#ffa94d", "null space -- crushed to zero")
        plot.add_point_2d(fig2, (1, 2), "#51cf66", "A·(1, 0) lands on (1, 2)")
        plot.add_point_2d(fig2, (2, 4), "#51cf66", "A·(0, 1) lands on (2, 4)")
        st.plotly_chart(fig2, width="stretch")

    # Block 4 -- the lesson (text only)
    st.markdown(_LESSON)
