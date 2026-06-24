"""
Topic 4 -- Inverse Transformations.

Pattern: MULTI-EXAMPLE. A top selector chooses one of four screens.
Two recurring devices used throughout:
  - There-and-back: slider t in [0,1] + radio Apply M / Undo with M-1.
  - Inverse meter: shows M-1 and 1/det, or warns when det = 0.
"""
import numpy as np
import streamlit as st

from engine import animate
from engine import plotting as plot
from engine import widgets as w

TITLE = "4 · Inverse Transformations"
SLUG = "inverse"

OVERVIEW = """
Topic 3 ended on a cliffhanger: det = 0 means a transformation can't be undone.
This topic is the answer. The **inverse** of a transformation is the one that
reverses it — apply M, then apply M⁻¹, and every point lands exactly back where
it started. It exists only when det ≠ 0, and it scales area by 1/det. We'll meet
"undoing" as the central question in four fields: robotics, secret codes,
medical scans, and business planning.
"""

HOWTO = """
The left panel sets the numbers; the right panel shows the shape or the result.
On the visual screens, use **Apply M / Undo with M⁻¹** to watch a shape deform
and then return home. The **inverse meter** shows M⁻¹ and 1/det — or warns you
when there's no inverse.
"""

_E1_PRESETS = {
    "Reachable pose": np.array([[1.5, 0.5], [0.0, 1.0]]),
    "Singular pose":  np.array([[1.0, 1.0], [1.0, 1.0]]),
}

_E2_KEYS = {
    "Key 1":                 np.array([[3, 3], [2, 5]]),
    "Key 2":                 np.array([[1, 2], [3, 5]]),
    "Broken key (singular)": np.array([[2, 4], [1, 2]]),
}

_E3_PRESETS = {
    "Full data":                          np.array([[1.0, 0.5], [0.5, 1.0]]),
    "Too few angles (unstable)":          np.array([[1.0, 1.0], [1.0, 1.05]]),
    "No data in a direction (singular)":  np.array([[1.0, 1.0], [1.0, 1.0]]),
}

_E4_PRESETS = {
    "Two distinct products":            np.array([[2.0, 1.0], [1.0, 3.0]]),
    "Proportional products (singular)": np.array([[2.0, 4.0], [1.0, 2.0]]),
}


# ----------------------------------------------------------------------------
# Shared helpers
# ----------------------------------------------------------------------------

def _mod_inv_matrix(M_int, mod=26):
    """Modular inverse of a 2x2 integer matrix mod `mod`; returns None if it doesn't exist."""
    a, b, c, d = int(M_int[0, 0]), int(M_int[0, 1]), int(M_int[1, 0]), int(M_int[1, 1])
    det_int = a * d - b * c
    det_mod = det_int % mod
    try:
        det_inv = pow(det_mod, -1, mod)
    except ValueError:
        return None
    adj = np.array([[d, -b], [-c, a]])
    return (det_inv * adj) % mod


def _inv_meter(M):
    det = float(np.linalg.det(M))
    st.metric("Determinant", f"{det:.4f}")
    if abs(det) > 1e-9:
        Minv = np.linalg.inv(M)
        st.latex(r"M^{-1} = " + w.bmatrix(Minv))
        st.markdown(f"invertible — area scales by 1/det = {1/det:.3f}")
    else:
        st.warning("det = 0 — no inverse. This transform can't be undone.")


# _inv_meter and preset dicts are defined above; submodules import them via
# `from . import _inv_meter, _E1_PRESETS` etc.
from .robotics import _example_robotics
from .medical import _example_medical


# ----------------------------------------------------------------------------
# Example 2 -- Cryptography (Hill cipher, mod 26)
# ----------------------------------------------------------------------------

def _prep_message(text):
    """Uppercase, A-Z only, split into 2-char blocks, pad odd tail with X."""
    cleaned = "".join(c for c in text.upper() if c.isalpha())
    if not cleaned:
        cleaned = "X"
    if len(cleaned) % 2 == 1:
        cleaned += "X"
    return cleaned


def _example_crypto():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Cryptography.** A matrix scrambles a message; its inverse unscrambles it. "
            "This is a Hill cipher on 2-letter blocks (A=0 … Z=25, arithmetic mod 26)."
        )
        msg_raw = st.text_input("Message (A–Z)", value="MATH", key="t04e2_msg")
        key_name = st.selectbox("Cipher key", list(_E2_KEYS), key="t04e2_key")

    M = _E2_KEYS[key_name]
    det_int = int(M[0, 0]) * int(M[1, 1]) - int(M[0, 1]) * int(M[1, 0])
    Minv_mod = _mod_inv_matrix(M)
    invertible_mod = Minv_mod is not None

    msg = _prep_message(msg_raw)
    rows = []
    cipher_letters = []
    decoded_letters = []
    for i in range(0, len(msg), 2):
        p = np.array([ord(msg[i]) - 65, ord(msg[i + 1]) - 65])
        c = (M @ p) % 26
        if invertible_mod:
            d = (Minv_mod @ c) % 26
        else:
            d = np.array([-1, -1])
        for k in range(2):
            pl = msg[i + k]
            pn = int(p[k])
            cn = int(c[k])
            cl = chr(cn + 65)
            dl = chr(int(d[k]) + 65) if invertible_mod else "?"
            rows.append({
                "Plaintext": pl,
                "#": pn,
                "Cipher #": cn,
                "Ciphertext": cl,
                "Decoded": dl,
            })
            cipher_letters.append(cl)
            decoded_letters.append(dl)

    ciphertext = "".join(cipher_letters)
    decoded = "".join(decoded_letters) if invertible_mod else "— unrecoverable —"

    with right:
        st.markdown(f"**Plaintext:** `{msg}`  \n**Ciphertext:** `{ciphertext}`  \n"
                    f"**Decoded:** `{decoded}`")
        st.table(rows)

        st.markdown("**Inverse meter**")
        st.metric("det M (integer)", str(det_int))
        if invertible_mod:
            st.latex(r"M^{-1}\!\pmod{26} = " + w.bmatrix(Minv_mod.astype(float)))
            st.markdown(f"invertible mod 26 — decryption matrix shown above")
        else:
            st.warning(
                "this key can't be undone — its determinant shares a factor with 26 "
                "(or is 0), so the message is unrecoverable."
            )

    st.info(
        "Multiplying by a matrix scrambles a message; multiplying by its inverse "
        "unscrambles it. Not every key works — its determinant must be \"compatible\" with "
        "the 26 letters. If the determinant is 0, the message is destroyed: there's no "
        "inverse, so no way to read it back."
    )

    with st.expander("Show the math"):
        st.latex(r"M = " + w.bmatrix(M.astype(float)))
        if len(msg) >= 2:
            p0 = np.array([ord(msg[0]) - 65, ord(msg[1]) - 65])
            c0 = (M @ p0) % 26
            st.latex(
                r"c = M\,p \pmod{26}: \quad"
                + w.bmatrix(M.astype(float))
                + w.bmatrix(p0.reshape(-1, 1).astype(float))
                + r"\equiv " + w.bmatrix(c0.reshape(-1, 1).astype(float))
                + r"\pmod{26}"
            )
        if invertible_mod:
            st.latex(r"M^{-1}\!\pmod{26} = " + w.bmatrix(Minv_mod.astype(float)))
            if len(msg) >= 2:
                c0r = (M @ np.array([ord(msg[0]) - 65, ord(msg[1]) - 65])) % 26
                d0 = (Minv_mod @ c0r) % 26
                st.latex(
                    r"p = M^{-1}c \pmod{26}: \quad"
                    + w.bmatrix(Minv_mod.astype(float))
                    + w.bmatrix(c0r.reshape(-1, 1).astype(float))
                    + r"\equiv " + w.bmatrix(d0.reshape(-1, 1).astype(float))
                    + r"\pmod{26}"
                )
        st.caption(
            "The arithmetic is mod 26 because there are 26 letters — the one place the "
            "inverse is \"modular\" rather than the ordinary 1/det."
        )


# ----------------------------------------------------------------------------
# Example 4 -- Business / economics
# ----------------------------------------------------------------------------

def _example_business():
    left, right = st.columns([1.05, 1.35], gap="large")
    with left:
        st.markdown(
            "**Business.** Matrix A maps production → resources used. "
            "The inverse answers: \"I have these resources — how much of each product "
            "can I make?\""
        )
        preset = st.selectbox("Preset", list(_E4_PRESETS), key="t04e4_preset")
        if st.session_state.get("t04e4_last") != preset:
            w.set_matrix_state("t04e4_A", _E4_PRESETS[preset])
            st.session_state["t04e4_last"] = preset

        A = w.matrix_editor("t04e4_A", 2,
                            label="Resource-usage matrix A (column j = resources for product j)")
        x = w.vector_editor("t04e4_x", 2, (4.0, 2.0), label="Production x (units of each product)")

    det = float(np.linalg.det(A))
    invertible = abs(det) > 1e-9
    r = A @ x

    with right:
        fig = plot.new_figure_2d(rng=14, x_title="resource 1", y_title="resource 2")
        plot.add_vector_2d(fig, [0, 0], r, "seagreen", f"resources r = ({r[0]:.1f}, {r[1]:.1f})")
        plot.add_point_2d(fig, r, "seagreen", "r = Ax", size=14)
        if invertible:
            x_back = np.linalg.inv(A) @ r
            plot.add_point_2d(fig, x_back, "crimson", "A⁻¹r (round-trip)", size=10, symbol="x")
        st.plotly_chart(fig, use_container_width=True)

    # ---- The algebra block (shown openly, not in expander) ----
    st.markdown("#### The algebra, step by step")

    a11, a12 = float(A[0, 0]), float(A[0, 1])
    a21, a22 = float(A[1, 0]), float(A[1, 1])
    x1, x2   = float(x[0]), float(x[1])
    r1, r2   = float(r[0]), float(r[1])

    # Step 1 — forward, general
    st.markdown("**1. Forward map (general)**")
    st.latex(
        r"r = Ax = "
        r"\begin{bmatrix}a_{11}&a_{12}\\a_{21}&a_{22}\end{bmatrix}"
        r"\begin{bmatrix}x_1\\x_2\end{bmatrix}"
        r"= \begin{bmatrix}a_{11}x_1+a_{12}x_2\\a_{21}x_1+a_{22}x_2\end{bmatrix}"
    )

    # Step 2 — forward, live numbers
    st.markdown("**2. Forward map (your numbers)**")
    st.latex(
        r"r = " + w.bmatrix(A)
        + w.bmatrix(x.reshape(-1, 1))
        + " = " + w.bmatrix(r.reshape(-1, 1))
    )

    # Step 3 — inverse formula, emphasise det in denominator
    st.markdown("**3. Inverse formula** — det in the denominator is the key")
    if invertible:
        st.latex(
            r"A^{-1} = \frac{1}{\det A}"
            r"\begin{bmatrix}a_{22}&-a_{12}\\-a_{21}&a_{11}\end{bmatrix}"
            + r"\qquad \det A = a_{11}a_{22} - a_{12}a_{21} = " + f"{det:.4f}"
        )
    else:
        st.latex(
            r"A^{-1} = \frac{1}{\det A}"
            r"\begin{bmatrix}a_{22}&-a_{12}\\-a_{21}&a_{11}\end{bmatrix}"
            r"\quad \det A = " + f"{det:.4f}"
            r"\implies \frac{1}{\det A} = \frac{1}{0} \text{ — undefined}"
        )
        st.caption(
            "These two products use resources in the same proportion, so from the "
            "resources alone you can't tell how much of each you made. There's no way "
            "to work backwards — the inverse doesn't exist."
        )

    if invertible:
        Ainv = np.linalg.inv(A)
        x_back = Ainv @ r

        # Step 4 — inverse, live numbers
        st.markdown("**4. Inverse (your numbers)**")
        st.latex(r"A^{-1} = " + w.bmatrix(Ainv))

        # Step 5 — recover and verify
        st.markdown("**5. Recover production from resources**")
        st.latex(
            r"x = A^{-1}r = "
            + w.bmatrix(Ainv)
            + w.bmatrix(r.reshape(-1, 1))
            + " = " + w.bmatrix(x_back.reshape(-1, 1))
        )
        st.success(f"Round trip returns x = ({x_back[0]:.3f}, {x_back[1]:.3f}) ✓")

    # ---- Optional target solver ----
    with st.expander("Solve for a resource target"):
        rt = w.vector_editor("t04e4_rt", 2, (8.0, 6.0), label="Resource target r")
        if invertible:
            xt = Ainv @ rt
            st.latex(r"x = A^{-1}r = " + w.bmatrix(xt.reshape(-1, 1)))
            if any(xt < 0):
                st.info(
                    "The algebra returns a negative number of products — mathematically "
                    "valid, physically impossible. The model is more permissive than a "
                    "real factory."
                )
        else:
            st.warning("No inverse — can't solve for a resource target.")

    # ---- Inverse meter ----
    st.markdown("**Inverse meter**")
    _inv_meter(A)

    st.info(
        "Run the matrix forward and it tells you resources used; run it backward (the "
        "inverse) and it tells you how much to produce to use exactly what you have. This "
        "\"solve A x = r for x\" is the exact question of the next topic — linear systems."
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
        ["1 · Robotics", "2 · Cryptography", "3 · Medical imaging", "4 · Business"],
        horizontal=True,
        key="t04_example",
    )
    st.divider()

    if example.startswith("1"):
        _example_robotics()
    elif example.startswith("2"):
        _example_crypto()
    elif example.startswith("3"):
        _example_medical()
    else:
        _example_business()
