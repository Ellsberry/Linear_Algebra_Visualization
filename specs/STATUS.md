# Topic Status Checklist

Tracks implementation against the specs in `specs/`. Updated manually as work lands.

Legend: [x] done · [~] partial · [ ] not started

---

## App-level navigation

- [x] Dark theme applied (`.streamlit/config.toml`: dark base, `#4dabf7` primary, `#0e1117` bg)
- [x] Topic selector replaced with a **3-column button grid** (full titles, active topic highlighted with `type="primary"`, scrolls with page — not sticky). Replaces the old sidebar nav and the interim top-of-page selectbox.
- [x] Plotting palette re-tuned for dark backgrounds (transparent bg, light font/axes, brighter data colors)
- [x] Graph heights reduced (2D ~420, 3D ~420) and Plotly margins tightened (`l=10,r=10,t=10,b=10`)
- [x] `editable_matrix` bracket widget added to `engine/widgets.py` (editable + read-only `editable=False` modes; flexbox-centered bracket glyphs)
- [x] `engine/layout.py` added (`two_col(ratio)` helper)

---

## Layout refactor + dark mode (app-wide)

All six topics are now refactored. Summary of what the refactor applied to each:
- Controls in a full-width band above the columns
- `st.columns([0.5, 0.5])` — math left, graph right (with per-topic exceptions noted below)
- "Show the math" expanders removed — math always visible
- `editable_matrix` widget in use where a matrix is shown

**NOT yet refactored:** none — Topics 1, 2, 3, 4, 5, and 5.5 are all done.

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

## Topic 5.5 — Elimination & Triangular Form (`topics/t05b_elimination/`)

**Spec:** `specs/topic5b_elimination.md`, `specs/topic5b_logistics_redesign.md`

**File structure:** `t05b_elimination` is now a per-screen package:
- `__init__.py` — TITLE, SLUG, OVERVIEW, HOWTO (as `st.caption`), render() dispatcher
- `workbench.py` — shared elimination engine (all row-op logic, state management, `workbench()` callable)
- `eq_parser.py` — equation parser + equivalence checker (`parse_equation`, `rows_equivalent`, `ParseError`; hardcoded `N_VARS=7`)
- `eq_builder.py` — shared equation-builder UI (`equation_builder(key, n_unknowns, target_aug, ...)`) — n-agnostic, proven at n=6 and n=7
- `screen_workbench.py` — Screen 1 (The workbench: presets, math block)
- `logistics_one.py` — Screen 2a (Logistics one plan: 6-route tree, unique solution)
- `logistics.py` — Screen 2b (Logistics many plans: 7-route cycle, infinitely many)
- `circuit.py` — Screen 3 (Circuit: fill-values, workbench reveal, Topic 9 pointer)

- [x] Module exists and registered in `app.py`
- [x] OVERVIEW
- [x] HOWTO rendered as `st.caption` (no expander)
- [x] Four screens — selector: "1 · The workbench / 2a · Logistics (one plan) / 2b · Logistics (many plans) / 3 · Circuit"
- [x] `aug_array_latex` in `engine/widgets.py`

### Layout refactor
- [x] Page-level "How to use this screen" expander removed; HOWTO now `st.caption` under OVERVIEW
- [x] Workbench screen: "Show the math" expander removed — math block always shown below workbench
- [x] Circuit screen: already expander-free; no change needed
- [x] Workbench engine's internal expanders ("All operations (N)", "Back-substitution steps") retained — these are legitimate in-workbench UI, not content wrappers

### Shared workbench engine
- [x] Equations displayed above augmented matrix (both update on every op)
- [x] Augmented matrix via `aug_array_latex`
- [x] Manual controls: Add multiple / Swap / Scale
- [x] Guided: "Do one step" (one standard forward-elimination op)
- [x] Guided: "Run to triangular form"
- [x] "Back-substitute & solve" (enabled once triangular with nonzero pivots)
- [x] Undo + Reset
- [x] Scenario detection: 0 = c (no solution), zero row (infinite), pivot count
- [x] Pivot count with quiet rank / Topic 6 seed
- [x] **Bug fix:** `_show_scenario` now checks `n_pivots < n_unknowns` before reporting "infinitely many solutions" on a zero row — previously fired a false positive for over-determined systems (7 equations / 6 unknowns) where a redundant row zeros out after full elimination even though rank = n_unknowns and the solution is unique

### Shared equation-builder (`eq_builder.py`)
- [x] `equation_builder(key, n_unknowns, target_aug, row_labels, diagram_fn, solution_labels, intro_md, reduce_caption, closing_md, builder_intro_md)` — renders the full flow for any n
- [x] Parameterized helpers: `_row_to_eq_str(row, n)`, `_row_to_latex(row, n)`, `_live_aug_latex(key, n, n_rows)`, `_assemble_from_builder(key, n, row_labels)`, `_node_balance_builder(key, n, row_labels, intro_md)`
- [x] Parameterized callbacks: `_check_cb(key, target_aug, row_labels)`, `_fill_cb(key, target_aug)` — wired via Streamlit `on_click` + `args`
- [x] **Bug fix:** `eq_parser.parse_equation` always returns a length-8 row (`N_VARS=7` hardcoded). For n=6, b is at `row[-1]` (index 7), not `row[n]` (index 6 = x₇ coefficient = 0). Fixed in `_row_to_latex`, `_live_aug_latex` (b reads), and `_check_cb` (condensed comparison: `list(parsed[:n]) + [parsed[-1]]` before `rows_equivalent`)
- [x] **Bug fix:** `_live_aug_latex` previously looped `range(n_unknowns)`, hiding the last row of over-determined systems (e.g. Store D on 2a). Added `n_rows` param; `equation_builder` passes `len(target_aug)`

### Screen 1 — The workbench
- [x] 4 presets (One solution / Needs a row swap / Redundant / Contradiction)
- [x] Notice
- [x] Math block always shown (elementary row operations + det = product of pivots + rank preview)

### Screen 2a — Logistics (one plan) — `logistics_one.py`

**Teaching role:** Introduces the equation-builder pattern on a simpler tree network where every store has exactly one incoming route. Elimination gives a unique answer — students see the method work cleanly before the harder case.

- [x] **6-route tree network** — B fed only by W1 (route x₄); no cycle. Routes: x₁ F→W1, x₂ F→W2, x₃ W1→A, x₄ W1→B, x₅ W2→C, x₆ W2→D. Demands: A=30, B=20, C=25, D=25 (total 100 = factory supply).
- [x] **Verified math:** 7 equations / 6 unknowns, rank=6 → unique solution x=(50,50,30,20,25,25). One redundant row zeros out after elimination (F-row is dependent); `_show_scenario` correctly falls through to "Ready to back-substitute."
- [x] **Diagram** (`_logistics_one_diagram`): B placed under W1's side with a single incoming arrow — visually contrasts with 2b where B has two incoming arrows.
- [x] **Powered by `equation_builder`** with `key="t05b_e2a"`, `n_unknowns=6`. All state keys prefixed `t05b_e2a_*`, fully isolated from 2b's `t05b_e2_*` keys.
- [x] **Closing text:** "One definite plan" — every route pinned; explains that adding a second route to B (the next screen) changes this completely.

### Screen 2b — Logistics (many plans) — `logistics.py` (REDESIGNED)

**Teaching role:** Same network as 2a plus one extra route (W2→B = x₅). That single edge creates a cycle and changes the solution from one plan to a whole family. The teaching arc: 2a gives the endpoints (x₄=20,x₅=0) and (x₄=0,x₅=20); 2b's free parameter slides between them.

- [x] **7-route cycle network** — B fed by BOTH W1 (x₄) and W2 (x₅). Routes: x₁–x₇ as before. Same demands. 7 equations / 7 unknowns.
- [x] **Verified math:** rank(A)=6, rank([A|b])=6 → one free variable → infinitely many valid plans. Free parameter t = x₅ (freight to B via W2), 0 ≤ t ≤ 20; general solution x₁=50−t, x₂=50+t, x₃=30, x₄=20−t, x₅=t, x₆=25, x₇=25.
- [x] **Strict sign convention:** in=+1, out=−1, RHS=net supply/demand. F row: −x₁−x₂=−100.
- [x] **`eq_parser.py`:** `parse_equation(s)` → `[a1..a7, b]` (Fractions); `rows_equivalent` accepts any nonzero scalar multiple. `ParseError` for bad input.
- [x] **Powered by `equation_builder`** with `key="t05b_e2"`, `n_unknowns=7`. Equation boxes keyed `t05b_e2_eq__{i}`.
- [x] **Live [A|b]** always visible as student types; faint dash rows for blank/unparseable equations.
- [x] **Check / Fill it in for me** — check distinguishes "couldn't read" from "wrong".
- [x] **Workbench** (`workbench("t05b_e2", 7, ...)`) — engine detects free-variable outcome correctly.
- [x] **Closing text:** explains the free variable as the B-delivery split and why a real logistics network needs the math (a family of plans, business picks the cheapest).

### Screen 3 — Circuit (3 currents)
- [x] Circuit diagram (plotly schematic with V, R1/R2/R3, I1/I2/I3 labeled)
- [x] Value fill-in (R1, R2, R3, V) with Check / "Fill it in for me"
- [x] Workbench renders after correct/filled values
- [x] Solution labeled as currents (I₁, I₂, I₃ in amps)
- [x] Looking-ahead note (Topic 9 / AC / complex numbers)
- [x] Notice

### Outstanding work (future design + build)

- [ ] **(a) Circuit redesign** — the current Circuit screen (3) asks the student to fill in R/V values against a pre-structured matrix. The goal is a richer experience: a more complex diagram, and the student derives the KCL/KVL equations themselves via the shared `equation_builder` (same pattern as Logistics). Needs its own design session to settle the network topology, exact equations, and closing text before coding.
- [ ] **(b) [A | I] inverse-by-elimination screen** — the Topic 4 ↔ 5.5 bridge: extend the workbench to full reduced row echelon form applied to [A | I] to produce A⁻¹. Specced separately, not yet built.
- [ ] **(c) Pivot highlighting in LaTeX** — pivots counted but not visually marked (spec: bold/colored pivots in the augmented-matrix display). Minor; pending.

---

## Topics not yet started

- [ ] 6 — Subspaces, Basis, Dimension
- [ ] 7 — Projection & Least Squares
- [ ] 8 — Eigenvalues & Eigenvectors
- [ ] 9 — Complex Numbers in LA
- [ ] 10 — Fourier Matrices (DFT)
- [ ] 11 — Linear Algebra in AI/ML (PCA & SVD)
