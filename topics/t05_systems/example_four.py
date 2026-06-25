"""Example 4 -- Chemistry (balance a reaction)."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from engine import widgets as w
from engine import plotting as plot


def _example_four():
    st.markdown(
        "**Balance** `a H₂ + b O₂ → c H₂O`.\n\n"
        "Set the sliders until both atom counts match on left and right."
    )
    a_val = w.scalar_slider("t05e4_a", "a  (H₂ molecules)", 0, 8, 0, 1)
    b_val = w.scalar_slider("t05e4_b", "b  (O₂ molecules)", 0, 8, 0, 1)
    c_val = w.scalar_slider("t05e4_c", "c  (H₂O molecules)", 0, 8, 0, 1)

    a_val, b_val, c_val = int(a_val), int(b_val), int(c_val)
    h_l, h_r = 2 * a_val, 2 * c_val
    o_l, o_r = 2 * b_val, c_val
    h_ok   = (h_l == h_r)
    o_ok   = (o_l == o_r)
    both_ok = h_ok and o_ok and (a_val + b_val + c_val > 0)

    left, right = st.columns([0.5, 0.5], gap="large")

    with right:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="left side",
            x=["H atoms", "O atoms"], y=[h_l, o_l],
            marker_color=["seagreen" if h_ok else "steelblue",
                          "seagreen" if o_ok else "steelblue"],
            text=[str(h_l), str(o_l)], textposition="outside",
        ))
        fig.add_trace(go.Bar(
            name="right side",
            x=["H atoms", "O atoms"], y=[h_r, o_r],
            marker_color=["seagreen" if h_ok else "tomato",
                          "seagreen" if o_ok else "tomato"],
            text=[str(h_r), str(o_r)], textposition="outside",
        ))
        fig.update_layout(
            barmode="group", height=320,
            margin=dict(l=10, r=10, t=40, b=10),
            title="Atom balance: left ← → right",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
            yaxis=dict(range=[0, max(h_l, h_r, o_l, o_r, 3) + 2]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e6e6e6"),
        )
        st.plotly_chart(fig, use_container_width=True)

        if both_ok:
            st.success("✓ Balanced!")
        elif a_val + b_val + c_val == 0:
            st.info("Move the sliders to try a combination.")
        else:
            h_mark = "✓" if h_ok else "✗"
            o_mark = "✓" if o_ok else "✗"
            st.warning(f"Not balanced yet: {h_mark} H  ·  {o_mark} O")

    with left:
        st.markdown("**Hydrogen atoms:** left = 2a, right = 2c  →  equation: a = c")
        st.markdown("**Oxygen atoms:** left = 2b, right = c  →  equation: 2b = c")
        st.markdown("Free variable: set a = 2, then c = 2 and b = 1  →  ratio **a : b : c = 2 : 1 : 2**")
        st.latex(r"2\,\text{H}_2 + \text{O}_2 \;\longrightarrow\; 2\,\text{H}_2\text{O}")

    st.markdown(
        "> Balancing any chemical reaction is solving a linear system — the coefficients "
        "that conserve every atom. Notice the answer is a *ratio*: 2 : 1 : 2 works, and "
        "so does 4 : 2 : 4. The system has infinitely many solutions, so chemists pick "
        "the smallest whole numbers. So 2 H₂ + O₂ → 2 H₂O."
    )
