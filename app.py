"""
Linear Algebra — interactive lessons.

Run from a terminal (or a PyCharm Run Configuration, see README):
    streamlit run app.py

The sidebar is the instructor's topic navigator. Each topic is a small module
in topics/ that exposes TITLE, SLUG, and render(). Add a topic by importing it
and appending it to TOPICS below — nothing else changes.
"""
import streamlit as st

from topics import t01_vectors, t02_transformations, t03_determinant, t04_inverse

st.set_page_config(page_title="Linear Algebra", layout="wide")

# Registry. The learnable order; uncomment modules as you build them.
TOPICS = [
    (t01_vectors.TITLE, t01_vectors),
    (t02_transformations.TITLE, t02_transformations),
    (t03_determinant.TITLE, t03_determinant),
    (t04_inverse.TITLE, t04_inverse),
    # ("5 · Linear Systems (Ax = b)", t05_systems),
    # ("6 · Subspaces, Basis, Dimension", t06_subspaces),
    # ("7 · Projection & Least Squares", t07_least_squares),
    # ("8 · Eigenvalues & Eigenvectors", t08_eigen),
    # ("9 · Complex Numbers in LA", t09_complex),
    # ("10 · Fourier Matrices (DFT)", t10_fourier),
    # ("11 · Linear Algebra in AI/ML", t11_ml),
]

st.sidebar.title("Linear Algebra")
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
