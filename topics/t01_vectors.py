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
PEANUT = np.array([4.0, 1.0])
PROTEIN_AXIS = "protein →"
SUGAR_AXIS = "sugar ↑"


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


# ----------------------------------------------------------------------------
# Example 1 -- One ingredient (a vector is already a recipe)
# ----------------------------------------------------------------------------
_E1_PRESETS = {
    "More scoops": ("The arrow keeps its direction and just gets longer. "
                    "Scaling a vector stretches it without turning it.", 3.0, False),
    "Half a scoop": ("You land halfway out. Scaling works with fractions, "
                     "not just whole steps.", 0.5, False),
    "Read the recipe": ("banana = (1, 4) means 1 step along the protein axis plus "
                        "4 along the sugar axis. So even a single vector is a "
                        "combination of those two axis directions — that's where "
                        "\"basis\" comes from.", 1.0, True),
}


def _example_one():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**One ingredient.** Start with one ingredient — banana, at (1, 4): "
            "one gram of protein and four of sugar per scoop. The slider is how "
            "many scoops. Watch the arrow grow as you add scoops and shrink back "
            "toward the origin as you take them away."
        )
        preset = st.selectbox("Example", list(_E1_PRESETS), key="t01e1_preset")
        notice, c_default, brk_default = _E1_PRESETS[preset]

        if st.session_state.get("t01e1_last") != preset:
            st.session_state["t01e1_c"] = c_default
            st.session_state["t01e1_break"] = brk_default
            st.session_state["t01e1_last"] = preset

        st.info(notice, icon="💡")
        c = w.scalar_slider("t01e1_c", "Scoops of banana", -3.0, 5.0, c_default, step=0.25)
        show_break = st.checkbox("Show the recipe breakdown", key="t01e1_break")

    end = c * BANANA
    with right:
        fig = plot.new_figure_2d(VIEW, PROTEIN_AXIS, SUGAR_AXIS)
        plot.add_vector_2d(fig, [0, 0], BANANA, "rgba(180,140,0,0.45)",
                           "banana (1 scoop)", dash="dot")
        plot.add_vector_2d(fig, [0, 0], end, "darkorange", f"{c:g} scoops")
        if show_break:
            plot.add_vector_2d(fig, [0, 0], [end[0], 0], "crimson",
                               "protein part", dash="dash", arrow=False)
            plot.add_vector_2d(fig, [end[0], 0], end, "royalblue",
                               "sugar part", dash="dash", arrow=False)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show the math"):
        st.latex(rf"{c:g} \cdot " + w.bmatrix(BANANA.reshape(-1, 1))
                 + " = " + w.bmatrix(end.reshape(-1, 1)))
        st.caption("Scaling multiplies every component by the same number.")


# ----------------------------------------------------------------------------
# Example 2 -- Two ingredients, added (tip-to-tail / parallelogram)
# ----------------------------------------------------------------------------
_E2_PRESETS = {
    "Tip-to-tail": ("The sum is simply where you land after following one arrow "
                    "and then the other.", BANANA, PEANUT),
    "Same direction": ("Two ingredients pointing the same way just give a longer "
                       "arrow in that direction — nothing new about where you can go.",
                       np.array([2.0, 1.0]), np.array([4.0, 2.0])),
    "Opposite directions": ("Pointing against each other, they partly cancel, and "
                            "the sum comes out shorter than either one.",
                            np.array([3.0, 2.0]), np.array([-2.0, -1.0])),
}


def _example_two():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Two ingredients, added.** Add a second ingredient: peanut butter at "
            "(4, 1). One scoop of each gives a smoothie of banana + peanut butter. "
            "The result is the two arrows laid **tip-to-tail** — walk out along "
            "banana, then keep going along peanut butter, and where you end up is "
            "the sum. Flip to the **parallelogram** view to see the same answer a "
            "second way."
        )
        preset = st.selectbox("Example", list(_E2_PRESETS), key="t01e2_preset")
        notice, u_def, v_def = _E2_PRESETS[preset]

        if st.session_state.get("t01e2_last") != preset:
            w.set_vector_state("t01e2_u", u_def)
            w.set_vector_state("t01e2_v", v_def)
            st.session_state["t01e2_last"] = preset

        st.info(notice, icon="💡")
        view = st.radio("View", ["Tip-to-tail", "Parallelogram"], horizontal=True,
                        key="t01e2_view")
        u = w.vector_editor("t01e2_u", 2, u_def, label="banana (u)")
        v = w.vector_editor("t01e2_v", 2, v_def, label="peanut butter (v)")

    s = u + v
    with right:
        fig = plot.new_figure_2d(VIEW, PROTEIN_AXIS, SUGAR_AXIS)
        if view == "Tip-to-tail":
            plot.add_vector_2d(fig, [0, 0], u, "darkorange", "u")
            plot.add_vector_2d(fig, u, s, "seagreen", "v (from tip of u)")
        else:
            plot.add_vector_2d(fig, [0, 0], u, "darkorange", "u")
            plot.add_vector_2d(fig, [0, 0], v, "seagreen", "v")
            plot.add_vector_2d(fig, u, s, "rgba(0,0,0,0.25)", "", arrow=False,
                               dash="dot", showlegend=False)
            plot.add_vector_2d(fig, v, s, "rgba(0,0,0,0.25)", "", arrow=False,
                               dash="dot", showlegend=False)
        plot.add_vector_2d(fig, [0, 0], s, "crimson", "u + v", width=5)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show the math"):
        st.latex(w.bmatrix(u.reshape(-1, 1)) + " + " + w.bmatrix(v.reshape(-1, 1))
                 + " = " + w.bmatrix(s.reshape(-1, 1)))
        st.caption("Add vectors component by component — protein with protein, "
                   "sugar with sugar.")


# ----------------------------------------------------------------------------
# Example 3 -- The smoothie mixer (combinations, span, basis)
# ----------------------------------------------------------------------------
_E3_PRESETS = {
    "Two good ingredients": ("The span fills the whole plane — any target is "
                             "reachable, and there's exactly one recipe for it. "
                             "This is a basis. ✓", BANANA, PEANUT),
    "Standard axes": ("The ordinary grid is just one choice of two vectors. The "
                      "recipe for (3, 2) is the obvious 3 and 2 — no mystery, but "
                      "no more special than banana and peanut butter.",
                      np.array([1.0, 0.0]), np.array([0.0, 1.0])),
    "Proportional ingredients": ("The second ingredient is just the first one "
                                 "doubled, so it adds nothing new. Every mix lands "
                                 "on a single line, and most targets are impossible "
                                 "to hit. Not a basis. ✗",
                                 np.array([1.0, 2.0]), np.array([2.0, 4.0])),
}
TARGET = np.array([10.0, 10.0])

DEFINITION = (
    "**What's a basis?**  A *basis* is a small set of vectors you can build "
    "everything else out of — every point you can reach is one combination "
    "*c₁v₁ + c₂v₂* of them, and with a *good* basis each point has **exactly one** "
    "recipe. Banana and peanut butter point in genuinely different directions, so "
    "together they reach the whole plane *and* every target has a single scoop "
    "recipe — that makes them a basis for these two nutrients. The plain "
    "protein/sugar axes are just the most obvious basis of all."
)


def _skewed_grid(fig, v1, v2):
    T = 14
    faint = "rgba(120,120,200,0.22)"
    for k in range(-10, 11):
        a, b = k * v1 - T * v2, k * v1 + T * v2
        plot.add_vector_2d(fig, a, b, faint, "", width=1, arrow=False, showlegend=False)
        a, b = -T * v1 + k * v2, T * v1 + k * v2
        plot.add_vector_2d(fig, a, b, faint, "", width=1, arrow=False, showlegend=False)


def _example_three():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**The smoothie mixer.** Now you control the amounts. Banana (1, 4) and "
            "peanut butter (4, 1), each with its own scoops slider: *c₁ scoops of "
            "banana plus c₂ scoops of peanut butter.* The moving point is your "
            "smoothie, **c₁·banana + c₂·peanut butter** — and that expression is a "
            "**linear combination**. Turn on **Show span** to shade every smoothie "
            "you could possibly make from these two ingredients. Then take the "
            "**target** and tune the two sliders to land on it."
        )
        st.info(DEFINITION, icon="🧱")

        preset = st.selectbox("Example", list(_E3_PRESETS), key="t01e3_preset")
        notice, v1_def, v2_def = _E3_PRESETS[preset]
        if st.session_state.get("t01e3_last") != preset:
            w.set_vector_state("t01e3_v1", v1_def)
            w.set_vector_state("t01e3_v2", v2_def)
            st.session_state["t01e3_last"] = preset
        st.info(notice, icon="💡")

        v1 = w.vector_editor("t01e3_v1", 2, v1_def, label="banana (v₁)")
        v2 = w.vector_editor("t01e3_v2", 2, v2_def, label="peanut butter (v₂)")

        allow_neg = st.checkbox("Allow negative scoops", key="t01e3_neg")
        lo = -12.0 if allow_neg else 0.0
        c1 = w.scalar_slider("t01e3_c1", "Scoops of banana (c₁)", lo, 12.0, 2.0, step=0.25)
        c2 = w.scalar_slider("t01e3_c2", "Scoops of peanut butter (c₂)", lo, 12.0, 2.0, step=0.25)
        show_span = st.checkbox("Show span", value=True, key="t01e3_span")

    result = c1 * v1 + c2 * v2
    det = float(np.linalg.det(np.column_stack([v1, v2])))
    independent = abs(det) > 1e-9
    dist = float(np.linalg.norm(result - TARGET))

    with right:
        fig = plot.new_figure_2d(VIEW, PROTEIN_AXIS, SUGAR_AXIS)
        if show_span:
            span_fill = "rgba(0,150,136,0.13)"
            if not independent:
                d = v1 if np.linalg.norm(v1) > 0 else v2
                if np.linalg.norm(d) > 0:
                    d = d / np.linalg.norm(d)
                    plot.add_vector_2d(fig, -30 * d, 30 * d, "rgba(0,150,136,0.30)",
                                       "span (a line)", width=14, arrow=False)
            elif allow_neg:
                R = VIEW
                plot.shade_polygon(fig, [(-R, -R), (R, -R), (R, R), (-R, R)],
                                   span_fill, "span (whole plane)")
            else:
                B = 14
                plot.shade_polygon(fig, [(0, 0), B * v1, B * (v1 + v2), B * v2],
                                   span_fill, "reachable smoothies")
        _skewed_grid(fig, v1, v2)
        plot.add_vector_2d(fig, [0, 0], v1, "darkorange", "banana v₁")
        plot.add_vector_2d(fig, [0, 0], v2, "seagreen", "peanut butter v₂")
        plot.add_point_2d(fig, TARGET, "crimson", "target (10, 10)", size=15, symbol="star")
        plot.add_point_2d(fig, result, "navy", "your smoothie", size=13)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"recipe: **{c1:g}** · banana + **{c2:g}** · peanut butter")
        st.markdown(f"smoothie = ({result[0]:.1f}, {result[1]:.1f}) · "
                    f"target (10, 10) · distance **{dist:.2f}**")
        if independent:
            st.success("basis ✓ — two different directions reach the whole plane.")
        else:
            st.warning("not a basis ✗ — proportional vectors only reach one line.")
        if dist < 0.3:
            st.success("🎯 You hit the target smoothie!")

    with st.expander("Show the math"):
        st.latex(rf"{c1:g}\," + w.bmatrix(v1.reshape(-1, 1)) + rf" + {c2:g}\,"
                 + w.bmatrix(v2.reshape(-1, 1)) + " = " + w.bmatrix(result.reshape(-1, 1)))
        st.markdown(
            f"det[v₁ v₂] = `{det:.2f}`. "
            + ("Non-zero ⇒ independent ⇒ a basis ⇒ every target has **exactly one** recipe."
               if independent else
               "Zero ⇒ dependent ⇒ **not** a basis ⇒ targets off the line have **no** recipe, "
               "and targets on it have **infinitely many**.")
        )
        st.caption("That one-solution / no-solution / many-solutions split is exactly "
                   "the question we formalize later when solving Ax = b.")

    with st.expander("Challenge — Make the target smoothie"):
        st.markdown(
            "Hit the target by setting the two scoop sliders. With two good "
            "ingredients there's exactly *one* pair that works — find it. Then "
            "switch to the proportional pair and try the same target: anything off "
            "the line simply can't be made, no matter how you set the sliders. That "
            "\"one solution / no solution\" feeling is the exact question we'll "
            "formalize later when we solve **Ax = b**."
        )

    with st.expander("Reality check"):
        st.markdown(
            "In a real kitchen you can't add −2 scoops. Math is more generous: it "
            "lets coefficients go negative — subtracting an ingredient — and that's "
            "how vectors reach in *every* direction, not just the first quadrant. "
            "Turn on **Allow negative scoops** to free the vectors to the full "
            "plane; just remember that's the math being more flexible than your "
            "blender."
        )
