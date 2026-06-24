"""
Topic 4 -- Inverse Transformations.

Pattern: MULTI-EXAMPLE. A top selector chooses one of four screens.
Two recurring devices used throughout:
  - There-and-back: slider t in [0,1] + radio Apply M / Undo with M-1.
  - Inverse meter: shows M-1 and 1/det, or warns when det = 0.
"""
import numpy as np
import streamlit as st

from engine import animate
from engine import plotting as plot
from engine import widgets as w

TITLE = "4 · Inverse Transformations"
SLUG = "inverse"

OVERVIEW = """
Topic 3 ended on a cliffhanger: det = 0 means a transformation can't be undone.
This topic is the answer. The **inverse** of a transformation is the one that
reverses it — apply M, then apply M⁻¹, and every point lands exactly back where
it started. It exists only when det ≠ 0, and it scales area by 1/det. We'll meet
"undoing" as the central question in four fields: robotics, secret codes,
medical scans, and business planning.
"""

HOWTO = """
The left panel sets the numbers; the right panel shows the shape or the result.
On the visual screens, use **Apply M / Undo with M⁻¹** to watch a shape deform
and then return home. The **inverse meter** shows M⁻¹ and 1/det — or warns you
when there's no inverse.
"""

_E1_PRESETS = {
    "Reachable pose": np.array([[1.5, 0.5], [0.0, 1.0]]),
    "Singular pose":  np.array([[1.0, 1.0], [1.0, 1.0]]),
}

_E3_PRESETS = {
    "Full data":                          np.array([[1.0, 0.5], [0.5, 1.0]]),
    "Too few angles (unstable)":          np.array([[1.0, 1.0], [1.0, 1.05]]),
    "No data in a direction (singular)":  np.array([[1.0, 1.0], [1.0, 1.0]]),
}

# ----------------------------------------------------------------------------
# Shared helpers
# ----------------------------------------------------------------------------

def _mod_inv_matrix(M_int, mod=26):
    """Modular inverse of a 2x2 integer matrix mod `mod`; returns None if it doesn't exist."""
    a, b, c, d = int(M_int[0, 0]), int(M_int[0, 1]), int(M_int[1, 0]), int(M_int[1, 1])
    det_int = a * d - b * c
    det_mod = det_int % mod
    try:
        det_inv = pow(det_mod, -1, mod)
    except ValueError:
        return None
    adj = np.array([[d, -b], [-c, a]])
    return (det_inv * adj) % mod


def _inv_meter(M):
    det = float(np.linalg.det(M))
    st.metric("Determinant", f"{det:.4f}")
    if abs(det) > 1e-9:
        Minv = np.linalg.inv(M)
        st.latex(r"M^{-1} = " + w.bmatrix(Minv))
        st.markdown(f"invertible — area scales by 1/det = {1/det:.3f}")
    else:
        st.warning("det = 0 — no inverse. This transform can't be undone.")


# _inv_meter and preset dicts are defined above; submodules import them via
# `from . import _inv_meter, _E1_PRESETS` etc.
from .robotics import _example_robotics
from .medical import _example_medical
from .cryptography import _example_crypto
from .business import _example_business


# ----------------------------------------------------------------------------
# Top-level render
# ----------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)
    with st.expander("How to use this screen"):
        st.markdown(HOWTO)

    example = st.radio(
        "Example",
        ["1 · Robotics", "2 · Cryptography", "3 · Medical imaging", "4 · Business"],
        horizontal=True,
        key="t04_example",
    )
    st.divider()

    if example.startswith("1"):
        _example_robotics()
    elif example.startswith("2"):
        _example_crypto()
    elif example.startswith("3"):
        _example_medical()
    else:
        _example_business()
