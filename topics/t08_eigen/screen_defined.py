"""Topic 8, Screen 1 -- Eigenvector & eigenvalue defined."""
import streamlit as st

from engine import plotting as plot

_DEFINITIONS = """
A special direction where A·v stays on the same line as v is called an
**eigenvector** of A. The number that tells you how much it got stretched is the
**eigenvalue**, written with the Greek letter lambda (λ). The whole idea fits in
one short equation:

**A·v = λ·v** -- "the matrix acting on the eigenvector v is the same as just
multiplying v by the number λ." ("Eigen" is German for "own" -- these are the
matrix's own special directions.)
"""

_FIRST_EIGENVECTOR = """
**First eigenvector.** A·(1,1) = (3,3) = 3·(1,1). Same direction, tripled. So
(1,1) is an eigenvector with eigenvalue λ = 3.
"""

_SECOND_EIGENVECTOR = """
**Second eigenvector.** A·(1,−1) = (1,−1) = 1·(1,−1). Same direction, unchanged. So
(1,−1) is an eigenvector with eigenvalue λ = 1.
"""

_CAPTION = "Each eigenvector stays on its own line; the eigenvalue is how much it stretched."

_CLOSING = """
That is the definition. But we were handed the eigenvectors -- how would you FIND
them for a matrix you have never seen? The next two screens show the method:
first the eigenvalues, then the eigenvectors.
"""


def render_defined():
    # Block 1 -- the definitions (text only)
    st.markdown(_DEFINITIONS)

    # Block 2 -- the two eigenvectors, shown (math left, graph right)
    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        st.markdown(_FIRST_EIGENVECTOR)
        st.markdown(_SECOND_EIGENVECTOR)
    with right:
        fig = plot.new_figure_2d(rng=7)
        plot.add_line_2d(fig, 1, -1, 0, "rgba(160,160,160,0.5)", "line through (1, 1)", rng=7)
        plot.add_line_2d(fig, 1, 1, 0, "rgba(160,160,160,0.5)", "line through (1, −1)", rng=7)
        plot.add_vector_2d(fig, (0, 0), (1, 1), "#4dabf7", "v = (1, 1)")
        plot.add_vector_2d(fig, (0, 0), (3, 3), "#51cf66", "A·v = (3, 3), λ = 3")
        plot.add_vector_2d(fig, (0, 0), (1, -1), "#ffa94d", "v = (1, −1)")
        plot.add_vector_2d(fig, (0, 0), (1, -1), "#e6e6e6", "A·v = (1, −1), λ = 1",
                           width=2, dash="dot")
        st.plotly_chart(fig, use_container_width=True)
        st.caption(_CAPTION)

    # Block 3 -- closing (text only)
    st.markdown(_CLOSING)
