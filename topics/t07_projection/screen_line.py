"""Screen 1 -- Projecting onto a line."""
import numpy as np
import streamlit as st

from engine import plotting as plot

_INTRO = """
You have a target point b and a line through the origin (all the multiples of one
direction vector a). The line is everything you can reach; b is usually NOT on it.
The question: which point ON the line is CLOSEST to b?

The answer is b's **shadow** on the line -- drop straight down from b onto the
line at a right angle. That closest point is called the **projection** of b onto
the line. The little arrow from the shadow up to b is the **residual** (the
leftover), and it is perpendicular to the line.
"""

_GRAPH_CAPTION = "The shadow is the closest point; the dashed drop is perpendicular."

_DERIVATION_TEXT = """
**Step 1 -- the shadow is some amount of a.** The closest point sits on the line,
so it is a scalar multiple of the direction: p = c·a, for some number c we must
find.

**Step 2 -- the leftover is perpendicular to the line.** The residual r = b − p
must be perpendicular to a. From Screen 0, perpendicular means the dot product is
zero: a · (b − p) = 0.

**Step 3 -- substitute p = c·a and solve for c.** a · (b − c·a) = 0, so
a·b − c(a·a) = 0, which gives **c = (a·b) / (a·a)**.

**Step 4 -- the projection.** p = c·a = ((a·b)/(a·a)) · a.
"""

_CLOSING = """
That single number c measures how much of b points along the line. The projection
is the closest reachable point, found purely by the perpendicular rule. Next: the
same idea when the line becomes a whole plane.
"""


def _clean(x, eps=0.005):
    v = round(float(x), 2)
    return 0.0 if abs(v) < eps else v


def render_line():
    # Block 1 -- the setup (text only)
    st.markdown(_INTRO)

    # Block 2 -- interactive: drag the target, see its shadow
    bx = st.slider("Target b, x", -6, 6, 2, key="t07_line_bx")
    by = st.slider("Target b, y", -6, 6, 5, key="t07_line_by")
    a = np.array([3.0, 1.0])
    b = np.array([float(bx), float(by)])
    c = np.dot(a, b) / np.dot(a, a)
    p = c * a
    r = b - p
    dot_ra = np.dot(r, a)

    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        st.latex(
            r"\begin{aligned}"
            rf"p &= {_clean(c)}\cdot a = ({_clean(p[0])},\ {_clean(p[1])}) "
            r"\quad \text{(the shadow)} \\"
            rf"r &= b - p = ({_clean(r[0])},\ {_clean(r[1])}) "
            r"\quad \text{(the leftover, perpendicular to the line)}"
            r"\end{aligned}"
        )
        st.markdown(f"Check: r · a = {_clean(dot_ra)} ≈ 0.")
    with right:
        fig = plot.new_figure_2d(rng=7)
        plot.add_line_2d(fig, 1, -3, 0, "#4dabf7", "the line (multiples of a)", rng=7)
        plot.add_point_2d(fig, (b[0], b[1]), "#ff6b6b", "b (target)")
        plot.add_point_2d(fig, (p[0], p[1]), "#51cf66", "shadow (closest point)")
        plot.add_vector_2d(fig, (p[0], p[1]), (b[0], b[1]), "#ffa94d",
                           "residual (perpendicular)", dash="dash")
        r_norm = np.linalg.norm(r)
        a_unit = a / np.linalg.norm(a)
        if r_norm > 1e-6:
            r_unit = r / r_norm
        else:
            r_unit = np.array([-a_unit[1], a_unit[0]])
        s = 0.4
        corner = p + s * a_unit + s * r_unit
        plot.add_vector_2d(fig, p + s * a_unit, corner, "#e6e6e6", "right angle",
                           arrow=False, showlegend=False)
        plot.add_vector_2d(fig, p + s * r_unit, corner, "#e6e6e6", "right angle",
                           arrow=False, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.caption(_GRAPH_CAPTION)

    # Block 3 -- derive the projection formula (math left, no graph)
    st.markdown(_DERIVATION_TEXT)
    st.latex(
        r"\begin{aligned}"
        rf"c &= \frac{{a \cdot b}}{{a \cdot a}} = {_clean(c)} \\"
        rf"p &= c\cdot a = ({_clean(p[0])},\ {_clean(p[1])})"
        r"\end{aligned}"
    )

    # Block 4 -- closing text
    st.markdown(_CLOSING)
