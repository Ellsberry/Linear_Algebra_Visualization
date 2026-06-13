# Build Spec — Topic 3: Determinant

**For the builder (Claude Code):** Implement this as a new topic module
`topics/t03_determinant.py` and register it in `app.py`. Follow the conventions
in `CLAUDE.md`. Use the **multi-example selector** pattern — copy
`topics/t01_vectors.py` as the structural template (top `st.radio` selects the
example; only the selected example renders; `OVERVIEW` pinned at top; `HOWTO` in
a collapsed expander). **Reuse the existing engine** (`engine/widgets.py`,
`engine/plotting.py`, `engine/animate.py`); do not hand-roll inputs or figures.
Do not invent new examples or change the wording below — the text is final.

`TITLE = "3 · Determinant"`, `SLUG = "determinant"`.

## If Topic 3 is already built

If `topics/t03_determinant.py` already exists from an earlier version of this spec,
**update it** to match — apply the clarifications below (A naming, live
substituted calculations, P/Q/R corners, the k explanation, Graphics math) and
preserve the working visuals. Otherwise build it fresh.

## Global conventions for this topic (apply on every screen)

- **Name the matrix `A`** everywhere the student sees it (not "M"), consistent with
  Topic 2 and the course's Ax = b throughline. Use **A·x** wherever a vector or
  point is actually being transformed.
- **Surveying corners are `P, Q, R`** — the letter **A** is reserved for the
  matrix, so corners must not be named A/B/C.
- **Show the determinant (and any area/volume) as a LIVE calculation** in every
  "Show the math" panel — never a bare final number. Substitute the current entries
  and show the arithmetic, then the result, recomputing as inputs change. E.g.
  `det A = (5)(4) − (2)(1) = 18`, then `area = ½ × 18 = 9`. This is the same
  "show the real numbers" principle used in Topic 2's corner math.
- **No internal shorthand in student-facing text** — do NOT write "det(kI)" or
  "det[u v]"; write the explicit matrix with its current numbers and the
  multiplied-out determinant.
- **Build the matrix visibly** — on each screen, show how A is assembled from the
  inputs (points → edge vectors → columns; or "scaling by k → diagonal matrix"), so
  A never appears fully formed by magic.
- **CRITICAL — the math must move with the morph slider.** On any screen with a
  morph slider, every "Show the math" value must be computed from the **current
  morphing matrix** `At = interpolate(A, t)` (or the current-`k` matrix in biology),
  **NOT** the target `A` in the cells. This includes the determinant, the
  area/volume, the matrix entries displayed, and the A·vertex lines. If the numbers
  don't change as the slider moves, that's the bug — it means something is still
  reading `A` instead of `At`. This rule keeps getting dropped; it is on every
  screen's acceptance check below.
- **"Now vs destination" labeling** (use the same two-line pattern everywhere a
  morph exists, as in Topic 2): show the live matrix as "Current transform (morph
  t = {t:.2f}): At = […]" and, when helpful, the target as "Your matrix A (the
  destination at t = 1): […]".

## Core idea (the spine of the whole topic)

The determinant is **an area (2D) or a volume (3D)** — the factor by which a
transformation scales it — and **its sign tells you whether orientation
flipped.** Every screen must show the determinant value *next to the area or
volume it represents*, so the two read as the same thing. Implement a shared
helper `_det_meter(...)` (see last section) and call it on every screen.

## Selector and always-on text

Top selector (st.radio, horizontal, key `t03_example`), in THIS order:
`["1 · Surveying", "2 · Medical imaging", "3 · Biology", "4 · Graphics"]`.

`OVERVIEW` (pinned markdown at top):
> A determinant is one number that answers a simple question: when a
> transformation acts on space, **by what factor does area (in 2D) or volume (in
> 3D) change — and does it flip things into a mirror image?** That single number
> turns out to matter to surveyors, radiologists, biologists, and game
> programmers. We'll meet it in all four fields, and each time you'll see the
> determinant *is* an area or a volume — not just a formula.
>
> Here's the formula in letters (the examples fill in real numbers):
>
> 2D: det [[a, b], [c, d]] = a·d − b·c
>
> 3D: det [[a, b, c], [d, e, f], [g, h, i]] = a(e·i − f·h) − b(d·i − f·g) + c(d·h − e·g)
>
> The 3D formula looks like a lot, but notice each term is just one top-row entry
> times a little 2×2 determinant of what's left — it's the 2D formula used three
> times. And when the matrix is simple, like the diagonal one in biology, almost
> everything is zero and it collapses to just the diagonal multiplied together.

(Render both formulas with `st.latex` using proper bmatrix notation.)

`HOWTO` (collapsed expander "How to use this screen"):
> The left panel sets the numbers; the right panel shows the shape. The
> **determinant meter** under each picture shows the determinant and the area or
> volume it equals — watch them change together. Open **Show the math** to see
> the formula behind the number.

---

## Example 1 — Surveying (engineering). OWN SCREEN, the centerpiece.

**Concept:** the two edges of a triangular plot, taken as the **columns of a matrix
A**, have a determinant equal to the area of the parallelogram they span — and the
triangle is exactly half of that. So `area = ½ |det A|`. This is the screen where
the determinant becomes a concrete area, built step by step from the corner points.

**Inputs (left panel), editable coordinates (NOT mouse-drag). Corners are P, Q, R
(A is the matrix):**
- P, key `t03e1_P`, default `(1, 1)`, label "Corner P (m)"
- Q, key `t03e1_Q`, default `(6, 2)`, label "Corner Q (m)"
- R, key `t03e1_R`, default `(3, 5)`, label "Corner R (m)"

**Compute (build A from the points, visibly):** edge vectors `u = Q - P` and
`v = R - P`. **These two edges are the columns of A:** `A = [[u0, v0], [u1, v1]]`.
Then `det = u0*v1 - u1*v0` and `area = 0.5 * abs(det)`.

**Right panel** — `plotting.new_figure_2d(rng=10, x_title="meters →",
y_title="meters ↑")`, then:
- Faint filled **parallelogram** spanned by u, v from P: corners
  `[P, P+u, P+u+v, P+v]` via `shade_polygon(..., "rgba(0,150,136,0.10)",
  "parallelogram (det A)")`.
- Filled **triangle** `[P, Q, R]` via `shade_polygon(..., "rgba(0,150,136,0.28)",
  "land parcel (½ of it)")`.
- Edge vectors as arrows from P: `add_vector_2d(fig, P, Q, "crimson", "edge u = Q−P (column 1 of A)")`
  and `add_vector_2d(fig, P, R, "royalblue", "edge v = R−P (column 2 of A)")`.
- Corner markers + labels P, Q, R via `add_point_2d`.

**Determinant meter:** `_det_meter(det, kind="area_tri")`.

**Orientation moment:** if `det < 0`, the meter state line reads: "det is negative —
you listed the corners clockwise. Area is still ½|det|; surveyors keep a consistent
corner order to control the sign."

**Notice (always shown, st.info):**
> Surveyors and mapping software compute a parcel's area straight from its corner
> coordinates — the determinant *is* the area (this is the "shoelace formula"
> inside every GIS and land-title system). The determinant is the area of the
> **parallelogram** the two edges span; your triangular plot is exactly **half** of
> that, which is where the ½ comes from.

**Show the math (expander) — the full LIVE chain, every line recomputing from the
current P, Q, R:**
> Corner points: P = (1, 1), Q = (6, 2), R = (3, 5)
> Edge vectors (the columns of A): u = Q − P = (5, 1), v = R − P = (2, 4)
> A = [[5, 2], [1, 4]]
> det A = (5)(4) − (2)(1) = 20 − 2 = **18**  ← the parallelogram's area
> area of the triangle = ½ × |det A| = ½ × 18 = **9 square meters**

Render each line with `st.latex`/`st.markdown` using the **current** numbers (the
ones above are just the default-corner example). Show the determinant with the
entries plugged in — `(5)(4) − (2)(1)` — not just the result, and show the `½ ×`
step explicitly so the area is a visible calculation. Add one line: "the ½ is
because the triangle is half the parallelogram the two edges make." (Optional: the
equivalent shoelace expansion as a single extra line, noted as "the same number
your textbook's formula gives.")

---

## Example 2 — Medical imaging. Reuses the square+grid figure.

**Concept:** rescaling a scan scales every measured area by the determinant;
shearing to correct a tilt distorts shape but preserves area (det = 1).

**Inputs:**
- Preset selectbox, key `t03e2_preset`, options below.
- `widgets.matrix_editor("t03e2_A", 2, label="Alignment matrix A")`.
- Morph slider `widgets.scalar_slider("t03e2_t", "Morph t: identity → matrix A",
  0.0, 1.0, 1.0, 0.01)`; draw `animate.interpolate(A, t)`.

**Presets** (apply via `widgets.set_matrix_state` on selection change, tracking a
`t03e2_last` key, exactly like t02):
- **"Calibration (rescale)"** → `[[1.5, 0], [0, 1.5]]` (det = 2.25). Notice:
  > If a scan is rescaled, every measured area — a tumor, a vessel — scales by
  > the determinant. Radiologists calibrate so a 2 cm lesion still measures 2 cm.
- **"Tilt correction (shear)"** → `[[1, 0.6], [0, 1]]` (det = 1). Notice:
  > When software shears a tilted scan into alignment, the shape skews but the
  > area is unchanged (det = 1) — the correction doesn't falsify any measurement.

**Right panel:** `plotting.figure_2d(At, obj="square")` where `At = interpolate(A,
t)`; the unit square = the scan region, and its corners are transformed by A·x.
**The morph must actually redraw** — recompute `At` from the slider each run and
pass `At` (not the static A) to the figure, so dragging t animates identity → A. (A
dead/static morph here is a bug; verify it animates.)

**Notice (always shown) — what the matrix does and what to look for:**
> This matrix is how the scanner's image is being **stretched or skewed**. Change
> its entries (or pick a preset) and watch the scan region deform; the determinant
> tells you whether the **area** of anything you measure — a tumor, a vessel — got
> bigger, smaller, or stayed the same. **What to look for:** the *Calibration*
> preset scales everything up, so areas grow (det > 1); the *Tilt correction* shear
> skews the shape but **keeps the area unchanged (det = 1)** — that's the important
> case, because a measurement taken after it is still trustworthy.

**Determinant meter:** `_det_meter(det_of_At, kind="area_sq")` — use the **live**
determinant of `At`, so it changes with the slider.

**Show the math (expander) — all values from `At = interpolate(A, t)`, so they move
with the slider:**
- **Now vs destination:** "Current transform (morph t = {t:.2f}): At = […]" and
  "Your matrix A (destination at t = 1): […]".
- `det At = a·d − b·c` with the current At entries substituted, then the result.
- **Measured area, before → after:** "region area before = 1.00 → after =
  |det At| × 1.00 = {…}." Recompute live.
- **At · x = x′ for the square's 4 corners** `(0,0)`, `(1,0)`, `(1,1)`, `(0,1)` —
  using the live At numbers, so the region's corners visibly move as he drags.
- The sentence: "det = 1 means the area is preserved even though the shape changed
  (the tilt correction)."
- **Topic 4 pointer (one line):** "Actually *undoing* a distortion — turning a
  tilted scan back into a square one — means applying the transform's **inverse**.
  That's the next topic; here we're just seeing how the determinant tells us
  whether area was preserved."

---

## Example 3 — Biology. 3D, uniform scaling, surface-area-to-volume law.

**Concept:** volume (the determinant) grows as k³ while surface area grows only as
k², so big things have a small surface-to-volume ratio. This is why cells stay
small.

**Inputs:**
- One slider: `widgets.scalar_slider("t03e3_k", "Scale factor k (how many times bigger)", 0.5, 3.0, 1.5, 0.1)`.

**Compute (build A from k, visibly):** scaling every axis by k is the diagonal
matrix `A = [[k,0,0],[0,k,0],[0,0,k]]` (= `k * np.eye(3)`). `volume = det = k**3`;
`surface = 6 * k**2`; `ratio = 6 / k`.

**Right panel:** `plotting.figure_3d(A)` (the unit cube scaled by k = a cell).

**Determinant meter:** `_det_meter(det, kind="volume", extra={"surface": surface,
"ratio": ratio})`. State the ratio in plain language (no colon): "For every 1 unit
of volume, there are **{6/k:.1f} units of surface**."

**Notice (always shown) — introduce k in words first, then the surface-vs-volume
consequence with real context:**
> **k is the scale factor** — how many times bigger you make the cell. This matrix
> **scales the whole cell uniformly by k**: every direction grows by the same
> factor k (k = 2 means twice as wide, twice as tall, twice as deep).
>
> A cell absorbs food and oxygen through its **surface**, but it has to feed its
> whole **volume**. When you make something bigger, the volume (k³) outgrows the
> surface (k²), so the surface can't keep up with the demand — which is why cells
> stay tiny, and why large animals can't just be "scaled-up" cells: they need extra
> surface area folded in (lungs, gills, intestines). It's also why an **elephant
> has enormous ears**: a big warm body makes heat throughout its volume but can
> only shed it through its surface, so the elephant grows extra surface — those
> huge, blood-rich ears — to dump the heat its size can't otherwise lose.

**Show the math (expander) — live, no "det(kI)" shorthand, recompute from current k:**
> This matrix scales the whole cell uniformly by k: A = [[k,0,0],[0,k,0],[0,0,k]].
> The determinant of any **triangular** matrix — including this **diagonal** one —
> is just the diagonal entries multiplied together. So: det A = k × k × k = k³ =
> (with k = 2) **2 × 2 × 2 = 8** ← the volume factor.
> Surface area grows as 6k² = 6 × 4 = 24; volume as k³ = 8. So **for every 1 unit of
> volume there are 6/k = 3 units of surface** — and that number *falls* as the cell
> grows (k = 1 → 6 units of surface per volume; k = 3 → 2), so the surface can't
> keep up with the volume it has to serve.

Then show **A · x = x′ for three cube corners** (e.g. `(1,0,0)`, `(0,1,0)`,
`(1,1,1)`) using the current scaling matrix, so as he drags k the corners move
outward and the numbers grow. Substitute the **current** k everywhere (the numbers
above are the k = 2 example), so everything recomputes as he drags the slider. Keep
the bridging sentence about triangular matrices — it forward-links to triangular
form in Topic 5.5, where "determinant = product of the diagonal" gets used in
earnest. (Call the matrix
**diagonal** — that's accurate; just note a diagonal matrix is a special triangular
one.)

---

## Example 4 — Graphics. 2D rocket, the sign and the collapse. ENDS THE TOPIC.

**Concept:** negative determinant = mirror image (orientation flip); zero
determinant = flattened, area gone, cannot be undone → cliffhanger into Topic 4.

**Inputs:**
- Preset selectbox, key `t03e4_preset`.
- `widgets.matrix_editor("t03e4_A", 2, label="Matrix A")`, presets set it.
- **Morph slider** `widgets.scalar_slider("t03e4_t", "Morph t: identity → matrix A",
  0.0, 1.0, 1.0, 0.01)` — so the mirror animates from identity to the reflection
  instead of snapping.

**Presets:**
- **"Mirror (reflection)"** → `[[-1, 0], [0, 1]]` (det = −1, horizontal flip →
  backwards rocket). Notice:
  > Games flip sprites to draw reflections, and use the *sign* of the determinant
  > to tell which way a surface faces — that's how an engine skips drawing the
  > hidden back of an object (back-face culling).
- **"Shadow (collapse)"** → `[[1, 0], [0, 0]]` (det = 0, flattens to a line).
  Notice:
  > A shadow flattens an object onto the ground. det = 0 means the area is gone —
  > and you can't rebuild the rocket from its shadow. There is no way to undo it.

**Right panel:** `plotting.figure_2d(At, obj="rocket")` where `At = interpolate(A,
t)` — the rocket morphs from upright (identity) to mirrored/flattened as t goes 0→1.

**Determinant meter:** `_det_meter(det_of_At, kind="area_sq")` — use the **live**
determinant of the morphing matrix, so it animates (for the mirror it runs 1 → 0 →
−1, and the rocket visibly flattens to a line at det = 0 mid-morph before re-forming
mirrored; for the shadow it runs 1 → 0).

**Show the math (expander) — show BOTH matrices, clearly labeled, all values from
`At = interpolate(A, t)` so they move with the slider:**
- **The two matrices, labeled:** "Current transform (morph t = {t:.2f}): At = […]"
  (the live morphing matrix, entries changing from `[[1,0],[0,1]]` toward
  `[[−1,0],[0,1]]` for the mirror, matching the rocket) AND "Your matrix A (the
  destination at t = 1): […]" (the target in the cells).
- **The live determinant** of At: `det = a·d − b·c` with the current At entries
  substituted, then the result. State: "negative ⇒ orientation flipped (mirror
  image); 0 ⇒ area collapsed to nothing."
- **At · x = x′ for the rocket's vertices:** the **nose**, one **fin tip**, and the
  **window** (coordinates from `engine/plotting.py`: `_ROCKET` columns +
  `_ROCKET_WINDOW`), using the live At numbers, plus "every other vertex transforms
  the same way."

**Closing line (st.info or st.markdown under the meter, always shown on this
screen):**
> det = 0 means this transform has no inverse — the flattened rocket can't be turned
> back. Topic 4 is about exactly which transformations can be undone, and how.

---

## Shared helper: `_det_meter`

Define once in the module and call on every screen. Signature suggestion:
`_det_meter(det, kind, extra=None)`. Render with `st.metric` for the determinant
value plus a short colored state line:

- `det > 1e-9`: neutral/blue. Text by kind:
  - `area_tri`: "area = ½ × |det| = {0.5*abs(det):.2f} m²"
  - `area_sq`: "area scales by ×{det:.2f}"
  - `volume`: "volume = det = {det:.2f}; surface = {extra['surface']:.2f}; "
    "surface:volume = {extra['ratio']:.2f}"
- `det < -1e-9`: info color. "orientation flips (det < 0); area = |det| = "
  "{abs(det):.2f}" (and the surveying clockwise note for `area_tri`).
- `abs(det) <= 1e-9`: warning color. "collapses — area is zero, no inverse."

Keep it self-contained in the topic for now (it can move to `engine/widgets.py`
later if another topic reuses it). The meter is the headline number; the **live
substituted calculation** (entries plugged in, then the result) lives in each
screen's "Show the math" panel per the global conventions above.

## Registration

In `app.py`: add `t03_determinant` to the `from topics import ...` line, and
insert `(t03_determinant.TITLE, t03_determinant),` in `TOPICS` immediately after
the `t02_transformations` entry.

## Acceptance checklist (verify before committing)

- [ ] Sidebar shows "3 · Determinant" after Topic 2.
- [ ] **On every screen with a morph slider, the "Show the math" numbers change as
      the slider moves** (computed from `At`/current-k, not the target A). This is
      the most-dropped requirement — test it on Medical, Biology, and Graphics.
- [ ] The intro shows both the 2D and 3D determinant formulas in letters, with the
      "each 3D term is the 2D formula" framing line.
- [ ] **Medical:** the morph animates AND the math moves with it; the notice
      explains what the matrix does and what to look for; the math shows At vs A
      labeled, `det At` live, area before→after, and At·(4 corners); Topic 4
      inverse pointer appears.
- [ ] **Biology:** wording says it **scales the whole cell uniformly by k**; the
      cell + elephant context appears; the math shows A = diag(k,k,k),
      `det A = k×k×k`, and At·(3 corners) all live as k changes; the ratio reads
      "for every 1 unit of volume there are 6/k units of surface" (no colon, no
      percent); diagonal-matrix-is-special-triangular bridge present.
- [ ] **Graphics:** morph slider animates (mirror flattens at det 0 mid-morph); the
      math shows BOTH "Current transform At" and "Your matrix A" labeled, `det At`
      live, and At·(rocket vertices) — all moving with the slider; the reworded
      no-inverse / Topic-4 closing line appears.
- [ ] **Surveying:** the math walks points → edge vectors → columns of A → det →
      area; the ½ is explained; dragging R across line PQ makes det negative with
      the clockwise note. Matrix called **A**, corners **P, Q, R**; no
      "det(kI)"/"det[u v]" shorthand anywhere.
- [ ] Every screen shows the determinant meter; the app runs with
      `streamlit run app.py` and no import errors.
