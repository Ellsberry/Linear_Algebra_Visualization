"""Example 1 -- One ingredient (a vector is already a recipe)."""
import numpy as np
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

from . import BANANA, PEANUT, PROTEIN_AXIS, SUGAR_AXIS, VIEW

_ING = {
    "Banana": dict(
        vec=BANANA, name="banana", color="darkorange", faint="rgba(180,140,0,0.45)",
        own_ratio="4×", other_name="peanut butter",
        other_line="sugar = ¼·protein",
    ),
    "Peanut butter": dict(
        vec=PEANUT, name="peanut butter", color="sienna", faint="rgba(160,82,45,0.45)",
        own_ratio="¼×", other_name="banana",
        other_line="sugar = 4·protein",
    ),
}


def _example_one():
    st.markdown(
        "**One ingredient.** The goal: a smoothie with a target amount of "
        "protein and sugar. Your ingredients are banana and peanut butter. "
        "Each ingredient is a vector -- (protein, sugar) per scoop. Banana "
        "is (1, 4). Peanut butter is (8, 2). This screen uses one "
        "ingredient at a time."
    )

    ingredient = st.radio("Ingredient", list(_ING), horizontal=True,
                         key="t01e1_ingredient")
    info = _ING[ingredient]
    vec, name = info["vec"], info["name"]

    if st.session_state.get("t01e1_ing_last") != ingredient:
        st.session_state["t01e1_c"] = 1.0
        st.session_state["t01e1_ing_last"] = ingredient

    c = w.scalar_slider("t01e1_c", f"Scoops of {name}", -3.0, 5.0, 1.0, step=0.25)
    show_break = st.checkbox("Show the recipe breakdown", key="t01e1_break")
    show_span = st.checkbox("Show the span line", key="t01e1_span")

    end = c * vec

    left, right = st.columns([0.5, 0.5], gap="large")

    with right:
        fig = plot.new_figure_2d(VIEW, PROTEIN_AXIS, SUGAR_AXIS)
        if show_span:
            plot.add_line_2d(fig, vec[1], -vec[0], 0, "rgba(200,200,200,0.35)",
                             f"span of {name}", rng=VIEW)
        plot.add_vector_2d(fig, [0, 0], vec, info["faint"],
                           f"{name} (1 scoop)", dash="dot")
        plot.add_vector_2d(fig, [0, 0], end, info["color"], f"{c:g} scoops")
        if show_break:
            plot.add_vector_2d(fig, [0, 0], [end[0], 0], "crimson",
                               "protein part", dash="dash", arrow=False)
            plot.add_vector_2d(fig, [end[0], 0], end, "royalblue",
                               "sugar part", dash="dash", arrow=False)
        st.plotly_chart(fig, use_container_width=True)

    with left:
        st.latex(rf"{c:g} \cdot " + w.bmatrix(vec.reshape(-1, 1))
                 + " = " + w.bmatrix(end.reshape(-1, 1)))
        st.caption("Every choice stretches or shrinks the same arrow -- the "
                   "direction never changes.")

        other_cap = info["other_name"].capitalize()
        st.markdown(
            f"One ingredient spans only a line. With {name} alone, every "
            f"reachable smoothie is c·({vec[0]:g}, {vec[1]:g}) = "
            f"({vec[0]:g}c, {vec[1]:g}c): sugar is always exactly "
            f"{info['own_ratio']} protein, no matter the scoops. All those "
            "points lie on one line through the origin — that line is "
            f"the span of {name}. You cannot reach most targets with {name} "
            "alone: a target like (14, 11) is off this line, so no number "
            f"of {name} scoops makes it. {other_cap} alone gives a "
            f"different line ({info['other_line']}) — still just a "
            "line. Reaching the whole plane needs both."
        )
