"""
Topic 2 -- Linear Transformations: a matrix is a function that moves space.

This module is the template for every other topic. To add a new topic, copy
this file, change TITLE / SLUG / INTRO, the PRESETS, and the body of render().
Reuse engine.widgets and engine.plotting so the look and behaviour stay
consistent.
"""
import streamlit as st

TITLE = "2 · Linear Transformations"
SLUG = "transformations"

INTRO = """
Throughout this course we'll keep meeting the equation **Ax = b**. Here's the
first piece of it. The matrix **A** is a function that transforms space. Apply it
to a vector **x** — written **A·x**, the matrix on the left acting on x — and out
comes a new vector, the result **b**. So **Ax = b** just says "apply A to x, and
you land on b." Right now we're exploring that forward action — *what A does to
x*. Later we'll turn it around and ask the harder question: given b, which x gets
you there?

Two words we'll use a lot:
- A **vertex** is a corner of the shape — a specific point, like a corner of the
  parallelogram below. "Vertex" is the geometry word.
- A **vector** is the arrow from the origin to that point — the column of numbers
  you actually multiply by A. "Vector" is the algebra word.

These are two views of the same thing: **every corner of a shape is described by
a vector**, and that's exactly why a matrix can transform a shape — it multiplies
the vector of each corner, and the corners move.

The two vectors that build every other vector are the x-direction vector (one step
right, written (1, 0)) and the y-direction vector (one step up, written (0, 1)).
Every point on the grid is just some amount of the x-direction vector plus some
amount of the y-direction vector -- so if you know where those two land after a
transformation, you know where everything lands. And the columns of A tell you
exactly that: the first column is where the x-direction vector lands, the second
column is where the y-direction vector lands. For example, Scale x2 sends the
x-direction vector to (2, 0) and the y-direction vector to (0, 2), so the whole
shape doubles in size. Pick a preset below (or choose Custom to set the four
entries yourself) and watch the parallelogram transform.
"""

from .screen_2d import _render_2d
from .screen_3d import _render_3d


def render():
    screen = st.radio(
        "Example",
        ["1 · 2D (parallelogram / rocket)", "2 · 3D (cube)"],
        horizontal=True,
        key="t02_screen",
    )

    if screen.startswith("1"):
        _render_2d()
    else:
        _render_3d()
