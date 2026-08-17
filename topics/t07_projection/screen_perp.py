"""Screen 0 -- Perpendicular means dot product zero."""
import math

import streamlit as st

from engine import plotting as plot

_INTRO = """
You already know the **dot product**: multiply two vectors component by component
and add. For (a1, a2) and (b1, b2) it is a1·b1 + a2·b2 -- a single number.

Here is the fact this whole topic is built on: **two vectors are perpendicular
(at a right angle, 90 degrees) exactly when their dot product is zero.** Not
close to zero -- exactly zero. Turn one vector until it makes a right angle with
the other, and the dot product lands on 0 at that precise moment.
"""

_CAPTION = "Slide to 90 degrees and watch the dot product hit exactly zero."

_CHECK1_TEXT = """
**Perpendicular pair:** (3, 0) and (0, 2). Dot product 3·0 + 0·2 = 0. Right angle. ✓
"""

_CHECK1_LATEX = r"""
\begin{aligned}
(3, 0) \cdot (0, 2) &= 3\cdot 0 + 0\cdot 2 = 0
\end{aligned}
"""

_CHECK2_TEXT = """
**Another perpendicular pair (tilted):** (2, 1) and (−1, 2). Dot product
2·(−1) + 1·2 = 0. Also a right angle. ✓
"""

_CHECK2_LATEX = r"""
\begin{aligned}
(2, 1) \cdot (-1, 2) &= 2\cdot(-1) + 1\cdot 2 = 0
\end{aligned}
"""

_CHECK3_TEXT = """
**Not perpendicular:** (2, 1) and (1, 1). Dot product 2·1 + 1·1 = 3, not zero -- so
not a right angle.
"""

_CHECK3_LATEX = r"""
\begin{aligned}
(2, 1) \cdot (1, 1) &= 2\cdot 1 + 1\cdot 1 = 3
\end{aligned}
"""

_CLOSING = """
Keep this one fact in your pocket: perpendicular means dot product zero. Every
screen from here on uses it to find the closest point.
"""


def render_perp():
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- interactive: rotate a vector, watch the dot product
    angle = st.slider("Angle of the blue vector (degrees)", 0, 180, 30, key="t07_angle")
    rad = math.radians(angle)
    vx, vy = 3 * math.cos(rad), 3 * math.sin(rad)
    dot = 3 * vx + 0 * vy
    if abs(dot) < 0.05:
        dot = 0.0

    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        st.latex(rf"u \cdot v = 3\cdot({vx:.2f}) + 0\cdot({vy:.2f}) = {dot:.2f}")
        if abs(dot) < 0.05:
            verdict = "That's a right angle -- and the dot product is zero. Perpendicular."
        elif dot > 0:
            verdict = ("The vectors lean the same way (less than 90 degrees apart), "
                      "so the dot product is positive.")
        else:
            verdict = ("The vectors lean apart (more than 90 degrees), so the dot "
                      "product is negative.")
        st.markdown(f"Right now the angle is {angle} degrees and the dot product "
                    f"is {dot:.2f}. {verdict}")
    with right:
        fig = plot.new_figure_2d(rng=4)
        perpendicular = abs(angle - 90) < 2
        v_color = "#51cf66" if perpendicular else "#4dabf7"
        v_name = "v (perpendicular)" if perpendicular else "v"
        plot.add_vector_2d(fig, (0, 0), (3, 0), "#ff6b6b", "u")
        plot.add_vector_2d(fig, (0, 0), (vx, vy), v_color, v_name)
        if perpendicular:
            s = 0.4
            u_dir = (1.0, 0.0)
            v_dir = (vx / 3.0, vy / 3.0)
            corner = (s * u_dir[0] + s * v_dir[0], s * u_dir[1] + s * v_dir[1])
            plot.add_vector_2d(fig, (s * u_dir[0], s * u_dir[1]), corner,
                               "#e6e6e6", "right angle", arrow=False, showlegend=False)
            plot.add_vector_2d(fig, (s * v_dir[0], s * v_dir[1]), corner,
                               "#e6e6e6", "right angle", arrow=False, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.caption(_CAPTION)

    # Block 3 -- three quick checks (math left, no graph)
    st.markdown(_CHECK1_TEXT)
    st.latex(_CHECK1_LATEX)
    st.markdown(_CHECK2_TEXT)
    st.latex(_CHECK2_LATEX)
    st.markdown(_CHECK3_TEXT)
    st.latex(_CHECK3_LATEX)

    # Block 4 -- closing text
    st.markdown(_CLOSING)
