"""
Topic 3 -- Determinant.

Pattern: MULTI-EXAMPLE. A top selector chooses one of four real-world screens;
only the selected screen renders. OVERVIEW pinned at top; HOWTO in a collapsed
expander. Follow the t01 structural template.
"""
import streamlit as st

TITLE = "3 · Determinant"
SLUG = "determinant"

OVERVIEW = """
A determinant is one number that answers a simple question: when a
transformation acts on space, **by what factor does area (in 2D) or volume (in
3D) change — and does it flip things into a mirror image?** That single number
turns out to matter to surveyors, radiologists, biologists, and game
programmers. We'll meet it in all four fields, and each time you'll see the
determinant *is* an area or a volume — not just a formula.

Here's the formula in letters (the examples fill in real numbers):
"""

HOWTO = """
The left panel sets the numbers; the right panel shows the shape. The
**determinant meter** under each picture shows the determinant and the area or
volume it equals — watch them change together. Open **Show the math** to see
the formula behind the number.
"""

# ----------------------------------------------------------------------------
# Shared helper: determinant meter
# ----------------------------------------------------------------------------

def _det_meter(det, kind, extra=None):
    st.metric("Determinant", f"{det:.4f}")
    if abs(det) <= 1e-9:
        st.warning("collapses — area is zero, no inverse.")
    elif det < 0:
        if kind == "area_tri":
            st.info(
                f"det is negative — you listed the corners clockwise. "
                f"Area is still ½|det| = {0.5 * abs(det):.2f} m²; "
                "surveyors keep a consistent corner order to control the sign."
            )
        else:
            st.info(f"orientation flips (det < 0); area = |det| = {abs(det):.2f}")
    else:
        if kind == "area_tri":
            st.markdown(f"area = ½ × |det| = {0.5 * abs(det):.2f} m²")
        elif kind == "area_sq":
            st.markdown(f"area scales by ×{det:.2f}")
        else:  # volume
            st.markdown(
                f"volume = det = {det:.2f}; "
                f"surface = {extra['surface']:.2f}; "
                f"surface:volume = {extra['ratio']:.2f}"
            )


# _det_meter is defined above; submodules import it via `from . import _det_meter`
from .surveying import _example_surveying
from .medical import _example_medical
from .biology import _example_biology
from .graphics import _example_graphics


# ----------------------------------------------------------------------------
# Top-level render
# ----------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)
    st.latex(
        r"\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc"
        r"\qquad \text{(2D)}"
    )
    st.latex(
        r"\det \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}"
        r" = a(ei - fh) - b(di - fg) + c(dh - eg)"
        r"\qquad \text{(3D)}"
    )
    st.markdown(
        "The 3D formula looks like a lot, but notice each term is just one top-row entry "
        "times a little 2×2 determinant of what's left — it's the 2D formula used three "
        "times. And when the matrix is simple, like the diagonal one in biology, almost "
        "everything is zero and it collapses to just the diagonal multiplied together."
    )

    st.caption(
        "The left panel sets the numbers and shows the math; the right panel "
        "shows the shape. The determinant meter shows the determinant and the "
        "area or volume it equals — watch them change together."
    )

    example = st.radio(
        "Example",
        ["1 · Surveying", "2 · Medical imaging", "3 · Biology", "4 · Graphics"],
        horizontal=True,
        key="t03_example",
    )
    st.divider()

    if example.startswith("1"):
        _example_surveying()
    elif example.startswith("2"):
        _example_medical()
    elif example.startswith("3"):
        _example_biology()
    else:
        _example_graphics()
