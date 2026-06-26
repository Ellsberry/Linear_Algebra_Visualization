import streamlit as st
from fractions import Fraction

from .eq_parser import parse_equation, rows_equivalent, ParseError
from .workbench import workbench, _load_aug


def _row_to_eq_str(row, n):
    """Convert an augmented row to a plain-text equation string for a text box."""
    parts = []
    for j in range(n):
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
    b = int(row[n])
    lhs = " ".join(parts) if parts else "0"
    return f"{lhs} = {b}"


def _row_to_latex(row, n):
    """Convert a parsed augmented row to a LaTeX equation string."""
    parts = []
    for j in range(n):
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
    b = Fraction(row[-1]).limit_denominator(10**6)
    if b.denominator == 1:
        b_str = str(int(b))
    else:
        b_str = rf"\frac{{{b.numerator}}}{{{b.denominator}}}"
    lhs = " ".join(parts) if parts else "0"
    return lhs + rf" = {b_str}"


def _live_aug_latex(key, n, n_rows=None):
    """Build augmented [A|b] LaTeX from current typed equations; faint dashes for blank/unparseable rows.

    n_rows defaults to n; pass len(target_aug) when equations > unknowns.
    """
    if n_rows is None:
        n_rows = n
    col_spec = "c" * n + "|c"

    def _fmt(v):
        v = float(v)
        if abs(v) < 1e-10:
            return "0"
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.4g}"

    dash = r"\color{gray}{-}"
    row_strs = []
    for i in range(n_rows):
        text = st.session_state.get(f"{key}_eq__{i}", "").strip()
        if not text:
            row_strs.append(" & ".join([dash] * (n + 1)))
            continue
        try:
            row = parse_equation(text)
            cells = [_fmt(row[j]) for j in range(n)] + [_fmt(row[-1])]
            row_strs.append(" & ".join(cells))
        except ParseError:
            row_strs.append(" & ".join([dash] * (n + 1)))

    body = r" \\ ".join(row_strs)
    return r"\left[\begin{array}{" + col_spec + r"}" + body + r"\end{array}\right]"


def _assemble_from_builder(key, n, row_labels):
    """Parse each row's text input; return a list of float rows, or None for unparseable entries."""
    rows = []
    for i in range(len(row_labels)):
        text = st.session_state.get(f"{key}_eq__{i}", "").strip()
        try:
            row = parse_equation(text)
            rows.append([float(row[j]) for j in range(n)] + [float(row[-1])])
        except (ParseError, Exception):
            rows.append(None)
    return rows


def _check_cb(key, target_aug, row_labels):
    n = len(target_aug[0]) - 1
    wrong = []
    parse_errors = []
    for i, target_row in enumerate(target_aug):
        text = st.session_state.get(f"{key}_eq__{i}", "").strip()
        try:
            parsed = parse_equation(text)
        except ParseError:
            parse_errors.append(i)
            wrong.append(i)
            continue
        condensed = list(parsed[:n]) + [parsed[-1]]
        if not rows_equivalent(condensed, target_row):
            wrong.append(i)
    st.session_state[f"{key}_check_result"] = wrong
    st.session_state[f"{key}_parse_errors"] = parse_errors
    if not wrong:
        _load_aug(key, target_aug)
        st.session_state[f"{key}_ready"] = True


def _fill_cb(key, target_aug):
    n = len(target_aug[0]) - 1
    for i, row in enumerate(target_aug):
        st.session_state[f"{key}_eq__{i}"] = _row_to_eq_str(row, n)
    st.session_state[f"{key}_check_result"] = []
    st.session_state.pop(f"{key}_parse_errors", None)
    _load_aug(key, target_aug)
    st.session_state[f"{key}_ready"] = True


def _node_balance_builder(key, n, row_labels, intro_md=None):
    """Typed-equation builder: one text box per row, with live LaTeX preview."""
    if intro_md:
        st.markdown(intro_md)
    for i, node_label in enumerate(row_labels):
        col_input, col_preview = st.columns([2, 3])
        with col_input:
            st.text_input(
                node_label,
                key=f"{key}_eq__{i}",
                placeholder="e.g. x1 - x3 - x4 = 0",
            )
        with col_preview:
            text = st.session_state.get(f"{key}_eq__{i}", "").strip()
            if text:
                try:
                    row = parse_equation(text)
                    st.latex(_row_to_latex(row, n))
                except ParseError:
                    st.caption("...")
            else:
                st.caption("...")


def equation_builder(key, n_unknowns, target_aug, row_labels, diagram_fn,
                     solution_labels, intro_md, reduce_caption, closing_md=None,
                     builder_intro_md=None):
    """Render the full equation-builder flow: diagram + node boxes, live [A|b], Check/Fill, workbench."""
    st.markdown(intro_md)

    diagram_col, builder_col = st.columns([0.5, 0.5], gap="large")
    with diagram_col:
        st.plotly_chart(diagram_fn(), use_container_width=True)
    with builder_col:
        _node_balance_builder(key, n_unknowns, row_labels, intro_md=builder_intro_md)

    st.markdown("**Your system as an augmented matrix [A | b]**")
    st.caption("Each equation you write becomes a row. Dashes mark rows you haven't written yet.")
    st.latex(_live_aug_latex(key, n_unknowns, n_rows=len(target_aug)))

    c1, c2 = st.columns(2)
    with c1:
        st.button("Check", key=f"{key}_check_btn", on_click=_check_cb,
                  args=(key, target_aug, row_labels))
    with c2:
        st.button("Fill it in for me", key=f"{key}_fill_btn", on_click=_fill_cb,
                  args=(key, target_aug))

    check = st.session_state.get(f"{key}_check_result")
    if check is not None:
        if not check:
            st.success(f"All {len(row_labels)} equations are correct.")
        else:
            parse_errs = set(st.session_state.get(f"{key}_parse_errors", []))
            msgs = []
            for i in check:
                if i in parse_errs:
                    msgs.append(f"{row_labels[i]} (couldn't read)")
                else:
                    msgs.append(f"{row_labels[i]} (wrong)")
            st.warning(f"Not quite -- check {', '.join(msgs)}.")

    if st.session_state.get(f"{key}_ready") and st.session_state.get(f"{key}_M"):
        st.markdown("---")
        st.markdown(reduce_caption)
        workbench(key, n_unknowns, solution_labels=solution_labels)
        if closing_md:
            st.info(closing_md)
