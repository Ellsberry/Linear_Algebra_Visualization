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
 "4 · Row space and the counting rule", "5 · Left null space",
 "6 · One matrix, all four spaces",
 "7 · Work it yourself: all four spaces of a big matrix"]

## OVERVIEW (pinned, verbatim)

> Every matrix hides four collections of vectors inside it — one that describes
> everywhere it can send you (the **column space**), one that describes everything
> it crushes to zero (the **null space**), one that captures its genuinely different
> rules (the **row space**), and one that reveals all the ways those rules can
> cancel out (the **left null space**). This topic names those four collections,
> shows that you have already met the first three, and ends with the counting rule
> and the fourth space that tie the whole picture together.
>
> **Orthogonal: the math word for perpendicular.** You already know
> **perpendicular** — two arrows meeting at a right angle. **Orthogonal** is just
> the mathematician's word for the same thing, and it means exactly perpendicular
> when you're talking about two arrows in 2D or 3D: they're orthogonal when they
> meet at 90 degrees, which is exactly when their dot product is zero.
>
> So why have a second word? Because "orthogonal" keeps working in places where
> "perpendicular" stops making sense. You can picture two arrows at a right angle,
> but what about two functions, like sin(x) and cos(x)? You can't draw them meeting
> at 90 degrees — yet there's a version of the dot product for functions, and by
> that measure sin(x) and cos(x) come out to zero, so we say they are
> **orthogonal**. Same idea — "their product cancels to zero" — stretched to things
> you can't draw as arrows.
>
> This matters here because the four collections inside a matrix come in
> **orthogonal pairs**: the row space is orthogonal to the null space, and the
> column space is orthogonal to the left null space. Orthogonality is the thread
> that ties the four spaces together.

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

### Block 0 — how to compute a column space, step by step (math, no graph)

A worked recipe at the TOP of the screen, before the intro. Uses the SAME made-up
4×4 matrix as the Screen 3 null-space recipe:
A = [[1,2,1,1],[1,3,2,4],[2,5,3,5],[0,1,1,3]] (VERIFIED: rank 2; RREF =
[[1,0,-1,-5],[0,1,1,3],[0,0,0,0],[0,0,0,0]]; pivots in columns 1,2; column space =
span of the ORIGINAL columns (1,1,2,0) and (2,3,5,1); dimension 2). NO graph (lives
in 4D). Every matrix a real bracketed LaTeX matrix — never comma text. This mirrors
the null-space recipe so the student sees ONE matrix yield BOTH spaces.

Heading (verbatim): **How to compute the column space of a matrix, step by step.**

**Step 1 — Write the matrix and look at its columns.** (verbatim) "The column space
is every output A can produce, which is every combination of its columns. So start
with the columns themselves." Then st.latex: A as a 4×4 bmatrix, and note its four
columns c1, c2, c3, c4.

**Step 2 — Row-reduce to find the pivot columns.** (verbatim) "Row-reduce to the
reduced form (Reduced Row Echelon Form) and see which columns get a pivot (a leading
1)." Then st.latex the reduced form as a 4×4 bmatrix (NOT augmented — no b column
here) with the two pivot leading-1s color-coded yellow (`\color{#ffd43b}{1}` at
(1,1) and (2,2)).

**Step 3 — The pivot columns of the ORIGINAL matrix are the answer.** (verbatim)
"Columns 1 and 2 hold the pivots, so they are the independent ones — columns 3 and 4
are just combinations of them and add nothing new. IMPORTANT: take these columns
from the ORIGINAL matrix A, not from the reduced form. The reduced form only tells
you WHICH columns to pick." Then st.latex the two original pivot columns side by
side as bmatrix columns: (1,1,2,0) and (2,3,5,1).

**Step 4 — Write the column space in parametric form.** (verbatim) "Every vector in
the column space is some amount of the first pivot column plus some amount of the
second. Call those amounts c1 and c2." Then st.latex the parametric form using
\underbrace + color, MIRRORING the null-space Step 5 style but GREEN for the column
space (`\color{#37b24d}`), with the \color OUTSIDE the whole group so the c1, c2
scalars are green too:
  \text{any output} = \underbrace{\color{#37b24d}{c_1\begin{bmatrix}1\\1\\2\\0\end{bmatrix}
  + c_2\begin{bmatrix}2\\3\\5\\1\end{bmatrix}}}_{\text{column space}}
Caption (verbatim): "Two pivot columns, so the column space is 2-dimensional — its
dimension is the rank, 2. Those two columns are a basis for it. (This is the SAME
matrix whose null space you compute on the next screen — one matrix, two spaces.)"

---

### Block 1 — the idea (text only, verbatim)

> The **column space** is all possible outputs of the matrix, and its **dimension**
> is the **rank** — which determines solvability, uniqueness of solutions, and how
> much information the matrix preserves. It determines whether a system A·x = b has
> a solution, because a vector b is solvable only if it lies in the column space of
> A. If b is in the column space of A then at least one solution exists; if b is not
> in the column space of A then no solution exists.
>
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

### Block 0 — how to compute a null space, step by step (math, no graph)

A worked recipe at the TOP of the screen, before the intro. Made-up 4×4 matrix
A = [[1,2,1,1],[1,3,2,4],[2,5,3,5],[0,1,1,3]] (VERIFIED: rows 3,4 are combinations
of rows 1,2; rank 2; RREF = [[1,0,-1,-5],[0,1,1,3],[0,0,0,0],[0,0,0,0]]; 2 free
variables x3,x4; null-space basis (1,-1,1,0) and (5,-3,0,1)). NO graph (4D can't be
drawn). Every matrix rendered as a real bracketed matrix (LaTeX bmatrix / array with
vertical rule for augmented) — never comma-delimited text.

Heading (verbatim): **How to compute the null space of a matrix, step by step.**

**Step 1 — Set up A·x = 0.** (verbatim) "The null space is every input x the matrix
sends to zero. So we solve A·x = 0." Then a SINGLE st.latex (do NOT show a standalone
copy of A first): the equation `A x =` with A the 4×4 bmatrix times the x column,
equal to a 4×1 zero column — i.e. A\,x = [A bmatrix][x1;x2;x3;x4] = [0;0;0;0].

**Step 2 — Form the augmented matrix [A | 0] and row-reduce.** (verbatim) "Attach a
column of zeros and row-reduce to the reduced form (Reduced Row Echelon Form)." Then
st.latex TWO augmented matrices (array with vertical rule `{cccc|c}`): first [A | 0],
then `\;\to\;` to the reduced form
  [[1,0,-1,-5|0],[0,1,1,3|0],[0,0,0,0|0],[0,0,0,0|0]].

**Step 3 — Identify pivot and free variables.** (verbatim) "The reduced form has
pivots (leading 1s) in columns 1 and 2, so x1 and x2 are the pivot variables.
Columns 3 and 4 have no pivot, so x3 and x4 are free — you may choose them to be
anything." Then RE-SHOW the reduced form (array {cccc|c}) with the two PIVOT entries
(the leading 1s at positions (1,1) and (2,2)) color-coded yellow via
`\color{#ffd43b}{1}` (same yellow as the workbench pivot highlight), so the pivots
are visually picked out.

**Step 4 — Solve the pivot variables in terms of the free variables.** (verbatim)
"First read each pivot row straight off the reduced form, then move the free
variables to the right side." Show BOTH forms as st.latex.
  BEFORE (raw pivot rows, as read from RREF), one aligned block:
    x_1 - x_3 - 5x_4 = 0
    x_2 + x_3 + 3x_4 = 0
  AFTER (free variables moved right), one aligned block:
    x_1 = x_3 + 5x_4
    x_2 = -x_3 - 3x_4
    x_3 = x_3\ (\text{free})
    x_4 = x_4\ (\text{free})

**Step 5 — Write the null space in parametric form.** (verbatim) "To turn those
equations into vectors, do what you learned earlier: set one free variable to 1 and
the rest to 0, and read off the column. Setting (x3, x4) = (1, 0) gives the first
direction; (0, 1) gives the second." Then st.latex the COMPLETE parametric equation
using \underbrace labels AND color: the all-zeros particular vector kept white/
default and underbraced "particular"; the ENTIRE null-space part — both the free-
variable scalars x3, x4 AND the two direction vectors — colored blue
(`\color{#4dabf7}`) and underbraced "null space". Put the \color OUTSIDE the whole
group so the x3, x4 coefficients are blue too (Claude Code's first attempt left the
scalars default-colored). Exact LaTeX shape:
  x = \underbrace{\begin{bmatrix}0\\0\\0\\0\end{bmatrix}}_{\text{particular}}
      + \underbrace{\color{#4dabf7}{x_3\begin{bmatrix}1\\-1\\1\\0\end{bmatrix}
      + x_4\begin{bmatrix}5\\-3\\0\\1\end{bmatrix}}}_{\text{null space}}
(the \color wraps the entire x3·d1 + x4·d2 expression, so scalars and vectors are all
blue; the + between the particular and null-space groups stays default). Caption
(verbatim): "Because the system equals zero, the particular part is zero — so the
ENTIRE answer is the null space (the blue part). Two free variables, so it is
2-dimensional; those two vectors are a basis for it."

---

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

### Block 0 — how to compute a row space, step by step (math, no graph)

A worked recipe at the TOP of the screen, before the intro. Uses the SAME made-up
4×4 matrix as the column-space (Screen 2) and null-space (Screen 3) recipes:
A = [[1,2,1,1],[1,3,2,4],[2,5,3,5],[0,1,1,3]] (VERIFIED: rank 2; RREF =
[[1,0,-1,-5],[0,1,1,3],[0,0,0,0],[0,0,0,0]]; row space = span of the two NONZERO
REDUCED rows (1,0,-1,-5) and (0,1,1,3); dimension 2). NO graph (lives in 4D). Every
matrix a real bracketed LaTeX matrix — never comma text. Third recipe on the same
matrix, so the student now sees ONE matrix yield ALL THREE spaces.

Heading (verbatim): **How to compute the row space of a matrix, step by step.**

**Step 1 — Write the matrix and look at its rows.** (verbatim) "The row space is
every rule you can build by mixing the rows. So start with the rows themselves."
Then st.latex: A as a 4×4 bmatrix, noting its four rows.

**Step 2 — Row-reduce to the reduced form.** (verbatim) "Row operations never change
the row space — mixing rows just rewrites the same rules — so row-reduce to the
reduced form (Reduced Row Echelon Form), which gives the cleanest version of those
rules." Then st.latex the reduced form as a 4×4 bmatrix, with the two NONZERO rows
color-coded purple (`\color{#9775fa}`) and the two zero rows in gray
(`\color{gray}`).

**Step 3 — The nonzero rows of the REDUCED form are the answer.** (verbatim)
"Keep the rows that are not all zeros — those are the genuinely different rules. The
two zero rows were redundant and drop out. IMPORTANT: unlike the column space (where
you took columns from the ORIGINAL matrix), for the row space you take the rows from
the REDUCED form — because row operations don't change the row space, the reduced
rows are the tidiest basis." Then st.latex the two nonzero reduced rows as row
vectors: (1, 0, -1, -5) and (0, 1, 1, 3).

**Step 4 — Write the row space in parametric form.** (verbatim) "Every vector in the
row space is some amount of the first reduced row plus some amount of the second.
Call those amounts r1 and r2." Then st.latex the parametric form using \underbrace +
color, MIRRORING the other two recipes but PURPLE for the row space
(`\color{#9775fa}`), \color OUTSIDE the whole group so the r1, r2 scalars are purple
too (write the basis as row vectors inside the combination):
  \text{any rule} = \underbrace{\color{#9775fa}{r_1\begin{bmatrix}1&0&-1&-5\end{bmatrix}
  + r_2\begin{bmatrix}0&1&1&3\end{bmatrix}}}_{\text{row space}}
Caption (verbatim): "Two nonzero rows, so the row space is 2-dimensional — its
dimension is the rank, 2, the SAME rank as the column space. Those two rows are a
basis for it. (Same matrix as the column-space and null-space recipes — one matrix,
all three spaces.)"

---

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

## Screen 5 — Left null space: the ways the rules cancel out

The fourth collection. Uses the SAME shared 4×4 matrix as the Screen 2/3/4 recipes:
A = [[1,2,1,1],[1,3,2,4],[2,5,3,5],[0,1,1,3]] (VERIFIED: rank 2; left null space =
null space of Aᵀ, basis (-1,-1,1,0) and (1,-1,0,1), dimension 2 = rows - rank =
4 - 2; each basis vector y satisfies yᵀA = 0). NO graph (lives in 4D). Fourth color
for this space: ORANGE (`\color{#f76707}`), distinct from green (column) / blue
(null) / purple (row). All matrices as real bracketed LaTeX.

### Block 1 — the idea (text only, verbatim)

> You have met three collections so far: the column space (what the matrix can
> reach), the null space (what it squashes to zero), and the row space (its
> genuinely different rules). There is a fourth. Remember how, during elimination,
> some rows collapsed to "0 = 0"? Those redundant rows didn't vanish by accident —
> they happened because certain combinations of the rows themselves add up to
> nothing. The collection of all those row-combinations that cancel to zero is the
> **left null space**. It measures the redundancy among the rows — exactly the
> "0 = 0" leftovers, now given a name.

### Block 2 — how to compute it (math, no graph)

Verbatim lead-in:
> To find it, flip the matrix on its side — swap its rows and columns to get
> **A-transpose** (written Aᵀ) — and then find the null space of Aᵀ using the same
> recipe from the null-space screen. The vectors you get are the row-combinations
> that cancel A to zero.

Then the worked steps as st.latex (all VERIFIED):
- Show A (4×4 bmatrix).
- Show Aᵀ = [[1,1,2,0],[2,3,5,1],[1,2,3,1],[1,4,5,3]] (4×4 bmatrix — A with rows and
  columns swapped).
- Show the RREF of Aᵀ: [[1,0,1,-1],[0,1,1,1],[0,0,0,0],[0,0,0,0]] (2 pivots, 2 free)
  as a bmatrix.
- Parametric left-null-space answer, ORANGE, \underbrace "left null space" (\color
  OUTSIDE the whole group so the y1,y2 scalars are orange too):
    y = \underbrace{\color{#f76707}{y_1\begin{bmatrix}-1\\-1\\1\\0\end{bmatrix}
        + y_2\begin{bmatrix}1\\-1\\0\\1\end{bmatrix}}}_{\text{left null space}}
- Verification line (verbatim caption + st.latex): "Check: each of these
  row-combinations really cancels A to zero." Show yᵀA = 0 for the first basis
  vector y=(-1,-1,1,0): (-1)·row1 + (-1)·row2 + 1·row3 + 0·row4 = (0,0,0,0).
  (VERIFIED: yᵀA = 0 for both basis vectors.)
Caption (verbatim): "Two free variables, so the left null space is 2-dimensional —
its dimension is rows minus rank, 4 - 2 = 2. Same matrix as the other three recipes
— now all four spaces come from one matrix."

### Block 3 — the four-subspaces picture (text only, verbatim)

> Now all four collections are named, and they pair up by orthogonality — the idea
> from the top of this topic. The **row space** and the **null space** are
> orthogonal: one holds the rules, the other holds what those rules leave free, and
> they meet at right angles. The **column space** and the **left null space** are
> orthogonal in the same way. Four spaces, two orthogonal pairs — the complete
> anatomy of a matrix.

### Block 4 — closing (verbatim)

> That completes the set. The next screen takes one matrix and lays all four of
> these spaces out together.

---

## Screen 6 — One matrix, all four spaces

One worked matrix taken all the way. Use A = [[1, 2], [2, 4]], b-free (the spaces
belong to A alone) — the same matrix from Screens 2 and 3, now unified. All FOUR
spaces are read off it (VERIFIED for this 2×2: column space = line along (1,2); null
space = line along (-2,1); row space = the rule x1 + 2 x2, i.e. direction (1,2);
left null space = line along (-2,1); rank 1). Note the orthogonal pairs are visible
here: row space (1,2) is perpendicular to null space (-2,1); column space (1,2) is
perpendicular to left null space (-2,1).

### Block 1 — eliminate once (math left, graph right)

LEFT: A, one elimination step shown (R2 → R2 − 2·R1), the reduced form
[[1, 2], [0, 0]], each line as one aligned block. Verbatim caption:
> One elimination and everything is visible: one pivot row (one real rule), one
> zero row (one redundant rule), one free variable.

RIGHT: `new_figure_2d` with BOTH lines on one graph: the column-space line along
(1,2) and the null-space line along (−2,1), labeled. Caption: "one matrix, two
different lines."

### Block 2 — read all FOUR spaces off the reduced form (single wide block)

Verbatim, one compact four-row layout (four narrow columns or one aligned list):
> **Column space** — what it can reach: the line along (1, 2). Targets on it are
> solvable; targets off it are not.
> **Null space** — what it squashes to zero: the line along (−2, 1). This is the
> freedom: add any multiple of (−2, 1) to a solution and it is still a solution.
> **Row space** — its genuinely different rules: one rule, x1 + 2·x2 (rank 1),
> which points along (1, 2).
> **Left null space** — the ways the rows cancel: the line along (−2, 1) (row 2
> minus 2·row 1 gives all zeros).
> Counting rule check: 1 real rule + 1 free variable = 2 unknowns. ✓
>
> Notice the **orthogonal pairs**: the row space (1, 2) is perpendicular to the null
> space (−2, 1) — their dot product 1·(−2) + 2·1 = 0. The column space (1, 2) is
> perpendicular to the left null space (−2, 1) the same way. Two perpendicular
> pairs, all on one little 2 by 2.

The RIGHT graph from Block 1 already shows the (1,2) line and the (−2,1) line — those
two lines ARE all four spaces (column space and row space share the (1,2) line here;
null space and left null space share the (−2,1) line), and they are perpendicular.
Add a caption to that effect if it fits.

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

Then FOUR short labeled lines (verbatim):
> **Column space** — a plane: everything the matrix can reach is the flat sheet
> spanned by the two surviving columns (2, 1, 3) and (1, 1, 2). Two independent
> directions, so a plane, not a line.
> **Null space** — a line: everything squashed to zero runs along (-1, -1, 1). One
> free variable, so a single line — and it points straight through the plane.
> **Row space** — a plane: the two surviving reduced rows, rank 2.
> **Left null space** — a line: the row-combination that cancels is along (-1, -1, 1)
> (row 3 minus row 1 minus row 2 gives all zeros). It is perpendicular to the
> column-space plane — it is exactly the line poking through it in the picture.
> **Counting rule check:** 2 real rules + 1 free variable = 3 unknowns. ✓ The line
> (1 dimension) and the plane (2 dimensions) add up to all of 3D space.

(VERIFIED for this 3×3: left null space = line along (-1,-1,1) = null space of Aᵀ =
the normal to the column-space plane. So the null-space line already drawn in the 3D
graph doubles as the left-null-space direction — same line, and it is the plane's
perpendicular.)

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

## Screen 7 — Work it yourself: all four spaces of a big matrix

The capstone: the student computes ALL FOUR spaces of a genuinely big, NON-symmetric
matrix, doing the row reduction themselves in the workbench. Uses the Logistics
many-plans flow matrix (7x7), the SAME network from Topic 5.5:
  A = [[-1,-1,0,0,0,0,0],
       [ 1, 0,-1,-1,0,0,0],
       [ 0, 1, 0, 0,-1,-1,-1],
       [ 0, 0, 1, 0, 0, 0, 0],
       [ 0, 0, 0, 1, 1, 0, 0],
       [ 0, 0, 0, 0, 0, 1, 0],
       [ 0, 0, 0, 0, 0, 0, 1]]
VERIFIED: rank 6; NOT symmetric (so the transpose genuinely matters, unlike Screen
6). RREF of A has pivots in columns 1-4,6,7 (column 5 free). null space = line along
(-1, 1, 0, -1, 1, 0, 0) (the free shipping-plan direction from Topic 5.5). RREF of
Aᵀ leaves row 7 free; left null space = line along (1, 1, 1, 1, 1, 1, 1). Dimensions:
column space 6, row space 6, null space 1, left null space 1; counting 6 + 1 = 7.

Uses the interactive space_workbench (topics/t06_spaces/space_workbench.py). TWO
workbenches: one on A, one on Aᵀ. Colors as elsewhere: column green (#37b24d), null
blue (#4dabf7), row purple (#9775fa), left null orange (#f76707).

### Block 1 — intro (text only, verbatim)

> This is the shipping network from Topic 5.5 — seven routes, seven balance rules —
> stripped down to its 7-by-7 matrix. This time YOU find all four of its spaces. It
> is bigger than anything you've reduced by hand, so here's the plan: do the first
> few row operations yourself to get the feel, then let **Do one step** finish the
> job (or jump straight to the answer with **Run to reduced form**). Watch the
> pivots appear, then read each space off the result.

### Block 2 — reduce A yourself (interactive)

Heading: **Step 1 — reduce A to find the column space, null space, and row space.**
Load A into space_workbench with key "t06_big_A", n=7, matrix_label="A". Suggest in a
caption: "Try a few manual row operations first, then use Do one step to finish."

After it, the read-off (verbatim), gated is not needed — show it below the workbench:
> **Column space** (green) — 6 pivots appear, in columns 1, 2, 3, 4, 6, and 7. So
> the column space is spanned by those 6 columns of the ORIGINAL A. It is
> 6-dimensional — too big to draw, but its dimension is the rank, 6.
> **Null space** (blue) — only column 5 has no pivot, so there is one free variable
> (route x5). Reading it off gives the single direction (-1, 1, 0, -1, 1, 0, 0) — the
> exact free shipping-plan direction from Topic 5.5. The null space is a line.
> **Row space** (purple) — the 6 nonzero reduced rows, a 6-dimensional space.

Show the null-space direction as one st.latex, blue:
  \text{null space} = \color{#4dabf7}{x_5\begin{bmatrix}-1\\1\\0\\-1\\1\\0\\0\end{bmatrix}}

### Block 3 — reduce Aᵀ yourself (interactive)

Heading: **Step 2 — reduce Aᵀ to find the left null space.**
Verbatim lead-in:
> The last space needs the transpose. Unlike the neat matrices on the last screen,
> this one is NOT symmetric — Aᵀ is genuinely different from A, so this step really
> does new work. Flip A to Aᵀ (swap rows and columns) and reduce it below.
Load Aᵀ into space_workbench with key "t06_big_AT", n=7, matrix_label="A^{T}".
(Aᵀ = [[-1,1,0,0,0,0,0],[-1,0,1,0,0,0,0],[0,-1,0,1,0,0,0],[0,-1,0,0,1,0,0],
[0,0,-1,0,1,0,0],[0,0,-1,0,0,1,0],[0,0,-1,0,0,0,1]] — A with rows and columns
swapped.)

After it, read-off (verbatim):
> **Left null space** (orange) — reducing Aᵀ leaves one free variable, giving the
> single direction (1, 1, 1, 1, 1, 1, 1). This one has a beautiful meaning: it says
> "add up all seven balance equations" — and they cancel to zero, because across the
> whole network total flow in equals total flow out. The left null space is the
> conservation law itself. It is a line.

Show it as one st.latex, orange:
  \text{left null space} = \color{#f76707}{y_1\begin{bmatrix}1\\1\\1\\1\\1\\1\\1\end{bmatrix}}

### Block 4 — the four-space summary + counting (text only, verbatim)

> **All four spaces of the 7-by-7:**
> - Column space: 6-dimensional (what the network can produce).
> - Row space: 6-dimensional (its genuinely different rules).
> - Null space: 1-dimensional, the line along (-1, 1, 0, -1, 1, 0, 0).
> - Left null space: 1-dimensional, the line along (1, 1, 1, 1, 1, 1, 1).
>
> Counting rule: 6 real rules + 1 free variable = 7 unknowns. ✓ And because this
> matrix is NOT symmetric, the null space and the left null space are genuinely
> different directions — not the same line, the way they were on the symmetric
> examples last screen. That is the normal situation; symmetry was the special case.

### Block 5 — closing (verbatim)

> You just found all four fundamental spaces of a real 7-by-7 system by hand. Every
> matrix, no matter how big, has exactly these four — two that live in the input
> space (row space and null space) and two in the output space (column space and
> left null space), each pair orthogonal. That is the complete anatomy of a matrix,
> and you can now dissect any one you meet.

---

## Screen 8 — The four spaces of a transformation

Bridges Topic 2 (transformations) to Topic 6: the four spaces reveal whether a
transformation LOSES information. Five 2×2 matrices from Topic 2. STATIC, with small
graphs (no workbench). VERIFIED spaces:
- Identity [[1,0],[0,1]], Rotation 90 [[0,-1],[1,0]], Shear [[1,1],[0,1]],
  Scale x2 [[2,0],[0,2]]: ALL rank 2 (invertible). Column space = all of 2D; null
  space = just the origin (only the zero vector); left null space = just the origin.
- Collapse (singular) [[1,2],[2,4]]: rank 1. Column space = line along (1,2); null
  space = line along (-2,1); left null space = line along (-2,1).

### Block 1 — the idea (text only, verbatim)

> Back in Topic 2 you watched matrices transform space — rotating, shearing,
> scaling, or flattening it. Now you can ask a sharp question about each one: does it
> LOSE any information? The four spaces answer it. If a transformation can be undone,
> nothing is lost: it reaches the whole plane (its column space is everything) and
> only the zero vector maps to zero (its null space is just the origin). If it
> flattens space, information is lost: a whole line of inputs gets crushed to zero.
> Here are five transformations from Topic 2, sorted by that question.

### Block 2 — the invertible four (grouped; small graphs)

Verbatim lead-in:
> **Four that lose nothing: identity, rotation, shear, and scale.** Each of these can
> be undone (each has an inverse), and all four tell the same four-space story:
> - **Column space = the whole plane.** Their two columns point in different
>   directions, so mixing them reaches every point in 2D. Every target is reachable.
> - **Null space = just the origin.** Nothing except the zero vector gets sent to
>   zero — no information is crushed.
> - **Row space = the whole plane** as well, and the **left null space = just the
>   origin**. Full rank (2), zero free variables: 2 + 0 = 2.

Show the four matrices compactly (a row of four small labeled matrices via st.latex
or st.columns(4)): Identity [[1,0],[0,1]], Rotation 90 [[0,-1],[1,0]], Shear
[[1,1],[0,1]], Scale x2 [[2,0],[0,2]]. For each (or as one representative graph), a
small new_figure_2d showing the two columns as arrows landing in different directions
with the whole plane lightly shaded (column space = everything) and the origin marked
"null space = just this point." Keep the graphs small; one graph per matrix in
st.columns(4), or a single representative graph with a caption that the other three
behave the same way (rank 2, fill the plane). Caption (verbatim): "All four fill the
plane and crush nothing — that is exactly what makes them invertible."

### Block 3 — the collapse (singular; full treatment, graph)

Verbatim:
> **One that loses information: the collapse.** The matrix [[1,2],[2,4]] has a second
> column that is just twice the first, so it flattens the whole plane onto a single
> line. Watch what happens to its four spaces:
> - **Column space = a line** (along (1, 2)). Everything the matrix produces lands on
>   this one line — most of the plane is now unreachable.
> - **Null space = a line** (along (-2, 1)). A WHOLE line of inputs gets crushed to
>   zero — that is the information being lost. (This is why a singular matrix has no
>   inverse: once a line is crushed to a point, you cannot undo it.)
> - Rank 1, one free variable: 1 + 1 = 2. The column space (1 dimension) plus the
>   null space (1 dimension) still account for all of 2D.

Graph: new_figure_2d showing the column-space line along (1,2) (labeled "column space
— everything lands here") and the null-space line along (-2,1) (labeled "null space —
crushed to zero"), the two lines through the origin. Optionally show a couple of
sample vectors collapsing onto the (1,2) line.

### Block 4 — the lesson (text only, verbatim)

> Here is the whole point, tying three topics together: a transformation is
> **invertible** exactly when it loses nothing — when its column space is the whole
> space and its null space is just the origin (Topic 4's "the determinant is not
> zero" is the same fact). The moment a transformation crushes even one line to zero,
> its null space grows, its column space shrinks, and it can no longer be undone. The
> four spaces are the complete report card on what a matrix does — and whether you
> can get back what you started with.

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
