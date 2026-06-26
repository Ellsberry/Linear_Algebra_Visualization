import plotly.graph_objects as go
import streamlit as st
from fractions import Fraction

from engine import plotting as plot
from engine import widgets as w
from .eq_parser import parse_equation, rows_equivalent, ParseError
from .workbench import workbench, _load_aug


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
_E2_RHS        = [-100, 0, 0, 30, 20, 25, 25]   # net supply/demand per node, F..D


def _row_to_eq_str(row):
    """Convert an _E2_AUG row to a plain-text equation string for the text box."""
    parts = []
    for j in range(7):
        c = int(row[j])
        if c == 0:
            continue
        var = f"x{j + 1}"
        if not parts:
            parts.append(f"-{var}" if c == -1 else (var if c == 1 else f"{c}{var}"))
        else:
            if c == 1:
                parts.append(f"+ {var}")
            elif c == -1:
                parts.append(f"- {var}")
            elif c > 0:
                parts.append(f"+ {c}{var}")
            else:
                parts.append(f"- {abs(c)}{var}")
    b = int(row[7])
    lhs = " ".join(parts) if parts else "0"
    return f"{lhs} = {b}"


def _row_to_latex(row):
    """Convert a parsed [a1..a7, b] row (Fractions) to a LaTeX string."""
    parts = []
    for j in range(7):
        c = Fraction(row[j]).limit_denominator(10**6)
        if c == 0:
            continue
        pos = c > 0
        c_abs = abs(c)
        if c_abs == 1:
            coeff_str = ""
        elif c_abs.denominator == 1:
            coeff_str = str(c_abs.numerator)
        else:
            coeff_str = rf"\frac{{{c_abs.numerator}}}{{{c_abs.denominator}}}"
        var = rf"x_{{{j + 1}}}"
        term = f"{coeff_str}{var}"
        if not parts:
            parts.append(term if pos else f"-{term}")
        else:
            parts.append(rf"+ {term}" if pos else rf"- {term}")
    b = Fraction(row[7]).limit_denominator(10**6)
    if b.denominator == 1:
        b_str = str(int(b))
    else:
        b_str = rf"\frac{{{b.numerator}}}{{{b.denominator}}}"
    lhs = " ".join(parts) if parts else "0"
    return lhs + rf" = {b_str}"


def _check_grid_cb():
    wrong = []
    parse_errors = []
    for i, target_row in enumerate(_E2_AUG):
        text = st.session_state.get(f"t05b_e2_eq__{i}", "").strip()
        try:
            parsed = parse_equation(text)
        except ParseError:
            parse_errors.append(i)
            wrong.append(i)
            continue
        if not rows_equivalent(parsed, target_row):
            wrong.append(i)
    st.session_state["t05b_e2_check_result"] = wrong
    st.session_state["t05b_e2_parse_errors"] = parse_errors
    if not wrong:
        _load_aug("t05b_e2", _E2_AUG)
        st.session_state["t05b_e2_ready"] = True


def _fill_for_me_cb():
    for i, row in enumerate(_E2_AUG):
        st.session_state[f"t05b_e2_eq__{i}"] = _row_to_eq_str(row)
    st.session_state["t05b_e2_check_result"] = []
    st.session_state.pop("t05b_e2_parse_errors", None)
    _load_aug("t05b_e2", _E2_AUG)
    st.session_state["t05b_e2_ready"] = True


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


def _assemble_from_builder():
    """Parse each node's text input and return a 7x8 augmented matrix (floats).

    Nodes that fail to parse contribute None (handled by caller).
    """
    rows = []
    for i in range(len(_E2_ROW_LABELS)):
        text = st.session_state.get(f"t05b_e2_eq__{i}", "").strip()
        try:
            row = parse_equation(text)
            rows.append([float(x) for x in row])
        except (ParseError, Exception):
            rows.append(None)
    return rows


def _node_balance_builder():
    """Typed-equation builder: one text box per node, with live LaTeX preview."""
    st.markdown(
        "Read the network and write the balance equation for each node -- "
        "flow in = flow out, with each store's demand and the factory's supply "
        "on the right. Type equations like `x1 - x3 - x4 = 0`."
    )
    for i, node_label in enumerate(_E2_ROW_LABELS):
        col_input, col_preview = st.columns([2, 3])
        with col_input:
            st.text_input(
                node_label,
                key=f"t05b_e2_eq__{i}",
                placeholder="e.g. x1 - x3 - x4 = 0",
            )
        with col_preview:
            text = st.session_state.get(f"t05b_e2_eq__{i}", "").strip()
            if text:
                try:
                    row = parse_equation(text)
                    st.latex(_row_to_latex(row))
                except ParseError:
                    st.caption("...")
            else:
                st.caption("...")


def _example_two():
    st.markdown(
        "You're solving for the amount of freight on each of the seven routes "
        "(x₁…x₇) -- the shipping plan where flow in = flow out at every node "
        "and every store's demand is met. Read the network, then write each "
        "node's balance equation."
    )

    diagram_col, builder_col = st.columns([0.5, 0.5], gap="large")
    with diagram_col:
        st.plotly_chart(_logistics_diagram(), use_container_width=True)
    with builder_col:
        _node_balance_builder()

    c1, c2 = st.columns(2)
    with c1:
        st.button("Check", key="t05b_e2_check_btn", on_click=_check_grid_cb)
    with c2:
        st.button("Fill it in for me", key="t05b_e2_fill_btn", on_click=_fill_for_me_cb)

    check = st.session_state.get("t05b_e2_check_result")
    if check is not None:
        if not check:
            st.success("All seven equations are correct.")
        else:
            parse_errs = set(st.session_state.get("t05b_e2_parse_errors", []))
            msgs = []
            for i in check:
                if i in parse_errs:
                    msgs.append(f"{_E2_ROW_LABELS[i]} (couldn't read)")
                else:
                    msgs.append(f"{_E2_ROW_LABELS[i]} (wrong)")
            st.warning(f"Not quite -- check {', '.join(msgs)}.")

    if st.session_state.get("t05b_e2_ready") and st.session_state.get("t05b_e2_M"):
        st.markdown("**Your system as an augmented matrix [A | b]**")
        st.caption(
            "The seven equations you wrote, stacked. Each row is one node's "
            "balance; the bar separates the coefficients A from the demands b. "
            "Now reduce it."
        )
        st.latex(w.aug_array_latex(st.session_state["t05b_e2_M"], 7))
        st.markdown("---")
        st.markdown("**Reduce it** -- same three moves, seven unknowns.")
        workbench("t05b_e2", 7, solution_labels=_E2_LABELS)
        st.info(
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
        )
