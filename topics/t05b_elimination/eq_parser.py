"""
Equation parser and equivalence checker for the Topic 5.5 logistics builder.

The student types a node balance equation (e.g. "x1 - x3 - x4 = 0" or
"x1 = x3 + x4"). parse_equation turns it into a coefficient row
[a1, ..., a7, b] meaning a1*x1 + ... + a7*x7 = b. rows_equivalent accepts any
nonzero scalar multiple of the target row, so algebraically rearranged or
rescaled forms are all treated as correct.
"""
import re
from fractions import Fraction

N_VARS = 7

_SUBS = {"₀": "0", "₁": "1", "₂": "2", "₃": "3",
         "₄": "4", "₅": "5", "₆": "6", "₇": "7",
         "₈": "8", "₉": "9"}


class ParseError(Exception):
    pass


def _normalize(s):
    s = s.strip()
    for k, v in _SUBS.items():
        s = s.replace(k, v)
    s = s.lower().replace(" ", "").replace("−", "-")
    return s


def _parse_side(expr):
    if expr == "":
        return {}, Fraction(0)
    if expr[0] not in "+-":
        expr = "+" + expr
    tokens = re.findall(r"[+-][^+-]+", expr)
    if not tokens:
        raise ParseError(f"could not read '{expr}'")
    coeffs, const = {}, Fraction(0)
    for tok in tokens:
        sign = 1 if tok[0] == "+" else -1
        body = tok[1:]
        if body == "":
            raise ParseError("dangling sign")
        m = re.fullmatch(r"(\d*\.?\d*)x(\d+)", body)
        if m:
            num, idx = m.group(1), int(m.group(2))
            if idx < 1 or idx > N_VARS:
                raise ParseError(f"x{idx} out of range 1..{N_VARS}")
            coeff = Fraction(1) if num in ("", ".") else Fraction(num)
            coeffs[idx - 1] = coeffs.get(idx - 1, Fraction(0)) + sign * coeff
            continue
        m2 = re.fullmatch(r"(\d+\.?\d*|\.\d+)", body)
        if m2:
            const += sign * Fraction(m2.group(1))
            continue
        raise ParseError(f"could not read term '{tok}'")
    return coeffs, const


def parse_equation(s):
    """Parse 'lhs = rhs' into [a1..a7, b] (Fractions) for a1*x1+...+a7*x7 = b."""
    s = _normalize(s)
    if s.count("=") != 1:
        raise ParseError("equation must contain exactly one '='")
    lhs, rhs = s.split("=")
    lc, lk = _parse_side(lhs)
    rc, rk = _parse_side(rhs)
    row = [Fraction(0)] * N_VARS
    for i, v in lc.items():
        row[i] += v
    for i, v in rc.items():
        row[i] -= v
    return row + [rk - lk]


def rows_equivalent(r1, r2):
    """True if r1 is a nonzero scalar multiple of r2 (length N_VARS+1 each)."""
    r1 = [x if isinstance(x, Fraction) else Fraction(x).limit_denominator(10**6) for x in r1]
    r2 = [x if isinstance(x, Fraction) else Fraction(x).limit_denominator(10**6) for x in r2]
    scale = None
    for a, b in zip(r1, r2):
        if b != 0:
            if a == 0:
                return False
            scale = a / b
            break
        elif a != 0:
            return False
    if scale is None:
        return all(x == 0 for x in r1)
    if scale == 0:
        return False
    return all(a == scale * b for a, b in zip(r1, r2))
