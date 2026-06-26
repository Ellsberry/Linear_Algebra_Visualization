import streamlit as st
from fractions import Fraction as Fr

from .rref_reducer import (
    make_augmented, compute_one_step, run_to_reduced,
    left_is_identity, right_block,
)

_N = 3
_KEY = "t05b_inv"

_EXAMPLES = {
    "Integer inverse":       [[2, 1, 1], [1, 3, 2], [1, 0, 0]],
    "Fractional inverse":    [[2, 0, 0], [1, 2, 0], [1, 1, 2]],
    "Singular (no inverse)": [[1, 2, 3], [2, 4, 6], [1, 0, 1]],
}


def _fmt_entry(v):
    """Format a Fraction as LaTeX: int or \\frac{p}{q}, with sign."""
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    num = abs(v.numerator)
    den = v.denominator
    frac = rf"\frac{{{num}}}{{{den}}}"
    return f"-{frac}" if v < 0 else frac


def _aug_latex(M, n):
    """Render the n x 2n augmented matrix [A | I/A^-1] with a LaTeX divider."""
    col_spec = "c" * n + "|" + "c" * n
    rows = []
    for row in M:
        cells = [_fmt_entry(row[j]) for j in range(2 * n)]
        rows.append(" & ".join(cells))
    body = r" \\ ".join(rows)
    return r"\left[\begin{array}{" + col_spec + r"}" + body + r"\end{array}\right]"


def _bmatrix(block):
    """Render a list-of-rows (Fractions) as a LaTeX bmatrix."""
    rows = []
    for row in block:
        cells = [_fmt_entry(v) for v in row]
        rows.append(" & ".join(cells))
    body = r" \\ ".join(rows)
    return r"\begin{bmatrix}" + body + r"\end{bmatrix}"


def _init(choice):
    A = _EXAMPLES[choice]
    M = make_augmented(A)
    st.session_state[f"{_KEY}_M"]      = M
    st.session_state[f"{_KEY}_orig"]   = [row[:] for row in M]
    st.session_state[f"{_KEY}_log"]    = []
    st.session_state[f"{_KEY}_hist"]   = []
    st.session_state[f"{_KEY}_status"] = None
    st.session_state[f"{_KEY}_last"]   = choice


def _step_cb():
    M = st.session_state[f"{_KEY}_M"]
    new_M, desc, status = compute_one_step(M, _N)
    if status == "step":
        st.session_state.setdefault(f"{_KEY}_hist", []).append([row[:] for row in M])
        st.session_state[f"{_KEY}_M"] = new_M
        st.session_state[f"{_KEY}_log"].append(desc)
    else:
        st.session_state[f"{_KEY}_status"] = status
        st.session_state[f"{_KEY}_log"].append(desc)


def _run_cb():
    M = st.session_state[f"{_KEY}_M"]
    st.session_state.setdefault(f"{_KEY}_hist", []).append([row[:] for row in M])
    final, steps, status = run_to_reduced(M, _N)
    st.session_state[f"{_KEY}_M"] = final
    st.session_state[f"{_KEY}_log"].extend(steps)
    st.session_state[f"{_KEY}_status"] = status


def _undo_cb():
    hist = st.session_state.get(f"{_KEY}_hist", [])
    if hist:
        st.session_state[f"{_KEY}_M"] = hist.pop()
        st.session_state[f"{_KEY}_hist"] = hist
        log = st.session_state.get(f"{_KEY}_log", [])
        if log:
            log.pop()
    st.session_state[f"{_KEY}_status"] = None


def _reset_cb():
    orig = st.session_state.get(f"{_KEY}_orig")
    if orig is not None:
        st.session_state[f"{_KEY}_M"] = [row[:] for row in orig]
    st.session_state[f"{_KEY}_log"]    = []
    st.session_state[f"{_KEY}_hist"]   = []
    st.session_state[f"{_KEY}_status"] = None


def render_inverse_elim():
    st.markdown(
        "**[A | I] -> [I | A^-1].** "
        "Augment A with the identity matrix, then row-reduce until the left block "
        "becomes I. At that point the right block has become A^-1. "
        "This is how you actually compute an inverse -- no formula, just elimination."
    )

    choice = st.selectbox("Example", list(_EXAMPLES.keys()), key=f"{_KEY}_sel")
    if st.session_state.get(f"{_KEY}_last") != choice:
        _init(choice)

    M = st.session_state.get(f"{_KEY}_M")
    if M is None:
        _init(choice)
        M = st.session_state[f"{_KEY}_M"]

    status   = st.session_state.get(f"{_KEY}_status")
    log      = st.session_state.get(f"{_KEY}_log", [])
    hist     = st.session_state.get(f"{_KEY}_hist", [])
    done     = (status == "done") or left_is_identity(M, _N)
    singular = status == "singular"

    left, right = st.columns([1, 1.3], gap="large")

    with right:
        st.latex(_aug_latex(M, _N))
        if log:
            st.caption(f"Last: {log[-1]}")
            if len(log) > 1:
                with st.expander(f"All operations ({len(log)})"):
                    for entry in log:
                        st.text(entry)
        if singular:
            st.warning(
                "A is singular -- the left block can't become the identity, "
                "so A has no inverse."
            )
        elif done:
            st.success("Left block is the identity -- the right block is A^-1.")

    with left:
        st.markdown("**Guided reduction**")
        st.button("Do one step", key=f"{_KEY}_step_btn",
                  on_click=_step_cb,
                  disabled=done or singular)
        st.button("Run to reduced form", key=f"{_KEY}_run_btn",
                  on_click=_run_cb,
                  disabled=done or singular)
        st.markdown("---")
        st.button("Undo", key=f"{_KEY}_undo_btn",
                  on_click=_undo_cb,
                  disabled=not bool(hist))
        st.button("Reset", key=f"{_KEY}_reset_btn",
                  on_click=_reset_cb)

    if done:
        inv = right_block(M, _N)
        st.markdown("---")
        st.markdown(
            "**Why does the right side become A^-1?** "
            "The sequence of row operations that turns A into I is, together, "
            "multiplication by A^-1 -- that is what 'reduces A to I' means. "
            "Those same operations applied to the identity on the right produce "
            "A^-1 * I = A^-1. So the right half gives you the inverse for free."
        )
        st.latex(r"A^{-1} = " + _bmatrix(inv))
