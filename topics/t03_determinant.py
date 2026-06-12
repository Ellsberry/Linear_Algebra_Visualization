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
        "A": np.array([[1.5, 0.0], [0.0, 1.5]]),
        "notice": (
            "If a scan is rescaled, every measured area — a tumor, a vessel — scales by "
            "the determinant. Radiologists calibrate so a 2 cm lesion still measures 2 cm."
        ),
    },
    "Tilt correction (shear)": {
        "A": np.array([[1.0, 0.6], [0.0, 1.0]]),
        "notice": (
            "When software shears a tilted scan into alignment, the shape skews but the "
            "area is unchanged (det = 1) — the correction doesn't falsify any measurement."
        ),
    },
}

_E4_PRESETS = {
    "Mirror (reflection)": {
        "A": np.array([[-1.0, 0.0], [0.0, 1.0]]),
        "notice": (
            "Games flip sprites to draw reflections, and use the *sign* of the determinant "
            "to tell which way a surface faces — that's how an engine skips drawing the "
            "hidden back of an object (back-face culling)."
        ),
    },
    "Shadow (collapse)": {
        "A": np.array([[1.0, 0.0], [0.0, 0.0]]),
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
            "The two edges from P become the columns of a matrix A whose "
            "determinant equals twice the triangle's area."
        )
        P = w.vector_editor("t03e1_P", 2, (1.0, 1.0), label="Corner P (m)")
        Q = w.vector_editor("t03e1_Q", 2, (6.0, 2.0), label="Corner Q (m)")
        R = w.vector_editor("t03e1_R", 2, (3.0, 5.0), label="Corner R (m)")

    u = Q - P
    v = R - P
    u0, u1 = float(u[0]), float(u[1])
    v0, v1 = float(v[0]), float(v[1])
    det = u0 * v1 - u1 * v0
    area = 0.5 * abs(det)

    with right:
        fig = plot.new_figure_2d(rng=10, x_title="meters →", y_title="meters ↑")
        plot.shade_polygon(fig, [P, P + u, P + u + v, P + v],
                           "rgba(0,150,136,0.10)", "parallelogram (det A)")
        plot.shade_polygon(fig, [P, Q, R], "rgba(0,150,136,0.28)", "land parcel (½ of it)")
        plot.add_vector_2d(fig, P, Q, "crimson", "edge u = Q−P (column 1 of A)")
        plot.add_vector_2d(fig, P, R, "royalblue", "edge v = R−P (column 2 of A)")
        plot.add_point_2d(fig, P, "black", "P")
        plot.add_point_2d(fig, Q, "black", "Q")
        plot.add_point_2d(fig, R, "black", "R")
        st.plotly_chart(fig, use_container_width=True)
        _det_meter(det, kind="area_tri")

    st.info(
        "Surveyors and mapping software compute a parcel's area straight from its corner "
        "coordinates — the determinant *is* the area (this is the \"shoelace formula\" "
        "inside every GIS and land-title system). The determinant is the area of the "
        "**parallelogram** the two edges span; your triangular plot is exactly **half** of "
        "that, which is where the ½ comes from."
    )

    with st.expander("Show the math"):
        xP, yP = float(P[0]), float(P[1])
        xQ, yQ = float(Q[0]), float(Q[1])
        xR, yR = float(R[0]), float(R[1])

        st.markdown(
            f"Corner points: P = ({xP:.4g}, {yP:.4g}), "
            f"Q = ({xQ:.4g}, {yQ:.4g}), "
            f"R = ({xR:.4g}, {yR:.4g})"
        )
        st.markdown(
            f"Edge vectors (the columns of A):  "
            f"**u** = Q − P = ({u0:.4g}, {u1:.4g}),  "
            f"**v** = R − P = ({v0:.4g}, {v1:.4g})"
        )
        st.latex(r"A = " + w.bmatrix(np.column_stack([u, v])))
        prod1 = u0 * v1
        prod2 = v0 * u1
        st.latex(
            r"\det A = ("
            + f"{u0:.4g}" + r")(" + f"{v1:.4g}" + r") - ("
            + f"{v0:.4g}" + r")(" + f"{u1:.4g}" + r")"
            + r" = " + f"{prod1:.4g}" + r" - " + f"{prod2:.4g}"
            + r" = \mathbf{" + f"{det:.2f}" + r"}"
            + r"\quad \leftarrow \text{the parallelogram's area}"
        )
        st.latex(
            r"\text{area of triangle} = \tfrac{1}{2} \times |\det A|"
            + r" = \tfrac{1}{2} \times |" + f"{det:.2f}" + r"|"
            + r" = \mathbf{" + f"{area:.2f}" + r"} \text{ m}^2"
        )
        st.markdown(
            "The ½ is because the triangle is half the parallelogram the two edges make."
        )
        shoelace = abs(xP * (yQ - yR) + xQ * (yR - yP) + xR * (yP - yQ)) / 2
        st.latex(
            r"\tfrac{1}{2}|x_P(y_Q - y_R) + x_Q(y_R - y_P) + x_R(y_P - y_Q)|"
            + rf" = {shoelace:.2f} \text{{ m}}^2"
        )
        st.caption("Same number — the shoelace formula is the determinant in disguise.")


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
            w.set_matrix_state("t03e2_A", info["A"])
            st.session_state["t03e2_last"] = preset

        st.info(info["notice"])
        A = w.matrix_editor("t03e2_A", 2, label="Alignment matrix A")
        t = w.scalar_slider("t03e2_t", "Morph t: identity → matrix A", 0.0, 1.0, 1.0, 0.01)

    At = animate.interpolate(A, t)
    det = float(np.linalg.det(A))

    with right:
        st.plotly_chart(plot.figure_2d(At, obj="square"), use_container_width=True)
        _det_meter(det, kind="area_sq")

    with st.expander("Show the math"):
        a, b = float(A[0, 0]), float(A[0, 1])
        c, d = float(A[1, 0]), float(A[1, 1])
        st.latex(r"\det A = " + w.bmatrix(A) + r" = a \cdot d - b \cdot c")
        st.latex(
            r"\det A = ("
            + f"{a:.4g}" + r")(" + f"{d:.4g}" + r") - ("
            + f"{b:.4g}" + r")(" + f"{c:.4g}" + r")"
            + r" = \mathbf{" + f"{det:.4f}" + r"}"
        )
        st.markdown(
            f"The scan region's area is multiplied by |det A| = {abs(det):.4f}."
        )
        st.markdown(
            "det = 1 means the area is preserved even though the shape changed "
            "(the tilt correction)."
        )


# ----------------------------------------------------------------------------
# Example 3 -- Biology
# ----------------------------------------------------------------------------

def _example_biology():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Biology.** A cell is roughly a cube. Scaling every side by k "
            "gives a diagonal matrix A whose determinant — the volume factor — "
            "grows much faster than its surface area."
        )
        k = w.scalar_slider(
            "t03e3_k", "Scale factor k (how many times bigger)", 0.5, 3.0, 1.5, 0.1
        )

    A = k * np.eye(3)
    volume = k ** 3
    surface = 6 * k ** 2
    ratio = 6 / k

    with right:
        st.plotly_chart(plot.figure_3d(A), use_container_width=True)
        _det_meter(volume, kind="volume", extra={"surface": surface, "ratio": ratio})

    st.info(
        "**k is the scale factor** — how many times bigger you make the cell. k = 2 means "
        "twice as wide, twice as tall, twice as deep. Volume scales with the determinant "
        "(k³), but the surface that feeds and cools a body only scales as k². So as things "
        "get bigger the surface-to-volume ratio drops — which is why cells stay tiny, why "
        "large animals need lungs, gills, and folded intestines, and why an elephant's "
        "ears are huge."
    )

    with st.expander("Show the math"):
        st.markdown(
            f"Scaling every axis by k gives A = diag(k, k, k) = diag({k:.4g}, {k:.4g}, {k:.4g}):"
        )
        st.latex(r"A = " + w.bmatrix(A))
        st.markdown(
            "For a diagonal matrix, the determinant is the product of the diagonal entries:"
        )
        st.latex(
            r"\det A = k \times k \times k = k^3"
            + r" = " + f"{k:.4g}" + r" \times " + f"{k:.4g}" + r" \times " + f"{k:.4g}"
            + r" = \mathbf{" + f"{volume:.2f}" + r"}"
            + r"\quad \leftarrow \text{the volume factor}"
        )
        st.latex(
            r"\text{surface area} = 6k^2 = 6 \times "
            + f"{k:.4g}^2 = {surface:.2f}"
        )
        st.markdown(
            f"At k = {k:.4g}, surface:volume = 6/k = 6/{k:.4g} = {ratio:.2f}."
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
            w.set_matrix_state("t03e4_A", info["A"])
            st.session_state["t03e4_last"] = preset

        st.info(info["notice"])
        A = w.matrix_editor("t03e4_A", 2, label="Matrix A")

    det = float(np.linalg.det(A))

    with right:
        st.plotly_chart(plot.figure_2d(A, obj="rocket"), use_container_width=True)
        _det_meter(det, kind="area_sq")
        st.info(
            "det = 0 means the transform has no inverse. Next topic: exactly when a "
            "transformation *can* be undone."
        )

    with st.expander("Show the math"):
        a, b = float(A[0, 0]), float(A[0, 1])
        c, d = float(A[1, 0]), float(A[1, 1])
        st.latex(
            r"\det A = a \cdot d - b \cdot c = ("
            + f"{a:.4g}" + r")(" + f"{d:.4g}" + r") - ("
            + f"{b:.4g}" + r")(" + f"{c:.4g}" + r")"
            + r" = \mathbf{" + f"{det:.4f}" + r"}"
        )
        st.markdown(
            "Area scales by |det A|; a negative sign means orientation flipped (mirror image); "
            "det = 0 means the area collapsed to nothing."
        )

        # A times the rocket's key vertices so the student sees the flip/collapse
        nose = plot._ROCKET[:, 0]
        fin_tip = plot._ROCKET[:, 3]
        window = plot._ROCKET_WINDOW

        st.markdown("**A · (rocket vertices):**")
        for label, x in [("nose", nose), ("right fin tip", fin_tip), ("window", window)]:
            xp = A @ x
            st.latex(
                r"A \cdot \begin{pmatrix}"
                + f"{x[0]:.2f}" + r" \\ " + f"{x[1]:.2f}"
                + r"\end{pmatrix} = \begin{pmatrix}"
                + f"{xp[0]:.2f}" + r" \\ " + f"{xp[1]:.2f}"
                + r"\end{pmatrix}"
                + r"\quad \text{(" + label + r")}"
            )
        st.markdown("Every other vertex transforms the same way.")
