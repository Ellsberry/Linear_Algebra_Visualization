"""
Topic 1 -- Vectors & Combinations.

Pattern: MULTI-EXAMPLE. A top selector chooses Example 1/2/3; only the chosen
example's text, inputs, and visual render, so the student sees just the lesson
being discussed. The Overview is pinned at the top; "How to use" is a collapsed
expander. Contrast with Topic 2 (single surface + presets).
"""
import numpy as np
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

TITLE = "1 · Vectors & Combinations"
SLUG = "vectors"

VIEW = 12  # nutrition numbers run larger than the transformation topics

OVERVIEW = """
You already know a vector is an arrow with a direction and a length — or a list
of numbers like (3, 2). This module is about what happens when you start
*combining* vectors: adding them and scaling them. That one move is what almost
all of linear algebra is built on. By the end you'll own three words that show
up everywhere later — **linear combination**, **span**, and **basis** — and
we'll build all three with smoothies.

The setup we'll use the whole way through: each ingredient is a vector of two
numbers, its *(protein, sugar)* per scoop. A smoothie is just a mix — some
scoops of this, some scoops of that — and that mix *is* a linear combination.
Watching the result move as you change the scoops is the entire idea.

The question we keep circling — which combinations of your vectors can reach a
given target? — is the central one of the whole course. You'll meet it soon
written as **Ax = b**. For now, just build the intuition with smoothies.
"""

HOWTO = """
- The **left panel** is the numbers: the ingredient vectors and the sliders for
  how many scoops of each.
- The **right panel** is the picture: every vector is an arrow from the origin,
  drawn on the protein (→) and sugar (↑) axes.
- Change a number or drag a slider and the picture updates instantly. Nothing's
  hidden — open **Show the math** anytime to see the arithmetic behind the arrows.
- Use the **Example** selector to jump between the three setups, and **Reset**
  to start over.
"""

BANANA = np.array([1.0, 4.0])
PEANUT = np.array([8.0, 2.0])
PROTEIN_AXIS = "protein →"
SUGAR_AXIS = "sugar ↑"


# Shared constants are defined above; submodules import them via
# `from . import BANANA, PROTEIN_AXIS, SUGAR_AXIS, VIEW` etc.
from .example_one import _example_one
from .example_two import _example_two
from .example_three import _example_three


# ----------------------------------------------------------------------------
# Top-level render
# ----------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)
    with st.expander("How to use this screen"):
        st.markdown(HOWTO)

    example = st.radio(
        "Example",
        ["1 · One ingredient", "2 · Two ingredients, added", "3 · The smoothie mixer"],
        horizontal=True, key="t01_example",
    )
    st.divider()

    if example.startswith("1"):
        _example_one()
    elif example.startswith("2"):
        _example_two()
    else:
        _example_three()
