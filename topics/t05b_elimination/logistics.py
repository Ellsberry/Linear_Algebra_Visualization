import plotly.graph_objects as go

from engine import plotting as plot
from .eq_builder import equation_builder


# ---------------------------------------------------------------------------
# Screen 2 -- Logistics (7-variable cycle shipping network)
# ---------------------------------------------------------------------------

# Augmented matrix [A | b] -- strict uniform sign rule: in=+1, out=-1, RHS=net supply/demand
_E2_AUG = [
    [-1, -1,  0,  0,  0,  0,  0, -100],   # F : -x1 - x2 = -100  (source, routes out)
    [ 1,  0, -1, -1,  0,  0,  0,    0],   # W1: x1 - x3 - x4 = 0
    [ 0,  1,  0,  0, -1, -1, -1,    0],   # W2: x2 - x5 - x6 - x7 = 0
    [ 0,  0,  1,  0,  0,  0,  0,   30],   # A : x3 = 30
    [ 0,  0,  0,  1,  1,  0,  0,   20],   # B : x4 + x5 = 20  (shared store)
    [ 0,  0,  0,  0,  0,  1,  0,   25],   # C : x6 = 25
    [ 0,  0,  0,  0,  0,  0,  1,   25],   # D : x7 = 25
]
_E2_LABELS     = ["F→W1", "F→W2", "W1→A", "W1→B", "W2→B", "W2→C", "W2→D"]
_E2_ROW_LABELS = ["F (factory)", "W1 node", "W2 node", "Store A", "Store B", "Store C", "Store D"]


def _logistics_diagram():
    """Static plotly diagram of the 7-route cycle shipping network.

    Store B is fed by BOTH W1 (x4) and W2 (x5) -- the cycle that makes
    elimination necessary and produces infinitely many valid plans.
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
    A  = [0.5, 2.5];  B  = [5.0, 2.5];  C = [8.0, 2.5];  D = [10.0, 2.5]

    # (src, dst, label, color, (label_x_offset, label_y_offset))
    # x4 and x5 both arrive at B from opposite sides -- offsets keep labels apart
    routes = [
        (F,  W1, "x₁", "royalblue",    (-0.40,  0.0)),
        (F,  W2, "x₂", "seagreen",     ( 0.40,  0.0)),
        (W1, A,  "x₃", "darkorange",   (-0.55,  0.1)),
        (W1, B,  "x₄", "crimson",      (-0.55,  0.0)),
        (W2, B,  "x₅", "mediumorchid", ( 0.55,  0.0)),
        (W2, C,  "x₆", "#B8860B",      ( 0.40,  0.1)),
        (W2, D,  "x₇", "steelblue",    ( 0.55,  0.1)),
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


def _example_two():
    equation_builder(
        key="t05b_e2",
        n_unknowns=7,
        target_aug=_E2_AUG,
        row_labels=_E2_ROW_LABELS,
        diagram_fn=_logistics_diagram,
        solution_labels=_E2_LABELS,
        intro_md=(
            "You're solving for the amount of freight on each of the seven routes "
            "(x₁…x₇) -- the shipping plan where flow in = flow out at every node "
            "and every store's demand is met. Read the network, then write each "
            "node's balance equation."
        ),
        builder_intro_md=(
            "Read the network and write the balance equation for each node -- "
            "flow in = flow out, with each store's demand and the factory's supply "
            "on the right. Type equations like `x1 - x3 - x4 = 0`."
        ),
        reduce_caption="**Reduce it** -- same three moves, seven unknowns.",
        closing_md=(
            "**Why infinitely many plans?** Elimination leaves a free variable -- "
            "store B can be supplied from either warehouse. Send any amount from "
            "0 to 20 units to B via W2 (route x₅), and the rest via W1 "
            "(route x₄ = 20 − x₅); both warehouses' totals adjust to match "
            "(x₁ = 50 − x₅, x₂ = 50 + x₅), and every choice is a valid "
            "shipping plan. That free choice is the free variable -- and it's "
            "exactly why a real logistics network needs the math: there isn't one "
            "answer, there's a whole family, and the business picks the cheapest. "
            "This is the 'infinitely many solutions' case from Topic 5, now in a "
            "system too big to picture."
        ),
    )
