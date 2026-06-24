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

## Running the app

1. Do **NOT** start, run, or restart the Streamlit server — the user runs it
   themselves.
2. Only edit files; when a change needs testing, tell the user it's ready and
   let them reload.
3. Never run `streamlit run`.

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
To add one: copy a template and change (1) TITLE/SLUG, (2) intro text, (3) the
presets / examples, (4) the body of `render()`. Then register it in `app.py`.

## Topics are built from approved specs (read this before building a topic)

The pedagogy — which examples, which fields, the exact student-facing text, the
preset values — is decided **before** any code, in a design conversation, and
written into a spec file in `specs/` (e.g. `specs/topic3_determinant.md`). When
asked to build or change a topic:

- **Build from the spec.** Treat the spec as the source of truth. Implement the
  examples, presets, numbers, and wording exactly as written.
- **Do not invent examples or rewrite the lesson text.** The examples are chosen
  so each field genuinely fits the math (e.g. the determinant topic uses
  surveying/medical/biology/graphics because those are honestly about
  area/volume/orientation). Don't add, drop, swap, or reword examples, captions,
  or notices to taste — the text is final copy.
- **If no spec exists** for the topic you're asked to build, say so and ask for
  one (or for the relevant text) rather than improvising the pedagogy. You may,
  of course, make the *implementation* decisions (state handling, plotting,
  layout) — just not the teaching content.
- **If the spec and the code conflict, or the spec seems wrong, flag it** rather
  than silently "fixing" it. Implementation feedback is welcome; pedagogy changes
  go back through the spec.

Each finished topic's spec stays in `specs/` as the record of what was agreed.

## Two topic patterns (pick the one that fits)

- **Single surface + presets** — template `t02_transformations.py`. One set of
  inputs and one visual; a preset dropdown swaps the *values* (via
  `widgets.set_matrix_state` / `set_vector_state`). Use when every example is the
  same picture with different numbers. Aim ~100 lines.
- **Multi-example selector** — template `t01_vectors.py`. A top `st.radio`
  chooses Example 1/2/3; each example is its own helper (`_example_one()`, ...)
  with its *own* inputs, visual, text, and "Show the math". Only the selected
  branch renders, so the student sees only the lesson being discussed. Pin a
  short `OVERVIEW` at the top and put `HOWTO` in a collapsed expander. These
  topics are naturally longer than ~100 lines — that's expected; keep each
  example helper small instead.

Within either pattern, apply presets only when the selection *changes* (track a
`..._last` key) so manual edits persist, and use `on_click` callbacks for Reset.

## Shared helpers (reuse; don't re-roll per topic)

- `widgets.py`: `matrix_editor`, `vector_editor`, `scalar_slider`,
  `set_matrix_state`, `set_vector_state`, `bmatrix`.
- `plotting.py`: transformation visuals `figure_2d` / `figure_3d`; generic 2D
  primitives `new_figure_2d`, `add_vector_2d`, `add_point_2d`, `shade_polygon`
  (used by combinations/subspaces-style topics).
- `animate.py`: `interpolate(M, t)`.

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

1 Vectors & combinations **(built)** · **2 Linear transformations (built)** · 3 Determinant ·
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
- Don't invent or reword a topic's examples or lesson text — build from the spec
  in `specs/`. Implementation is yours; pedagogy comes from the spec.

## Working agreement (read before every change)

### Running the app — the user owns the server
- Do NOT start, run, or restart the Streamlit server. The user runs it themselves
  in their own terminal.
- Never run `streamlit run app.py` or launch the app in a background shell.
- When a change is ready to look at, say so and let the user reload. Do not spawn a
  server to "test" — multiple servers on the same port cause stale, misleading
  screens.
- If the user asks you to stop the server, you may run a stop command; otherwise
  leave server processes alone.

### Quotes — straight ASCII only
- Use only straight ASCII quotes: " and '. NEVER use curly/smart quotes (" " ' ').
  Smart quotes cause Python SyntaxErrors and have broken this project repeatedly.
- After any edit that adds strings, assume smart quotes may have slipped in and
  check.

### Edits — surgical, never wholesale rewrites
- Make targeted edits: move, add, or change specific lines. Do NOT rewrite an entire
  function from memory — that keeps silently dropping blocks (notices, presets,
  math).
- When relocating code (e.g. into columns), move the existing `st.` calls; keep
  every other line intact.
- If text must be restored, copy it verbatim from git or from the relevant file in
  `specs/`. Do not regenerate approved wording from memory.

### Verify before reporting — show, don't claim
- Do not report a change as "done." Instead: run
  `python -c "import ast; ast.parse(open('PATH').read())"` to confirm it parses,
  then PASTE the changed code (the full function or block) and STOP.
- The user verifies from the pasted code, not from your summary. Wait for review
  before continuing.
- When asked whether something exists in a file, run `grep -n` and paste the raw
  output rather than describing it.

### Scope — one screen/task per turn
- Do exactly one screen or one task per turn, then stop. Never sweep through
  "the remaining screens" or "the rest of the changes" in one pass.
- Wait for the user to confirm and commit before starting the next.

### After each verified change
- Update `specs/STATUS.md` to reflect what is now done.
- Then the user commits before the next change.

### Project structure notes
- `topics/t03_determinant/` is a per-screen package: `surveying.py`, `medical.py`,
  `biology.py`, `graphics.py`, with shared helpers in `__init__.py`. Edit one screen
  file at a time.
- Pedagogy/content decisions are made with the user in chat and recorded in `specs/`.
  Implement from the spec; do not invent new lesson content.