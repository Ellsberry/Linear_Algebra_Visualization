"""
Topic 5.5 -- Elimination & Triangular Form.

Pattern: MULTI-EXAMPLE (3 screens).
Stage 2: workbench + Screen 1 + Screen 2 (Logistics). Screen 3 is a stub.
"""
import plotly.graph_objects as go
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

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
# Augmented-matrix helpers
# ---------------------------------------------------------------------------

def _make_aug(A, b):
    return [list(map(float, row)) + [float(b[i])] for i, row in enumerate(A)]


def _is_upper_triangular(M, n_unknowns, tol=1e-9):
    for i in range(len(M)):
        for j in range(min(i, n_unknowns)):
            if abs(M[i][j]) > tol:
                return False
    return True


def _all_pivots_nonzero(M, nc, tol=1e-9):
    return all(abs(M[i][i]) > tol for i in range(nc))


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def _push_state(key):
    """Snapshot current M onto the undo stack."""
    st.session_state.setdefault(f"{key}_history", []).append(
        [row[:] for row in st.session_state[f"{key}_M"]]
    )


def _commit(key, new_M, desc):
    """Replace working M, append to log, clear any cached solution."""
    st.session_state[f"{key}_M"] = new_M
    st.session_state.setdefault(f"{key}_log", []).append(desc)
    st.session_state.pop(f"{key}_solution", None)


# ---------------------------------------------------------------------------
# Row-operation callbacks (all use on_click so edits land before the rerun)
# ---------------------------------------------------------------------------

def _parse_row(s):
    return int(s.split()[1]) - 1


def _do_apply_cb(key, n_unknowns):
    M = [row[:] for row in st.session_state[f"{key}_M"]]
    nc = n_unknowns + 1
    op = st.session_state.get(f"{key}_op_type", "Add multiple of a row")
    _push_state(key)
    if op == "Add multiple of a row":
        i = _parse_row(st.session_state.get(f"{key}_add_i", "Row 1"))
        j = _parse_row(st.session_state.get(f"{key}_add_j", "Row 2"))
        k = float(st.session_state.get(f"{key}_add_k", -1.0))
        for c in range(nc):
            M[i][c] += k * M[j][c]
        sign = "+" if k >= 0 else "−"
        desc = f"R{i+1} → R{i+1} {sign} {abs(k):.4g}·R{j+1}"
    elif op == "Swap two rows":
        i = _parse_row(st.session_state.get(f"{key}_swap_i", "Row 1"))
        j = _parse_row(st.session_state.get(f"{key}_swap_j", "Row 2"))
        M[i], M[j] = M[j], M[i]
        desc = f"R{i+1} ↔ R{j+1}"
    else:  # Scale a row
        i = _parse_row(st.session_state.get(f"{key}_scale_i", "Row 1"))
        k = float(st.session_state.get(f"{key}_scale_k", 2.0))
        for c in range(nc):
            M[i][c] *= k
        desc = f"R{i+1} → {k:.4g}·R{i+1}"
    _commit(key, M, desc)


def _compute_one_step(M_in, n_unknowns):
    """One standard forward-elimination op. Returns (new_M, desc) or (None, None)."""
    M = [row[:] for row in M_in]
    n = len(M)
    nc = n_unknowns + 1
    TOL = 1e-9
    for p in range(min(n, n_unknowns)):
        if abs(M[p][p]) < TOL:
            r = next((r for r in range(p + 1, n) if abs(M[r][p]) > TOL), None)
            if r is not None:
                M[p], M[r] = M[r], M[p]
                return M, f"R{p+1} ↔ R{r+1}"
            continue
        i = next((r for r in range(p + 1, n) if abs(M[r][p]) > TOL), None)
        if i is not None:
            factor = M[i][p] / M[p][p]
            for c in range(nc):
                M[i][c] -= factor * M[p][c]
            sign = "+" if factor < 0 else "−"
            desc = f"R{i+1} → R{i+1} {sign} {abs(factor):.4g}·R{p+1}"
            return M, desc
    return None, None


def _do_one_step_cb(key, n_unknowns):
    new_M, desc = _compute_one_step(st.session_state[f"{key}_M"], n_unknowns)
    if new_M is not None:
        _push_state(key)
        _commit(key, new_M, desc)


def _run_to_triangular_cb(key, n_unknowns):
    n = len(st.session_state[f"{key}_M"])
    for _ in range(max(50, 10 * n * n)):
        new_M, desc = _compute_one_step(st.session_state[f"{key}_M"], n_unknowns)
        if new_M is None:
            break
        _push_state(key)
        _commit(key, new_M, desc)


def _back_solve_cb(key, n_unknowns):
    M = st.session_state[f"{key}_M"]
    nc = n_unknowns
    x = [0.0] * nc
    steps = []
    TOL = 1e-9
    for i in range(min(len(M), nc) - 1, -1, -1):
        if abs(M[i][i]) < TOL:
            continue
        b_val = M[i][nc]
        tail = sum(M[i][j] * x[j] for j in range(i + 1, nc))
        x[i] = (b_val - tail) / M[i][i]
        if abs(tail) < TOL:
            steps.append(f"Row {i+1}: x{i+1} = {b_val:.4g} / {M[i][i]:.4g} = **{x[i]:.4g}**")
        else:
            steps.append(
                f"Row {i+1}: x{i+1} = ({b_val:.4g} − {tail:.4g}) / {M[i][i]:.4g} = **{x[i]:.4g}**"
            )
    st.session_state[f"{key}_solution"] = (x, steps)


def _undo_cb(key):
    history = st.session_state.get(f"{key}_history", [])
    if history:
        st.session_state[f"{key}_M"] = history.pop()
        st.session_state[f"{key}_history"] = history
        log = st.session_state.get(f"{key}_log", [])
        if log:
            log.pop()
    st.session_state.pop(f"{key}_solution", None)


def _reset_cb(key):
    orig = st.session_state.get(f"{key}_orig")
    if orig is not None:
        st.session_state[f"{key}_M"] = [row[:] for row in orig]
    st.session_state[f"{key}_log"] = []
    st.session_state[f"{key}_history"] = []
    st.session_state.pop(f"{key}_solution", None)


# ---------------------------------------------------------------------------
# Scenario detection (runs after every op)
# ---------------------------------------------------------------------------

def _show_scenario(M, n_unknowns):
    TOL = 1e-9
    n = len(M)
    nc = n_unknowns
    for i, row in enumerate(M):
        zero_coeffs = all(abs(row[j]) < TOL for j in range(nc))
        if zero_coeffs:
            if abs(row[nc]) > TOL:
                st.error(
                    f"Row {i+1} says 0 = {row[nc]:.4g} — impossible. "
                    "This system has no solution."
                )
                return
            else:
                st.info(
                    f"Row {i+1} became all zeros — that equation was redundant, "
                    "so there's a free variable: infinitely many solutions."
                )
                return
    is_tri = _is_upper_triangular(M, nc)
    if is_tri:
        n_pivots = sum(1 for i in range(min(n, nc)) if abs(M[i][i]) > TOL)
        if n_pivots == nc:
            st.success(f"Upper triangular — {n_pivots} pivot(s). Ready to back-substitute.")
            st.caption(
                f"Pivot count = {n_pivots} = number of genuinely independent equations. "
                "(That count is the *rank* — a preview of Topic 6.)"
            )
        else:
            st.info(
                f"Upper triangular with {n_pivots} of {nc} nonzero pivots "
                "— free variables exist."
            )


# ---------------------------------------------------------------------------
# Equation display (column-aligned, updates with every op)
# ---------------------------------------------------------------------------

def _equations_latex(M, n_unknowns):
    """LaTeX aligned block — one equation per row, variable columns aligned.

    Places & before each sign so the x₁, x₂, … columns line up vertically.
    Zero coefficients produce an empty column, visually showing elimination.
    """
    var_names = [f"x_{{{i+1}}}" for i in range(n_unknowns)]
    TOL = 1e-10
    lines = []
    for row in M:
        first_nz = next((j for j in range(n_unknowns) if abs(float(row[j])) > TOL), None)
        parts = []
        for j in range(n_unknowns):
            c = float(row[j])
            if abs(c) < TOL:
                parts.append("")
                continue
            c_abs = abs(c)
            if abs(c_abs - 1) < 1e-9:
                coeff = ""
            elif abs(c_abs - round(c_abs)) < 1e-9:
                coeff = str(int(round(c_abs)))
            else:
                coeff = f"{c_abs:.4g}"
            term = coeff + var_names[j]
            if j == first_nz:
                parts.append(f"-{term}" if c < 0 else term)
            else:
                parts.append(f"{'-' if c < 0 else '+'}\\,{term}")
        b = float(row[n_unknowns])
        b_str = str(int(round(b))) if abs(b - round(b)) < 1e-9 else f"{b:.4g}"
        parts.append(f"= {b_str}")
        lines.append(" & ".join(parts))
    return r"\begin{aligned}" + r" \\ ".join(lines) + r"\end{aligned}"


# ---------------------------------------------------------------------------
# The shared elimination workbench
# ---------------------------------------------------------------------------

def workbench(key, n_unknowns, solution_labels=None, solution_suffix=""):
    """Elimination workbench for st.session_state[key + '_M'] (list of rows).

    solution_labels: optional list of strings to replace x1, x2, … in the
    solution readout (e.g. ["F→W1", "F→W2", …] for the logistics screen).
    solution_suffix: appended to every value (e.g. " A" for currents).
    """
    M = st.session_state.get(f"{key}_M")
    if M is None:
        return
    n = len(M)
    row_opts = [f"Row {i+1}" for i in range(n)]

    is_tri = _is_upper_triangular(M, n_unknowns)
    has_pivots = _all_pivots_nonzero(M, min(n, n_unknowns))
    is_ready = is_tri and has_pivots

    left, right = st.columns([1, 1.3], gap="large")

    # --- Right: equations + matrix (both read from M, update together) ---
    with right:
        st.latex(_equations_latex(M, n_unknowns))
        st.latex(w.aug_array_latex(M, n_unknowns))
        _show_scenario(M, n_unknowns)

        log = st.session_state.get(f"{key}_log", [])
        if log:
            st.caption(f"Last: {log[-1]}")
            if len(log) > 1:
                with st.expander(f"All operations ({len(log)})"):
                    for entry in log:
                        st.text(entry)

        if is_ready and f"{key}_solution" in st.session_state:
            x, steps = st.session_state[f"{key}_solution"]
            with st.expander("Back-substitution steps", expanded=True):
                for step in steps:
                    st.markdown(step)
            if solution_labels:
                sol_str = "  ·  ".join(
                    f"{solution_labels[i]} = {xi:.4g}{solution_suffix}"
                    for i, xi in enumerate(x)
                )
            else:
                sol_str = "  ·  ".join(
                    f"x{i+1} = {xi:.4g}{solution_suffix}" for i, xi in enumerate(x)
                )
            st.success(f"Solution:  {sol_str}")

    # --- Left: controls ---
    with left:
        st.markdown("**Row operations**")
        op = st.selectbox(
            "Operation type",
            ["Add multiple of a row", "Swap two rows", "Scale a row"],
            key=f"{key}_op_type",
        )

        if op == "Add multiple of a row":
            c1, c2, c3 = st.columns(3)
            with c1:
                st.number_input("k", value=-1.0, step=0.5, format="%.2f",
                                key=f"{key}_add_k")
            with c2:
                st.selectbox("Source j", row_opts,
                             index=min(1, n - 1), key=f"{key}_add_j")
            with c3:
                st.selectbox("Target i", row_opts, key=f"{key}_add_i")
            k_d = st.session_state.get(f"{key}_add_k", -1.0)
            j_d = st.session_state.get(f"{key}_add_j", row_opts[min(1, n - 1)])
            i_d = st.session_state.get(f"{key}_add_i", row_opts[0])
            sign = "+" if k_d >= 0 else "−"
            st.caption(f"{i_d} → {i_d} {sign} {abs(k_d):.4g}·{j_d}")
        elif op == "Swap two rows":
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox("Row i", row_opts, key=f"{key}_swap_i")
            with c2:
                st.selectbox("Row j", row_opts,
                             index=min(1, n - 1), key=f"{key}_swap_j")
        else:  # Scale a row
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox("Row i", row_opts, key=f"{key}_scale_i")
            with c2:
                st.number_input("Factor k", value=2.0, step=0.5, format="%.2f",
                                key=f"{key}_scale_k")

        ba, bu, br = st.columns(3)
        with ba:
            st.button("Apply", key=f"{key}_apply_btn",
                      on_click=_do_apply_cb, args=(key, n_unknowns))
        with bu:
            st.button("Undo", key=f"{key}_undo_btn",
                      on_click=_undo_cb, args=(key,),
                      disabled=not bool(st.session_state.get(f"{key}_history")))
        with br:
            st.button("Reset", key=f"{key}_reset_btn",
                      on_click=_reset_cb, args=(key,))

        st.markdown("---")
        st.markdown("**Guided elimination**")
        g1, g2 = st.columns(2)
        with g1:
            st.button("Do one step", key=f"{key}_step_btn",
                      on_click=_do_one_step_cb, args=(key, n_unknowns))
        with g2:
            st.button("Run to triangular form", key=f"{key}_run_btn",
                      on_click=_run_to_triangular_cb, args=(key, n_unknowns))

        st.button(
            "Back-substitute & solve",
            key=f"{key}_backsolve_btn",
            on_click=_back_solve_cb,
            args=(key, n_unknowns),
            disabled=not is_ready,
        )


# ---------------------------------------------------------------------------
# Screen 1 — The workbench
# ---------------------------------------------------------------------------

_E1_PRESETS = {
    "One solution": {
        "A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
        "b": [8, -11, -3],
        "notice": "A clean 3×3 — three nonzero pivots appear after elimination. "
                  "Back-substitute to reach x = (2, 3, −1).",
    },
    "Needs a row swap": {
        "A": [[0, 2, 1], [1, 1, 1], [2, 1, 3]],
        "b": [5, 6, 11],
        "notice": "The top-left entry is 0 — **Do one step** immediately triggers a swap. "
                  "After that, elimination proceeds normally to x = (3, 2, 1).",
    },
    "Redundant equation (infinite)": {
        "A": [[1, 1, 1], [1, 2, 3], [2, 3, 4]],
        "b": [6, 14, 20],
        "notice": "Row 3 = Row 1 + Row 2, so it vanishes during elimination — "
                  "a free variable appears and there are infinitely many solutions.",
    },
    "Contradiction (no solution)": {
        "A": [[1, 1, 1], [1, 2, 3], [2, 3, 4]],
        "b": [6, 14, 21],
        "notice": "Same coefficient equations as *Redundant*, but the last constant "
                  "differs — elimination produces a row \"0 = 1\", which is impossible.",
    },
}

_E1_NOTICE = """
Try the standard method with **Do one step**, then experiment in manual mode —
you can't break it, because every move keeps the same solution. The four presets
show the four things that can happen: a clean triangle (one solution), a forced
swap when a pivot is zero, a row that vanishes (infinitely many), and a row that
becomes "0 = something" (no solution).
"""


def _example_one():
    st.markdown(
        "**The workbench.** A 3×3 system — small enough to relate to planes "
        "and still big enough to show every scenario. Use it to learn the moves, "
        "then explore each of the four preset outcomes."
    )
    st.info(_E1_NOTICE)

    preset = st.selectbox("Preset", list(_E1_PRESETS), key="t05b_e1_preset")
    p = _E1_PRESETS[preset]
    if st.session_state.get("t05b_e1_last") != preset:
        aug = _make_aug(p["A"], p["b"])
        st.session_state["t05b_e1_M"] = aug
        st.session_state["t05b_e1_orig"] = [row[:] for row in aug]
        st.session_state["t05b_e1_log"] = []
        st.session_state["t05b_e1_history"] = []
        st.session_state.pop("t05b_e1_solution", None)
        st.session_state["t05b_e1_last"] = preset
    st.caption(p["notice"])

    workbench("t05b_e1", 3)

    with st.expander("Show the math"):
        st.markdown(
            "The three legal moves — add a multiple, swap, scale — are the "
            "**elementary row operations**. Each can be undone, so they never "
            "change the solution set.\n\n"
            "Once the matrix is upper triangular, its determinant equals the "
            "**product of the diagonal pivots**. If any pivot is zero, the "
            "determinant is zero — exactly the *singular* / \"no unique solution\" "
            "case from Topic 3. The number of nonzero pivots is the *rank* of A, "
            "a preview of Topic 6."
        )


# ---------------------------------------------------------------------------
# Screen 2 — Logistics (6-variable shipping network)
# ---------------------------------------------------------------------------

# Augmented matrix [A | b] for the six balance equations
_E2_AUG = [
    [ 1,  0, -1, -1,  0,  0,  0],   # W1: x₁ − x₃ − x₄ = 0
    [ 0,  1,  0,  0, -1, -1,  0],   # W2: x₂ − x₅ − x₆ = 0
    [ 0,  0,  1,  0,  0,  0, 30],   # A:  x₃ = 30
    [ 0,  0,  0,  1,  0,  0, 20],   # B:  x₄ = 20
    [ 0,  0,  0,  0,  1,  0, 25],   # C:  x₅ = 25
    [ 0,  0,  0,  0,  0,  1, 25],   # D:  x₆ = 25
]
_E2_LABELS     = ["F→W1", "F→W2", "W1→A", "W1→B", "W2→C", "W2→D"]
_E2_ROW_LABELS = ["W1 node", "W2 node", "Store A", "Store B", "Store C", "Store D"]

_E2_NOTICE = """
The unknowns are how much travels on each route. "Flow in = flow out" at every
node gives one equation each; solving the system is the shipping plan. Six
unknowns — no picture for that — but the same three moves solve it. (Networks
with alternative routes can have *many* valid plans; this tree has exactly one.)
"""


def _load_aug(wb_key, aug):
    """Initialize workbench state from an augmented matrix."""
    st.session_state[f"{wb_key}_M"]    = [row[:] for row in aug]
    st.session_state[f"{wb_key}_orig"] = [row[:] for row in aug]
    st.session_state[f"{wb_key}_log"]  = []
    st.session_state[f"{wb_key}_history"] = []
    st.session_state.pop(f"{wb_key}_solution", None)


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
    [ 1.0, -1.0, -1.0,  0.0],   # KCL node:  I₁ − I₂ − I₃ = 0
    [ 2.0,  4.0,  0.0, 12.0],   # KVL loop 1: R1·I₁ + R2·I₂ = V
    [ 0.0,  4.0, -4.0,  0.0],   # KVL loop 2: R2·I₂ − R3·I₃ = 0
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

    # I₁ arrow: left of R1 on top rail
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
    # I₂ arrow
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
    # I₃ arrow
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
