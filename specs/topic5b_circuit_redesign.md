# Build Spec — Topic 5.5, Circuit screen REDESIGN

**Status:** approved design, not yet built. Replaces the current fill-in-values
`_example_three` in `topics/t05b_elimination/circuit.py`. Follow `CLAUDE.md`.

## Why the redesign

The current Circuit screen only has the student **fill in R/V values** — the
equation structure and signs are pre-placed. The redesign has the student
**derive and write the equations themselves** (KCL + KVL), getting loop
directions and signs right — the actual skill of circuit analysis — then see
them assembled into `[A|b]` and reduced. It reuses the shared `equation_builder`
pattern (like Logistics 2a/2b), but needs a NEW **symbolic** parser.

## Teaching points
- Student picks/reads loop directions (clockwise / counter-clockwise) and gets
  the **signs** right (the hard part).
- Student writes the **symbolic** equations (`R1*I1 + R3*I3 = V`), not just
  numbers — closer to how circuit analysis is actually taught.
- The same elimination method that solved freight networks solves circuits.
- One definite answer (unique solution).

## The verified circuit (DO NOT change these facts — checked numerically)

One battery plus five resistive elements with DISTINCT values (two of them are a
motor and a lightbulb, modeled as resistances with nice icons):

- **V = 36 V** (battery)
- **R1 = 2 Ω** (series resistor with battery)
- **R2 = 6 Ω** (resistor)
- **R3 = 8 Ω** — the **MOTOR** (resistive)
- **R4 = 4 Ω** — the **LIGHTBULB** (resistive)
- **R5 = 12 Ω** (resistor)

Five unknown **branch currents** I1…I5. Two nodes P, Q (for KCL); three marked
directional loops (for KVL).

## The 5 equations the student writes (symbolic)

- **KCL node P:**  `I1 - I2 - I3 - I5 = 0`
- **KCL node Q:**  `I2 - I4 + I5 = 0`
- **KVL loop 1 (battery):**  `R1*I1 + R3*I3 = V`
- **KVL loop 2:**  `R2*I2 - R3*I3 + R4*I4 = 0`
- **KVL loop 3:**  `R2*I2 - R5*I5 = 0`

Augmented matrix after substitution (coefficients on I1..I5 | b), rows in the
order above:
```
[ 1  -1  -1   0  -1 |  0 ]   KCL P
[ 0   1   0  -1   1 |  0 ]   KCL Q
[ 2   0   8   0   0 | 36 ]   KVL1 (R1=2, R3=8, V=36)
[ 0   6  -8   4   0 |  0 ]   KVL2 (R2=6, R3=8, R4=4)
[ 0   6   0   0 -12 |  0 ]   KVL3 (R2=6, R5=12)
```

## Verified math (do not change)
- rank(A) = 5, n = 5 -> **unique** solution.
- **I = (6, 2, 3, 3, 1) A** (clean integers).
- NOT pre-triangular (4 below-diagonal nonzeros) -> elimination does real work.
- Distinct resistor values -> each component identifiable on the diagram.

## The symbolic parser (NEW — must be built and tested before use)

The existing `eq_parser.py` only handles numeric coefficients on x-variables.
The circuit needs a **symbolic** parser that:
- Knows a symbol table: `R1=2, R2=6, R3=8, R4=4, R5=12, V=36`, and variables
  `I1..I5`.
- Parses equations like `R1*I1 + R3*I3 = V`, `I1 - I2 - I3 - I5 = 0`,
  `R2*I2 - R3*I3 + R4*I4 = 0`. Accept `*` optional (R1 I1 or R1*I1), spaces,
  subscripts, caps.
- A term is: optional resistor symbol times a current variable (`R3*I2`,
  coefficient = value of R3), OR a bare current (`I2`, coefficient 1), OR a bare
  constant / `V` on the RHS.
- Produces a coefficient row [c1..c5, b] by SUBSTITUTING the symbol values.
- **Checking is two-stage:** (1) validate the SYMBOLIC form is correct (right
  resistors in the right places, right signs) by comparing against the target
  symbolic equation up to nonzero scalar multiple AFTER substitution — i.e.
  reuse the scalar-multiple equivalence on the substituted rows. (Acceptable
  for v1: substitute then check scalar-multiple equivalence to the target row,
  which catches wrong resistors/signs since they change the coefficients.)
- Build and TEST this parser standalone (like the numeric one) against correct,
  rearranged, and wrong forms BEFORE wiring into the screen.

Student input format: `R1*I1 + R3*I3 = V` (symbolic). The checker substitutes
R/V values and validates.

## Layout / interaction (reuse the equation_builder pattern)
- Framing sentence on top: solving for the five branch currents; read the
  circuit, write each node's KCL and each loop's KVL.
- Diagram and equation builder side by side (diagram must stay visible while
  writing — it carries the marked loops and component values).
- Live assembled `[A|b]` (substituted) that fills in as equations are written;
  dashes for unwritten rows.
- Check / Fill-it-in-for-me; then the workbench (`n_unknowns=5`,
  solution_labels=["I1".."I5"], suffix " A"); unique solution I=(6,2,3,3,1).
- Note: may need a circuit-specific symbolic equation_builder variant, OR
  parameterize the existing one to accept a parser + symbol table. Decide during
  build; prefer reusing/parameterizing over duplicating.

## The diagram (nicer components + marked loops)
- Proper component icons drawn in plotly: zigzag **resistors**, a **motor**
  (circle with M), a **lightbulb** (circle with filament/X). Battery symbol as
  now.
- Label each component with its symbol and value (R1=2Ω, motor R3=8Ω,
  lamp R4=4Ω, etc.).
- Mark the two **nodes P, Q** (for KCL) and the three **loops** with directional
  arrows (so the student reads the assumed positive direction and gets signs
  right).
- Label the five branch currents I1..I5 with direction arrows.

## AC revisit (future, Topic 9)
This same circuit topology is reused in Topic 9 (AC circuits): each resistance R
becomes a complex impedance Z, the same 5 equations become complex, and the
solution is complex (magnitude + phase). Keep the topology and equation
structure clean so that callback works — same circuit, richer (complex) answer.

## Acceptance checklist
- [ ] New symbolic parser built and unit-tested (correct/rearranged accepted,
      wrong resistors/signs rejected) BEFORE wiring in.
- [ ] Diagram shows nice resistor/motor/lightbulb icons, marked nodes P/Q,
      three directional loops, labeled currents and component values.
- [ ] Student writes 5 symbolic equations; live substituted [A|b] fills in.
- [ ] Check validates symbolic correctness; Fill populates correct equations.
- [ ] Workbench reduces to the UNIQUE solution I=(6,2,3,3,1) A; real elimination.
- [ ] Reuses/extends equation_builder rather than duplicating it.
