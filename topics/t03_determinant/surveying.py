"""Example 1 -- Surveying (engineering)."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w


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

        from . import _det_meter
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
