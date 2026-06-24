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
_E1 = "#ff6b6b"
_E2 = "#4dabf7"
_E3 = "#51cf66"
_SQUARE = "#20c997"
_SQUARE_FILL = "rgba(32,201,151,0.22)"
_GRIDLINE = "rgba(160,160,220,0.35)"
_VEC = "#ffa94d"

_DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e6e6e6"),
)
_DARK_XAXIS = dict(zeroline=True, zerolinecolor="#aaa",
                    gridcolor="rgba(200,200,220,0.12)")
_DARK_YAXIS = dict(zeroline=True, zerolinecolor="#aaa",
                    gridcolor="rgba(200,200,220,0.12)")
_DARK_3D_AXIS = dict(
    backgroundcolor="rgba(0,0,0,0)",
    gridcolor="rgba(200,200,220,0.15)",
    zerolinecolor="#aaa",
    color="#e6e6e6",
)

# An asymmetric "rocket" outline (2xN points) used as an alternative object to
# the unit square. Asymmetric on purpose: a reflection makes a backwards rocket,
# a shear tips it, a rotation tumbles it -- orientation changes are unmissable.
_ROCKET = np.array([
    [0.00, 2.20],   # nose
    [0.60, 0.90],   # right shoulder
    [0.60, -0.60],  # right body
    [1.30, -1.50],  # right fin tip (long)
    [0.60, -1.10],  # right fin notch
    [0.50, -1.60],  # bottom right
    [-0.50, -1.60],  # bottom left
    [-0.60, -1.10],  # left fin notch
    [-0.90, -1.50],  # left fin tip (shorter -> asymmetric)
    [-0.60, -0.60],  # left body
    [-0.60, 0.90],  # left shoulder
]).T * 0.9
_ROCKET_WINDOW = np.array([0.0, 0.27]) * 0.9


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


def figure_2d(M, show_vector=False, v=None, vt=None, obj="square"):
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

    if obj == "rocket":
        pts = M @ _ROCKET
        fig.add_trace(go.Scatter(
            x=np.append(pts[0], pts[0][0]), y=np.append(pts[1], pts[1][0]),
            mode="lines", fill="toself", fillcolor=_SQUARE_FILL,
            line=dict(color=_SQUARE, width=2), name="rocket", hoverinfo="skip",
        ))
        win = M @ _ROCKET_WINDOW
        fig.add_trace(go.Scatter(
            x=[win[0]], y=[win[1]], mode="markers",
            marker=dict(color="#e6e6e6", size=9, line=dict(color=_SQUARE, width=2)),
            showlegend=False, hoverinfo="skip",
        ))
    else:
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

    fig.update_xaxes(range=[-VIEW, VIEW], **_DARK_XAXIS)
    fig.update_yaxes(range=[-VIEW, VIEW], **_DARK_YAXIS,
                     scaleanchor="x", scaleratio=1)
    fig.update_layout(
        height=420, margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0),
        **_DARK_LAYOUT,
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
        height=480, margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0),
        scene=dict(
            xaxis=dict(range=rng, title="x", **_DARK_3D_AXIS),
            yaxis=dict(range=rng, title="y", **_DARK_3D_AXIS),
            zaxis=dict(range=rng, title="z", **_DARK_3D_AXIS),
            aspectmode="cube",
            bgcolor="rgba(0,0,0,0)",
        ),
        **_DARK_LAYOUT,
    )
    return fig


# ---------- generic 2D primitives (for multi-vector topics: combinations, subspaces) ----------

def new_figure_2d(rng=8, x_title="x", y_title="y", height=420, equal=True):
    """A blank 2D canvas with origin axes, fixed range, and equal aspect."""
    fig = go.Figure()
    fig.update_xaxes(range=[-rng, rng], **_DARK_XAXIS, title=x_title)
    yaxis = dict(range=[-rng, rng], **_DARK_YAXIS, title=y_title)
    if equal:
        yaxis.update(scaleanchor="x", scaleratio=1)
    fig.update_yaxes(**yaxis)
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=10, b=10),
                      legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0),
                      **_DARK_LAYOUT)
    return fig


def add_vector_2d(fig, start, end, color, name, width=4, dash=None,
                  arrow=True, showlegend=True):
    """Draw an arrow from start to end (both length-2 sequences)."""
    fig.add_trace(go.Scatter(
        x=[start[0], end[0]], y=[start[1], end[1]], mode="lines",
        line=dict(color=color, width=width, dash=dash),
        name=name, showlegend=showlegend, hoverinfo="skip"))
    if arrow:
        fig.add_annotation(x=end[0], y=end[1], ax=start[0], ay=start[1],
                           xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowsize=1.3,
                           arrowwidth=3, arrowcolor=color)


def add_point_2d(fig, p, color, name, size=13, symbol="circle"):
    fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers",
                             marker=dict(color=color, size=size, symbol=symbol,
                                         line=dict(color="#e6e6e6", width=1)),
                             name=name))


def shade_polygon(fig, pts, fillcolor, name=None):
    """Shade a filled region given its corner points."""
    xs = [p[0] for p in pts] + [pts[0][0]]
    ys = [p[1] for p in pts] + [pts[0][1]]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", fill="toself",
                             fillcolor=fillcolor, line=dict(color="rgba(0,0,0,0)"),
                             name=name, hoverinfo="skip", showlegend=bool(name)))


# ---------- linear-systems helpers (Topic 5 and later) ----------

def add_line_2d(fig, a, b, c, color, name, rng=VIEW):
    """Draw the line a*x + b*y = c as a segment within ±rng."""
    if abs(a) < 1e-9 and abs(b) < 1e-9:
        return
    if abs(b) < 1e-9:
        xv = c / a
        fig.add_trace(go.Scatter(x=[xv, xv], y=[-rng, rng], mode="lines",
                                 line=dict(color=color, width=2), name=name))
    else:
        x0, x1 = float(-rng), float(rng)
        y0, y1 = (c - a * x0) / b, (c - a * x1) / b
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines",
                                 line=dict(color=color, width=2), name=name))


def new_figure_3d(rng=6, titles=("x", "y", "z"), height=480):
    """Blank 3D scene with cube aspect ratio and fixed ranges."""
    fig = go.Figure()
    r = [-rng, rng]
    fig.update_layout(
        height=height, margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0),
        scene=dict(
            xaxis=dict(range=r, title=titles[0], **_DARK_3D_AXIS),
            yaxis=dict(range=r, title=titles[1], **_DARK_3D_AXIS),
            zaxis=dict(range=r, title=titles[2], **_DARK_3D_AXIS),
            aspectmode="cube",
            bgcolor="rgba(0,0,0,0)",
        ),
        **_DARK_LAYOUT,
    )
    return fig


def add_plane_3d(fig, a, b, c, d, color, name, rng=6):
    """Draw a*x + b*y + c*z = d as a translucent surface."""
    if abs(a) < 1e-9 and abs(b) < 1e-9 and abs(c) < 1e-9:
        return
    t = np.linspace(-rng, rng, 25)
    if abs(c) > 1e-9:
        xs, ys = np.meshgrid(t, t)
        zs = (d - a * xs - b * ys) / c
    elif abs(b) > 1e-9:
        xs, zs = np.meshgrid(t, t)
        ys = (d - a * xs - c * zs) / b
    else:
        ys, zs = np.meshgrid(t, t)
        xs = (d - b * ys - c * zs) / a
    fig.add_trace(go.Surface(
        x=xs, y=ys, z=zs,
        colorscale=[[0, color], [1, color]],
        opacity=0.35, showscale=False, name=name,
        hoverinfo="name",
    ))
