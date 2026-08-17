"""Screen 2 -- Projecting onto a plane."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from engine import plotting as plot

_INTRO = """
Same story, one dimension up. Now the thing you can reach is a whole PLANE through
the origin -- and from Topic 6 you know a plane like this is a **column space**
(all the combinations of a matrix's columns). The target b floats in 3D, usually
off the plane. The closest point is again b's perpendicular shadow, dropped
straight down onto the plane.

When b is off the plane, there is no exact solution to A·x = b -- but the shadow is
the closest we can get. That shadow is what "best answer" will mean.
"""

_SETUP_TEXT = """
The plane is spanned by two column vectors, a1 and a2. The target b sits off the
plane. Its shadow p is the closest point ON the plane, and the residual r = b − p
is what is left over.
"""

_MATH_LATEX = r"""
\begin{aligned}
a_1 &= (1,\ 0,\ 1) \\
a_2 &= (0,\ 1,\ 1) \\
b &= (1,\ 2,\ 4) \\
p &= \left(\tfrac{4}{3},\ \tfrac{7}{3},\ \tfrac{11}{3}\right) \\
r &= b - p = \left(-\tfrac{1}{3},\ -\tfrac{1}{3},\ \tfrac{1}{3}\right)
\end{aligned}
"""

_CHECK_TEXT = "Check: r · a1 = 0 and r · a2 = 0 -- perpendicular to the whole plane."

_GRAPH_CAPTION = (
    "The shadow on the plane is the closest point; the drop is perpendicular to "
    "the whole plane. Rotate to see it."
)

_CLOSING = """
Perpendicular to the whole plane means perpendicular to every direction in it -- to
each column. Turning that sentence into equations is the next screen, and it gives
the formula that runs everything.
"""


def render_plane():
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- the picture (math left, 3D graph right)
    a1 = np.array([1.0, 0.0, 1.0])
    a2 = np.array([0.0, 1.0, 1.0])
    b = np.array([1.0, 2.0, 4.0])
    p = np.array([4.0 / 3.0, 7.0 / 3.0, 11.0 / 3.0])
    r = b - p

    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        st.markdown(_SETUP_TEXT)
        st.latex(_MATH_LATEX)
        st.markdown(
            f"{_CHECK_TEXT} (r · a1 = {round(float(np.dot(r, a1)), 6)}, "
            f"r · a2 = {round(float(np.dot(r, a2)), 6)})"
        )
    with right:
        fig = plot.new_figure_3d(rng=5)
        plot.add_plane_3d(fig, -1, -1, 1, 0, "#4dabf7", "plane (a column space)", rng=5)
        plot._arrow3d(fig, a1, "#ff6b6b", "a1 = (1, 0, 1)")
        plot._arrow3d(fig, a2, "#51cf66", "a2 = (0, 1, 1)")
        fig.add_trace(go.Scatter3d(
            x=[b[0]], y=[b[1]], z=[b[2]], mode="markers",
            marker=dict(color="#ffa94d", size=6), name="b (target)",
        ))
        fig.add_trace(go.Scatter3d(
            x=[p[0]], y=[p[1]], z=[p[2]], mode="markers",
            marker=dict(color="#e6e6e6", size=6), name="shadow (closest point)",
        ))
        fig.add_trace(go.Scatter3d(
            x=[b[0], p[0]], y=[b[1], p[1]], z=[b[2], p[2]], mode="lines",
            line=dict(color="#ffa94d", width=5, dash="dash"), name="residual (dashed)",
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(_GRAPH_CAPTION)

    # Block 3 -- closing text
    st.markdown(_CLOSING)
