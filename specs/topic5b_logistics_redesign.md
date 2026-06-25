# Build Spec — Topic 5.5, Logistics screen REDESIGN

**Status:** approved design, not yet built. Replaces the current `_example_two`
(Logistics) in `topics/t05b_elimination/logistics.py`. Follow `CLAUDE.md`.

## Why the redesign

The current Logistics screen has three fatal flaws:
1. The network is a pure **tree**, so its augmented matrix is **already upper
   triangular** — elimination has nothing to do. The screen can't teach the
   method it exists to teach.
2. The build step is a 6×7 grid of `number_input` boxes — a spreadsheet, not a
   matrix. It doesn't look like the bracketed matrices used everywhere else, and
   it reduces "modeling" to transcription.
3. No clear statement of what the student is solving for.

The redesign fixes all three: a **cycle network** (so elimination does real
work and the system has infinitely many plans), an **(2a) node-balance builder**
(student picks in/out routes per node; app assembles a bracketed `[A|b]`), and a
**framing sentence** stating the goal.

## The network (a store fed by BOTH warehouses → a cycle)

Nodes: F (factory, supply 100), W1, W2 (warehouses), A, B, C, D (stores).
**Store B is reachable from both W1 and W2** — the cycle. Two paths to B is the
free choice that makes plans non-unique.

Routes (the 7 unknowns):
- x₁: F → W1
- x₂: F → W2
- x₃: W1 → A
- x₄: W1 → B   (W1's path to the shared store)
- x₅: W2 → B   (W2's path to the shared store — the extra route making the cycle)
- x₆: W2 → C
- x₇: W2 → D

Demands: A=30, B=20, C=25, D=25 (total 100 = supply). Supply at F = 100.

## The 7 balance equations (one per node — what the student builds)

Convention: each node, (flow in) − (flow out) handled as +1 in / −1 out; demand
or supply on the right.

- **F:**  x₁ + x₂ = 100         (supply leaves the factory)
- **W1:** x₁ − x₃ − x₄ = 0      (in = out)
- **W2:** x₂ − x₅ − x₆ − x₇ = 0
- **A:**  x₃ = 30
- **B:**  x₄ + x₅ = 20          ← shared store: TWO routes in (the teachable row)
- **C:**  x₆ = 25
- **D:**  x₇ = 25

Augmented matrix [A | b], rows in node order F, W1, W2, A, B, C, D; columns
x₁ … x₇, b:

```
[ 1  1  0  0  0  0  0 | 100 ]   F
[ 1  0 -1 -1  0  0  0 |   0 ]   W1
[ 0  1  0  0 -1 -1 -1 |   0 ]   W2
[ 0  0  1  0  0  0  0 |  30 ]   A
[ 0  0  0  1  1  0  0 |  20 ]   B
[ 0  0  0  0  0  1  0 |  25 ]   C
[ 0  0  0  0  0  0  1 |  25 ]   D
```

## Verified math (checked numerically — do not change these facts)

- shape 7×7, **rank(A) = 6, rank([A|b]) = 6, unknowns = 7** → consistent with
  **exactly one free variable** → **infinitely many plans**.
- **NOT already upper-triangular** — below-diagonal nonzeros at (row2,col1),
  (row3,col2), (row4,col3), (row5,col4). Elimination must clear these: real work.
- The redundant equation is **F** (total in = total out is automatic).
- General solution, free parameter **t = x₅** (freight to B via W2):
  - x₄ = 20 − t,  x₃ = 30,  x₆ = 25,  x₇ = 25
  - x₁ = 50 − t,  x₂ = 50 + t
  - Check F: x₁ + x₂ = 100 ✓ (auto-satisfied — the redundancy)
  - Physical range (non-negative flows): **0 ≤ t ≤ 20**.
- **The story:** the shared store B's 20 units can be split between the two
  warehouses any way that adds up — send t via W2 and 20−t via W1. Every split is
  a valid shipping plan. THAT is why there are infinitely many plans, and it's a
  real logistics choice a student can picture.

## The student's task — (2a) node-balance builder

The student builds the system one node at a time, NOT by filling 42 raw cells:

- For each of the 7 nodes, the student specifies the node's balance by selecting
  **which routes flow IN** and **which flow OUT** (e.g. multiselect or checkboxes:
  "Into B: x₄, x₅; Out of B: (none); demand 20"). For source/sink nodes the
  supply/demand value is given on the diagram.
- The app converts each node's selection into a matrix row: **+1** for an
  in-route, **−1** for an out-route, the demand/supply on the right.
- Store **B is the teachable node** — it has TWO in-routes (x₄ and x₅). That's the
  moment the student sees the cycle in the equations.
- The assembled augmented matrix appears as a **clean bracketed `[A | b]`**
  (consistent with every other lesson — NOT a spreadsheet grid), with the
  vertical divider before the b column.
- Provide **Check** (validates against the target matrix above, names wrong nodes)
  and **Fill it in for me** (assembles the correct matrix and reveals the
  reduce step) — same affordances as the current screen.

## Layout (reduce scrolling; consistent with the topic)

- **Framing sentence, full width, at top:** "You're solving for the amount of
  freight on each of the seven routes (x₁…x₇) — the shipping plan where flow in =
  flow out at every node and every store's demand is met."
- **Diagram and the node-balance builder side by side** (two columns). The
  builder is the wider column if it needs the room; the diagram can be the
  narrower one. (Eyeball widths during build; if the builder is cramped, give it
  more width.)
- **Assembled bracketed [A | b]** shown below or within the builder column once
  built.
- **Workbench** (the shared elimination engine, `workbench("t05b_e2", 7,
  solution_labels=...)`) appears after Check/Fill succeeds — its internal
  [1, 1.3] wide-math columns stay (the topic's wide-math exception).
- Solution labels for the workbench readout: the seven route names
  ["F→W1","F→W2","W1→A","W1→B","W2→B","W2→C","W2→D"].

## Outcome handling

The workbench will end on the **infinitely-many-solutions** scenario (the engine
already detects this: a row goes all-zero → free variable). After reduction, the
screen should explain the result in network terms: **the free variable is how
B's 20 units split between W1 and W2 (0 ≤ via-W2 ≤ 20); every split is a valid
plan.** This is the intended, correct ending — not a single number.

## Acceptance checklist
- [ ] Framing sentence states the unknowns (route flows) and the goal up top.
- [ ] Diagram shows the cycle (B fed by W1 and W2); routes x₁…x₇ labeled.
- [ ] Node-balance builder: per node, pick in/out routes; B has two in-routes.
- [ ] App assembles a **bracketed [A | b]** (not a spreadsheet grid), divider
      before b.
- [ ] Check validates against the verified target matrix; Fill assembles it.
- [ ] After build, the workbench reduces a system that is NOT pre-triangular
      (elimination visibly does work) and lands on infinitely-many.
- [ ] The free-variable result is explained as "split B's delivery between the
      two warehouses, 0..20 either way."
- [ ] Diagram + builder side by side; far less scrolling than the old screen.
