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

## Topic 0 — Matrix Operations & Multiplication (`topics/t00_matmul/`) — COMPLETE

**Spec:** `specs/topic00_matrix_multiplication.md`

**Status:** NEW standalone topic, built BEFORE Topic 1 in the learnable order.
All 5 screens built and working.

- [x] Registered **first** in `app.py`'s `TOPICS` list (imports as `topics.t00_matmul`, `TITLE = "0 · Matrix multiplication"`)
- [x] Module structure: `__init__.py` (OVERVIEW + screen dispatch, screen order "0 · Operations", "1 · Multiply 2x2", "2 · Multiply 3x3", "3 · Rectangular", "4 · Special matrices"), `screen_ops.py` (Screen 0), `screen_2x2.py` (Screen 1), `screen_3x3.py` (Screen 2), `screen_rect.py` (Screen 3), `screen_special.py` (Screen 4)

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
- [x] Per-example Check (per-cell, flags wrong `(row, col)` without revealing values) + Show solution, via the reveal-flag pattern (Show solution sets a `{ans_key}_reveal` flag + reruns; the actual write happens at the top of the render, before that run's answer widgets are instantiated — avoids the `StreamlitAPIException` from writing a widget's session_state key after it's already been created this run)

### Screen 2 — four 3×3 · 3×3 (COMPLETE)
- [x] Mirrors Screen 1 exactly at dim=3 (four verified practice examples, 2×2 grid arrangement, same reveal-flag Check/Show solution pattern, unique `t00_3x3_ex*` state keys)
- [x] Fixed a real dim>2 bug found here: the read-only compact path's per-row `st.columns([0.07, 1, 0.07])` call, nested 3 Streamlit-column-levels deep inside a loop, produced phantom duplicate "0.00" rows once the loop ran 3+ times (fine at dim=2, broken at dim=3+). Fixed by rendering each row as a single flex `<div>` (one `st.markdown()` call, no nested `st.columns`) instead — see `editable_matrix` entry below

### Screen 3 — Rectangular multiplication (COMPLETE)
- [x] Shape rule stated (A(m×n)·B(p×q) needs n=p; result is m×q)
- [x] Three verified practice examples at genuinely different shapes: 2×3·3×2=2×2, 5×3·3×2=5×2, 3×3·3×1=3×1 — each using `editable_matrix(..., rows=, cols=)` (the new non-square support) for A, B, and the answer independently
- [x] Fourth block: non-conformable pair (2×2 vs 3×3) rejected with a message instead of an answer grid, no Check button
- [x] Required extending `editable_matrix` to non-square shapes (done — see below) and fixing `set_matrix_state`, which assumed square (`M.shape[0]` for both loop bounds) and would have mis-written non-square Show-solution reveals (e.g. the 5×2 and 3×1 results here)

### Screen 4 — Special matrices (COMPLETE)
- [x] Exposition only, no practice, no widget changes: Identity (definition + why + 3×3 example with a live `I · A = A` demo), Upper-triangular (definition + why + `[[2,3,1],[0,4,2],[0,0,5]]` example), RREF (definition + why + `[[1,0,2],[0,1,3],[0,0,0]]` example contrasted with a NOT-RREF example of the same shape)

### `editable_matrix` (`engine/widgets.py`) — `compact` path + non-square support
- [x] Added optional `compact: bool = False` parameter (default unchanged — every existing caller, e.g. t02/t03/t04/t05, is unaffected)
- [x] `compact=True, editable=False` — read-only rows render as a single tight flex `<div>` per row (no nested `st.columns` at all — fixes the dim=3+ phantom-row bug found on Screen 2)
- [x] `compact=True, editable=True` — tight cell grid; bracket rendered as a CSS border (`border-left`/`border-right` + four absolutely-positioned corner ticks) on the single container that is the immediate parent of the cell grid, so the bracket height always equals the actual rendered cell content — no fixed/guessed height, no overhang
- [x] Confirmed dim-generic square case at dim=4 (Screen 0's Transpose practice) before non-square support existed
- [x] Added optional `rows`/`cols` params for non-square matrices (`dim` is now optional and used as the fallback for both when `rows`/`cols` are omitted) — every rendering branch (compact read-only, compact editable, and the original non-compact default path) uses `nrows`/`ncols` throughout. **Non-compact callers (t02/t03/t04/t05) are completely unaffected** — they only ever pass `dim`, so `rows`/`cols` fall back to it and behavior is identical to before
- [x] `set_matrix_state` fixed alongside this to use both dimensions of `M.shape` (was `M.shape[0]` for both loop bounds, silently assuming square) — needed so Show solution writes correctly for non-square results (Screen 3)

### Related cleanup
- [x] Removed the stray top-level `topics/t05b_elimination.py` module that shadowed the real `topics/t05b_elimination/` package (superseded; package version is authoritative)

### Screens 5-7 -- Three views of multiplication (BUILT; Screen 7 practice layout pending)

**Spec:** `specs/topic00_multiplication_views.md` (scoped addition -- Screens 5-7
only; does not modify Screens 0-4).

- [x] Screen 5 -- Row picture (`screen_rows.py`): rows of C are combinations of rows
      of B. Worked Ex 1 (general mix) + Ex 2 (permutation) + Ex 3 (elimination step),
      each with its own 3-row highlight selector. Practice redesigned: A·B=C top row
      with touch-tracked live-fill C (blank-until-touched, real 0 shows as 0),
      per-row work stacked, per-row Check / Show solution.
- [x] Screen 6 -- Column picture (`screen_cols.py`): columns of C are combinations of
      columns of A. Worked Ex 1 (general mix, result as vertical bmatrix) + Ex 2
      (column permutation) + Ex 3 (diagonal scale), each with its own 3-column
      highlight selector. Practice redesigned: A·B=C top row with touch-tracked
      live-fill C (blank-until-touched, real 0 shows as 0), per-column work side by
      side, per-column Check / Show solution.
- [~] Screen 7 -- Outer products (`screen_outer.py`): AB = sum of (col of A)(row of B).
      Worked example (Term 1/2/3/Sum selector) + 3 practice examples building each
      term then the sum -- BUILT and registered, but practice layout NOT yet
      redesigned to match Screens 5/6 (still original stacked layout); pending review.
- [x] Selector in `__init__.py`: "5 · Row picture", "6 · Column picture",
      "7 · Outer products" after "4 · Special matrices".
- [x] Shared worked example A(2x3)*B(3x2) = C(2x2) = [[13,16],[7,11]] on all three;
      same three practice A/B pairs across all screens.

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

### Layout refactor (all three screens)
- [x] Per-screen package split complete (example_one.py, example_two.py, example_three.py)
- [x] Controls in full-width band above the two columns
- [x] `st.columns([0.5, 0.5])` — math left, graph right
- [x] All "Show the math" expanders removed — math always visible in left column
- [x] Notice/closing content full-width at bottom

### Reworked — smoothie-focused redesign (all three screens rebuilt)
- [x] Shared constant `PEANUT` changed from (4, 1) to (8, 2) in `__init__.py` (ratio unchanged — still the 4:1 protein:sugar direction, just double the magnitude per scoop)
- [x] **Screen 1 (One ingredient):** banana ⇄ peanut-butter toggle (`st.radio`) drives a single set of inputs — the slider, arrow, live math, and text all follow whichever ingredient is selected. New "Show the span line" checkbox draws a faint line through the origin along the active ingredient's direction. Basis/span text always shown below the math: "one ingredient spans only a line," reachable points are `c·(1,4)` or `c·(8,2)`, with (14, 11) called out as unreachable by either ingredient alone. Old preset dropdown (More scoops / Half a scoop / Read the recipe) removed — superseded by the toggle + always-shown span text.
- [x] **Screen 2 (Two ingredients, added):** old free-vector presets (Tip-to-tail / Same direction / Opposite directions) removed. Two scalar sliders now scale the fixed BANANA/PEANUT constants directly — c1 (scoops of banana, default 3) and c2 (scoops of peanut butter, default 1) — matching the worked example `3·(1,4) + 1·(8,2) = (11,14)`. Tip-to-tail / Parallelogram view toggle kept (both constructions land on the same resultant). Live math shows `c1·banana + c2·PB = resultant`; a per-axis basis/span paragraph reads off protein/sugar sums and notes the resultant is off banana's line alone.
- [x] **Screen 3 (The smoothie mixer):** fixed target (14, 11); two scalar sliders (c1 = scoops banana, c2 = scoops peanut butter) default to the exact solution (2, 1.5). New "Allow negative scoops" checkbox (default off): OFF shows only the non-negative reachable wedge (the cone between the two vectors) shaded and floors both sliders at 0; ON floors sliders at −5 and shades the whole plane. Text adapts to match ("Real smoothies use non-negative scoops... reaches the wedge" vs. the basis/span sentence, which stays present either way). Kept: the two scalar target equations (Protein: 1c1 + 8c2 = 14, Sugar: 4c1 + 2c2 = 11), the det = −30 independence/basis explanation, the exact-solution check, and the target star + moving "your smoothie" point. Old preset dropdown, DEFINITION callout, Challenge, Reality check, and Ax=b-preview blocks all removed — superseded by this simplified design.
- [x] **Basis and span are now shown in numbers and words on all three screens** — Screen 1 shows a single ingredient's span as a line (with the span-line visual), Screen 2 shows a specific combination landing off that line, and Screen 3 shows the full basis payoff (determinant, uniqueness, wedge-vs-plane) with a live toggle between the "real" non-negative case and the full mathematical span.

**Note:** Topic 1 uses hardcoded light-mode plot colors (e.g. "darkorange", "crimson", "navy", "sienna", "gold") unlike Topics 2-4 which use the engine's dark-palette constants. May need a color-tune follow-up if anything looks dim on dark backgrounds.

## Topic 2 — Linear Transformations (`topics/t02_transformations/`) — COMPLETE (2 screens)

**Spec:** rework done via chat; no standalone spec file (unlike Topics 1, 5.5).

**File structure:** per-screen package, matching the pattern used by Topics 0, 1, 3, 4, 5, 5.5:
- `__init__.py` — TITLE, SLUG, INTRO, top-level "Example" radio (2D / 3D), dispatches to `_render_2d()` / `_render_3d()`
- `screen_2d.py` — Screen 1 (2D: parallelogram / rocket) — `_NOTICE`, `PRESET_NAMES`, `_PRESET_MATRICES`, `CORNERS`, `VIEW`, `ROCKET_POINTS`, `ROCKET_LABELS`, `_corner_latex`, `_render_2d()`
- `screen_3d.py` — Screen 2 (3D: cube) — `GOAL`, `V1`..`V8`/`VERTICES`, `FACES`, `FACE_COLORS`, `EDGES`, `VIEW_3D`, `PRESET_NAMES_3D`, `_PRESET_MATRICES_3D`, `_vertex_latex`, `_add_wireframe`, `_add_solid_faces`, `_render_3d()`

- [x] Module exists and registered in `app.py` (imports as `topics.t02_transformations`)
- [x] Ax = b intro with vertex/vector definitions (kept from the original rework; still points at "a corner of the parallelogram")
- [x] Restructured from a single-screen package into a 2-screen package: `__init__.py` now holds only TITLE/SLUG/INTRO + the selector/dispatch; both screens' bodies moved out verbatim into `screen_2d.py`/`screen_3d.py`

### Screen 1 — 2D (parallelogram / rocket) — `screen_2d.py`
- [x] Object: asymmetric parallelogram, corners (−3,−2), (4,−1), (3,4), (−4,3) — one per quadrant, no 0s/1s so no corner reads as a basis vector
- [x] Object toggle: parallelogram ↔ rocket (`st.radio`), reusing `engine.plotting`'s existing `_ROCKET` outline scaled ×3 so it spans all four quadrants like the parallelogram
- [x] Preset buttons (3-per-row grid): Identity, Shear, Rotation 45°, Reflection, Scale ×2, Non-uniform scale, General warp, Collapse (singular), Custom — tracked via `st.session_state["t02_preset"]`; Custom reveals four compact `st.number_input` cells (not the bracket widget)
- [x] Matrix A shown beside the buttons (`A = ` LaTeX + "columns = where î, ĵ land" + î/ĵ columns line)
- [x] Per-corner A·x=b math beside the graph — when Rocket is selected, four representative rocket vertices (nose, right fin tip, left fin tip, base) are labeled and shown instead of the four parallelogram corners
- [x] Before (faint, transparent fill, muted gray outline) / after (bold, semi-transparent orange fill, solid orange outline) shapes, matching legend entries — same `shade_polygon` calls drive both the parallelogram and the rocket
- [x] Determinant text + preset notice
- [x] No sliders anywhere on this screen (the old morph slider is gone — see "Removed" below)

### Screen 2 — 3D (cube) — `screen_3d.py`
- [x] Object: origin-centered cube, vertices (±2, ±2, ±2) — went through two intermediate shapes during development (tetrahedron → asymmetric hexahedron) before settling here per explicit request
- [x] 6 quad faces (standard cube topology: bottom/top/front/right/back/left), each a distinct solid color, fully opaque (`opacity=1.0`)
- [x] The original (untransformed) cube is drawn as a bright white wireframe overlay (12 edges, one `Scatter3d` "lines" trace) added AFTER the solid transformed faces, so the outline sits on top of them for direct before/after comparison
- [x] Preset buttons mirror Screen 1's layout, with verified 3D matrices: Identity, Scale ×2 (=2I, det=8), Non-uniform scale (diag(2,1,0.5), det=1), Shear (xy) (det=1), Rotation 90° z (det=1), Reflection z (det=−1), Collapse (singular, det=0), Custom (compact 3×3 `editable_matrix`, 9 cells)
- [x] Goal description + live 8-vertex list at the top, generated directly from the `VERTICES` array (can't drift out of sync with the geometry)
- [x] Matrix A 3×3 LaTeX display + "columns = where the basis vectors land" caption
- [x] 3-vertex (v1, v2, v3) A·x=b corner math, with a note that the other five vertices transform the same way
- [x] Determinant text: |det| = volume scale factor; sign = orientation flip; det=0 collapses the solid to a flat plane
- [x] Layout mirrors Screen 1: preset buttons + Matrix A in a top band; vertex math + determinant + meaning on the left, graph on the right, both starting at the same height

### Removed from Topic 2 (across both screens)
- [x] The morph slider (`t02_t`) and all `interpolate`/morph logic — both screens are static, no animation
- [x] The big `editable_matrix` widget from the pre-rework version (Screen 1 hand-rolls four compact number_inputs; Screen 2 uses `editable_matrix(..., compact=True)` only for its 9-cell Custom entry)
- [x] î/ĵ basis-vector arrows on the graph — both screens show only the object itself, no basis-vector legend entries
- [x] The old unit-square/unit-cube framing — replaced by the asymmetric parallelogram/rocket (Screen 1) and the 6-colored cube (Screen 2)

**Shared code:** `engine/plotting.py`'s `_ROCKET`/`_ROCKET_WINDOW` constants and `figure_2d`'s `obj="rocket"`/`obj="square"` branches are unchanged and still serve Topic 3's graphics/medical screens and Topic 4's medical/robotics screens; `figure_3d` (the old basis-vector-arrow cube figure) is also unchanged and still used by Topic 3's biology screen. Topic 2 no longer calls `figure_2d`/`figure_3d` at all — both of its own screens build their pictures from generic primitives instead (`new_figure_2d`/`shade_polygon` for 2D; `new_figure_3d` plus raw `go.Mesh3d`/`go.Scatter3d` for 3D).

**Notes (flagged, not yet resolved):**
- The "General warp" preset's notice text (Screen 1) still references a "sample vector x" toggle-and-compare interaction (turn on the sample vector, compare A·x to x, hunt for eigenvectors) that does not exist on this screen — flagged during the original rework, still unresolved. Either restore that interaction or trim the notice text.
- `__init__.py`'s screen-selector radio option still reads "2 · 3D (tetrahedron)" even though the 3D object is now a cube (it went tetrahedron → hexahedron → cube across three follow-up requests and the label was never updated to match). Flagging rather than silently editing lesson-adjacent UI text.

## Topic 3 — Determinant (`topics/t03_determinant/`)

**File structure:** `t03_determinant` is now a per-screen package:
- `__init__.py` — TOPIC registry, OVERVIEW, example selector, dispatch, `_det_meter` helper
- `surveying.py` — Example 1
- `medical.py` — Example 2
- `biology.py` — Example 3
- `graphics.py` — Example 4

- [x] Module exists and registered in `app.py` (imports as `topics.t03_determinant`)
- [x] OVERVIEW with 2D and 3D formulas in LaTeX + "each 3D term is the 2D formula" framing
- [x] OVERVIEW notes determinants are only defined for square matrices
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
- [x] P, Q, R each rendered in a narrow left sub-column (`st.columns([0.35, 0.65])`) so each reads as a single (x, y) point instead of spanning the panel
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

**Topic 4 — naming + intro:** A/A⁻¹ used throughout (intro, inverse meter, all
screens) EXCEPT Cryptography's Hill-cipher key, which stays M by design. OVERVIEW
ends with "ONLY SQUARE MATRICES HAVE AN INVERSE. How to calculate an inverse will be
shown in lesson 5.5." HOWTO reworded (not every screen is there-and-back). Spec file
specs/topic4_inverse.md fully updated to match.

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

- [x] Example 1 — Robotics: REDESIGNED, destination-driven. Preset sets arm map A
      (actuator columns); destination b editable; NO slider/radio; graph from
      primitives (actuator-column arrows + destination b + tip-to-tail solved
      controls landing on b; singular draws the reachable line and marks b
      unreachable); 3-step math (A/detA, A⁻¹/detA⁻¹=1/detA, x=A⁻¹b, check A·x=b);
      singular shows "column 2 = column 1 → det 0 → no inverse". Inputs narrow.
- [x] Example 2 — Cryptography: Hill cipher unchanged; key stays M by design.
- [x] Example 3 — Medical: REDESIGNED, mix/unmix leg bone. Plain-English CT
      narrative; object is a leg-bone cross-section (outer ring + marrow) shown ghost
      (true) vs solid (reconstructed); preset sets scanner A; measurement-error
      slider (no morph/radio); math shows A & A⁻¹ with plain-word labels then a live
      4-line pipeline for two landmarks (bone edge, marrow edge) with real matrix
      arithmetic on lines 2 and 4; unstable preset visibly blows up; singular shows
      ghost only + "no inverse — can't unmix". A/A⁻¹ naming.
- [x] Example 4 — Business: DE-CRYPTED, bakery. Cakes & cookies from flour & sugar;
      A is the recipe table (col 1 = cake, col 2 = cookie; rows = flour, sugar);
      5 algebra steps each led by a plain sentence; step 3 explains the 2×2 adjugate
      in words; round trip returns the batch; singular = "cookie is a double cake";
      presets renamed "Two different recipes" / "Recipes in the same ratio (singular)".
- [x] Shared _inv_meter renders A⁻¹; all matrix inputs compact/narrow (no screen-wide
      matrices).

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

**Spec:** `specs/topic5b_elimination.md`, `specs/topic5b_logistics_redesign.md`, `specs/topic5b_infinite_nosolution.md`, `specs/topic5b_smoothie.md`

**File structure:** `t05b_elimination` is now a per-screen package:
- `__init__.py` — TITLE, SLUG, OVERVIEW, HOWTO (as `st.caption`), render() dispatcher
- `workbench.py` — shared elimination engine (all row-op logic, state management, `workbench()` callable); includes `_active_pivot_tri` (active pivot, blue) and `_completed_pivots` (finished pivots, yellow) for pivot highlighting
- `eq_parser.py` — numeric parser for Logistics (x-variables, N_VARS=7; `parse_equation`, `rows_equivalent`, `ParseError`)
- `eq_builder.py` — shared equation-builder UI (`equation_builder(key, n_unknowns, target_aug, ...)`) — n-agnostic, parser-agnostic; powers three screens with two parsers
- `circuit_parser.py` — symbolic parser for Circuit (I-variables + R/V symbol table; N_VARS=5)
- `rref_reducer.py` — dedicated Gauss-Jordan RREF reducer for [A|I] inversion (`make_augmented`, `compute_one_step`, `run_to_reduced`, `op_*`); uses Fraction; pure logic, no Streamlit; built and unit-tested before wiring
- `screen_workbench.py` — Screen 1 (Augmented Matrix: presets, math block) — renamed from "The workbench" this session
- `inverse_elim.py` — Screen 2 ([A|I] inverse-by-elimination; spec: `specs/topic5b_inverse_elimination.md`)
- `infinite_nosolution.py` — Screen 3 (Infinite and No Solutions: two presets, reuses `workbench()` unchanged; spec: `specs/topic5b_infinite_nosolution.md`) — NEW this session
- `logistics_one.py` — Screen 4 (Logistics one plan: 6-route tree, unique solution)
- `logistics.py` — Screen 5 (Logistics many plans: 7-route cycle, infinitely many)
- `smoothie.py` — Screen 6 (Smoothie: homogeneous 5x5 system, 3 free variables, solution-space payoff; spec: `specs/topic5b_smoothie.md`)
- `circuit.py` — Screen 7 (Circuit: KCL/KVL symbolic equations, 5 currents, unique solution)

- [x] Module exists and registered in `app.py`
- [x] OVERVIEW
- [x] HOWTO rendered as `st.caption` (no expander)
- [x] Seven screens — selector: "1 · Augmented Matrix / 2 · Inverse by elimination / 3 · Infinite and No Solutions / 4 · Logistics (one plan) / 5 · Logistics (many plans) / 6 · Smoothie / 7 · Circuit" — **this session:** Smoothie and Circuit swapped (was 6 · Circuit / 7 · Smoothie); updated in `__init__.py` (labels + dispatch) and `specs/topic5b_elimination.md`
- [x] `aug_array_latex` in `engine/widgets.py` — optional `highlight=(row,col)` arg (defaults `None`; existing callers unaffected); **this session:** added optional `highlights={(row,col): hex_color, ...}` dict arg (takes precedence per-cell over `highlight`; existing single-`highlight` callers unaffected)

### Layout refactor
- [x] Page-level "How to use this screen" expander removed; HOWTO now `st.caption` under OVERVIEW
- [x] Workbench screen: "Show the math" expander removed — math block always shown below workbench
- [x] Circuit screen: already expander-free; no change needed
- [x] Workbench engine's internal expanders ("All operations (N)", "Back-substitution steps") retained — these are legitimate in-workbench UI, not content wrappers

### Shared workbench engine
- [x] Equations displayed above augmented matrix (both update on every op)
- [x] Augmented matrix via `aug_array_latex` — active pivot highlighted blue `#4dabf7` (`_active_pivot_tri` in `workbench.py`; highlight advances column by column as elimination proceeds); **this session:** completed pivots (nonzero diagonal entry, all zeros below it in-column) ALSO highlighted, in yellow `#ffd43b` (`_completed_pivots`, new helper in `workbench.py`), both passed together via the new `highlights=` dict — applies to every screen that calls `workbench()` (Augmented Matrix, Infinite/No Solutions, both Logistics screens, Circuit)
- [x] Manual controls: Add multiple / Swap / Scale
- [x] **This session:** the operation-type picker and every source/target/row selector in the manual controls converted from `st.selectbox` to `st.radio` (`horizontal=True`); same session_state keys throughout, so `_do_apply_cb` and every other callback are unchanged
- [x] Guided: "Do one step" (one standard forward-elimination op)
- [x] Guided: "Run to triangular form"
- [x] **This session:** new "Run to reduced form" button beside "Run to triangular form" in the Guided elimination row — runs full RREF from any state (forward-eliminate, normalize each pivot to 1, clear above and below) via new `_rref_full` + `_run_to_reduced_cb`; single undo entry
- [x] "Back-substitute & solve" (enabled once triangular with nonzero pivots)
- [x] Undo + Reset
- [x] **This session:** `workbench()` gained an optional `right_extra=None` callback rendered inside its right column (under the matrix + banner + solution box), so callers can place content beside the matrix instead of below the whole workbench row; default `None` means every existing caller is unaffected. `equation_builder()` (`eq_builder.py`) forwards its own optional `right_extra=None` through to its internal `workbench()` call for the same reason
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

### Screen 1 — Augmented Matrix (renamed from "The workbench" this session)
- [x] Intro rewritten (verbatim, two paragraphs): augmented-matrix definition + the 3 allowable operations (swap / scale / add a multiple) + upper-triangular form + back-substitution; second paragraph defines PIVOTS (nonzero diagonal entries required for a completed upper-triangular form) and says to use the swap operation if a zero appears in a pivot position
- [x] Old `_E1_NOTICE` `st.info` block removed
- [x] Presets TRIMMED to two: "One solution" / "Needs a row swap" (matrices unchanged) — "Redundant equation (infinite)" and "Contradiction (no solution)" MOVED to the new Screen 3 (Infinite and No Solutions) below
- [x] Preset picker: `st.selectbox` → `st.radio` (`horizontal=True`), same state key, so the existing preset-load-on-change logic is unchanged
- [x] Math block always shown (elementary row operations + det = product of pivots + rank preview)
- [ ] Not yet manually re-verified in the running app after this session's edits (pending your review)

### Screen 3 — Infinite and No Solutions — `infinite_nosolution.py` (ENHANCED this session)

**Spec:** `specs/topic5b_infinite_nosolution.md`; parametric engine per `specs/parametric_solution.md`

Dedicated home for the two non-unique outcomes elimination can reveal: no solution and infinitely many. Reuses the shared `workbench()` engine unchanged — no engine edits were needed for this screen itself.

- [x] `render_infinite_nosolution()` — module, imported in `__init__.py` (import wrapped in `try/except ImportError` with an `st.info("Coming soon.")` placeholder fallback while the module didn't yet exist; now resolves to the real screen)
- [x] Two presets, both A=[[1,1,1],[2,2,2],[1,2,3]] (row 2 = 2×row 1): "No solution (0 = 3)" b=(6,15,14); "Infinitely many (0 = 0)" b=(6,12,14)
- [x] State keys prefixed `t05b_infns_*`, isolated from Screen 1's `t05b_e1_*`
- [x] Preset load path: `_make_aug` + `_load_aug` (the shared workbench helper, functionally identical to Screen 1's inline load block), gated by a `t05b_infns_last` change-tracker, mirroring Screen 1's pattern
- [x] **This session:** Preset picker changed from `st.selectbox` to `st.radio` (`horizontal=True`), same state key `t05b_infns_preset`, load-on-change logic unchanged
- [x] **This session:** Intro and notice reworded (verbatim replacement, straight-ASCII-quote, `--` style preserved). Intro now generalizes to n-dimensional systems in plain 14-year-old language (each equation is a "rule" the answer must obey; rules that secretly agree waste one and free an unknown, infinitely many answers; rules that flatly clash give no answer — works the same at 2, 3, or 20 unknowns). Notice explains the second equation is the first times 2 ("the same rule written twice"), so eliminating row 2 against row 1 always leaves a bottom row `0 = something`, and walks through the two outcomes: not zero (here 0 = 3) -> no solution; 0 = 0 -> infinitely many.
- [x] **This session, BUILT (pending review):** General-solution display added below the workbench, gated behind triangular form (`_is_upper_triangular(M, 3)` — nothing shown until the student's own elimination reaches upper-triangular; a "Reach triangular form to see the general solution." caption shows until then). Reads the CURRENT live matrix (`st.session_state["t05b_infns_M"]`) and calls the new `engine/parametric.py` (`solve_parametric`, `parametric_latex`, `solution_equations_latex`):
  - no_solution: stacked-vector LaTeX statement + caption explaining the impossible row.
  - unique: per-variable equations + the particular-vector stacked form.
  - infinite: per-variable equations (e.g. x1 = x3 - 2, x2 = 8 - 2 x3, x3 = x3) plus the stacked vector form X = particular + sum of free_var * direction, using the real variable index as each free variable's label; caption states the free-variable count.
  - Wrapped in try/except — falls back to a caption ("Keep eliminating to see the general solution.") rather than crashing.
- [x] No hand-rolled scenario detection — the workbench's existing `_show_scenario` still supplies the live no-solution / infinitely-many banner, independent of the new general-solution display
- [x] **This session:** the general-solution block moved into `workbench()`'s right column via `right_extra` (sits under the matrix + banner instead of below the whole workbench row); per-variable equation gaps tightened via `solution_equations_block` (replacing the per-line `st.latex` loop with one combined aligned block)
- [ ] Not yet manually verified in the running app (built this session; pending your review — confirm "No solution" reduces to `0 0 0 | 3` with the no-solution banner, and "Infinitely many" reduces to `0 0 0 | 0` with the infinitely-many banner, and that the general-solution block only appears once triangular form is reached)

### Shared parametric-solution engine — `engine/parametric.py` (NEW this session, BUILT pending review)

**Spec:** `specs/parametric_solution.md`

Engine-level helper (no Streamlit import) that takes an augmented matrix + n_unknowns and returns the general solution in parametric form: X = particular + sum over free vars of (free_var * direction_vector). Built to be reused by multiple Topic 5.5 screens, not just Screen 3.

- [x] `solve_parametric(M, n_unknowns, var_name="x") -> dict(status, particular, free_vars, directions, n_free)` — converts the augmented matrix's floats to exact sympy Rationals (`sp.nsimplify(sp.Float(str(v)), rational=True)`, so 1.5 -> 3/2 and 0.3333... -> 1/3 cleanly), computes RREF via sympy, and detects no_solution / unique / infinite for ANY number of free variables (0, 1, 2, 3+).
- [x] `parametric_latex(result, var_name="x")` — stacked-vector LaTeX: X = particular_column + sum of var_i * direction_column, one bmatrix column per free variable, using the free variable's real 1-based index as its scalar label (not generic t1, t2).
- [x] `solution_equations_latex(result, var_name="x")` — per-variable equation lines: pivot variables solved in terms of the free variables; free variables read as themselves (e.g. x3 = x3).
- [x] **This session:** `solution_equations_block(result, var_name="x")` — returns one combined LaTeX string with all per-variable equations stacked in an aligned environment (tight, single `st.latex` call), reusing `solution_equations_latex`'s lines internally and aligning on "&="; removes the blank gaps that appeared between per-variable equation lines when each was rendered as its own `st.latex` call. `solution_equations_latex` itself is unchanged (other code may still use the list form).
- [x] `sympy>=1.12` added to `requirements.txt`.
- [x] Verified via inline self-tests (no test file added): a 3-free-variable 5-unknown system and a 1-free-variable 3x3 system both produce correct particular + direction vectors, fractions display exactly (e.g. 3/2), and no_solution / unique are both detected correctly.
- [x] Reused this session by Screen 3 (Infinite and No Solutions), `var_name="x"`.
- [x] Also reused by Screen 6 (Smoothie), `var_name="f"` — a homogeneous 5-unknown system with 3 free variables (f3, f4, f5), the multi-free-variable payoff case (Screen 3 exercises only 0/1 free variables).

### Screen 4 — Logistics (one plan) — `logistics_one.py` (moved from Screen 2a this session)

**Teaching role:** Introduces the equation-builder pattern on a simpler tree network where every store has exactly one incoming route. Elimination gives a unique answer — students see the method work cleanly before the harder case.

- [x] **6-route tree network** — B fed only by W1 (route x₄); no cycle. Routes: x₁ F→W1, x₂ F→W2, x₃ W1→A, x₄ W1→B, x₅ W2→C, x₆ W2→D. Demands: A=30, B=20, C=25, D=25 (total 100 = factory supply).
- [x] **Verified math:** 7 equations / 6 unknowns, rank=6 → unique solution x=(50,50,30,20,25,25). One redundant row zeros out after elimination (F-row is dependent); `_show_scenario` correctly falls through to "Ready to back-substitute."
- [x] **Diagram** (`_logistics_one_diagram`): B placed under W1's side with a single incoming arrow — visually contrasts with 2b where B has two incoming arrows.
- [x] **Powered by `equation_builder`** with `key="t05b_e2a"`, `n_unknowns=6`. All state keys prefixed `t05b_e2a_*`, fully isolated from 2b's `t05b_e2_*` keys.
- [x] **Closing text:** "One definite plan" — every route pinned; explains that adding a second route to B (the next screen) changes this completely.
- [x] **This session, BUILT (pending review):** screen-specific green-background/yellow-text banner (only this screen), shown after triangular form, explaining 7 equations for 6 unknowns -> one redundant equation -> harmless 0=0 row -> 6 pivots -> one solution; contrasts 0=0 (harmless) vs 0=nonzero (no solution).

### Screen 5 — Logistics (many plans) — `logistics.py` (REDESIGNED; moved from Screen 2b this session)

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
- [x] **This session, BUILT (pending review):** general-solution display wired in via `engine/parametric.py`. After `equation_builder(...)` returns, a full-width block (below the workbench, not inside `right_extra`) reads the current matrix and, once triangular/reduced: for the infinite case, renders a two-column row (`st.columns([1, 1], gap="large")`) — per-variable equations (`solution_equations_block`) on the left, the stacked vector form (`parametric_latex`) on the right, equal height; for the unique case, just the per-variable equations, no columns. Layout iterated across several passes (right_extra-only -> split right_extra/full-width -> this two-column full-width row) before landing here. Verified: 1 free variable (x5); solution x1=50-x5, x2=50+x5, x3=30, x4=20-x5, x5 free, x6=25, x7=25.

### Screen 7 — Circuit (redesigned — complete, no polish pending; moved from Screen 3 to Screen 6 in an earlier session, then to Screen 7 this session in the Smoothie/Circuit selector swap)

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

### Screen 6 — Smoothie — `smoothie.py` (NEW, BUILT pending review; selector position updated to 6 this session in the Smoothie/Circuit swap, was 7)

**Spec:** `specs/topic5b_smoothie.md`

Multi-free-variable payoff screen: a homogeneous 5x5 system (total volume and total
sweetness held fixed under an ingredient swap) whose five equations collapse to rank
2, leaving three free variables — the solution space is 3-dimensional rather than a
single point or a single free parameter.

- [x] `render_smoothie()` — module, imported in `__init__.py` (import wrapped in
      `try/except ImportError` with an `st.info("Smoothie: coming soon")` placeholder
      fallback while the module didn't yet exist; now resolves to the real screen).
- [x] Ingredients f1..f5 (strawberries, bananas, yogurt, milk, honey) shown as a
      compact legend above the workbench.
- [x] Homogeneous system `A=[[1,1,1,1,1],[1,-1,1,-1,2],[2,0,2,0,3],[1,3,1,3,0],
      [7,-1,7,-1,11]]`, `b=(0,0,0,0,0)` loaded via the shared `_make_aug`/`_load_aug`
      path (per spec: rank 2, free vars f3/f4/f5, particular = 0).
- [x] Single preset ("Volume + sweetness locked", one-item radio) — no scenario
      branching needed since the system is fixed.
- [x] **This session:** `var_name="f"` threaded through `workbench()` (new `var_name`
      param on `workbench()`, defaults to `"x"`, so other screens are unchanged) so
      the equations/matrix display shows f1..f5 consistently instead of x1..x5.
      Call is now `workbench("t05b_smoothie", 5, var_name="f", right_extra=...)`
      (was `workbench("t05b_smoothie", 5)` unchanged, per the original note below).
- [x] General-solution display gated behind triangular form (same
      `_is_upper_triangular` gate as Screen 3), calling `solve_parametric(M, 5, "f")`
      from `engine/parametric.py`: per-variable equations
      (**this session:** via `solution_equations_block`, one combined aligned
      LaTeX string instead of a per-line loop — tightens the gaps between rows)
      then the stacked vector form (`parametric_latex`) with the three direction
      vectors ("adjustment patterns"); caption states the free-variable count and
      the 3-dimensional-solution-space framing. Wrapped in try/except — falls back
      to a "Keep eliminating to see the general solution." caption. **This
      session:** moved into `workbench()`'s right column via `right_extra` (sits
      under the matrix + banner instead of below the whole workbench row).
- [x] Intro / notice / closing text render verbatim from the spec.
- [ ] Not yet manually verified in the running app (built this session; pending
      your review — confirm the legend renders, the system loads under
      `t05b_smoothie_*` keys, eliminating reaches triangular form, and the
      parametric block shows 3 free variables f3/f4/f5 with particular = 0).

### Screen 2 — Inverse by elimination [A|I] — `inverse_elim.py` (COMPLETE; moved from Screen 4 to Screen 2 this session)

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
- [x] **Wired into selector** as "2 · Inverse by elimination" in `__init__.py` radio (selector position 2 this session; was position 4).

### Polish & fixes (this session, BUILT pending review)

Cross-cutting refinements applied after the screens above were built:

- [x] **Shared workbench engine — fraction input:** the "Factor k" (Scale a row) and "k" (Add multiple) inputs changed from `st.number_input` to `st.text_input`, with a new `_parse_factor` helper that accepts decimals and simple fractions like `1/11.6` (splits on a single `/`, falls back to a default on bad input). Both branches of `_do_apply_cb` read the factor via `_parse_factor`. Applies to every screen using `workbench()`; the +/- steppers are gone from those two fields (tradeoff for fraction entry).
- [x] **Shared workbench engine — number formatting:** `_equations_latex` (raised its zero-snap `TOL` to `1e-4`, coefficient/b formatting switched from `.4g` to snap-then-2-decimal) and `engine/widgets.py`'s `aug_array_latex` `_fmt` (and `eq_builder.py`'s `_live_aug_latex` `_fmt`) now snap near-zero values (`<1e-4`) to `0` and format non-integers to 2 decimals — eliminates floating-point dust that displayed as scientific notation (e.g. `-4.611e-05`) in reduced matrices. Whole numbers still render as integers; only genuinely fractional values get 2 decimals.
- [x] **Shared eq_builder — variable name in preview + workbench:** `equation_builder` now forwards `var_name` to its `workbench()` call so the workbench equation display uses the screen's variable letter (Circuit shows `I1..I5`, not `x`). `_row_to_latex`, `_row_to_eq_str`, `_node_balance_builder`, and `_fill_cb` all take a `var_name` param (default `"x"`); Circuit passes `var_name="I"`. Logistics screens default to `"x"`, unchanged.
- [x] **Shared eq_builder — input hygiene:** browser autofill/autocomplete suppressed on the equation-builder text inputs via an injected `components.html` script (sets `autocomplete`/`autocorrect`/`autocapitalize` off, `spellcheck` false, randomizes each input's `name` to defeat Chrome/Edge autofill matching). Equation-builder state (typed boxes + check/ready/matrix) cleared on screen entry via a per-switch clear in `__init__.py`'s `render()` (tracks `t05b_prev_example`; on a change, pops the entered screen's `t05b_e2a_*` / `t05b_e2_*` / `t05b_e3_*` equation + state keys) so boxes no longer persist across visits. (Replaced an earlier one-time `{key}_initialized` clear that only fired once per session.)
- [x] **Screen 6 Smoothie — ingredient legend beside the vector:** the ingredient legend (f1=strawberries … f5=honey) is now ALSO shown to the LEFT of the "single vector equation" (a two-column `st.columns` row), in addition to the legend up top; intro reworded from "thousands of gallons" to "one thousand gallons".
- [x] **Screen 7 Circuit — instructions rewritten for a 14-year-old:** the intro now teaches HOW to build the equations — KCL ("what flows in must flow out": add arrows into a node, subtract arrows out, set to 0) with node P worked (`I1 - I2 - I3 - I5 = 0`); KVL (voltage drops around a clockwise loop sum to zero, `R*I` per resistor, subtract the battery voltage when the clockwise path reaches its negative terminal first) with Loop 1 worked (`R1*I1 + R3*I3 - 36 = 0`) and Loop 3 worked (`R5*I5 - R2*I2 = 0`, minus because clockwise runs against I2). The `- 36 = 0` form parses correctly (constant moved to b). Diagram label font sizes enlarged for readability (resistor/node/current/loop/battery labels bumped ~+4–5pt; motor/lamp/node letters to 17–18; layout height `420 -> 520`).
- [x] **Screen 2 Inverse by elimination — fuller verify display:** the "Verify: A * A^-1 = I" line now shows the actual A and A⁻¹ matrices in the product — `A[matrix] · A⁻¹[matrix] = I[matrix]` (via `_bmatrix(A_fr) · _bmatrix(inv) = _bmatrix(product)`) — instead of just the identity result.

### Future hook (not Topic 5.5 work)

- **AC-circuit revisit (Topic 9)** — the same circuit topology reused with complex impedances; same 5 equations, complex solution. `circuit_parser.py` and the Plotly diagram are kept clean for this future hook.

---

## Topic 6 — Vector Spaces (`topics/t06_spaces/`) — BUILT this session, pending review

**Spec:** `specs/topic6_spaces.md`

Names the three spaces hiding inside every matrix — column space, null space, row
space — plus the counting rule (rank + free variables = unknowns). Design principle:
each screen is a vertical stack of self-contained **viewport blocks** (math LEFT /
graph RIGHT, everything for one example visible without scrolling inside the block);
embedded compact recaps of Robotics/Smoothie/Logistics/Circuit so the student never
jumps topics; plain words before symbols; no C(A)/N(A) notation. No workbench, no new
engine code (recaps are result-only). Registered in `app.py` after `t05b_elimination`.
`TITLE = "6 · Vector Spaces"`, `SLUG = "spaces"`.

**File structure:** per-screen package — `__init__.py` (TITLE, SLUG, OVERVIEW,
selector key `t06_screen`, dispatch) + `screen_what.py`, `screen_column.py`,
`screen_null.py`, `screen_row.py`, `screen_together.py`.

### Screen 1 — What a vector space is (`screen_what.py`)
- [x] Block 1 intro (the "no escape" rule; span-as-vector-space, any amounts incl.
      negative/zero).
- [x] Block 2a — whole x-y plane: arrows (3,1)+(1,2)=(4,3) tip-to-tail, shaded plane,
      stacked-vector math beside the graph.
- [x] Block 2b — line through the origin along (1,2): points (1,2),(2,4),(3,6),
      stacked-vector math (add + triple).
- [x] Block 3 — FAIL examples: off-origin line y=3 ("not a vector space, because it
      fails the no-escape rule"), first-quadrant fail, smoothie-mix-fails contrast
      (positive amounts only), and the must-contain-the-zero-vector rule.
- [x] Block 4 closing.

### Screen 2 — Column space (`screen_column.py`)
- [x] Block 0 — NEW step-by-step "how to compute a column space" recipe at the top
      (before the intro), math only, no graph. Shared made-up 4x4
      A=[[1,2,1,1],[1,3,2,4],[2,5,3,5],[0,1,1,3]] (rank 2). 4 steps: write matrix +
      columns; row-reduce to find pivot columns (RREF pivots yellow); take the
      ORIGINAL matrix's pivot columns (1,1,2,0) and (2,3,5,1) — explicit "from the
      ORIGINAL, not the reduced form"; parametric span form with GREEN highlight +
      \underbrace "column space" label (c1, c2 scalars green too). Same matrix as the
      null-space and row-space recipes.
- [x] Block 1 intro — expanded: opens with a paragraph defining column space = all
      possible outputs, its dimension = rank, and the solvability rule (b solvable iff
      b in the column space), before the original "Take a matrix A" paragraph.
- [x] Block 2 — Robotics recap, the ONE allowed pose toggle (Reachable
      [[1.5,0.5],[0,1]] / Singular [[1,1],[1,1]]); reachable pose shows the full
      matrix times x for x=(3,-3)->(3,-3) and x=(-2,3)->(-1.5,3), outputs spread
      across the plane -> whole-plane column space; singular shows the line + an
      unreachable point.
- [x] Block 3 — A=[[1,2],[2,4]]: full-matrix A·(3,-3)=(-3,-6) and A·(-2,3)=(4,8),
      both landing on the line along (1,2); (3,6) reachable vs (3,5) unreachable.
- [x] Block 4 closing.

### Screen 3 — Null space (`screen_null.py`)
- [x] Block 0 — NEW step-by-step "how to compute a null space" recipe at the top
      (before the intro), math only, no graph. Same shared 4x4 A. 5 steps: set up
      A·x=0 (A times x column = zero column, no standalone A); form [A|0] and
      row-reduce (array+vertical-rule, "reduced form (Reduced Row Echelon Form)");
      identify pivot/free variables (RREF re-shown with pivots yellow); solve pivots
      in terms of free variables shown BOTH before (raw rows =0) and after (free vars
      moved right); write the null space in parametric form with the all-zeros
      particular vector (\underbrace "particular", white) plus the BLUE null-space part
      (x3,x4 scalars + direction vectors, \underbrace "null space"). Basis (1,-1,1,0)
      and (5,-3,0,1), 2 free variables. VERIFIED.
- [x] Block 1 intro (null space = the freedom; particular + null space = every answer).
- [x] Block 2 — A=[[1,2],[2,4]] null-space line along (-2,1), drawn WITH the
      column-space line along (1,2) fainter on the same graph (same matrix, two lines).
- [x] Block 3 — Smoothie recap: the three direction vectors as the visual (5D can't
      be plotted), ingredient legend.
- [x] Block 4 — Logistics many-plans recap: direction (-1,1,0,-1,1,0,0) lives in the
      null space (VERIFIED A·direction = 0).
- [x] Block 5 closing.

### Screen 4 — Row space and the counting rule (`screen_row.py`)
- [x] Block 0 — NEW step-by-step "how to compute a row space" recipe at the top
      (before the intro), math only, no graph. Same shared 4x4 A. 4 steps: write
      matrix + rows; row-reduce ("row operations never change the row space"), RREF
      with nonzero rows PURPLE and zero rows gray; take the NONZERO rows of the
      REDUCED form (1,0,-1,-5) and (0,1,1,3) — explicit contrast with the column-space
      rule ("columns from ORIGINAL, rows from REDUCED"); parametric span form with
      PURPLE highlight + \underbrace "row space" label (r1, r2 scalars purple too).
      Consistent color code across the three recipes: GREEN column / BLUE null /
      PURPLE row, all on the SAME matrix (one matrix, all three spaces). VERIFIED.
- [x] Block 1 intro (row space; rank = pivot count).
- [x] Block 2 — TWO Logistics cards side by side (one-plan and many-plans), each with
      its surviving RULES (route variable x, one per line) on the left and its reduced
      form (array+vertical-rule LaTeX, dimmed zero row) on the right; the many-plans
      card also shows its parametric solution X = [50;50;30;20;0;25;25] +
      x5·[-1;1;0;-1;1;0;0] below its matrix.
- [x] Block 3 — the counting rule centerpiece + two count cards (Smoothie, Circuit;
      Logistics is covered by Block 2). Each card: RULES left (correct letter — f for
      Smoothie, I for Circuit) / reduced matrix right. Smoothie card shows the
      all-zeros particular vector explicitly plus its three free-variable directions
      X = [0;0;0;0;0] + f3·[...] + f4·[...] + f5·[...]; Circuit card's b column IS the
      answer I=(6,2,3,3,1), no free variables.
- [x] Block 4 closing.
- Note: all reduced forms VERIFIED (Smoothie rank 2 / 3 free; Logistics one-plan
      rank 6 / 0 free, unique (50,50,30,20,25,25); Logistics many-plans rank 6 / 1
      free; Circuit rank 5 / 0 free). Matrices use array + vertical rule (NEVER
      bmatrix with `\big|`, which fails to render — that was the initial bug).

### Screen 5 — One matrix, all three spaces (`screen_together.py`)
- [x] Block 1 — 1-dimensional example: eliminate A=[[1,2],[2,4]] once; both the
      column-space line (1,2) and null-space line (-2,1) on one 2D graph.
- [x] Block 2 — read all three spaces off the reduced form (column space line,
      null space line, row space rule x1+2x2 rank 1; counting 1+1=2).
- [x] Banner — "Now let's go bigger" bridge between the 1D and 2D examples.
- [x] Block 3 — 2-dimensional example (3D graph): A=[[2,1,3],[1,1,2],[3,2,5]]
      (row3=row1+row2, rank 2; RREF [[1,0,1],[0,1,1],[0,0,0]]). Column space = the
      PLANE -x-y+z=0 spanned by (2,1,3) and (1,1,2); null space = the LINE along
      (-1,-1,1) — which is perpendicular to the plane, poking straight through it;
      counting 2+1=3. 3D plot via `new_figure_3d` + `add_plane_3d` + `_arrow3d` +
      a Scatter3d line segment; rotatable. All VERIFIED.
- [x] Block 4 — closing bridge (dimension, basis; Topic 7 preview: closest point
      when b is outside the column space -> least-squares / GPS / camera apps).

- [ ] Not yet manually verified in the running app (built this session; pending your
      review — confirm every block fits one viewport with math + graph together, the
      3D plane/line renders and rotates, and all embedded recaps render verbatim).

---

## Core curriculum status

**Topics 0, 1–5, and 5.5 are FULLY COMPLETE** — all refactored to the dark-mode layout, all screens built and verified, all engines shared and tested. The core curriculum (matrix operations → vectors → transformations → determinant → inverse → linear systems → elimination & inversion) is done. **Topic 6 (Vector Spaces) is BUILT this session, pending in-app review.**

---

## Topics not yet started

- [ ] 7 — Projection & Least Squares
- [ ] 8 — Eigenvalues & Eigenvectors
- [ ] 9 — Complex Numbers in LA (AC-circuit screen reuses Topic 5.5 Circuit topology + `circuit_parser` with complex impedances)
- [ ] 10 — Fourier Matrices (DFT)
- [ ] 11 — Linear Algebra in AI/ML (PCA & SVD)
