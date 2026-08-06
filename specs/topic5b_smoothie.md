# Build Spec — Topic 5.5, Example 7: Smoothie (solution space / free variables)

> **SCOPE.** ONE new screen in Topic 5.5, "Smoothie", at selector position 7. Reuses
> the workbench engine (topics/t05b_elimination/workbench.py) AND the parametric engine
> (engine/parametric.py). Does not modify other screens. Own spec (living -- may be
> extended). Companion one-line edit to specs/topic5b_elimination.md adds it to the
> selector at position 7.

## What it teaches
A real system with MORE unknowns than independent equations, so the answer is not a
single point but a whole SOLUTION SPACE. Five ingredient adjustments constrained by
redundant rules collapse to 2 real constraints, leaving 3 FREE VARIABLES -- three
independent "adjustment patterns." This is the multi-free-variable payoff of the
parametric engine (Example 3 had one free variable; this has three).

## The story
You make smoothies and want to change a recipe while keeping Total volume and Total
sweetness unchanged. Each ingredient's change is an unknown f1..f5. The constraints
produce 5 equations, but several are redundant, so many different ingredient tweaks
satisfy them.

Ingredient legend (show above the math, compact):
  f1 = strawberries, f2 = bananas, f3 = yogurt, f4 = milk, f5 = honey

## The system (homogeneous -- every equation = 0, since changes must net out)
  f1 + f2 + f3 + f4 + f5   = 0
  f1 - f2 + f3 - f4 + 2 f5 = 0
  2 f1 + 2 f3 + 3 f5       = 0
  f1 + 3 f2 + f3 + 3 f4    = 0
  7 f1 - f2 + 7 f3 - f4 + 11 f5 = 0

Matrix A (5x5), b = all zeros:
  [[1, 1, 1, 1, 1],
   [1,-1, 1,-1, 2],
   [2, 0, 2, 0, 3],
   [1, 3, 1, 3, 0],
   [7,-1, 7,-1,11]]

VERIFIED (sympy): rank 2, free variables f3, f4, f5 (3 free), solution space is
3-dimensional. Particular = 0 (homogeneous). Direction vectors:
  f3 -> (-1, 0, 1, 0, 0)
  f4 -> (0, -1, 0, 1, 0)
  f5 -> (-3/2, 1/2, 0, 0, 1)
Sanity: set f3 = 2, f4 = f5 = 0 -> f1 = -2, rest 0 (change yogurt by 2, strawberries
by -2). Do not change these facts.

## Layout / interaction
- Reuse workbench(key, 5, ...) with key prefix t05b_smoothie_. Load the homogeneous
  system via the same _make_aug / _load_aug path the other screens use.
- Single preset (a one-item radio is fine): "Volume + sweetness locked".
- Ingredient legend rendered compactly above the workbench.
- BELOW the workbench, gated behind triangular form (same _is_upper_triangular gate as
  Example 3): call solve_parametric(M, 5, "f") and show:
    * "Read each ingredient change off the reduced rows:" then
      solution_equations_latex(res, "f") (one line per f_i).
    * "As a single vector equation:" then parametric_latex(res, "f")
      (X = f3*(...) + f4*(...) + f5*(...); particular is 0).
    * A caption: 3 free variables -> a 3-dimensional solution space -> three
      independent ways to tweak the recipe while keeping the constraints satisfied.
- No graph (5D can't be drawn); the math is the star.

## Screen text (verbatim)

Intro:
> **Smoothie.** You sell thousands of gallons of smoothies a month, and an ingredient
> shortage means you have to change a recipe -- but you must keep two things exactly
> the same: the total volume and the total sweetness. The question is how much to
> change each ingredient. Each change is an unknown: f1 = strawberries, f2 = bananas,
> f3 = yogurt, f4 = milk, f5 = honey. Your nutrition app turns "keep volume and
> sweetness fixed" into five equations -- but as you'll see, several of them say the
> same thing, so there isn't one right answer. There are infinitely many, and they
> form a whole space of choices.

Notice (st.info):
> Because a change can't add or remove total volume or sweetness, every equation is
> set to 0. Run the elimination: three of the five equations turn out to be repeats of
> the others, so they vanish to 0 = 0. That leaves only two real constraints on five
> unknowns -- so three of the ingredients are FREE. You can pick any change for those
> three, and the other two are then forced. Three free choices means the answers form
> a 3-dimensional space.

Closing (after the parametric solution):
> Each direction vector is one "adjustment pattern" -- a way to tweak the ingredients
> that keeps volume and sweetness fixed. For example, changing yogurt (f3) by +2 while
> leaving milk and honey alone forces strawberries (f1) by -2 and the rest at 0. Any
> mix of the three patterns is a valid new recipe. That's what a 3-dimensional solution
> space means: three independent dials you can turn, each keeping every constraint
> satisfied.

## Reuse / new
- REUSE: workbench(), _make_aug, _load_aug, _is_upper_triangular (workbench.py);
  solve_parametric, parametric_latex, solution_equations_latex (engine/parametric.py).
- NEW: topics/t05b_elimination/smoothie.py exposing render_smoothie().
- WIRING: selector position 7 in __init__.py (companion edit to topic5b_elimination.md).

## Acceptance
- [ ] New screen at selector position 7, "7 · Smoothie".
- [ ] Ingredient legend shown; homogeneous 5x5 loads into the workbench (keys prefixed
      t05b_smoothie_).
- [ ] After reaching triangular form, the parametric solution shows 3 free variables
      (f3, f4, f5), per-variable equations, and the stacked vector form with the three
      direction vectors; particular is 0.
- [ ] Intro / notice / closing render verbatim.
- [ ] Reuses workbench() and engine/parametric.py -- no edits to either.
