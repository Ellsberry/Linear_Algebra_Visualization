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

1. **New intro** (replaces the current INTRO) — introduces `Ax = b` (with explicit
   order) and the vertex/vector vocabulary. Full text below.
2. **Standardize on `A`** as the matrix name **everywhere the student sees it** —
   the matrix-editor label, the morph slider text, the "Show the math" content,
   the sample-vector math, etc. The current build calls it "M"; rename all
   student-facing references (and ideally the code variable) to **A**. The sample
   vector is now called **x**.
3. **Name the morph variable `t`** on the slider and explain it in words in the
   math panel (it was previously unnamed).
4. **Add "Where each corner lands"** to "Show the math": show the **live numeric
   morphing matrix** (the interpolated matrix as concrete numbers) times each
   vertex. Details below.
5. **Make the determinant track the morph:** show BOTH the live det of the current
   (morphing) transform AND the final det of the target A.
6. **Rewrite the General Warp preset notice** (the eigenvector hunt) — the old
   wording said "drag the sample vector," but it's typed, not dragged, and it
   should compare A·x to **x** and mention there are usually **two** eigenvector
   directions. New text below.

## Core idea (the spine — unchanged)

A matrix `A` is a **function that transforms space**: feed it a vector, it returns
a new vector. The **columns of A are where the basis vectors land** (î, ĵ, and in
3D ẑ), and because every vector is built from those, that determines where
everything goes. This is the keystone the rest of the course hangs from.

## Intro (final text — use verbatim)

`INTRO` markdown, shown at the top of the page:

> Throughout this course we'll keep meeting the equation **Ax = b**. Here's the
> first piece of it. The matrix **A** is a function that transforms space. Apply it
> to a vector **x** — written **A·x**, the matrix on the left acting on x — and out
> comes a new vector, the result **b**. So **Ax = b** just says "apply A to x, and
> you land on b." Right now we're exploring that forward action — *what A does to
> x*. Later we'll turn it around and ask the harder question: given b, which x gets
> you there?
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
- **Morph slider** — name the variable **t** on the slider:
  `scalar_slider("t02_t", "Morph t: identity → matrix A", 0.0, 1.0, 1.0, 0.01)`.
  (t runs 0 → 1; the math panel explains what t means in words.)
- **Sample vector** checkbox "Show a sample vector x" + `vector_editor` when on.
  (Note: call it **x** now, to match Ax = b.)
- **Reset** button (on_click → back to Identity).

## Presets (existing — keep all nine, with real-world notices)

Identity, Shear, Rotation 45°, Reflection, Scale ×2, Non-uniform scale, General
warp, Collapse (singular), Custom — each dimension-aware, each with the real-world
caption already in the build. Keep the preset matrices unchanged. **Change ONE
notice — "General warp"** — replacing the old "drag the sample vector" wording with
this (it's typed, not dragged; compare A·x to x; mention two directions):

> A general transformation that stretches and skews at once. 'Liquify' and
> image-morphing filters bend a picture like this. When A acts on most vectors it
> swings them to point a new way — but a few special vectors come out pointing
> along the *same line* they started on (same direction or exactly opposite, just
> longer or shorter). Turn on the sample vector, type different values into **x**,
> and compare its arrow (x) with its image (A·x): for most x they point different
> ways. Find a direction where A·x lies right along x — then look for a *second*
> one. Those are **eigenvectors** (Topic 8), and most 2D transforms have two.

## Right panel (existing — keep)

Compute `At = interpolate(A, t)` and draw:
- 2D: `figure_2d(At, show_vec, x, At@x, obj=obj)` — deformed grid, square or rocket,
  basis-vector arrows (the columns of At), optional sample vector.
- 3D: `figure_3d(At, show_vec, x, At@x)` — deformed unit cube, basis arrows.

## "Show the math" expander

Keep the existing content, with A naming, then ADD the new corner section.

**Existing (rename M→A):**
- `A = ` [bmatrix of the target matrix A from the cells] — label it "Your matrix A".
- **Determinant — show BOTH, because the picture mid-morph shows the morphing
  transform, not the target.** Display the **live determinant of the current
  morphing transform** `interpolate(A, t)` (the area/volume factor that matches
  what's drawn right now) AND the **final determinant of your matrix A**. E.g.:
  "Area factor now: 2.25 · final (your matrix A): 4.00". Keep the orientation-flip
  / singular notes, applied to the final A. (Honest aside worth a line: for a
  reflection the live factor dips through 0 partway — the shape briefly flattens as
  it flips before reaching the final negative value.)
- Columns mapping: î → col 1, ĵ → col 2 (and ẑ → col 3 in 3D), for the target A.
- If sample vector shown: `A · x = …`.

**NEW — "Where each corner lands":** show the matrix times each vertex of the
on-screen object, using `widgets.bmatrix` and `st.latex`. **Show the actual
morphing matrix as concrete numbers** (not the abstract symbol "A(t)") so the
student watches the entries themselves change as he drags.

- Compute the current transform `T = interpolate(A, t)` and **display its real
  numeric entries** in the multiplication. One plain-language line first, e.g.:
  "These are the matrix's numbers right now (morph **t = {t:.2f}** — {0 = the
  identity, 1 = your full matrix A}). Drag t to 1 to reach A." (Phrase the t value
  in words: t = 0 → "the identity, nothing moves"; t = 1 → "your full matrix A";
  in between → "part-way from the identity to A".)
- For each chosen vertex v, render one `st.latex` line showing the numeric matrix
  times the vertex equals the result:
  `\begin{bmatrix}…numbers of T…\end{bmatrix}\begin{bmatrix}…v…\end{bmatrix} =
  \begin{bmatrix}…T@v…\end{bmatrix}` (2 decimals). The left matrix is the live
  `T`, so it visibly morphs with the slider.
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
> you can check it right here. *(Check it with the Morph slider all the way over at
> t = 1; mid-morph the numbers above are the columns of the in-between transform,
> not yet your final A.)*

## "Try this" expander (existing — keep)

Keep the current challenges (negative determinant; find a vector whose direction
doesn't change → eigenvector teaser; make a column equal to another → collapse).
Update any "M" references to "A" and "v" to "x" for consistency.

## Acceptance checklist

- [ ] Intro shows the Ax = b paragraph (with explicit "A·x, matrix on the left
      acting on x" order) and the vertex/vector definitions at the top.
- [ ] The matrix is called **A** and the sample vector **x** everywhere the student
      sees them (editor label, morph slider, Show-the-math); no leftover "M".
- [ ] The morph slider names **t** ("Morph t: …"), and the math panel explains t in
      words (0 = identity, 1 = your matrix A).
- [ ] All nine presets still work; the **General warp** notice uses the new
      eigenvector wording (compare A·x to x, two directions, no "drag").
- [ ] Determinant shows BOTH the live area/volume factor of the morphing transform
      AND the final det of A; for a reflection the live factor dips through 0
      mid-morph.
- [ ] "Where each corner lands" shows the **live numeric morphing matrix** times
      each vertex (square = 4 corners; rocket = nose, fin tip, window + note); the
      matrix numbers and results change as the morph slider moves; a plain-language
      line explains t.
- [ ] The clarified columns note appears with the "check at t = 1" caveat.
- [ ] Rocket toggle, 2D/3D, morph, sample vector, and Reset all still work; app runs
      with `streamlit run app.py`, no errors.
