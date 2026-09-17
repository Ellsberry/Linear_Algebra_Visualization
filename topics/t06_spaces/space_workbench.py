"""
General square-matrix row-reduction workbench for Topic 6 (Vector Spaces).

Unlike the determinant workbench (det_workbench.py), this one:
  - has NO determinant tracker (no sign / no scale-divisor display),
  - can run all the way to REDUCED row echelon form (RREF), not just triangular,
  - is meant for reducing a matrix so the student can read a subspace off it.

No augmented b-column, no equations display, no scenario banner, no
back-substitution -- just row operations on an n x n matrix, with Do one step
(walks forward to triangular, then normalizes pivots and clears above, all the
way to RREF), Run to triangular form, Run to reduced form, manual ops, Undo,
Reset. The row-op control layout mirrors the shared elimination workbench.
"""
import streamlit as st


# ---------------------------------------------------------------------------
# Parsing / formatting helpers
# ---------------------------------------------------------------------------

def _parse_factor(s, default=0.0):
    """Parse a scale factor: decimals ('0.5', '-2') and simple fractions
    ('1/3', '-3/2'). Returns float, or default on failure."""
    s = str(s).strip()
    if not s:
        return default
    try:
        if "/" in s:
            num, den = s.split("/", 1)
            return float(num.strip()) / float(den.strip())
        return float(s)
    except (ValueError, ZeroDivisionError):
        return default


def _parse_row(s):
    return int(s.split()[1]) - 1


def _fmt(v, tol=1e-9):
    v = float(v)
    if abs(v) < tol:
        return "0"
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:g}"


def _is_upper_tri_square(M, n, tol=1e-9):
    for i in range(n):
        for j in range(i):
            if abs(M[i][j]) > tol:
                return False
    return True


def _is_rref(M, n, tol=1e-9):
    """True when the matrix is in reduced row echelon form: each nonzero row's
    leading entry is 1, pivots step strictly right as you go down, each pivot
    column is clear everywhere else, and zero rows sit at the bottom. Pivots are
    found by leading entry (NOT by diagonal position), so rank-deficient
    matrices are handled correctly."""
    prev_pivot_col = -1
    for i in range(n):
        lead = None
        for j in range(n):
            if abs(M[i][j]) > tol:
                lead = j
                break
        if lead is None:
            continue  # zero row
        if abs(M[i][lead] - 1.0) > tol:
            return False           # leading entry must be 1
        if lead <= prev_pivot_col:
            return False           # pivots must move strictly right
        prev_pivot_col = lead
        for r in range(n):
            if r != i and abs(M[r][lead]) > tol:
                return False       # pivot column must be clear elsewhere
    # zero rows must all sit below the nonzero rows
    seen_zero = False
    for i in range(n):
        is_zero = all(abs(M[i][j]) < tol for j in range(n))
        if is_zero:
            seen_zero = True
        elif seen_zero:
            return False
    return True


def _pivot_cells(M, n, tol=1e-9):
    """Return the set of (i, lead) positions that are each row's leading nonzero
    entry (the pivots), for highlighting. Found by leading entry, not diagonal,
    so it is correct for rank-deficient matrices too."""
    cells = set()
    for i in range(n):
        for j in range(n):
            if abs(M[i][j]) > tol:
                cells.add((i, j))
                break
    return cells


def _bmat_square(M, n, highlight=None, hl_color="#ffd43b"):
    """Bracketed LaTeX matrix; highlight is an optional set of (i, j) cells to
    color with hl_color."""
    highlight = highlight or set()
    lines = []
    for i in range(n):
        cells = []
        for j in range(n):
            s = _fmt(M[i][j])
            if (i, j) in highlight:
                s = r"\color{" + hl_color + "}{" + s + "}"
            cells.append(s)
        lines.append(" & ".join(cells))
    return r"\begin{bmatrix}" + r" \\ ".join(lines) + r"\end{bmatrix}"


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

def space_load(key, A):
    """Initialize workbench state from a square matrix A (list of rows)."""
    M = [list(map(float, row)) for row in A]
    st.session_state[f"{key}_M"] = M
    st.session_state[f"{key}_orig"] = [row[:] for row in M]
    st.session_state[f"{key}_log"] = []
    st.session_state[f"{key}_hist"] = []


def _push_state(key):
    st.session_state.setdefault(f"{key}_hist", []).append(
        [row[:] for row in st.session_state[f"{key}_M"]]
    )


def _commit(key, new_M, desc):
    st.session_state[f"{key}_M"] = new_M
    st.session_state.setdefault(f"{key}_log", []).append(desc)


# ---------------------------------------------------------------------------
# One-step engine: forward elimination, then normalize pivots, then clear above
# (one operation per call), so "Do one step" walks all the way to RREF.
# ---------------------------------------------------------------------------

def _compute_one_step(M_in, n, tol=1e-9):
    """Return (new_M, desc) for the next single row operation toward RREF, or
    (None, None) once already in reduced form."""
    M = [row[:] for row in M_in]

    # PHASE 1 -- forward elimination (clear below pivots; swap up zero pivots)
    for p in range(n):
        if abs(M[p][p]) < tol:
            r = next((r for r in range(p + 1, n) if abs(M[r][p]) > tol), None)
            if r is not None:
                M[p], M[r] = M[r], M[p]
                return M, f"R{p+1} ↔ R{r+1}"
            continue
        i = next((r for r in range(p + 1, n) if abs(M[r][p]) > tol), None)
        if i is not None:
            f = M[i][p] / M[p][p]
            for c in range(n):
                M[i][c] -= f * M[p][c]
            sign = "+" if f < 0 else "−"
            return M, f"R{i+1} → R{i+1} {sign} {abs(f):.4g}·R{p+1}"

    # PHASE 2 -- normalize a pivot to 1
    for p in range(n):
        if abs(M[p][p]) > tol and abs(M[p][p] - 1.0) > tol:
            k = 1.0 / M[p][p]
            for c in range(n):
                M[p][c] *= k
            return M, f"R{p+1} → {k:.4g}·R{p+1}"

    # PHASE 3 -- clear above a pivot
    for p in range(n):
        if abs(M[p][p] - 1.0) < tol:
            for i in range(p - 1, -1, -1):
                if abs(M[i][p]) > tol:
                    f = M[i][p]
                    for c in range(n):
                        M[i][c] -= f * M[p][c]
                    sign = "+" if f < 0 else "−"
                    return M, f"R{i+1} → R{i+1} {sign} {abs(f):.4g}·R{p+1}"

    return None, None


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

def _apply_cb(key, n):
    M = [row[:] for row in st.session_state[f"{key}_M"]]
    op = st.session_state.get(f"{key}_op_type", "Add multiple of a row")
    _push_state(key)
    if op == "Add multiple of a row":
        i = _parse_row(st.session_state.get(f"{key}_add_i", "Row 1"))
        j = _parse_row(st.session_state.get(f"{key}_add_j", "Row 2"))
        k = _parse_factor(st.session_state.get(f"{key}_add_k", "-1"), -1.0)
        for c in range(n):
            M[i][c] += k * M[j][c]
        sign = "+" if k >= 0 else "−"
        _commit(key, M, f"R{i+1} → R{i+1} {sign} {abs(k):.4g}·R{j+1}")
    elif op == "Swap two rows":
        i = _parse_row(st.session_state.get(f"{key}_swap_i", "Row 1"))
        j = _parse_row(st.session_state.get(f"{key}_swap_j", "Row 2"))
        M[i], M[j] = M[j], M[i]
        _commit(key, M, f"R{i+1} ↔ R{j+1}")
    else:  # Scale a row
        i = _parse_row(st.session_state.get(f"{key}_scale_i", "Row 1"))
        k = _parse_factor(st.session_state.get(f"{key}_scale_k", "2"), 2.0)
        for c in range(n):
            M[i][c] *= k
        _commit(key, M, f"R{i+1} → {k:.4g}·R{i+1}")


def _step_cb(key, n):
    new_M, desc = _compute_one_step(st.session_state[f"{key}_M"], n)
    if new_M is not None:
        _push_state(key)
        _commit(key, new_M, desc)


def _run_triangular_cb(key, n):
    for _ in range(max(50, 10 * n * n)):
        if _is_upper_tri_square(st.session_state[f"{key}_M"], n):
            break
        new_M, desc = _compute_one_step(st.session_state[f"{key}_M"], n)
        if new_M is None:
            break
        # Only take forward-elimination steps for "run to triangular": stop
        # once triangular even though _compute_one_step would continue to RREF.
        _push_state(key)
        _commit(key, new_M, desc)
        if _is_upper_tri_square(st.session_state[f"{key}_M"], n):
            break


def _run_reduced_cb(key, n):
    for _ in range(max(80, 20 * n * n)):
        new_M, desc = _compute_one_step(st.session_state[f"{key}_M"], n)
        if new_M is None:
            break
        _push_state(key)
        _commit(key, new_M, desc)


def _undo_cb(key):
    hist = st.session_state.get(f"{key}_hist", [])
    if hist:
        st.session_state[f"{key}_M"] = hist.pop()
        st.session_state[f"{key}_hist"] = hist
        log = st.session_state.get(f"{key}_log", [])
        if log:
            log.pop()


def _reset_cb(key):
    orig = st.session_state.get(f"{key}_orig")
    if orig is not None:
        st.session_state[f"{key}_M"] = [row[:] for row in orig]
    st.session_state[f"{key}_log"] = []
    st.session_state[f"{key}_hist"] = []


# ---------------------------------------------------------------------------
# The workbench
# ---------------------------------------------------------------------------

def space_workbench(key, n, matrix_label="A"):
    """General square-matrix row-reduction workbench for
    st.session_state[key + '_M'] (an n x n list of rows, no augmented column).
    Controls mirror the shared elimination workbench; goes all the way to RREF.
    matrix_label sets the LaTeX name shown before the matrix (e.g. "A" or
    "A^{T}")."""
    M = st.session_state.get(f"{key}_M")
    if M is None:
        return
    row_opts = [f"Row {i+1}" for i in range(n)]

    left, right = st.columns([1, 1.3], gap="large")

    # --- Right: the matrix (pivots highlighted) ---
    with right:
        reduced = _is_rref(M, n)
        st.latex(matrix_label + " = " + _bmat_square(M, n, highlight=_pivot_cells(M, n)))
        if reduced:
            st.success("Reduced row echelon form reached.")
        elif _is_upper_tri_square(M, n):
            st.caption("Upper-triangular. Keep going for reduced form (pivots = 1, "
                       "zeros above and below).")

        log = st.session_state.get(f"{key}_log", [])
        if log:
            st.caption(f"Last: {log[-1]}")
            if len(log) > 1:
                with st.expander(f"All operations ({len(log)})"):
                    for entry in log:
                        st.text(entry)

    # --- Left: controls ---
    with left:
        st.markdown("**Row operations**")
        op = st.radio(
            "Operation type",
            ["Add multiple of a row", "Swap two rows", "Scale a row"],
            key=f"{key}_op_type",
            horizontal=True,
        )

        if op == "Add multiple of a row":
            c1, c2, c3 = st.columns(3)
            with c1:
                st.text_input("k (e.g. -1 or 1/2)", value="-1", key=f"{key}_add_k")
            with c2:
                st.radio("Source j", row_opts,
                         index=min(1, n - 1), key=f"{key}_add_j", horizontal=True)
            with c3:
                st.radio("Target i", row_opts, key=f"{key}_add_i", horizontal=True)
            k_d = _parse_factor(st.session_state.get(f"{key}_add_k", "-1"), -1.0)
            j_d = st.session_state.get(f"{key}_add_j", row_opts[min(1, n - 1)])
            i_d = st.session_state.get(f"{key}_add_i", row_opts[0])
            sgn = "+" if k_d >= 0 else "−"
            st.caption(f"{i_d} → {i_d} {sgn} {abs(k_d):.4g}·{j_d}")
        elif op == "Swap two rows":
            c1, c2 = st.columns(2)
            with c1:
                st.radio("Row i", row_opts, key=f"{key}_swap_i", horizontal=True)
            with c2:
                st.radio("Row j", row_opts,
                         index=min(1, n - 1), key=f"{key}_swap_j", horizontal=True)
        else:  # Scale a row
            c1, c2 = st.columns(2)
            with c1:
                st.radio("Row i", row_opts, key=f"{key}_scale_i", horizontal=True)
            with c2:
                st.text_input("Factor k (e.g. 1/3)", value="2", key=f"{key}_scale_k")

        import streamlit.components.v1 as components
        components.html(
            """
            <script>
            const inputs = window.parent.document.querySelectorAll('input[type="text"]');
            inputs.forEach((el) => {
                el.setAttribute('autocomplete', 'off');
                el.setAttribute('autocorrect', 'off');
                el.setAttribute('autocapitalize', 'off');
                el.setAttribute('spellcheck', 'false');
                el.setAttribute('name', 'nofill_' + Math.random().toString(36).slice(2));
            });
            </script>
            """,
            height=0,
        )

        ba, bu, br = st.columns(3)
        with ba:
            st.button("Apply", key=f"{key}_apply_btn",
                      on_click=_apply_cb, args=(key, n))
        with bu:
            st.button("Undo", key=f"{key}_undo_btn",
                      on_click=_undo_cb, args=(key,),
                      disabled=not bool(st.session_state.get(f"{key}_hist")))
        with br:
            st.button("Reset", key=f"{key}_reset_btn",
                      on_click=_reset_cb, args=(key,))

        st.markdown("---")
        st.markdown("**Guided elimination**")
        g1, g2, g3 = st.columns(3)
        with g1:
            st.button("Do one step", key=f"{key}_step_btn",
                      on_click=_step_cb, args=(key, n))
        with g2:
            st.button("Run to triangular form", key=f"{key}_runtri_btn",
                      on_click=_run_triangular_cb, args=(key, n))
        with g3:
            st.button("Run to reduced form", key=f"{key}_runrref_btn",
                      on_click=_run_reduced_cb, args=(key, n))
