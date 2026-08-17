"""Topic 8, Screen 5 -- Why it matters: Markov chains."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from engine import widgets as w

P = np.array([
    [0.7, 0.2, 0.2],
    [0.2, 0.6, 0.2],
    [0.1, 0.2, 0.6],
])

_STATES = ["sunny", "cloudy", "rainy"]
_COLORS = ["#ffd43b", "#74c0fc", "#4dabf7"]

_DEF_TEXT = """
A **Markov chain** is a system that hops between a few states, one step at a time,
where the next step depends only on where you are now -- not on how you got there.
You describe it with a matrix whose columns are probabilities: each column says,
"if I am in THIS state now, here are the chances of each state next." Every column
adds up to 1, because something must happen next.

Our example: the weather, with three states -- sunny, cloudy, rainy. The matrix P
below reads column by column. The first column says a sunny day is followed by
another sunny day 70% of the time, a cloudy day 20%, a rainy day 10%.
"""

_B2_CAPTION = ("Drag the days forward and watch the chances stop changing -- the "
              "weather forgets where it started.")

_B3_TEXT = """
Push far enough and the numbers stop moving: about 40% sunny, 33% cloudy, 27%
rainy -- no matter what day you started from. That settled distribution is a special
vector: applying P leaves it unchanged, so P·s = 1·s. It is an eigenvector of P with
eigenvalue 1 -- the **dominant eigenvector**. The long-run climate is literally the
matrix's own special direction.
"""

_B3_CAPTION = "steady state = dominant eigenvector"

_BIG_PICTURE = """
This is why eigenvectors matter: whenever a system repeats a step over and over --
weather settling into a climate, web pages ranked by PageRank, populations reaching
balance -- it lines up with the dominant eigenvector, and the eigenvalue tells you
whether it grows, shrinks, or holds steady. The special directions are where things
end up.
"""

_CLOSING = """
One loose end remains: the rotation with no real eigenvectors. To handle it we need
a new kind of number -- one whose square can be negative. That is the imaginary unit,
and complex numbers are the next topic -- where rotations finally get their
eigenvalues.
"""


def _bar_fig(probs, height=340):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=_STATES, y=list(probs), marker_color=_COLORS,
        text=[f"{p * 100:.0f}%" for p in probs], textposition="outside",
    ))
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(range=[0, 1], zeroline=True, zerolinecolor="#aaa",
                  gridcolor="rgba(200,200,220,0.12)"),
        xaxis=dict(zeroline=True, zerolinecolor="#aaa"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
    )
    return fig


def render_markov():
    # Block 1 -- what a Markov chain is (text only)
    st.markdown(_DEF_TEXT)
    st.latex(r"P = " + w.bmatrix(P))
    st.caption("Rows and columns, in order: sunny, cloudy, rainy.")

    # Block 2 -- run it forward (math left, bar chart right)
    step = st.slider("Days from now", 0, 20, 0, key="t08_markov_step")
    x0 = np.array([1.0, 0.0, 0.0])
    x = np.linalg.matrix_power(P, step) @ x0

    left2, right2 = st.columns([0.5, 0.5], gap="large")
    with left2:
        st.latex(rf"x_{{{step}}} = " + w.bmatrix(x.reshape(-1, 1)))
        s_pct, c_pct, r_pct = x[0] * 100, x[1] * 100, x[2] * 100
        st.markdown(
            f"Starting from a sunny day, in {step} days the chances are "
            f"{s_pct:.0f}% sunny, {c_pct:.0f}% cloudy, {r_pct:.0f}% rainy."
        )
    with right2:
        st.plotly_chart(_bar_fig(x), use_container_width=True)
        st.caption(_B2_CAPTION)

    # Block 3 -- the steady state is the dominant eigenvector (math left, bar chart right)
    eigvals, eigvecs = np.linalg.eig(P)
    idx = int(np.argmin(np.abs(eigvals - 1)))
    s = np.real(eigvecs[:, idx])
    s = s / s.sum()

    left3, right3 = st.columns([0.5, 0.5], gap="large")
    with left3:
        st.markdown(_B3_TEXT)
        st.latex(r"P \cdot s = s, \qquad s = " + w.bmatrix(s.reshape(-1, 1))
                 + r", \qquad \lambda = 1")
    with right3:
        st.plotly_chart(_bar_fig(s), use_container_width=True)
        st.caption(_B3_CAPTION)

    # Block 4 -- the big picture (text only)
    st.markdown(_BIG_PICTURE)

    # Block 5 -- closing bridge (text only)
    st.markdown(_CLOSING)
