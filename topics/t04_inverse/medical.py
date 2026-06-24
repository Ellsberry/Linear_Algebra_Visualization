"""Example 3 -- Medical imaging (inverse reconstruction)."""
import numpy as np
import streamlit as st

from engine import animate
from engine import plotting as plot
from engine import widgets as w

from . import _inv_meter, _E3_PRESETS


def _example_medical():
    st.markdown(
        "**Medical imaging.** A scanner measures a transformed version of the body; "
        "reconstructing the true image means applying the inverse. If det is close to "
        "zero, the inverse is huge and unstable — small errors blow up."
    )
    preset = st.selectbox("Preset", list(_E3_PRESETS), key="t04e3_preset")
    if st.session_state.get("t04e3_last") != preset:
        w.set_matrix_state("t04e3_M", _E3_PRESETS[preset])
        st.session_state["t04e3_last"] = preset

    M = w.editable_matrix("t04e3_M", 2, label="Measurement M")
    det = float(np.linalg.det(M))
    invertible = abs(det) > 1e-9

    if invertible:
        direction = st.radio("Direction", ["Apply M", "Undo with M⁻¹"],
                             horizontal=True, key="t04e3_dir")
    else:
        st.warning("Singular — information lost in this direction. Reconstruction impossible.")
        direction = "Apply M"

    t = w.scalar_slider("t04e3_t", "Morph", 0.0, 1.0, 1.0, 0.01)

    if invertible and direction == "Undo with M⁻¹":
        T = ((1 - t) * np.eye(2) + t * np.linalg.inv(M)) @ M
    else:
        T = animate.interpolate(M, t)

    left, right = st.columns([0.5, 0.5], gap="large")

    with right:
        st.plotly_chart(plot.figure_2d(T, obj="rocket"), use_container_width=True)
        _inv_meter(M)

    with left:
        st.latex(r"M = " + w.bmatrix(M) + rf"\qquad \det M = {det:.4f}")
        if invertible:
            Minv = np.linalg.inv(M)
            st.latex(r"{\small M^{-1} = " + w.bmatrix(Minv)
                     + rf"\qquad \tfrac{{1}}{{\det M}} = {1/det:.3f}" + r"}")
            st.markdown(
                "A tiny det makes 1/det and M⁻¹ large — every small measurement error "
                "gets amplified by that factor. That is the instability."
            )
        else:
            st.latex(r"\det M = 0 \implies \text{no inverse — reconstruction impossible}")

    st.info(
        "A CT scanner never sees your insides directly — it measures transformed data "
        "and *inverts* the transformation to reconstruct the image. With too little data "
        "the inverse becomes unstable, so small measurement errors explode — which is why "
        "scans need enough angles. (Topic 10 shows the real version: MRI reconstruction "
        "is an inverse Fourier transform.)"
    )
