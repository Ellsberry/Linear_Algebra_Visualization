# Build Spec — Topic 5.5, [A | I] Inverse-by-Elimination screen (NEW)

**Status:** approved design, not yet built. A NEW screen added to the
`topics/t05b_elimination/` package. The Topic 4 <-> 5.5 bridge. Follow `CLAUDE.md`.

## What this screen teaches

How you actually COMPUTE an inverse (Gauss-Jordan inversion). Topic 4 introduced
A^-1 as a concept; here the student sees the method: augment A with the identity
to form `[A | I]`, then row-reduce until the LEFT block becomes I -- at which
point the RIGHT block has become A^-1.

New idea vs every other Topic 5.5 screen: those reduce to TRIANGULAR form (zeros
below the diagonal) then back-substitute. This screen reduces all the way to
REDUCED ROW ECHELON FORM (RREF) -- zeros below AND above the diagonal, pivots
scaled to 1 -- so the left block literally becomes the identity. That full
reduction is genuinely new engine logic.

## The payoff insight (show at the end)

Why does the right side become A^-1? The sequence of row operations that turns A
into I is, together, multiplication by A^-1 (that's what "reduces A to I" means).
Those SAME operations applied to the identity on the right produce A^-1 * I =
A^-1. So the right half becomes the inverse "for free." Surface this once the
student reaches `[I | A^-1]`.

## Examples (verified numerically -- do not change these facts)

**Example 1 -- clean integer inverse** (the "watch it work" example):
```
A = [2 1 1]      A^-1 = [ 0  0  1]
    [1 3 2]             [-2  1  3]
    [1 0 0]             [ 3 -1 -5]
```
det = -1. Integer inverse (no fractions) -- ideal first example. Reduces
`[A|I] -> [I|A^-1]` in ~9 Gauss-Jordan steps. A * A^-1 = I verified.

**Example 2 -- fractional inverse** (the "still just elimination" example):
```
A = [2 0 0]      A^-1 = [ 1/2    0    0 ]
    [1 2 0]             [-1/4   1/2   0 ]
    [1 1 2]             [-1/8  -1/4  1/2]
```
det = 8. Fractional inverse -- shows inverses routinely involve fractions (from
scaling by pivots). The engine uses `fractions.Fraction`, so these render as
exact fractions (1/2, -1/4, ...), NOT decimals. ~6 steps. A * A^-1 = I verified.

**Example 3 -- singular (no inverse)** (optional third, strong concept):
```
A = [1 2 3]
    [2 4 6]    det = 0
    [1 0 1]
```
During reduction a pivot column ends up with no nonzero pivot -> the left block
CANNOT become I -> the method DETECTS that A has no inverse. Ties back to
Topic 3/4: det = 0 => no inverse. Show a clear "no inverse" message instead of a
right-block answer.

## The engine -- a DEDICATED [A|I] RREF reducer (NOT the triangular workbench)

Build a separate reducer (do NOT modify the existing triangular `workbench` --
the four working screens depend on it). The [A|I] reducer operates on an n x 2n
augmented matrix (n=3 here) of `Fraction`s and supports:

- **Row operations** (reuse the existing op set / callbacks where possible):
  swap two rows, scale a row by a constant, add a multiple of one row to another.
  Manual mode + Undo/Reset, like the workbench.
- **Guided "Do one step"** and **"Run to reduced form"** that perform full
  GAUSS-JORDAN to RREF (NOT just triangular):
  1. For each pivot column p: if pivot is 0, swap up a row with a nonzero entry.
  2. Scale the pivot row so the pivot becomes 1.
  3. Eliminate that pivot column in ALL OTHER rows (above AND below), not just
     below.
  Continue until the left n x n block is the identity (or a pivot column has no
  pivot -> singular).
- **Singular detection:** if any pivot column has no available nonzero pivot, stop
  and report "A has no inverse (singular)".
- **Completion detection:** when the left block == I, announce success and the
  right block IS A^-1.
- Use `Fraction` throughout so fractional inverses display exactly.

### Step-description formatting (note)
When scaling a row by the reciprocal of a fraction, format the factor cleanly --
e.g. multiplying R2 by the reciprocal of 5/2 should read "x 2/5", NOT "1/5/2".
Avoid nested-fraction strings in the operations log.

## Interaction (NO equation_builder -- there is no modeling step)

Unlike Logistics/Circuit, the student does NOT write equations. Their activity is
PERFORMING the reduction:
1. The screen shows `[A | I]` (a 3x6 augmented matrix, vertical divider before
   the identity block).
2. The student applies row operations (manual, or "Do one step" / "Run to reduced
   form") to drive the LEFT 3x3 block toward I.
3. The RIGHT block transforms in lockstep; when the left becomes I, the right is
   A^-1.
4. Show a verification: A * (right block) = I (optional "Verify" affordance).
5. Highlight pivots as the reduction proceeds (ties into the pending pivot-
   highlighting item -- nice to do here).

## Layout -- WIDE-MATH (like the existing workbench screens)

The `[A|I]` matrix is 3x6 -- the widest in the project. Use the workbench's
wide-math split: controls in a NARROWER left column, the wide augmented matrix in
a WIDER right column (e.g. `st.columns([1, 1.3])`), NOT the standard half/half
graph layout (there is no graph). Render `[A|I]` with a clear vertical divider
between the A block and the I/inverse block (an augmented-array LaTeX with
`{ccc|ccc}` column spec).

- Example selector at top (Example 1 integer / Example 2 fractional /
  Example 3 singular).
- Framing/intro text: what `[A|I] -> [I|A^-1]` does and why.
- The reducer (controls + wide matrix).
- On completion: the "why the right side became A^-1" payoff, the boxed A^-1, and
  the A*A^-1=I check. On singular: the "no inverse" explanation.

## Reuse vs new
- REUSE: the row-operation control UI pattern and (where clean) the op callbacks;
  the augmented-matrix LaTeX rendering style; `Fraction`-based arithmetic; the
  wide-math column layout.
- NEW: the full Gauss-Jordan-to-RREF reduction (eliminate above + below, scale
  pivots to 1), singular detection, completion detection, the `[A|I]` initial
  augmentation, and the inverse-extraction + verification.

## Acceptance checklist
- [ ] Screen shows `[A|I]` (3x6) with a clear divider; wide-math layout.
- [ ] Manual row ops + Undo/Reset work; "Do one step" / "Run to reduced form"
      perform full Gauss-Jordan to RREF (above AND below).
- [ ] Example 1 reduces to `[I | A^-1]` with the verified integer inverse.
- [ ] Example 2 reduces to the verified fractional inverse, shown as exact
      fractions.
- [ ] Example 3 (singular) is DETECTED -> "no inverse" message, no false answer.
- [ ] On completion: the "why the right side is A^-1" insight, the boxed inverse,
      and an A * A^-1 = I check.
- [ ] Step-description formatting is clean (no nested "1/5/2" strings).
- [ ] The existing triangular workbench and the four working screens are
      UNCHANGED (dedicated reducer, not a modification of `workbench`).
