"""Example 2 -- Cryptography (Hill cipher, mod 26)."""
import numpy as np
import streamlit as st

from engine import widgets as w

from . import _mod_inv_matrix

_E2_KEYS = {
    "Key 1":                 np.array([[3, 3], [2, 5]]),
    "Key 2":                 np.array([[1, 2], [3, 5]]),
    "Broken key (singular)": np.array([[2, 4], [1, 2]]),
}


def _prep_message(text):
    """Uppercase, A-Z only, split into 2-char blocks, pad odd tail with X."""
    cleaned = "".join(c for c in text.upper() if c.isalpha())
    if not cleaned:
        cleaned = "X"
    if len(cleaned) % 2 == 1:
        cleaned += "X"
    return cleaned


def _example_crypto():
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

    left, right = st.columns([0.5, 0.5], gap="large")

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

    with left:
        st.latex(r"M = " + w.bmatrix(M.astype(float)))
        if len(msg) >= 2:
            p0 = np.array([ord(msg[0]) - 65, ord(msg[1]) - 65])
            c0 = (M @ p0) % 26
            st.latex(
                r"{\small c = M\,p \pmod{26}: \quad"
                + w.bmatrix(M.astype(float))
                + w.bmatrix(p0.reshape(-1, 1).astype(float))
                + r"\equiv " + w.bmatrix(c0.reshape(-1, 1).astype(float))
                + r"\pmod{26}}"
            )
        if invertible_mod:
            st.latex(r"M^{-1}\!\pmod{26} = " + w.bmatrix(Minv_mod.astype(float)))
            if len(msg) >= 2:
                c0r = (M @ np.array([ord(msg[0]) - 65, ord(msg[1]) - 65])) % 26
                d0 = (Minv_mod @ c0r) % 26
                st.latex(
                    r"{\small p = M^{-1}c \pmod{26}: \quad"
                    + w.bmatrix(Minv_mod.astype(float))
                    + w.bmatrix(c0r.reshape(-1, 1).astype(float))
                    + r"\equiv " + w.bmatrix(d0.reshape(-1, 1).astype(float))
                    + r"\pmod{26}}"
                )
        st.caption(
            "The arithmetic is mod 26 because there are 26 letters — the one place the "
            "inverse is \"modular\" rather than the ordinary 1/det."
        )

    st.info(
        "Multiplying by a matrix scrambles a message; multiplying by its inverse "
        "unscrambles it. Not every key works — its determinant must be \"compatible\" with "
        "the 26 letters. If the determinant is 0, the message is destroyed: there's no "
        "inverse, so no way to read it back."
    )
