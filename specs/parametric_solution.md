# Build Spec -- Parametric General-Solution Engine (shared)

## Purpose
An engine-level helper that takes a linear system (augmented matrix + n_unknowns) and
returns its general solution in parametric form: X = particular + sum over free vars of
(free_var * direction_vector). Reused by multiple Topic 5.5 screens (Infinite/No
Solutions now; a smoothie "solution space" screen later). Must handle ANY number of
free variables (0, 1, 2, 3+), and detect no-solution.

## Where
New module engine/parametric.py. Uses sympy for exact rational arithmetic (clean
fraction display like 3/2, not 1.50). Add "sympy>=1.12" to requirements.txt.

## Input
- M: the augmented matrix as the workbench stores it (list of lists of floats; the
  last column is b; n_unknowns coefficient columns before it).
- n_unknowns: int.
- var_name: str = "x" (parameter/variable label base; the smoothie screen passes "f").

## Behavior
1. Convert M's floats to exact sympy Rationals (use sp.nsimplify or Rational(str(...))
   with a tolerance so 1.5 -> 3/2, 0.3333 -> 1/3 cleanly; document the approach).
2. Compute RREF of the augmented matrix.
3. Detect the three cases:
   - NO SOLUTION: a row with all-zero coefficients but nonzero b -> return a result
     object marked no_solution.
   - UNIQUE: zero free variables -> particular vector only, no directions.
   - INFINITE: >=1 free variable -> particular + one direction vector per free var.
4. Free variables are the non-pivot columns; label each with its real 1-based index
   using var_name (e.g. x3, or f3/f4/f5), NOT generic t1,t2.

## Output (a small dataclass or dict)
- status: "unique" | "infinite" | "no_solution"
- particular: list of Rationals (length n_unknowns) [for unique/infinite]
- free_vars: list of 1-based indices that are free
- directions: list of (free_index, direction_vector_as_list_of_Rationals)
- n_free: int

## Render helper (same module)
parametric_latex(result, var_name="x") -> a LaTeX string in the stacked-vector format:
  X = [x1;...;xn] = particular_col  + x_i * dir_col_i + x_j * dir_col_j + ...
matching this shape (one particular column plus one t*(vector) term per free var,
each rendered as a bmatrix column; use the real variable index as the scalar label).
For no_solution, return a short LaTeX/text stating no solution exists.
For unique, render X = the particular column only.

## Reuse / consumers (not built here)
- Infinite/No Solutions screen: call with its 3x3 system, var_name="x".
- Future smoothie screen: 5-unknown system, var_name="f" (has 3 free vars).

## Acceptance
- [ ] engine/parametric.py exists; sympy added to requirements.txt.
- [ ] Returns correct particular + direction vectors for a 1-free-var system and a
      3-free-var system; fractions display exactly (e.g. 3/2).
- [ ] Detects no-solution and unique correctly.
- [ ] parametric_latex renders the stacked X = point + sum t*(dir) format with real
      variable indices as scalars.
