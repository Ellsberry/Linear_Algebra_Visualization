# Build Spec — Topic 6: Vector Spaces (Null Space, Column Space, Row Space)

> **For the builder (Claude Code):** implement as a per-screen package
> `topics/t06_spaces/` registered in `app.py` after `t05b_elimination`. Follow
> `CLAUDE.md`. Reuse the engine (`engine/widgets.py`, `engine/plotting.py`,
> `engine/parametric.py`) and the Topic 5.5 patterns. The student-facing text below
> is final copy — implement it, don't reword. Straight ASCII quotes in code.

`TITLE = "6 · Vector Spaces"`, `SLUG = "spaces"`.

## Design rules for this topic (apply to every screen)

1. **Viewport blocks.** Each screen is a vertical stack of self-contained blocks.
   Each block fits ONE screen-height: the student scrolls BETWEEN blocks, never
   inside one. A block with math shows the math LEFT and its graph RIGHT
   (`st.columns([0.5, 0.5])`), everything for that example visible at once.
2. **Embedded recaps, no jumping.** Where a concept calls back to an earlier topic
   (Robotics, Smoothie, Logistics, Circuit), a COMPACT RECAP of that example is
   embedded on this screen — result-only, no controls, no re-derivation. The
   student never navigates away.
3. **One toggle max per recap.** A recap may have at most one radio/toggle, and only
   where it teaches (the Robotics good-pose/singular toggle). Otherwise static.
4. **Tight math.** Multi-line equation sets render as ONE combined aligned LaTeX
   block (the `solution_equations_block` treatment), never per-line st.latex calls.
5. **Graphs at the standard ~420 height**, engine dark palette, primitives
   (`new_figure_2d`, `add_vector_2d`, `add_point_2d`, `shade_polygon`, `add_line_2d`).
6. Plain words before symbols, every time. No unexplained notation anywhere.

## Selector

`st.radio` horizontal, key `t06_screen`:
["1 · What a vector space is", "2 · Column space", "3 · Null space",
 "4 · Row space and the counting rule", "5 · One matrix, all three spaces"]

## OVERVIEW (pinned, verbatim)

> Every matrix hides three collections of vectors inside it — one that describes
> everywhere it can send you, one that describes everything it squashes to zero,
> and one that describes its genuinely different rules. This topic names those
> three collections, shows that you have already met each of them, and ends with
> one simple counting rule that ties the whole course so far together.

---

## Screen 1 — What a vector space is (and what isn't one)

### Block 1 — the idea (text only)

**Intro (verbatim):**
> A **vector space** is a collection of vectors with a "no escape" rule: add any
> two vectors in the collection and the answer is still in the vector space;
> stretch or shrink any vector in it (multiply by any number) and the answer is
> still in it. You cannot get out by combining what is inside.
>
> Back in Topic 1, "span" meant everywhere you can reach by mixing vectors — using
> any amounts, including negative ones and zero. Every span passes the no-escape
> rule, so a span is always a vector space.

### Block 2a — the whole x-y plane (math left, graph right)

LEFT (verbatim):
> **The whole x-y plane is a vector space.** Every point on the screen counts. Pick
> any two arrows — say (3, 1) and (1, 2). Add them tip-to-tail and you get (4, 3).
> That result is still just a point on the x-y plane. Stretch any arrow longer or
> shorter and it's still on the plane. There is nowhere off the plane to land, so
> you can never escape.

LEFT also shows the addition as stacked-vector math (st.latex, bmatrix columns):
  [3;1] + [1;2] = [4;3]
(placed under the paragraph, before the graph column.)

RIGHT: `new_figure_2d` (rng~6); lightly shade the whole plane (shade_polygon of a
big square). Draw arrow (3,1) from the origin; draw arrow (1,2) tip-to-tail starting
at (3,1) so it ends at (4,3); draw the result arrow (0,0)->(4,3). Label the three:
"(3,1)", "(1,2)", "sum (4,3)". (VERIFIED: (3,1)+(1,2)=(4,3).)

### Block 2b — a straight line through the origin (math left, graph right)

LEFT (verbatim):
> **A straight line through the origin** — the graph shows the line that runs
> through (0,0) in the direction of the arrow (1, 2). Watch two things happen right
> on that line:
> - **Adding stays on the line.** The point (1, 2) and the point (2, 4) are both on
>   it. Add them: (1, 2) + (2, 4) = (3, 6) — and (3, 6) is also on the line (it's
>   just farther out). The dots on the graph are these three points; they all sit on
>   the same line.
> - **Stretching stays on the line.** Take (1, 2) and triple it: 3·(1, 2) = (3, 6) —
>   still on the line.
>
> No matter how you add or stretch points on this line, you land back on the line.
> It passes the no-escape rule, so a line through the origin is a vector space.

LEFT also shows the addition as stacked-vector math (st.latex, bmatrix columns):
  [1;2] + [2;4] = [3;6]   and   3·[1;2] = [3;6]
(placed under the paragraph, before the graph column.)

RIGHT: `new_figure_2d` (rng~8), the line through the origin along (1,2) drawn long
both ways, the origin marked, and the points (1,2), (2,4), (3,6) marked and labeled
with their coordinates.

### Block 3 — examples that FAIL, and exactly where (math left, graph right)

LEFT (verbatim):
> **A line that misses the origin fails.** Take the specific line through (0, 3)
> that runs flat (parallel to the x-axis). The point (2, 3) sits on it. A line that
> misses the origin is not a vector space, because it fails the no-escape rule
> (multiply a point on it by 0 and you land at the origin, which isn't on the
> line).
>
> **The top-right quarter of the plane fails.** Take just the first quadrant (both
> coordinates positive). The point (2, 1) is in it. Multiply by −1 and you get
> (−2, −1) — down in the bottom-left, outside the quarter. Escaped. Fails.
>
> **The smoothie mix from Topic 1 fails too.** Mixing ingredients only used
> positive amounts — you can't have negative banana — so it only ever filled that
> same first-quarter corner. Multiply a mix by −1 and you'd need negative smoothie,
> which escapes. That's exactly why smoothie-mixing was never a vector space, even
> though a true span (any amounts allowed) always is.
>
> **The rule underneath all three:** every vector space must contain the zero
> vector, because multiplying by zero is always allowed. Miss the origin, and you
> fail.

RIGHT: `new_figure_2d`, the off-origin flat line y=3 drawn, (2,3) marked on it,
(0,0) marked off it with label "escaped — off the line"; the first quadrant lightly
shaded (this same shaded quadrant also stands for the smoothie mix), (2,1) marked
inside, (−2,−1) marked outside with label "escaped".

### Block 4 — closing text (verbatim)

> Lines and planes through the origin, whole spaces, and every span you have ever
> drawn — those are vector spaces. The next three screens meet the three vector
> spaces that live inside every matrix.

---

## Screen 2 — Column space: every place the matrix can send you

### Block 1 — the idea (text only, verbatim)

> Take a matrix A. Feed it every possible input x and collect every output A·x.
> That collection of all possible outputs is called the **column space**. It gets
> that name because every output is a mix of A's columns — so the collection of
> outputs and the collection of column-mixes are the same thing.
>
> Here is the sentence that makes this whole topic matter: **the equation A·x = b
> has a solution exactly when the target b sits inside the column space** — when b
> is somewhere the matrix can actually reach. If b is outside, no input can get
> there: no solution.

### Block 2 — EMBEDDED RECAP: the robot arm (Topic 4), math left, graph right

The ONE allowed toggle: `st.radio(["Reachable pose", "Singular pose"],
horizontal=True, key="t06_cs_pose")`. Matrices exactly as Topic 4:
Reachable `[[1.5, 0.5], [0.0, 1.0]]`; Singular `[[1.0, 1.0], [1.0, 1.0]]`.

LEFT: A as read-only compact matrix; its two columns written out as the actuator
directions; then (verbatim, per pose):
- Reachable: "The two actuator columns point different ways. Mixing them reaches
  the entire plane — the column space is the whole plane, so EVERY target b is
  reachable."
- Singular: "Both actuator columns point the same way. Mixing them only slides
  along one line — the column space is just that line, so any target off the line
  is unreachable. You saw this in Topic 4; that line WAS a column space."

LEFT, REACHABLE POSE ONLY — also show two inputs fed through the FULL matrix as
A·x = b stacked-vector products (st.latex, w.bmatrix; write out the whole 2×2
matrix, not the letter A):
  [[1.5, 0.5],[0, 1]] · [3; -3] = [3; -3]
  [[1.5, 0.5],[0, 1]] · [-2; 3] = [-1.5; 3]
Then a caption: "Two different inputs, and their outputs land in different
quadrants — all over the plane. That is why this matrix's column space is the whole
plane: it can reach anywhere."
(VERIFIED: A·(3,-3)=(3,-3) in Q4, A·(-2,3)=(-1.5,3) in Q2.)

RIGHT: `new_figure_2d` — the two column arrows; Reachable: light full-plane shade
+ caption "column space = the whole plane"; ALSO mark the two outputs (3,-3) and
(-1.5,3) as points labeled "A·(3,-3)" and "A·(-2,3)" so the spread is visible.
Singular: the line along (1,1) drawn long both ways, labeled
"column space = this line", plus a sample point b = (4, 2) marked
"unreachable — outside the column space".

### Block 3 — NEW worked example (math left, graph right)

Matrix A = [[1, 2], [2, 4]] (VERIFIED: columns (1,2) and (2,4) are parallel; the
column space is the line along (1,2); rank 1).

LEFT: A read-only compact; both columns written out; (verbatim)
> Column 2 is exactly 2 × column 1 — they point the same way. Every mix of them
> lands on the line along (1, 2). That line is this matrix's column space. A
> target like b = (3, 6) is ON the line — reachable. A target like b = (3, 5) is
> OFF the line — no solution exists, no matter what x you try.

LEFT also shows two example inputs fed through A, as stacked-vector products
(st.latex, w.bmatrix), to make "any input lands on the same line" concrete:
  A·[3;-3] = [-3;-6]   and   A·[-2;3] = [4;8]
(VERIFIED: both outputs lie on the line along (1,2). Two very different inputs,
same line.)

RIGHT: `new_figure_2d` — the line along (1,2) long both ways; (3,6) marked
"reachable"; (3,5) marked "unreachable"; ALSO mark the two computed outputs
(-3,-6) and (4,8) on the line, labeled "A·(3,-3)" and "A·(-2,3)", showing both
inputs land on the column space.

### Block 4 — closing (verbatim)

> The column space answers "can we get there?" The next screen asks the opposite
> question: what does the matrix squash to nothing?

---

## Screen 3 — Null space: every input the matrix squashes to zero

### Block 1 — the idea (text only, verbatim)

> Some inputs x get sent by the matrix to the zero vector: A·x = (0, 0, ..., 0).
> Collect ALL the inputs that get squashed to zero. That collection is the **null
> space** ("null" means zero). The input x = 0 is always in it — the matrix always
> sends zero to zero. The interesting question is whether anything ELSE is in it.
>
> Why care? The null space is exactly the FREEDOM in your answers. If A·x = b has
> one solution, then adding anything from the null space to that solution gives
> another solution — because the null-space part contributes zero. One particular
> answer plus the null space = every answer.

### Block 2 — NEW worked example, drawable (math left, graph right)

Same matrix as Screen 2 Block 3: A = [[1, 2], [2, 4]]. (VERIFIED: null space is
the line along (−2, 1): A·(−2,1) = (0,0), A·(−4,2) = (0,0), A·(2,−1) = (0,0).)

LEFT: the system written out as one aligned block:
  1·x1 + 2·x2 = 0
  2·x1 + 4·x2 = 0
then (verbatim):
> The second rule is just twice the first — one real rule. It says x1 = −2·x2. So
> pick anything for x2 and the rule hands you x1. Every choice gives an input the
> matrix squashes to zero: (−2, 1), (−4, 2), (2, −1)... all of them on one line.
> That line — the line along (−2, 1) — is this matrix's null space.
Then the check, one aligned block: A·(−2,1) = (0,0) with the arithmetic shown.

RIGHT: `new_figure_2d` — the null-space line along (−2,1) long both ways, labeled
"null space — everything squashed to zero", with the three sample points marked.
ALSO draw (fainter) the column-space line along (1,2) from Screen 2, labeled
"column space (from the last screen)" — the SAME matrix, two DIFFERENT lines.

### Block 3 — EMBEDDED RECAP: the smoothie (Topic 5.5), math left, vectors right

No toggle (static). LEFT (verbatim):
> On the Smoothie screen every equation was "= 0": five rules, five unknowns, and
> the answer was a whole 3-dimensional space of recipe changes that all satisfied
> A·x = 0. That solution space WAS a null space — you have already computed one.
> Five unknowns live in 5-dimensional space, which nobody can draw — so for this
> one the picture is the three direction vectors themselves.

RIGHT: the three direction vectors as the visual — the stacked vector form he
knows: X = f3·(−1,0,1,0,0) + f4·(0,−1,0,1,0) + f5·(−3/2,1/2,0,0,1), rendered as
one LaTeX line with the ingredient legend (f1 = strawberries ... f5 = honey) in a
caption beneath. (This is the one example whose "graph" is its vectors — 5D can't
be plotted.)

### Block 4 — EMBEDDED RECAP: logistics many-plans (Topic 5.5), math left, graph-free

Static, compact — this block is text + one aligned equation set, no graph
(the network diagram would exceed the block; the point here is the formula shape).
LEFT+RIGHT single column (verbatim):
> On the Logistics screen the answer was one particular plan plus any multiple of
> a direction vector: x1 = 50 − x5, x2 = 50 + x5, x3 = 30, x4 = 20 − x5, x5 free,
> x6 = 25, x7 = 25. That direction vector — (−1, 1, 0, −1, 1, 0, 0) — lives in the
> null space. One particular answer plus the null space = every answer. That is
> the sentence from the top of this screen, working on a real problem.

### Block 5 — closing (verbatim)

> Column space: what the matrix can reach. Null space: what it squashes to zero.
> One more space to name, and then a counting rule connects all three.

---

## Screen 4 — Row space and the big counting rule

### Block 1 — the idea (text only, verbatim)

> Each row of a matrix is one equation — one rule the answer must obey. The **row
> space** is the collection of every rule you can build by mixing the rows. If one
> row is secretly a copy or a combination of the others, mixing it in adds nothing
> new — the row space does not get any bigger.
>
> The number of genuinely different rules — the rows that actually pin something
> down — is called the **rank**. You have already met it: it is the pivot count on
> the workbench banner ("Pivot count = number of genuinely independent equations").

### Block 2 — EMBEDDED LOGISTICS RECAP: two plans side by side (static, no graph)

Static (verbatim intro):
> On the two Logistics screens you built shipping plans where flow in = flow out at
> every node. One had a single answer; the other had a free choice. Put them side by
> side and the difference is a single zero row — the same seven-row count, but the
> many-plans version leaves one route free.

Then TWO cards side by side (`st.columns(2)`), each with its RULES on the left and
its REDUCED FORM matrix on the right (a small `st.columns([1,1])` split inside each
card). Route variables x1..x6 (one plan) / x1..x7 (many plans). Array + vertical
rule for matrices (never \big| in bmatrix). All VERIFIED — do not change numbers.

- **Logistics (one plan)** — 7 equations, 6 routes, UNIQUE answer. Bold header
  "One plan: 6 real rules + 0 free = 6 unknowns ✓".
  RULES (st.latex, aligned block — each route pinned, ONE PER LINE):
    x_1 = 50
    x_2 = 50
    x_3 = 30
    x_4 = 20
    x_5 = 25
    x_6 = 25
  (note: 1 more row collapsed to 0 = 0)
  MATRIX (6 pivot rows + 1 dimmed zero row):
    \left[\begin{array}{cccccc|c}
    1&0&0&0&0&0&50\\ 0&1&0&0&0&0&50\\ 0&0&1&0&0&0&30\\
    0&0&0&1&0&0&20\\ 0&0&0&0&1&0&25\\ 0&0&0&0&0&1&25\\
    \color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0
    \end{array}\right]
  Caption: "Six rules, six routes, no freedom — one definite plan."

- **Logistics (many plans)** — 7 equations, 7 routes, INFINITELY many. Bold header
  "Many plans: 6 real rules + 1 free = 7 unknowns ✓".
  RULES (st.latex, the 6 surviving rows as one aligned block):
    x_1 + x_5 = 50
    x_2 - x_5 = 50
    x_3 = 30
    x_4 + x_5 = 20
    x_6 = 25
    x_7 = 25
  (note: 1 more row collapsed to 0 = 0)
  MATRIX (6 pivot rows + 1 dimmed zero row):
    \left[\begin{array}{ccccccc|c}
    1&0&0&0&1&0&0&50\\ 0&1&0&0&-1&0&0&50\\ 0&0&1&0&0&0&0&30\\
    0&0&0&1&1&0&0&20\\ 0&0&0&0&0&1&0&25\\ 0&0&0&0&0&0&1&25\\
    \color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0
    \end{array}\right]
  PARAMETRIC SOLUTION shown BELOW the matrix (st.latex, stacked vectors):
    X = [50;50;30;20;0;25;25] + x_5\,[-1;1;0;-1;1;0;0]
  Caption: "Six rules, seven routes — route x5 is free, giving a whole family of plans."

(This two-card block replaces the single one-plan recap; the paragraph about "rank
6, not 7" is now shown by the dimmed zero row in BOTH cards.)

### Block 3 — THE COUNTING RULE (full-width, the screen's centerpiece)

Verbatim:
> **(number of genuinely different rules) + (number of free variables) = (number
> of unknowns).**
>
> Every unknown is either pinned down by a real rule or left free. No unknown is
> both; none is neither. That is the whole rule.

Then two count cards side by side (`st.columns(2)`), each showing the surviving
RULES on the LEFT and the problem's REDUCED FORM matrix on the RIGHT (use each
problem's OWN variable letter -- f for Smoothie, I for Circuit currents). Within
each card use a small 2-column split. Use array + vertical rule for matrices (never
\big| in bmatrix). All VERIFIED -- do not change numbers. (Logistics is already
covered by the two-card block above, so it is not repeated here.)

- **Smoothie** (5 ingredients, 5 equations = 0; variables f1..f5). Bold header
  "Smoothie: 2 real rules + 3 free = 5 unknowns ✓".
  RULES (st.latex, the 2 surviving rows as one aligned block):
    f_1 + f_3 + \tfrac{3}{2}f_5 = 0
    f_2 + f_4 - \tfrac{1}{2}f_5 = 0
  (note: 3 more rows collapsed to 0 = 0)
  MATRIX (reduced form, 2 pivot rows + 3 dimmed zero rows):
    \left[\begin{array}{ccccc|c}
    1&0&1&0&\tfrac{3}{2}&0\\ 0&1&0&1&-\tfrac{1}{2}&0\\
    \color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0\\
    \color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0\\
    \color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0&\color{gray}0
    \end{array}\right]
  Caption: "Two rules survive; three ingredients are free."
  PARAMETRIC SOLUTION shown BELOW the matrix (st.latex, stacked vectors; homogeneous
  so the particular part is the all-zeros vector — show it explicitly as the leading
  term, then the three free-variable directions):
    X = [0;0;0;0;0] + f_3\,[-1;0;1;0;0] + f_4\,[0;-1;0;1;0] + f_5\,[-\tfrac{3}{2};\tfrac{1}{2};0;0;1]

- **Circuit** (5 currents, 5 equations; variables I1..I5 = currents). Bold header
  "Circuit: 5 real rules + 0 free = 5 unknowns ✓".
  RULES (st.latex, the 5 rows as one aligned block -- each pins a current):
    I_1 = 6
    I_2 = 2
    I_3 = 3
    I_4 = 3
    I_5 = 1
  MATRIX (reduced form, 5 pivot rows, no zero row -- b column IS the answer):
    \left[\begin{array}{ccccc|c}
    1&0&0&0&0&6\\ 0&1&0&0&0&2\\ 0&0&1&0&0&3\\
    0&0&0&1&0&3\\ 0&0&0&0&1&1
    \end{array}\right]
  Caption: "Every current pinned down -- no free variables, one definite answer."

### Block 4 — closing (verbatim)

> Rank counts the real rules. Free variables count the freedom. Together they
> always account for every unknown. The last screen puts all three spaces on one
> matrix at once.

---

## Screen 5 — One matrix, all three spaces

One worked matrix taken all the way. Use A = [[1, 2], [2, 4]], b-free (the spaces
belong to A alone) — the same matrix from Screens 2 and 3, now unified.

### Block 1 — eliminate once (math left, graph right)

LEFT: A, one elimination step shown (R2 → R2 − 2·R1), the reduced form
[[1, 2], [0, 0]], each line as one aligned block. Verbatim caption:
> One elimination and everything is visible: one pivot row (one real rule), one
> zero row (one redundant rule), one free variable.

RIGHT: `new_figure_2d` with BOTH lines on one graph: the column-space line along
(1,2) and the null-space line along (−2,1), labeled. Caption: "one matrix, two
different lines."

### Block 2 — read all three spaces off the reduced form (single wide block)

Verbatim, one compact three-row layout (three narrow columns or one aligned list):
> **Column space** — what it can reach: the line along (1, 2). Targets on it are
> solvable; targets off it are not.
> **Null space** — what it squashes to zero: the line along (−2, 1). This is the
> freedom: add any multiple of (−2, 1) to a solution and it is still a solution.
> **Row space** — its genuinely different rules: one rule, x1 + 2·x2 (rank 1).
> Counting rule check: 1 real rule + 1 free variable = 2 unknowns. ✓

### Banner — between the 1D and 2D examples

Between the read-off block (all three spaces from the 2×2) and the new 3×3 example,
show a full-width banner (st.info or a styled markdown divider) with this verbatim
text:
> **Now let's go bigger.** The example above lived in 2D, so each space was a line.
> Next, a 3-by-3 matrix in 3D — the same three spaces, but now they're planes and
> lines. Watch the ideas scale up one dimension.

### Block 3 — a bigger matrix: spaces become PLANES (2-dimensional example)

Below the 1-dimensional example, add a second worked matrix where the spaces are
2-dimensional, drawn in 3D. Use A = [[2,1,3],[1,1,2],[3,2,5]] (VERIFIED: row 3 =
row 1 + row 2, so rank 2; RREF = [[1,0,1],[0,1,1],[0,0,0]]; column space = the plane
spanned by columns (2,1,3) and (1,1,2), whose equation is -x - y + z = 0; null space
= the line along (-1,-1,1); row space = a plane, rank 2; counting: rank 2 + 1 free
= 3 unknowns). Neat fact to mention: the null-space line points along (-1,-1,1),
which is exactly perpendicular to the column-space plane — the line pokes straight
through the plane.

LEFT (math): A as compact read-only; note row 3 = row 1 + row 2; show the reduced
form RREF = [[1,0,1],[0,1,1],[0,0,0]] (array + vertical rule, gray zero row).
Verbatim caption:
> This time the matrix is 3 by 3, and row 3 is just row 1 plus row 2 — a redundant
> rule that collapses to a zero row. Two real rules survive out of three, so the
> spaces are now two-dimensional: not lines, but whole PLANES.

Then three short labeled lines (verbatim):
> **Column space** — a plane: everything the matrix can reach is the flat sheet
> spanned by the two surviving columns (2, 1, 3) and (1, 1, 2). Two independent
> directions, so a plane, not a line.
> **Null space** — a line: everything squashed to zero runs along (-1, -1, 1). One
> free variable, so a single line — and it points straight through the plane.
> **Counting rule check:** 2 real rules + 1 free variable = 3 unknowns. ✓ The line
> (1 dimension) and the plane (2 dimensions) add up to all of 3D space.

RIGHT (graph): a 3D figure (`new_figure_3d(rng~6)`) showing:
- the column-space PLANE via `add_plane_3d(fig, -1, -1, 1, 0, color, "column space
  (a plane)")` (the plane -x - y + z = 0), translucent;
- the two spanning column arrows (2,1,3) and (1,1,2) lying in that plane, drawn with
  `_arrow3d` (or Scatter3d segments) so the student sees the plane is their span;
- the null-space LINE along (-1,-1,1) drawn long both ways as a Scatter3d segment
  from (2,2,-2) to (-2,-2,2), labeled "null space (a line)", clearly piercing the
  plane at the origin.
Caption: "One matrix, in 3D: the column space is a plane, the null space is a line
through it. Rotate to see the line pierce the plane."

### Block 4 — closing bridge (verbatim)

> Two more words make this vocabulary complete. The **dimension** of a space is
> how many independent directions it has — a line has dimension 1, a plane 2, the
> smoothie's null space 3. A **basis** is the smallest set of vectors that builds
> the whole space — the direction vectors you have been reading off the reduced
> form are exactly a basis for the null space. Topic 7 asks a new kind of
> question: when the target b is OUTSIDE the column space and there is no exact
> answer, what is the CLOSEST we can get? That single question is how line-of-best-
> fit, GPS, and camera apps all work.

---

## Reuse / new

- REUSE: `new_figure_2d`, `add_vector_2d`, `add_point_2d`, `add_line_2d`,
  `shade_polygon` (engine/plotting.py); `editable_matrix(..., compact=True,
  editable=False)` for read-only matrices; aligned-block LaTeX treatment.
- NEW: package `topics/t06_spaces/` — `__init__.py` (TITLE, SLUG, OVERVIEW,
  selector, dispatch) + `screen_what.py`, `screen_column.py`, `screen_null.py`,
  `screen_row.py`, `screen_together.py`.
- NO new engine code required. No workbench on this topic (recaps are result-only).

## Acceptance checklist

- [ ] Registered in app.py after Topic 5.5; selector shows 5 screens.
- [ ] Every screen is a stack of viewport blocks: each embedded example's math and
      graph are visible together without scrolling inside the block.
- [ ] All student-facing text renders verbatim from this spec; plain words precede
      every symbol; no C(A)/N(A) notation anywhere.
- [ ] Screen 2: Robotics recap has the ONE pose toggle; the [[1,2],[2,4]] example
      shows reachable (3,6) vs unreachable (3,5).
- [ ] Screen 3: the [[1,2],[2,4]] null-space line along (−2,1) is drawn WITH the
      column-space line along (1,2) fainter on the same graph; Smoothie recap shows
      the three direction vectors as the visual; Logistics recap ties the direction
      vector to the null space.
- [ ] Screen 4: counting rule centerpiece + three count cards (2+3=5, 6+1=7, 5+0=5).
- [ ] Screen 5: one elimination, both lines on one graph, all three spaces read off
      the reduced form, counting check 1+1=2.
- [ ] All matrices/numbers match the VERIFIED values in this spec exactly.
