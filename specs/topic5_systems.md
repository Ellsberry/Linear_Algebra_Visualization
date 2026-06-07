# Build Spec — Topic 5: Linear Systems (Ax = b)

**For the builder (Claude Code):** Implement as `topics/t05_systems.py` and
register in `app.py`. Follow `CLAUDE.md`. Use the **multi-example selector**
pattern (template `topics/t01_vectors.py`). **Reuse the engine** and add the few
new shared plotting helpers noted below to `engine/plotting.py` (they are reusable
— Topic 7 will use the line helper too). Text below is final copy; implement it,
don't reword or invent examples.

`TITLE = "5 · Linear Systems (Ax = b)"`, `SLUG = "systems"`.

## Core idea (the spine)

A linear system is a set of equations bundled as **Ax = b**: "what input x
produces the output b?" Every system has exactly **one solution, none, or
infinitely many**, and you can see why two ways:
- **Row picture:** each equation is a line (2D) or plane (3D); solutions are where
  they all meet.
- **Column picture:** which combination of A's *columns* builds b? (This is the
  Topic 1 / Topic 4 view.)

The big payoff of the core screen is showing **both pictures of the same system at
once** so he sees they're the same problem. Tie the three outcomes back to the
determinant (Topic 3): det ≠ 0 ⇒ unique; det = 0 ⇒ none or infinitely many.

## New shared plotting helpers to add to `engine/plotting.py`

- `add_line_2d(fig, a, b, c, color, name, rng=VIEW)` — draw the line `a*x + b*y = c`
  across the view (compute two endpoints within ±rng; handle the vertical case
  b≈0 by drawing x = c/a).
- `new_figure_3d(rng=6, titles=("x","y","z"), height=560)` — a blank 3D scene with
  cube aspect and fixed ranges (mirror the layout in `figure_3d`).
- `add_plane_3d(fig, a, b, c, d, color, name, rng=6)` — draw `a*x + b*y + c*z = d`
  as a translucent `Surface`: if c≉0 solve `z = (d - a*x - b*y)/c` over an x,y
  grid; otherwise solve for whichever coefficient is nonzero.

## Shared outcome meter `_outcome(A, b)`

Define once, call on every screen. Classify with NumPy:
- square A and `abs(det(A)) > 1e-9` → **unique**, `x = np.linalg.solve(A, b)`.
- else compare `np.linalg.matrix_rank(A)` to `matrix_rank([A|b])`:
  - rank(A) < rank([A|b]) → **no solution** (inconsistent).
  - equal → **infinitely many** (a free variable).
Render a colored state line: unique (blue, show x), none (warning), infinite
(info). Always mention the link: det = 0 is exactly when "unique" breaks.

## Selector and always-on text

Selector (st.radio, horizontal, key `t05_example`), in THIS order:
`["1 · The three outcomes", "2 · Business", "3 · Engineering", "4 · Chemistry",
"5 · 3D: three planes"]`.

`OVERVIEW`:
> In Topic 4's business screen you solved Ax = r for x. That's a **linear
> system**: a set of equations bundled into Ax = b, asking "what input x produces
> the output b?" A system can have exactly one solution, none, or infinitely many
> — and you can see why two ways: the **row picture** (each equation is a line or
> plane; solutions are where they meet) and the **column picture** (which
> combination of A's columns builds b?). We'll see both, then meet linear systems
> in business, engineering, chemistry, and nutrition.
>
> *(We can picture systems with up to 3 unknowns. For bigger ones — six, or six
> thousand — there's a systematic method that doesn't rely on a drawing. That's
> the next topic.)*

`HOWTO`:
> The left panel sets the equations; the right panel shows the picture. The
> **outcome meter** tells you whether there's one solution, none, or infinitely
> many — and why. On the core screen you'll see the row picture and the column
> picture of the *same* system side by side.

---

## Example 1 — The three outcomes (math first; BOTH pictures side by side)

**Inputs:**
- `widgets.matrix_editor("t05e1_A", 2, label="Coefficients A")`.
- `widgets.vector_editor("t05e1_b", 2, (3.0, 1.0), label="Right side b")`.
- Preset selectbox `t05e1_preset` (apply via `set_matrix_state` / `set_vector_state`
  on change, track `t05e1_last`):
  - **"One solution"** → A `[[1, 1], [1, -1]]`, b `(3, 1)` (solution x = (2, 1);
    det = −2).
  - **"No solution"** → A `[[1, 1], [1, 1]]`, b `(2, 5)` (parallel distinct lines;
    det = 0).
  - **"Infinitely many"** → A `[[1, 1], [2, 2]]`, b `(2, 4)` (same line twice;
    det = 0).

**Right panel — two figures side by side (`st.columns`):**
- **Row picture** (`new_figure_2d`): draw each equation as a line via
  `add_line_2d` (row i: `A[i,0]*x + A[i,1]*y = b[i]`). If unique, mark the
  intersection point with `add_point_2d`.
- **Column picture** (`new_figure_2d`): draw columns `c1 = A[:,0]`, `c2 = A[:,1]`
  as arrows from origin (`add_vector_2d`), the target b as a point, and — if
  unique — the solution path `x1*c1` then `+ x2*c2` reaching b (tip-to-tail, like
  Topic 1).

**Outcome meter** below the figures.

**Notice (always shown):**
> Same system, two views. The row picture asks "where do the lines cross?"; the
> column picture asks "what mix of these two arrows reaches the target?" They
> always agree — one crossing point matches one mix; parallel lines match a target
> you can't reach; one repeated line matches a target with many mixes.

**Show the math (expander):** A, b, det, and the solution or the reason there
isn't one.

---

## Example 2 — Business: break-even (row picture)

**Concept:** revenue and cost are two lines; they cross at the break-even
quantity.

**Inputs (sliders):**
- `scalar_slider("t05e2_price", "Selling price per unit ($)", 0.0, 20.0, 8.0, 0.5)`
- `scalar_slider("t05e2_fixed", "Fixed cost ($)", 0.0, 100.0, 40.0, 1.0)`
- `scalar_slider("t05e2_var", "Variable cost per unit ($)", 0.0, 20.0, 4.0, 0.5)`

**Logic:** revenue line `y = price*q`; cost line `y = fixed + var*q`. Break-even
where equal: `q* = fixed / (price - var)` if `price > var`, else they never cross
in the positive region (no break-even).

**Right panel:** `new_figure_2d(rng=..., x_title="quantity sold",
y_title="dollars")` (use a range suited to the numbers, e.g. 0..20 on x). Draw
both lines with `add_line_2d`; mark the crossing if it exists.

**Outcome meter / readout:** if `price > var`, show "break-even at q* = … units";
else "no break-even — each unit loses money (price ≤ variable cost): the lines are
parallel-ish and never cross."

**Notice (always shown):**
> Every break-even calculation, and every "supply meets demand" price, is the
> solution of a linear system — the point where two lines cross. If price never
> beats the per-unit cost, the lines never meet: no solution.

**Show the math (expander):** the two line equations and `q* = fixed/(price−var)`.

---

## Example 3 — Engineering: mixing to a target (column picture)

**Concept (state this plainly to the student):** You have two metal alloys. Each
alloy, per unit you add, contributes a known amount of **copper** and **zinc** —
that pair of numbers is the alloy's "makeup vector." You want to combine some
amount **x₁** of alloy 1 and **x₂** of alloy 2 to hit an exact target: so many
units of copper and so many of zinc. "How much of each alloy?" is the system
`x₁·c₁ + x₂·c₂ = b`, where c₁, c₂ are the alloys' makeup vectors (the columns of
A) and b is the target. **He is solving for x₁ and x₂ — how many units of each
alloy to add.** This is the *column picture*: build the target out of the column
vectors. (Direct callback to Topic 1's smoothies — same idea, now solved exactly.)

**Inputs (label them clearly):**
- `matrix_editor("t05e3_A", 2, label="Alloy makeup — column 1 = alloy 1 (copper, zinc), column 2 = alloy 2 (copper, zinc)")`.
- `vector_editor("t05e3_b", 2, (8.0, 9.0), label="Target (copper, zinc)")`.
- Preset selectbox `t05e3_preset`:
  - **"Reachable target"** → A `[[2, 1], [1, 3]]`, b `(8, 9)`. Alloy 1 = (2 copper,
    1 zinc), alloy 2 = (1 copper, 3 zinc). Unique blend **x = (3, 2)**: 3 units of
    alloy 1 + 2 units of alloy 2.
  - **"Unreachable target"** → A `[[2, 4], [1, 2]]`, b `(8, 9)`. The two alloys are
    proportional (alloy 2 is just 2× alloy 1), so every blend lands on one line and
    the target is off it → **no solution** (you can't make this target from these
    two alloys).
  - **"Redundant alloys"** → A `[[2, 4], [1, 2]]`, b `(8, 4)`. Proportional alloys
    again, but now the target lies on their shared line → **infinitely many** blends
    work.

**Right panel (column picture) — make the construction explicit:** draw alloy
vectors `c1 = A[:,0]` and `c2 = A[:,1]` as arrows from the origin, and the target b
as a point. If there's a unique blend, draw the solution as a **tip-to-tail path**:
the arrow `x1·c1` from the origin, then `x2·c2` from its tip, landing exactly on b
— so he sees the blend literally building the target. Label the arrows "x₁ × alloy
1" and "x₂ × alloy 2".

**Outcome meter / readout:** state the answer in words — "Blend: 3 units of alloy 1
+ 2 units of alloy 2", or "No blend of these two alloys reaches the target", or
"Many blends work (the alloys are redundant)".

**Notice (always shown):**
> Metallurgists, chemists, and chefs solve linear systems to hit a target blend
> from the ingredients on hand. You're solving for *how much of each alloy* to add.
> If the two alloys aren't truly different — one is just a scaled copy of the other
> — then every blend lands on a single line, and any target off that line is
> impossible to make: no solution.

**Show the math (expander):** write `x₁·c₁ + x₂·c₂ = b` with the live numbers, then
the solution (or the reason there's none).

---

## Example 4 — Chemistry: balance a reaction (the "infinitely many → pick simplest" case)

**Concept:** balancing `a H₂ + b O₂ → c H₂O` is solving a linear system that
conserves each atom. It has a free variable (a *ratio*), so you pick the smallest
whole numbers — a concrete face of "infinitely many solutions."

**Inputs (integer sliders 0–8):**
- `scalar_slider("t05e4_a", "a  (H₂ molecules)", 0, 8, 0, 1)`
- `scalar_slider("t05e4_b", "b  (O₂ molecules)", 0, 8, 0, 1)`
- `scalar_slider("t05e4_c", "c  (H₂O molecules)", 0, 8, 0, 1)`

**Logic:** Hydrogen atoms: left `2a`, right `2c`. Oxygen atoms: left `2b`, right
`c`. Balanced when `2a == 2c` and `2b == c` (and not all zero).

**Right panel — atom-balance display** (simple, not geometric): for H and for O,
show left-count vs right-count (a small `plotly` bar pair, or `st.metric` pairs),
turning green/showing a ✓ when the two match. Show a ✓ "Balanced!" banner when
both atoms balance.

**Notice (always shown):**
> Balancing any chemical reaction is solving a linear system — the coefficients
> that conserve every atom. Notice the answer is a *ratio*: 2 : 1 : 2 works, and
> so does 4 : 2 : 4. The system has infinitely many solutions, so chemists pick
> the smallest whole numbers. So 2 H₂ + O₂ → 2 H₂O.

**Show the math (expander):** the two conservation equations and the ratio
a : b : c = 2 : 1 : 2.

---

## Example 5 — 3D: three planes / a three-nutrient plan (medical/nutrition). ENDS THE TOPIC.

**Concept (state this plainly):** A dietician has **three foods** and must hit
exact targets for **three nutrients** (say protein, carbs, vitamin C). If `x₁, x₂,
x₃` are the amounts of each food, then *each nutrient* gives one equation:
"(amount of that nutrient per unit of food 1)·x₁ + … = target for that nutrient."
Three nutrients → three equations in three unknowns. **He is solving for x₁, x₂, x₃
— how much of each food.** Each equation is a flat **plane** in the space of food
amounts; the solution is the point where all three planes meet.

**How to read the matrix:** in A, **column j is food j** and **row i is nutrient
i** (entry A[i,j] = how much of nutrient i is in one unit of food j). Row i is the
plane `A[i,0]·x₁ + A[i,1]·x₂ + A[i,2]·x₃ = b[i]`.

**Inputs (label clearly):**
- `matrix_editor("t05e5_A", 3, label="Nutrient content — row i = nutrient i, column j = food j")`.
- `vector_editor("t05e5_b", 3, (5.0, 8.0, 7.0), label="Nutrient targets (one per row)")`.
- Preset selectbox `t05e5_preset`:
  - **"Unique plan"** → A `[[2, 1, 1], [1, 3, 1], [1, 1, 4]]`, b `(5, 8, 7)`
    (the three planes meet at one point; solution **x = (1, 2, 1)** — 1 unit of food
    1, 2 of food 2, 1 of food 3).
  - **"Redundant foods (infinite)"** → A `[[1, 1, 1], [1, 2, 3], [2, 3, 4]]`,
    b `(6, 14, 20)` (row 3 = row 1 + row 2, b consistent → the planes meet in a
    *line*: many plans work).
  - **"Impossible targets (none)"** → A `[[1, 1, 1], [1, 2, 3], [2, 3, 4]]`,
    b `(6, 14, 21)` (same A, b inconsistent → the three planes share no common
    point: impossible).

**Right panel:** `new_figure_3d(titles=("food 1","food 2","food 3"))`; draw the
three planes with `add_plane_3d` (row i: `A[i,0]x + A[i,1]y + A[i,2]z = b[i]`),
translucent and in three distinct colors. If unique, mark the meeting point with a
clear marker. Caption: "drag to rotate · scroll to zoom — the solution is where all
three planes cross." (Tell him to rotate: head-on, a single intersection point can
hide behind a plane.)

**Outcome meter / readout:** "Plan: 1 unit food 1, 2 food 2, 1 food 3", or "Many
plans work (a redundant food)", or "No plan hits all three targets".

**Notice (always shown):**
> A dietician hitting exact nutrient targets from three foods is solving three
> equations in three unknowns — three planes in space. They meet at one point (one
> plan), along a line (many plans), or nowhere (impossible). You're solving for how
> much of each food to use.

**Looking ahead (st.info, shown on this screen):**
> This is the biggest system we can still *picture* — three unknowns, three planes.
> Real problems have six, or six thousand, unknowns, and there's no drawing for
> that. The next topic introduces the systematic method — elimination to
> **triangular form** — that solves a system of any size, the same algorithm every
> engineering simulation runs internally.

**Show the math (expander):** A, b, det, and the solution or classification.

---

## Registration

In `app.py`: add `t05_systems` to the `from topics import ...` line and insert
`(t05_systems.TITLE, t05_systems),` in `TOPICS` immediately after the
`t04_inverse` entry.

## Acceptance checklist (verify before committing)

- [ ] Sidebar shows "5 · Linear Systems (Ax = b)" after Topic 4.
- [ ] **Three outcomes:** row and column pictures show side by side and agree;
      the three presets give one / none / infinitely many, each labeled with the
      det link.
- [ ] **Business:** moving the sliders slides the break-even crossing; setting
      price ≤ variable cost reports "no break-even."
- [ ] **Engineering:** "Reachable" shows the unique blend as a tip-to-tail column
      path; "Unreachable" reports no solution; "Redundant" reports infinitely many.
- [ ] **Chemistry:** setting a=2, b=1, c=2 turns both atom checks green and shows
      "Balanced!"; the notice's ratio point is made.
- [ ] **3D:** three translucent planes render and rotate; "Unique plan" marks the
      point (1,2,1); "Redundant" = infinite; "Impossible" = none; the looking-ahead
      note appears.
- [ ] New helpers `add_line_2d`, `new_figure_3d`, `add_plane_3d` live in
      `engine/plotting.py`; app runs with `streamlit run app.py`, no import errors.
