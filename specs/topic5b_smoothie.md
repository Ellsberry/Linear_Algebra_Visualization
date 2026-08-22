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

## Interactive "Try it yourself" block (bottom of screen, below the parametric solution)

An interactive compensation explorer: the student fixes THREE ingredient changes and
the app computes the other TWO so volume and sweetness stay locked at zero. Reuses no
engine code -- inline numpy/python. Placed at the very bottom of render_smoothie(),
after the closing text.

Heading: **Try it yourself: fix any three, the recipe fills in the rest.**
Intro (verbatim):
> The recipe has three free choices and two forced ones. Pick any THREE ingredients to
> set yourself (check their boxes and type a change: positive = add, negative =
> remove). The other two are then computed for you so that the total volume and total
> sweetness both stay at zero. For example, set strawberries to -10 (short by 10) and
> watch the recipe work out how to compensate.

UI (per ingredient, five rows or a compact grid):
  - a checkbox "set this one" (keys t05b_smoothie_fix_f1 .. _f5)
  - a text_input for the value (decimals; keys t05b_smoothie_val_f1 .. _f5), only
    used when that ingredient's box is checked. Default: check f1, f2, f3; values
    f1 = -10, f2 = 0, f3 = 0 (a strawberry-shortage starting example).
  Ingredient labels: f1 strawberries, f2 bananas, f3 yogurt, f4 milk, f5 honey.

Constraint rows (both must end at 0):
  volume    = f1 + f2 + f3 + f4 + f5
  sweetness = f1 - f2 + f3 - f4 + 2*f5
Matrix of the two constraints C = [[1,1,1,1,1],[1,-1,1,-1,2]].

Logic (inline):
  - Let `fixed` = the indices whose box is checked, with their typed values; `dep` =
    the other two indices (the ones to compute).
  - If exactly 3 are NOT checked as fixed (i.e. checked count != 3): st.warning(
    "Pick exactly 3 ingredients to set -- the other 2 are forced.") and stop.
  - Else build Cdep = C[:, dep] (2x2). If abs(det(Cdep)) < 1e-9: st.warning(
    "Those three don't pin down a unique fix -- try setting a different combination "
    "(for example, swap one for another ingredient).") and stop. (VERIFIED: only the
    trios {f1,f3,f5} and {f2,f4,f5} are singular; all other 8 trios solve.)
  - Else solve Cdep @ x_dep = -Cfix @ x_fix (numpy.linalg.solve) for the two computed
    values. Assemble the full 5-vector x.

Display:
  - Show the full resulting swap as a labeled list or one bmatrix: the 5 ingredient
    changes (fixed ones as typed, computed ones highlighted as "computed for you").
  - THEN show the parametric formula EVALUATED with the resulting free-variable values.
    After solving, every variable has a definite value, including the formula's three
    free vars f3, f4, f5. Substitute those into the parametric equation and show it
    filled in and evaluated (st.latex), e.g. with heading
    "**The parametric formula with your numbers:**":
      X = <f3val>\,[-1;0;1;0;0] + <f4val>\,[0;-1;0;1;0]
          + <f5val>\,[-\tfrac{3}{2};\tfrac{1}{2};0;0;1] = [f1;f2;f3;f4;f5]
    (bmatrix columns; the three scalars are the computed f3, f4, f5; the right-hand
    side is the full resulting swap vector). This ties the interactive back to the
    parametric solution shown above -- no matter which three ingredients the student
    fixed, the formula fed with the resulting f3, f4, f5 reproduces the same swap.
    (VERIFIED: fix f1=-10,f2=0,f3=0 -> f3=0,f4=10/3,f5=20/3 -> formula gives
    (-10,0,0,10/3,20/3), matching.)
  - Show Total volume and Total sweetness live (both snap to 0), labeled, NEXT TO the
    evaluated formula.
  - st.success("Valid swap -- the two free ingredients were adjusted to keep volume "
    "and sweetness locked.")

(VERIFIED: fixing f1=-10, f2=0, f3=0 -> computes f4=10/3, f5=20/3; volume 0,
sweetness 0. 8 of 10 trios solvable; {f1,f3,f5} and {f2,f4,f5} singular.)

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
