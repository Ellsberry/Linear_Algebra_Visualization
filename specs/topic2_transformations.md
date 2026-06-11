# Build Spec — Topic 2: Linear Transformations

**For the builder (Claude Code):** Topic 2 **already exists** as
`topics/t02_transformations.py`. This spec documents the whole topic AND specifies
the changes to apply. **Update the existing module to match this spec — preserve
every existing feature (presets, rocket toggle, 2D/3D, morph slider, sample
vector) and apply the changes marked below.** Follow `CLAUDE.md`. This file
supersedes the earlier `topic2_revision_show_vertices.md` (you can ignore/delete
that one).

`TITLE = "2 · Linear Transformations"`, `SLUG = "transformations"`. Pattern:
**single surface + presets** (one visual; the preset dropdown swaps the matrix
values — NOT the multi-example selector).

## Changes from the current build (apply these)

1. **New intro** (replaces the current INTRO) — introduces `Ax = b` and the
   vertex/vector vocabulary. Full text below.
2. **Standardize on `A`** as the matrix name **everywhere the student sees it** —
   the matrix-editor label, the morph slider text, the "Show the math" content,
   the sample-vector math, etc. The current build calls it "M"; rename all
   student-facing references (and ideally the code variable) to **A**.
3. **Add "Where each corner lands"** to the "Show the math" expander: show the
   matrix times each vertex of the on-screen object. Details below.

## Core idea (the spine — unchanged)

A matrix `A` is a **function that transforms space**: feed it a vector, it returns
a new vector. The **columns of A are where the basis vectors land** (î, ĵ, and in
3D ẑ), and because every vector is built from those, that determines where
everything goes. This is the keystone the rest of the course hangs from.

## Intro (final text — use verbatim)

`INTRO` markdown, shown at the top of the page:

> Throughout this course we'll keep meeting the equation **Ax = b**. Here's the
> first piece of it. The matrix **A** is a function that transforms space: multiply
> it by a vector **x** and out comes a new vector — that result is **b**. So
> **Ax = b** just says "apply A to x, and you land on b." Right now we're exploring
> that forward action — *what A does to x*. Later we'll turn it around and ask the
> harder question: given b, which x gets you there?
>
> Two words we'll use a lot:
> - A **vertex** is a corner of the shape — a specific point, like the nose of the
>   rocket or the (1,1) corner of the square. "Vertex" is the geometry word.
> - A **vector** is the arrow from the origin to that point — the column of numbers
>   you actually multiply by A. "Vector" is the algebra word.
>
> These are two views of the same thing: **every corner of a shape is described by
> a vector**, and that's exactly why a matrix can transform a shape — it multiplies
> the vector of each corner, and the corners move.
>
> The columns of A tell you where the basis vectors (î, ĵ, and in 3D ẑ) land. Watch
> the grid deform: edit the cells of A or pick an example, and drag the **Morph**
> slider to see the identity turn into your matrix A.

(The vertex/vector definitions live in the intro on purpose — keeping them at the
top reduces scrolling between the graph and the math panel.)

## Left panel (existing — keep, with A naming)

- **Space** radio: 2D / 3D (`dim` = 2 or 3).
- **Object** radio (2D only): "Unit square" / "Rocket 🚀".
- **Example** preset selectbox (presets below). On change, set the matrix cells via
  `set_matrix_state` (track a `_last` key so manual edits persist); for "General
  warp" also force the sample-vector checkbox ON.
- `st.info(notice)` for the selected preset.
- **Matrix editor** — `matrix_editor("t02_A", dim, label="Matrix A (its columns = where the basis lands)")`.
- **Morph slider** — `scalar_slider("t02_t", "Morph: identity → matrix A", 0.0, 1.0, 1.0, 0.01)`.
- **Sample vector** checkbox "Show a sample vector x" + `vector_editor` when on.
  (Note: call it **x** now, to match Ax = b.)
- **Reset** button (on_click → back to Identity).

## Presets (existing — keep all nine, with real-world notices)

Identity, Shear, Rotation 45°, Reflection, Scale ×2, Non-uniform scale, General
warp, Collapse (singular), Custom — each dimension-aware, each with the real-world
caption already in the build. (No changes to the preset matrices or notices.)

## Right panel (existing — keep)

Compute `At = interpolate(A, t)` and draw:
- 2D: `figure_2d(At, show_vec, x, At@x, obj=obj)` — deformed grid, square or rocket,
  basis-vector arrows (the columns of At), optional sample vector.
- 3D: `figure_3d(At, show_vec, x, At@x)` — deformed unit cube, basis arrows.

## "Show the math" expander

Keep the existing content, with A naming, then ADD the new corner section.

**Existing (rename M→A):**
- `A = ` [bmatrix of the target matrix A from the cells] — label it "Your matrix A".
- Determinant of A, with the orientation-flip / singular notes.
- Columns mapping: î → col 1, ĵ → col 2 (and ẑ → col 3 in 3D).
- If sample vector shown: `A · x = …`.

**NEW — "Where each corner lands":** show the matrix times each vertex of the
on-screen object, using `widgets.bmatrix` and `st.latex`.

- **Use the current transform `At = interpolate(A, t)`**, so the numbers match the
  picture at the current slider position (including mid-morph). To avoid any
  "which matrix?" confusion, **display the current matrix explicitly at the top of
  this section**: "Current transform (morph slider at t = {t:.2f}): A(t) =
  [bmatrix of At]". Every corner line below uses this same At, so it's
  self-consistent at any slider position.
- For each chosen vertex v, render one `st.latex` line:
  `A(t)\,\begin{bmatrix}…\end{bmatrix} = \begin{bmatrix}…\end{bmatrix}` with the
  right side = `At @ v` (2 decimals).
- **Square (`obj=="square"`, 2D):** show all 4 corners — `(0,0)`, `(1,0)`, `(1,1)`,
  `(0,1)`.
- **Rocket (`obj=="rocket"`, 2D):** show 3 labeled vertices — **nose**, one **fin
  tip**, and the **window** — using the actual coordinates from
  `engine/plotting.py` (`_ROCKET` columns for nose + a fin tip; `_ROCKET_WINDOW`).
  Add: "Every other vertex transforms the same way."
- **3D (`dim==3`):** optional; if included, show the three axis corners
  `(1,0,0)`, `(0,1,0)`, `(0,0,1)`. 2D-only is acceptable — the square/rocket case is
  where the confusion arose.

**Columns note (clear wording — include after the corner lines):**
> Two of these corners are special. The corner **(1,0)** is the basis vector **î**,
> and **(0,1)** is **ĵ**. Look at where they land: **A · (1,0)** is the **first
> column of A**, and **A · (0,1)** is the **second column**. That's the rule from
> the top of this topic — "the columns of A are where the basis vectors go" — and
> you can check it right here. *(Exactly true when the Morph slider is all the way
> over at t = 1; mid-morph these are the columns of the in-between transform A(t).)*

## "Try this" expander (existing — keep)

Keep the current challenges (negative determinant; find a vector whose direction
doesn't change → eigenvector teaser; make a column equal to another → collapse).
Update any "M" references to "A" and "v" to "x" for consistency.

## Acceptance checklist

- [ ] Intro shows the Ax = b paragraph and the vertex/vector definitions at the top.
- [ ] The matrix is called **A** everywhere the student sees it (editor label, morph
      slider, Show-the-math, sample-vector math); no leftover "M".
- [ ] All nine presets and their real-world notices still work; rocket toggle, 2D/3D,
      morph, sample vector, and Reset all still work.
- [ ] "Show the math" → "Where each corner lands": square shows all 4 corners as
      `A(t)·v = v′`; rocket shows nose, a fin tip, and the window, plus the
      "every other vertex…" note; numbers match the picture as the morph slider
      moves; the current matrix A(t) is shown at the top of the section.
- [ ] The clarified columns note appears with the t = 1 caveat.
- [ ] App runs with `streamlit run app.py`, no errors.
