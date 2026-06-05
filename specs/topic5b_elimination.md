# Build Spec — Topic 5.5: Elimination & Triangular Form

**For the builder (Claude Code):** Implement as `topics/t05b_elimination.py` and
register in `app.py`. Follow `CLAUDE.md`. Use the **multi-example selector**
pattern (template `topics/t01_vectors.py`). Text below is final copy.

**Build note — read first.** This is the most state-heavy screen in the course.
The centerpiece is a reusable **elimination workbench** that all three screens
share. **Build and fully test the workbench on Screen 1 (the warmup) before
wiring the two diagram screens.** Keep all working state in `st.session_state`
under per-screen keys (no browser storage). Use `on_click` callbacks for every
button that mutates state, so edits land before the rerun redraws.

`TITLE = "5.5 · Elimination & Triangular Form"`, `SLUG = "elimination"`.

## Core idea (the spine)

Topic 5 could only picture systems up to 3 unknowns. This topic is the
**systematic method that solves a system of any size** by simplifying the
augmented matrix `[A | b]` with three legal moves until it is **upper
triangular** (a staircase of zeros below the diagonal), then **back-substituting**
from the bottom row up. The three moves never change the solution set — that's
why elimination is allowed.

The three row operations (the whole interaction vocabulary):
1. **Swap** two rows (Rᵢ ↔ Rⱼ).
2. **Scale** a row (Rᵢ → k·Rᵢ).
3. **Add a multiple** of one row to another (Rᵢ → Rᵢ + k·Rⱼ) — the move that
   makes zeros below a pivot.

## The shared elimination workbench (build this first)

A function `workbench(key, n_unknowns)` that operates on an augmented matrix
stored at `st.session_state[f"{key}_M"]` (a list of `n` rows, each `n_unknowns+1`
floats — last entry is the b-value). It assumes the matrix is already populated
(Screen 1 sets it from a preset; Screens 2–3 set it from the diagram step).

**State keys (per `key`):**
- `{key}_M` — current augmented matrix (working state).
- `{key}_orig` — original matrix (for Reset).
- `{key}_log` — list of operation strings (e.g. `"R2 → R2 − 2·R1"`).
- `{key}_history` — list of prior `_M` snapshots (for Undo).

**Display:** render the current augmented matrix with `st.latex` using an
augmented array, e.g.
`\left[\begin{array}{ccc|c} … \end{array}\right]` (the vertical bar separates A
from b; column count = `n_unknowns` then 1). Add a helper
`widgets.aug_array_latex(M, n_unknowns)` to format it. Below it, show the last
operation and the running **operation log** (an expander or a small list).

**Manual controls (always available):**
- An operation-type selectbox: `["Add multiple of a row", "Swap two rows",
  "Scale a row"]`.
- Depending on type, show 1-indexed row selectboxes and a number input for the
  factor k:
  - Add multiple: "Add ( k ) × Row ( j ) to Row ( i )".
  - Swap: "Swap Row ( i ) and Row ( j )".
  - Scale: "Multiply Row ( i ) by ( k )".
- An **Apply** button (on_click): push current `_M` to `_history`, perform the op,
  append a description to `_log`.

**Guided controls:**
- **"Do one step"** (on_click): compute and apply the single next standard
  forward-elimination operation, defined as — scan diagonal positions p = 0,1,…:
  if `M[p][p] ≈ 0`, find the first row r > p with `M[r][p] ≠ 0` and **swap** (p, r);
  otherwise find the first row i > p with `M[i][p] ≠ 0` and apply
  `Ri → Ri − (M[i][p]/M[p][p])·Rp`. If no below-diagonal nonzero entries remain,
  do nothing (already triangular). Apply exactly one op per press so he can watch
  the staircase build.
- **"Run to triangular form"** (on_click): loop "Do one step" until upper
  triangular (all entries strictly below the diagonal ≈ 0), capped at a safe
  iteration limit.
- **"Back-substitute & solve"** (enabled once upper triangular and every diagonal
  pivot ≠ 0): compute the solution from the bottom row up and show each step in an
  expander ("Row 3 ⇒ x₃ = …; substitute into Row 2 ⇒ x₂ = …; …"), then the
  solution.

**Undo** (pop `_history` into `_M`) and **Reset** (restore `_orig`, clear log).

**Live scenario detection** (run after every op; show a colored banner):
- A row of the form `[0 0 … 0 | c]` with c ≠ 0 → **No solution** (warning):
  "Row {i} says 0 = {c} — impossible. This system has no solution."
- A fully zero row `[0 … 0 | 0]` → **Infinitely many** (info): "Row {i} became all
  zeros — that equation was redundant, so there's a free variable: infinitely
  many solutions."
- Otherwise, when upper triangular with all nonzero pivots → **Ready to
  back-substitute** (blue), and report the **pivot count** with a light note that
  it equals the number of genuinely independent equations (quiet Topic 6 seed).

**Reusability:** keep `workbench` and `aug_array_latex` general (any size). The
three screens differ only in how `{key}_M` gets populated and how the final
answer is labeled.

## Selector and always-on text

Selector (st.radio, horizontal, key `t05b_example`):
`["1 · The workbench", "2 · Logistics", "3 · Circuit"]`.

`OVERVIEW`:
> Topic 5 ended at the edge of what we can draw — three unknowns, three planes.
> This topic is the method that goes further. We simplify the system's augmented
> matrix `[A | b]` with three reversible moves — swap rows, scale a row, add a
> multiple of one row to another — until it's **upper triangular** (zeros below
> the diagonal). Then we read the answer off from the bottom row up
> (**back-substitution**). The moves never change the answer, so it's always safe
> to experiment. First on a 3×3 you can still relate to planes, then on a
> six-variable shipping network and a circuit you *can't* picture — where the
> procedure is the only way through.

`HOWTO`:
> Use **Do one step** / **Run to triangular form** to watch the standard method,
> or compose your own row operations in **manual** mode. The banner tells you when
> you've hit a special case (no solution, or infinitely many). Once the matrix is
> triangular, **back-substitute** to solve. **Undo** and **Reset** make
> experimenting safe.

---

## Example 1 — The workbench (math first; learn the moves and the scenarios)

A 3×3 system he reduces by hand or with guidance. Presets produce each scenario.

**Inputs:**
- Preset selectbox `t05b_e1_preset` (on change, set `t05b_e1_M` and `_orig` from
  the augmented matrix below, clear `_log`/`_history`, track `t05b_e1_last`):
  - **"One solution"** → A `[[2,1,-1],[-3,-1,2],[-2,1,2]]`, b `(8,-11,-3)`
    (solution x = (2, 3, −1)).
  - **"Needs a row swap"** → A `[[0,2,1],[1,1,1],[2,1,3]]`, b `(5,6,11)` (top-left
    pivot is 0, so a swap is required first; solution (3, 2, 1)).
  - **"Redundant equation (infinite)"** → A `[[1,1,1],[1,2,3],[2,3,4]]`,
    b `(6,14,20)` (row 3 = row 1 + row 2 → a zero row appears → infinitely many).
  - **"Contradiction (no solution)"** → A `[[1,1,1],[1,2,3],[2,3,4]]`,
    b `(6,14,21)` (a `0 = nonzero` row appears → no solution).
- Then render `workbench("t05b_e1", 3)`.

**Notice (always shown):**
> Try the standard method with **Do one step**, then experiment in manual mode —
> you can't break it, because every move keeps the same solution. The four
> examples show the four things that can happen: a clean triangle (one solution),
> a forced swap when a pivot is zero, a row that vanishes (infinitely many), and a
> row that becomes "0 = something" (no solution).

**Show the math (expander):** restate the three row operations and note that the
determinant of a triangular matrix is the product of its diagonal — so a zero on
the diagonal is exactly the det = 0 / "no unique solution" case from Topic 3.

---

## Example 2 — Logistics (build the matrix from the diagram, 6 variables)

**Concept:** a shipping network; the unknowns are the flow on each route. He reads
the diagram and **builds the whole augmented matrix himself**, the screen checks
it, then he reduces it. This is the "too big to picture" maturity moment.

**The network (tree-structured → unique flows).** Factory **F** (supplies 100)
ships to warehouses **W1** and **W2**, which ship to stores **A, B** (from W1) and
**C, D** (from W2). Six routes = six unknowns:
- x₁ = F→W1, x₂ = F→W2, x₃ = W1→A, x₄ = W1→B, x₅ = W2→C, x₆ = W2→D.
Store demands: A = 30, B = 20, C = 25, D = 25.

**Diagram panel:** draw this network with plotly using existing helpers — nodes as
labeled points (`add_point_2d`), routes as labeled arrows (`add_vector_2d`) — with
each store's demand and the factory's supply clearly labeled. (Static, not
clickable; the art just has to be readable and carry every number he needs.)

**Build-the-matrix step:** the six balance equations (flow in = flow out at each
node), in this row order, are what he should enter:
- Row 1 (W1): `x₁ − x₃ − x₄ = 0`
- Row 2 (W2): `x₂ − x₅ − x₆ = 0`
- Row 3 (store A): `x₃ = 30`
- Row 4 (store B): `x₄ = 20`
- Row 5 (store C): `x₅ = 25`
- Row 6 (store D): `x₆ = 25`
Give him an **editable 6×7 augmented grid** (use `widgets.matrix_editor`-style
number inputs, all defaulting to 0) and a **Check** button that compares his grid
(row-normalized to allow equivalent scaling is NOT required — compare to the exact
target above) to the correct `[A | b]`. On mismatch, report which rows are wrong
(don't reveal the answer). A **"Fill it in for me"** button loads the correct
matrix so he can skip to reducing on mechanics-only days. Once correct/filled,
load it into `t05b_e2_M`/`_orig` and render `workbench("t05b_e2", 6)`.

**Correct matrix** (for the checker and the fill button):
`A = [[1,0,-1,-1,0,0],[0,1,0,0,-1,-1],[0,0,1,0,0,0],[0,0,0,1,0,0],
[0,0,0,0,1,0],[0,0,0,0,0,1]]`, `b = (0,0,30,20,25,25)`. Solution
x = (50, 50, 30, 20, 25, 25).

**Solution readout — label by route, not x₁…x₆:**
> F→W1: 50 units · F→W2: 50 units · W1→A: 30 · W1→B: 20 · W2→C: 25 · W2→D: 25.

**Notice (always shown):**
> The unknowns are how much travels on each route. "Flow in = flow out" at every
> node gives one equation each; solving the system is the shipping plan. Six
> unknowns — no picture for that — but the same three moves solve it. (Networks
> with alternative routes can have *many* valid plans; this tree has exactly one.)

---

## Example 3 — Circuit (fill values into a structured matrix, 3 currents)

**Concept:** a DC circuit; the unknowns are the currents. The equation
**structure and signs are pre-placed** (Kirchhoff's sign bookkeeping is provided);
he reads the resistance and voltage **values** off the diagram and types them into
the marked cells. Then he reduces. Ties forward to Topic 9.

**The circuit (fixed topology).** A battery of voltage **V** drives three branches
carrying currents **I₁, I₂, I₃**, with resistors **R1, R2, R3**. The governing
equations are:
- Node (KCL): `I₁ − I₂ − I₃ = 0`
- Loop 1 (Ohm/KVL): `R1·I₁ + R2·I₂ = V`
- Loop 2: `R2·I₂ − R3·I₃ = 0`

**Diagram panel:** a simple, clearly labeled circuit schematic (battery labeled V,
resistors labeled R1/R2/R3, branch currents labeled I₁/I₂/I₃). Drawn with plotly
lines/shapes or an SVG — the exact art is implementation, but every value he must
read (V, R1, R2, R3) and the current labels must be visible. Diagram values:
**V = 12, R1 = 2, R2 = 4, R3 = 4.**

**Fill-the-values step:** present the augmented matrix with the **structure and
signs fixed** and only the value cells editable — i.e. the matrix is
`[[1, −1, −1 | 0], [R1, R2, 0 | V], [0, R2, −R3 | 0]]` with `R1, R2, R3, V` as the
blanks he fills (note R2 appears in two rows — filling it once should populate
both, or check both). A **Check** button verifies against the diagram values; a
**"Fill it in for me"** button loads them. Then load
`A = [[1,-1,-1],[2,4,0],[0,4,-4]]`, `b = (0,12,0)` into `t05b_e3_M`/`_orig` and
render `workbench("t05b_e3", 3)`.

**Solution:** I₁ = 3 A, I₂ = 1.5 A, I₃ = 1.5 A. Readout:
> Branch 1 current I₁ = 3 A · I₂ = 1.5 A · I₃ = 1.5 A.

**Notice (always shown):**
> The unknowns are the currents. The same "what flows in must flow out" idea as
> the shipping network — electricity and freight obey the same linear algebra.
> Here the signs are set up for you; you just read the resistor and battery values
> off the diagram.

**Looking ahead (st.info, on this screen):**
> This circuit runs on steady (DC) current, so the answers are plain numbers. In
> Topic 9 the *same circuit* on alternating current uses **complex numbers** to
> capture both the size and the timing of each current — same question, richer
> answer.

---

## New helper to add

`widgets.aug_array_latex(M, n_unknowns)` — return a LaTeX string for an augmented
matrix using `\left[\begin{array}{…|c} … \end{array}\right]` (column spec: one `c`
per unknown, a `|`, then one `c` for b). Used by the workbench display.

## Registration

In `app.py`: add `t05b_elimination` to the `from topics import …` line and insert
`(t05b_elimination.TITLE, t05b_elimination),` in `TOPICS` immediately after the
`t05_systems` entry.

## Acceptance checklist (verify before committing)

- [ ] Sidebar shows "5.5 · Elimination & Triangular Form" after Topic 5.
- [ ] **Workbench:** manual Add/Swap/Scale each apply correctly and append to the
      log; Undo and Reset work; "Do one step" performs one standard op; "Run to
      triangular form" produces zeros below the diagonal.
- [ ] **Scenarios:** "One solution" back-substitutes to (2,3,−1); "Needs a row
      swap" triggers a swap and solves to (3,2,1); "Redundant" shows a zero row +
      infinitely-many banner; "Contradiction" shows a 0 = nonzero row + no-solution
      banner.
- [ ] **Logistics:** the network diagram is readable; entering the six balance
      equations and pressing Check validates (wrong rows are flagged, answer not
      revealed); "Fill it in for me" works; reducing solves to
      (50,50,30,20,25,25) shown as labeled routes.
- [ ] **Circuit:** the schematic is readable; filling R1=2,R2=4,R3=4,V=12 and
      Check validates; reducing solves to I₁=3, I₂=1.5, I₃=1.5 A; the Topic 9
      looking-ahead note appears.
- [ ] `widgets.aug_array_latex` added; app runs with `streamlit run app.py`, no
      import errors.
