"""Example 3 -- Biology (surface-area-to-volume law)."""
import numpy as np
import streamlit as st

from engine import plotting as plot
from engine import widgets as w


def _example_biology():
    from . import _det_meter

    st.markdown(
        "**Biology.** A cell is roughly a cube. Scaling every side by k "
        "gives a diagonal matrix A whose determinant — the volume factor — "
        "grows much faster than its surface area."
    )

    left, right = st.columns([0.42, 0.58], gap="large")

    with left:
        k = w.scalar_slider(
            "t03e3_k", "Scale factor k (how many times bigger)", 0.5, 3.0, 1.5, 0.1
        )

    A = k * np.eye(3)
    volume = k ** 3
    surface = 6 * k ** 2
    ratio = 6 / k

    with left:
        _det_meter(volume, kind="volume", extra={"surface": surface, "ratio": ratio})

        st.markdown(
            f"This matrix **scales the whole cell uniformly by k**:"
        )
        st.latex(r"A = " + w.bmatrix(A))
        st.markdown(
            "The determinant of any **triangular** matrix — including this **diagonal** "
            "one — is just the diagonal entries multiplied together. "
            "(A diagonal matrix is a special case of triangular; this becomes important "
            'in Topic 5.5, where "determinant = product of the diagonal" gets used in earnest.)'
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
            f"For every 1 unit of volume there are 6/k = 6/{k:.4g} = **{ratio:.2f}** units of surface "
            f"— and that number *falls* as the cell grows (k = 1 → 6 units of surface per volume; "
            f"k = 3 → 2), so the surface can't keep up with the volume it has to serve."
        )

        st.markdown("**A · (cube corners):**")
        for label, x in [
            ("(1,0,0)", np.array([1., 0., 0.])),
            ("(0,1,0)", np.array([0., 1., 0.])),
            ("(1,1,1)", np.array([1., 1., 1.])),
        ]:
            xp = A @ x
            st.latex(
                r"A \cdot \begin{pmatrix}"
                + f"{x[0]:.0f}" + r" \\ " + f"{x[1]:.0f}" + r" \\ " + f"{x[2]:.0f}"
                + r"\end{pmatrix} = \begin{pmatrix}"
                + f"{xp[0]:.2f}" + r" \\ " + f"{xp[1]:.2f}" + r" \\ " + f"{xp[2]:.2f}"
                + r"\end{pmatrix}"
                + r"\quad \text{" + label + r"}"
            )

    with right:
        st.plotly_chart(plot.figure_3d(A), use_container_width=True)

    st.info(
        "**k is the scale factor** — how many times bigger you make the cell. This matrix "
        "**scales the whole cell uniformly by k**: every direction grows by the same "
        f"factor k (k = 2 means twice as wide, twice as tall, twice as deep).\n\n"
        "A cell absorbs food and oxygen through its **surface**, but it has to feed its "
        "whole **volume**. When you make something bigger, the volume (k³) outgrows the "
        "surface (k²), so the surface can't keep up with the demand — which is why cells "
        "stay tiny, and why large animals can't just be \"scaled-up\" cells: they need extra "
        "surface area folded in (lungs, gills, intestines). It's also why an **elephant "
        "has enormous ears**: a big warm body makes heat throughout its volume but can "
        "only shed it through its surface, so the elephant grows extra surface — those "
        "huge, blood-rich ears — to dump the heat its size can't otherwise lose."
    )
