"""Screen 1 -- What a vector space is (and what isn't one)."""
import numpy as np
import streamlit as st

import engine.widgets as w
from engine.plotting import (
    new_figure_2d, add_vector_2d, add_point_2d, shade_polygon, add_line_2d,
)

_INTRO = """
A **vector space** is a collection of vectors with a "no escape" rule: add any
two vectors in the collection and the answer is still in the vector space;
stretch or shrink any vector in it (multiply by any number) and the answer is
still in it. You cannot get out by combining what is inside.

Back in Topic 1, "span" meant everywhere you can reach by mixing vectors — using
any amounts, including negative ones and zero. Every span passes the no-escape
rule, so a span is always a vector space.
"""

_PLANE_LEFT = """
**The whole x-y plane is a vector space.** Every point on the screen counts. Pick
any two arrows — say (3, 1) and (1, 2). Add them tip-to-tail and you get (4, 3).
That result is still just a point on the x-y plane. Stretch any arrow longer or
shorter and it's still on the plane. There is nowhere off the plane to land, so
you can never escape.
"""

_LINE_LEFT = """
**A straight line through the origin** — the graph shows the line that runs
through (0,0) in the direction of the arrow (1, 2). Watch two things happen right
on that line:
- **Adding stays on the line.** The point (1, 2) and the point (2, 4) are both on
  it. Add them: (1, 2) + (2, 4) = (3, 6) — and (3, 6) is also on the line (it's
  just farther out). The dots on the graph are these three points; they all sit on
  the same line.
- **Stretching stays on the line.** Take (1, 2) and triple it: 3·(1, 2) = (3, 6) —
  still on the line.

No matter how you add or stretch points on this line, you land back on the line.
It passes the no-escape rule, so a line through the origin is a vector space.
"""

_FAIL_LEFT = """
**A line that misses the origin fails.** Take the specific line through (0, 3)
that runs flat (parallel to the x-axis). The point (2, 3) sits on it. Now
multiply that point by 0 — you're always allowed to multiply by any number,
including zero — and you get (0, 0). But (0, 0) is not on this line; the line
never touches the origin. You escaped, so this line fails the no-escape rule.
(The reason is always the same: multiplying any vector by 0 gives the zero
vector, so a vector space has to contain (0, 0) — and a line that misses the
origin can't.)

**The top-right quarter of the plane fails.** Take just the first quadrant (both
coordinates positive). The point (2, 1) is in it. Multiply by −1 and you get
(−2, −1) — down in the bottom-left, outside the quarter. Escaped. Fails.

**The smoothie mix from Topic 1 fails too.** Mixing ingredients only used
positive amounts — you can't have negative banana — so it only ever filled that
same first-quarter corner. Multiply a mix by −1 and you'd need negative smoothie,
which escapes. That's exactly why smoothie-mixing was never a vector space, even
though a true span (any amounts allowed) always is.

**The rule underneath all three:** every vector space must contain the zero
vector, because multiplying by zero is always allowed. Miss the origin, and you
fail.
"""

_CLOSING = """
Lines and planes through the origin, whole spaces, and every span you have ever
drawn — those are vector spaces. The next three screens meet the three vector
spaces that live inside every matrix.
"""


def render_what():
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2a -- the whole x-y plane (math left, graph right)
    left_a, right_a = st.columns([0.5, 0.5], gap="large")
    with left_a:
        st.markdown(_PLANE_LEFT)
        st.latex(
            w.bmatrix(np.array([3.0, 1.0]).reshape(-1, 1))
            + " + "
            + w.bmatrix(np.array([1.0, 2.0]).reshape(-1, 1))
            + " = "
            + w.bmatrix(np.array([4.0, 3.0]).reshape(-1, 1))
        )
    with right_a:
        fig_a = new_figure_2d(rng=6)
        shade_polygon(fig_a, [(-6, -6), (6, -6), (6, 6), (-6, 6)],
                     "rgba(77,171,247,0.08)", "the whole plane")
        add_vector_2d(fig_a, (0, 0), (3, 1), "#ff6b6b", "(3, 1)")
        add_vector_2d(fig_a, (3, 1), (4, 3), "#4dabf7", "(1, 2)")
        add_vector_2d(fig_a, (0, 0), (4, 3), "#51cf66", "sum (4, 3)", dash="dash")
        st.plotly_chart(fig_a, use_container_width=True)

    # Block 2b -- a straight line through the origin (math left, graph right)
    left_b, right_b = st.columns([0.5, 0.5], gap="large")
    with left_b:
        st.markdown(_LINE_LEFT)
        st.latex(
            w.bmatrix(np.array([1.0, 2.0]).reshape(-1, 1))
            + " + "
            + w.bmatrix(np.array([2.0, 4.0]).reshape(-1, 1))
            + " = "
            + w.bmatrix(np.array([3.0, 6.0]).reshape(-1, 1))
            + r"\qquad 3\cdot"
            + w.bmatrix(np.array([1.0, 2.0]).reshape(-1, 1))
            + " = "
            + w.bmatrix(np.array([3.0, 6.0]).reshape(-1, 1))
        )
    with right_b:
        fig_b = new_figure_2d(rng=8)
        add_line_2d(fig_b, 2, -1, 0, "#4dabf7", "line along (1, 2)")
        add_point_2d(fig_b, (0, 0), "#e6e6e6", "origin")
        add_point_2d(fig_b, (1, 2), "#ffa94d", "(1, 2)")
        add_point_2d(fig_b, (2, 4), "#ffa94d", "(2, 4)")
        add_point_2d(fig_b, (3, 6), "#51cf66", "(3, 6)")
        st.plotly_chart(fig_b, use_container_width=True)

    # Block 3 -- examples that FAIL, and exactly where (math left, graph right)
    left_c, right_c = st.columns([0.5, 0.5], gap="large")
    with left_c:
        st.markdown(_FAIL_LEFT)
    with right_c:
        fig_c = new_figure_2d(rng=8)
        shade_polygon(fig_c, [(0, 0), (8, 0), (8, 8), (0, 8)],
                     "rgba(77,171,247,0.12)", "first quadrant (also the smoothie mix)")
        add_line_2d(fig_c, 0, 1, 3, "#ff6b6b", "line through (0, 3) parallel to (1, 0)")
        add_point_2d(fig_c, (2, 3), "#ffa94d", "(2, 3) -- on the line")
        add_point_2d(fig_c, (0, 0), "#e6e6e6", "(0, 0) -- escaped, off the line")
        add_point_2d(fig_c, (2, 1), "#51cf66", "(2, 1) -- inside")
        add_point_2d(fig_c, (-2, -1), "#e6e6e6", "(−2, −1) -- escaped")
        st.plotly_chart(fig_c, use_container_width=True)

    # Block 4 -- closing text
    st.markdown(_CLOSING)
