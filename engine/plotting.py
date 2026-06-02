"""
Shared plotting helpers (the "right panel").

The figures here draw whatever matrix they are given -- the caller passes the
already-interpolated matrix M(t), so these functions stay dumb and reusable.

2D shows the deformed grid (the 3Blue1Brown-style picture), the unit square,
and the basis vectors (which become the columns of the matrix). 3D shows the
deformed unit cube and basis vectors.
"""
import numpy as np
import plotly.graph_objects as go

GRID = 6          # grid lines run from -GRID..GRID
VIEW = 6          # axis range shown
_E1 = "crimson"
_E2 = "royalblue"
_E3 = "seagreen"
_SQUARE = "rgba(0,150,136,0.9)"
_SQUARE_FILL = "rgba(0,150,136,0.22)"
_GRIDLINE = "rgba(120,120,200,0.35)"
_VEC = "darkorange"


# ---------- 2D ----------

def _arrow2d(fig, end, color, name):
    fig.add_trace(go.Scatter(
        x=[0, end[0]], y=[0, end[1]], mode="lines",
        line=dict(color=color, width=4), name=name,
    ))
    fig.add_annotation(
        x=end[0], y=end[1], ax=0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=1.3, arrowwidth=3, arrowcolor=color,
    )


def figure_2d(M, show_vector=False, v=None, vt=None):
    fig = go.Figure()

    # deformed grid
    samples = np.linspace(-GRID, GRID, 60)
    for k in range(-GRID, GRID + 1):
        vert = M @ np.vstack([np.full_like(samples, k), samples])
        horz = M @ np.vstack([samples, np.full_like(samples, k)])
        for line in (vert, horz):
            fig.add_trace(go.Scatter(
                x=line[0], y=line[1], mode="lines",
                line=dict(color=_GRIDLINE, width=1),
                hoverinfo="skip", showlegend=False,
            ))

    # unit square
    sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]).T
    tsq = M @ sq
    fig.add_trace(go.Scatter(
        x=tsq[0], y=tsq[1], mode="lines", fill="toself",
        fillcolor=_SQUARE_FILL, line=dict(color=_SQUARE, width=2),
        name="unit square", hoverinfo="skip",
    ))

    # basis vectors = columns of M
    _arrow2d(fig, M @ np.array([1.0, 0.0]), _E1, "î → column 1")
    _arrow2d(fig, M @ np.array([0.0, 1.0]), _E2, "ĵ → column 2")

    if show_vector and v is not None and vt is not None:
        # faint original, solid image
        fig.add_trace(go.Scatter(
            x=[0, v[0]], y=[0, v[1]], mode="lines",
            line=dict(color="rgba(180,140,0,0.45)", width=3, dash="dot"), name="v",
        ))
        _arrow2d(fig, vt, _VEC, "M·v")

    fig.update_xaxes(range=[-VIEW, VIEW], zeroline=True, zerolinecolor="#888",
                     gridcolor="rgba(0,0,0,0)")
    fig.update_yaxes(range=[-VIEW, VIEW], zeroline=True, zerolinecolor="#888",
                     gridcolor="rgba(0,0,0,0)", scaleanchor="x", scaleratio=1)
    fig.update_layout(
        height=560, margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0),
    )
    return fig


# ---------- 3D ----------

_CUBE_EDGES = [
    (0, 1), (1, 3), (3, 2), (2, 0),      # bottom face
    (4, 5), (5, 7), (7, 6), (6, 4),      # top face
    (0, 4), (1, 5), (2, 6), (3, 7),      # verticals
]
_CUBE_VERTS = np.array([
    [0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0],
    [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1],
], dtype=float)


def _arrow3d(fig, end, color, name):
    fig.add_trace(go.Scatter3d(
        x=[0, end[0]], y=[0, end[1]], z=[0, end[2]], mode="lines",
        line=dict(color=color, width=7), name=name,
    ))
    fig.add_trace(go.Cone(
        x=[end[0]], y=[end[1]], z=[end[2]],
        u=[end[0]], v=[end[1]], w=[end[2]],
        sizemode="absolute", sizeref=0.5, anchor="tip",
        showscale=False, colorscale=[[0, color], [1, color]],
    ))


def figure_3d(M, show_vector=False, v=None, vt=None):
    fig = go.Figure()

    tv = (M @ _CUBE_VERTS.T).T
    for a, b in _CUBE_EDGES:
        fig.add_trace(go.Scatter3d(
            x=[tv[a, 0], tv[b, 0]], y=[tv[a, 1], tv[b, 1]], z=[tv[a, 2], tv[b, 2]],
            mode="lines", line=dict(color=_SQUARE, width=4),
            hoverinfo="skip", showlegend=False,
        ))

    _arrow3d(fig, M @ np.array([1.0, 0, 0]), _E1, "x̂ → column 1")
    _arrow3d(fig, M @ np.array([0, 1.0, 0]), _E2, "ŷ → column 2")
    _arrow3d(fig, M @ np.array([0, 0, 1.0]), _E3, "ẑ → column 3")

    if show_vector and v is not None and vt is not None:
        fig.add_trace(go.Scatter3d(
            x=[0, v[0]], y=[0, v[1]], z=[0, v[2]], mode="lines",
            line=dict(color="rgba(180,140,0,0.5)", width=4, dash="dot"), name="v",
        ))
        _arrow3d(fig, vt, _VEC, "M·v")

    rng = [-VIEW, VIEW]
    fig.update_layout(
        height=560, margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0),
        scene=dict(
            xaxis=dict(range=rng, title="x"),
            yaxis=dict(range=rng, title="y"),
            zaxis=dict(range=rng, title="z"),
            aspectmode="cube",
        ),
    )
    return fig
