"""Example 1 -- Robotics (inverse kinematics)."""
import numpy as np
import streamlit as st

from engine import animate
from engine import plotting as plot
from engine import widgets as w

from . import _inv_meter, _E1_PRESETS


def _example_robotics():
    st.markdown(
        "**Robotics.** Matrix A maps a control input to an end-effector position. "
        "The inverse recovers the input needed for a desired output. "
        "Use the slider to deform, then undo."
    )
    preset = st.selectbox("Preset", list(_E1_PRESETS), key="t04e1_preset")
    if st.session_state.get("t04e1_last") != preset:
        w.set_matrix_state("t04e1_A", _E1_PRESETS[preset])
        st.session_state["t04e1_last"] = preset

    A = w.editable_matrix("t04e1_A", 2, label="Arm map A (control → hand position)")
    det = float(np.linalg.det(A))
    invertible = abs(det) > 1e-9

    if invertible:
        direction = st.radio("Direction", ["Apply M", "Undo with M⁻¹"],
                             horizontal=True, key="t04e1_dir")
    else:
        st.warning("Singular pose — the arm has lost a degree of freedom. "
                   "Undo is not available.")
        direction = "Apply M"

    t = w.scalar_slider("t04e1_t", "Morph", 0.0, 1.0, 1.0, 0.01)
    target = w.vector_editor("t04e1_target", 2, (3.0, 2.0),
                             label="Desired hand position")

    if invertible and direction == "Undo with M⁻¹":
        T = ((1 - t) * np.eye(2) + t * np.linalg.inv(A)) @ A
    else:
        T = animate.interpolate(A, t)

    left, right = st.columns([0.5, 0.5], gap="large")

    with right:
        st.plotly_chart(plot.figure_2d(T, obj="square"), use_container_width=True)
        _inv_meter(A)
        if invertible:
            x_req = np.linalg.inv(A) @ target
            check = A @ x_req
            st.markdown(
                f"Required input: **({x_req[0]:.3f}, {x_req[1]:.3f})**  \n"
                f"Verify A·x = ({check[0]:.3f}, {check[1]:.3f}) "
                f"≈ target ({target[0]:.2f}, {target[1]:.2f})"
            )

    with left:
        st.latex(r"A = " + w.bmatrix(A) + rf"\qquad \det A = {det:.4f}")
        if invertible:
            Ainv = np.linalg.inv(A)
            x_req = Ainv @ target
            st.latex(r"{\small A^{-1} = " + w.bmatrix(Ainv)
                     + rf"\qquad \tfrac{{1}}{{\det A}} = {1/det:.3f}" + r"}")
            st.latex(r"{\small x = A^{-1}\,b = " + w.bmatrix(Ainv)
                     + w.bmatrix(target.reshape(-1, 1))
                     + " = " + w.bmatrix(x_req.reshape(-1, 1)) + r"}")
            check = A @ x_req
            st.latex(r"{\small A\,x = " + w.bmatrix(A)
                     + w.bmatrix(x_req.reshape(-1, 1))
                     + " = " + w.bmatrix(check.reshape(-1, 1)) + r"}")
        else:
            st.latex(r"\det A = 0 \implies \text{no inverse}")

    st.info(
        "Every robot arm and animated character solves an inverse problem: given where "
        "the hand should go, work backwards to the settings that put it there. When the "
        "inverse doesn't exist, the arm physically can't reach that way — it's stuck in a "
        "\"singular\" pose. (Real arms bend at angles, so this is the linear heart of the "
        "idea, not the full mechanics.)"
    )
