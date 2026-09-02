"""
Dedicated square-matrix determinant workbench for Topic 5.5's Determinant
Calculation screen. No augmented b-column, no equations display, no scenario
banner, no back-substitution -- just row operations on a square matrix plus a
live determinant tracker (running sign + scale divisor).
"""
import streamlit as st


def _parse_factor(s, default=0.0):
    """Parse a user-entered scale factor: accepts decimals ('0.5', '-2') and
    simple fractions ('1/11.6', '-3/2'). Returns float, or default on failure."""
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


def _is_upper_tri_square(M, n, tol=1e-9):
    for i in range(n):
        for j in range(i):
            if abs(M[i][j]) > tol:
                return False
    return True


def _fmt(v, tol=1e-9):
    v = float(v)
    if abs(v) < tol:
        return "0"
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:g}"


def _bmat_square(M, n, diag_color=None):
    """Bracketed LaTeX matrix for an n x n grid; diag_color, if given, colors
    the (i, i) diagonal entries with that hex color."""
    lines = []
    for i in range(n):
        cells = []
        for j in range(n):
            s = _fmt(M[i][j])
            if diag_color is not None and i == j:
                s = r"\color{" + diag_color + "}{" + s + "}"
            cells.append(s)
        lines.append(" & ".join(cells))
    return r"\begin{bmatrix}" + r" \\ ".join(lines) + r"\end{bmatrix}"


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

def _det_load(key, A):
    """Initialize det_workbench state from a square matrix A (list of rows)."""
    M = [list(map(float, row)) for row in A]
    st.session_state[f"{key}_M"] = M
    st.session_state[f"{key}_orig"] = [row[:] for row in M]
    st.session_state[f"{key}_log"] = []
    st.session_state[f"{key}_hist"] = []
    st.session_state[f"{key}_sign"] = 1
    st.session_state[f"{key}_div"] = 1.0


def _parse_row(s):
    return int(s.split()[1]) - 1


def _push_state(key):
    """Snapshot M plus the running sign/divisor onto the undo stack."""
    st.session_state.setdefault(f"{key}_hist", []).append((
        [row[:] for row in st.session_state[f"{key}_M"]],
        st.session_state.get(f"{key}_sign", 1),
        st.session_state.get(f"{key}_div", 1.0),
    ))


def _commit(key, new_M, desc, sign_mult=1, div_mult=1.0):
    """Replace working M, append to log, update running sign/divisor."""
    st.session_state[f"{key}_M"] = new_M
    st.session_state.setdefault(f"{key}_log", []).append(desc)
    st.session_state[f"{key}_sign"] = st.session_state.get(f"{key}_sign", 1) * sign_mult
    st.session_state[f"{key}_div"] = st.session_state.get(f"{key}_div", 1.0) * div_mult


# ---------------------------------------------------------------------------
# Callbacks (all use on_click so edits land before the rerun)
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
        desc = f"R{i+1} → R{i+1} {sign} {abs(k):.4g}·R{j+1}"
        _commit(key, M, desc)
    elif op == "Swap two rows":
        i = _parse_row(st.session_state.get(f"{key}_swap_i", "Row 1"))
        j = _parse_row(st.session_state.get(f"{key}_swap_j", "Row 2"))
        M[i], M[j] = M[j], M[i]
        desc = f"R{i+1} ↔ R{j+1}"
        _commit(key, M, desc, sign_mult=-1)
    else:  # Scale a row
        i = _parse_row(st.session_state.get(f"{key}_scale_i", "Row 1"))
        k = _parse_factor(st.session_state.get(f"{key}_scale_k", "2"), 2.0)
        for c in range(n):
            M[i][c] *= k
        desc = f"R{i+1} → {k:.4g}·R{i+1}"
        _commit(key, M, desc, div_mult=k)


def _compute_one_step_forward(M_in, n):
    """One forward-elimination-only op toward upper-triangular form. Returns
    (new_M, desc, sign_mult) or (None, None, 1) once triangular. Swap up a
    zero pivot; else clear the first nonzero below a pivot. No normalization
    or back-clearing -- this workbench stops at triangular form."""
    M = [row[:] for row in M_in]
    TOL = 1e-9
    for p in range(n):
        if abs(M[p][p]) < TOL:
            r = next((r for r in range(p + 1, n) if abs(M[r][p]) > TOL), None)
            if r is not None:
                M[p], M[r] = M[r], M[p]
                return M, f"R{p+1} ↔ R{r+1}", -1
            continue
        i = next((r for r in range(p + 1, n) if abs(M[r][p]) > TOL), None)
        if i is not None:
            factor = M[i][p] / M[p][p]
            for c in range(n):
                M[i][c] -= factor * M[p][c]
            sign = "+" if factor < 0 else "−"
            desc = f"R{i+1} → R{i+1} {sign} {abs(factor):.4g}·R{p+1}"
            return M, desc, 1
    return None, None, 1


def _step_cb(key, n):
    new_M, desc, sign_mult = _compute_one_step_forward(st.session_state[f"{key}_M"], n)
    if new_M is not None:
        _push_state(key)
        _commit(key, new_M, desc, sign_mult=sign_mult)


def _run_cb(key, n):
    for _ in range(max(50, 10 * n * n)):
        if _is_upper_tri_square(st.session_state[f"{key}_M"], n):
            break
        new_M, desc, sign_mult = _compute_one_step_forward(st.session_state[f"{key}_M"], n)
        if new_M is None:
            break
        _push_state(key)
        _commit(key, new_M, desc, sign_mult=sign_mult)


def _undo_cb(key):
    hist = st.session_state.get(f"{key}_hist", [])
    if hist:
        M, sign, div = hist.pop()
        st.session_state[f"{key}_M"] = M
        st.session_state[f"{key}_sign"] = sign
        st.session_state[f"{key}_div"] = div
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
    st.session_state[f"{key}_sign"] = 1
    st.session_state[f"{key}_div"] = 1.0


# ---------------------------------------------------------------------------
# The dedicated determinant workbench
# ---------------------------------------------------------------------------

def det_workbench(key, n):
    """Square-matrix determinant workbench for st.session_state[key + '_M']
    (an n x n list of rows, no augmented column). Row-op controls mirror the
    shared elimination workbench, but there's no equation display, no
    scenario banner, and no back-substitution -- just the matrix and a live
    determinant tracker.
    """
    M = st.session_state.get(f"{key}_M")
    if M is None:
        return
    row_opts = [f"Row {i+1}" for i in range(n)]

    left, right = st.columns([1, 1.3], gap="large")

    # --- Right: matrix + determinant tracker ---
    with right:
        is_tri = _is_upper_tri_square(M, n)
        diag_color = "#ffd43b" if is_tri else "#4dabf7"
        st.latex("A = " + _bmat_square(M, n, diag_color=diag_color))

        sign = st.session_state.get(f"{key}_sign", 1)
        div = st.session_state.get(f"{key}_div", 1.0)
        n_swaps = sum(1 for d in st.session_state.get(f"{key}_log", []) if "↔" in d)

        st.markdown("**Determinant tracker**")
        st.caption(f"Row swaps so far: {n_swaps}  (sign: {'+' if sign>0 else '−'})   "
                   f"Scale factor to divide out: {div:g}")

        if is_tri:
            diag = 1.0
            for i in range(n):
                diag *= M[i][i]
            det = sign * diag / div if div != 0 else float('nan')
            if abs(det) < 1e-9:
                det = 0.0
            st.latex(r"\det(A) = " + f"({'+' if sign>0 else '-'}1)"
                     + r"\times(" + " \\times ".join(_fmt(M[i][i]) for i in range(n)) + ")"
                     + (r"\div" + f"{div:g}" if div != 1 else "")
                     + f" = {det:g}")
            st.success(f"Determinant = {det:g}")

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
                st.text_input("Factor k (e.g. 1/11.6)", value="2", key=f"{key}_scale_k")

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
        g1, g2 = st.columns(2)
        with g1:
            st.button("Do one step", key=f"{key}_step_btn",
                      on_click=_step_cb, args=(key, n))
        with g2:
            st.button("Run to triangular form", key=f"{key}_run_btn",
                      on_click=_run_cb, args=(key, n))
