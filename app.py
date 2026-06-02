"""
Linear Algebra, Seen — interactive lessons.

Run from a terminal (or a PyCharm Run Configuration, see README):
    streamlit run app.py

The sidebar is the instructor's topic navigator. Each topic is a small module
in topics/ that exposes TITLE, SLUG, and render(). Add a topic by importing it
and appending it to TOPICS below — nothing else changes.
"""
import streamlit as st

from topics import t02_transformations

st.set_page_config(page_title="Linear Algebra, Seen", layout="wide")

# Registry. The learnable order; uncomment modules as you build them.
TOPICS = [
    # ("1 · Vectors & Combinations", t01_vectors),
    (t02_transformations.TITLE, t02_transformations),
    # ("3 · Determinant", t03_determinant),
    # ("4 · Inverse Transformations", t04_inverse),
    # ("5 · Linear Systems (Ax = b)", t05_systems),
    # ("6 · Subspaces, Basis, Dimension", t06_subspaces),
    # ("7 · Projection & Least Squares", t07_least_squares),
    # ("8 · Eigenvalues & Eigenvectors", t08_eigen),
    # ("9 · Complex Numbers in LA", t09_complex),
    # ("10 · Fourier Matrices (DFT)", t10_fourier),
    # ("11 · Linear Algebra in AI/ML", t11_ml),
]

st.sidebar.title("Linear Algebra, Seen")
st.sidebar.caption("Left: the numbers.  Right: the effect.")
labels = [label for label, _ in TOPICS]
choice = st.sidebar.radio("Topic", labels, index=0)

st.sidebar.divider()
st.sidebar.markdown(
    "**How to use**\n\n"
    "Pick an *Example* or edit the cells. Slide *Morph* to animate. "
    "Open *Show the math* to see the numbers behind the picture."
)

module = dict(TOPICS)[choice]
st.header(module.TITLE)
module.render()
