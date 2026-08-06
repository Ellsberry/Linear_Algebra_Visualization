"""
Parametric general-solution engine (shared).

Given an augmented matrix, returns the general solution in parametric form:
X = particular + sum over free vars of (free_var * direction_vector).
Uses sympy for exact rational arithmetic so fractions display cleanly
(e.g. 3/2, not 1.50). No Streamlit imports here -- pure math module.
"""
import sympy as sp


def _to_rational_matrix(M):
    """Convert a list-of-lists of floats to a sympy Matrix of exact Rationals.

    Each entry goes through sp.nsimplify(sp.Float(str(v)), rational=True) so
    that e.g. 1.5 -> 3/2 and 0.3333... -> 1/3 rather than staying a float.
    Routing through str(v) first avoids binary-float noise (e.g. 0.1 as a
    Python float) leaking into the Rational.
    """
    rows = [[sp.nsimplify(sp.Float(str(v)), rational=True) for v in row] for row in M]
    return sp.Matrix(rows)


def solve_parametric(M, n_unknowns, var_name="x"):
    """Solve an augmented system and return its general parametric solution.

    M: augmented matrix as a list of lists of floats (last column is b,
       the preceding n_unknowns columns are coefficients).
    n_unknowns: number of unknowns (coefficient columns).
    var_name: label base for free-variable subscripts in the output.

    Returns a dict:
      status: "unique" | "infinite" | "no_solution"
      particular: list of Rationals, length n_unknowns (unique/infinite only)
      free_vars: list of 1-based free-variable indices
      directions: list of (free_index, direction_vector) pairs, each vector
                  a list of Rationals of length n_unknowns
      n_free: number of free variables
    """
    aug = _to_rational_matrix(M)
    rref, pivots = aug.rref()
    pivots = list(pivots)

    b_col = n_unknowns

    for i in range(rref.rows):
        coeffs_zero = all(rref[i, c] == 0 for c in range(n_unknowns))
        if coeffs_zero and rref[i, b_col] != 0:
            return dict(status="no_solution")

    free_cols = [c for c in range(n_unknowns) if c not in pivots]

    particular = [sp.Integer(0)] * n_unknowns
    for row_idx, pcol in enumerate(pivots):
        if pcol < n_unknowns:
            particular[pcol] = rref[row_idx, b_col]

    directions = []
    for f in free_cols:
        vec = [sp.Integer(0)] * n_unknowns
        vec[f] = sp.Integer(1)
        for row_idx, pcol in enumerate(pivots):
            if pcol < n_unknowns:
                vec[pcol] = -rref[row_idx, f]
        directions.append((f + 1, vec))

    status = "unique" if not free_cols else "infinite"

    return dict(
        status=status,
        particular=particular,
        free_vars=[f + 1 for f in free_cols],
        directions=directions,
        n_free=len(free_cols),
    )


def _col_bmatrix(vec):
    """LaTeX bmatrix for a column vector of sympy values, via sp.latex (exact fractions)."""
    rows = r" \\ ".join(sp.latex(v) for v in vec)
    return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"


def parametric_latex(result, var_name="x"):
    """Render a solve_parametric() result as a LaTeX stacked-vector string."""
    if result["status"] == "no_solution":
        return r"\text{No solution: } 0 = \text{nonzero.}"

    n = len(result["particular"])
    x_col = _col_bmatrix([sp.Symbol(f"{var_name}_{{{i+1}}}") for i in range(n)])
    particular_col = _col_bmatrix(result["particular"])

    lhs = f"X = {x_col} = {particular_col}"

    if result["status"] == "unique":
        return lhs

    terms = [lhs]
    for idx, vec in result["directions"]:
        dir_col = _col_bmatrix(vec)
        terms.append(f"{var_name}_{{{idx}}} {dir_col}")

    return " + ".join(terms)


def solution_equations_latex(result, var_name="x"):
    """Return a list of LaTeX strings, one per unknown, expressing each variable
    in terms of the free variable(s). Pivot variables are solved from the RREF rows;
    free variables read '<var>_i = <var>_i' (i.e. = itself, the parameter)."""
    if result["status"] == "no_solution":
        return [r"\text{No solution.}"]

    n = len(result["particular"])
    free_syms = {idx: sp.Symbol(f"{var_name}{idx}") for idx in result["free_vars"]}

    lines = []
    for i in range(1, n + 1):
        if i in free_syms:
            lines.append(f"{var_name}{i} = " + sp.latex(free_syms[i]))
            continue
        expr = result["particular"][i - 1]
        for free_idx, vec in result["directions"]:
            coeff = vec[i - 1]
            if coeff != 0:
                expr = expr + coeff * free_syms[free_idx]
        lines.append(f"{var_name}{i} = " + sp.latex(expr))

    return lines
