# Build Spec — Topic 6.5: Putting It Together (Inverse, Transpose, Complete Solution)

> **For the builder (Claude Code):** implement as a per-screen package
> `topics/t06b_consolidate/` registered in `app.py` **between** `t06_spaces` and
> `t07_projection`. Follow `CLAUDE.md`. Reuse the engine (`engine/widgets.py` —
> `editable_matrix`, `scalar_slider`; `engine/plotting.py`) and the Topic 6 /
> Topic 5.5 patterns. Student-facing text below is final copy — implement it,
> don't reword. Straight ASCII quotes in code. Color per-entry INSIDE every
> bmatrix (never `\color{}` wrapping a whole bmatrix — it does not render).

`TITLE = "6.5 · Putting It Together"`, `SLUG = "consolidate"`.

## Why this topic exists

The student has just finished the four fundamental subspaces. Before projection,
they need three pieces of algebra named out loud that earlier topics used but
never stated cleanly: the **inverse** A⁻¹ (and why "matrix division" doesn't
exist), the **transpose** Aᵀ, and the **complete solution** (particular + null).
The topic ends with a rules table that fixes exactly when each tool applies, then
hands off to projection: *when there is no exact solution, find the closest one.*

## Design rules (same as Topic 6)

1. **Viewport blocks.** Vertical stack of self-contained blocks; each fits one
   screen-height. Math LEFT / visual RIGHT via `st.columns([0.5, 0.5])` where a
   visual applies.
2. **Plain words before symbols**, every time.
3. **One interaction max per screen** where it teaches.
4. Tight math: multi-line equation sets as one aligned LaTeX block.
5. Engine dark palette; color code unchanged (column green `#37b24d`, null blue
   `#4dabf7`, row purple `#9775fa`, left-null orange `#f76707`, pivots yellow
   `#ffd43b`).

## Selector

`st.radio` horizontal, key `t06b_screen`:
`["1 · The inverse A⁻¹", "2 · The transpose Aᵀ", "3 · The complete solution", "4 · The rules, and what's next"]`

## OVERVIEW (pinned, verbatim)

> You now know the four spaces hiding inside a matrix. This short topic names
> three tools you've been using without a clean definition — the **inverse**, the
> **transpose**, and the **complete solution** of a system — and ends with one
> table that tells you exactly when each one is allowed. That table is also the
> doorway to the next topic: it shows you the cases where a system has **no exact
> answer at all**, which is precisely the problem projection is built to solve.

---

## Screen 1 — The inverse A⁻¹ ("matrix division" that isn't)

**Module:** `screen_inverse.py` → `render_inverse()`. Keys prefixed `t06b_inv_`.

### Block 1 — There is no matrix division (the algebra, stated)

Left column, verbatim intro:

> **You can't divide by a matrix.** To solve `Ax = b` with ordinary numbers you'd
> divide both sides by A. But there is no such thing as `b / A` — matrix division
> is not defined. Instead we build a matrix that *undoes* A, called the
> **inverse** and written **A⁻¹**. It's defined by one property: `A⁻¹A = I`, the
> identity matrix, which does nothing — the matrix version of multiplying by 1.

Then the solving chain as ONE aligned LaTeX block (verbatim math):

$$\begin{aligned}
Ax &= b \\
A^{-1}(Ax) &= A^{-1}b \\
(A^{-1}A)\,x &= A^{-1}b \\
Ix &= A^{-1}b \\
x &= A^{-1}b
\end{aligned}$$

Bolded + bright-green note directly under it (verbatim):

> **Multiply on the LEFT, both sides.** Matrix multiplication does not commute:
> `A⁻¹b` is not the same as `bA⁻¹` (the second one may not even be a legal size).
> With numbers the order never matters; with matrices it always does. So A⁻¹ goes
> on the *left* of both sides, and the order can't be swapped.

### Block 2 — Watch it solve, and watch it break

`st.columns([0.5, 0.5])`.

- **Left:** `editable_matrix("t06b_inv_A", dim=2, label="A")` and
  `editable_matrix("t06b_inv_b", rows=2, cols=1, label="b")`. Default
  A = [[2, 1], [1, 3]], b = (3, 5) (det = 5, clean; solution x = (0.8, 1.4)).
  Below, computed live:
  - `det A = ...`
  - if det ≠ 0: show `A⁻¹ = [...]` (color each entry, not the bracket), then the
    chain result `x = A⁻¹b = [...]`, then a check line `A x = [...] = b ✓`.
  - if det = 0: show `det A = 0`, no A⁻¹ line, and the break message below.
- **Right:** small live readout, not a plot — render the identity check
  `A⁻¹A = [...]` and confirm it equals I. (A plot is optional; the point here is
  algebraic, so a clean matrix readout is enough. If a visual is wanted, draw the
  two column vectors of A to show det ≠ 0 means they span the plane.)

Break message (verbatim, shown only when det A = 0):

> **det A = 0 — there is no inverse.** When the determinant is zero, no matrix can
> undo A: there is nothing to multiply by, so `x = A⁻¹b` can't even be written.
> This is the same "squashed" case as the singular rockets in Vector Spaces — A
> collapses the plane, and you can't un-collapse it.

### Block 3 — The rule for the inverse (verbatim)

> An inverse exists only when **A is square** (same number of rows and columns)
> **and** its **determinant is not zero**. Square is required because A⁻¹ has to
> undo A from both sides (`A⁻¹A = AA⁻¹ = I`), and only a square matrix can do
> that. Nonzero determinant is required because a zero determinant means A crushes
> space flat, and nothing can bring it back. We'll see in the final table that
> "square and det ≠ 0" is the same as "full rank."

---

## Screen 2 — The transpose Aᵀ (flip rows and columns)

**Module:** `screen_transpose.py` → `render_transpose()`. Keys prefixed `t06b_tr_`.

### Block 1 — What the transpose is (verbatim)

> The **transpose** of a matrix, written **Aᵀ**, is the matrix you get by flipping
> it across its diagonal — every **row** of A becomes a **column** of Aᵀ. If A is
> 2 rows by 3 columns, Aᵀ is 3 rows by 2 columns. The entry in row i, column j of
> A lands in row j, column i of Aᵀ. That's the whole definition. Unlike the
> inverse, the transpose **always exists and the matrix does not have to be
> square.**

### Block 2 — Flip it yourself

`st.columns([0.5, 0.5])`.

- **Left:** `editable_matrix("t06b_tr_A", rows=2, cols=3, label="A")`, default
  A = [[1, 2, 3], [4, 5, 6]].
- **Right:** live `Aᵀ` rendered with `editable_matrix(..., editable=False,
  value=A.T, rows=3, cols=2, label="A^{T}")` (or a static bmatrix). Caption below:
  "2×3 becomes 3×2. Row 1 of A — (1, 2, 3) — is now column 1 of Aᵀ."

Highlight the shape label live: show `A is m×n = 2×3`, `Aᵀ is n×m = 3×2`.

### Block 3 — Symmetry, and why the transpose matters next (verbatim, bolded+colored lead)

> **A symmetric matrix is one that equals its own transpose: A = Aᵀ.** That can
> only happen for a square matrix, and it means the matrix is a mirror image
> across its diagonal — the entry in row i, column j equals the entry in row j,
> column i.

Then the bridge (verbatim):

> Here's why the transpose is the last tool we needed before projection. Take any
> matrix A — any shape — and multiply it by its own transpose to form **AᵀA**.
> That product is always **square** and always **symmetric**, no matter what shape
> A started as. In the next topic, when a system `Ax = b` has no exact answer,
> we'll multiply both sides by Aᵀ to turn it into a square, solvable system —
> `AᵀA x̂ = Aᵀb` — and read the closest answer off of it. You don't need that
> formula yet. Just remember: **Aᵀ is what makes a tall, unsolvable system square.**

Optional live confirm (nice-to-have): compute AᵀA from the Block-2 matrix and show
it is square and symmetric.

---

## Screen 3 — The complete solution (particular + null)

**Module:** `screen_complete.py` → `render_complete()`. Keys prefixed `t06b_comp_`.

### Block 1 — The idea in words (verbatim)

> When a system has **infinitely many** solutions, we don't list them one by one —
> we write them with a formula called the **complete solution**. It has two parts
> added together: one **particular solution** — any single point that satisfies
> `Ax = b` — plus the **entire null space** of A, the directions you can move
> without changing the result. In symbols:
>
> **x = x_particular + (null-space part)**
>
> You already met the null-space part in Vector Spaces: those are the inputs A
> sends to zero. Adding any of them to a working solution gives another working
> solution, because A turns that added piece into zero and leaves `b` unchanged.

### Block 2 — Work one (student fills the null part)

Use a rank-deficient system with a clean one-dimensional null space.

**Verified case (locked — these exact numbers, confirmed with sympy):**
A = [[1, 2, 2], [2, 4, 5]], b = **(6, 14)**.
- RREF of [A | b] = [[1, 2, 0, 2], [0, 0, 1, 2]] → pivots in columns **1 and 3**,
  free variable **x₂**. rank r = 2, m = 2, n = 3.
- Particular (set free x₂ = 0): **x_p = (2, 0, 2)**. Check A·(2,0,2) = (6, 14) = b ✓.
- Null space (1-D, dim = n − r = 1): direction **v = (−2, 1, 0)**.
  Check A·(−2, 1, 0) = (0, 0) ✓.
- Complete solution: **x = (2, 0, 2) + x₂·(−2, 1, 0)**.

> **BUILDER:** the numbers above are final. Still compute them live in code (RREF,
> x_particular, null direction) rather than hard-coding display strings, but they
> must come out to exactly these values. Reuse the Screen-3 (null) fill-in pattern
> from `topics/t06_spaces/screen_null.py`: show
> `x = [x_p] + x2·[ _ ; _ ; _ ]` with the null vector entries as the blanks the
> student fills, live-check `A·v = 0`, and reveal the clean complete-solution
> LaTeX on correct. **Keep the three components close together** (the tight inline
> layout from screen_null — not spread across the width).

### Block 3 — Why both parts (verbatim)

> The particular solution pins you to the right "height" — it makes `Ax` equal `b`.
> The null-space part lets you slide along every direction that doesn't change the
> answer. One solution plus all the ways to move without consequence equals every
> solution there is. When the null space is just the zero vector (nothing gets
> crushed), the null part disappears and the particular solution is the *only*
> solution — that's the one-answer case.

---

## Screen 4 — The rules, and what's next

**Module:** `screen_rules.py` → `render_rules()`. Keys prefixed `t06b_rules_`.
Tables render as **markdown** (not `st.table` — pandas/NumPy version crash).

### Block 1 — Intro (verbatim)

> Here is the whole topic on one screen. `m` is the number of **rows** (equations),
> `n` the number of **columns** (unknowns), and `r` the **rank** — the number of
> genuinely independent rows, the pivots you find by elimination. Every rule about
> inverses, solvability, and the four spaces is really a statement about how `m`,
> `n`, and `r` compare.

### Block 2 — Tool rules table (markdown, verbatim)

| Tool | Shape rule | Extra condition | What you get |
|---|---|---|---|
| **A⁻¹** (inverse) | square only — m = n | det ≠ 0 (same as r = n) | undoes A: x = A⁻¹b, exactly one answer |
| **Aᵀ** (transpose) | any shape — m×n becomes n×m | none | always exists; AᵀA is square & symmetric |
| **AᵀA** | always square (n×n) | — | the square system projection will solve |

### Block 3 — Solution-count table (markdown, verbatim — VERIFIED)

| Rank situation | Shape of A | How many solutions to Ax = b | Why |
|---|---|---|---|
| **r = m = n** | square, full rank | **exactly one**, for every b | invertible, det ≠ 0 |
| **r = n < m** | tall, full column rank | **0 or 1** | null space = {0}; solvable only if b is in the column space |
| **r = m < n** | wide, full row rank | **infinitely many**, for every b | always solvable; free variables = n − r > 0 |
| **r < m and r < n** | rank-deficient | **0 or infinitely many** | 0 if b is unreachable, otherwise free variables remain |

Footer facts directly under the table (verbatim):

> - Free variables = null-space dimension = **n − r**.
> - Left-null-space dimension = **m − r**.
> - A is invertible **exactly when m = n = r** — square and full rank, which is the
>   same as det ≠ 0.

### Block 4 — Bridge to projection (verbatim, `st.info` or bolded+colored)

> Look at the rows that say **"0 or 1"** and **"0 or ..."** — the cases where
> `Ax = b` can have **no solution at all**. That happens whenever the target `b`
> sits outside the column space: no combination of A's columns can reach it, so no
> exact answer exists. That's not a dead end — it's the whole next topic. When we
> can't hit `b` exactly, we find the point in the column space that comes
> **closest**, using a perpendicular shadow. That's projection, and the Aᵀ you just
> learned is the tool that builds it.

---

## Wiring

1. New package `topics/t06b_consolidate/` with `__init__.py` exposing
   `TITLE = "6.5 · Putting It Together"`, `SLUG = "consolidate"`, the OVERVIEW,
   and `render()` with the 4-screen `st.radio` (key `t06b_screen`) as above.
2. In `app.py`: import `t06b_consolidate` and insert it in `TOPICS` **between**
   `t06_spaces` and `t07_projection`.
3. Reuse `editable_matrix` (non-square via rows/cols), the screen_null fill-in
   pattern, and the standard color code. No engine changes expected.

## Acceptance checklist

- [ ] New topic button "6.5 · Putting It Together" appears between Vector Spaces
      and Projection.
- [ ] Screen 1 states "no matrix division", shows the five-line solving chain, the
      LEFT-multiply/non-commutative note in bold green, solves the default system
      live, and shows the det = 0 break message when the determinant is zeroed.
- [ ] Screen 2 flips a 2×3 into a 3×2 live, labels the shapes m×n → n×m, defines
      symmetric (A = Aᵀ), and gives the AᵀA bridge.
- [ ] Screen 3 shows x = particular + null, student fills the null direction with
      the tight inline layout, A·v = 0 is checked live, complete solution revealed
      on correct. Numbers re-verified by the builder.
- [ ] Screen 4 renders both markdown tables verbatim, the footer facts, and the
      projection bridge.
- [ ] All inverse/solution math computed live (not hard-coded); per-entry coloring
      inside bmatrix; no `use_container_width`.
