"""Screen 5 -- Where this lives in the real world."""
import streamlit as st

_GPS_TEXT = """
**GPS.** Your phone hears from several satellites, each giving a distance. Three
would be enough for a perfect fix -- but your phone usually hears from many more,
and the numbers never agree exactly (signals bounce, clocks drift). That is an
over-crowded system with no exact solution -- exactly the case this topic solves.
GPS uses least squares to find the position closest to satisfying ALL the
measurements at once. The little leftover in each signal is a residual, made as
small as possible.
"""

_CAMERAS_TEXT = """
**Cameras and computer vision.** When your phone stitches a panorama or tracks a
face, it matches hundreds of points between images. The points are noisy and never
line up perfectly, so the software fits the best transformation by least squares --
the same AᵀA·x-hat = Aᵀb -- minimizing the total leftover. Best-fit, not exact,
because exact is impossible with real measurements.
"""

_BIG_PICTURE_TEXT = """
The pattern is always the same: more measurements than unknowns, no exact answer,
so find the one that comes closest -- the perpendicular shadow, the projection, the
least-squares fit. From a drink warming on a counter to a phone finding itself on
Earth, "closest when you can't be exact" is one of the most useful ideas in all of
mathematics.
"""

_CLOSING = """
You have now turned "no solution" into "best solution." Next comes a different
question about a matrix: are there special directions it only stretches, never
turns? Those are eigenvectors -- the heart of the next topic.
"""


def render_world():
    # Block 1 -- GPS (text only)
    st.markdown(_GPS_TEXT)

    # Block 2 -- cameras and computer vision (text only)
    st.markdown(_CAMERAS_TEXT)

    # Block 3 -- the big picture (text only)
    st.markdown(_BIG_PICTURE_TEXT)

    # Block 4 -- closing bridge (text only)
    st.markdown(_CLOSING)
