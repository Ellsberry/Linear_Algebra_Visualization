"""Example 1 -- Robotics (inverse kinematics)."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w

from . import _inv_meter, _E1_PRESETS


def _example_robotics():
    st.markdown(
        "**Robotics.** The hand is moved by two actuators. The two columns of "
        "the arm map A are the directions those actuators push, and the "
        "controls (x1, x2) say how hard each one pushes — so the hand reaches "
        "b = x1·(column 1) + x2·(column 2). The hand can reach anything "
        "spanned by the two actuator vectors, but nothing outside them."
    )
    st.markdown(
        "You want the hand at b. Working backward through the arm map with "
        "A⁻¹ tells you the controls x that get it there. Then check: pushing "
        "those controls (A·x) does land at b."
    )

    preset = st.selectbox("Preset", list(_E1_PRESETS), key="t04e1_preset")
    if st.session_state.get("t04e1_last") != preset:
        w.set_matrix_state("t04e1_A", _E1_PRESETS[preset])
        st.session_state["t04e1_last"] = preset

    ac, _ = st.columns([0.4, 0.6])
    with ac:
        A = w.editable_matrix("t04e1_A", 2, compact=True,
                              label="Arm map A (columns = the two actuator directions)")

    bc, _ = st.columns([0.4, 0.6])
    with bc:
        b = w.vector_editor("t04e1_target", 2, (4.0, 2.0),
                            label="Desired hand position (x, y)")

    det = float(np.linalg.det(A))
    invertible = abs(det) > 1e-9

    left, right = st.columns([0.5, 0.5], gap="large")

    with right:
        fig = plot.new_figure_2d(rng=8, x_title="hand x", y_title="hand y")
        col1 = A[:, 0]
        col2 = A[:, 1]
        plot.add_vector_2d(fig, (0, 0), col1, "#ff6b6b", "actuator 1 (column 1)")
        plot.add_vector_2d(fig, (0, 0), col2, "#4dabf7", "actuator 2 (column 2)")
        plot.add_point_2d(fig, b, "#ffa94d", "destination b")

        if invertible:
            x = np.linalg.inv(A) @ b
            c1 = x[0] * col1
            plot.add_vector_2d(fig, (0, 0), c1, "#20c997", "x1 · (column 1)")
            plot.add_vector_2d(fig, c1, c1 + x[1] * col2, "#20c997", "x2 · (column 2)")
        else:
            d = col1 if np.linalg.norm(col1) > 1e-9 else col2
            d = d / np.linalg.norm(d)
            far = 12.0
            plot.add_vector_2d(fig, (-far * d[0], -far * d[1]),
                               (far * d[0], far * d[1]),
                               "#868e96", "everything the arm can reach", arrow=False)
            on_line = abs(d[0] * b[1] - d[1] * b[0]) < 1e-6
            if not on_line:
                plot.add_point_2d(fig, b, "#ff6b6b", "unreachable — off the line")

        st.plotly_chart(fig, use_container_width=True)
        _inv_meter(A)

    with left:
        st.latex(r"A = " + w.bmatrix(A) + rf"\qquad \det A = {det:.4f}")
        if invertible:
            Ainv = np.linalg.inv(A)
            x = Ainv @ b
            st.latex(r"A^{-1} = " + w.bmatrix(Ainv)
                     + rf"\qquad \det A^{{-1}} = \tfrac{{1}}{{\det A}} = {1/det:.4f}")
            st.markdown("**Solve (working backward):** find the controls that reach b.")
            st.latex(r"{\small x = A^{-1}b = " + w.bmatrix(Ainv)
                     + w.bmatrix(b.reshape(-1, 1))
                     + " = " + w.bmatrix(x.reshape(-1, 1)) + r"}")
            st.markdown("**Check (forward):** pushing those controls lands on b.")
            check = A @ x
            st.latex(r"{\small A\,x = " + w.bmatrix(A)
                     + w.bmatrix(x.reshape(-1, 1))
                     + " = " + w.bmatrix(check.reshape(-1, 1)) + r"}")
        else:
            st.latex(r"\det A = 0 \implies \text{no inverse}")
            st.markdown(
                "This arm map is singular: column 2 is the same as column 1, so both "
                "actuators push the same way and det A = 0. A matrix with determinant 0 "
                "has no inverse — you can't work backward from a hand position to the "
                "controls. With both columns pointing the same direction, the hand is "
                "stuck on that single line and can't reach anywhere off it."
            )

    st.info(
        "Every robot arm and animated character solves an inverse problem: given where "
        "the hand should go, work backwards to the settings that put it there. When the "
        "inverse doesn't exist, the arm physically can't reach that way — it's stuck in a "
        "\"singular\" pose, able to reach only along a single line. (Real arms bend at "
        "angles, so this is the linear heart of the idea, not the full mechanics.)"
    )
