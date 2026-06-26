import plotly.graph_objects as go
import streamlit as st

from engine import plotting as plot
from .eq_builder import equation_builder


# ---------------------------------------------------------------------------
# Screen 2a -- Logistics (one plan): 6-route tree, unique solution
# ---------------------------------------------------------------------------

# Augmented matrix [A | b] -- in=+1, out=-1, RHS=net supply/demand
# 6 unknowns: x1=F->W1, x2=F->W2, x3=W1->A, x4=W1->B, x5=W2->C, x6=W2->D
_E2A_AUG = [
    [-1, -1,  0,  0,  0,  0, -100],   # F : -x1 - x2 = -100
    [ 1,  0, -1, -1,  0,  0,    0],   # W1: x1 - x3 - x4 = 0
    [ 0,  1,  0,  0, -1, -1,    0],   # W2: x2 - x5 - x6 = 0
    [ 0,  0,  1,  0,  0,  0,   30],   # A : x3 = 30
    [ 0,  0,  0,  1,  0,  0,   20],   # B : x4 = 20  (single incoming route from W1)
    [ 0,  0,  0,  0,  1,  0,   25],   # C : x5 = 25
    [ 0,  0,  0,  0,  0,  1,   25],   # D : x6 = 25
]
_E2A_LABELS     = ["F→W1", "F→W2", "W1→A", "W1→B", "W2→C", "W2→D"]
_E2A_ROW_LABELS = ["F (factory)", "W1 node", "W2 node", "Store A", "Store B", "Store C", "Store D"]


def _logistics_one_diagram():
    """Static plotly diagram of the 6-route tree shipping network.

    Store B is fed only by W1 (x4) -- no cycle, so elimination yields a unique plan.
    B is positioned under W1 to make the single incoming route visually clear.
    """
    fig = go.Figure()
    fig.update_layout(
        height=360, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
        xaxis=dict(range=[-0.5, 11.5], visible=False),
        yaxis=dict(range=[0.8, 10.5], visible=False),
    )

    F  = [5.0, 9.3]
    W1 = [2.5, 6.0];  W2 = [7.5, 6.0]
    A  = [0.5, 2.5];  B  = [3.5, 2.5];  C = [6.5, 2.5];  D = [9.5, 2.5]

    # B is placed under W1 (not centered) -- one arrow arrives from W1 only
    routes = [
        (F,  W1, "x₁", "royalblue",    (-0.40,  0.0)),
        (F,  W2, "x₂", "seagreen",     ( 0.40,  0.0)),
        (W1, A,  "x₃", "darkorange",   (-0.55,  0.1)),
        (W1, B,  "x₄", "crimson",      ( 0.45,  0.0)),
        (W2, C,  "x₅", "mediumorchid", (-0.40,  0.1)),
        (W2, D,  "x₆", "steelblue",    ( 0.45,  0.1)),
    ]
    for src, dst, label, color, (ox, oy) in routes:
        plot.add_vector_2d(fig, src, dst, color, label, width=2, showlegend=False)
        mx = (src[0] + dst[0]) / 2 + ox
        my = (src[1] + dst[1]) / 2 + oy
        fig.add_annotation(x=mx, y=my, text=f"<b>{label}</b>", showarrow=False,
                           font=dict(size=13, color=color),
                           bgcolor="rgba(30,33,41,0.85)", borderpad=2)

    plot.add_point_2d(fig, F, "#E65C00", "F", size=24)
    fig.add_annotation(x=F[0], y=F[1] + 0.5, text="<b>F</b>  (supply 100)",
                       showarrow=False, font=dict(size=12),
                       bgcolor="rgba(30,33,41,0.85)", borderpad=3)

    for name, pos in [("W1", W1), ("W2", W2)]:
        plot.add_point_2d(fig, pos, "#1565C0", name, size=22)
        fig.add_annotation(x=pos[0], y=pos[1] + 0.5, text=f"<b>{name}</b>",
                           showarrow=False, font=dict(size=12),
                           bgcolor="rgba(30,33,41,0.85)", borderpad=3)

    for name, pos, demand in [("A", A, 30), ("B", B, 20), ("C", C, 25), ("D", D, 25)]:
        plot.add_point_2d(fig, pos, "#2E7D32", name, size=20)
        fig.add_annotation(x=pos[0], y=pos[1] - 0.5, showarrow=False,
                           text=f"<b>{name}</b>  demand {demand}",
                           font=dict(size=11), yanchor="top",
                           bgcolor="rgba(30,33,41,0.85)", borderpad=3)
    return fig


def _example_two_a():
    equation_builder(
        key="t05b_e2a",
        n_unknowns=6,
        target_aug=_E2A_AUG,
        row_labels=_E2A_ROW_LABELS,
        diagram_fn=_logistics_one_diagram,
        solution_labels=_E2A_LABELS,
        intro_md=(
            "You're solving for the freight on each of the six routes "
            "(x₁…x₆) -- the shipping plan where flow in = flow out at every "
            "node and every store's demand is met. Read the network, then "
            "write each node's balance equation."
        ),
        reduce_caption="**Reduce it** -- same three moves, six unknowns.",
        closing_md=(
            "**One definite plan.** Elimination drives this system to a "
            "single answer: x = (50, 50, 30, 20, 25, 25). Every route is "
            "pinned down -- there's exactly one way to meet all the demands, "
            "because each store is fed by just one path. In the next screen, "
            "opening a second route to store B changes that completely."
        ),
    )
