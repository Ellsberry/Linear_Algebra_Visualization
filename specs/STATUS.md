# Topic Status Checklist

Tracks implementation against the specs in `specs/`. Updated manually as work lands.

Legend: [x] done · [~] partial · [ ] not started

---

## Layout refactor + dark mode (app-wide)

- [x] Dark theme applied (`.streamlit/config.toml`: dark base, `#4dabf7` primary, `#0e1117` bg)
- [x] Topic selector moved to top-of-page selectbox (sidebar topic nav removed)
- [x] Plotting palette re-tuned for dark backgrounds (transparent bg, light font/axes, brighter data colors)
- [x] Graph heights reduced (2D ~420, 3D ~420) and Plotly margins tightened (`l=10,r=10,t=10,b=10`)
- [x] `editable_matrix` bracket widget added to `engine/widgets.py` (editable + read-only `editable=False` modes; flexbox-centered bracket glyphs)
- [x] `engine/layout.py` added (`two_col(ratio)` helper)

**NOT yet refactored:** Topic 5.5 still uses the OLD layout (wide augmented matrices need a wider-math layout, not the standard 0.5/0.5 split — explicitly exempted). It also has outstanding content work (see Topic 5.5 section below).

---

## Topic 1 — Vectors & Combinations (`topics/t01_vectors/`)

**Spec:** `specs/topic1_vectors.md`

**File structure:** `t01_vectors` is now a per-screen package:
- `__init__.py` — TITLE, SLUG, VIEW, OVERVIEW, HOWTO, shared constants (BANANA, PEANUT, PROTEIN_AXIS, SUGAR_AXIS), render() dispatcher
- `example_one.py` — Example 1 (One ingredient)
- `example_two.py` — Example 2 (Two ingredients, added)
- `example_three.py` — Example 3 (The smoothie mixer)

- [x] Module exists and registered in `app.py` (imports as `topics.t01_vectors`)
- [x] OVERVIEW with smoothie framing + Ax = b forward-gesture paragraph
- [x] HOWTO in collapsed expander
- [x] Three examples in correct order

### Content additions
- [x] Light Ax = b gesture added to OVERVIEW ("The question we keep circling...")
- [x] Explicit ingredients-to-algebra mapping added after Example 3's math (ingredients→A columns, scoops→x, target→b)

### Layout refactor (all three screens)
- [x] Per-screen package split complete (example_one.py, example_two.py, example_three.py)
- [x] Controls in full-width band above the two columns
- [x] `st.columns([0.5, 0.5])` — math left, graph right
- [x] All "Show the math" expanders removed — math always visible in left column
- [x] Example 3: DEFINITION block full-width above columns; readouts under graph in right column; Ax = b mapping + Challenge + Reality check all full-width always-shown at bottom (expanders removed)
- [x] Notice/closing content full-width at bottom

**Note:** Topic 1 uses hardcoded light-mode plot colors (e.g. "darkorange", "crimson", "navy") unlike Topics 2-4 which use the engine's dark-palette constants. May need a color-tune follow-up if anything looks dim on dark backgrounds.

## Topic 2 — Linear Transformations (`t02_transformations.py`)

- [x] Module exists and registered in `app.py`
- [x] Ax = b intro with vertex/vector definitions
- [x] Matrix named A everywhere (no leftover "M")
- [x] Morph slider names t ("Morph t: identity → matrix A")
- [x] All 9 presets work (Identity through Custom)
- [x] General Warp notice: updated eigenvector wording (compare A·x to x, two directions, no "drag")
- [x] Determinant: both live (morphing) and final (target A), labeled "determinant"
- [x] Meaning line (area scales by |det|, sign = orientation)
- [x] Mid-morph acknowledgment (dips below 1 / dips through 0 for reflection)
- [x] "Where each corner lands" — live numeric morphing matrix × each vertex
  - [x] Square: 4 corners
  - [x] Rocket: nose, fin tip, window + "every other vertex" note
  - [x] 3D: three axis corners
- [x] Columns note with "check at t = 1" caveat
- [x] Sample vector checkbox + vector editor (named x)
- [x] Reset button

### Layout refactor
- [x] Controls in full-width band: left-packed toggle row (`st.columns([1,1,1.3,1.3,3])`) grouping Space/Object/Preset/sample-vector checkbox, then slider + notice full-width below
- [x] `st.columns([0.5, 0.5])` — math left, graph right
- [x] "Show the math" expander removed — math always visible in left column
- [x] "Try this" expander removed — content shown as full-width block at bottom
- [x] `editable_matrix` widget in use (editable, runs at both 2x2 and 3x3)
- [x] Corner blocks wrapped in `{\small}`
- [x] Single-screen topic (not split into files)

## Topic 3 — Determinant (`topics/t03_determinant/`)

**File structure:** `t03_determinant` is now a per-screen package:
- `__init__.py` — TOPIC registry, OVERVIEW, example selector, dispatch, `_det_meter` helper
- `surveying.py` — Example 1
- `medical.py` — Example 2
- `biology.py` — Example 3
- `graphics.py` — Example 4

- [x] Module exists and registered in `app.py` (imports as `topics.t03_determinant`)
- [x] OVERVIEW with 2D and 3D formulas in LaTeX + "each 3D term is the 2D formula" framing
- [x] HOWTO folded into a caption under the overview (no separate expander)
- [x] Four examples in correct order (Surveying, Medical, Biology, Graphics)
- [x] `_det_meter` shared helper on every screen

### Layout refactor (all four screens)
- [x] Controls in full-width band above the two columns
- [x] `st.columns([0.5, 0.5])` — math left, graph + det meter right
- [x] "Show the math" expander removed — math always visible in left column
- [x] Matrix shown via `editable_matrix` (editable for Medical/Graphics; read-only for Biology/Surveying)
- [x] `_det_meter` placed under the graph in the right column
- [x] Notice/closing line full-width at bottom

### Example 1 — Surveying
- [x] Editable P, Q, R corners (A reserved for matrix)
- [x] Parallelogram + triangle + edge arrows + corner markers on figure
- [x] Determinant meter (area_tri)
- [x] Orientation note when det < 0 (clockwise corners)
- [x] Notice (shoelace / GIS)
- [x] Math: full live chain (points → edges → columns → det → area)
- [x] Shoelace expansion line
- [x] "The ½ is because..." explanation
- [x] A shown as read-only `editable_matrix` (derived from P, Q, R)

### Example 2 — Medical imaging
- [x] Preset selectbox (Calibration / Tilt correction) with `set_matrix_state`
- [x] Editable A via `editable_matrix` widget + morph slider
- [x] Morph animates (figure uses `At = interpolate(A, t)`)
- [x] Notice: what the matrix does + what to look for
- [x] Determinant meter uses live `det(At)`
- [x] Math: now-vs-destination labeling (At as read-only `editable_matrix`, A as read-only)
- [x] Math: `det At` with entries substituted
- [x] Math: area before → after
- [x] Math: At · (4 square corners) with `{\small}` and numeric `bmatrix(At)`
- [x] Math: "det = 1 means area preserved" sentence
- [x] Topic 4 pointer ("inverse" forward-link)

### Example 3 — Biology
- [x] Scale factor k slider (full-width above columns)
- [x] Diagonal matrix A = kI shown as read-only `editable_matrix` (3×3)
- [x] 3D figure (unit cube scaled by k)
- [x] Determinant meter (volume + surface + ratio) — under the graph
- [x] Notice: k intro + surface-vs-volume + cells + elephant ears (full-width at bottom)
- [x] Ratio wording: "For every 1 unit of volume there are 6/k units of surface"
- [x] Math: det = k × k × k with current k substituted
- [x] Math: surface area = 6k²
- [x] Math: A · (3 cube corners) with `\small` and numeric `bmatrix(A)`
- [x] Triangular-matrix bridge sentence — references "Topic 5.5" (text fix applied)

### Example 4 — Graphics
- [x] Preset selectbox (Mirror / Shadow) with `set_matrix_state`
- [x] Editable A via `editable_matrix` widget + morph slider
- [x] Morph animates (rocket morphs via `At = interpolate(A, t)`)
- [x] Determinant meter uses live `det(At)` — under the graph
- [x] Closing line: "det = 0 means no inverse... Topic 4"
- [x] Math: both matrices shown as read-only `editable_matrix` (current At + destination A)
- [x] Math: `det At` with entries substituted + sign/collapse meaning
- [x] Math: At · (rocket vertices — nose, fin tip, window) with `{\small}` and numeric `bmatrix(At)` + "every other vertex" note

## Topic 4 — Inverse Transformations (`topics/t04_inverse/`)

**File structure:** `t04_inverse` is now a per-screen package:
- `__init__.py` — TITLE, SLUG, OVERVIEW, HOWTO, shared helpers (`_inv_meter`, `_mod_inv_matrix`), preset dicts (`_E1_PRESETS`, `_E3_PRESETS`), render() dispatcher
- `robotics.py` — Example 1
- `cryptography.py` — Example 2 (includes `_E2_KEYS`, `_prep_message`)
- `medical.py` — Example 3
- `business.py` — Example 4 (includes `_E4_PRESETS`)

- [x] Module exists and registered in `app.py` (imports as `topics.t04_inverse`)
- [x] OVERVIEW (Topic 3 cliffhanger callback)
- [x] HOWTO in collapsed expander
- [x] Four examples in correct order (Robotics, Cryptography, Medical, Business)
- [x] `_inv_meter` shared helper on every screen

### Layout refactor (all four screens)
- [x] Per-screen package split complete (robotics.py, cryptography.py, medical.py, business.py)
- [x] Controls in full-width band above the two columns
- [x] `editable_matrix` widget in use on Robotics, Medical, Business
- [x] "Show the math" expanders removed — math always visible in left column
- [x] `_inv_meter` placed under the graph in right column (Robotics, Medical, Business)
- [x] Notice/closing line full-width at bottom
- [x] Robotics: standard 0.5/0.5 layout, math left (with `{\small}`), figure + meter right
- [x] Medical: standard 0.5/0.5 layout, math left (with `{\small}`), figure + meter right
- [x] Cryptography: custom math-left / table-right layout (no graph; table + inverse meter in right column)
- [x] Business: custom 0.6/0.4 layout (5-step algebra in wide left column with `{\small}`, skinny graph + meter right); target solver stays as expander

### Example 1 — Robotics
- [x] Editable matrix + presets (Reachable / Singular)
- [x] There-and-back: Apply M / Undo with M⁻¹ radio + morph slider
- [x] Singular pose disables undo + warning
- [x] Desired hand target vector editor
- [x] Required input x = A⁻¹ · target + verify A·x = target
- [x] Notice
- [x] Math: A, A⁻¹, det, 1/det, recovered x, check (always shown, `{\small}`)

### Example 2 — Cryptography
- [x] Text input for message + cipher key selectbox (Key 1, Key 2, Broken)
- [x] Hill cipher mod 26 logic (encode + decode)
- [x] Table: plaintext / # / cipher # / ciphertext / decoded
- [x] Inverse meter (crypto variant): det, M⁻¹ mod 26, or "can't be undone" warning
- [x] Notice
- [x] Math: M, c = Mp, M⁻¹, p = M⁻¹c (always shown, `{\small}`)

### Example 3 — Medical imaging
- [x] Editable matrix + presets (Full data / Unstable / Singular)
- [x] There-and-back on rocket
- [x] Singular disables undo
- [x] Inverse meter (large 1/det visible for unstable preset)
- [x] Notice (Topic 10 forward-link)
- [x] Math: M, M⁻¹, det, instability note (always shown, `{\small}`)

### Example 4 — Business
- [x] Editable matrix + production vector editor + presets (Distinct / Proportional)
- [x] Resource point plotted on figure
- [x] 5-step algebra in left column (with `{\small}`)
  - [x] Step 1: forward general
  - [x] Step 2: forward with live numbers
  - [x] Step 3: inverse formula with det in denominator
  - [x] Step 4: inverse with live numbers
  - [x] Step 5: recover and verify round trip
- [x] Singular: 1/det = 1/0 undefined + caption
- [x] Optional target solver with negative-production note (in expander)
- [x] Inverse meter (under graph)
- [x] Notice (bridges to Topic 5)

## Topic 5 — Linear Systems (`topics/t05_systems/`)

**File structure:** `t05_systems` is now a per-screen package:
- `__init__.py` — TITLE, SLUG, OVERVIEW, HOWTO, preset dicts (`_E1_PRESETS`, `_E3_PRESETS`, `_E5_PRESETS`), `_PLANE_COLORS`, shared helpers (`_classify`, `_render_outcome`), render() dispatcher
- `example_one.py` — Example 1 (The three outcomes)
- `example_two.py` — Example 2 (Business / break-even)
- `example_three.py` — Example 3 (Engineering / metal mixing)
- `example_four.py` — Example 4 (Chemistry / balance a reaction)
- `example_five.py` — Example 5 (3D: three planes)

- [x] Module exists and registered in `app.py` (imports as `topics.t05_systems`)
- [x] OVERVIEW (Topic 4 callback + row/column picture intro)
- [x] HOWTO in collapsed expander
- [x] Five examples in correct order
- [x] `_classify` + `_render_outcome` shared helpers

### Layout refactor (all five screens)
- [x] Per-screen package split complete (example_one.py ... example_five.py)
- [x] Controls in full-width band above the columns
- [x] All "Show the math" expanders removed — math always visible
- [x] `editable_matrix` widget in use on Examples 1, 3, and 5 (the screens with a matrix)
- [x] Notice/closing content full-width at bottom
- [x] Example 1 (Three outcomes): **Option-A exception** — row picture and column picture side by side (`st.columns(2)`), outcome meter + blockquote + math all full-width below
- [x] Example 2 (Break-even): slider-driven, no matrix; 0.5/0.5 math-left / graph-right
- [x] Example 3 (Metal mixing): 0.5/0.5, `editable_matrix` 2x2, Ax=b in `{\small}`
- [x] Example 4 (Chemistry): slider-driven, no matrix; 0.5/0.5 math-left / bar-chart-right
- [x] Example 5 (3D planes): 0.5/0.5, `editable_matrix` 3x3, A/b/x in `{\small}`

### Example 1 — The three outcomes
- [x] `editable_matrix` + vector editor + 3 presets (One / None / Infinite)
- [x] Row picture (lines via `add_line_2d`) + column picture side by side
- [x] Intersection point marked when unique
- [x] Tip-to-tail path in column picture when unique
- [x] Notice (same system, two views)
- [x] Math always shown (full-width below figures)

### Example 2 — Business (break-even)
- [x] Three sliders (price, fixed cost, variable cost)
- [x] Revenue + cost lines on figure
- [x] Break-even point marked; no-break-even warning when price ≤ var cost
- [x] Notice
- [x] Math always shown: line equations + q* formula

### Example 3 — Engineering (metal mixing)
- [x] `editable_matrix` + target vector + 3 presets (Reachable / Unreachable / Redundant)
- [x] Column picture with alloy vectors + target + tip-to-tail path
- [x] Outcome readout in words ("Blend: ... units")
- [x] Notice
- [x] Math always shown (left column, `{\small}`)

### Example 4 — Chemistry (balance a reaction)
- [x] Three integer sliders (a, b, c)
- [x] Atom-balance bar chart (H and O, green when matched)
- [x] Balanced banner
- [x] Notice (ratio point: 2:1:2)
- [x] Math always shown: conservation equations + ratio

### Example 5 — 3D: three planes
- [x] `editable_matrix` (3x3) + target vector + 3 presets (Unique / Redundant / Impossible)
- [x] Three translucent planes via `add_plane_3d`
- [x] Solution point marked when unique
- [x] Outcome readout in words
- [x] Notice
- [x] Looking-ahead note (elimination / triangular form)
- [x] Math always shown (left column, `{\small}`)

### Shared helpers added to `engine/plotting.py`
- [x] `add_line_2d`
- [x] `new_figure_3d`
- [x] `add_plane_3d`

## Topic 5.5 — Elimination & Triangular Form (`t05b_elimination.py`)

**Layout refactor not yet applied** — wide augmented matrices (6x7 in Logistics) need a wider-math layout, not the standard 0.5/0.5 split. Exempted until a custom layout is designed.

- [x] Module exists and registered in `app.py`
- [x] OVERVIEW
- [x] HOWTO in collapsed expander
- [x] Three screens (Workbench, Logistics, Circuit)
- [x] `aug_array_latex` added to `engine/widgets.py`

### Outstanding work (next priorities)
- [~] **(a) Logistics row-order inversion** — warehouses first (rows 1-2), stores last (rows 3-6). Spec requires stores first (rows 1-4), warehouses last (rows 5-6), so the first two diagonal positions are zero and elimination *requires row swaps*. Current order has nonzero diagonal from the start, defeating the pedagogical point.
- [~] **(b) Circuit equation-development step** — spec requires a 3-step guided process: (1) student enters coefficients for each of 3 laws (KCL node, KVL left loop, KVL right loop) with per-equation Check / Hint / "Show this equation"; (2) student assembles the 3x4 augmented matrix; (3) reduce. Code only asks for R/V values with a pre-structured matrix, skipping the equation-building pedagogy.
- [ ] **(c) [A | I] inverse-by-elimination screen** — the Topic 4 <-> 5.5 bridge (specced separately, not yet built).
- [ ] **(d) Pivot highlighting in LaTeX** — pivots counted but not visually marked (spec: bold/colored pivots).

### Shared workbench
- [x] Equations displayed above augmented matrix (both update on every op)
- [x] Augmented matrix via `aug_array_latex`
- [x] Manual controls: Add multiple / Swap / Scale
- [x] Guided: "Do one step" (one standard forward-elimination op)
- [x] Guided: "Run to triangular form"
- [x] "Back-substitute & solve" (enabled once triangular with nonzero pivots)
- [x] Undo + Reset
- [x] Scenario detection: 0 = c (no solution), zero row (infinite), pivot count
- [x] Pivot count with quiet rank/Topic 6 seed

### Screen 1 — The workbench
- [x] 4 presets (One solution / Needs a row swap / Redundant / Contradiction)
- [x] Notice
- [x] Show the math (row operations + det = product of diagonal)

### Screen 2 — Logistics (6-variable shipping network)
- [x] Network diagram (plotly, nodes + labeled arrows + demands)
- [x] Editable 6x7 augmented grid
- [x] Check button (flags wrong rows without revealing answer)
- [x] "Fill it in for me" button
- [x] Workbench renders after correct/filled matrix
- [x] Solution labeled by route name (F->W1, etc.)
- [x] Notice

### Screen 3 — Circuit (3 currents)
- [x] Circuit diagram (plotly schematic with V, R1/R2/R3, I1/I2/I3 labeled)
- [x] Value fill-in (R1, R2, R3, V) with Check / "Fill it in for me"
- [x] Workbench renders after correct/filled values
- [x] Solution labeled as currents (I1, I2, I3 in amps)
- [x] Looking-ahead note (Topic 9 / AC / complex numbers)
- [x] Notice

---

## Topics not yet started

- [ ] 6 — Subspaces, Basis, Dimension
- [ ] 7 — Projection & Least Squares
- [ ] 8 — Eigenvalues & Eigenvectors
- [ ] 9 — Complex Numbers in LA
- [ ] 10 — Fourier Matrices (DFT)
- [ ] 11 — Linear Algebra in AI/ML (PCA & SVD)
