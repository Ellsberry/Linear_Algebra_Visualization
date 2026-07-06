"""
Shared input widgets used by every topic.

These are the reusable building blocks of the "left panel". A topic module
calls these to render editable inputs; the engine handles Streamlit state so
presets and Reset work consistently everywhere.
"""
import numpy as np
import streamlit as st


def editable_matrix(state_key: str, dim: int = None, label: str = "A",
                    editable: bool = True, value=None,
                    compact: bool = False, rows: int = None,
                    cols: int = None) -> np.ndarray:
    """Render a matrix in bracket form with editable or read-only cells.

    editable=True  → number_input cells using session_state keys {state_key}__i__j
                     (same keys as matrix_editor, so presets/Reset keep working).
    editable=False → static text displaying the provided `value` array.
    compact=False (default, unchanged) preserves the original wide per-cell
    st.columns layout used by every existing caller. compact=True tightens the
    inter-cell spacing: read-only rows render as a single flex line (no
    per-cell column gutters) and editable rows use a narrower bracket width
    with gap="small" on the internal st.columns.
    dim renders a square dim x dim matrix (unchanged default behavior). For a
    non-square matrix, pass rows and cols instead (dim can be omitted); when
    rows/cols are omitted they each fall back to dim, so existing square
    callers are unaffected.
    Returns the matrix as a numpy array of shape (rows, cols).
    """
    st.markdown(f"**{label} =**")

    nrows = rows if rows is not None else dim
    ncols = cols if cols is not None else dim

    if nrows == 1:
        lb, rb = ["["], ["]"]
    else:
        lb = ["⎡"] + ["⎢"] * (nrows - 2) + ["⎣"]
        rb = ["⎤"] + ["⎥"] * (nrows - 2) + ["⎦"]

    bstyle = (
        "display:flex;align-items:center;justify-content:center;"
        "font-size:2.4em;line-height:1;color:#e6e6e6;min-height:58px"
    )
    vstyle = (
        "display:flex;align-items:center;justify-content:center;"
        "font-size:1.05em;font-weight:500;color:#e6e6e6;min-height:58px"
    )

    M = np.zeros((nrows, ncols))

    if compact and not editable:
        # A per-row st.columns([0.07, 1, 0.07]) call, nested inside a loop,
        # sits three Streamlit-column levels deep once this widget is itself
        # placed inside a caller's own columns (e.g. a 2x2 example grid whose
        # cells are A/B/answer columns). At dim=3+ (3+ loop iterations at
        # that depth) this produced phantom duplicate "0.00" rows -- a known
        # class of Streamlit rendering artifact from nesting st.columns more
        # than the officially-supported one level, especially inside a loop.
        # Fix: render each row as a single flex <div> (pure CSS, one
        # st.markdown() call, no nested st.columns at all) -- same approach
        # already used for the compact editable bracket below.
        row_style = (
            "display:flex;align-items:center;gap:0.35em;"
            "font-size:1.05em;font-weight:500;color:#e6e6e6;min-height:40px"
        )
        row_bstyle = (
            "display:flex;align-items:center;justify-content:center;"
            "font-size:2.4em;line-height:1;color:#e6e6e6;"
        )
        for i in range(nrows):
            row = value[i] if value is not None else np.zeros(ncols)
            M[i, :] = [float(x) for x in row]
            nums = "".join(
                f'<span style="min-width:1.6em;text-align:right;">{float(x):.2f}</span>'
                for x in row
            )
            row_html = (
                f'<div style="display:flex;align-items:center;gap:0.3em;">'
                f'<div style="{row_bstyle}">{lb[i]}</div>'
                f'<div style="{row_style}">{nums}</div>'
                f'<div style="{row_bstyle}">{rb[i]}</div>'
                f'</div>'
            )
            st.markdown(row_html, unsafe_allow_html=True)
        return M

    if compact and editable:
        # Draw the bracket as CSS borders on the SINGLE container that is the
        # immediate parent of the cell grid (the st.columns(...) call right
        # below) -- nothing else lives in it, so its rendered height is
        # exactly the two stacked number_input rows, never a guess and never
        # inflated by an intermediate wrapper. (An earlier version split the
        # left/right borders across two nested containers -- box_key wrapping
        # an inner_key wrapping the grid -- which put border-left on a
        # non-immediate ancestor; collapsing to one container removes that
        # asymmetry.) Corner "ticks" are real absolutely-positioned divs
        # (position:absolute is taken out of flow, so they add zero height)
        # rather than ::before/::after, since one element only gets two
        # pseudo-elements and we need all four corners. CSS is scoped to this
        # widget's own container key so no other screen is affected.
        box_key = f"{state_key}_compactbox"
        bcolor = "#e6e6e6"
        st.markdown(
            f"""
            <style>
            .st-key-{box_key}[data-testid="stVerticalBlock"],
            .st-key-{box_key} [data-testid="stVerticalBlock"] {{
                gap: 0rem !important;
            }}
            .st-key-{box_key}[data-testid="stElementContainer"],
            .st-key-{box_key} [data-testid="stElementContainer"] {{
                margin: 0 !important;
            }}
            .st-key-{box_key} [data-testid="stWidgetLabel"] {{
                display: none !important;
            }}
            .st-key-{box_key} {{
                position: relative;
                border-left: 2px solid {bcolor};
                border-right: 2px solid {bcolor};
                padding: 0 0.4em;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        tick = "position:absolute;width:7px;height:2px;background:{0};".format(bcolor)
        ticks_html = (
            f'<div style="{tick}top:0;left:-2px;"></div>'
            f'<div style="{tick}bottom:0;left:-2px;"></div>'
            f'<div style="{tick}top:0;right:-2px;"></div>'
            f'<div style="{tick}bottom:0;right:-2px;"></div>'
        )
        with st.container(key=box_key):
            st.markdown(ticks_html, unsafe_allow_html=True)
            cols = st.columns([1] * ncols, gap="small")
            for j in range(ncols):
                with cols[j]:
                    for i in range(nrows):
                        wkey = f"{state_key}__{i}__{j}"
                        if wkey not in st.session_state:
                            st.session_state[wkey] = 1.0 if i == j else 0.0
                        M[i, j] = st.number_input(
                            label=wkey, key=wkey, step=0.1, format="%.2f",
                            label_visibility="collapsed",
                        )
        return M

    bracket_w = 0.05 if compact else 0.07
    col_widths = [bracket_w] + [1] * ncols + [bracket_w]

    for i in range(nrows):
        cols = st.columns(col_widths, gap="small") if compact else st.columns(col_widths)
        cols[0].markdown(
            f'<div style="{bstyle}">{lb[i]}</div>', unsafe_allow_html=True,
        )
        for j in range(ncols):
            if editable:
                wkey = f"{state_key}__{i}__{j}"
                if wkey not in st.session_state:
                    st.session_state[wkey] = 1.0 if i == j else 0.0
                M[i, j] = cols[j + 1].number_input(
                    label=wkey, key=wkey, step=0.1, format="%.2f",
                    label_visibility="collapsed",
                )
            else:
                v = float(value[i, j]) if value is not None else 0.0
                M[i, j] = v
                cols[j + 1].markdown(
                    f'<div style="{vstyle}">{v:.2f}</div>',
                    unsafe_allow_html=True,
                )
        cols[ncols + 1].markdown(
            f'<div style="{bstyle}">{rb[i]}</div>', unsafe_allow_html=True,
        )
    return M


def matrix_editor(state_key: str, dim: int, label: str = "Matrix M") -> np.ndarray:
    """Render a dim x dim grid of number inputs and return the matrix.

    Cell values live in st.session_state under keys "{state_key}__i__j" so that
    presets and Reset (which write those keys) take effect automatically.
    """
    st.markdown(f"**{label}**")
    M = np.zeros((dim, dim))
    for i in range(dim):
        cols = st.columns(dim)
        for j in range(dim):
            wkey = f"{state_key}__{i}__{j}"
            if wkey not in st.session_state:
                st.session_state[wkey] = 1.0 if i == j else 0.0
            M[i, j] = cols[j].number_input(
                label=wkey,
                key=wkey,
                step=0.1,
                format="%.2f",
                label_visibility="collapsed",
            )
    return M


def vector_editor(state_key: str, dim: int, default, label: str = "Vector v") -> np.ndarray:
    """Render dim number inputs in a row and return the vector."""
    st.markdown(f"**{label}**")
    v = np.zeros(dim)
    cols = st.columns(dim)
    for i in range(dim):
        wkey = f"{state_key}__{i}"
        if wkey not in st.session_state:
            st.session_state[wkey] = float(default[i])
        v[i] = cols[i].number_input(
            label=wkey,
            key=wkey,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
        )
    return v


def scalar_slider(state_key: str, label: str, lo: float, hi: float,
                  default: float, step: float = 0.01) -> float:
    """Render a single labelled slider."""
    if state_key not in st.session_state:
        st.session_state[state_key] = default
    return st.slider(label, min_value=lo, max_value=hi, step=step, key=state_key)


def set_matrix_state(state_key: str, M: np.ndarray) -> None:
    """Write a matrix into session_state so the editor picks it up (used by presets/Reset).

    Works for non-square M too (uses both dimensions of M.shape, not just
    rows) -- square callers are unaffected since rows == cols for them.
    """
    nrows, ncols = M.shape
    for i in range(nrows):
        for j in range(ncols):
            st.session_state[f"{state_key}__{i}__{j}"] = float(M[i, j])


def bmatrix(M: np.ndarray) -> str:
    """Format a numpy matrix (or column vector) as a LaTeX bmatrix string."""
    M = np.atleast_2d(M)
    rows = r" \\ ".join(" & ".join(f"{val:.2f}" for val in row) for row in M)
    return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"


def set_vector_state(state_key: str, v) -> None:
    """Write a vector into session_state so vector_editor picks it up (presets/Reset)."""
    for i in range(len(v)):
        st.session_state[f"{state_key}__{i}"] = float(v[i])


def aug_array_latex(M, n_unknowns: int, highlight=None) -> str:
    """LaTeX string for an augmented matrix [A | b].

    M is a list of rows, each with n_unknowns + 1 floats (last entry is b).
    Produces \\left[\\begin{array}{cc...|c} ... \\end{array}\\right].
    highlight: optional (row, col) to color/bold that entry in accent blue.
    """
    col_spec = "c" * n_unknowns + "|c"

    def _fmt(v: float) -> str:
        v = float(v)
        if abs(v) < 1e-10:
            return "0"
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.4g}"

    row_strs = []
    for ri in range(len(M)):
        cells = []
        for ci in range(n_unknowns + 1):
            entry = _fmt(M[ri][ci])
            if highlight is not None and (ri, ci) == highlight:
                entry = r"\textcolor{#4dabf7}{\mathbf{" + entry + r"}}"
            cells.append(entry)
        row_strs.append(" & ".join(cells))
    rows = r" \\ ".join(row_strs)
    return r"\left[\begin{array}{" + col_spec + r"}" + rows + r"\end{array}\right]"
