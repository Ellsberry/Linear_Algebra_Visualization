import plotly.graph_objects as go

from .eq_builder import equation_builder
from .circuit_parser import parse_circuit_equation, rows_equivalent


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
        height=420, margin=dict(l=10, r=10, t=10, b=10),
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
                       showarrow=False, font=dict(size=13, color="crimson"),
                       xanchor="center")
    fig.add_annotation(x=0.25, y=bmy - 0.55, text="<b>-</b>",
                       showarrow=False, font=dict(size=13, color="royalblue"),
                       xanchor="center")
    fig.add_annotation(x=0.5, y=bmy + 1.1, text="<b>V = 36 V</b>",
                       showarrow=False, font=dict(size=9), xanchor="center")

    # --- R1 box (top-left rail, centered x=2.25, y=7) ---
    fig.add_shape(type="rect", x0=1.65, y0=6.7, x1=2.85, y1=7.3,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=2.25, y=7.46, text="<b>R1 = 2 Ω</b>",
                       showarrow=False, font=dict(size=10))

    # --- R2 box (P->Q segment, centered x=5.25, y=7) ---
    fig.add_shape(type="rect", x0=4.5, y0=6.7, x1=6.0, y1=7.3,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=5.25, y=6.1, text="<b>R2 = 6 Ω</b>",
                       showarrow=False, font=dict(size=10))

    # --- R5 box (raised rail, centered x=5.25, y=8.2) ---
    fig.add_shape(type="rect", x0=4.5, y0=7.9, x1=6.0, y1=8.5,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=5.25, y=8.64, text="<b>R5 = 12 Ω</b>",
                       showarrow=False, font=dict(size=10))

    # --- Motor (R3) circle centered (3.5, 4), radius 0.5 ---
    fig.add_shape(type="circle", x0=3.0, y0=3.5, x1=4.0, y1=4.5,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=3.5, y=4.0, text="<b>M</b>",
                       showarrow=False, font=dict(size=13, color="#e6e6e6"))
    fig.add_annotation(x=3.5, y=3.1, text="motor R3=8 Ω",
                       showarrow=False, font=dict(size=9), xanchor="center",
                       bgcolor="rgba(30,33,41,0.8)", borderpad=1)

    # --- Lamp (R4) circle centered (7, 4), radius 0.5 ---
    fig.add_shape(type="circle", x0=6.5, y0=3.5, x1=7.5, y1=4.5,
                  line=dict(color="#aaa", width=1.5),
                  fillcolor="rgba(30,33,41,0.95)")
    fig.add_annotation(x=7.0, y=4.0, text="<b>X</b>",
                       showarrow=False, font=dict(size=13, color="#e6e6e6"))
    fig.add_annotation(x=7.0, y=3.1, text="lamp R4=4 Ω",
                       showarrow=False, font=dict(size=9), xanchor="center",
                       bgcolor="rgba(30,33,41,0.8)", borderpad=1)

    # --- Nodes P and Q (dots + labels) ---
    fig.add_trace(go.Scatter(x=[3.5, 7], y=[7, 7], mode="markers",
                             marker=dict(color="#e6e6e6", size=9),
                             showlegend=False, hoverinfo="skip"))
    fig.add_annotation(x=3.28, y=7.4, text="<b>P</b>",
                       showarrow=False, font=dict(size=12), xanchor="right")
    fig.add_annotation(x=7.18, y=7.4, text="<b>Q</b>",
                       showarrow=False, font=dict(size=12), xanchor="left")

    # --- Current arrows ---
    # I1 upward on left branch (below battery)
    fig.add_annotation(x=1, y=2.65, ax=1, ay=2.1,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=1.18, y=2.35, text="<b>I₁↑</b>",
                       showarrow=False, font=dict(size=16), xanchor="left")

    # I2 rightward along R2 (between P and R2 box left edge)
    fig.add_annotation(x=4.4, y=7, ax=3.7, ay=7,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=4.05, y=7.42, text="<b>I₂→</b>",
                       showarrow=False, font=dict(size=16))

    # I3 downward on motor branch (above motor circle)
    fig.add_annotation(x=3.5, y=5.1, ax=3.5, ay=5.65,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=3.65, y=5.32, text="<b>I₃↓</b>",
                       showarrow=False, font=dict(size=16), xanchor="left")

    # I4 downward on lamp branch (above lamp circle)
    fig.add_annotation(x=7, y=5.1, ax=7, ay=5.65,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=7.15, y=5.32, text="<b>I₄↓</b>",
                       showarrow=False, font=dict(size=16), xanchor="left")

    # I5 rightward on R5 raised rail (between P corner and R5 box left edge)
    fig.add_annotation(x=4.3, y=8.2, ax=3.7, ay=8.2,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=4.0, y=8.48, text="<b>I₅→</b>",
                       showarrow=False, font=dict(size=16))

    # --- Loop indicators ---
    fig.add_annotation(x=2.25, y=1.8, text="Loop 1 ↻",
                       showarrow=False, font=dict(size=11, color="#6aa3d5"),
                       bgcolor="rgba(30,33,41,0.75)", borderpad=3)
    fig.add_annotation(x=5.25, y=1.8, text="Loop 2 ↻",
                       showarrow=False, font=dict(size=11, color="#6aa3d5"),
                       bgcolor="rgba(30,33,41,0.75)", borderpad=3)
    fig.add_annotation(x=5.25, y=7.62, text="Loop 3 ↻",
                       showarrow=False, font=dict(size=11, color="#6aa3d5"),
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
        intro_md=("You're solving for the five branch currents I1..I5. Read the "
                  "circuit, then write each node's KCL equation (current in = current "
                  "out) and each marked loop's KVL equation. Use the resistor and "
                  "source symbols, e.g. `R1*I1 + R3*I3 = V`."),
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
