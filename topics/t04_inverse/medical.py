"""Example 3 -- Medical imaging (mix/unmix leg-bone reconstruction)."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

from . import _inv_meter, _E3_PRESETS

_OUTER = np.array([
    [2.2, 0.0], [1.91, 1.5], [1.1, 2.6], [0.0, 3.0], [-1.1, 2.6], [-1.91, 1.5],
    [-2.2, 0.0], [-1.91, -1.5], [-1.1, -2.6], [0.0, -3.0], [1.1, -2.6], [1.91, -1.5],
]).T
_MARROW = np.array([
    [0.9, 0.0], [0.78, 0.65], [0.45, 1.13], [0.0, 1.3], [-0.45, 1.13], [-0.78, 0.65],
    [-0.9, 0.0], [-0.78, -0.65], [-0.45, -1.13], [0.0, -1.3], [0.45, -1.13], [0.78, -0.65],
]).T
_P1 = np.array([0.0, 3.0])   # bone edge (top of outer ring)
_P2 = np.array([0.9, 0.0])   # marrow edge


def _example_medical():
    st.markdown(
        "**Medical imaging.** A CT scanner can't photograph a slice of you directly. It "
        "shoots X-rays through the body from many angles and records how much comes out the "
        "other side. Each reading isn't a picture — it's a blend of everything along that "
        "X-ray's path.\n\n"
        "The shape below is a cross-section of a leg bone: the outer ring is hard bone, the "
        "inner ring is the soft marrow inside. We pick out specific points on it — call them "
        "p1, p2 — the true positions of the bone's edge and the marrow's edge.\n\n"
        "**Matrix A is built into the scanner.** It's set by the manufacturer and describes "
        "the physics of how X-rays pass through and get measured — how many angles, where "
        "the detectors sit. Multiplying a true point by the matrix A gives the scanner's "
        "measurement of that point — so A turns each real position on the slice into the "
        "reading the machine records.\n\n"
        "**Matrix A⁻¹ runs it backward.** It takes the scanner's measurements and unmixes "
        "them to recover the true points p1, p2 — turning the raw readings back into a "
        "picture of the bone and marrow you can actually look at. That recovery *is* the "
        "reconstructed image on your screen.\n\n"
        "The catch: real readings carry a little error, and when det A is close to zero, A⁻¹ "
        "magnifies that error enormously — so the reconstructed bone comes out badly wrong. "
        "Drag the error slider on each preset to see it."
    )
    preset = st.selectbox("Preset", list(_E3_PRESETS), key="t04e3_preset")
    if st.session_state.get("t04e3_last") != preset:
        w.set_matrix_state("t04e3_A", _E3_PRESETS[preset])
        st.session_state["t04e3_last"] = preset

    ac, _ = st.columns([0.4, 0.6])
    with ac:
        A = w.editable_matrix("t04e3_A", 2, compact=True, label="Scanner matrix A")
    det = float(np.linalg.det(A))
    invertible = abs(det) > 1e-9

    ec, _ = st.columns([0.5, 0.5])
    with ec:
        err = w.scalar_slider("t04e3_err", "Measurement error", 0.0, 0.5, 0.0, 0.01)
    E = np.array([err, 0.0])

    left, right = st.columns([0.5, 0.5], gap="large")

    with right:
        fig = plot.new_figure_2d(rng=10, x_title="x", y_title="y")

        def poly(pts):
            return [pts[:, k] for k in range(pts.shape[1])]

        def recon(pts):
            return np.linalg.inv(A) @ (A @ pts + E[:, None])

        plot.shade_polygon(fig, poly(_OUTER), "rgba(120,144,156,0.15)", "true slice",
                           line_color="rgba(160,170,180,0.7)", line_width=2)
        plot.shade_polygon(fig, poly(_MARROW), "rgba(120,144,156,0.25)",
                           line_color="rgba(160,170,180,0.7)", line_width=1)
        if invertible:
            plot.shade_polygon(fig, poly(recon(_OUTER)), "rgba(32,201,151,0.18)",
                               "reconstructed", line_color="#20c997", line_width=2)
            plot.shade_polygon(fig, poly(recon(_MARROW)), "rgba(32,201,151,0.25)",
                               line_color="#20c997", line_width=1)
        else:
            st.warning("Singular — the scan lost information in one direction. Reconstruction impossible.")
        plot.add_point_2d(fig, _P1, "#ffa94d", "bone edge (p1)")
        plot.add_point_2d(fig, _P2, "#ff6b6b", "marrow edge (p2)")
        st.plotly_chart(fig, use_container_width=True)
        _inv_meter(A)

    with left:
        st.latex(r"A = " + w.bmatrix(A) + rf"\qquad \det A = {det:.4f}")
        st.markdown("**A**: real slice → scanner reading.")
        if invertible:
            Ainv = np.linalg.inv(A)
            st.latex(r"A^{-1} = " + w.bmatrix(Ainv)
                     + rf"\qquad \det A^{{-1}} = \tfrac{{1}}{{\det A}} = {1/det:.4f}")
            st.markdown("**A⁻¹**: scanner reading → recovered image. A⁻¹ doesn't change "
                        "when you add error — the error is in the reading, not the matrix.")
            d1 = A @ _P1
            d2 = A @ _P2
            d1e = d1 + E
            d2e = d2 + E
            r1 = Ainv @ d1e
            r2 = Ainv @ d2e

            def pt(v):
                return f"({v[0]:.2f}, {v[1]:.2f})"

            def col(v):
                return w.bmatrix(v.reshape(-1, 1))

            st.markdown(f"1. The actual bone edge p1 is at **{pt(_P1)}**; the actual "
                        f"marrow edge p2 is at **{pt(_P2)}**.")

            st.markdown("2. The scanner measures each point by multiplying it by A:")
            st.latex(r"{\small A\,p_1 = " + w.bmatrix(A) + col(_P1) + " = " + col(d1) + r"}")
            st.latex(r"{\small A\,p_2 = " + w.bmatrix(A) + col(_P2) + " = " + col(d2) + r"}")

            st.markdown(f"3. If the machine is off by {err:.2f} in the x-direction, the "
                        f"readings become **{pt(d1e)}** and **{pt(d2e)}**.")

            st.markdown("4. A⁻¹ unmixes the readings back into positions:")
            st.latex(r"{\small A^{-1}(A p_1 + \text{err}) = " + w.bmatrix(Ainv) + col(d1e)
                     + " = " + col(r1) + r"}")
            st.latex(r"{\small A^{-1}(A p_2 + \text{err}) = " + w.bmatrix(Ainv) + col(d2e)
                     + " = " + col(r2) + r"}")
            st.markdown(f"— instead of the true {pt(_P1)} and {pt(_P2)}.")

            st.markdown("On Full data these barely move; on Too few angles the same error "
                        "throws them far off.")
            st.markdown(
                "A tiny det makes 1/det and the entries of A⁻¹ large — so every small "
                "measurement error gets amplified by that factor. On \"Full data\" the "
                "reconstruction barely moves; on \"Too few angles\" the same error throws "
                "it far off. That is the instability."
            )
        else:
            st.latex(r"\det A = 0")
            st.markdown(
                "det A = 0 — no inverse. The scan lost information in one direction, so "
                "there is no way to unmix the readings back into the true slice."
            )

    st.info(
        "A CT scanner never sees your insides directly — it measures blended data and "
        "*unmixes* it (applies the inverse) to reconstruct the image. With too little data "
        "the inverse becomes unstable, so small measurement errors explode — which is why "
        "scans need enough angles. (Topic 10 shows the real version: MRI reconstruction is "
        "an inverse Fourier transform.)"
    )
