"""Screen 4 -- Line of best fit."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from engine import plotting as plot

_T = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])
_TEMP = np.array([6.0, 8.0, 13.0, 17.0, 20.0, 26.0])

_INTRO = """
Here is real data: a cold drink warming up on the counter, its temperature
measured every 2 minutes. The points do NOT sit on any straight line -- real
measurements never do. We want the line that misses them by the least total
amount. That is the **line of best fit**, and it is exactly a projection: no line
hits every point (the target is outside the column space), so we find the closest
line instead.
"""

_FIT_CAPTION = (
    "Every 2 minutes the drink warms about 4 degrees (2 degrees per minute); "
    "it started near 5."
)

_GRAPH_CAPTION = (
    "The line of best fit; dashed drops are the leftovers (residuals) it "
    "could not avoid."
)

_NORMAL_EQ_TEXT = """
This is the normal equations at work. Set up A with two columns -- a column of
1s (for the starting temperature) and the column of times (for the rate) -- and let
b be the measured temperatures. Then solve AᵀA·x-hat = Aᵀb for x-hat = (start,
rate).
"""

_NORMAL_EQ_CAPTION = (
    "The same AᵀA·x-hat = Aᵀb from the last screen, on real numbers -- and the "
    "best fit comes out to clean values."
)

_PREDICT_TEXT = """
Once you have the line, you can PREDICT. At t = 12 minutes the line says
temp = 5 + 2·12 = 29 degrees -- a reasonable guess even though we never measured
there. That is the real power of a best-fit line: filling in what you didn't
measure.
"""

_CLOSING = """
No line hit every point, so we found the closest line -- a projection onto what a
line can reach. Last screen: the places this exact math runs in the real world.
"""


def render_fit():
    A = np.column_stack([np.ones_like(_T), _T])
    AtA = A.T @ A
    Atb = A.T @ _TEMP
    x_hat = np.linalg.solve(AtA, Atb)
    intercept, slope = x_hat[0], x_hat[1]
    predicted = A @ x_hat

    # Block 1 -- the setup (text only)
    st.markdown(_INTRO)

    # Block 2 -- the data and the fit (math left, graph right)
    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        rows = " \\\\\n".join(
            rf"t={int(t)} &\to \text{{temp}}={int(temp)}"
            for t, temp in zip(_T, _TEMP)
        )
        st.latex(r"\begin{aligned}" + "\n" + rows + "\n" + r"\end{aligned}")
        st.latex(rf"\text{{temp}} = {intercept:g} + {slope:g}\cdot t")
        st.markdown(_FIT_CAPTION)
    with right:
        fig = plot.new_figure_2d(rng=11, x_title="time (minutes)",
                                 y_title="temperature (degrees)", equal=False)
        fig.update_xaxes(range=[0, 11])
        fig.update_yaxes(range=[0, 28])
        plot.add_line_2d(fig, -slope, 1, intercept, "#4dabf7",
                         f"best fit: temp = {intercept:g} + {slope:g}·t", rng=11)
        for t, temp, pred in zip(_T, _TEMP, predicted):
            plot.add_vector_2d(fig, (t, temp), (t, pred), "#ffa94d", "residual",
                               dash="dash", arrow=False, showlegend=False)
        fig.add_trace(go.Scatter(
            x=_T, y=_TEMP, mode="markers",
            marker=dict(color="#ff6b6b", size=11, line=dict(color="#e6e6e6", width=1)),
            name="measured temperature",
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(_GRAPH_CAPTION)

    # Block 3 -- how the fit is computed (math left, no graph)
    st.markdown(_NORMAL_EQ_TEXT)
    AtA_latex = (
        r"A^T A = \begin{bmatrix} " + f"{AtA[0,0]:g} & {AtA[0,1]:g} \\\\ "
        f"{AtA[1,0]:g} & {AtA[1,1]:g}" + r" \end{bmatrix}"
    )
    Atb_latex = r"A^T b = \begin{bmatrix} " + f"{Atb[0]:g} \\\\ {Atb[1]:g}" + r" \end{bmatrix}"
    xhat_latex = (
        r"\hat{x} = \begin{bmatrix} " + f"{intercept:g} \\\\ {slope:g}" +
        r" \end{bmatrix} \;\Longrightarrow\; " +
        rf"\text{{temp}} = {intercept:g} + {slope:g}\cdot t"
    )
    st.latex(AtA_latex + r"\qquad" + Atb_latex)
    st.latex(xhat_latex)
    st.markdown(_NORMAL_EQ_CAPTION)

    # Block 4 -- use it to predict (text only)
    st.markdown(_PREDICT_TEXT)

    # Block 5 -- closing text
    st.markdown(_CLOSING)
