# Linear Algebra, Seen

Interactive lessons that show linear algebra: the **numbers on the left**, the
**effect on the right**. Built with Streamlit + NumPy + Plotly so the student
can edit values in a UI *and* open the same `.py` and read the math.

## Setup (do this once, before the first lesson)

1. Clone the repo and open the folder in PyCharm.
2. Create a virtual environment (PyCharm: *Settings → Project → Python Interpreter → Add → Virtualenv*).
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running it

Streamlit launches from a terminal, not PyCharm's green Run button. Two ways:

- **Terminal** (PyCharm's built-in terminal works): `streamlit run app.py`
- **Run Configuration** (so the green button works): *Run → Edit Configurations → +
  → Python*. Set **module name** (not script) to `streamlit`, **parameters** to
  `run app.py`, working directory to the project root.

It opens in the browser. Save any `.py` and the page offers to re-run — great for
editing live during a session.

## How it's organized

```
app.py                     sidebar topic navigator + registry
engine/
  widgets.py               matrix/vector/scalar editors + LaTeX helper (shared)
  plotting.py              2D & 3D Plotly figures (shared)
  animate.py               identity → matrix morph
topics/
  t02_transformations.py   one module per topic (the template)
```

## Adding a topic (the contract)

Copy a topic module, then change four things:

1. `TITLE` and `SLUG`
2. the intro / overview text
3. the **presets** or **examples** (your 2–3 examples per topic)
4. the body of `render()` — which inputs to show and what to draw

Then import it in `app.py` and add it to the `TOPICS` list. Reuse
`engine.widgets` and `engine.plotting` so every topic looks and behaves the same.

There are two templates depending on the topic:

- `topics/t02_transformations.py` — **one visual, presets swap the numbers.**
- `topics/t01_vectors.py` — **several distinct examples** chosen by a selector at
  the top; only the selected example's text, inputs, and visual show. The
  Overview is pinned and "How to use" sits in a collapsed expander.

## Learnable order

1. Vectors & combinations **(built)** → 2. **Linear transformations (built)** →
3. Determinant → 4. Inverse → 5. Linear systems (Ax=b) →
6. Subspaces, basis, dimension → 7. Projection & least squares →
8. Eigenvalues & eigenvectors → 9. Complex numbers → 10. Fourier (DFT) →
11. AI/ML (PCA & image/SVD).
