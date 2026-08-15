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
> two vectors in the collection and the answer is still in the collection; stretch
> or shrink any vector in it (multiply by any number) and the answer is still in
> it. You cannot get out by combining what is inside.
>
> Back in Topic 1, "span" meant everywhere you can reach by mixing some
> ingredients. Every span automatically passes the no-escape rule — a span is
> always a vector space.

### Block 2 — examples that pass (math left, graph right)

LEFT (one aligned block + short captions):
- The whole 2D plane: add any two arrows, still in the plane; stretch any arrow,
  still in the plane. Passes.
- A straight line through the origin (use the line along (1, 2)): show
  (1,2) + (2,4) = (3,6) — still on the line; 3·(1,2) = (3,6) — still on the line.
  Passes.

RIGHT: `new_figure_2d`, the line through the origin along (1,2) drawn long both
ways, with the vectors (1,2), (2,4), (3,6) marked on it.

### Block 3 — examples that FAIL, and exactly where (math left, graph right)

LEFT (verbatim captions with the arithmetic):
> **A line that misses the origin** (the line through (0,3) parallel to (1,0)):
> multiply the vector (2,3) on it by 0 and you get (0,0) — which is OFF the line.
> Escaped. FAILS.
>
> **The top-right quarter of the plane only:** multiply (2,1) by −1 and you get
> (−2,−1) — bottom-left. Escaped. FAILS.
>
> Lesson: every vector space must contain the zero vector, because multiplying by
> zero is always allowed.

RIGHT: `new_figure_2d`, the off-origin line drawn, (2,3) marked on it, (0,0)
marked off it with label "escaped — off the line"; the first quadrant lightly
shaded, (2,1) marked inside, (−2,−1) marked outside with label "escaped".

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

RIGHT: `new_figure_2d` — the two column arrows; Reachable: light full-plane shade
+ caption "column space = the whole plane"; Singular: the line along (1,1) drawn
long both ways, labeled "column space = this line", plus a sample point b = (4, 2)
marked "unreachable — outside the column space".

### Block 3 — NEW worked example (math left, graph right)

Matrix A = [[1, 2], [2, 4]] (VERIFIED: columns (1,2) and (2,4) are parallel; the
column space is the line along (1,2); rank 1).

LEFT: A read-only compact; both columns written out; (verbatim)
> Column 2 is exactly 2 × column 1 — they point the same way. Every mix of them
> lands on the line along (1, 2). That line is this matrix's column space. A
> target like b = (3, 6) is ON the line — reachable. A target like b = (3, 5) is
> OFF the line — no solution exists, no matter what x you try.

RIGHT: `new_figure_2d` — the line along (1,2) long both ways; (3,6) marked
"reachable"; (3,5) marked "unreachable".

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

### Block 2 — EMBEDDED RECAP: the redundant row (Logistics one-plan), math left, graph-free

Static (verbatim):
> On the Logistics (one plan) screen you developed 7 equations for 6 unknowns, and
> one collapsed to the harmless row 0 = 0 — it was already implied by the others.
> Seven rows, but only six genuinely different rules: the rank is 6, not 7. The
> row space is built from six rules; the seventh added nothing.

Show the reduced matrix's shape compactly (6 pivot rows + the one zero row) as a
single small LaTeX array with the zero row dimmed/labeled "added nothing".

### Block 3 — THE COUNTING RULE (full-width, the screen's centerpiece)

Verbatim:
> **(number of genuinely different rules) + (number of free variables) = (number
> of unknowns).**
>
> Every unknown is either pinned down by a real rule or left free. No unknown is
> both; none is neither. That is the whole rule.

Then three "count cards" side by side (`st.columns(3)`), each one compact card:
- **Smoothie:** 2 real rules + 3 free = 5 unknowns ✓
- **Logistics (many plans):** 6 real rules + 1 free = 7 unknowns ✓
- **Circuit:** 5 real rules + 0 free = 5 unknowns ✓ (zero free variables is
  exactly why the circuit had one definite answer)

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

### Block 3 — closing bridge (verbatim)

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
