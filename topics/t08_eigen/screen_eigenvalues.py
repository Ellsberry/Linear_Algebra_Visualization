"""Topic 8, Screen 2 -- Finding eigenvalues: the characteristic equation."""
import plotly.graph_objects as go
import streamlit as st

from engine import plotting as plot

_DERIVATION = """
Start from the definition A·v = λ·v and move everything to one side:
A·v − λ·v = 0. Factor out v -- but carefully, because A is a matrix and λ is a
number, so we write λ as λ·I (lambda times the identity): (A − λI)·v = 0.

Now the key idea. We want a NON-zero eigenvector v that this squashes to zero. From
Topic 6, a matrix squashes a non-zero vector to zero only when it is singular -- and
from Topic 3, a matrix is singular exactly when its determinant is zero. So:

**det(A − λI) = 0.** This is the **characteristic equation**. Solve it for λ.
"""

_B2_TEXT = """
Subtract λ down the diagonal: A − λI = [[2−λ, 1], [1, 2−λ]]. Its determinant is
(2−λ)(2−λ) − (1)(1) = (2−λ)² − 1. Set it to zero:

(2−λ)² − 1 = 0  →  (2−λ)² = 1  →  2−λ = ±1  →  λ = 1 or λ = 3.

Two eigenvalues, exactly the stretch factors we saw: 3 and 1.
"""

_B2_LATEX = r"""
\begin{aligned}
A - \lambda I &= \begin{bmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{bmatrix} \\
\det(A - \lambda I) &= (2-\lambda)(2-\lambda) - (1)(1) = (2-\lambda)^2 - 1 \\
(2-\lambda)^2 - 1 &= 0 \\
2 - \lambda &= \pm 1 \\
\lambda &= 1 \text{ or } \lambda = 3
\end{aligned}
"""

_B3_TEXT = """
The same method scales up. For a 3 by 3, det(B − λI) = 0 becomes a cubic (a
degree-3 equation), giving up to three eigenvalues. This matrix's extra row and
column are simple (a 4 sitting alone in the corner), so the answer splits into the
same 2 by 2 as before plus that corner: the eigenvalues are 1, 3, and 4.
"""

_B3_LATEX = r"""
\begin{aligned}
\det(B - \lambda I) &= 0 \\
\left((2-\lambda)^2 - 1\right)(4 - \lambda) &= 0 \\
\lambda &= 1, \ 3, \ 4
\end{aligned}
"""

_B3_CAPTION = "Three eigenvalues, three special directions -- now in 3D. Rotate to see them."

_CLOSING = """
Eigenvalues in hand, we still need the directions themselves. For each λ, finding
its eigenvector is a null-space problem you already know how to do.
"""


def render_eigenvalues():
    # Block 1 -- the derivation (text + math)
    st.markdown(_DERIVATION)
    st.latex(r"(A - \lambda I) v = 0")
    st.latex(r"\det(A - \lambda I) = 0")

    # Block 2 -- worked 2x2 (math left, graph right)
    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        st.markdown(_B2_TEXT)
        st.latex(_B2_LATEX)
    with right:
        fig = plot.new_figure_2d(rng=7)
        plot.add_line_2d(fig, 1, -1, 0, "rgba(160,160,160,0.5)", "line through (1, 1)", rng=7)
        plot.add_line_2d(fig, 1, 1, 0, "rgba(160,160,160,0.5)", "line through (1, −1)", rng=7)
        plot.add_vector_2d(fig, (0, 0), (1, 1), "#4dabf7", "(1, 1), λ = 3")
        plot.add_vector_2d(fig, (0, 0), (1, -1), "#ffa94d", "(1, −1), λ = 1")
        st.plotly_chart(fig, use_container_width=True)

    # Block 3 -- worked 3x3 (math left, 3D graph right)
    left3, right3 = st.columns([0.5, 0.5], gap="large")
    with left3:
        st.markdown(_B3_TEXT)
        st.latex(_B3_LATEX)
    with right3:
        fig3 = plot.new_figure_3d(rng=5)
        fig3.add_trace(go.Scatter3d(
            x=[-4, 4], y=[4, -4], z=[0, 0], mode="lines",
            line=dict(color="#ffa94d", width=7), name="(−1, 1, 0), λ = 1",
        ))
        fig3.add_trace(go.Scatter3d(
            x=[-4, 4], y=[-4, 4], z=[0, 0], mode="lines",
            line=dict(color="#4dabf7", width=7), name="(1, 1, 0), λ = 3",
        ))
        fig3.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[-4, 4], mode="lines",
            line=dict(color="#51cf66", width=7), name="(0, 0, 1), λ = 4",
        ))
        st.plotly_chart(fig3, use_container_width=True)
        st.caption(_B3_CAPTION)

    # Block 4 -- closing (text only)
    st.markdown(_CLOSING)
