"""Animation helper.

Dragging a t-slider from 0 to 1 morphs the identity into the target matrix:
    M(t) = I + t * (M - I)
Streamlit reruns on each slider change, so the drag itself produces the
animation -- no timers or threads needed.
"""
import numpy as np


def interpolate(M: np.ndarray, t: float) -> np.ndarray:
    """Linear morph from identity (t=0) to M (t=1)."""
    I = np.eye(M.shape[0])
    return I + t * (M - I)
