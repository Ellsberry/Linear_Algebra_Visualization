"""Screen 3 -- The complete solution (particular + null)."""
import numpy as np
import streamlit as st

_BLUE = "#4dabf7"
_YELLOW = "#ffd43b"

# Locked, verified case (spec): RREF[A|b] = [[1,2,0,2],[0,0,1,2]],
# x_p = (2, 0, 2), null direction v = (-2, 1, 0). Computed live below.
_A = np.array([[1.0, 2.0, 2.0], [2.0, 4.0, 5.0]])
_B = np.array([6.0, 14.0])

_INTRO = """
When a system has **infinitely many** solutions, we don't list them one by one —
we write them with a formula called the **complete solution**. It has two parts
added together: one **particular solution** — any single point that satisfies
`Ax = b` — plus the **entire null space** of A, the directions you can move
without changing the result. In symbols:

**x = x_particular + (null-space part)**

You already met the null-space part in Vector Spaces: those are the inputs A
sends to zero. Adding any of them to a working solution gives another working
solution, because A turns that added piece into zero and leaves `b` unchanged.
"""

_WHY_BOTH = """
The particular solution pins you to the right "height" — it makes `Ax` equal `b`.
The null-space part lets you slide along every direction that doesn't change the
answer. One solution plus all the ways to move without consequence equals every
solution there is. When the null space is just the zero vector (nothing gets
crushed), the null part disappears and the particular solution is the *only*
solution — that's the one-answer case.
"""


def _rref(M, tol=1e-10):
    """Reduced row echelon form by Gauss-Jordan; returns (R, pivot_columns)."""
    R = M.astype(float).copy()
    rows, cols = R.shape
    pivots = []
    r = 0
    for c in range(cols):
        if r == rows:
            break
        p = r + int(np.argmax(np.abs(R[r:, c])))
        if abs(R[p, c]) < tol:
            continue
        R[[r, p]] = R[[p, r]]
        R[r] = R[r] / R[r, c]
        for i in range(rows):
            if i != r:
                R[i] = R[i] - R[i, c] * R[r]
        pivots.append(c)
        r += 1
    R[np.abs(R) < tol] = 0.0
    return R, pivots


def _solve_parts(A, b):
    """Particular solution (free vars = 0) and one null direction per free var."""
    n = A.shape[1]
    R, pivots = _rref(np.column_stack([A, b]))
    pivots = [c for c in pivots if c < n]
    free = [c for c in range(n) if c not in pivots]
    x_p = np.zeros(n)
    for row, pc in enumerate(pivots):
        x_p[pc] = R[row, n]
    nulls = []
    for f in free:
        v = np.zeros(n)
        v[f] = 1.0
        for row, pc in enumerate(pivots):
            v[pc] = -R[row, f]
        nulls.append(v)
    return R, pivots, free, x_p, nulls


def _g(v) -> str:
    return f"{float(v) + 0.0:g}"


def _col(v) -> str:
    """Plain column vector in LaTeX, compact number format."""
    return r"\begin{bmatrix}" + r" \\ ".join(_g(x) for x in v) + r"\end{bmatrix}"


def _ccol(v, color) -> str:
    """Colored column vector (per entry), compact number format."""
    return (r"\begin{bmatrix}"
            + r" \\ ".join(rf"\color{{{color}}}{{{_g(x)}}}" for x in v)
            + r"\end{bmatrix}")


def _aug_latex(R, pivots, free, n) -> str:
    """[R | b] with pivot columns yellow and free columns blue (per entry)."""
    rows = []
    for row in R:
        cells = []
        for j, val in enumerate(row):
            if j in pivots:
                cells.append(rf"\color{{{_YELLOW}}}{{{_g(val)}}}")
            elif j in free:
                cells.append(rf"\color{{{_BLUE}}}{{{_g(val)}}}")
            else:
                cells.append(_g(val))
        rows.append(" & ".join(cells))
    spec = "c" * n + "|c"
    return r"\left[\begin{array}{" + spec + "}" + r" \\ ".join(rows) + r"\end{array}\right]"


def render_complete():
    # --- Block 1 -- The idea in words ----------------------------------------
    st.markdown(_INTRO)

    st.divider()

    # --- Block 2 -- Work one (student fills the null part) -------------------
    st.markdown("**Work one.**")
    A, b = _A, _B
    m, n = A.shape
    R, pivots, free, x_p, nulls = _solve_parts(A, b)
    r = len(pivots)

    left, right = st.columns([0.5, 0.5])
    with left:
        st.latex(
            r"\begin{aligned}"
            + r" \\ ".join(
                " + ".join(rf"{_g(A[i, j])}x_{{{j + 1}}}" for j in range(n))
                + rf" &= {_g(b[i])}"
                for i in range(m)
            )
            + r"\end{aligned}"
        )
    with right:
        st.latex(r"\text{RREF}[A \mid b] = " + _aug_latex(R, pivots, free, n))
        st.caption(
            f"Pivots in columns {', '.join(str(c + 1) for c in pivots)}; free "
            f"variable {', '.join(f'x{c + 1}' for c in free)}. "
            f"rank r = {r}, m = {m}, n = {n}."
        )

    st.markdown("**Fill in the blue part of the complete solution:**")
    # Constrain to the left part so the pieces cluster instead of spanning the page.
    outer = st.columns([0.62, 0.38])
    with outer[0]:
        # tight inner columns for the equation pieces (small ratios, no big gaps)
        p = st.columns([0.16, 0.26, 0.24, 0.34], gap="small")
        with p[0]:
            st.latex(r"x =")
        with p[1]:
            st.latex(r"\underbrace{" + _col(x_p) + r"}_{\text{particular}}")
        with p[2]:
            st.latex(r"+\, x_2\!\cdot")
        with p[3]:
            v0 = st.number_input("top", value=0.0, step=1.0,
                                 key="t06b_comp_v0", label_visibility="collapsed")
            v1 = st.number_input("middle", value=0.0, step=1.0,
                                 key="t06b_comp_v1", label_visibility="collapsed")
            v2 = st.number_input("bottom", value=0.0, step=1.0,
                                 key="t06b_comp_v2", label_visibility="collapsed")
    st.caption("Type the three numbers of the null-space direction (the blue vector).")

    # live check (no button -- updates as they type)
    v = np.array([v0, v1, v2], float)
    Av = A @ v
    if np.allclose(v, 0):
        st.info("All zero -- the zero vector is always in the null space, but find a "
                "NONZERO direction.")
    elif np.allclose(Av, 0):
        st.success(f"Correct! A sends ({_g(v0)}, {_g(v1)}, {_g(v2)}) to (0, 0).")
        st.latex(
            r"x = \underbrace{" + _col(x_p) + r"}_{\text{particular}}"
            r" + \underbrace{x_2" + _ccol(v, _BLUE) + r"}_{\text{null space}}"
        )
        st.caption(
            "One free variable, so the null space is a 1-dimensional line. Any nonzero "
            f"multiple of ({', '.join(_g(x) for x in nulls[0])}) is a valid direction."
        )
    else:
        st.error(f"Not yet: A sends ({_g(v0)}, {_g(v1)}, {_g(v2)}) to "
                 f"({_g(Av[0])}, {_g(Av[1])}), not (0, 0).")

    st.divider()

    # --- Block 3 -- Why both parts -------------------------------------------
    st.markdown(_WHY_BOTH)
