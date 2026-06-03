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

**Concept:** the determinant of the two edge vectors of a triangle *is* twice its
area. This is the screen where the number becomes concrete.

**Inputs (left panel), editable coordinates (NOT mouse-drag):**
- Three corners via `widgets.vector_editor`, dim 2:
  - A, key `t03e1_A`, default `(1, 1)`, label "Corner A (m)"
  - B, key `t03e1_B`, default `(6, 2)`, label "Corner B (m)"
  - C, key `t03e1_C`, default `(3, 5)`, label "Corner C (m)"

**Compute:** `u = B - A`, `v = C - A`, `det = u[0]*v[1] - u[1]*v[0]`,
`area = 0.5 * abs(det)`.

**Right panel** — use `plotting.new_figure_2d(rng=10, x_title="meters →",
y_title="meters ↑")`, then:
- Faint filled **parallelogram** spanned by u, v from A: corners
  `[A, A+u, A+u+v, A+v]` via `plotting.shade_polygon(..., "rgba(0,150,136,0.10)",
  "parallelogram (2× the triangle)")`.
- Filled **triangle** `[A, B, C]` via `plotting.shade_polygon(...,
  "rgba(0,150,136,0.28)", "land parcel")`.
- Edge vectors as arrows from A: `add_vector_2d(fig, A, B, "crimson", "edge B−A")`
  and `add_vector_2d(fig, A, C, "royalblue", "edge C−A")`.
- Corner markers + labels via `add_point_2d` (A, B, C).

**Determinant meter:** `_det_meter(det, kind="area_tri")` →
shows `det`, and `area = ½ × |det| = {area:.2f} m²`.

**Orientation moment:** if `det < 0`, the meter state line reads: "det is
negative — you listed the corners clockwise. Area is still ½|det|; surveyors keep
a consistent corner order to control the sign."

**Notice (always shown, st.info):**
> Surveyors and mapping software compute a parcel's area straight from its corner
> coordinates — the determinant *is* the area (this is the "shoelace formula"
> inside every GIS and land-title system). The triangle is exactly half the
> parallelogram its two edges span.

**Show the math (expander):**
- `st.latex` showing `area = ½ |det[u v]|` with u, v as bmatrix columns and the
  numeric determinant.
- One line: the shoelace equivalent
  `½ |x_A(y_B − y_C) + x_B(y_C − y_A) + x_C(y_A − y_B)|`, noting it's the same
  number he might see in a textbook.

---

## Example 2 — Medical imaging. Reuses the square+grid figure.

**Concept:** rescaling a scan scales every measured area by the determinant;
shearing to correct a tilt distorts shape but preserves area (det = 1).

**Inputs:**
- Preset selectbox, key `t03e2_preset`, options below.
- `widgets.matrix_editor("t03e2_M", 2, label="Alignment matrix M")`.
- Optional morph slider (`widgets.scalar_slider("t03e2_t", "Morph: identity →
  matrix", 0.0, 1.0, 1.0, 0.01)`) and draw `animate.interpolate(M, t)`.

**Presets** (apply via `widgets.set_matrix_state` on selection change, tracking a
`t03e2_last` key, exactly like t02):
- **"Calibration (rescale)"** → `[[1.5, 0], [0, 1.5]]` (det = 2.25). Notice:
  > If a scan is rescaled, every measured area — a tumor, a vessel — scales by
  > the determinant. Radiologists calibrate so a 2 cm lesion still measures 2 cm.
- **"Tilt correction (shear)"** → `[[1, 0.6], [0, 1]]` (det = 1). Notice:
  > When software shears a tilted scan into alignment, the shape skews but the
  > area is unchanged (det = 1) — the correction doesn't falsify any measurement.

**Right panel:** `plotting.figure_2d(Mt, obj="square")` (Mt = interpolated matrix;
the unit square = the scan region).

**Determinant meter:** `_det_meter(det, kind="area_sq")` → `det`, and
`area of the region = |det| × original`.

**Show the math:** det of M, and the sentence "area scales by |det|; det = 1 means
area is preserved even though the shape changed."

---

## Example 3 — Biology. 3D, uniform scaling, surface-area-to-volume law.

**Concept:** volume (the determinant) grows as k³ while surface area grows only as
k², so big things have a small surface-to-volume ratio. This is why cells stay
small.

**Inputs:**
- One slider: `widgets.scalar_slider("t03e3_k", "Scale factor k", 0.5, 3.0, 1.5,
  0.1)`.

**Compute:** `M = k * np.eye(3)`; `volume = det = k**3`; `surface = 6 * k**2`;
`ratio = 6 / k`.

**Right panel:** `plotting.figure_3d(M)` (the unit cube scaled by k = a cell).

**Determinant meter:** `_det_meter(det, kind="volume", extra={"surface": surface,
"ratio": ratio})` → show `volume = det = k³ = {volume:.2f}`,
`surface area = 6k² = {surface:.2f}`, `surface : volume = 6/k = {ratio:.2f}`.

**Notice (always shown):**
> Volume scales with the determinant (k³), but the surface that feeds and cools a
> body only scales as k². So as things get bigger the surface-to-volume ratio
> drops — which is why cells stay tiny, why large animals need lungs, gills, and
> folded intestines, and why an elephant's ears are huge.

**Show the math:** `det(kI) = k³` for the 3×3 case; contrast with surface 6k².

---

## Example 4 — Graphics. 2D rocket, the sign and the collapse. ENDS THE TOPIC.

**Concept:** negative determinant = mirror image (orientation flip); zero
determinant = flattened, area gone, cannot be undone → cliffhanger into Topic 4.

**Inputs:**
- Preset selectbox, key `t03e4_preset`.
- `widgets.matrix_editor("t03e4_M", 2, label="Matrix M")`, presets set it.

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

**Right panel:** `plotting.figure_2d(M, obj="rocket")`.

**Determinant meter:** `_det_meter(det, kind="area_sq")`.

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
later if another topic reuses it).

## Registration

In `app.py`: add `t03_determinant` to the `from topics import ...` line, and
insert `(t03_determinant.TITLE, t03_determinant),` in `TOPICS` immediately after
the `t02_transformations` entry.

## Acceptance checklist (verify before committing)

- [ ] Sidebar shows "3 · Determinant" after Topic 2.
- [ ] Selector switches between exactly four screens; only the selected one's
      text/inputs/visual render.
- [ ] **Surveying:** moving a corner updates the triangle, the determinant, and
      `area = ½|det|` together; dragging C to the other side of AB makes det
      negative with the clockwise note. Default corners give a clean triangle.
- [ ] **Medical:** "Calibration" shows det 2.25; "Tilt correction" shows det 1
      with a visibly skewed-but-same-area square.
- [ ] **Biology:** raising k grows the cube; volume = k³ and surface:volume = 6/k
      update; ratio visibly drops as k rises.
- [ ] **Graphics:** "Mirror" shows a backwards rocket with det −1; "Shadow"
      flattens the rocket with det 0 and the no-inverse closing line.
- [ ] Every screen shows the determinant meter; the app runs with
      `streamlit run app.py` and no import errors.
