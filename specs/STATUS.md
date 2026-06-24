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

**NOT yet refactored:** Topics 2, 4, 5, and 5.5 still use the OLD layout (no two-column math/graph split, no `editable_matrix`, expanders still present). They are unchanged by this refactor.

---

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
- [x] "Try this" expander
- [x] Sample vector checkbox + vector editor (named x)
- [x] Reset button

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

## Topic 4 — Inverse Transformations (`t04_inverse.py`)

- [x] Module exists and registered in `app.py`
- [x] OVERVIEW (Topic 3 cliffhanger callback)
- [x] HOWTO in collapsed expander
- [x] Four examples in correct order (Robotics, Cryptography, Medical, Business)
- [x] `_inv_meter` shared helper on every screen

### Example 1 — Robotics
- [x] Matrix editor + presets (Reachable / Singular)
- [x] There-and-back: Apply M / Undo with M⁻¹ radio + morph slider
- [x] Singular pose disables undo + warning
- [x] Desired hand target vector editor
- [x] Required input x = A⁻¹ · target + verify A·x = target
- [x] Notice
- [x] Show the math: A, A⁻¹, det, 1/det, recovered x, check

### Example 2 — Cryptography
- [x] Text input for message + cipher key selectbox (Key 1, Key 2, Broken)
- [x] Hill cipher mod 26 logic (encode + decode)
- [x] Table: plaintext / # / cipher # / ciphertext / decoded
- [x] Inverse meter (crypto variant): det, M⁻¹ mod 26, or "can't be undone" warning
- [x] Notice
- [x] Show the math: block encoding/decoding with mod 26

### Example 3 — Medical imaging
- [x] Matrix editor + presets (Full data / Unstable / Singular)
- [x] There-and-back on rocket
- [x] Singular disables undo
- [x] Inverse meter (large 1/det visible for unstable preset)
- [x] Notice (Topic 10 forward-link)
- [x] Show the math: M, M⁻¹, det, instability note

### Example 4 — Business
- [x] Matrix editor + production vector editor + presets (Distinct / Proportional)
- [x] Resource point plotted on figure
- [x] 5-step algebra shown openly (not in expander)
  - [x] Step 1: forward general
  - [x] Step 2: forward with live numbers
  - [x] Step 3: inverse formula with det in denominator
  - [x] Step 4: inverse with live numbers
  - [x] Step 5: recover and verify round trip
- [x] Singular: 1/det = 1/0 undefined + caption
- [x] Optional target solver with negative-production note
- [x] Inverse meter
- [x] Notice (bridges to Topic 5)

## Topic 5 — Linear Systems (`t05_systems.py`)

- [x] Module exists and registered in `app.py`
- [x] OVERVIEW (Topic 4 callback + row/column picture intro)
- [x] HOWTO in collapsed expander
- [x] Five examples in correct order
- [x] `_classify` + `_render_outcome` shared helpers

### Example 1 — The three outcomes
- [x] Matrix editor + vector editor + 3 presets (One / None / Infinite)
- [x] Row picture (lines via `add_line_2d`) + column picture side by side
- [x] Intersection point marked when unique
- [x] Tip-to-tail path in column picture when unique
- [x] Notice (same system, two views)
- [x] Show the math

### Example 2 — Business (break-even)
- [x] Three sliders (price, fixed cost, variable cost)
- [x] Revenue + cost lines on figure
- [x] Break-even point marked; no-break-even warning when price ≤ var cost
- [x] Notice
- [x] Show the math: line equations + q* formula

### Example 3 — Engineering (metal mixing)
- [x] Matrix editor + target vector + 3 presets (Reachable / Unreachable / Redundant)
- [x] Column picture with alloy vectors + target + tip-to-tail path
- [x] Outcome readout in words ("Blend: ... units")
- [x] Notice
- [x] Show the math

### Example 4 — Chemistry (balance a reaction)
- [x] Three integer sliders (a, b, c)
- [x] Atom-balance bar chart (H and O, green when matched)
- [x] Balanced banner
- [x] Notice (ratio point: 2:1:2)
- [x] Show the math: conservation equations + ratio

### Example 5 — 3D: three planes
- [x] Matrix editor (3×3) + target vector + 3 presets (Unique / Redundant / Impossible)
- [x] Three translucent planes via `add_plane_3d`
- [x] Solution point marked when unique
- [x] Outcome readout in words
- [x] Notice
- [x] Looking-ahead note (elimination / triangular form)
- [x] Show the math

### Shared helpers added to `engine/plotting.py`
- [x] `add_line_2d`
- [x] `new_figure_3d`
- [x] `add_plane_3d`

## Topic 5.5 — Elimination & Triangular Form (`t05b_elimination.py`)

- [x] Module exists and registered in `app.py`
- [x] OVERVIEW
- [x] HOWTO in collapsed expander
- [x] Three screens (Workbench, Logistics, Circuit)
- [x] `aug_array_latex` added to `engine/widgets.py`

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
- [ ] Pivot highlighting in LaTeX (spec: bold/colored pivots) — pivots counted but not visually marked

### Screen 1 — The workbench
- [x] 4 presets (One solution / Needs a row swap / Redundant / Contradiction)
- [x] Notice
- [x] Show the math (row operations + det = product of diagonal)

### Screen 2 — Logistics (6-variable shipping network)
- [x] Network diagram (plotly, nodes + labeled arrows + demands)
- [x] Editable 6×7 augmented grid
- [x] Check button (flags wrong rows without revealing answer)
- [x] "Fill it in for me" button
- [x] Workbench renders after correct/filled matrix
- [x] Solution labeled by route name (F→W1, etc.)
- [x] Notice
- [~] **Row order is inverted** — warehouses first (rows 1-2), stores last (rows 3-6). Spec requires stores first (rows 1-4), warehouses last (rows 5-6), so the first two diagonal positions are zero and elimination *requires row swaps*. Current order has nonzero diagonal from the start, defeating the pedagogical point.

### Screen 3 — Circuit (3 currents)
- [x] Circuit diagram (plotly schematic with V, R1/R2/R3, I1/I2/I3 labeled)
- [x] Value fill-in (R1, R2, R3, V) with Check / "Fill it in for me"
- [x] Workbench renders after correct/filled values
- [x] Solution labeled as currents (I1, I2, I3 in amps)
- [x] Looking-ahead note (Topic 9 / AC / complex numbers)
- [x] Notice
- [~] **Equation-development step missing** — spec requires a 3-step guided process: (1) student enters coefficients for each of 3 laws (KCL node, KVL left loop, KVL right loop) with per-equation Check / Hint / "Show this equation"; (2) student assembles the 3x4 augmented matrix; (3) reduce. Code only asks for R/V values with a pre-structured matrix, skipping the equation-building pedagogy.

---

## Topics not yet started

- [ ] 6 — Subspaces, Basis, Dimension
- [ ] 7 — Projection & Least Squares
- [ ] 8 — Eigenvalues & Eigenvectors
- [ ] 9 — Complex Numbers in LA
- [ ] 10 — Fourier Matrices (DFT)
- [ ] 11 — Linear Algebra in AI/ML (PCA & SVD)
