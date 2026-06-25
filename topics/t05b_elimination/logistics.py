import plotly.graph_objects as go
import streamlit as st

from engine import plotting as plot
from .workbench import workbench, _load_aug


# ---------------------------------------------------------------------------
# Screen 2 — Logistics (6-variable shipping network)
# ---------------------------------------------------------------------------

# Augmented matrix [A | b] for the six balance equations
_E2_AUG = [
    [ 1,  0, -1, -1,  0,  0,  0],   # W1: x1 - x3 - x4 = 0
    [ 0,  1,  0,  0, -1, -1,  0],   # W2: x2 - x5 - x6 = 0
    [ 0,  0,  1,  0,  0,  0, 30],   # A:  x3 = 30
    [ 0,  0,  0,  1,  0,  0, 20],   # B:  x4 = 20
    [ 0,  0,  0,  0,  1,  0, 25],   # C:  x5 = 25
    [ 0,  0,  0,  0,  0,  1, 25],   # D:  x6 = 25
]
_E2_LABELS     = ["F→W1", "F→W2", "W1→A", "W1→B", "W2→C", "W2→D"]
_E2_ROW_LABELS = ["W1 node", "W2 node", "Store A", "Store B", "Store C", "Store D"]

_E2_NOTICE = """
The unknowns are how much travels on each route. "Flow in = flow out" at every
node gives one equation each; solving the system is the shipping plan. Six
unknowns — no picture for that — but the same three moves solve it. (Networks
with alternative routes can have *many* valid plans; this tree has exactly one.)
"""


def _check_grid_cb():
    wrong = []
    for i, target_row in enumerate(_E2_AUG):
        for j, tv in enumerate(target_row):
            wkey = f"t05b_e2_grid__{i}__{j}"
            if abs(float(st.session_state.get(wkey, 0.0)) - float(tv)) > 1e-9:
                if i not in wrong:
                    wrong.append(i)
    st.session_state["t05b_e2_check_result"] = wrong
    if not wrong:
        _load_aug("t05b_e2", _E2_AUG)
        st.session_state["t05b_e2_ready"] = True


def _fill_for_me_cb():
    for i, row in enumerate(_E2_AUG):
        for j, val in enumerate(row):
            st.session_state[f"t05b_e2_grid__{i}__{j}"] = float(val)
    st.session_state["t05b_e2_check_result"] = []
    _load_aug("t05b_e2", _E2_AUG)
    st.session_state["t05b_e2_ready"] = True


def _logistics_diagram():
    """Static plotly diagram of the 7-route cycle shipping network.

    Store B is fed by BOTH W1 (x4) and W2 (x5) — the cycle that makes
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
    # x4 and x5 both arrive at B from opposite sides — offsets keep labels apart
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


def _grid_display():
    """Editable 6×7 augmented-matrix grid (all cells default to 0)."""
    col_labels = ["x₁", "x₂", "x₃", "x₄", "x₅", "x₆", "b"]
    widths = [1.5] + [0.65] * 7

    hcols = st.columns(widths)
    hcols[0].markdown("**Node**")
    for j, lbl in enumerate(col_labels):
        hcols[j + 1].markdown(f"**{lbl}**")

    for i, row_label in enumerate(_E2_ROW_LABELS):
        rcols = st.columns(widths)
        rcols[0].markdown(f"*{row_label}*")
        for j in range(7):
            wkey = f"t05b_e2_grid__{i}__{j}"
            if wkey not in st.session_state:
                st.session_state[wkey] = 0.0
            rcols[j + 1].number_input(
                label=wkey, key=wkey, step=1.0, format="%.0f",
                label_visibility="collapsed",
            )


def _example_two():
    st.info(_E2_NOTICE)

    st.markdown(
        "**The shipping network** — every value you need to build the matrix "
        "is labeled here."
    )
    st.plotly_chart(_logistics_diagram(), use_container_width=True)

    st.markdown("---")
    st.markdown(
        "**Build the augmented matrix.** Six unknowns (one flow per route), "
        "one balance equation per node: flow in = flow out. Fill in each "
        "coefficient — **+1** if that route flows *into* the node, **−1** if "
        "it flows *out*, **0** if it doesn't touch that node."
    )

    _grid_display()

    c1, c2 = st.columns(2)
    with c1:
        st.button("Check", key="t05b_e2_check_btn", on_click=_check_grid_cb)
    with c2:
        st.button("Fill it in for me", key="t05b_e2_fill_btn", on_click=_fill_for_me_cb)

    check = st.session_state.get("t05b_e2_check_result")
    if check is not None:
        if not check:
            st.success("All six equations are correct.")
        else:
            wrong_names = [_E2_ROW_LABELS[i] for i in check]
            st.warning(
                f"Not quite — check {', '.join(wrong_names)}. "
                "Remember: +1 if the route flows into the node, −1 if it flows out."
            )

    if st.session_state.get("t05b_e2_ready") and st.session_state.get("t05b_e2_M"):
        st.markdown("---")
        st.markdown("**Reduce it** — same three moves, six unknowns.")
        workbench("t05b_e2", 6, solution_labels=_E2_LABELS)
