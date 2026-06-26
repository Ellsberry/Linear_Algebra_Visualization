"""
Symbolic equation parser for the Topic 5.5 circuit screen.

Student types circuit equations using resistor/voltage SYMBOLS and current
variables, e.g. "R1*I1 + R3*I3 = V" or "I1 - I2 - I3 - I5 = 0". The parser
substitutes the known symbol values to produce a coefficient row [c1..c5, b]
meaning c1*I1 + ... + c5*I5 = b. Equivalence is a nonzero scalar multiple of
the target row (rearranged/rescaled forms accepted; wrong resistors or signs
rejected because they change the coefficients).
"""
import re
from fractions import Fraction

N_VARS = 5  # I1..I5

SYMBOLS = {
    "r1": Fraction(2), "r2": Fraction(6), "r3": Fraction(8),
    "r4": Fraction(4), "r5": Fraction(12), "v": Fraction(36),
}

_SUBS = {"₀":"0","₁":"1","₂":"2","₃":"3","₄":"4",
         "₅":"5","₆":"6","₇":"7","₈":"8","₉":"9"}


class ParseError(Exception):
    pass


def _normalize(s):
    s = s.strip()
    for k, v in _SUBS.items():
        s = s.replace(k, v)
    s = s.lower().replace(" ", "").replace("−", "-")
    s = s.replace("·", "*")
    return s


def _split_juxtaposed(body):
    parts = re.findall(r"r\d+|v|i\d+|\d+\.?\d*|\.\d+", body)
    if "".join(parts) != body:
        raise ParseError(f"could not read term '{body}'")
    return parts


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
        factors = body.split("*") if "*" in body else _split_juxtaposed(body)
        coeff = Fraction(1)
        var_idx = None
        for f in factors:
            if f == "":
                raise ParseError(f"bad term '{tok}'")
            mvar = re.fullmatch(r"i(\d+)", f)
            if mvar:
                idx = int(mvar.group(1))
                if idx < 1 or idx > N_VARS:
                    raise ParseError(f"I{idx} out of range 1..{N_VARS}")
                if var_idx is not None:
                    raise ParseError(f"two currents in one term '{tok}'")
                var_idx = idx - 1
                continue
            if f in SYMBOLS:
                coeff *= SYMBOLS[f]
                continue
            mnum = re.fullmatch(r"\d+\.?\d*|\.\d+", f)
            if mnum:
                coeff *= Fraction(mnum.group(0))
                continue
            raise ParseError(f"unknown symbol '{f}' in '{tok}'")
        if var_idx is None:
            const += sign * coeff
        else:
            coeffs[var_idx] = coeffs.get(var_idx, Fraction(0)) + sign * coeff
    return coeffs, const


def parse_circuit_equation(s):
    """Parse 'lhs = rhs' into [c1..c5, b] (Fractions), substituting symbol values."""
    s = _normalize(s)
    if s.count("=") != 1:
        raise ParseError("equation must contain exactly one '='")
    lhs, rhs = s.split("=")
    lc, lk = _parse_side(lhs)
    rc, rk = _parse_side(rhs)
    row = [Fraction(0)] * N_VARS
    for i, val in lc.items():
        row[i] += val
    for i, val in rc.items():
        row[i] -= val
    return row + [rk - lk]


def rows_equivalent(r1, r2):
    """True if r1 is a nonzero scalar multiple of r2."""
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
