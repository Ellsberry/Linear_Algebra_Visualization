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

**Determinant meter:** `_det_meter(det, kind="area_sq")`.

**Show the math (expander) — live calculation:** show `det A = a·d − b·c` with the
current entries substituted, then the result, e.g.
`det A = (1.5)(1.5) − (0)(0) = 2.25`, then "the scan region's area is multiplied by
|det A| = 2.25." Add the sentence: "det = 1 means the area is preserved even though
the shape changed (the tilt correction)."

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
"ratio": ratio})`.

**Notice (always shown) — introduce k in words first:**
> **k is the scale factor** — how many times bigger you make the cell. k = 2 means
> twice as wide, twice as tall, twice as deep. Volume scales with the determinant
> (k³), but the surface that feeds and cools a body only scales as k². So as things
> get bigger the surface-to-volume ratio drops — which is why cells stay tiny, why
> large animals need lungs, gills, and folded intestines, and why an elephant's
> ears are huge.

**Show the math (expander) — live, no "det(kI)" shorthand:**
> Scaling every axis by k gives A = [[k,0,0],[0,k,0],[0,0,k]].
> For a diagonal matrix, the determinant is just the diagonal entries multiplied
> together, so: det A = k × k × k = k³ = (with k = 2) **2 × 2 × 2 = 8** ← the volume
> factor.
> Surface area grows as 6k² = 6 × 4 = 24; volume as k³ = 8; ratio 6/k = 3.

Substitute the **current** k everywhere (the numbers above are the k = 2 example),
so the products recompute as he drags the slider. State the rule plainly: "for a
diagonal matrix, the determinant is the product of the diagonal entries" — that's
why it's k·k·k.

---

## Example 4 — Graphics. 2D rocket, the sign and the collapse. ENDS THE TOPIC.

**Concept:** negative determinant = mirror image (orientation flip); zero
determinant = flattened, area gone, cannot be undone → cliffhanger into Topic 4.

**Inputs:**
- Preset selectbox, key `t03e4_preset`.
- `widgets.matrix_editor("t03e4_A", 2, label="Matrix A")`, presets set it.

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

**Right panel:** `plotting.figure_2d(A, obj="rocket")`.

**Determinant meter:** `_det_meter(det, kind="area_sq")`.

**Show the math (expander) — this screen was missing it; add it, matching the other
screens and reusing Topic 2's corner-math idea:**
- The live determinant with entries substituted: `det A = a·d − b·c`, e.g. mirror
  `(−1)(1) − (0)(0) = −1`; shadow `(1)(0) − (0)(0) = 0`. State: "area scales by
  |det A|; a negative sign means orientation flipped (mirror image); det = 0 means
  the area collapsed to nothing."
- **A times the rocket's vertices** (same as Topic 2): show `A·x = x′` for the
  **nose**, one **fin tip**, and the **window** (coordinates from
  `engine/plotting.py`: `_ROCKET` columns + `_ROCKET_WINDOW`), with the live matrix
  numbers, so he sees the mirror swap left/right (or the shadow flatten every point
  onto the line). Add: "every other vertex transforms the same way."

**Closing line (st.info or st.markdown under the meter, always shown on this
screen):**
> det = 0 means the transform has no inverse. Next topic: exactly when a
> transformation *can* be undone.

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
- [ ] The matrix is called **A** on every screen (not "M"); surveying corners are
      **P, Q, R**.
- [ ] Every "Show the math" shows the determinant (and area/volume) as a **live
      calculation with the current numbers substituted** — e.g. surveying shows
      `det A = (5)(4) − (2)(1) = 18` and `area = ½ × 18 = 9`, and these recompute as
      inputs change. No bare final-only numbers; no "det(kI)" / "det[u v]" shorthand.
- [ ] **Surveying:** the math panel walks points → edge vectors → columns of A →
      det → area; the ½ is explained (triangle = half the parallelogram); moving a
      corner updates everything; dragging R across line PQ makes det negative with
      the clockwise note.
- [ ] **Medical:** "Calibration" shows det 2.25 via `(1.5)(1.5) − (0)(0)`; "Tilt
      correction" shows det 1 with a skewed-but-same-area square; matrix labeled A,
      slider names t.
- [ ] **Biology:** k is introduced as "scale factor" in words; the math shows
      A = diag(k,k,k) and `det A = k × k × k = k³` with the current k substituted,
      plus the "determinant of a diagonal matrix = product of the diagonal" rule;
      surface:volume drops as k rises.
- [ ] **Graphics:** has a "Show the math" panel — live `det A = a·d − b·c` (−1 for
      mirror, 0 for shadow) AND A·(rocket vertices: nose, fin tip, window); "Mirror"
      shows a backwards rocket, "Shadow" flattens it; the no-inverse closing line
      appears.
- [ ] Every screen shows the determinant meter; the app runs with
      `streamlit run app.py` and no import errors.
