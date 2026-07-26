# Build Spec — Topic 0, Screens 5–7: Three Views of Matrix Multiplication

> **SCOPE — read first.** This spec covers **Topic 0, Screens 5–7 ONLY** (Row
> picture, Column picture, Outer products). It is an **ADDITION** to Topic 0, not a
> replacement. It does **not** modify Screens 0–4, whose spec remains
> `specs/topic00_matrix_multiplication.md` (the authoritative record for those five
> already-built screens). When building from this file: add the three new screen
> files and extend the selector in `__init__.py` only; **do not edit
> `screen_ops.py`, `screen_2x2.py`, `screen_3x3.py`, `screen_rect.py`, or
> `screen_special.py`**, and do not alter the existing five screens' behavior.
> If anything here appears to conflict with the Screens 0–4 spec, STOP and flag it
> rather than changing either file.

**For the builder (Claude Code):** These are THREE NEW SCREENS added to the
existing `topics/t00_matmul/` package (Row picture, Column picture, Outer
products). They come AFTER the existing five screens. Follow `CLAUDE.md`. Reuse
the existing engine (`engine/widgets.py`, `engine/plotting.py`) — in particular
`editable_matrix` (with its `compact`, `editable`, `rows`, `cols` params) and the
reveal-flag Check / Show-solution pattern already used on Screens 1–3. Do NOT
hand-roll inputs. Do NOT invent examples or reword the text below — it is final
copy. Straight ASCII quotes only in code.

## Where these go

Add to `topics/t00_matmul/`:
- `screen_rows.py` — Screen 5 (Row picture)
- `screen_cols.py` — Screen 6 (Column picture)
- `screen_outer.py` — Screen 7 (Outer products)

In `topics/t00_matmul/__init__.py`, extend the screen selector order to:
`"0 · Operations", "1 · Multiply 2x2", "2 · Multiply 3x3", "3 · Rectangular",
"4 · Special matrices", "5 · Row picture", "6 · Column picture",
"7 · Outer products"`, and dispatch the three new titles to the three new
screen functions. Nothing else in `__init__.py` changes.

## Global conventions for these three screens

- **One shared worked example, identical on all three screens** (top of screen),
  so a student flipping between screens sees the SAME C built three ways:

  ```
  A (2x3) = [ 2  1  3 ]      B (3x2) = [ 1  4 ]
            [ 0  2  1 ]                [ 2  5 ]
                                       [ 3  1 ]
  C = AB (2x2) = [ 13  16 ]
                 [  7  11 ]
  ```

- **Shape rule stays visible on every screen** (a one-line caption near the top):
  "A is m×n, B is n×p, so C = AB is m×p — the shared inner dimension n is what
  gets summed over." Show the concrete shapes for that screen's matrices too.

- **Worked example is READ-ONLY** (no editable inputs) and carries the
  **highlight selector** (see below). Render A, B, C with
  `editable_matrix(..., editable=False, compact=True, rows=, cols=)`.

- **Highlight selector (worked example only):** an `st.radio` (horizontal) that
  picks which row / column / term is currently being built. When a choice is
  active, that row/column/term is emphasized in A, B, and C together, and the
  live combination for that piece is written out below the matrices (the exact
  weights and the sum). Implementation note: `editable_matrix` has no built-in
  cell-highlight, so render the highlighted worked matrices with a small local
  HTML/LaTeX helper (color the active row/column) OR use `st.latex` with the
  active row/column wrapped in `\color{#4dabf7}{...}`. Keep it compact; do not
  make the matrix span the screen.

- **Three practice examples per screen** BELOW the worked example, using the same
  three A/B pairs on all three screens (values + verified answers in each screen
  section). Practice is the fade: **Practice 1 aided, Practice 2 and 3 unaided.**
  - *Aided (Practice 1):* the highlight/weights recipe for each unit is written
    out next to its answer box (e.g. "Row 1 = 2·(row 1 of B) + 1·(row 2 of B) +
    3·(row 3 of B) = ___"); no highlight selector, just the spelled-out recipe.
  - *Unaided (Practice 2, 3):* answer boxes only, no recipe, no highlight — the
    student reads the weights off the method themselves.
  - Every practice example asks the student to build the WHOLE of C, in the
    method's units (row picture → one answer box per row of C; column picture →
    one box per column; outer products → one box per term, plus a final box for
    the sum). Use `editable_matrix(..., editable=True, compact=True,
    hide_steppers=True)` for answer boxes.
  - **Practice layout (Screens 5 and 6):** top row shows `A · B = C` on one line
    as matrices, C being a read-only live-fill display. Below it, the per-unit work
    (rows stacked top-to-bottom on Screen 5; columns side by side via `st.columns(p)`
    on Screen 6), each unit with its recipe (aided only), answer box, and Check /
    Show solution. C fills in per unit only after that unit's Check or Show solution
    is clicked (touch-tracked).
  - **Blank-until-touched:** track a `{prefix}_{unit}{k}_touched` flag per unit
    (default False), set True on that unit's Check OR Show solution. C's unit renders
    BLANK until touched; once touched it shows the entered values, including a
    legitimate 0 answer (must show as 0, never blank). C uses a small local HTML
    render helper (`_answer_matrix_html`), not `editable_matrix`, so blank cells are
    possible.
  - **Check (per unit, per-cell reveal-flag pattern, like Screens 1–3)** and
    **Show solution** on each practice example. Check flags wrong cells without
    revealing the value; Show solution writes the correct answer via the
    reveal-flag → rerun pattern (set a `{key}_reveal` flag, rerun, write at top
    of render before the answer widgets instantiate — avoids the
    StreamlitAPIException).

- **No morph, no graph** on these screens — they are about the algebra of the
  product, not a geometric transform.

## Screen 5 — Row picture (`screen_rows.py`)

**Top-of-screen explanation (verbatim):**
> **Row picture.** Look at one row of C at a time. The **first row of C** is built
> entirely from the **rows of B** — you take *2 of row 1, 1 of row 2, and 3 of
> row 3* of B and add them up. Those weights (2, 1, 3) are exactly the **first
> row of A**. So each row of A is a recipe, and it mixes the rows of B to make the
> matching row of C. **Row i of C = (row i of A) used as weights on the rows of B.**

**Worked example (read-only, shared A/B/C above), highlight selector:**
`st.radio("Building:", ["Row 1 of C", "Row 2 of C"], horizontal=True)`.
- "Row 1 of C" highlights row 1 of A (the weights) and all rows of B and row 1
  of C, and writes: `Row 1 of C = 2·(1, 4) + 1·(2, 5) + 3·(3, 1) = (13, 16)`.
- "Row 2 of C" highlights row 2 of A and writes:
  `Row 2 of C = 0·(1, 4) + 2·(2, 5) + 1·(3, 1) = (7, 11)`.

**Worked Example 2 (permutation) — same structure, own highlight selector:**
A = [[0,1,0],[1,0,0],[0,0,1]], B = [[1,4],[2,5],[3,1]], C = [[2,5],[1,4],[3,1]].
Read-only, compact; `st.radio("Building:", ["Row 1 of C", "Row 2 of C",
"Row 3 of C"], horizontal=True, key="t00_rows_worked2")`. Live combination per row
(weights = row i of A, colored):
- Row 1: `0·(1,4) + 1·(2,5) + 0·(3,1) = (2,5)`
- Row 2: `1·(1,4) + 0·(2,5) + 0·(3,1) = (1,4)`
- Row 3: `0·(1,4) + 0·(2,5) + 1·(3,1) = (3,1)`
Caption (verbatim): "This A is a permutation matrix — each row of C picks exactly
one row of B (weight 1), so multiplying just reorders B's rows. Here rows 1 and 2 of
B swap."

**Worked Example 3 (elimination step) — same structure, own highlight selector:**
A = [[1,0,0],[-2,1,0],[0,0,1]], B = [[1,4],[2,5],[3,1]], C = [[1,4],[0,-3],[3,1]].
Read-only, compact; `st.radio("Building:", ["Row 1 of C", "Row 2 of C",
"Row 3 of C"], horizontal=True, key="t00_rows_worked3")`. Live combination per row:
- Row 1: `1·(1,4) + 0·(2,5) + 0·(3,1) = (1,4)`
- Row 2: `-2·(1,4) + 1·(2,5) + 0·(3,1) = (0,-3)`
- Row 3: `0·(1,4) + 0·(2,5) + 1·(3,1) = (3,1)`
Caption (verbatim): "This A is an elimination matrix — the kind you'll use to solve
systems later. Rows 1 and 3 of B pass through unchanged, but row 2 of C is *row 2 of
B minus 2 times row 1* (weights −2, 1, 0). That single subtraction is one step of the
elimination method, written as a matrix."

**Practice (build C one ROW at a time; A · B = C top row with live-fill C; per-row
work stacked top-to-bottom; blank-until-touched; verified answers):**

- **Practice 1 (aided) — A(2×2)·B(2×2):**
  A = [[2,1],[1,3]], B = [[1,2],[4,1]], C = [[6,5],[13,5]].
  Recipes shown:
  `Row 1 = 2·(1, 2) + 1·(4, 1) = ___` (answer 6, 5)
  `Row 2 = 1·(1, 2) + 3·(4, 1) = ___` (answer 13, 5)
- **Practice 2 (unaided) — A(2×3)·B(3×2):**
  A = [[1,0,2],[3,1,1]], B = [[2,1],[1,4],[0,2]], C = [[2,5],[7,9]].
  Row 1 answer (2, 5); Row 2 answer (7, 9).
- **Practice 3 (unaided) — A(3×2)·B(2×3):**
  A = [[1,2],[0,3],[2,1]], B = [[3,1,2],[1,0,4]],
  C = [[5,1,10],[3,0,12],[7,2,8]].
  Row 1 (5, 1, 10); Row 2 (3, 0, 12); Row 3 (7, 2, 8).

## Screen 6 — Column picture (`screen_cols.py`)

**Top-of-screen explanation (verbatim):**
> **Column picture.** Now look at one column of C at a time. The **first column of
> C** is built entirely from the **columns of A** — you take *1 of column 1, 2 of
> column 2, and 3 of column 3* of A and add them up. Those weights (1, 2, 3) are
> exactly the **first column of B**. So each column of B is a recipe, and it mixes
> the columns of A to make the matching column of C. **Column j of C = (column j
> of B) used as weights on the columns of A.**

**Worked example (same shared A/B/C), highlight selector:**
`st.radio("Building:", ["Column 1 of C", "Column 2 of C"], horizontal=True)`.
- "Column 1 of C" highlights column 1 of B (the weights) and all columns of A and
  column 1 of C, and writes:
  `Column 1 of C = 1·(2, 0) + 2·(1, 2) + 3·(3, 1) = (13, 7)`.
- "Column 2 of C" highlights column 2 of B and writes:
  `Column 2 of C = 4·(2, 0) + 5·(1, 2) + 1·(3, 1) = (16, 11)`.
  (Columns of A are (2,0), (1,2), (3,1); column of C is written as a column.)

**Worked Example 2 (column permutation) — own highlight selector:**
A = [[2,1,3],[4,2,5]], B = [[0,1,0],[1,0,0],[0,0,1]], C = [[1,2,3],[2,4,5]].
Read-only, compact; `st.radio("Building:", ["Column 1 of C", "Column 2 of C",
"Column 3 of C"], horizontal=True, key="t00_cols_worked2")`. Weights = column j of B,
applied to columns of A ((2,4),(1,2),(3,5)); result column shown vertically as a
bmatrix. Live combination per column:
- Col 1: `0·(2,4) + 1·(1,2) + 0·(3,5) = (1,2)`
- Col 2: `1·(2,4) + 0·(1,2) + 0·(3,5) = (2,4)`
- Col 3: `0·(2,4) + 0·(1,2) + 1·(3,5) = (3,5)`
Caption (verbatim): "This B is a permutation matrix — each column of C picks exactly
one column of A (weight 1), so multiplying reorders A's columns. Here columns 1 and 2
of A swap."

**Worked Example 3 (diagonal scale) — own highlight selector:**
A = [[2,1,3],[4,2,5]], B = [[1,0,0],[0,1,0],[0,0,2]], C = [[2,1,6],[4,2,10]].
Read-only, compact; `st.radio("Building:", ["Column 1 of C", "Column 2 of C",
"Column 3 of C"], horizontal=True, key="t00_cols_worked3")`. Result column vertical
bmatrix. Live combination per column:
- Col 1: `1·(2,4) + 0·(1,2) + 0·(3,5) = (2,4)`
- Col 2: `0·(2,4) + 1·(1,2) + 0·(3,5) = (1,2)`
- Col 3: `0·(2,4) + 0·(1,2) + 2·(3,5) = (6,10)`
Caption (verbatim): "This B is diagonal, so each column of C is just one column of A
scaled: column 1 unchanged, column 2 unchanged, column 3 doubled (weight 2). A
diagonal B scales each column independently."

**Practice (build C one COLUMN at a time; A · B = C top row with live-fill C;
per-column work side by side; blank-until-touched; SAME three pairs; verified
answers):**

- **Practice 1 (aided) — A(2×2)·B(2×2):** same A, B as Screen 5 Practice 1.
  C columns: col 1 = (6, 13), col 2 = (5, 5).
  Recipes shown:
  `Col 1 = 1·(2, 1) + 4·(1, 3) = ___` (answer 6, 13)
  `Col 2 = 2·(2, 1) + 1·(1, 3) = ___` (answer 5, 5)
- **Practice 2 (unaided) — A(2×3)·B(3×2):**
  columns of A are (1,3), (0,1), (2,1); weights are columns of B.
  Col 1 = (2, 7); Col 2 = (5, 9).
- **Practice 3 (unaided) — A(3×2)·B(2×3):**
  columns of A are (1,0,2), (2,3,1); weights are columns of B.
  Col 1 = (5, 3, 7); Col 2 = (1, 0, 2); Col 3 = (10, 12, 8).

## Screen 7 — Outer products (`screen_outer.py`)

**Top-of-screen explanation (verbatim):**
> **The whole thing at once.** The row picture and the column picture are two
> halves of one idea. Take **column 1 of A** and **row 1 of B** and multiply them
> — a column times a row gives a full 2×2 matrix (an "outer product"). Do the same
> for column 2 of A with row 2 of B, and column 3 with row 3. **Add those three
> matrices and you get C.** So AB is a *sum of simple pieces*, one piece per column
> of A paired with the matching row of B. This is the view that powers the big
> ideas later — it's how PCA and SVD break a matrix into a stack of simple layers.

**Worked example (same shared A/B/C), highlight selector:**
`st.radio("Building:", ["Term 1", "Term 2", "Term 3", "Sum = C"], horizontal=True)`.
- "Term 1" highlights column 1 of A and row 1 of B and shows the outer product
  `(2, 0)ᵀ · (1, 4) = [[2, 8], [0, 0]]`.
- "Term 2": `(1, 2)ᵀ · (2, 5) = [[2, 5], [4, 10]]`.
- "Term 3": `(3, 1)ᵀ · (3, 1) = [[9, 3], [3, 1]]`.
- "Sum = C": show all three term-matrices added:
  `[[2,8],[0,0]] + [[2,5],[4,10]] + [[9,3],[3,1]] = [[13,16],[7,11]] = C`.

**Practice (build each TERM, then the sum; SAME three pairs; verified answers):**

- **Practice 1 (aided) — A(2×2)·B(2×2):** two terms.
  Recipes shown:
  `Term 1 = (2, 1)ᵀ · (1, 2) = ___` (answer [[2,4],[1,2]])
  `Term 2 = (1, 3)ᵀ · (4, 1) = ___` (answer [[4,1],[12,3]])
  `Sum = Term 1 + Term 2 = ___` (answer [[6,5],[13,5]])
- **Practice 2 (unaided) — A(2×3)·B(3×2):** three terms.
  Term 1 [[2,1],[6,3]]; Term 2 [[0,0],[1,4]]; Term 3 [[0,4],[0,2]];
  Sum [[2,5],[7,9]].
- **Practice 3 (unaided) — A(3×2)·B(2×3):** two terms (inner dim = 2).
  Term 1 = (1,0,2)ᵀ·(3,1,2) = [[3,1,2],[0,0,0],[6,2,4]];
  Term 2 = (2,3,1)ᵀ·(1,0,4) = [[2,0,8],[3,0,12],[1,0,4]];
  Sum = [[5,1,10],[3,0,12],[7,2,8]].
  (Note: number of terms = the inner/shared dimension n, NOT the result size —
  a nice thing to have the student notice: Practice 3 makes a 3×3 result from
  just 2 terms.)

## Acceptance checklist (verify before committing)

- [ ] Topic 0 selector shows screens 5, 6, 7 after "4 · Special matrices".
- [ ] All three screens show the SAME worked A/B and the SAME C = [[13,16],[7,11]],
      built three different ways.
- [ ] Shape-rule caption present on every screen, with that screen's concrete shapes.
- [ ] Worked example is read-only and compact; matrices never span the screen.
- [ ] Highlight selector works on each worked example (row/column/term emphasized
      across A, B, C together) and the live combination is written out.
- [ ] Each screen has 3 practice examples, same A/B pairs across screens; Practice 1
      aided (recipe spelled out), Practice 2 and 3 unaided.
- [ ] Every practice builds the WHOLE C in that method's units (rows / columns /
      terms + sum), with per-unit Check and Show solution via the reveal-flag
      pattern; answer boxes use compact editable_matrix with hide_steppers=True.
- [ ] All answer keys match the verified values in this spec.
- [ ] No morph, no graph on these screens.
- [ ] App runs with no import errors (I will run it — do not start the server).
