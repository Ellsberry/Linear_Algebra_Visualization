# Build Spec — Topic 5.5, Example: Infinite and No Solutions (NEW screen)

> **SCOPE.** This spec covers ONE new screen in Topic 5.5: "Infinite and No
> Solutions", inserted at selector position 3. It REUSES the shared elimination
> engine (`topics/t05b_elimination/workbench.py`, the `workbench()` UI). It does not
> modify the other screens' behavior. The rename of Screen 1 ("The workbench" →
> "Augmented Matrix"), the trim of that screen's presets, and the selector reorder
> are recorded as a small edit to `specs/topic5b_elimination.md` (not here). This is a
> living spec — more cases may be added later.

## What this screen teaches

Every linear system has exactly one of three outcomes: one solution, no solution, or
infinitely many. The Augmented Matrix screen (Screen 1) shows the one-solution path.
This screen is the dedicated home for the other two — the cases elimination reveals
as a special bottom row. The student watches each system eliminate and reads the
outcome directly off the augmented matrix.

The teaching hook: the two systems are **almost identical** — same coefficients (the
second equation is just twice the first), differing by a single number on the right.
That one number is the difference between "no solution" and "infinitely many."

## The two cases (verified numerically — do not change these facts)

Both use the same coefficient matrix A = [[1,1,1],[2,2,2],[1,2,3]] (row 2 = 2 × row 1),
so eliminating row 2 against row 1 always zeros its coefficients. Only b differs:

- **No solution** — b = (6, 15, 14). Eliminating row2 − 2·row1 gives `0 0 0 | 3`,
  i.e. **0 = 3**, impossible. rank(A) = 2, rank([A|b]) = 3.
- **Infinitely many** — b = (6, 12, 14). Eliminating row2 − 2·row1 gives `0 0 0 | 0`,
  i.e. **0 = 0**, always true → a free variable. rank(A) = 2, rank([A|b]) = 2.

(The engine's `_show_scenario` already detects both: a zero-coefficient row with
nonzero b → "no solution"; a fully-zero row with pivot count < unknowns → "infinitely
many". No engine change needed.)

## Layout / interaction

- Reuse `workbench(key, 3, ...)` exactly as Screen 1 does — the same augmented-matrix
  UI with Do one step / Run to triangular form / manual row ops / Undo / Reset and
  the scenario banner. No equation_builder (there is no modeling step here).
- Two presets, loaded via the workbench's preset-loading path (`_load_aug` / the same
  mechanism Screen 1 uses), keys prefixed `t05b_infns_*` so state is isolated from
  Screen 1's `t05b_e1_*`:
  - **"No solution (0 = 3)"** → A = [[1,1,1],[2,2,2],[1,2,3]], b = (6,15,14).
  - **"Infinitely many (0 = 0)"** → A = [[1,1,1],[2,2,2],[1,2,3]], b = (6,12,14).
- Intro + notice as below; the workbench scenario banner supplies the live outcome
  message as the student eliminates.

## Screen text

**Intro (verbatim):**
> **Infinite and no solutions.** Not every system has a single answer. Some have
> none, and some have infinitely many — and elimination shows you which, by what
> happens to the bottom row. These two systems look almost the same: the second
> equation is just twice the first, and only one number on the right-hand side is
> different. Run each one and watch that one number decide everything.

**Notice (st.info, verbatim):**
> Eliminate row 2 against row 1 in both systems and its coefficients vanish — you're
> left with 0 = something. If that something is not zero (here 0 = 3), the equation is
> impossible and the system has **no solution**. If it's 0 = 0, the equation was
> always true — it added nothing, so one unknown is free and there are **infinitely
> many solutions**. Same coefficients, one different number, opposite outcomes.

**Closing (verbatim):**
> "No solution" and "infinitely many" are exactly the cases where a matrix has no
> inverse (det = 0, from Topic 4) — the system can't be pinned to a single answer.
> Which one you get depends on the right-hand side.

## Reuse vs new

- REUSE: `workbench()` and its helpers from `workbench.py` — no changes to the engine.
- NEW: one screen module `topics/t05b_elimination/infinite_nosolution.py` exposing a
  render function (match the naming style of the other screens, e.g.
  `render_infinite_nosolution()` or `_example_infns()`), plus its two presets.
- WIRING: registered in `__init__.py`'s selector at position 3 (see the companion
  edit to `specs/topic5b_elimination.md`).

## Acceptance checklist

- [ ] New screen appears at selector position 3, labeled "3 · Infinite and No Solutions".
- [ ] Two presets load correctly; state keys prefixed `t05b_infns_` (isolated from
      Screen 1).
- [ ] "No solution" preset eliminates to a `0 0 0 | 3` row and the banner reads no
      solution; "Infinitely many" eliminates to `0 0 0 | 0` and the banner reads
      infinitely many.
- [ ] Intro, notice, and closing render verbatim.
- [ ] Reuses workbench() — no edits to workbench.py.
- [ ] The two cases have been REMOVED from Screen 1 (Augmented Matrix) so they aren't
      taught twice (companion edit to Screen 1's presets).
