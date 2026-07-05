# Build Spec — Topic T00: Matrix Operations & Multiplication (NEW standalone topic)

**Status:** approved design, not yet built. NEW standalone topic BEFORE Topic 1.
Follow `CLAUDE.md`. Uses ONLY the clean bracket `editable_matrix` widget in a
COMPACT layout (never the wide stretched style).

## Why this topic exists
The app uses matrix operations everywhere but never TEACHES them. T00 introduces
the operations and gives hands-on practice before they appear inside applications.

## GLOBAL layout rules (every screen)
- **Compact matrices:** matrices render tight (small bracketed grids), NOT
  stretched across the page. Constrain each matrix to a narrow column/container.
- **Side by side:** where it fits, show an example's matrices (and multiple
  examples) side by side.
- **Practice screens show ALL examples at once** — no radio/selector to pick one;
  display them together on the page.
- **Widget:** `editable_matrix`. Read-only operands via `editable=False, value=`;
  editable answer via `editable=True`. Compact number_input cells (collapsed
  labels, narrow columns).
- **Numbers:** entries 1-9. At most ONE zero, and only in example 2 or 3 (never
  ex1/ex4). All examples below are VERIFIED.

## Practice interaction (screens 0 practice items, 1, 2, 3)
Student sees fixed operands, computes the result mentally, types into an editable
answer matrix, clicks **Check** (per-cell validation; wrong cells flagged WITHOUT
revealing the number). A **Show solution** reveals the correct result.

---

## Screen 0 — Operations Overview
Describe the seven operations: what each is, why it matters, real-world examples.
Four simple ops get inline PRACTICE; matrix-mult is described (practice deferred
to Screens 1-3); inverse & division are described only (covered in Topics 4/5.5).

For each operation: a short "What it is", "Why it matters", and 2-4 real examples
(bullets). Text below is the source content (keep it tight).

1. **Addition — Combine Systems.** Element-by-element sum, same dimensions.
   Merges systems/datasets/transformations. (adjacency matrices, blend images,
   combine perturbations.) **PRACTICE.**
2. **Subtraction — Compare Systems.** Element-by-element difference. Shows how two
   systems differ (residuals, change detection). **PRACTICE.**
3. **Scalar Multiplication — Scale a Transformation.** Multiply every entry by k.
   Uniformly scales effect. (brightness, stretching, scaling coefficients.)
   **PRACTICE.**
4. **Matrix Multiplication — Compose Transformations.** Row-by-column; A(m×n)·B(n×p)
   = m×p. Represents doing one transformation after another. (graphics pipeline,
   neural net layers, input-output economics, robotics.) **Described here;
   practiced on Screens 1-3.**
5. **Transpose — Flip Perspective.** Swap rows and columns. Essential for dot
   products, projections, symmetry. **PRACTICE.**
6. **Inverse — Undo a Transformation.** A⁻¹ with A·A⁻¹=I; exists iff det≠0. Solves
   Ax=b, undoes transforms. **Described only** (see Topics 4 & 5.5).
7. **Division (via inverse) — Solve Relationships.** No direct division;
   A/B = A·B⁻¹. **Described only.**

### Screen 0 verified practice examples (compact, all shown, side by side)
Addition (3): 
  ex1 [[2,3],[5,1]]+[[4,1],[2,6]]=[[6,4],[7,7]]
  ex2 [[7,0],[3,4]]+[[1,5],[6,2]]=[[8,5],[9,6]]
  ex3 [[3,8],[2,0]]+[[5,1],[7,9]]=[[8,9],[9,9]]
Subtraction (3):
  ex1 [[8,6],[7,9]]-[[3,2],[5,4]]=[[5,4],[2,5]]
  ex2 [[9,0],[6,7]]-[[4,3],[2,5]]=[[5,-3],[4,2]]
  ex3 [[7,8],[9,0]]-[[1,3],[4,2]]=[[6,5],[5,-2]]
Scalar (3):
  ex1 2*[[3,4],[1,5]]=[[6,8],[2,10]]
  ex2 3*[[2,0],[4,1]]=[[6,0],[12,3]]
  ex3 2*[[6,3],[0,7]]=[[12,6],[0,14]]
Transpose (3):
  ex1 [[2,7],[3,5]]^T=[[2,3],[7,5]]
  ex2 [[4,0],[6,1]]^T=[[4,6],[0,1]]
  ex3 [[8,3],[2,9]]^T=[[8,2],[3,9]]

(Subtraction ex2/ex3 produce one negative each — intentional, teaches signed
results. Scalar products exceed 9 (that's fine; only INPUT entries are 1-9.))

---

## Screen 1 — Rules + four 2×2 · 2×2 (PRACTICE, all shown)
Lead with the row·column rule + shape rule (2×2·2×2→2×2). Four examples:
  Ex1 [[2,3],[1,4]]·[[1,2],[3,1]]=[[11,7],[13,6]]
  Ex2 [[4,0],[2,3]]·[[2,1],[3,5]]=[[8,4],[13,17]]
  Ex3 [[3,1],[2,5]]·[[4,2],[1,0]]=[[13,6],[13,4]]
  Ex4 [[2,4],[3,2]]·[[1,3],[2,1]]=[[10,10],[7,11]]

## Screen 2 — four 3×3 · 3×3 (PRACTICE, all shown)
  Ex1 [[1,2,1],[3,1,2],[2,1,3]]·[[2,1,1],[1,3,2],[1,2,1]]=[[5,9,6],[9,10,7],[8,11,7]]
  Ex2 [[2,1,0],[1,3,2],[4,1,1]]·[[1,2,3],[2,1,1],[3,1,2]]=[[4,5,7],[13,7,10],[9,10,15]]
  Ex3 [[3,1,2],[2,4,1],[1,2,0]]·[[1,3,2],[2,1,4],[3,2,1]]=[[11,14,12],[13,12,21],[5,5,10]]
  Ex4 [[1,2,3],[4,1,2],[2,3,1]]·[[2,1,1],[1,2,3],[3,1,2]]=[[13,8,13],[15,8,11],[10,9,13]]

## Screen 3 — rectangular (PRACTICE, all shown) + shape rule
Teach: inner dims must match (n==p); result is m×q.
  1. 2×3·3×2=2×2: [[1,2,3],[4,1,2]]·[[2,1],[1,3],[2,1]]=[[10,10],[13,9]]
  2. 5×3·3×2=5×2: [[1,2,1],[3,1,2],[2,2,1],[1,3,2],[2,1,3]]·[[2,1],[1,2],[3,1]]
       =[[7,6],[13,7],[9,7],[11,9],[14,7]]
  3. 3×3·3×1=3×1 (Ax=b): [[1,2,3],[2,1,4],[3,2,1]]·[[2],[1],[3]]=[[13],[17],[11]]
  4. NON-CONFORMABLE 2×2·3×3: inner dims 2≠3. Show both, NO answer grid; message:
     "Can't multiply — A has 2 columns but B has 3 rows; inner dimensions must
     match."
NOTE: `editable_matrix` takes a single `dim` (square). Screen 3 needs RECTANGULAR
support — extend the widget to accept rows≠cols (e.g. add `cols` param, or a new
`editable_matrix_rect`). Decide at build time; keep square callers unchanged.

## Screen 4 — Special matrices (DEFINITIONS + why + example; NOT practice)
Identity (multiplying by I is unchanged — the "1" of mult), upper-triangular
(instant back-substitution; ties to 5.5), RREF (end state of elimination; reads
off solutions/inverse; ties to [A|I]). Show small example matrices read-only.

## Nav placement
Register in `app.py` `TOPICS` list FIRST (before t01_vectors). Module has
`TITLE = "0 · Matrix operations"` and `render()`.

## Acceptance checklist
- [ ] T00 appears first in nav.
- [ ] All matrices use compact `editable_matrix` (no stretched style); examples
      side by side where sensible.
- [ ] Screen 0: 7 operations described; addition/subtraction/scalar/transpose have
      inline practice; all practice examples shown at once.
- [ ] Screens 1-3: all examples shown at once (no selector); practice with
      per-cell Check + Show solution.
- [ ] Products match the verified values above; inputs 1-9, one zero only in ex2/3.
- [ ] Screen 3 teaches shape rule; rejects non-conformable pair with a message.
- [ ] Screen 4: definition+why+example for identity/upper-triangular/RREF.
