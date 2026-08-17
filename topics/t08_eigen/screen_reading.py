"""Topic 8, Screen 4 -- What eigenvalues tell you."""
import streamlit as st

from engine import plotting as plot

_RULES = """
The eigenvalue λ tells you what the matrix does along its special direction:
λ greater than 1 STRETCHES; λ between 0 and 1 SHRINKS; λ = 1 leaves it UNCHANGED;
λ negative FLIPS it to the opposite side (and stretches by the size of λ). Here is
a gallery.
"""

_B2_TEXT = """
Along (1,0) the eigenvalue is 2 -- it stretches to double.
Along (0,1) the eigenvalue is 0.5 -- it shrinks to half.
"""

_B3_TEXT = """
Along (1,0) the eigenvalue is −1 -- the vector flips to the
opposite side. Along (0,1) the eigenvalue is +1 -- unchanged. This matrix is a mirror
reflection.
"""

_B4_TEXT = """
Not every matrix has real special directions. A rotation turns EVERY vector onto a
new line -- nothing stays put, so there are no real eigenvectors at all. (There is
still an answer, but it uses a new kind of number -- the "imaginary" numbers -- which
is exactly where the next topic, Topic 9, begins.)
"""

_B4_CAPTION = "A pure rotation: every arrow turns, none stays on its line."

_CLOSING = """
Stretch, shrink, flip, or turn -- the eigenvalues read out a matrix's whole
personality. Last screen: one place this pays off spectacularly -- predicting
weather in the long run.
"""


def render_reading():
    # Block 1 -- reading an eigenvalue (text only)
    st.markdown(_RULES)

    # Block 2 -- stretch and shrink (math left, graph right)
    left2, right2 = st.columns([0.5, 0.5], gap="large")
    with left2:
        st.markdown(_B2_TEXT)
    with right2:
        fig2 = plot.new_figure_2d(rng=4)
        plot.add_vector_2d(fig2, (0, 0), (1, 0), "#4dabf7", "(1, 0)")
        plot.add_vector_2d(fig2, (0, 0), (2, 0), "#51cf66", "(2, 0), λ = 2", dash="dot")
        plot.add_vector_2d(fig2, (0, 0), (0, 1), "#ffa94d", "(0, 1)")
        plot.add_vector_2d(fig2, (0, 0), (0, 0.5), "#e6e6e6", "(0, 0.5), λ = 0.5", dash="dot")
        st.plotly_chart(fig2, use_container_width=True)

    # Block 3 -- flip (math left, graph right)
    left3, right3 = st.columns([0.5, 0.5], gap="large")
    with left3:
        st.markdown(_B3_TEXT)
    with right3:
        fig3 = plot.new_figure_2d(rng=4)
        plot.add_vector_2d(fig3, (0, 0), (1, 0), "#4dabf7", "(1, 0)")
        plot.add_vector_2d(fig3, (0, 0), (-1, 0), "#51cf66", "(−1, 0), λ = −1")
        plot.add_vector_2d(fig3, (0, 0), (0, 1), "#ffa94d", "(0, 1)")
        plot.add_vector_2d(fig3, (0, 0), (0, 1), "#e6e6e6", "(0, 1), λ = 1", dash="dot")
        st.plotly_chart(fig3, use_container_width=True)

    # Block 4 -- the honest exception: no real eigenvectors (math left, graph right)
    left4, right4 = st.columns([0.5, 0.5], gap="large")
    with left4:
        st.markdown(_B4_TEXT)
    with right4:
        fig4 = plot.new_figure_2d(rng=4)
        plot.add_vector_2d(fig4, (0, 0), (1, 0.4), "#4dabf7", "v1")
        plot.add_vector_2d(fig4, (0, 0), (-0.4, 1), "#51cf66", "A·v1")
        plot.add_vector_2d(fig4, (0, 0), (-0.8, 0.6), "#ffa94d", "v2")
        plot.add_vector_2d(fig4, (0, 0), (-0.6, -0.8), "#e6e6e6", "A·v2")
        st.plotly_chart(fig4, use_container_width=True)
        st.caption(_B4_CAPTION)

    # Block 5 -- closing (text only)
    st.markdown(_CLOSING)
