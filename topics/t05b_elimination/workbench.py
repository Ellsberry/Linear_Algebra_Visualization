"""
Shared elimination workbench engine for Topic 5.5.
"""
import streamlit as st

from engine import widgets as w


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


def _active_pivot_tri(M, n_unknowns, tol=1e-9):
    """Return (p, p) for the first column with nonzeros below the diagonal, or None."""
    n = len(M)
    for p in range(min(n, n_unknowns)):
        for i in range(p + 1, n):
            if abs(M[i][p]) > tol:
                return (p, p)
    return None


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
            # Zero RHS: redundant equation. Only a free variable if rank < n_unknowns.
            n_pivots = sum(1 for k in range(min(n, nc)) if abs(M[k][k]) > TOL)
            if n_pivots < nc:
                st.info(
                    f"Row {i+1} became all zeros — that equation was redundant, "
                    "so there's a free variable: infinitely many solutions."
                )
                return
            # n_pivots == nc: redundant but fully determined -- fall through to triangular check
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
    """LaTeX aligned block -- one equation per row, variable columns aligned.

    Places & before each sign so the x1, x2, ... columns line up vertically.
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
# Shared state loader
# ---------------------------------------------------------------------------

def _load_aug(wb_key, aug):
    """Initialize workbench state from an augmented matrix."""
    st.session_state[f"{wb_key}_M"]    = [row[:] for row in aug]
    st.session_state[f"{wb_key}_orig"] = [row[:] for row in aug]
    st.session_state[f"{wb_key}_log"]  = []
    st.session_state[f"{wb_key}_history"] = []
    st.session_state.pop(f"{wb_key}_solution", None)


# ---------------------------------------------------------------------------
# The shared elimination workbench
# ---------------------------------------------------------------------------

def workbench(key, n_unknowns, solution_labels=None, solution_suffix=""):
    """Elimination workbench for st.session_state[key + '_M'] (list of rows).

    solution_labels: optional list of strings to replace x1, x2, ... in the
    solution readout (e.g. ["F->W1", "F->W2", ...] for the logistics screen).
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
        hp = _active_pivot_tri(M, n_unknowns)
        st.latex(w.aug_array_latex(M, n_unknowns, highlight=hp))
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
