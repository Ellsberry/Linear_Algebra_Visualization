"""Example 2 -- Business (break-even)."""
import streamlit as st

from engine import widgets as w
from engine import plotting as plot


def _example_two():
    st.markdown(
        "**Break-even.** Revenue and cost are two lines. They cross where profit = 0 "
        "— that crossing point is the solution of a linear system."
    )
    price    = w.scalar_slider("t05e2_price", "Selling price per unit ($)", 0.0, 20.0,  8.0, 0.5)
    fixed    = w.scalar_slider("t05e2_fixed", "Fixed cost ($)",             0.0, 100.0, 40.0, 1.0)
    var_cost = w.scalar_slider("t05e2_var",   "Variable cost per unit ($)", 0.0, 20.0,  4.0, 0.5)

    rng_x = 20
    y_max = max(price * rng_x, fixed + var_cost * rng_x) * 1.15 + 10

    left, right = st.columns([0.5, 0.5], gap="large")

    with right:
        fig = plot.new_figure_2d(rng=rng_x, x_title="quantity sold", y_title="dollars",
                                 equal=False)
        fig.update_xaxes(range=[0, rng_x])
        fig.update_yaxes(range=[0, y_max])
        # Revenue: y = price·q  →  −price·x + y = 0
        plot.add_line_2d(fig, -price, 1, 0,     "royalblue", f"Revenue = {price:.2g}·q",                    rng=rng_x)
        # Cost:    y = fixed + var·q  →  −var·x + y = fixed
        plot.add_line_2d(fig, -var_cost, 1, fixed, "crimson", f"Cost = {fixed:.2g} + {var_cost:.2g}·q",     rng=rng_x)

        if price > var_cost:
            q_star = fixed / (price - var_cost)
            y_star = price * q_star
            if 0 <= q_star <= rng_x * 1.5:
                plot.add_point_2d(fig, [q_star, y_star], "seagreen",
                                  f"break-even  q* = {q_star:.1f}", size=14)
            st.plotly_chart(fig, use_container_width=True)
            st.success(f"Break-even at **q* = {q_star:.1f} units** "
                       f"(revenue = cost = ${y_star:.2f}).")
        else:
            st.plotly_chart(fig, use_container_width=True)
            st.warning("No break-even — each unit loses money (price ≤ variable cost): "
                       "the lines are parallel-ish and never cross.")

    with left:
        st.markdown(f"Revenue line: $y = {price:.2g}\\,q$")
        st.markdown(f"Cost line: $y = {fixed:.2g} + {var_cost:.2g}\\,q$")
        if price > var_cost:
            st.latex(
                r"q^* = \frac{\text{fixed}}{\text{price} - \text{var}} = "
                rf"\frac{{{fixed:.2g}}}{{{price:.2g} - {var_cost:.2g}}} "
                rf"= {fixed / (price - var_cost):.2f}"
            )

    st.markdown(
        "> Every break-even calculation, and every \"supply meets demand\" price, is the "
        "solution of a linear system — the point where two lines cross. If price never "
        "beats the per-unit cost, the lines never meet: no solution."
    )
