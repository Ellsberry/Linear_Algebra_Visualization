# Build Spec — Topic 8: Eigenvalues & Eigenvectors

> **For the builder (Claude Code):** implement as a per-screen package
> `topics/t08_eigen/` registered in `app.py` after `t07_projection`. Follow
> `CLAUDE.md`. Reuse the engine (`engine/widgets.py`, `engine/plotting.py`) and the
> Topic 6 / 7 patterns. Student-facing text below is final copy — implement it,
> don't reword. Straight ASCII quotes in code.

`TITLE = "8 · Eigenvalues & Eigenvectors"`, `SLUG = "eigen"`.

## The through-line

When a matrix multiplies a vector, it usually knocks it onto a NEW direction. But
every matrix has a few special directions where the vector comes out pointing the
SAME way — only stretched, shrunk, or flipped. Those directions are eigenvectors;
the scale factor is the eigenvalue. The whole topic is: A·v = λ·v — "the matrix
acting on v is just scaling v." The recurring VISUAL ANCHOR: does A·v stay on v's
line?

## Design rules (same as Topics 6-7)

1. **Viewport blocks:** each screen is a stack of self-contained blocks, each fitting
   one screen-height (math LEFT / graph RIGHT via `st.columns([0.5,0.5])`).
2. **Plain words before symbols**, always.
3. **One interaction max per screen** where it teaches; otherwise static.
4. **Tight math:** multi-line sets as one aligned LaTeX block.
5. Graphs at ~420 height, engine dark palette, primitives.
6. **Selective 3×3:** Screens 2 and 3 add a worked 3×3 example (math + 3D graph)
   BELOW the 2×2; Screen 5 (Markov) is 3×3. Screens 0, 4 stay 2×2 (the "stays on its
   line?" insight is clearest in 2D).

## VERIFIED matrices (do not recompute; use exactly)

- **2×2 primary:** A = [[2,1],[1,2]]. Eigenvalues 3 and 1. Eigenvectors (1,1) for
  λ=3 (A·(1,1)=(3,3)=3·(1,1)) and (1,−1) for λ=1 (A·(1,−1)=(1,−1)=1·(1,−1)).
- **3×3 (Screens 2,3):** B = [[2,1,0],[1,2,0],[0,0,4]]. Eigenvalues 1, 3, 4.
  Eigenvectors: (−1,1,0) for λ=1; (1,1,0) for λ=3; (0,0,1) for λ=4. (Extends the 2×2:
  same top-left block.)
- **Stretch/shrink (Screen 4):** [[2,0],[0,0.5]] — eigenvalue 2 along the x-axis
  (1,0), eigenvalue 0.5 along the y-axis (0,1).
- **Flip/reflection (Screen 4):** [[−1,0],[0,1]] — eigenvalue −1 along (1,0),
  eigenvalue +1 along (0,1).
- **No real eigenvectors (Screen 4):** [[0,−1],[1,0]] — a 90-degree rotation; every
  vector turns, none stays on its line. Topic 9 hook (complex eigenvalues), NO
  computation here.
- **Markov (Screen 5):** P = [[0.7,0.2,0.2],[0.2,0.6,0.2],[0.1,0.2,0.6]]
  (columns = today's weather sunny/cloudy/rainy; rows = tomorrow's; columns sum to 1).
  Dominant eigenvalue 1; steady state (0.4, 0.333, 0.267) = 40% sunny / 33% cloudy /
  27% rainy. From a sunny start it converges in ~8 days.

## Selector

`st.radio` horizontal, key `t08_screen`:
["0 · The special directions", "1 · Eigenvector & eigenvalue defined",
 "2 · Finding eigenvalues", "3 · Finding eigenvectors",
 "4 · What eigenvalues tell you", "5 · Why it matters: Markov chains"]

## OVERVIEW (pinned, verbatim)

> Multiply a vector by a matrix and it usually swings onto a new direction. But
> every matrix has a few special directions that don't swing at all — the vector
> comes out pointing the same way, just longer, shorter, or flipped. Those special
> directions are eigenvectors, and the amount of stretch is the eigenvalue. They are
> the hidden skeleton of a matrix, and they explain everything from vibrating bridges
> to how weather settles into a climate.

---

## Screen 0 — The special directions (interactive, 2×2, pure intuition)

### Block 1 — the idea (text only, verbatim)

> When a matrix multiplies a vector, it moves it. Usually the output A·v points in a
> DIFFERENT direction than v — the matrix has swung it onto a new line. But for a few
> special starting directions, something surprising happens: A·v comes out on the
> SAME line as v, just longer or shorter. Those special directions are what this
> whole topic is about. Let's hunt for them.

### Block 2 — interactive: spin a vector, compare v and A·v (math left, graph right)

Matrix fixed: A = [[2,1],[1,2]]. ONE interaction: an angle slider for v.
  `angle = st.slider("Direction of v (degrees)", 0, 360, 20, key="t08_v_angle")`
  v = (cos, sin)·3 ; Av = A·v.

LEFT: st.latex v and A·v with current numbers; then a plain readout (verbatim
template):
> v points at <angle> degrees. A·v points at <angle_of_Av> degrees.
> <VERDICT>
VERDICT: if v is within ~3 degrees of the line through (1,1) or (1,−1) (i.e. A·v is
parallel to v): "A·v is on the SAME line as v — this is a special direction! Here A
just scales v." else: "A·v landed on a different line — v got swung away. Keep
looking."

RIGHT: `new_figure_2d` (rng~7); draw v (one color) and A·v (another) from the origin;
faintly draw the two eigenvector lines through (1,1) and (1,−1) WITHOUT labeling them
as special yet (just thin guide lines). When v aligns with one, highlight that both
arrows share the line. Caption: "Spin v. Most of the time A·v points elsewhere. Find
the directions where it stays on v's line."

### Block 3 — the reveal (text only, verbatim)

> Did you find them? For this matrix there are two special directions: along (1, 1)
> and along (1, −1). On (1, 1) the matrix triples the vector; on (1, −1) it leaves it
> unchanged. Every other direction gets swung away. Next we give these special
> directions their names.

---

## Screen 1 — Eigenvector & eigenvalue, defined (2×2)

### Block 1 — the definitions (text only, verbatim)

> A special direction where A·v stays on the same line as v is called an
> **eigenvector** of A. The number that tells you how much it got stretched is the
> **eigenvalue**, written with the Greek letter lambda (λ). The whole idea fits in
> one short equation:
>
> **A·v = λ·v** — "the matrix acting on the eigenvector v is the same as just
> multiplying v by the number λ." ("Eigen" is German for "own" — these are the
> matrix's own special directions.)

### Block 2 — the two eigenvectors, shown (math left, graph right)

A = [[2,1],[1,2]].
LEFT: two aligned blocks (verbatim):
> **First eigenvector.** A·(1,1) = (3,3) = 3·(1,1). Same direction, tripled. So
> (1,1) is an eigenvector with eigenvalue λ = 3.
> **Second eigenvector.** A·(1,−1) = (1,−1) = 1·(1,−1). Same direction, unchanged. So
> (1,−1) is an eigenvector with eigenvalue λ = 1.

RIGHT: `new_figure_2d` (rng~7); draw the eigenvector (1,1) and its image (3,3) on the
same line (labeled λ=3); draw (1,−1) and its image (1,−1) (labeled λ=1); both
eigenvector lines drawn through the origin. Caption: "Each eigenvector stays on its
own line; the eigenvalue is how much it stretched."

### Block 3 — closing (verbatim)

> That is the definition. But we were handed the eigenvectors — how would you FIND
> them for a matrix you have never seen? The next two screens show the method:
> first the eigenvalues, then the eigenvectors.

---

## Screen 2 — Finding eigenvalues: the characteristic equation (2×2 then 3×3)

### Block 1 — the derivation (text only + math, verbatim)

> Start from the definition A·v = λ·v and move everything to one side:
> A·v − λ·v = 0. Factor out v — but carefully, because A is a matrix and λ is a
> number, so we write λ as λ·I (lambda times the identity): (A − λI)·v = 0.
>
> Now the key idea. We want a NON-zero eigenvector v that this squashes to zero. From
> Topic 6, a matrix squashes a non-zero vector to zero only when it is singular — and
> from Topic 3, a matrix is singular exactly when its determinant is zero. So:
>
> **det(A − λI) = 0.** This is the **characteristic equation**. Solve it for λ.

Render (A − λI)·v = 0 and det(A − λI) = 0 as their own st.latex lines.

### Block 2 — worked 2×2 (math left, small graph right)

A = [[2,1],[1,2]]. Verbatim + aligned math:
> Subtract λ down the diagonal: A − λI = [[2−λ, 1], [1, 2−λ]]. Its determinant is
> (2−λ)(2−λ) − (1)(1) = (2−λ)² − 1. Set it to zero:
>   (2−λ)² − 1 = 0  →  (2−λ)² = 1  →  2−λ = ±1  →  λ = 1 or λ = 3.
> Two eigenvalues, exactly the stretch factors we saw: 3 and 1.

RIGHT: `new_figure_2d` reusing the two eigenvector lines with their λ labels (small
recap of Screen 1's picture), so eigenvalue-solving connects to the geometry.

### Block 3 — worked 3×3 (math left, 3D graph right)

B = [[2,1,0],[1,2,0],[0,0,4]] (VERIFIED eigenvalues 1, 3, 4). Verbatim:
> The same method scales up. For a 3 by 3, det(B − λI) = 0 becomes a cubic (a
> degree-3 equation), giving up to three eigenvalues. This matrix's extra row and
> column are simple (a 4 sitting alone in the corner), so the answer splits into the
> same 2 by 2 as before plus that corner: the eigenvalues are 1, 3, and 4.

Show det(B − λI) = 0 factoring as ((2−λ)² − 1)(4 − λ) = 0 → λ = 1, 3, 4 (aligned
block). RIGHT: `new_figure_3d` (rng~5) showing the three eigenvector lines
(−1,1,0), (1,1,0), (0,0,1) through the origin, each labeled with its λ. Caption:
"Three eigenvalues, three special directions — now in 3D. Rotate to see them."

### Block 4 — closing (verbatim)

> Eigenvalues in hand, we still need the directions themselves. For each λ, finding
> its eigenvector is a null-space problem you already know how to do.

---

## Screen 3 — Finding eigenvectors: solve (A − λI)v = 0 (2×2 then 3×3)

### Block 1 — the idea (text only, verbatim)

> For each eigenvalue λ, its eigenvectors are every non-zero v with (A − λI)·v = 0 —
> which is exactly the NULL SPACE of the matrix (A − λI). You already learned to
> compute a null space in Topic 6: subtract λ down the diagonal, row-reduce, and read
> off the free-variable direction. Do that once per eigenvalue.

### Block 2 — worked 2×2 (math left, graph right)

A = [[2,1],[1,2]], for λ = 3 and λ = 1. Verbatim, aligned blocks:
> **For λ = 3:** A − 3I = [[−1, 1], [1, −1]]. Row-reduce: the rule is −x₁ + x₂ = 0,
> so x₁ = x₂. The direction is (1, 1) — matching what we saw.
> **For λ = 1:** A − 1I = [[1, 1], [1, 1]]. Row-reduce: x₁ + x₂ = 0, so x₁ = −x₂. The
> direction is (1, −1).

RIGHT: `new_figure_2d` (rng~7); the two eigenvector lines (1,1) and (1,−1) drawn and
labeled with their λ. Caption: "Each eigenvalue's null space is a line — its
eigenvector direction."

### Block 3 — worked 3×3 (math left, 3D graph right)

B = [[2,1,0],[1,2,0],[0,0,4]]. Verbatim, for each λ show (B − λI) and the direction:
> **λ = 1:** direction (−1, 1, 0).  **λ = 3:** direction (1, 1, 0).  **λ = 4:**
> direction (0, 0, 1). Each is the null-space direction of (B − λI) — the same recipe,
> three times.

RIGHT: `new_figure_3d` (rng~5); the three eigenvector lines labeled with λ (1, 3, 4).
Caption: "Three eigenvalues, three eigenvector lines. Notice they are perpendicular —
that happens for symmetric matrices like this one."

### Block 4 — closing (verbatim)

> You can now find both halves: the eigenvalues from det(A − λI) = 0, and each
> eigenvector from its null space. Next: what the eigenvalues actually TELL you.

---

## Screen 4 — What eigenvalues tell you (2×2 gallery)

### Block 1 — reading an eigenvalue (text only, verbatim)

> The eigenvalue λ tells you what the matrix does along its special direction:
> λ greater than 1 STRETCHES; λ between 0 and 1 SHRINKS; λ = 1 leaves it UNCHANGED;
> λ negative FLIPS it to the opposite side (and stretches by the size of λ). Here is
> a gallery.

### Block 2 — stretch and shrink (math left, graph right)

[[2,0],[0,0.5]]. Verbatim: "Along (1,0) the eigenvalue is 2 — it stretches to double.
Along (0,1) the eigenvalue is 0.5 — it shrinks to half." RIGHT: `new_figure_2d`;
(1,0) with image (2,0); (0,1) with image (0,0.5), labeled λ=2 and λ=0.5.

### Block 3 — flip (math left, graph right)

[[−1,0],[0,1]]. Verbatim: "Along (1,0) the eigenvalue is −1 — the vector flips to the
opposite side. Along (0,1) the eigenvalue is +1 — unchanged. This matrix is a mirror
reflection." RIGHT: `new_figure_2d`; (1,0) with image (−1,0) (λ=−1); (0,1) with image
(0,1) (λ=1).

### Block 4 — the honest exception: no real eigenvectors (math left, graph right)

[[0,−1],[1,0]] (a 90-degree rotation). Verbatim:
> Not every matrix has real special directions. A rotation turns EVERY vector onto a
> new line — nothing stays put, so there are no real eigenvectors at all. (There is
> still an answer, but it uses a new kind of number — the "imaginary" numbers — which
> is exactly where the next topic, Topic 9, begins.)

RIGHT: `new_figure_2d`; show a couple of vectors and their 90-degree-rotated images,
none sharing a line. Caption: "A pure rotation: every arrow turns, none stays on its
line."

### Block 5 — closing (verbatim)

> Stretch, shrink, flip, or turn — the eigenvalues read out a matrix's whole
> personality. Last screen: one place this pays off spectacularly — predicting
> weather in the long run.

---

## Screen 5 — Why it matters: Markov chains & the dominant eigenvector (3×3)

### Block 1 — what a Markov chain is (text only, verbatim)

> A **Markov chain** is a system that hops between a few states, one step at a time,
> where the next step depends only on where you are now — not on how you got there.
> You describe it with a matrix whose columns are probabilities: each column says,
> "if I am in THIS state now, here are the chances of each state next." Every column
> adds up to 1, because something must happen next.
>
> Our example: the weather, with three states — sunny, cloudy, rainy. The matrix P
> below reads column by column. The first column says a sunny day is followed by
> another sunny day 70% of the time, a cloudy day 20%, a rainy day 10%.

Show P = [[0.7,0.2,0.2],[0.2,0.6,0.2],[0.1,0.2,0.6]] as a labeled matrix (rows/cols
= sunny/cloudy/rainy).

### Block 2 — run it forward (math left, graph right)

ONE interaction: a step slider.
  `step = st.slider("Days from now", 0, 20, 0, key="t08_markov_step")`
Start from a sunny day, x0 = (1,0,0). Show x_step = P^step · x0 (compute in code).

LEFT: st.latex the current distribution x_step (three numbers, % chance of
sunny/cloudy/rainy that many days out). Verbatim caption template:
> Starting from a sunny day, in <step> days the chances are <s>% sunny, <c>% cloudy,
> <r>% rainy.

RIGHT: `new_figure_2d` OR a simple bar chart of the three probabilities at the chosen
step (bars for sunny/cloudy/rainy). As `step` grows, the bars settle. Caption: "Drag
the days forward and watch the chances stop changing — the weather forgets where it
started."

### Block 3 — the steady state IS the dominant eigenvector (math left, graph right)

Verbatim:
> Push far enough and the numbers stop moving: about 40% sunny, 33% cloudy, 27%
> rainy — no matter what day you started from. That settled distribution is a special
> vector: applying P leaves it unchanged, so P·s = 1·s. It is an eigenvector of P with
> eigenvalue 1 — the **dominant eigenvector**. The long-run climate is literally the
> matrix's own special direction.

Show P·s = s (with s = (0.4, 0.333, 0.267)) as st.latex, and note eigenvalue 1. RIGHT:
the bar chart at the steady state, labeled "steady state = dominant eigenvector".

### Block 4 — the big picture (verbatim)

> This is why eigenvectors matter: whenever a system repeats a step over and over —
> weather settling into a climate, web pages ranked by PageRank, populations reaching
> balance — it lines up with the dominant eigenvector, and the eigenvalue tells you
> whether it grows, shrinks, or holds steady. The special directions are where things
> end up.

### Block 5 — closing bridge (verbatim)

> One loose end remains: the rotation with no real eigenvectors. To handle it we need
> a new kind of number — one whose square can be negative. That is the imaginary unit,
> and complex numbers are the next topic — where rotations finally get their
> eigenvalues.

---

## Reuse / new

- REUSE: `new_figure_2d`, `add_vector_2d`, `add_point_2d`, `add_line_2d`,
  `new_figure_3d`, `add_line_3d`/`_arrow3d` (engine/plotting.py); read-only compact
  matrices; aligned-block LaTeX. Bar chart on Screen 5 via a simple plotly bar (or
  reuse an existing bar helper if present).
- NEW: package `topics/t08_eigen/` — `__init__.py` + `screen_special.py`,
  `screen_defined.py`, `screen_eigenvalues.py`, `screen_eigenvectors.py`,
  `screen_reading.py`, `screen_markov.py`.
- Eigen math is inline numpy; no new engine module required.

## Acceptance checklist

- [ ] Registered in app.py after Topic 7; selector shows 6 screens (0–5).
- [ ] Screen 0: angle slider; v and A·v drawn; verdict fires when v aligns with
      (1,1) or (1,−1); guide lines present.
- [ ] Screen 1: A·(1,1)=3·(1,1) and A·(1,−1)=1·(1,−1) shown with the eigenvector lines.
- [ ] Screen 2: full (A−λI)v=0 → det(A−λI)=0 derivation; 2×2 solved to λ=1,3; 3×3
      B=[[2,1,0],[1,2,0],[0,0,4]] solved to λ=1,3,4 with a 3D eigenvector-line plot.
- [ ] Screen 3: eigenvectors as null spaces of (A−λI); 2×2 dirs (1,1),(1,−1); 3×3
      dirs (−1,1,0),(1,1,0),(0,0,1) with 3D plot.
- [ ] Screen 4: stretch/shrink [[2,0],[0,0.5]], flip [[−1,0],[0,1]], and the rotation
      [[0,−1],[1,0]] with the "no real eigenvectors / Topic 9 hook" (no computation).
- [ ] Screen 5: Markov defined plainly; P=[[0.7,0.2,0.2],[0.2,0.6,0.2],[0.1,0.2,0.6]];
      step slider drives P^step·(1,0,0) computed in code; converges to (0.4,0.333,
      0.267); steady state shown as the dominant eigenvector (P·s=s, λ=1); bar chart.
- [ ] Plain words precede every symbol; "does A·v stay on v's line?" is the recurring
      anchor; all numbers match the VERIFIED matrices above.
