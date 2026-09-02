# Build Spec — Topic 5.5, NEW Screen 3: Determinant Calculation

> **For the builder (Claude Code):** this adds ONE new screen to the EXISTING
> Topic 5.5 package (`topics/t05b_elimination/`) at selector position 3, and
> renumbers the current screens 3-7 up to 4-8. New module:
> `topics/t05b_elimination/determinant.py` exposing `render_determinant()`.
> Follow `CLAUDE.md`. Student-facing text below is FINAL COPY — implement verbatim,
> do not reword. Straight ASCII quotes in code. This screen is STATIC (no workbench,
> no interaction) — it is a worked demonstration.

## Selector change (in topics/t05b_elimination/__init__.py)

New order (the new screen is 3; everything from the old 3 shifts up by one):
```
1 · Augmented Matrix
2 · Inverse by elimination
3 · Determinant Calculation        <- NEW
4 · Infinite and No Solutions      (was 3)
5 · Logistics (one plan)           (was 4)
6 · Logistics (many plans)         (was 5)
7 · Smoothie                       (was 6)
8 · Circuit                        (was 7)
```

Dispatch changes:
- Add `from .determinant import render_determinant`.
- "3 ..." -> render_determinant().
- "4 ..." -> render_infinite_nosolution() (was "3").
- "5 ..." -> _example_two_a() (was "4").
- "6 ..." -> _example_two() (was "5").
- "7 ..." -> render_smoothie() (was "6").
- "8 ..." -> _example_three() (was "7").
- IMPORTANT: update the `_eb_keys` dict labels to the NEW numbers:
  "5 · Logistics (one plan)" -> ("t05b_e2a", 7),
  "6 · Logistics (many plans)" -> ("t05b_e2", 7),
  "8 · Circuit" -> ("t05b_e3", 5).
  (The session keys t05b_e2a / t05b_e2 / t05b_e3 stay the same; only the label
  numbers that index them change.)

No other screen file's internals change — only the selector labels and dispatch.

## The screen: render_determinant()

A vertical stack of blocks (this topic's blocks may just flow top to bottom; the
worked example uses math-left / matrix-right where noted). Verbatim copy follows.

### Block 1 — what a determinant is (text only, verbatim)

> **Determinant Calculation.** The determinant is a single number you can compute
> from a square matrix, and it tells you whether the matrix can be undone. When the
> determinant is zero, the matrix squashes space flat and has no inverse; when it is
> not zero, the matrix can be reversed. You met determinants back in Topic 3 — this
> screen is about how to actually calculate one, especially for big matrices.

### Block 2 — the small cases, formulas shown (verbatim + LaTeX)

Verbatim text:
> Here are the formulas again from Topic 3. For a 2 by 2 matrix, multiply the two
> numbers on the main diagonal and subtract the product of the other two. For a 3 by
> 3, there is a longer formula built from three smaller 2 by 2 determinants combined
> with alternating plus and minus signs.

Then two st.latex lines (show the matrices in brackets and the formulas, labeled):
  det [[a, b],[c, d]] = ad - bc      (2D)
  det [[a,b,c],[d,e,f],[g,h,i]] = a(ei - fh) - b(di - fg) + c(dh - eg)   (3D)

Then verbatim:
> The 3 by 3 formula is really just the 2 by 2 formula used three times. It works —
> but notice it is already getting complicated, and this is only a 3 by 3.

### Block 3 — why the official method falls apart (verbatim)

> The formula for the 3 by 3 came from a method called **cofactor expansion**: to
> find the determinant, you break the matrix into smaller matrices, find their
> determinants, and combine them. Those smaller matrices break into even smaller
> ones, and so on. It always works — but the amount of work explodes as the matrix
> grows.
>
> Here is how fast it explodes. A 3 by 3 needs about 6 steps. A 4 by 4 needs about
> 24. A 10 by 10 needs over 3 million. And a 20 by 20 matrix — still small by
> real-world standards — needs about 2,400,000,000,000,000,000 steps (that is 2.4
> quintillion). Even a computer doing a billion steps every second would take about
> 77 years to finish. Cofactor expansion is simply not usable for matrices of any
> real size.

(Optional: render the counts as a small 4-row table — 3x3: ~6, 4x4: ~24,
10x10: ~3,600,000, 20x20: ~2.4 quintillion (~77 years at a billion/sec). Keep it
compact; the prose already states them.)

### Block 4 — the method that works: elimination (verbatim)

> There is a far better way, and you already know most of it: **elimination** — the
> same row operations you used to solve systems. If you use elimination to turn the
> matrix into upper-triangular form (all zeros below the diagonal), the determinant
> is the product of the numbers left on the diagonal, with two small adjustments you
> keep track of as you go. That same 20 by 20 matrix takes only about 2,600 steps
> this way — done instantly instead of in 77 years.
>
> The two adjustments come from the row operations. Two of the three operations
> change the determinant, so you track them:
>
> - **Adding a multiple of one row to another does not change the determinant at
>   all.** This is the workhorse move, and it is free.
> - **Swapping two rows flips the sign of the determinant.** Every swap multiplies
>   your answer by −1, so you count the swaps: an even number leaves the sign alone,
>   an odd number flips it.
> - **Multiplying a row by a number k multiplies the determinant by that same k.** So
>   if you scale a row by k along the way, you divide your final answer by k to undo
>   it.
>
> Keep those three rules in mind and elimination gives you the determinant quickly,
> even for enormous matrices.

### Block 5 — worked 4 by 4 example (verbatim text + LaTeX matrices)

Matrix (VERIFIED): A = [[0,1,1,2],[1,2,3,1],[2,1,1,0],[1,1,2,3]], det = 8.
Elimination path (VERIFIED): swap R1<->R2 (sign -> -1), clear below with
add-multiple moves (no det change), reach upper-triangular with diagonal
(1, 1, -2, 4), product = -8, times the sign -1 = 8.

Layout: intro sentence, then the steps as verbatim text each followed by the
relevant st.latex matrix (show the matrix state after each stage). Math can be a
single column (matrices are 4x4, wide) or math-left / current-matrix-right.

Verbatim intro:
> Let's find the determinant of this 4 by 4 matrix by elimination. Notice the
> top-left entry is 0, so we cannot use the first row to clear the column below it
> yet — we need to swap first.

Show A as a bracketed 4x4 matrix.

> **Step 1 — swap.** Swap row 1 and row 2 so the top-left corner is no longer zero.
> That is one row swap, so we remember to flip the sign once (multiply the final
> answer by −1).

Show the matrix after the swap:
  [[1,2,3,1],[0,1,1,2],[2,1,1,0],[1,1,2,3]]

> **Step 2 — eliminate.** Now use "add a multiple of a row" moves to clear
> everything below the diagonal. These moves do not change the determinant, so no
> bookkeeping is needed for them. After clearing, the matrix is upper-triangular with
> 1, 1, −2, and 4 on its diagonal.

Show the upper-triangular result:
  [[1,2,3,1],[0,1,1,2],[0,0,-2,4],[0,0,0,4]]
(with the diagonal entries 1, 1, -2, 4 highlighted, e.g. \color{#ffd43b}).

> **Step 3 — multiply the diagonal.** Multiply the diagonal entries:
> 1 × 1 × (−2) × 4 = −8.
>
> **Step 4 — apply the sign.** We made one swap, so we flip the sign:
> (−1) × (−8) = 8. The determinant is 8.
>
> We never scaled a row, so there was nothing to divide out. If we had scaled a row
> by some number, we would divide the final answer by that number too.

Show the final result line prominently (st.latex or st.success):
  det(A) = (-1) × (1 × 1 × (-2) × 4) = (-1) × (-8) = 8

### Block 6 — closing (verbatim)

> So the determinant of a big matrix is not found by the textbook formula — it is
> found by elimination, reading the answer off the diagonal and adjusting for any
> swaps and scaling. It is the same elimination you already know, doing a second job.

## Reuse / new

- NEW: `topics/t05b_elimination/determinant.py` with `render_determinant()`.
- Uses only st.markdown / st.latex (and optionally a small st.table for the counts).
  No workbench, no engine plotting, no interaction. All matrices as bracketed LaTeX
  (bmatrix). Highlight the final diagonal with \color{#ffd43b} to match the pivot
  color used elsewhere.
- Update __init__.py selector + dispatch + _eb_keys labels as specified above.

## Acceptance checklist

- [ ] Selector shows 8 screens; "3 · Determinant Calculation" between Inverse (2) and
      Infinite/No Solutions (4); old 3-7 now 4-8; dispatch routes each correctly.
- [ ] _eb_keys labels updated to the new numbers (5/6/8) so equation-builder clearing
      still works on the Logistics and Circuit screens.
- [ ] Block 2 shows both formulas as bracketed matrices with (2D)/(3D) labels.
- [ ] Block 3 states the operation counts including 20x20 = 2.4 quintillion / 77 years.
- [ ] Block 4 states all three row-operation rules (add = no change, swap = flip sign,
      scale by k = divide by k); the word "almost" does NOT appear.
- [ ] Block 5 worked 4x4: A=[[0,1,1,2],[1,2,3,1],[2,1,1,0],[1,1,2,3]], one swap,
      diagonal (1,1,-2,4), det = 8, all matrices shown, sign logic correct.
- [ ] All student-facing text verbatim; no interaction on this screen.
