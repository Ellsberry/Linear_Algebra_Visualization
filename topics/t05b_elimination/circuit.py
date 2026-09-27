import streamlit as st
import plotly.graph_objects as go

from .eq_builder import equation_builder
from .circuit_parser import parse_circuit_equation, parse_circuit_equation_p2, rows_equivalent


# ---------------------------------------------------------------------------
# Screen 3 — Circuit (KCL/KVL symbolic equations, 5 currents)
# ---------------------------------------------------------------------------

_E3_AUG = [
    [ 1, -1, -1,  0, -1,  0],   # KCL P: I1 - I2 - I3 - I5 = 0
    [ 0,  1,  0, -1,  1,  0],   # KCL Q: I2 - I4 + I5 = 0
    [ 2,  0,  8,  0,  0, 36],   # KVL1: R1 I1 + R3 I3 = V
    [ 0,  6, -8,  4,  0,  0],   # KVL2: R2 I2 - R3 I3 + R4 I4 = 0
    [ 0,  6,  0,  0,-12,  0],   # KVL3: R2 I2 - R5 I5 = 0
]
_E3_ROW_LABELS = ["KCL node P", "KCL node Q", "Loop 1 (battery)", "Loop 2", "Loop 3"]
_E3_LABELS     = ["I1", "I2", "I3", "I4", "I5"]


def _circuit_diagram():
    """Static plotly schematic of the redesigned DC circuit (V=36, 5 branches, nodes P and Q)."""
    fig = go.Figure()
    fig.update_layout(
        height=520, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
        xaxis=dict(range=[-0.5, 8], visible=False),
        yaxis=dict(range=[0, 9], visible=False, scaleanchor="x", scaleratio=1),
    )

    def _wire(x0, y0, x1, y1):
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color="#aaa", width=2))

    # --- Wires ---
    _wire(1, 1, 7, 1)          # ground rail
    _wire(1, 1, 1, 7)          # left vertical (battery branch)
    _wire(1, 7, 3.5, 7)        # top-left rail (battery+ to P)
    _wire(3.5, 7, 3.5, 1)      # motor branch (P down to ground)
    _wire(7, 7, 7, 1)          # lamp branch (Q down to ground)
    _wire(3.5, 7, 7, 7)        # R2 direct path P->Q
    _wire(3.5, 7, 3.5, 8.2)    # R5 raised: left up from P
    _wire(3.5, 8.2, 7, 8.2)    # R5 raised: horizontal
    _wire(7, 8.2, 7, 7)        # R5 raised: right down to Q

    # --- Battery (left vertical, centered at y=4) ---
    bmy = 4.0
    _wire(0.52, bmy + 0.3, 1.48, bmy + 0.3)   # long bar (+, positive)
    _wire(0.72, bmy - 0.3, 1.28, bmy - 0.3)   # short bar (-, negative)
    fig.add_annotation(x=0.25, y=bmy + 0.55, text="<b>+</b>",
                       showarrow=False, font=dict(size=18, color="crimson"),
                       xanchor="center")
    fig.add_annotation(x=0.25, y=bmy - 0.55, text="<b>-</b>",
                       showarrow=False, font=dict(size=18, color="royalblue"),
                       xanchor="center")
    fig.add_annotation(x=0.5, y=bmy + 1.1, text="<b>V = 36 V</b>",
                       showarrow=False, font=dict(size=14), xanchor="center")

    # --- R1 box (top-left rail, centered x=2.25, y=7) ---
    fig.add_shape(type="rect", x0=1.65, y0=6.7, x1=2.85, y1=7.3,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=2.25, y=7.46, text="<b>R1 = 2 Ω</b>",
                       showarrow=False, font=dict(size=15))

    # --- R2 box (P->Q segment, centered x=5.25, y=7) ---
    fig.add_shape(type="rect", x0=4.5, y0=6.7, x1=6.0, y1=7.3,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=5.25, y=6.1, text="<b>R2 = 6 Ω</b>",
                       showarrow=False, font=dict(size=15))

    # --- R5 box (raised rail, centered x=5.25, y=8.2) ---
    fig.add_shape(type="rect", x0=4.5, y0=7.9, x1=6.0, y1=8.5,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=5.25, y=8.64, text="<b>R5 = 12 Ω</b>",
                       showarrow=False, font=dict(size=15))

    # --- Motor (R3) circle centered (3.5, 4), radius 0.5 ---
    fig.add_shape(type="circle", x0=3.0, y0=3.5, x1=4.0, y1=4.5,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=3.5, y=4.0, text="<b>M</b>",
                       showarrow=False, font=dict(size=18, color="#e6e6e6"))
    fig.add_annotation(x=3.5, y=3.1, text="motor R3=8 Ω",
                       showarrow=False, font=dict(size=14), xanchor="center",
                       bgcolor="rgba(30,33,41,0.8)", borderpad=1)

    # --- Lamp (R4) circle centered (7, 4), radius 0.5 ---
    fig.add_shape(type="circle", x0=6.5, y0=3.5, x1=7.5, y1=4.5,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=7.0, y=4.0, text="<b>X</b>",
                       showarrow=False, font=dict(size=18, color="#e6e6e6"))
    fig.add_annotation(x=7.0, y=3.1, text="lamp R4=4 Ω",
                       showarrow=False, font=dict(size=14), xanchor="center",
                       bgcolor="rgba(30,33,41,0.8)", borderpad=1)

    # --- Nodes P and Q (dots + labels) ---
    fig.add_trace(go.Scatter(x=[3.5, 7], y=[7, 7], mode="markers",
                             marker=dict(color="#e6e6e6", size=9),
                             showlegend=False, hoverinfo="skip"))
    fig.add_annotation(x=3.28, y=7.4, text="<b>P</b>",
                       showarrow=False, font=dict(size=17), xanchor="right")
    fig.add_annotation(x=7.18, y=7.4, text="<b>Q</b>",
                       showarrow=False, font=dict(size=17), xanchor="left")

    # --- Current arrows ---
    # I1 upward on left branch (below battery)
    fig.add_annotation(x=1, y=2.65, ax=1, ay=2.1,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=1.18, y=2.35, text="<b>I₁↑</b>",
                       showarrow=False, font=dict(size=20), xanchor="left")

    # I2 rightward along R2 (between P and R2 box left edge)
    fig.add_annotation(x=4.4, y=7, ax=3.7, ay=7,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=4.05, y=7.42, text="<b>I₂→</b>",
                       showarrow=False, font=dict(size=20))

    # I3 downward on motor branch (above motor circle)
    fig.add_annotation(x=3.5, y=5.1, ax=3.5, ay=5.65,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=3.65, y=5.32, text="<b>I₃↓</b>",
                       showarrow=False, font=dict(size=20), xanchor="left")

    # I4 downward on lamp branch (above lamp circle)
    fig.add_annotation(x=7, y=5.1, ax=7, ay=5.65,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=7.15, y=5.32, text="<b>I₄↓</b>",
                       showarrow=False, font=dict(size=20), xanchor="left")

    # I5 rightward on R5 raised rail (between P corner and R5 box left edge)
    fig.add_annotation(x=4.3, y=8.2, ax=3.7, ay=8.2,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=4.0, y=8.48, text="<b>I₅→</b>",
                       showarrow=False, font=dict(size=20))

    # --- Loop indicators ---
    fig.add_annotation(x=2.25, y=1.8, text="Loop 1 ↻",
                       showarrow=False, font=dict(size=15, color="#6aa3d5"),
                       bgcolor="rgba(30,33,41,0.75)", borderpad=3)
    fig.add_annotation(x=5.25, y=1.8, text="Loop 2 ↻",
                       showarrow=False, font=dict(size=15, color="#6aa3d5"),
                       bgcolor="rgba(30,33,41,0.75)", borderpad=3)
    fig.add_annotation(x=5.25, y=7.62, text="Loop 3 ↻",
                       showarrow=False, font=dict(size=15, color="#6aa3d5"),
                       bgcolor="rgba(30,33,41,0.75)", borderpad=3)

    return fig


# ---------------------------------------------------------------------------
# Screen 3 -- Circuit Problem 2 (KCL/KVL symbolic equations, 7 currents, 2 batteries)
# ---------------------------------------------------------------------------

_E3B_AUG = [
    [ 1, -1, -1,  0,  0,  0,  0,  0],   # KCL P: I1 - I2 - I3 = 0
    [ 0,  0,  1, -1, -1,  0,  0,  0],   # KCL Q: I3 - I4 - I5 = 0
    [ 0,  0,  0,  0,  1, -1, -1,  0],   # KCL S: I5 - I6 - I7 = 0
    [ 6,  3,  0,  0,  0,  0,  0, 24],   # Loop 1: R1 I1 + R2 I2 = V1
    [ 0, -3,  2,  2,  0,  0,  0,  0],   # Loop 2: R3 I3 + R4 I4 - R2 I2 = 0
    [ 0,  0,  0, -2,  2,  6,  0,  0],   # Loop 3: R5 I5 + R6 I6 - R4 I4 = 0
    [ 0,  0,  0,  0,  0, -6,  6, -18],  # Loop 4: R7 I7 - R6 I6 = -V2
]
_E3B_ROW_LABELS = ["KCL node P", "KCL node Q", "KCL node S", "Loop 1 (battery V1)",
                   "Loop 2", "Loop 3", "Loop 4 (battery V2)"]
_E3B_LABELS     = ["I1", "I2", "I3", "I4", "I5", "I6", "I7"]


def _circuit_diagram_p2():
    """Static plotly schematic of Circuit Problem 2 (two batteries, 7 branches, nodes P/Q/S)."""
    fig = go.Figure()
    fig.update_layout(
        height=520, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6"),
        xaxis=dict(range=[-0.5, 12], visible=False),
        yaxis=dict(range=[0, 9], visible=False, scaleanchor="x", scaleratio=1),
    )

    def _wire(x0, y0, x1, y1):
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color="#aaa", width=2))

    # --- Wires ---
    _wire(1, 1, 11, 1)         # ground rail
    _wire(1, 1, 1, 7)          # left battery branch
    _wire(11, 1, 11, 7)        # right battery branch
    _wire(1, 7, 11, 7)         # top rail (R1, P, R3, Q, R5/lamp, S, R7)
    _wire(3.5, 7, 3.5, 1)      # R2 rung (node P to ground)
    _wire(6.0, 7, 6.0, 1)      # R4 rung (node Q to ground)
    _wire(8.5, 7, 8.5, 1)      # R6/motor rung (node S to ground)

    # --- Battery V1 (left vertical, centered at y=4) ---
    bmy = 4.0
    _wire(0.52, bmy + 0.3, 1.48, bmy + 0.3)   # long bar (+, positive)
    _wire(0.72, bmy - 0.3, 1.28, bmy - 0.3)   # short bar (-, negative)
    fig.add_annotation(x=0.25, y=bmy + 0.55, text="<b>+</b>",
                       showarrow=False, font=dict(size=18, color="crimson"),
                       xanchor="center")
    fig.add_annotation(x=0.25, y=bmy - 0.55, text="<b>-</b>",
                       showarrow=False, font=dict(size=18, color="royalblue"),
                       xanchor="center")
    fig.add_annotation(x=0.5, y=bmy + 1.1, text="<b>V1 = 24 V</b>",
                       showarrow=False, font=dict(size=14), xanchor="center")

    # --- Battery V2 (right vertical, centered at y=4, mirrored) ---
    _wire(10.52, bmy + 0.3, 11.48, bmy + 0.3)   # long bar (+, positive), near top rail
    _wire(10.72, bmy - 0.3, 11.28, bmy - 0.3)   # short bar (-, negative), near ground
    fig.add_annotation(x=11.75, y=bmy + 0.55, text="<b>+</b>",
                       showarrow=False, font=dict(size=18, color="crimson"),
                       xanchor="center")
    fig.add_annotation(x=11.75, y=bmy - 0.55, text="<b>-</b>",
                       showarrow=False, font=dict(size=18, color="royalblue"),
                       xanchor="center")
    fig.add_annotation(x=11.5, y=bmy + 1.1, text="<b>V2 = 18 V</b>",
                       showarrow=False, font=dict(size=14), xanchor="center")

    # --- R1 box (top rail, centered x=2.25) ---
    fig.add_shape(type="rect", x0=1.65, y0=6.7, x1=2.85, y1=7.3,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=2.25, y=7.46, text="<b>R1 = 6 Ω</b>",
                       showarrow=False, font=dict(size=15))

    # --- R3 box (top rail, centered x=4.75) ---
    fig.add_shape(type="rect", x0=4.15, y0=6.7, x1=5.35, y1=7.3,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=4.75, y=7.46, text="<b>R3 = 2 Ω</b>",
                       showarrow=False, font=dict(size=15))

    # --- R7 box (top rail, centered x=9.75) ---
    fig.add_shape(type="rect", x0=9.15, y0=6.7, x1=10.35, y1=7.3,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=9.75, y=7.46, text="<b>R7 = 6 Ω</b>",
                       showarrow=False, font=dict(size=15))

    # --- Lamp (R5) circle, inline on top rail, centered x=7.25 ---
    fig.add_shape(type="circle", x0=6.75, y0=6.5, x1=7.75, y1=7.5,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=7.25, y=7.0, text="<b>X</b>",
                       showarrow=False, font=dict(size=18, color="#e6e6e6"))
    fig.add_annotation(x=7.25, y=6.1, text="lamp R5=2 Ω",
                       showarrow=False, font=dict(size=14), xanchor="center",
                       bgcolor="rgba(30,33,41,0.8)", borderpad=1)

    # --- R2 box (rung at node P, centered y=4) ---
    fig.add_shape(type="rect", x0=3.2, y0=3.4, x1=3.8, y1=4.6,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=4.15, y=4.0, text="<b>R2 = 3 Ω</b>",
                       showarrow=False, font=dict(size=15), xanchor="left")

    # --- R4 box (rung at node Q, centered y=4) ---
    fig.add_shape(type="rect", x0=5.7, y0=3.4, x1=6.3, y1=4.6,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=6.65, y=4.0, text="<b>R4 = 2 Ω</b>",
                       showarrow=False, font=dict(size=15), xanchor="left")

    # --- Motor (R6) circle, rung at node S, centered (8.5, 4) ---
    fig.add_shape(type="circle", x0=8.0, y0=3.5, x1=9.0, y1=4.5,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=8.5, y=4.0, text="<b>M</b>",
                       showarrow=False, font=dict(size=18, color="#e6e6e6"))
    fig.add_annotation(x=8.5, y=3.1, text="motor R6=6 Ω",
                       showarrow=False, font=dict(size=14), xanchor="center",
                       bgcolor="rgba(30,33,41,0.8)", borderpad=1)

    # --- Nodes P, Q, S (dots + labels) ---
    fig.add_trace(go.Scatter(x=[3.5, 6.0, 8.5], y=[7, 7, 7], mode="markers",
                             marker=dict(color="#e6e6e6", size=9),
                             showlegend=False, hoverinfo="skip"))
    fig.add_annotation(x=3.5, y=7.4, text="<b>P</b>",
                       showarrow=False, font=dict(size=17), xanchor="center")
    fig.add_annotation(x=6.0, y=7.4, text="<b>Q</b>",
                       showarrow=False, font=dict(size=17), xanchor="center")
    fig.add_annotation(x=8.5, y=7.4, text="<b>S</b>",
                       showarrow=False, font=dict(size=17), xanchor="center")

    # --- Current arrows ---
    # I1 upward on left branch (below battery)
    fig.add_annotation(x=1, y=2.65, ax=1, ay=2.1,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=1.18, y=2.35, text="<b>I₁↑</b>",
                       showarrow=False, font=dict(size=20), xanchor="left")

    # I2 downward on R2 rung (between node P and R2 box)
    fig.add_annotation(x=3.5, y=5.6, ax=3.5, ay=6.3,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=3.65, y=5.9, text="<b>I₂↓</b>",
                       showarrow=False, font=dict(size=20), xanchor="left")

    # I3 rightward on top rail (between node P and R3 box)
    fig.add_annotation(x=4.05, y=7, ax=3.75, ay=7,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=3.9, y=7.42, text="<b>I₃→</b>",
                       showarrow=False, font=dict(size=20))

    # I4 downward on R4 rung (between node Q and R4 box)
    fig.add_annotation(x=6.0, y=5.6, ax=6.0, ay=6.3,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=6.15, y=5.9, text="<b>I₄↓</b>",
                       showarrow=False, font=dict(size=20), xanchor="left")

    # I5 rightward on top rail (between node Q and lamp)
    fig.add_annotation(x=6.55, y=7, ax=6.25, ay=7,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=6.4, y=7.42, text="<b>I₅→</b>",
                       showarrow=False, font=dict(size=20))

    # I6 downward on motor rung (between node S and motor circle)
    fig.add_annotation(x=8.5, y=5.6, ax=8.5, ay=6.3,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=8.65, y=5.9, text="<b>I₆↓</b>",
                       showarrow=False, font=dict(size=20), xanchor="left")

    # I7 downward on right branch (below top rail, away from node S toward battery V2)
    fig.add_annotation(x=11, y=5.6, ax=11, ay=6.3,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=11.18, y=5.9, text="<b>I₇↓</b>",
                       showarrow=False, font=dict(size=20), xanchor="left")

    # --- Loop indicators ---
    fig.add_annotation(x=2.25, y=1.8, text="Loop 1 ↻",
                       showarrow=False, font=dict(size=15, color="#6aa3d5"),
                       bgcolor="rgba(30,33,41,0.75)", borderpad=3)
    fig.add_annotation(x=4.75, y=1.8, text="Loop 2 ↻",
                       showarrow=False, font=dict(size=15, color="#6aa3d5"),
                       bgcolor="rgba(30,33,41,0.75)", borderpad=3)
    fig.add_annotation(x=7.25, y=1.8, text="Loop 3 ↻",
                       showarrow=False, font=dict(size=15, color="#6aa3d5"),
                       bgcolor="rgba(30,33,41,0.75)", borderpad=3)
    fig.add_annotation(x=9.75, y=1.8, text="Loop 4 ↻",
                       showarrow=False, font=dict(size=15, color="#6aa3d5"),
                       bgcolor="rgba(30,33,41,0.75)", borderpad=3)

    return fig


def _example_three():
    equation_builder(
        key="t05b_e3",
        n_unknowns=5,
        target_aug=_E3_AUG,
        row_labels=_E3_ROW_LABELS,
        diagram_fn=_circuit_diagram,
        solution_labels=_E3_LABELS,
        var_name="I",
        intro_md=(
            "**Circuit.** You have an electronic circuit and need to determine if the current "
            "through your lamps and motors will not burn them out. To do this, find the 5 "
            "currents I₁…I₅ (the arrows show which way each flows). You'll write 5 "
            "equations — one for each node (P and Q) and one for each marked loop (1, 2, 3) "
            "— then elimination solves for the 5 currents.\n\n"
            "**Node rule (KCL, Kirchhoff's Current Law): what flows in must flow out.** At a "
            "node, add the currents whose arrows point into the node and subtract the currents "
            "pointing out. This must equal zero. At node P, I₁ comes in and I₂, "
            "I₃, I₅ go out, so: `I1 - I2 - I3 - I5 = 0`.\n\n"
            "**Loop rule (KVL, Kirchhoff's Voltage Law): voltage drops around any closed loop "
            "sum to zero.** You find the voltage drop across a resistor by multiplying its "
            "resistance times its current (R×I). The battery has its own voltage drop. "
            "Follow the marked clockwise loops (↻). In Loop 1, sum the voltage drops across "
            "the resistors; because you go clockwise you reach the battery's negative side "
            "first, so you subtract the battery voltage. Add the drops and set the total to "
            "zero. So Loop 1 is: `R1*I1 + R3*I3 - 36 = 0`. Loop 3 goes through R2 and R5 with "
            "no battery: `R5*I5 - R2*I2 = 0` (the minus is because you go around clockwise, and "
            "the diagram shows that clockwise direction is against current I₂)."
        ),
        reduce_caption="**Reduce it** -- same three moves, five currents.",
        parse_fn=parse_circuit_equation,
        equiv_fn=rows_equivalent,
        placeholder="e.g. R1*I1 + R3*I3 = V",
        fill_equations=[
            "I1 - I2 - I3 - I5 = 0",
            "I2 - I4 + I5 = 0",
            "R1*I1 + R3*I3 = V",
            "R2*I2 - R3*I3 + R4*I4 = 0",
            "R2*I2 - R5*I5 = 0",
        ],
        closing_md=("**One definite answer.** Elimination drives this to a single "
                    "solution: I = (6, 2, 3, 3, 1) A. The same method that solved the "
                    "freight network solves the circuit -- and in Topic 9, the very "
                    "same circuit on alternating current uses complex numbers for a "
                    "richer answer."),
    )

    st.markdown("---")
    st.markdown("## Circuit Problem 2 -- two batteries, four loops")
    equation_builder(
        key="t05b_e3b",
        n_unknowns=7,
        target_aug=_E3B_AUG,
        row_labels=_E3B_ROW_LABELS,
        diagram_fn=_circuit_diagram_p2,
        solution_labels=_E3B_LABELS,
        var_name="I",
        intro_md=(
            "**A bigger circuit.** This one has TWO batteries (V1 and V2) and three "
            "nodes (P, Q, S), which makes four loops instead of three. The rules "
            "don't change: at each node, what flows in must flow out (KCL), and "
            "around each closed loop, the voltage drops must sum to zero (KVL). You "
            "still need one equation per node and one per loop -- seven equations "
            "for the seven currents I₁…I₇.\n\n"
            "**Worked node example.** At node P, I₁ comes in and I₂, I₃ go out, so: "
            "`I1 - I2 - I3 = 0`.\n\n"
            "**Worked loop example.** Loop 1 (↻) is the leftmost loop, containing "
            "battery V1, resistor R1, and resistor R2. Going clockwise, you add the "
            "drops across R1 and R2 and set that equal to the battery's push: "
            "`R1*I1 + R2*I2 = V1`.\n\n"
            "**Watch for negative answers.** With two batteries pushing against each "
            "other through the shared branches, some currents come out NEGATIVE. "
            "That doesn't mean you did something wrong -- it means the real current "
            "flows opposite the arrow we drew, because the second battery pushes "
            "back against it."
        ),
        reduce_caption="**Reduce it** -- seven currents, two batteries.",
        parse_fn=parse_circuit_equation_p2,
        equiv_fn=rows_equivalent,
        placeholder="e.g. R1*I1 + R2*I2 = V1",
        fill_equations=[
            "I1 - I2 - I3 = 0",
            "I3 - I4 - I5 = 0",
            "I5 - I6 - I7 = 0",
            "R1*I1 + R2*I2 = V1",
            "R3*I3 + R4*I4 - R2*I2 = 0",
            "R5*I5 + R6*I6 - R4*I4 = 0",
            "R7*I7 - R6*I6 = -V2",
        ],
        closing_md=("**One definite answer.** I = (3, 2, 1, 2, -1, 1, -2) A. The "
                    "negative currents (I₅, I₇) flow opposite the arrows we drew -- "
                    "the math tells you the true direction."),
    )
