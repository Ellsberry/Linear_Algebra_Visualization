import plotly.graph_objects as go
import streamlit as st

from .workbench import workbench, _load_aug


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
                       showarrow=False, font=dict(size=11), xanchor="left")

    # I2 rightward along R2 (between P and R2 box left edge)
    fig.add_annotation(x=4.4, y=7, ax=3.7, ay=7,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=4.05, y=7.42, text="<b>I₂→</b>",
                       showarrow=False, font=dict(size=11))

    # I3 downward on motor branch (above motor circle)
    fig.add_annotation(x=3.5, y=5.1, ax=3.5, ay=5.65,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=3.65, y=5.32, text="<b>I₃↓</b>",
                       showarrow=False, font=dict(size=11), xanchor="left")

    # I4 downward on lamp branch (above lamp circle)
    fig.add_annotation(x=7, y=5.1, ax=7, ay=5.65,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=7.15, y=5.32, text="<b>I₄↓</b>",
                       showarrow=False, font=dict(size=11), xanchor="left")

    # I5 rightward on R5 raised rail (between P corner and R5 box left edge)
    fig.add_annotation(x=4.3, y=8.2, ax=3.7, ay=8.2,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=2, arrowcolor="#e6e6e6", text="")
    fig.add_annotation(x=4.0, y=8.48, text="<b>I₅→</b>",
                       showarrow=False, font=dict(size=11))

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
