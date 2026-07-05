"""
Linear Algebra — interactive lessons.

Run from a terminal (or a PyCharm Run Configuration, see README):
    streamlit run app.py

The sidebar is the instructor's topic navigator. Each topic is a small module
in topics/ that exposes TITLE, SLUG, and render(). Add a topic by importing it
and appending it to TOPICS below — nothing else changes.
"""
import streamlit as st

from topics import t00_matmul, t01_vectors, t02_transformations, t03_determinant, t04_inverse, t05_systems, t05b_elimination

st.set_page_config(page_title="Linear Algebra", layout="wide")

# Registry. The learnable order; uncomment modules as you build them.
TOPICS = [
    (t00_matmul.TITLE, t00_matmul),
    (t01_vectors.TITLE, t01_vectors),
    (t02_transformations.TITLE, t02_transformations),
    (t03_determinant.TITLE, t03_determinant),
    (t04_inverse.TITLE, t04_inverse),
    (t05_systems.TITLE, t05_systems),
    (t05b_elimination.TITLE, t05b_elimination),
]

labels = [label for label, _ in TOPICS]
if "topic_selector" not in st.session_state:
    st.session_state["topic_selector"] = labels[0]

NCOLS = 3
for start in range(0, len(labels), NCOLS):
    cols = st.columns(NCOLS)
    for col, label in zip(cols, labels[start:start + NCOLS]):
        is_active = (label == st.session_state["topic_selector"])
        if col.button(
            label,
            key=f"topicbtn_{label}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            st.session_state["topic_selector"] = label
            st.rerun()

module = dict(TOPICS)[st.session_state["topic_selector"]]
st.header(module.TITLE)
module.render()
