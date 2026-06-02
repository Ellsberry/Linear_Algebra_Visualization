# CLAUDE.md

Guidance for Claude Code (and any AI assistant) working in this repo.

## What this is

An interactive linear-algebra teaching tool for a motivated 14-year-old.
Streamlit + NumPy + Plotly. The principle: **numbers on the left panel, the
visual effect on the right.** The student edits values in the UI *and* is
expected to read the source, so code clarity is a feature, not just a nicety.

## Run

```
pip install -r requirements.txt
streamlit run app.py
```
Streamlit does not launch from PyCharm's green Run button by default; use the
terminal, or a Run Configuration with module `streamlit`, parameters `run app.py`.

## Architecture (do not break this shape)

- `app.py` — sidebar topic navigator + the `TOPICS` registry. Adding a topic
  means importing it and appending to that list. Nothing else in app.py changes.
- `engine/widgets.py` — shared input widgets (`matrix_editor`, `vector_editor`,
  `scalar_slider`, `set_matrix_state`, `bmatrix`). All Streamlit state handling
  for presets/Reset lives here. **Reuse these; do not hand-roll inputs per topic.**
- `engine/plotting.py` — shared Plotly figures (`figure_2d`, `figure_3d`). These
  draw whatever matrix they're given; callers pass the already-morphed matrix.
- `engine/animate.py` — `interpolate(M, t)` morphs identity → M.
- `topics/tNN_*.py` — one module per topic. **`topics/t02_transformations.py` is
  the canonical template.**

## The topic contract

Each topic module exposes `TITLE: str`, `SLUG: str`, and `render() -> None`.
To add one: copy `t02_transformations.py` and change (1) TITLE/SLUG, (2) INTRO,
(3) the presets + their "notice" lines (these are the 2–3 examples per topic),
(4) the body of `render()`. Then register it in `app.py`.

## Conventions

- Keep topic modules small (~100 lines). Push anything reusable into `engine/`.
- Every topic should offer: a short INTRO, named presets each with a one-line
  "what to notice", editable inputs, a "Show the math" expander (use `st.latex`
  + `widgets.bmatrix`), and a Reset. Add a "Try this" expander when it helps.
- Presets apply only when the (preset, dim) selection *changes*, so manual edits
  persist. Use `on_click` callbacks for Reset (see `_reset` in the template).
- No browser localStorage/sessionStorage. State lives in `st.session_state`.
- Tone is for a 14-year-old with strong spatial intuition: plain language,
  geometry first, formulas second. Prefer showing the deformed grid / shapes.

## Learnable order (build in this sequence; each depends on the prior)

1 Vectors & combinations · **2 Linear transformations (built)** · 3 Determinant ·
4 Inverse · 5 Linear systems (Ax=b) · 6 Subspaces/basis/dimension ·
7 Projection & least squares · 8 Eigenvalues & eigenvectors · 9 Complex numbers ·
10 Fourier (DFT) · 11 AI/ML (PCA & image/SVD).

Note: Topic 2 already wires the determinant examples (Scale → det 2,
Reflection → det −1, Collapse → det 0) as presets, so Topic 3 reuses them.

## Don't

- Don't introduce a web framework, build step, or Unity. Streamlit is the tool.
- Don't add heavyweight deps without updating `requirements.txt` and a reason.
- Don't turn the visuals into black boxes — the "Show the math" path must always
  expose the actual numbers behind the picture.
