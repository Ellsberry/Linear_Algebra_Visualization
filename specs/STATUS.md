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

## Topic 0 — Matrix Operations & Multiplication (`topics/t00_matmul/`)

**Spec:** `specs/topic00_matrix_multiplication.md`

**Status:** NEW standalone topic, built BEFORE Topic 1 in the learnable order.

- [x] Registered **first** in `app.py`'s `TOPICS` list (imports as `topics.t00_matmul`, `TITLE = "0 · Matrix multiplication"`)
- [x] Module structure: `__init__.py` (OVERVIEW + screen dispatch, screen order "0 · Operations" then "1 · The rule (2x2)"), `screen_ops.py` (Screen 0), `screen_2x2.py` (Screen 1)

### Screen 0 — Operations Overview (COMPLETE)
- [x] All 7 operations described (Addition, Subtraction, Scalar Multiplication, Matrix Multiplication, Transpose, Inverse, Division), each with What it is / Why it matters / real-world example bullets (expanded to short explanatory clauses, not bare labels)
- [x] Inline PRACTICE for Addition, Subtraction, Scalar Multiplication — 3 verified 2×2 examples each, shown 3-across, `compact=True` read-only operands + editable answer, per-cell Check + Show solution (shared `_check_and_solve` helper)
- [x] Inline PRACTICE for Transpose — single verified 4×4 example (`A` read-only, `A^T` editable answer), confirming `editable_matrix`'s compact path is dim-generic (works identically at dim=4, not just dim=2)
- [x] Matrix Multiplication, Inverse, Division are description-only (per spec), each with a pointer caption to where they're covered ("Practiced on Screens 1-3." / "see Topics 4 and 5.5." / "Described only.")

### Screen 1 — Rules + four 2×2 · 2×2 (COMPLETE)
- [x] Rule text (row·column rule) + shape rule (2×2 · 2×2 → 2×2) at top
- [x] Four verified practice examples, inputs 3–9 (one zero, in Ex2 only, per spec)
- [x] All four shown at once — no radio/selector — arranged in a 2×2 grid (`st.columns(2)` pairs, top row Ex1/Ex2, bottom row Ex3/Ex4)
- [x] Each example: A, B read-only + editable answer matrix in narrow side-by-side columns (reads "A · B = answer"), unique `state_key` per example
- [x] Per-example Check (per-cell, flags wrong `(row, col)` without revealing values) + Show solution

### `editable_matrix` (`engine/widgets.py`) — new `compact` path
- [x] Added optional `compact: bool = False` parameter (default unchanged — every existing caller, e.g. t02/t03/t04/t05, is unaffected)
- [x] `compact=True, editable=False` — read-only rows render as a single tight flex line (no per-cell column gutters)
- [x] `compact=True, editable=True` — tight cell grid; bracket rendered as a CSS border (`border-left`/`border-right` + four absolutely-positioned corner ticks) on the single container that is the immediate parent of the cell grid, so the bracket height always equals the actual rendered cell content — no fixed/guessed height, no overhang
- [x] Confirmed dim-generic, not just 2×2: Screen 0's Transpose practice exercises the same compact-editable code path at dim=4

### T00 remaining (not started)
- [ ] Screen 2 — four 3×3 · 3×3 practice examples (same pattern as Screen 1)
- [ ] Screen 3 — rectangular multiplication + shape rule + non-conformable rejection message. **Needs `editable_matrix` extended for non-square (rows ≠ cols)** — decide at build time (e.g. a `cols` param, or a new `editable_matrix_rect`); keep existing square callers unchanged
- [ ] Screen 4 — Special matrices (identity, upper-triangular, RREF) — definitions + why + example, not practice

### Related cleanup
- [x] Removed the stray top-level `topics/t05b_elimination.py` module that shadowed the real `topics/t05b_elimination/` package (superseded; package version is authoritative)

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
- `workbench.py` — shared elimination engine (all row-op logic, state management, `workbench()` callable); includes `_active_pivot_tri` for pivot highlighting
- `eq_parser.py` — numeric parser for Logistics (x-variables, N_VARS=7; `parse_equation`, `rows_equivalent`, `ParseError`)
- `eq_builder.py` — shared equation-builder UI (`equation_builder(key, n_unknowns, target_aug, ...)`) — n-agnostic, parser-agnostic; powers three screens with two parsers
- `circuit_parser.py` — symbolic parser for Circuit (I-variables + R/V symbol table; N_VARS=5)
- `rref_reducer.py` — dedicated Gauss-Jordan RREF reducer for [A|I] inversion (`make_augmented`, `compute_one_step`, `run_to_reduced`, `op_*`); uses Fraction; pure logic, no Streamlit; built and unit-tested before wiring
- `screen_workbench.py` — Screen 1 (The workbench: presets, math block)
- `logistics_one.py` — Screen 2a (Logistics one plan: 6-route tree, unique solution)
- `logistics.py` — Screen 2b (Logistics many plans: 7-route cycle, infinitely many)
- `circuit.py` — Screen 3 (Circuit: KCL/KVL symbolic equations, 5 currents, unique solution)
- `inverse_elim.py` — Screen 4 ([A|I] inverse-by-elimination; spec: `specs/topic5b_inverse_elimination.md`)

- [x] Module exists and registered in `app.py`
- [x] OVERVIEW
- [x] HOWTO rendered as `st.caption` (no expander)
- [x] Five screens — selector: "1 · The workbench / 2a · Logistics (one plan) / 2b · Logistics (many plans) / 3 · Circuit / 4 · Inverse by elimination"
- [x] `aug_array_latex` in `engine/widgets.py` — optional `highlight=(row,col)` arg (defaults `None`; existing callers unaffected)

### Layout refactor
- [x] Page-level "How to use this screen" expander removed; HOWTO now `st.caption` under OVERVIEW
- [x] Workbench screen: "Show the math" expander removed — math block always shown below workbench
- [x] Circuit screen: already expander-free; no change needed
- [x] Workbench engine's internal expanders ("All operations (N)", "Back-substitution steps") retained — these are legitimate in-workbench UI, not content wrappers

### Shared workbench engine
- [x] Equations displayed above augmented matrix (both update on every op)
- [x] Augmented matrix via `aug_array_latex` — with active-pivot highlight (`_active_pivot_tri` in `workbench.py`; highlight advances column by column as elimination proceeds)
- [x] Manual controls: Add multiple / Swap / Scale
- [x] Guided: "Do one step" (one standard forward-elimination op)
- [x] Guided: "Run to triangular form"
- [x] "Back-substitute & solve" (enabled once triangular with nonzero pivots)
- [x] Undo + Reset
- [x] Scenario detection: 0 = c (no solution), zero row (infinite), pivot count
- [x] Pivot count with quiet rank / Topic 6 seed
- [x] **Bug fix:** `_show_scenario` now checks `n_pivots < n_unknowns` before reporting "infinitely many solutions" on a zero row — previously fired a false positive for over-determined systems (7 equations / 6 unknowns) where a redundant row zeros out after full elimination even though rank = n_unknowns and the solution is unique

### Shared equation-builder (`eq_builder.py`) — fully parameterized
- [x] `equation_builder(key, n_unknowns, target_aug, row_labels, diagram_fn, solution_labels, intro_md, reduce_caption, closing_md, builder_intro_md, parse_fn, equiv_fn, fill_equations, placeholder)` — renders the full flow for any n with any parser
- [x] **`parse_fn` / `equiv_fn`** — parser and equivalence checker; default to the numeric `eq_parser` functions so Logistics 2a/2b are unchanged. Circuit passes `circuit_parser.parse_circuit_equation` / `rows_equivalent`.
- [x] **`fill_equations`** — optional list of correct equation strings (one per row) for "Fill it in for me". When `None`, falls back to auto-generated x-variable numeric strings (Logistics path). Circuit passes the five symbolic strings so Fill produces text the symbolic parser can read.
- [x] **`placeholder`** — optional text-box hint; defaults to `"e.g. x1 - x3 - x4 = 0"`. Circuit passes `"e.g. R1*I1 + R3*I3 = V"`.
- [x] All helpers accept `parse_fn` as a parameter; all `except ParseError` clauses changed to `except Exception` so any parser's error class is caught cleanly.
- [x] Powers three screens with two parsers: Logistics 2a (numeric, n=6), Logistics 2b (numeric, n=7), Circuit (symbolic, n=5).
- [x] **Bug fix:** `eq_parser.parse_equation` always returns length-8 rows (`N_VARS=7`). For n=6, b is at `row[-1]` not `row[n]`. Fixed in `_row_to_latex`, `_live_aug_latex`, and `_check_cb`.
- [x] **Bug fix:** `_live_aug_latex` previously looped `range(n_unknowns)`, hiding rows of over-determined systems. Added `n_rows` param; `equation_builder` passes `len(target_aug)`.
- [x] **Bug fix:** Fill always wrote x-variable numeric strings; symbolic parser could not read them, producing "(couldn't read)" on Circuit. Fixed via `fill_equations` param.

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

### Screen 3 — Circuit (redesigned — complete, no polish pending)

**Spec:** `specs/topic5b_circuit_redesign.md`

Student writes the five circuit equations themselves (2 KCL + 3 KVL, symbolic form e.g. `R1*I1 + R3*I3 = V`) and sees them assembled into [A|b], then eliminates.

**Verified circuit:** V=36 V; R1=2 Ω (series), R2=6 Ω, R3=8 Ω (motor), R4=4 Ω (lightbulb), R5=12 Ω; five branch currents I1..I5; two nodes P, Q; three marked directional loops. Unique solution **I = (6, 2, 3, 3, 1) A** (clean integers). Matrix is not pre-triangular — 4 below-diagonal nonzeros — so elimination does real work.

- [x] **`circuit_parser.py`** — symbolic parser: knows `{R1:2, R2:6, R3:8, R4:4, R5:12, V:36}`, substitutes values, accepts any rearranged/rescaled form, rejects wrong resistors or signs. Built and unit-tested (all cases pass) before wiring into the screen.
- [x] **Compact Plotly diagram** — xrange [-0.5, 8], yrange [0, 9], height=420, `scaleanchor="x"` for round motor/lamp circles. Resistor boxes (R1, R2, R5), motor circle (M), lightbulb circle (X), labeled nodes P/Q, three directional loop markers, five current-direction arrows with size-16 subscript labels. No polish pending.
- [x] **Symbolic equation boxes** — placeholder `"e.g. R1*I1 + R3*I3 = V"` (circuit-specific). Live [A|b] substitutes symbol values as student types.
- [x] **Check / Fill it in for me** — Check validates against `_E3_AUG` via `circuit_parser.rows_equivalent`; Fill writes the five correct symbolic strings (parseable by the circuit parser).
- [x] **Workbench** (`workbench("t05b_e3", 5, ...)`) — reduces to unique solution I = (6, 2, 3, 3, 1) A.
- [x] **Closing text:** "One definite answer" with solution; Topic 9 AC-circuit forward-link.
- [x] Powered by `equation_builder` with `parse_fn=parse_circuit_equation`, `equiv_fn=rows_equivalent`, `fill_equations=[...]`, `placeholder="e.g. R1*I1 + R3*I3 = V"`.

### Screen 4 — Inverse [A|I] — `inverse_elim.py` (COMPLETE)

**Spec:** `specs/topic5b_inverse_elimination.md`

The Topic 4 ↔ 5.5 bridge: augment A with the identity to form [A | I], row-reduce all the way to RREF (Gauss-Jordan — zeros below AND above diagonal, pivots scaled to 1) until the left block is I, and the right block is A⁻¹.

- [x] **`rref_reducer.py`** — dedicated Gauss-Jordan RREF reducer, separate from the triangular `workbench` so the four existing screens are untouched. Eliminates above and below each pivot; scales pivots to 1. Uses `Fraction` for exact arithmetic (fractional inverses display as 1/2, -1/4, not decimals). Clean step-description formatting (no nested "1/5/2" strings; `_fmt_factor` handles reciprocals of fractions). Built and unit-tested before wiring.
- [x] **Three verified examples:**
  - Integer inverse: A=[[2,1,1],[1,3,2],[1,0,0]], A⁻¹=[[0,0,1],[-2,1,3],[3,-1,-5]] (det=-1; no fractions in answer).
  - Fractional inverse: A=[[2,0,0],[1,2,0],[1,1,2]], A⁻¹=[[1/2,0,0],[-1/4,1/2,0],[-1/8,-1/4,1/2]] (det=8; exact fractions via `Fraction`).
  - Singular: A=[[1,2,3],[2,4,6],[1,0,1]] (det=0; reduction detects no pivot → "A has no inverse" warning, no false answer).
- [x] **Guided reduction:** "Do one step" (one Gauss-Jordan op) and "Run to reduced form" (full RREF in one click).
- [x] **Manual row-op controls:** swap / scale / add-multiple with fraction-parsable text inputs (student types `1/2`, `-3/4`); factor parsed via `Fraction`; bad input shows a gentle caption and does not apply.
- [x] **Undo / Reset** — same state pattern as the triangular workbench.
- [x] **Singular detection:** banner "A is singular — the left block can't become the identity, so A has no inverse." Controls disabled once singular.
- [x] **Completion payoff** (full-width below columns when left block is I):
  - "Why the right side becomes A⁻¹" insight paragraph.
  - Boxed inverse: `A⁻¹ = ...` as LaTeX bmatrix with exact Fraction entries.
  - A·A⁻¹ = I verification rendered as LaTeX (computed with Fraction arithmetic; confirms the inverse is exact).
- [x] **Active-pivot highlighting:** `_active_pivot(M, n)` finds the first diagonal position not yet fully reduced (pivot ≠ 1 or column not fully cleared); highlighted entry rendered in accent blue bold. No highlight when done or singular.
- [x] **Wide-math layout** (`st.columns([1, 1.3])`): controls narrow-left, 3×6 matrix wide-right (LaTeX `{ccc|ccc}` divider). Matches workbench column split.
- [x] **Wired into selector** as "4 · Inverse by elimination" in `__init__.py` radio.

### Future hook (not Topic 5.5 work)

- **AC-circuit revisit (Topic 9)** — the same circuit topology reused with complex impedances; same 5 equations, complex solution. `circuit_parser.py` and the Plotly diagram are kept clean for this future hook.

---

## Core curriculum status

**Topics 1–5 and 5.5 are FULLY COMPLETE** — all refactored to the dark-mode layout, all screens built and verified, all engines shared and tested. The core curriculum (vectors → transformations → determinant → inverse → linear systems → elimination & inversion) is done.

---

## Topics not yet started

- [ ] 6 — Subspaces, Basis, Dimension
- [ ] 7 — Projection & Least Squares
- [ ] 8 — Eigenvalues & Eigenvectors
- [ ] 9 — Complex Numbers in LA (AC-circuit screen reuses Topic 5.5 Circuit topology + `circuit_parser` with complex impedances)
- [ ] 10 — Fourier Matrices (DFT)
- [ ] 11 — Linear Algebra in AI/ML (PCA & SVD)
