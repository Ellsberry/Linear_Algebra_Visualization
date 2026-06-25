"""
Topic 5.5 -- Elimination & Triangular Form.

Pattern: MULTI-EXAMPLE (3 screens).
Stage 2: workbench + Screen 1 + Screen 2 (Logistics). Screen 3 is a stub.
"""
import plotly.graph_objects as go
import streamlit as st

from engine import plotting as plot
from .screen_workbench import _example_one
from .workbench import workbench, _load_aug

TITLE = "5.5 · Elimination & Triangular Form"
SLUG = "elimination"

OVERVIEW = """
Topic 5 ended at the edge of what we can draw — three unknowns, three planes.
This topic is the method that goes further. We simplify the system's augmented
matrix `[A | b]` with three reversible moves — swap rows, scale a row, add a
multiple of one row to another — until it's **upper triangular** (zeros below
the diagonal). Then we read the answer off from the bottom row up
(**back-substitution**). The moves never change the answer, so it's always safe
to experiment. First on a 3×3 you can still relate to planes, then on a
six-variable shipping network and a circuit you *can't* picture — where the
procedure is the only way through.
"""

HOWTO = """
Use **Do one step** / **Run to triangular form** to watch the standard method,
or compose your own row operations in **manual** mode. The banner tells you when
you've hit a special case (no solution, or infinitely many). Once the matrix is
triangular, **back-substitute** to solve. **Undo** and **Reset** make
experimenting safe.
"""



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
    """Static plotly diagram of the 6-route shipping network."""
    fig = go.Figure()
    fig.update_layout(
        height=340, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
        xaxis=dict(range=[-0.5, 10.5], visible=False),
        yaxis=dict(range=[0.8, 10.5], visible=False),
    )

    F  = [5.0, 9.3];  W1 = [2.0, 5.8];  W2 = [8.0, 5.8]
    A  = [0.5, 2.2];  B  = [3.5, 2.2];  C  = [6.5, 2.2];  D = [9.5, 2.2]

    routes = [
        (F,  W1, "x₁", "royalblue",    ( 0.55,  0.0)),
        (F,  W2, "x₂", "seagreen",     (-0.55,  0.0)),
        (W1, A,  "x₃", "darkorange",   (-0.55,  0.1)),
        (W1, B,  "x₄", "crimson",      ( 0.55,  0.1)),
        (W2, C,  "x₅", "mediumorchid", (-0.55,  0.1)),
        (W2, D,  "x₆", "#8B6914",      ( 0.55,  0.1)),
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
        fig.add_annotation(x=pos[0], y=pos[1] + 0.45, text=f"<b>{name}</b>",
                           showarrow=False, font=dict(size=12),
                           bgcolor="rgba(30,33,41,0.85)", borderpad=3)

    for name, pos, demand in [("A", A, 30), ("B", B, 20), ("C", C, 25), ("D", D, 25)]:
        plot.add_point_2d(fig, pos, "#2E7D32", name, size=20)
        fig.add_annotation(x=pos[0], y=pos[1] - 0.45, showarrow=False,
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


# ---------------------------------------------------------------------------
# Screen 3 — Circuit (fill values, 3 currents)
# ---------------------------------------------------------------------------

# Correct augmented matrix for the circuit: A=[[1,-1,-1],[2,4,0],[0,4,-4]], b=(0,12,0)
_E3_AUG = [
    [ 1.0, -1.0, -1.0,  0.0],   # KCL node:  I1 - I2 - I3 = 0
    [ 2.0,  4.0,  0.0, 12.0],   # KVL loop 1: R1*I1 + R2*I2 = V
    [ 0.0,  4.0, -4.0,  0.0],   # KVL loop 2: R2*I2 - R3*I3 = 0
]

_E3_NOTICE = """
The unknowns are the currents. The same "what flows in must flow out" idea as
the shipping network — electricity and freight obey the same linear algebra.
Here the signs are set up for you; you just read the resistor and battery values
off the diagram.
"""


def _circuit_diagram():
    """Static plotly schematic of the DC circuit."""
    fig = go.Figure()
    fig.update_layout(
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
        xaxis=dict(range=[-0.5, 11.5], visible=False),
        yaxis=dict(range=[0.0, 7.2], visible=False),
    )

    # Node coordinates
    TL = (0.5, 5.5); TR2 = (9.5, 5.5)
    BL = (0.5, 1.0); BR  = (9.5, 1.0)
    A  = (5.0, 5.5); AB  = (5.0, 1.0)   # node A top/bottom of R2 branch

    def _line(x0, y0, x1, y1):
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color="#aaa", width=2))

    # Wires
    _line(*TL, *TR2)           # top rail
    _line(*TL, *BL)            # left side (battery)
    _line(*BL, *BR)            # bottom rail
    _line(*TR2, *BR)           # right branch (R3)
    _line(A[0], A[1], AB[0], AB[1])  # middle branch (R2)

    # Battery symbol (left side, midpoint y=3.25)
    bx = TL[0]; bmy = (TL[1] + BL[1]) / 2
    _line(bx - 0.45, bmy + 0.3, bx + 0.45, bmy + 0.3)   # long bar (positive)
    _line(bx - 0.25, bmy - 0.3, bx + 0.25, bmy - 0.3)   # short bar (negative)
    fig.add_annotation(x=bx - 0.7, y=bmy + 0.45, text="<b>+</b>",
                       showarrow=False, font=dict(size=14, color="crimson"), xanchor="right")
    fig.add_annotation(x=bx - 0.7, y=bmy - 0.45, text="<b>−</b>",
                       showarrow=False, font=dict(size=14, color="royalblue"), xanchor="right")
    fig.add_annotation(x=bx - 0.9, y=bmy, text="<b>V=12</b>",
                       showarrow=False, font=dict(size=12), xanchor="right")

    # R1 box on top rail between TL and A
    r1x = (TL[0] + A[0]) / 2   # 2.75
    fig.add_shape(type="rect", x0=r1x - 0.75, y0=TL[1] - 0.35,
                  x1=r1x + 0.75, y1=TL[1] + 0.35,
                  line=dict(color="black", width=2), fillcolor="rgba(30,33,41,0.9)")
    fig.add_annotation(x=r1x, y=TL[1] + 0.75, text="<b>R1=2 Ω</b>",
                       showarrow=False, font=dict(size=11))

    # I1 arrow: left of R1 on top rail
    fig.add_annotation(x=1.5, y=TL[1], ax=0.9, ay=TL[1],
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6")
    fig.add_annotation(x=1.2, y=TL[1] - 0.55, text="<b>I₁→</b>",
                       showarrow=False, font=dict(size=12))

    # Node A dot and label
    fig.add_trace(go.Scatter(x=[A[0]], y=[A[1]], mode="markers",
                             marker=dict(color="#e6e6e6", size=9),
                             showlegend=False, hoverinfo="skip"))
    fig.add_annotation(x=A[0], y=A[1] + 0.55, text="<b>Node A</b>",
                       showarrow=False, font=dict(size=11))

    # R2 box on middle branch
    r2y = (A[1] + AB[1]) / 2   # 3.25
    fig.add_shape(type="rect", x0=A[0] - 0.35, y0=r2y - 0.75,
                  x1=A[0] + 0.35, y1=r2y + 0.75,
                  line=dict(color="black", width=2), fillcolor="rgba(30,33,41,0.9)")
    fig.add_annotation(x=A[0] + 0.85, y=r2y, text="<b>R2=4 Ω</b>",
                       showarrow=False, font=dict(size=11), xanchor="left")
    # I2 arrow
    fig.add_annotation(x=A[0], y=r2y + 1.4, ax=A[0], ay=r2y + 1.95,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="seagreen")
    fig.add_annotation(x=A[0] + 0.55, y=r2y + 1.85, text="<b>I₂↓</b>",
                       showarrow=False, font=dict(size=12, color="seagreen"))

    # R3 box on right branch
    r3y = (TR2[1] + BR[1]) / 2   # 3.25
    fig.add_shape(type="rect", x0=TR2[0] - 0.35, y0=r3y - 0.75,
                  x1=TR2[0] + 0.35, y1=r3y + 0.75,
                  line=dict(color="black", width=2), fillcolor="rgba(30,33,41,0.9)")
    fig.add_annotation(x=TR2[0] + 0.85, y=r3y, text="<b>R3=4 Ω</b>",
                       showarrow=False, font=dict(size=11), xanchor="left")
    # I3 arrow
    fig.add_annotation(x=TR2[0], y=r3y + 1.4, ax=TR2[0], ay=r3y + 1.95,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="crimson")
    fig.add_annotation(x=TR2[0] + 0.55, y=r3y + 1.85, text="<b>I₃↓</b>",
                       showarrow=False, font=dict(size=12, color="crimson"))

    return fig


def _circuit_matrix_latex(r1, r2, r3, v):
    """LaTeX for the circuit augmented matrix, showing variable names for zero entries."""
    def _val(x, name):
        if abs(float(x)) < 1e-9:
            return rf"\textit{{{name}}}"
        xf = float(x)
        return str(int(round(xf))) if abs(xf - round(xf)) < 1e-9 else f"{xf:.4g}"

    def _neg(x, name):
        if abs(float(x)) < 1e-9:
            return rf"-\textit{{{name}}}"
        xf = float(x)
        s = str(int(round(xf))) if abs(xf - round(xf)) < 1e-9 else f"{xf:.4g}"
        return f"-{s}"

    R1 = _val(r1, "R_1"); R2 = _val(r2, "R_2"); nR3 = _neg(r3, "R_3"); V = _val(v, "V")
    return (
        r"\left[\begin{array}{ccc|c}"
        rf"1 & -1 & -1 & 0 \\"
        rf"{R1} & {R2} & 0 & {V} \\"
        rf"0 & {R2} & {nR3} & 0"
        r"\end{array}\right]"
    )


def _load_circuit():
    _load_aug("t05b_e3", _E3_AUG)


def _check_circuit_cb():
    r1 = float(st.session_state.get("t05b_e3_R1", 0))
    r2 = float(st.session_state.get("t05b_e3_R2", 0))
    r3 = float(st.session_state.get("t05b_e3_R3", 0))
    v  = float(st.session_state.get("t05b_e3_V",  0))
    wrong = []
    if abs(r1 - 2) > 1e-9: wrong.append("R1")
    if abs(r2 - 4) > 1e-9: wrong.append("R2")
    if abs(r3 - 4) > 1e-9: wrong.append("R3")
    if abs(v - 12) > 1e-9: wrong.append("V")
    st.session_state["t05b_e3_check_result"] = wrong
    if not wrong:
        _load_circuit()
        st.session_state["t05b_e3_ready"] = True


def _fill_circuit_cb():
    st.session_state["t05b_e3_R1"] = 2.0
    st.session_state["t05b_e3_R2"] = 4.0
    st.session_state["t05b_e3_R3"] = 4.0
    st.session_state["t05b_e3_V"]  = 12.0
    st.session_state["t05b_e3_check_result"] = []
    _load_circuit()
    st.session_state["t05b_e3_ready"] = True


def _example_three():
    st.info(_E3_NOTICE)

    st.markdown(
        "**The circuit** — read the values (V, R1, R2, R3) and the current "
        "directions off the diagram."
    )
    st.plotly_chart(_circuit_diagram(), use_container_width=True)

    st.markdown("---")
    st.markdown(
        "**Fill in the values.** The equation structure and signs are already "
        "placed — you just read V, R1, R2, R3 from the diagram and type them. "
        "Notice R2 appears in both loop equations."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        r1 = st.number_input("R1 (Ω)", min_value=0.0, step=1.0, format="%.1f",
                             key="t05b_e3_R1")
    with c2:
        r2 = st.number_input("R2 (Ω)", min_value=0.0, step=1.0, format="%.1f",
                             key="t05b_e3_R2")
    with c3:
        r3 = st.number_input("R3 (Ω)", min_value=0.0, step=1.0, format="%.1f",
                             key="t05b_e3_R3")
    with c4:
        v  = st.number_input("V (volts)", min_value=0.0, step=1.0, format="%.1f",
                             key="t05b_e3_V")

    st.latex(_circuit_matrix_latex(r1, r2, r3, v))

    cc1, cc2 = st.columns(2)
    with cc1:
        st.button("Check", key="t05b_e3_check_btn", on_click=_check_circuit_cb)
    with cc2:
        st.button("Fill it in for me", key="t05b_e3_fill_btn", on_click=_fill_circuit_cb)

    check = st.session_state.get("t05b_e3_check_result")
    if check is not None:
        if not check:
            st.success("All four values are correct.")
        else:
            st.warning(
                f"Not quite — check {', '.join(check)}. "
                "Read the labeled values from the diagram."
            )

    if st.session_state.get("t05b_e3_ready") and st.session_state.get("t05b_e3_M"):
        st.markdown("---")
        st.markdown("**Reduce it** — same three moves, three currents.")
        workbench("t05b_e3", 3,
                  solution_labels=["I₁", "I₂", "I₃"],
                  solution_suffix=" A")

    st.info(
        "This circuit runs on steady (DC) current, so the answers are plain numbers. "
        "In **Topic 9** the *same circuit* on alternating current uses **complex numbers** "
        "to capture both the size and the timing of each current — same question, richer answer.",
        icon="\U0001f52e",
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)
    with st.expander("How to use this screen"):
        st.markdown(HOWTO)

    example = st.radio(
        "Example",
        ["1 · The workbench", "2 · Logistics", "3 · Circuit"],
        horizontal=True,
        key="t05b_example",
    )
    st.divider()

    if example.startswith("1"):
        _example_one()
    elif example.startswith("2"):
        _example_two()
    else:
        _example_three()
