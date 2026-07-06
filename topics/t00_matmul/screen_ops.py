"""Topic 0, Screen 0 -- the seven matrix operations: what/why/examples, with
inline practice for addition, subtraction, scalar multiplication, and transpose."""
import numpy as np
import streamlit as st

from engine.widgets import editable_matrix, set_matrix_state

ADD_EXAMPLES = [
    (np.array([[2.0, 3.0], [5.0, 1.0]]),
     np.array([[4.0, 1.0], [2.0, 6.0]]),
     np.array([[6.0, 4.0], [7.0, 7.0]])),
    (np.array([[7.0, 0.0], [3.0, 4.0]]),
     np.array([[1.0, 5.0], [6.0, 2.0]]),
     np.array([[8.0, 5.0], [9.0, 6.0]])),
    (np.array([[3.0, 8.0], [2.0, 0.0]]),
     np.array([[5.0, 1.0], [7.0, 9.0]]),
     np.array([[8.0, 9.0], [9.0, 9.0]])),
]

SUB_EXAMPLES = [
    (np.array([[8.0, 6.0], [7.0, 9.0]]),
     np.array([[3.0, 2.0], [5.0, 4.0]]),
     np.array([[5.0, 4.0], [2.0, 5.0]])),
    (np.array([[9.0, 0.0], [6.0, 7.0]]),
     np.array([[4.0, 3.0], [2.0, 5.0]]),
     np.array([[5.0, -3.0], [4.0, 2.0]])),
    (np.array([[7.0, 8.0], [9.0, 0.0]]),
     np.array([[1.0, 3.0], [4.0, 2.0]]),
     np.array([[6.0, 5.0], [5.0, -2.0]])),
]

SCALAR_EXAMPLES = [
    (2, np.array([[3.0, 4.0], [1.0, 5.0]]), np.array([[6.0, 8.0], [2.0, 10.0]])),
    (3, np.array([[2.0, 0.0], [4.0, 1.0]]), np.array([[6.0, 0.0], [12.0, 3.0]])),
    (2, np.array([[6.0, 3.0], [0.0, 7.0]]), np.array([[12.0, 6.0], [0.0, 14.0]])),
]

TRANSPOSE_A = np.array([
    [2.0, 7.0, 4.0, 9.0],
    [5.0, 3.0, 8.0, 1.0],
    [6.0, 2.0, 5.0, 7.0],
    [3.0, 9.0, 1.0, 4.0],
])
TRANSPOSE_AT = np.array([
    [2.0, 5.0, 6.0, 3.0],
    [7.0, 3.0, 2.0, 9.0],
    [4.0, 8.0, 5.0, 1.0],
    [9.0, 1.0, 7.0, 4.0],
])

_SYMBOL_STYLE = (
    "display:flex;align-items:center;justify-content:center;"
    "font-size:2em;color:#e6e6e6;height:116px;margin-top:32px"
)
_KLABEL_STYLE = (
    "display:flex;align-items:center;justify-content:center;"
    "font-size:1.3em;font-weight:600;color:#e6e6e6;height:116px;margin-top:32px"
)


def _symbol(sym: str) -> None:
    st.markdown(f'<div style="{_SYMBOL_STYLE}">{sym}</div>', unsafe_allow_html=True)


def _klabel(k) -> None:
    st.markdown(f'<div style="{_KLABEL_STYLE}">k = {k:g}</div>', unsafe_allow_html=True)


def _op_header(title: str, subtitle: str, what_it_is: str, why_it_matters: str,
               examples: list) -> None:
    st.markdown(f"### {title} -- {subtitle}")
    st.markdown(f"**What it is:** {what_it_is}")
    st.markdown(f"**Why it matters:** {why_it_matters}")
    if examples:
        st.markdown("\n".join(f"- {e}" for e in examples))


def _init_answer(ans_key: str, dim: int, result: np.ndarray) -> None:
    # Show solution must set the answer cells BEFORE the number_input widgets
    # are instantiated this run -- writing to a widget's session_state key
    # after it has already been created in the same run raises
    # StreamlitAPIException. So _check_and_solve's button only sets this
    # flag + reruns; the actual write happens here, at the top of the caller,
    # before editable_matrix(..., editable=True) creates the widgets.
    reveal_key = f"{ans_key}_reveal"
    if st.session_state.get(reveal_key):
        set_matrix_state(ans_key, result)
        st.session_state[reveal_key] = False

    for i in range(dim):
        for j in range(dim):
            wkey = f"{ans_key}__{i}__{j}"
            if wkey not in st.session_state:
                st.session_state[wkey] = 0.0


def _check_and_solve(prefix: str, ans_key: str, answer: np.ndarray,
                      result: np.ndarray, dim: int) -> None:
    check_col, solve_col = st.columns(2)
    if check_col.button("Check", key=f"{prefix}_check"):
        wrong = [
            (i + 1, j + 1)
            for i in range(dim)
            for j in range(dim)
            if abs(answer[i, j] - result[i, j]) > 1e-6
        ]
        if not wrong:
            st.success("Correct -- every entry matches.")
        else:
            cells = ", ".join(f"(row {i}, col {j})" for i, j in wrong)
            st.warning(f"Not quite -- check: {cells}")

    if solve_col.button("Show solution", key=f"{prefix}_solve"):
        st.session_state[f"{ans_key}_reveal"] = True
        st.rerun()


def _binary_example(prefix: str, symbol: str, A: np.ndarray, B: np.ndarray,
                     result: np.ndarray) -> None:
    ans_key = f"{prefix}_ans"
    _init_answer(ans_key, 2, result)

    cols = st.columns([1, 0.2, 1, 0.2, 1])
    with cols[0]:
        editable_matrix(f"{prefix}_A", 2, label="A", editable=False, value=A, compact=True)
    with cols[1]:
        _symbol(symbol)
    with cols[2]:
        editable_matrix(f"{prefix}_B", 2, label="B", editable=False, value=B, compact=True)
    with cols[3]:
        _symbol("=")
    with cols[4]:
        answer = editable_matrix(ans_key, 2, label="Your answer", editable=True, compact=True)

    _check_and_solve(prefix, ans_key, answer, result, 2)


def _scalar_example(prefix: str, k, A: np.ndarray, result: np.ndarray) -> None:
    ans_key = f"{prefix}_ans"
    _init_answer(ans_key, 2, result)

    cols = st.columns([0.6, 0.2, 1, 0.2, 1])
    with cols[0]:
        _klabel(k)
    with cols[1]:
        _symbol("&middot;")
    with cols[2]:
        editable_matrix(f"{prefix}_A", 2, label="A", editable=False, value=A, compact=True)
    with cols[3]:
        _symbol("=")
    with cols[4]:
        answer = editable_matrix(ans_key, 2, label="Your answer", editable=True, compact=True)

    _check_and_solve(prefix, ans_key, answer, result, 2)


def _transpose_example() -> None:
    prefix = "t00_ops_transpose"
    ans_key = f"{prefix}_ans"
    dim = 4
    _init_answer(ans_key, dim, TRANSPOSE_AT)

    cols = st.columns([1, 0.2, 1])
    with cols[0]:
        editable_matrix(f"{prefix}_A", dim, label="A", editable=False,
                         value=TRANSPOSE_A, compact=True)
    with cols[1]:
        _symbol("&rarr;")
    with cols[2]:
        answer = editable_matrix(ans_key, dim, label="A^T (your answer)",
                                  editable=True, compact=True)

    _check_and_solve(prefix, ans_key, answer, TRANSPOSE_AT, dim)


def render_ops():
    st.markdown(
        "Every operation below shows up somewhere else in this app. Learn what "
        "each one does and why it matters before you meet it inside an example."
    )
    st.divider()

    # 1. Addition
    _op_header(
        "1. Addition", "Combine Systems",
        "Element-by-element sum, same dimensions.",
        "Merges systems, datasets, and transformations.",
        [
            "Combine two adjacency matrices to merge two networks",
            "Add two image matrices to blend images",
            "Add two transformation matrices to combine perturbations in physics",
        ],
    )
    add_cols = st.columns(3)
    for i, (A, B, result) in enumerate(ADD_EXAMPLES):
        with add_cols[i]:
            _binary_example(f"t00_ops_add{i + 1}", "+", A, B, result)
    st.divider()

    # 2. Subtraction
    _op_header(
        "2. Subtraction", "Compare Systems",
        "Element-by-element difference.",
        "Shows how two systems differ.",
        [
            "Compute residuals in regression (A - B)",
            "Compare two time-step states in a simulation",
            "Detect pixel-level differences between images",
        ],
    )
    sub_cols = st.columns(3)
    for i, (A, B, result) in enumerate(SUB_EXAMPLES):
        with sub_cols[i]:
            _binary_example(f"t00_ops_sub{i + 1}", "-", A, B, result)
    st.divider()

    # 3. Scalar multiplication
    _op_header(
        "3. Scalar Multiplication", "Scale a Transformation",
        "Multiply every entry by k.",
        "Uniformly scales the effect.",
        [
            "Adjust image brightness (k . image)",
            "Scale a geometric transformation (stretching)",
            "Increase or decrease coefficients in a system of equations",
        ],
    )
    scalar_cols = st.columns(3)
    for i, (k, A, result) in enumerate(SCALAR_EXAMPLES):
        with scalar_cols[i]:
            _scalar_example(f"t00_ops_scalar{i + 1}", k, A, result)
    st.divider()

    # 4. Matrix multiplication -- description only
    _op_header(
        "4. Matrix Multiplication", "Compose Transformations",
        "Row-by-column; A(m x n) . B(n x p) = m x p.",
        "Represents doing one transformation after another.",
        [
            "Graphics pipeline: rotate, then scale, then project",
            "Neural networks: each layer is a matrix multiplication",
            "Economics: combine input-output resource flows",
            "Robotics: combine coordinate transformations",
        ],
    )
    st.caption("Practiced on Screens 1-3.")
    st.divider()

    # 5. Transpose
    _op_header(
        "5. Transpose", "Flip Perspective",
        "Swap rows and columns.",
        "Essential for dot products, projections, and symmetry.",
        [
            'Switch between "input" and "output" perspectives in ML',
            "Compute dot products in matrix form (x^T y)",
            "Build projection matrices in geometry",
        ],
    )
    _transpose_example()
    st.divider()

    # 6. Inverse -- description only
    _op_header(
        "6. Inverse", "Undo a Transformation",
        "A^-1 with A . A^-1 = I; exists iff det != 0.",
        "Solves Ax = b and undoes a transformation.",
        [
            "Solve Ax = b as x = A^-1 b",
            "Undo a rotation or scaling",
            "Convert coordinates between bases",
        ],
    )
    st.caption("Described only -- see Topics 4 and 5.5.")
    st.divider()

    # 7. Division -- description only
    _op_header(
        "7. Division (via inverse)", "Solve Relationships",
        "No direct division; A / B = A . B^-1.",
        "Solve relationships between systems.",
        [
            "Solve for unknowns in engineering systems",
            "Normalize transformations",
            "Compute ratios of linear effects",
        ],
    )
    st.caption("Described only.")
