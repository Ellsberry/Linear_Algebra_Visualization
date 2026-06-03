"""
Topic 3 -- Determinant.

Pattern: MULTI-EXAMPLE. A top selector chooses one of four real-world screens;
only the selected screen renders. OVERVIEW pinned at top; HOWTO in a collapsed
expander. Follow the t01 structural template.
"""
import numpy as np
import streamlit as st

from engine import animate
from engine import plotting as plot
from engine import widgets as w

TITLE = "3 · Determinant"
SLUG = "determinant"

OVERVIEW = """
A determinant is one number that answers a simple question: when a
transformation acts on space, **by what factor does area (in 2D) or volume (in
3D) change — and does it flip things into a mirror image?** That single number
turns out to matter to surveyors, radiologists, biologists, and game
programmers. We'll meet it in all four fields, and each time you'll see the
determinant *is* an area or a volume — not just a formula.
"""

HOWTO = """
The left panel sets the numbers; the right panel shows the shape. The
**determinant meter** under each picture shows the determinant and the area or
volume it equals — watch them change together. Open **Show the math** to see
the formula behind the number.
"""

_E2_PRESETS = {
    "Calibration (rescale)": {
        "M": np.array([[1.5, 0.0], [0.0, 1.5]]),
        "notice": (
            "If a scan is rescaled, every measured area — a tumor, a vessel — scales by "
            "the determinant. Radiologists calibrate so a 2 cm lesion still measures 2 cm."
        ),
    },
    "Tilt correction (shear)": {
        "M": np.array([[1.0, 0.6], [0.0, 1.0]]),
        "notice": (
            "When software shears a tilted scan into alignment, the shape skews but the "
            "area is unchanged (det = 1) — the correction doesn't falsify any measurement."
        ),
    },
}

_E4_PRESETS = {
    "Mirror (reflection)": {
        "M": np.array([[-1.0, 0.0], [0.0, 1.0]]),
        "notice": (
            "Games flip sprites to draw reflections, and use the *sign* of the determinant "
            "to tell which way a surface faces — that's how an engine skips drawing the "
            "hidden back of an object (back-face culling)."
        ),
    },
    "Shadow (collapse)": {
        "M": np.array([[1.0, 0.0], [0.0, 0.0]]),
        "notice": (
            "A shadow flattens an object onto the ground. det = 0 means the area is gone — "
            "and you can't rebuild the rocket from its shadow. There is no way to undo it."
        ),
    },
}


# ----------------------------------------------------------------------------
# Shared helper: determinant meter
# ----------------------------------------------------------------------------

def _det_meter(det, kind, extra=None):
    st.metric("Determinant", f"{det:.4f}")
    if abs(det) <= 1e-9:
        st.warning("collapses — area is zero, no inverse.")
    elif det < 0:
        msg = f"orientation flips (det < 0); area = |det| = {abs(det):.2f}"
        if kind == "area_tri":
            msg += (
                " — det is negative — you listed the corners clockwise. "
                "Area is still ½|det|; surveyors keep a consistent corner order "
                "to control the sign."
            )
        st.info(msg)
    else:
        if kind == "area_tri":
            msg = f"area = ½ × |det| = {0.5 * abs(det):.2f} m²"
        elif kind == "area_sq":
            msg = f"area scales by ×{det:.2f}"
        else:  # volume
            msg = (
                f"volume = det = {det:.2f}; "
                f"surface = {extra['surface']:.2f}; "
                f"surface:volume = {extra['ratio']:.2f}"
            )
        st.markdown(msg)


# ----------------------------------------------------------------------------
# Top-level render
# ----------------------------------------------------------------------------

def render():
    st.markdown(OVERVIEW)
    with st.expander("How to use this screen"):
        st.markdown(HOWTO)

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


# ----------------------------------------------------------------------------
# Example 1 -- Surveying (engineering)
# ----------------------------------------------------------------------------

def _example_surveying():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Surveying.** Enter three corner coordinates of a land parcel. "
            "The determinant of the two edge vectors from A equals twice the triangle's area."
        )
        A = w.vector_editor("t03e1_A", 2, (1.0, 1.0), label="Corner A (m)")
        B = w.vector_editor("t03e1_B", 2, (6.0, 2.0), label="Corner B (m)")
        C = w.vector_editor("t03e1_C", 2, (3.0, 5.0), label="Corner C (m)")

    u = B - A
    v = C - A
    det = float(u[0] * v[1] - u[1] * v[0])
    area = 0.5 * abs(det)

    with right:
        fig = plot.new_figure_2d(rng=10, x_title="meters →", y_title="meters ↑")
        plot.shade_polygon(fig, [A, A + u, A + u + v, A + v],
                           "rgba(0,150,136,0.10)", "parallelogram (2× the triangle)")
        plot.shade_polygon(fig, [A, B, C], "rgba(0,150,136,0.28)", "land parcel")
        plot.add_vector_2d(fig, A, B, "crimson", "edge B−A")
        plot.add_vector_2d(fig, A, C, "royalblue", "edge C−A")
        plot.add_point_2d(fig, A, "black", "A")
        plot.add_point_2d(fig, B, "black", "B")
        plot.add_point_2d(fig, C, "black", "C")
        st.plotly_chart(fig, use_container_width=True)
        _det_meter(det, kind="area_tri")

    st.info(
        "Surveyors and mapping software compute a parcel's area straight from its corner "
        "coordinates — the determinant *is* the area (this is the \"shoelace formula\" "
        "inside every GIS and land-title system). The triangle is exactly half the "
        "parallelogram its two edges span."
    )

    with st.expander("Show the math"):
        st.latex(
            r"\text{area} = \tfrac{1}{2} \left| \det"
            + w.bmatrix(np.column_stack([u, v]))
            + r"\right| = \tfrac{1}{2} \times "
            + f"|{det:.2f}| = {area:.2f}"
            + r"\text{ m}^2"
        )
        xA, yA = float(A[0]), float(A[1])
        xB, yB = float(B[0]), float(B[1])
        xC, yC = float(C[0]), float(C[1])
        st.latex(
            r"\tfrac{1}{2}|x_A(y_B - y_C) + x_B(y_C - y_A) + x_C(y_A - y_B)|"
            + rf" = {abs(xA*(yB-yC) + xB*(yC-yA) + xC*(yA-yB))/2:.2f}"
            + r"\text{ m}^2"
        )
        st.caption("Both formulas give the same number — the shoelace formula is the determinant in disguise.")


# ----------------------------------------------------------------------------
# Example 2 -- Medical imaging
# ----------------------------------------------------------------------------

def _example_medical():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Medical imaging.** A scan alignment matrix rescales or shears the image. "
            "The determinant tells you how every measured area inside the scan changes."
        )
        preset = st.selectbox("Preset", list(_E2_PRESETS), key="t03e2_preset")
        info = _E2_PRESETS[preset]

        if st.session_state.get("t03e2_last") != preset:
            w.set_matrix_state("t03e2_M", info["M"])
            st.session_state["t03e2_last"] = preset

        st.info(info["notice"])
        M = w.matrix_editor("t03e2_M", 2, label="Alignment matrix M")
        t = w.scalar_slider("t03e2_t", "Morph: identity → matrix", 0.0, 1.0, 1.0, 0.01)

    Mt = animate.interpolate(M, t)
    det = float(np.linalg.det(M))

    with right:
        st.plotly_chart(plot.figure_2d(Mt, obj="square"), use_container_width=True)
        _det_meter(det, kind="area_sq")

    with st.expander("Show the math"):
        st.latex(r"\det(M) = " + w.bmatrix(M) + f" = {det:.4f}")
        st.markdown("area scales by |det|; det = 1 means area is preserved even though the shape changed.")


# ----------------------------------------------------------------------------
# Example 3 -- Biology
# ----------------------------------------------------------------------------

def _example_biology():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Biology.** A cell is roughly a cube scaled by k. "
            "Volume is the determinant of kI — and it grows much faster than surface area."
        )
        k = w.scalar_slider("t03e3_k", "Scale factor k", 0.5, 3.0, 1.5, 0.1)

    M = k * np.eye(3)
    volume = k ** 3
    surface = 6 * k ** 2
    ratio = 6 / k

    with right:
        st.plotly_chart(plot.figure_3d(M), use_container_width=True)
        _det_meter(volume, kind="volume", extra={"surface": surface, "ratio": ratio})

    st.info(
        "Volume scales with the determinant (k³), but the surface that feeds and cools a "
        "body only scales as k². So as things get bigger the surface-to-volume ratio "
        "drops — which is why cells stay tiny, why large animals need lungs, gills, and "
        "folded intestines, and why an elephant's ears are huge."
    )

    with st.expander("Show the math"):
        st.latex(
            r"\det(kI) = k^3 = " + f"{volume:.2f}"
            + r"\qquad \text{surface} = 6k^2 = " + f"{surface:.2f}"
        )
        st.markdown(
            f"Volume grows as k³ while surface grows as k². "
            f"At k = {k:.1f}, surface:volume = 6/k = {ratio:.2f}."
        )


# ----------------------------------------------------------------------------
# Example 4 -- Graphics
# ----------------------------------------------------------------------------

def _example_graphics():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Graphics.** The sign of the determinant tells you if orientation flipped; "
            "zero means the object has been collapsed to a lower dimension."
        )
        preset = st.selectbox("Preset", list(_E4_PRESETS), key="t03e4_preset")
        info = _E4_PRESETS[preset]

        if st.session_state.get("t03e4_last") != preset:
            w.set_matrix_state("t03e4_M", info["M"])
            st.session_state["t03e4_last"] = preset

        st.info(info["notice"])
        M = w.matrix_editor("t03e4_M", 2, label="Matrix M")

    det = float(np.linalg.det(M))

    with right:
        st.plotly_chart(plot.figure_2d(M, obj="rocket"), use_container_width=True)
        _det_meter(det, kind="area_sq")
        st.info(
            "det = 0 means the transform has no inverse. Next topic: exactly when a "
            "transformation *can* be undone."
        )
