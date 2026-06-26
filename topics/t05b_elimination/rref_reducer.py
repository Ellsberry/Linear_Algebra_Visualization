"""
[A|I] inverse-by-elimination reducer for Topic 5.5.

Operates on an n x 2n augmented matrix [A | I] of fractions.Fraction values.
Provides the row-operation primitives plus a Gauss-Jordan "one step" that drives
the left block toward the identity; when the left block is I, the right block is
A^-1. Detects the singular case (no inverse).

All arithmetic uses Fraction so inverses display exactly (1/2, -1/4, ...).
Pure logic -- no Streamlit. The screen wires these into the existing row-op UI.
"""
from fractions import Fraction as Fr


def make_augmented(A):
    """Build [A | I] as a list of rows of Fractions from an n x n matrix A."""
    n = len(A)
    out = []
    for i in range(n):
        left = [Fr(x) for x in A[i]]
        right = [Fr(1) if j == i else Fr(0) for j in range(n)]
        out.append(left + right)
    return out


def _fmt_factor(f):
    """Format a Fraction factor cleanly for step descriptions.

    Avoids nested strings like '1/5/2'. A whole number prints as an int; a
    fraction prints as 'p/q'.
    """
    f = Fr(f)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def left_is_identity(M, n, tol=0):
    for i in range(n):
        for j in range(n):
            want = Fr(1) if i == j else Fr(0)
            if M[i][j] != want:
                return False
    return True


def right_block(M, n):
    return [row[n:] for row in M]


def op_swap(M, i, j):
    M = [row[:] for row in M]
    M[i], M[j] = M[j], M[i]
    return M, f"R{i+1} <-> R{j+1}"


def op_scale(M, i, factor):
    factor = Fr(factor)
    M = [row[:] for row in M]
    M[i] = [factor * x for x in M[i]]
    return M, f"R{i+1} -> ({_fmt_factor(factor)}) R{i+1}"


def op_add_multiple(M, target, source, factor):
    factor = Fr(factor)
    M = [row[:] for row in M]
    M[target] = [a + factor * b for a, b in zip(M[target], M[source])]
    sign = "+" if factor >= 0 else "-"
    return M, f"R{target+1} -> R{target+1} {sign} ({_fmt_factor(abs(factor))}) R{source+1}"


def compute_one_step(M, n):
    """Return (new_M, desc, status) for ONE Gauss-Jordan step toward RREF.

    status: 'step' (an op was done), 'done' (left block already I),
            'singular' (a pivot column has no available pivot).
    """
    for p in range(n):
        if M[p][p] == 0:
            r = next((r for r in range(p + 1, n) if M[r][p] != 0), None)
            if r is None:
                return M, "no pivot in column %d -- A is singular (no inverse)" % (p + 1), "singular"
            newM, desc = op_swap(M, p, r)
            return newM, desc, "step"
        if M[p][p] != 1:
            newM, desc = op_scale(M, p, Fr(1) / M[p][p])
            return newM, desc, "step"
        for i in range(n):
            if i != p and M[i][p] != 0:
                newM, desc = op_add_multiple(M, i, p, -M[i][p])
                return newM, desc, "step"
    return M, "reduced -- left block is the identity", "done"


def run_to_reduced(M, n, max_steps=200):
    """Apply compute_one_step repeatedly. Returns (final_M, steps_list, status)."""
    steps = []
    cur = [row[:] for row in M]
    for _ in range(max_steps):
        newM, desc, status = compute_one_step(cur, n)
        if status == "done":
            return cur, steps, "done"
        if status == "singular":
            steps.append(desc)
            return cur, steps, "singular"
        cur = newM
        steps.append(desc)
    return cur, steps, "stopped"
