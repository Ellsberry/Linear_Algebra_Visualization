# Build Spec — Layout Refactor + Dark Mode (PROTOTYPE on Topic 3)

**For the builder (Claude Code):** This establishes a new screen layout, a dark
theme, and a new merged editable-matrix widget. **Prototype it on Topic 3 only**
(`topics/t03_determinant.py`), plus the app-wide pieces (theme, top selector,
plotting palette) which necessarily affect every topic. Do NOT refactor topics 2,
4, 5, 5.5 yet — we review Topic 3 first, then roll the pattern out. Follow
`CLAUDE.md`. Keep all of Topic 3's existing content/behavior (the four screens,
all the math) — this changes *layout and styling*, not the lesson.

This is a **prototype to evaluate**. The riskiest piece is the styled
bracket-matrix widget; build it first and expect to tweak its look after review.

## Part A — App-wide changes (apply once; they affect all topics)

### A1. Dark theme (app chrome)
Create `.streamlit/config.toml`:
```
[theme]
base = "dark"
primaryColor = "#4dabf7"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#1a1d24"
textColor = "#e6e6e6"
```
(These are starting values; fine to adjust for contrast.)

### A2. Topic selector → top of page, scrolls with the page
In `app.py`, move topic navigation **out of the sidebar** to a compact selector at
the **top of the main area** (a `st.selectbox` is best — stays compact as the topic
list grows to 11). Remove the sidebar topic radio and the sidebar "How to use"
text entirely. The selector scrolls with the page (no pinning). The sidebar can be
dropped or left empty.

### A3. Plotting palette re-tuned for dark backgrounds (`engine/plotting.py`)
On dark, the current light-mode colors wash out or vanish. Update:
- **All figure layouts** (`figure_2d`, `figure_3d`, `new_figure_2d`,
  `new_figure_3d`): set `paper_bgcolor="rgba(0,0,0,0)"`,
  `plot_bgcolor="rgba(0,0,0,0)"`, and a **light font** (`font=dict(color="#e6e6e6")`).
  For 3D, set the scene background transparent and axis/grid colors light.
- **Axis lines / zerolines:** `zerolinecolor="#888"` → lighter, e.g. `"#aaa"`;
  gridlines a subtle light tint, e.g. `"rgba(200,200,220,0.12)"`.
- **Data colors → brighter, higher-contrast variants** (replace the constants):
  - `_E1` crimson → `"#ff6b6b"`; `_E2` royalblue → `"#4dabf7"`; `_E3` seagreen →
    `"#51cf66"`; `_VEC` darkorange → `"#ffa94d"`.
  - `_SQUARE` → `"#20c997"`; `_SQUARE_FILL` → `"rgba(32,201,151,0.22)"`.
  - `_GRIDLINE` (deformed grid) → `"rgba(160,160,220,0.35)"`.
- Check every rgba transparency reads on dark; bump alpha where things disappear.

### A4. Smaller graphs
Graph height is currently a fixed 560. Make it a **per-figure parameter** and
reduce it: **2D ≈ 420**, **3D ≈ 480**. This is the single biggest anti-scroll win.

## Part B — The new shared layout (build in engine, prototype on Topic 3)

### B1. Page structure (top → bottom)
```
[ Topic selector — top selectbox, scrolls with page ]          (app.py)
Topic header + description (FULL WIDTH; fold the old "how to use" bits in here)
[ Example selector — compact, horizontal, low vertical footprint ]
Example description + "what to notice" (FULL WIDTH, above the columns)
┌───────────────────────────┬──────────────────────────────┐
│ LEFT COLUMN (~40%)        │  RIGHT COLUMN (~60%)         │
│  • presets (compact)      │   the graph (smaller:        │
│  • A in bracket form      │    ~420 px 2D / ~480 px 3D)  │
│    (editable or derived)  │                              │
│  • det A (live)           │                              │
│  • sliders (vertical)     │                              │
│  • A·vertex lines (live)  │                              │
│  • [morph screens only:   │                              │
│     read-only A(t)]       │                              │
└───────────────────────────┴──────────────────────────────┘
Challenge / closing line (FULL WIDTH, bottom)
```
- Implement as a small reusable helper in `engine/` (e.g. `layout.py` with a
  `two_col()` returning `(left, right)` at a given ratio) so every topic uses the
  same skeleton. Allow a **per-screen column ratio** (default 0.4/0.6).
- **"Show the math" is always shown** — no expander, no button. The math lives in
  the left column under the matrix.
- **Example selector:** use a compact horizontal control (`st.radio(...,
  horizontal=True)` with tightened spacing, or `st.segmented_control` / `st.pills`
  if the installed Streamlit supports them). Goal: one short row, not a tall stack.

### B2. The merged editable-matrix widget (the prototype's key new piece)
Add `editable_matrix(state_key, dim, label="A", editable=True)` to
`engine/widgets.py`. It renders the matrix **A in bracket form with the entries as
the cells**, so the matrix the student edits *is* the matrix in the math —
replacing the old separate "number-input grid up top + `A = [[…]]` LaTeX below".

- **Layout:** a row of `st.columns` — a thin left column drawing the **left
  bracket**, `dim` middle columns of `st.number_input` (the entries), a thin right
  column drawing the **right bracket**, with an "A =" label to the left. Since
  Streamlit can't put live widgets inside real LaTeX, the brackets are **drawn with
  CSS / tall bracket glyphs** around the input grid — it should *read* as a
  bracketed matrix. (This is the approximation to confirm on review.)
- Use the **same cell state keys** as the current `matrix_editor` (`{key}__i__j`)
  so existing presets / `set_matrix_state` keep working unchanged.
- `editable=False` → render the same bracketed matrix but with the numbers as
  static text (for **derived** matrices: surveying's A from P/Q/R, biology's diag(k),
  and the read-only morphing A(t)).
- Free editing and presets coexist: presets write the cells, the student can type
  any values, **Reset** returns to a default. Keep Reset.

## Part C — Apply to Topic 3's four screens

Map each screen onto the new layout. **A is always shown in bracket form**;
*editable* where the student sets A directly, *derived (read-only)* where A comes
from upstream inputs.

- **Surveying:** left column = P, Q, R point editors → **derived read-only A** in
  bracket form (its columns are the edge vectors) → det/area live chain →
  (no sliders). Right = 2D figure (~420). The matrix is derived, not directly
  edited — that's correct here.
- **Medical:** left = preset control + **editable A** (merged bracket matrix) +
  morph slider (vertical) + det live + area before→after + A(t)·corners; plus a
  **read-only A(t)** "current transform" bracket matrix (morph screen). Right = 2D
  figure (~420).
- **Biology:** left = k slider → **derived read-only diag(k)** in bracket form +
  det = k³ live + surface/volume + A·corners. Right = 3D figure (~480).
- **Graphics:** like Medical — preset + **editable A** + morph slider + live det +
  A(t)·vertices + read-only A(t); the no-inverse/Topic-4 closing line full-width at
  bottom. Right = 2D figure (~420).

Topic 3's matrices are small (2×2 or 3×3 diagonal), so they fit the ~40% left
column comfortably — which is why Topic 3 is a good prototype. (Topic 5.5's wide
augmented matrices will need the wider-math exception when we get there; not part of
this prototype.)

## Not in this prototype (future, once layout is approved)
- Rolling the layout/widget/dark palette out to topics 2, 4, 5, 5.5.
- Topic 5.5 **double augmented matrix `[A | I]`** to compute the inverse by
  elimination (the Topic 4 ↔ 5.5 bridge) — a wider-math screen, specced separately.

## Acceptance checklist
- [ ] App is dark; plot backgrounds are transparent and all data colors read
      clearly on dark (basis arrows, fills, deformed grid, 3D scene).
- [ ] Topic selector is a compact selectbox at the top of the page (sidebar topic
      radio and "How to use" text removed).
- [ ] Topic 3 header/description is full width with the old "how to use" guidance
      folded in; the per-example description + "what to notice" is full width above
      the columns.
- [ ] Example selector is one compact row, not a tall stack.
- [ ] Two-column body: left = presets + bracketed A + det + vertical sliders +
      A·vertex math; right = a smaller graph (~420 2D / ~480 3D).
- [ ] "Show the math" is always visible (no expander).
- [ ] `editable_matrix` renders A as a bracketed matrix of editable cells; presets
      still set the cells; free editing works; Reset works.
- [ ] Surveying/biology show a **derived read-only** bracketed A; medical/graphics
      show an **editable** A plus a read-only A(t); morph screens still animate and
      the math still tracks the slider.
- [ ] App runs with `streamlit run app.py`, no errors. (Topics 2/4/5/5.5 untouched.)
