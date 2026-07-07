"""Screen 2 -- 3D: an origin-centered cube under a matrix A."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from engine import widgets as w
from engine import plotting as plot

GOAL = (
    "**Goal:** watch how a 3D transformation A moves every corner of this "
    "solid -- the columns of A show where the axes land, and the "
    "determinant shows how volume changes."
)

# Origin-centered cube, vertices at (+-2, +-2, +-2).
V1 = np.array([-2.0, -2.0, -2.0])
V2 = np.array([2.0, -2.0, -2.0])
V3 = np.array([2.0, 2.0, -2.0])
V4 = np.array([-2.0, 2.0, -2.0])
V5 = np.array([-2.0, -2.0, 2.0])
V6 = np.array([2.0, -2.0, 2.0])
V7 = np.array([2.0, 2.0, 2.0])
V8 = np.array([-2.0, 2.0, 2.0])
VERTICES = np.column_stack([V1, V2, V3, V4, V5, V6, V7, V8])

# Standard cube face topology: bottom, top, then front/right/back/left, each
# connecting a bottom edge (i, i+1) to the top edge above it (i+4, i+5) in
# consistent winding order. Column indices into VERTICES.
FACES = [
    (0, 1, 2, 3),  # bottom (z=-2): v1 v2 v3 v4
    (4, 5, 6, 7),  # top (z=+2): v5 v6 v7 v8
    (0, 1, 5, 4),  # front (y=-2): v1 v2 v6 v5
    (1, 2, 6, 5),  # right (x=+2): v2 v3 v7 v6
    (2, 3, 7, 6),  # back (y=+2): v3 v4 v8 v7
    (3, 0, 4, 7),  # left (x=-2): v4 v1 v5 v8
]
FACE_COLORS = ["#ff6b6b", "#4dabf7", "#51cf66", "#ffd43b", "#cc5de8", "#20c997"]

# The 12 cube edges (for the "before" wireframe overlay).
EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]

VIEW_3D = 6

PRESET_NAMES_3D = [
    "Identity",
    "Scale ×2",
    "Non-uniform scale",
    "Shear (xy)",
    "Rotation 90° z",
    "Reflection z",
    "Collapse (singular)",
    "Custom",
]

_PRESET_MATRICES_3D = {
    "Identity": np.eye(3),
    "Scale ×2": 2.0 * np.eye(3),
    "Non-uniform scale": np.diag([2.0, 1.0, 0.5]),
    "Shear (xy)": np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "Rotation 90° z": np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
    "Reflection z": np.diag([1.0, 1.0, -1.0]),
    "Collapse (singular)": np.array([[1.0, 2.0, 0.0], [2.0, 4.0, 0.0], [0.0, 0.0, 1.0]]),
}


def _vertex_latex(A: np.ndarray, v: np.ndarray) -> str:
    """Return LaTeX showing the numeric matrix A times vertex v equals result."""
    result = A @ v
    return w.bmatrix(A) + w.bmatrix(v.reshape(-1, 1)) + r" = " + w.bmatrix(result.reshape(-1, 1))


def _add_wireframe(fig, points):
    """Draw the solid's 12 edges as thin bright lines, no face fill -- call last so it draws on top."""
    xs, ys, zs = [], [], []
    for a, b in EDGES:
        xs += [points[0, a], points[0, b], None]
        ys += [points[1, a], points[1, b], None]
        zs += [points[2, a], points[2, b], None]
    fig.add_trace(go.Scatter3d(
        x=xs, y=ys, z=zs, mode="lines",
        line=dict(color="#ffffff", width=4),
        hoverinfo="skip", showlegend=False,
    ))


def _add_solid_faces(fig, points):
    """Draw the solid's 6 quad faces, each a solid distinct color -- the 'after'."""
    for idx, face in enumerate(FACES):
        pts = points[:, face]
        fig.add_trace(go.Mesh3d(
            x=pts[0], y=pts[1], z=pts[2],
            i=[0, 0], j=[1, 2], k=[2, 3],
            color=FACE_COLORS[idx], opacity=1.0,
            hoverinfo="skip", showlegend=False,
        ))


def _render_3d():
    st.markdown(GOAL)
    st.caption(", ".join(
        f"v{i + 1} = ({v[0]:.0f}, {v[1]:.0f}, {v[2]:.0f})"
        for i, v in enumerate(VERTICES.T)
    ))

    if "t02_3d_preset" not in st.session_state:
        st.session_state["t02_3d_preset"] = "Identity"

    # --- control band: Matrix A left, preset buttons right ---
    band_left, band_right = st.columns([0.5, 0.5], gap="large")

    with band_right:
        st.markdown("**Choose a transformation**")
        rows = [PRESET_NAMES_3D[i:i + 3] for i in range(0, len(PRESET_NAMES_3D), 3)]
        for row in rows:
            btn_cols = st.columns(3)
            for btn_col, name in zip(btn_cols, row):
                with btn_col:
                    if st.button(name, key=f"t02_3d_btn_{name}", use_container_width=True):
                        st.session_state["t02_3d_preset"] = name
        preset = st.session_state["t02_3d_preset"]

        if preset == "Custom":
            st.caption("Set the nine entries of A:")
            A = w.editable_matrix("t02_3d_custom_A", 3, compact=True)
        else:
            A = _PRESET_MATRICES_3D[preset]

    with band_left:
        st.latex(r"A = " + w.bmatrix(A))
        st.caption("Columns = where the basis vectors land.")

    # --- two-column row: vertex math/determinant/meaning left, graph right ---
    left, right = st.columns([0.5, 0.5], gap="large")

    with left:
        st.markdown("**Where three of the vertices land**")
        for label, v in (("v1", V1), ("v2", V2), ("v3", V3)):
            st.caption(label)
            st.latex(r"{\small " + _vertex_latex(A, v) + r"}")
        st.caption("The other five vertices transform the same way.")

        det = float(np.linalg.det(A))
        st.markdown(f"**Determinant:** `{det:.3f}`")
        meaning = f"**|det|** = `{abs(det):.3f}` is the volume scale factor."
        if det < 0:
            meaning += " The **negative sign** means orientation flips (a mirror image)."
        if abs(det) < 1e-9:
            meaning += " **det = 0 collapses the solid to a flat plane** -- A has no inverse."
        st.markdown(meaning)

    with right:
        fig = plot.new_figure_3d(rng=VIEW_3D)
        _add_solid_faces(fig, A @ VERTICES)
        _add_wireframe(fig, VERTICES)
        st.plotly_chart(fig, use_container_width=True)
