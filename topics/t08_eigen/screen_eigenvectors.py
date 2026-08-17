"""Topic 8, Screen 3 -- Finding eigenvectors: solve (A-lambda I)v = 0."""
import plotly.graph_objects as go
import streamlit as st

from engine import plotting as plot

_IDEA = """
For each eigenvalue λ, its eigenvectors are every non-zero v with (A − λI)·v = 0 --
which is exactly the NULL SPACE of the matrix (A − λI). You already learned to
compute a null space in Topic 6: subtract λ down the diagonal, row-reduce, and read
off the free-variable direction. Do that once per eigenvalue.
"""

_B2_TEXT = """
**For λ = 3:** A − 3I = [[−1, 1], [1, −1]]. Row-reduce: the rule is −x₁ + x₂ = 0,
so x₁ = x₂. The direction is (1, 1) -- matching what we saw.

**For λ = 1:** A − 1I = [[1, 1], [1, 1]]. Row-reduce: x₁ + x₂ = 0, so x₁ = −x₂. The
direction is (1, −1).
"""

_B2_LATEX = r"""
\begin{aligned}
\lambda = 3&: \quad A - 3I = \begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix}
  \ \to\ -x_1 + x_2 = 0 \ \to\ (1, 1) \\
\lambda = 1&: \quad A - 1I = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}
  \ \to\ x_1 + x_2 = 0 \ \to\ (1, -1)
\end{aligned}
"""

_B2_CAPTION = "Each eigenvalue's null space is a line -- its eigenvector direction."

_B3_TEXT = """
**λ = 1:** direction (−1, 1, 0).  **λ = 3:** direction (1, 1, 0).  **λ = 4:**
direction (0, 0, 1). Each is the null-space direction of (B − λI) -- the same recipe,
three times.
"""

_B3_LATEX = r"""
\begin{aligned}
B - I &= \begin{bmatrix} 1 & 1 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 3 \end{bmatrix}
  \ \to\ (-1, \ 1, \ 0) \\
B - 3I &= \begin{bmatrix} -1 & 1 & 0 \\ 1 & -1 & 0 \\ 0 & 0 & 1 \end{bmatrix}
  \ \to\ (1, \ 1, \ 0) \\
B - 4I &= \begin{bmatrix} -2 & 1 & 0 \\ 1 & -2 & 0 \\ 0 & 0 & 0 \end{bmatrix}
  \ \to\ (0, \ 0, \ 1)
\end{aligned}
"""

_B3_CAPTION = ("Three eigenvalues, three eigenvector lines. Notice they are perpendicular "
              "-- that happens for symmetric matrices like this one.")

_CLOSING = """
You can now find both halves: the eigenvalues from det(A − λI) = 0, and each
eigenvector from its null space. Next: what the eigenvalues actually TELL you.
"""


def render_eigenvectors():
    # Block 1 -- the idea (text only)
    st.markdown(_IDEA)

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
        st.caption(_B2_CAPTION)

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
