"""Screen 1 -- What a vector space is (and what isn't one)."""
import streamlit as st

from engine.plotting import new_figure_2d, add_line_2d, add_point_2d, shade_polygon

_INTRO = """
A **vector space** is a collection of vectors with a "no escape" rule: add any
two vectors in the collection and the answer is still in the collection; stretch
or shrink any vector in it (multiply by any number) and the answer is still in
it. You cannot get out by combining what is inside.

Back in Topic 1, "span" meant everywhere you can reach by mixing some
ingredients. Every span automatically passes the no-escape rule -- a span is
always a vector space.
"""

_PASS_LEFT = """
- The whole 2D plane: add any two arrows, still in the plane; stretch any arrow,
  still in the plane. Passes.
- A straight line through the origin (use the line along (1, 2)): show
  (1,2) + (2,4) = (3,6) -- still on the line; 3·(1,2) = (3,6) -- still on the line.
  Passes.
"""

_FAIL_LEFT = """
**A line that misses the origin** (the line through (0,3) parallel to (1,0)):
multiply the vector (2,3) on it by 0 and you get (0,0) -- which is OFF the line.
Escaped. FAILS.

**The top-right quarter of the plane only:** multiply (2,1) by −1 and you get
(−2,−1) -- bottom-left. Escaped. FAILS.

Lesson: every vector space must contain the zero vector, because multiplying by
zero is always allowed.
"""

_CLOSING = """
Lines and planes through the origin, whole spaces, and every span you have ever
drawn -- those are vector spaces. The next three screens meet the three vector
spaces that live inside every matrix.
"""


def render_what():
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- examples that pass (math left, graph right)
    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        st.markdown(_PASS_LEFT)
    with right:
        fig = new_figure_2d(rng=8)
        add_line_2d(fig, 2, -1, 0, "#4dabf7", "line along (1, 2)")
        add_point_2d(fig, (1, 2), "#ffa94d", "(1, 2)")
        add_point_2d(fig, (2, 4), "#ffa94d", "(2, 4)")
        add_point_2d(fig, (3, 6), "#51cf66", "(3, 6)")
        st.plotly_chart(fig, use_container_width=True)

    # Block 3 -- examples that FAIL, and exactly where (math left, graph right)
    left2, right2 = st.columns([0.5, 0.5], gap="large")
    with left2:
        st.markdown(_FAIL_LEFT)
    with right2:
        fig2 = new_figure_2d(rng=8)
        shade_polygon(fig2, [(0, 0), (8, 0), (8, 8), (0, 8)],
                     "rgba(77,171,247,0.12)", "first quadrant")
        add_line_2d(fig2, 0, 1, 3, "#ff6b6b", "line through (0, 3) parallel to (1, 0)")
        add_point_2d(fig2, (2, 3), "#ffa94d", "(2, 3) -- on the line")
        add_point_2d(fig2, (0, 0), "#e6e6e6", "(0, 0) -- escaped, off the line")
        add_point_2d(fig2, (2, 1), "#51cf66", "(2, 1) -- inside")
        add_point_2d(fig2, (-2, -1), "#e6e6e6", "(−2, −1) -- escaped")
        st.plotly_chart(fig2, use_container_width=True)

    # Block 4 -- closing text
    st.markdown(_CLOSING)
