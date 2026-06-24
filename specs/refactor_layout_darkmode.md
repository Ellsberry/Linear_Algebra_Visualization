# Build Spec — Layout Refactor + Dark Mode (Topic 3, with file split)

**For the builder (Claude Code):** This finalizes a new screen layout for Topic 3
and splits the topic into per-screen files first so each edit is small and
verifiable. Dark mode and the top selector are already applied. **Do Topic 3 only;**
do not touch topics 2, 4, 5, 5.5 yet. Follow `CLAUDE.md`. Keep all existing content
and the live morph-math — this changes *layout, structure, and the rendering of the
corner math*, not the lesson.

**Process rules (these have bitten us — follow exactly):**
- Make **surgical edits**: move existing `st.` calls into the new structure; do NOT
  rewrite whole functions from memory (that keeps dropping blocks).
- Use **straight ASCII quotes only** — never curly/smart quotes (they cause
  SyntaxErrors).
- After each step: run
  `python -c "import ast; ast.parse(open(PATH).read())"`, paste the changed code,
  and **stop** — wait for review before running the app.
- After a step is verified, update `specs/STATUS.md` and **commit** before the next.

---

## Part 0 — Split `t03_determinant.py` into per-screen files FIRST

The single 460+-line file is why edits keep clobbering each other. Split it before
applying the layout, as a pure mechanical move (no logic changes).

**Target structure:**
```
topics/t03_determinant/
    __init__.py        # TOPIC registry entry, OVERVIEW text, example selector, dispatch
    _shared.py         # _det_meter and any helper used by 2+ screens
    surveying.py       # _example_surveying
    medical.py         # _example_medical
    biology.py         # _example_biology
    graphics.py        # _example_graphics
```
- Move each `_example_*` function **verbatim** into its own file; fix imports
  (`from engine import widgets as w, plotting as plot`, `from ._shared import
  _det_meter`, etc.).
- `__init__.py` keeps the same `TOPIC`/registration so `app.py` needs **no change**
  and the module still imports as `topics.t03_determinant`.
- **Do this one function at a time**: move one, parse-check, run the app, confirm the
  screen still works, commit. Then the next. Four small commits, not one big one.
- No behavior changes in Part 0 — it's only relocation. The layout work is Part 1.

---

## Part 1 — The finalized layout (apply per screen, in the new files)

### 1A. Page structure (this REPLACES the earlier "controls in the left column" plan)
Controls and the example text move UP into the full-width band, so the two-column
body below is **purely math (left) and graph (right)** — maximizing room for the
math beside the picture (this is a visualization-first course).

```
[ Topic selector ]                                    (app.py — already done)
Topic header + description (FULL WIDTH)
[ Example selector — compact one-row control ]
─────────────────────────────────────────────────────────────────
 FULL-WIDTH CONTROL BAND:
   • example text ("Biology. A cell is roughly a cube…")
   • controls: preset dropdown, matrix editor, slider(s)
─────────────────────────────────────────────────────────────────
 ┌───────────────────────────┬─────────────────────────────────┐
 │ MATH (left, ~0.50)        │  GRAPH (right, ~0.50)           │
 │  always shown, NO expander│   smaller + tight margins       │
 │  matrix, det, A·corners   │                                 │
 └───────────────────────────┴─────────────────────────────────┘
 Notice / closing line (FULL WIDTH, bottom)
```
- Implement via a tiny helper in `engine/layout.py` (`two_col(ratio=(0.5,0.5))`
  returning `(left, right)`) so every screen uses the same skeleton.
- **"Show the math" expander is REMOVED on every screen** — the math renders
  unconditionally in the left column.
- The **example text and all controls render full-width ABOVE** the `two_col` block.
  Only the math goes in the left column; only the graph goes in the right.
- Column ratio default **0.5 / 0.5** (the math is the tall thing now, so it needs a
  real half). Per-screen override allowed.

### 1B. Shrink the graph (height AND margins — the real space win)
In `engine/plotting.py`, for every figure:
- Height: **2D ≈ 360–400**, **3D ≈ 420**.
- **Cut Plotly margins hard:** `margin=dict(l=10, r=10, t=10, b=10)` (defaults are
  ~80px and waste a third of the box). For 3D, tighten the scene domain similarly.
- Trim/relocate the legend so it doesn't add top padding (small legend, or overlay
  inside the plot). The goal: the graph box is mostly graph, not whitespace.

### 1C. Render the corner math compactly but CORRECTLY
The `A · (corner)` blocks are the tallest part of the math. Tighten them **without
breaking correct notation**:
- **Keep stacked column-vector notation** — the input and output are 3×1 **column**
  vectors (stacked, tall parentheses), NOT inline `(x,y,z)` tuples. A 3×3 times a
  3×1 giving a 3×1 is the correct, dimension-honest form, and it teaches the shape
  rule. Do **not** use inline/row-vector shorthand (a 3×3 times a 1×3 is undefined
  and mathematically wrong — never show that).
- **Show the actual numeric matrix** doing the multiplication, not the symbol "A".
  Each corner line is `[numeric 3×3 grid] · [stacked column] = [stacked column]`,
  with the grid showing the current entries (e.g. 1.50 on the diagonal for k=1.5).
- **Keep all three** cube corners `(1,0,0)`, `(0,1,0)`, `(1,1,1)`.
- **Shrink only these corner blocks' font** to reclaim height: wrap the corner
  `st.latex` expressions in `\small` (start there; `\scriptsize` only if still
  needed). Leave the headline math (the `A =` matrix, `det A = k³`, the meaning
  sentences) at **full size** — only the repetitive corner blocks shrink.

### 1D. Text fix
In Biology's triangular-bridge sentence, change **"Topic 5"** to **"Topic 5.5"**.

---

## Part 2 — Per-screen mapping (in the split files)

Each screen: example text + controls in the full-width band; math left; graph right;
notice/closing full-width at bottom; no expander.

- **Surveying** (`surveying.py`): band = P, Q, R point editors. Left = the derived A
  (from edge vectors) + the live det→area chain. Right = 2D figure. No slider.
- **Medical** (`medical.py`): band = preset + editable A matrix + morph slider.
  Left = det live + area before→after + the At·(square corners) math + read-only
  A(t). Right = 2D figure.
- **Biology** (`biology.py`): band = k slider. Left = derived diag(k) shown as the
  numeric matrix + det = k³ live + surface/volume line + the three A·corner blocks
  (compact, `\small`). Right = 3D figure. Notice (elephant) full-width at bottom.
- **Graphics** (`graphics.py`): band = preset + editable A + morph slider. Left =
  both matrices (current At + destination A) + live det + At·(rocket vertices).
  Right = 2D figure. No-inverse/Topic-4 closing line full-width at bottom.

(The merged editable-matrix-in-brackets widget from the earlier draft is **deferred**
— it's the riskiest piece and not needed to fix scrolling. Keep the existing
`matrix_editor` for now; revisit the bracket widget after this layout is approved.)

---

## Acceptance checklist (verify per screen, on disk, before trusting screenshots)
- [ ] `t03_determinant` is a package (per-screen files); `app.py` unchanged; app
      imports and all four screens render.
- [ ] On each screen: example text and ALL controls are full-width ABOVE the two
      columns; the left column contains ONLY math; the right column ONLY the graph.
- [ ] NO `st.expander` anywhere in Topic 3 (grep returns nothing); math always shown.
- [ ] Graphs are visibly smaller with tight margins (little whitespace in the box).
- [ ] Corner math: numeric matrix (not "A") × stacked column vector = stacked column
      vector; all three corners; corner blocks in `\small`; headline math full size.
      No inline/row-vector forms anywhere.
- [ ] Biology bridge says "Topic 5.5"; elephant notice present full-width at bottom.
- [ ] Morph screens (Medical, Graphics) still animate and the math still tracks the
      slider; straight ASCII quotes only; `ast.parse` clean.
