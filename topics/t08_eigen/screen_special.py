"""Topic 8, Screen 0 -- The special directions."""
import math

import numpy as np
import streamlit as st

import engine.widgets as w
from engine import plotting as plot

A = np.array([[2.0, 1.0], [1.0, 2.0]])

_INTRO = """
When a matrix multiplies a vector, it moves it. Usually the output A·v points in a
DIFFERENT direction than v -- the matrix has swung it onto a new line. But for a few
special starting directions, something surprising happens: A·v comes out on the
SAME line as v, just longer or shorter. Those special directions are what this
whole topic is about. Let's hunt for them.
"""

_CAPTION = "Spin v. Most of the time A·v points elsewhere. Find the directions where it stays on v's line."

_REVEAL = """
Did you find them? For this matrix there are two special directions: along (1, 1)
and along (1, −1). On (1, 1) the matrix triples the vector; on (1, −1) it leaves it
unchanged. Every other direction gets swung away. Next we give these special
directions their names.
"""


def _clean(x, eps=0.005):
    v = round(float(x), 2)
    return 0.0 if abs(v) < eps else v


def _ang_dist(a, b):
    return abs((a - b + 180) % 360 - 180)


def render_special():
    # Block 1 -- the idea (text only)
    st.markdown(_INTRO)

    # Block 2 -- interactive: spin v, compare v and A·v
    angle = st.slider("Direction of v (degrees)", 0, 360, 20, key="t08_v_angle")
    rad = math.radians(angle)
    v = np.array([math.cos(rad), math.sin(rad)]) * 3
    Av = A @ v

    angle_v = angle % 360
    angle_av = math.degrees(math.atan2(Av[1], Av[0])) % 360
    diff = _ang_dist(angle_v, angle_av)
    aligned = diff < 3

    dist_pos = min(_ang_dist(angle_v, 45), _ang_dist(angle_v, 225))
    dist_neg = min(_ang_dist(angle_v, 135), _ang_dist(angle_v, 315))
    aligned_line = "pos" if dist_pos <= dist_neg else "neg"

    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        st.latex(
            r"v = " + w.bmatrix(v.reshape(-1, 1))
            + r" \qquad A v = " + w.bmatrix(Av.reshape(-1, 1))
        )
        if aligned:
            verdict = ("A·v is on the SAME line as v -- this is a special direction! "
                       "Here A just scales v.")
        else:
            verdict = "A·v landed on a different line -- v got swung away. Keep looking."
        st.markdown(
            f"v points at {_clean(angle_v):g} degrees. A·v points at {_clean(angle_av):g} "
            f"degrees. {verdict}"
        )
    with right:
        fig = plot.new_figure_2d(rng=7)
        pos_color = "#51cf66" if aligned and aligned_line == "pos" else "rgba(160,160,160,0.5)"
        neg_color = "#51cf66" if aligned and aligned_line == "neg" else "rgba(160,160,160,0.5)"
        plot.add_line_2d(fig, 1, -1, 0, pos_color, "reference line (1, 1)", rng=7)
        plot.add_line_2d(fig, 1, 1, 0, neg_color, "reference line (1, −1)", rng=7)
        plot.add_vector_2d(fig, (0, 0), (v[0], v[1]), "#4dabf7", "v")
        plot.add_vector_2d(fig, (0, 0), (Av[0], Av[1]), "#ffa94d", "A·v")
        st.plotly_chart(fig, use_container_width=True)
        st.caption(_CAPTION)

    # Block 3 -- the reveal (text only)
    st.markdown(_REVEAL)
