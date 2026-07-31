# Build Spec — Topic 4: Inverse Transformations

**For the builder (Claude Code):** Implement as `topics/t04_inverse.py` (now a
per-screen package `topics/t04_inverse/`) and register in `app.py`. Follow
`CLAUDE.md`. Use the **multi-example selector** pattern (template
`topics/t01_vectors.py`): top `st.radio` selects the example; only the selected one
renders; `OVERVIEW` pinned; `HOWTO` collapsed. **Reuse the engine**
(`engine/widgets.py`, `engine/plotting.py`, `engine/animate.py`); do not hand-roll
inputs or figures. The text below is final copy — implement it, don't reword or
invent examples.

`TITLE = "4 · Inverse Transformations"`, `SLUG = "inverse"`.

## Naming convention (whole topic)

Name the transformation matrix **A** everywhere the student sees it (not "M"),
consistent with the course's Ax = b throughline. Use **A⁻¹** for the inverse.
Radio buttons read **"Apply A" / "Undo with A⁻¹"**. The shared inverse meter
renders **A⁻¹**.

## Core idea (the spine)

The **inverse** undoes a transformation: apply A, then apply A⁻¹, and every point
lands exactly back where it started. It exists **precisely when det ≠ 0**, and it
**scales area by 1/det**. This topic is the direct answer to Topic 3's cliffhanger
("det = 0 means no inverse").

Two recurring devices, used where noted:
- **There-and-back demo:** a slider `t` in [0,1] plus a radio
  `["Apply A", "Undo with A⁻¹"]`.
  - *Apply A* → draw `animate.interpolate(A, t)` (object morphs from home to the
    A-deformed shape) — EXCEPT on Robotics, which uses a point-moving graph (see
    Example 1).
  - *Undo with A⁻¹* → draw `((1-t)*np.eye(n) + t*np.linalg.inv(A)) @ A` (starts at
    the deformed shape, returns home as t→1). If A is singular, disable this option
    and show the no-inverse warning.
- **Inverse meter** `_inv_meter(A)` (define once, call on every screen):
  - `abs(det) > 1e-9`: show `det`, `1/det`, and `A⁻¹` as a bmatrix; state line
    "invertible — area scales by 1/det = {1/det:.3f}".
  - else: warning "det = 0 — no inverse. This transform can't be undone."

## Selector and always-on text

Selector (st.radio, horizontal, key `t04_example`), in THIS order:
`["1 · Robotics", "2 · Cryptography", "3 · Medical imaging", "4 · Business"]`.
Robotics opens with the clearest "undo" visual; Business ends the topic and
bridges to Topic 5 (solving Ax = b).

`OVERVIEW`:
> Topic 3 ended on a cliffhanger: det = 0 means a transformation can't be undone.
> This topic is the answer. The **inverse** of a transformation is the one that
> reverses it — apply A, then apply A⁻¹, and every point lands exactly back where
> it started. It exists only when det ≠ 0, and it scales area by 1/det. We'll meet
> "undoing" as the central question in four fields: robotics, secret codes,
> medical scans, and business planning.
>
> Note: ONLY SQUARE MATRICES HAVE AN INVERSE. How to calculate an inverse will be
> shown in lesson 5.5.

`HOWTO`:
> The left panel sets the numbers; the right panel shows the shape or the result.
> On the visual screens, use **Apply A / Undo with A⁻¹** to watch the hand or shape
> move out and then return home. The **inverse meter** shows A⁻¹ and 1/det — or
> warns you when there's no inverse.

---

## Example 1 — Robotics (engineering): recover the input

**Concept:** the hand is moved by two actuators. The two **columns** of the arm map
A are the directions those actuators push; the controls (x1, x2) say how hard each
one pushes, so the hand reaches `b = x1*(column 1) + x2*(column 2) = A*x`. The hand
can reach anything spanned by the two actuator vectors, but nothing outside them.
This screen is destination-driven: the student sets where the hand should go (b),
and the inverse works backward to the controls that get it there.

**Explanation (verbatim, shown near the top):**
> You want the hand at b. Working backward through the arm map with A⁻¹ tells you the
> controls x that get it there. Then check: pushing those controls (A·x) does land
> at b.

**Inputs:**
- Preset selectbox `t04e1_preset` (apply via `set_matrix_state` on change, tracking
  `t04e1_last`) — sets the **arm map A**:
  - **"Reachable pose"** -> `[[1.5, 0.5], [0.0, 1.0]]` (det = 1.5; the two actuator
    columns point different ways and span the whole plane).
  - **"Singular pose"** -> `[[1.0, 1.0], [1.0, 1.0]]` (det = 0; both columns point
    the same way, so the hand is stuck on one line).
- Arm map A: `editable_matrix("t04e1_A", 2, compact=True,
  label="Arm map A (columns = the two actuator directions)")`, narrow sub-column.
- Destination b: `vector_editor("t04e1_target", 2, (4.0, 2.0),
  label="Desired hand position (x, y)")`, narrow sub-column. Editable.
- **No slider, no Apply/Undo radio.** This is a solve-and-show, not a there-and-back.

**Intro line (verbatim):**
> **Robotics.** The hand is moved by two actuators. The two columns of the arm map A
> are the directions those actuators push, and the controls (x1, x2) say how hard
> each one pushes -- so the hand reaches b = x1*(column 1) + x2*(column 2). The hand
> can reach anything spanned by the two actuator vectors, but nothing outside them.

**The graph (built from primitives, NOT figure_2d):**
`new_figure_2d(rng=~8, x_title="hand x", y_title="hand y")`.
- Draw the two **actuator vectors** = columns of A, as arrows from the origin
  (`add_vector_2d`), labeled "actuator 1 (column 1)" and "actuator 2 (column 2)".
- Draw the **destination b** as a point (`add_point_2d`), labeled "destination b".
- INVERTIBLE: solve `x = A^-1 b`. Draw the solved controls as the two scaled actuator
  contributions tip-to-tail: origin -> x1*(col1) -> +x2*(col2), landing exactly on b
  (two `add_vector_2d` arrows), so the student SEES the controls combine to reach b.
- SINGULAR: do NOT solve. Draw the **reachable line** = span of the (parallel)
  columns, a long segment through the origin along the column direction
  (`add_vector_2d(..., arrow=False)`), labeled "everything the arm can reach". Plot
  b; if off the line, label "unreachable -- off the line". For `[[1,1],[1,1]]` the
  line is y = x.

**Inverse meter** `_inv_meter(A)` under the figure.

**Math (left column), IN THIS ORDER, all live:**
1. **A and its determinant, then A⁻¹ and its determinant.** Show
   `A = [..]`, `det A = ..`; then `A⁻¹ = [..]`, and `det A⁻¹ = 1/det A = ..`
   (show det A⁻¹ AS 1/det A so the reciprocal relationship is explicit, not two
   loose numbers). Invertible only; if singular, skip to the singular explanation.
2. **Solve (working backward):** `x = A⁻¹ b = [A⁻¹][b] = [x]` with live numbers.
3. **Check (forward):** `A x = [A][x] = [b]` -- confirms the solved controls land
   on b.

**Singular explanation (verbatim, shown when det = 0 instead of the 3 steps):**
> This arm map is singular: column 2 is the same as column 1, so both actuators push
> the same way and det A = 0. A matrix with determinant 0 has no inverse -- you can't
> work backward from a hand position to the controls. With both columns pointing the
> same direction, the hand is stuck on that single line and can't reach anywhere off
> it.

**Notice (always shown):**
> Every robot arm and animated character solves an inverse problem: given where the
> hand should go, work backwards to the settings that put it there. When the inverse
> doesn't exist, the arm physically can't reach that way -- it's stuck in a
> "singular" pose, able to reach only along a single line. (Real arms bend at angles,
> so this is the linear heart of the idea, not the full mechanics.)

---

## Example 2 — Cryptography (computer science): encode and decode with real letters

**Concept:** a matrix scrambles a message; its inverse unscrambles it. A classic
**Hill cipher** on 2-letter blocks (letters A–Z ↔ 0–25, arithmetic mod 26).

**Inputs:**
- Text input `st.text_input` for a short word, key `t04e2_msg`, default `"MATH"`.
  Uppercase it, keep A–Z only, split into 2-letter blocks, pad a final odd letter
  with `X`.
- Preset selectbox `t04e2_key` for the cipher matrix M:
  - **"Key 1"** → `[[3, 3], [2, 5]]` (det = 9, invertible mod 26).
  - **"Key 2"** → `[[1, 2], [3, 5]]` (det = −1 ≡ 25, invertible mod 26).
  - **"Broken key (singular)"** → `[[2, 4], [1, 2]]` (det = 0 — no inverse; the
    message can't be recovered).

**Logic:** for each block vector p, ciphertext `c = (M @ p) mod 26`; to decode,
compute the **modular inverse of M mod 26** (`M⁻¹ mod 26`) and `p = (M⁻¹ @ c) mod
26`. (Compute the modular inverse with NumPy/Python; the modular inverse exists
iff gcd(det, 26) = 1.) If the key is singular or not invertible mod 26, decoding
fails — show the warning instead of a decoded word.

Naming note: cryptography's cipher matrix stays **M** (a Hill-cipher key mod 26 —
a different object from the geometric transform A used on the other screens); do
not rename it to A. This is the one screen where M is correct.

**Right panel — a small table** (not a geometric plot; the mod-26 wrap makes a
plot confusing). Columns per letter: plaintext letter, its number, ciphertext
number, ciphertext letter, decoded letter. Show the scrambled CIPHERTEXT word and
the recovered PLAINTEXT word prominently above/below the table.

**Inverse meter (crypto variant):** show M, det, and either the decryption matrix
`M⁻¹ (mod 26)` as a bmatrix, or the warning "this key can't be undone — its
determinant shares a factor with 26 (or is 0), so the message is unrecoverable."

**Notice (always shown):**
> Multiplying by a matrix scrambles a message; multiplying by its inverse
> unscrambles it. Not every key works — its determinant must be "compatible" with
> the 26 letters. If the determinant is 0, the message is destroyed: there's no
> inverse, so no way to read it back.

**Show the math (expander):** the block being encoded, `c = M p (mod 26)`, the
decryption matrix, and `p = M⁻¹ c (mod 26)`. One line noting the arithmetic is mod
26 because there are 26 letters — the one place the inverse is "modular" rather
than the ordinary 1/det.

---

## Example 3 — Medical imaging: measure, then reconstruct

**Concept:** a scanner measures a transformed version of the body; reconstructing
the true image means applying the inverse of the measurement. If the data is
nearly incomplete (det close to 0), the inverse is huge and unstable.

**Inputs:**
- `editable_matrix("t04e3_A", 2, compact=True, label="Measurement A")`.
- Preset selectbox `t04e3_preset`:
  - **"Full data"** → `[[1.0, 0.5], [0.5, 1.0]]` (det = 0.75 — clean
    reconstruction).
  - **"Too few angles (unstable)"** → `[[1.0, 1.0], [1.0, 1.05]]` (det = 0.05 —
    invertible but A⁻¹ has large entries; small errors blow up).
  - **"No data in a direction (singular)"** → `[[1.0, 1.0], [1.0, 1.0]]` (det = 0
    — can't reconstruct; information is lost).
- There-and-back slider + radio on the **rocket** (`plotting.figure_2d(T(t),
  obj="rocket")`), framed as "measure" (Apply A) then "reconstruct" (Undo with
  A⁻¹).

**Inverse meter** under the figure. For the unstable preset, the large 1/det and
large A⁻¹ entries should be visible — that *is* the instability.

**Notice (always shown):**
> A CT scanner never sees your insides directly — it measures transformed data
> and *inverts* the transformation to reconstruct the image. With too little data
> the inverse becomes unstable, so small measurement errors explode — which is why
> scans need enough angles. (Topic 10 shows the real version: MRI reconstruction
> is an inverse Fourier transform.)

**Show the math (expander):** A, A⁻¹ (or none), det, 1/det; note that a tiny det
makes 1/det and A⁻¹ large = unstable.

---

## Example 4 — Business / economics: the algebra, forward and back. ENDS THE TOPIC.

**Concept:** a matrix maps production → resources used; the inverse answers "I
have these resources — how much of each product can I make?" Here the **algebra is
the centerpiece**, shown openly (not hidden in an expander).

**Inputs:**
- `editable_matrix("t04e4_A", 2, compact=True, label="Resource-usage matrix A (column j = resources for product j)")`.
- `widgets.vector_editor("t04e4_x", 2, (4.0, 2.0), label="Production x (units of each product)")`.
- Preset selectbox `t04e4_preset`:
  - **"Two distinct products"** → `[[2, 1], [1, 3]]` (det = 5, invertible).
  - **"Proportional products (singular)"** → `[[2, 4], [1, 2]]` (det = 0 — the two
    products use resources in the same proportion; the inverse fails).

**Compute:** `r = A @ x` (resources used). If invertible, also recover `x = A⁻¹ @
r` to show the round trip returns the original production.

**Right panel (secondary):** `plotting.new_figure_2d(rng=14, x_title="resource 1",
y_title="resource 2")` showing the production carried to the resource point
`r = Ax` (an arrow/point), and on recovery the same point mapped back. Keep it
light — the math is the star here.

**The algebra block (render openly with `st.latex`, in this order):**
1. Forward, general: `r = A x = [[a11,a12],[a21,a22]] [x1,x2]ᵀ = [a11 x1 + a12 x2,
   a21 x1 + a22 x2]ᵀ`.
2. Forward, with his live numbers (substitute A and x, show r).
3. Inverse, general formula:
   `A⁻¹ = (1/det A) [[a22, -a12], [-a21, a11]]`, with
   `det A = a11 a22 − a12 a21` — emphasize the **det in the denominator**.
4. Inverse, with his numbers (substitute, show A⁻¹).
5. Recover and verify: `x = A⁻¹ r = [original x]` — the round trip.

**Singular preset behavior:** when det = 0, step 3 shows `1/det = 1/0` is
**undefined** — render the formula with the denominator highlighted and the
caption: "These two products use resources in the same proportion, so from the
resources alone you can't tell how much of each you made. There's no way to work
backwards — the inverse doesn't exist."

**Optional sub-expander "Solve for a resource target":** let him enter a resource
target r directly via `vector_editor`; compute `x = A⁻¹ r`. If any component of x
is negative, show the honesty note: "The algebra returns a negative number of
products — mathematically valid, physically impossible. The model is more
permissive than a real factory."

**Notice (always shown):**
> Run the matrix forward and it tells you resources used; run it backward (the
> inverse) and it tells you how much to produce to use exactly what you have. This
> "solve A x = r for x" is the exact question of the next topic — linear systems.

**Inverse meter** under the algebra.

---

## Registration

In `app.py`: add `t04_inverse` to the `from topics import ...` line and insert
`(t04_inverse.TITLE, t04_inverse),` in `TOPICS` immediately after the
`t03_determinant` entry.

## Acceptance checklist (verify before committing)

- [ ] Sidebar shows "4 · Inverse Transformations" after Topic 3.
- [ ] Selector switches between exactly four screens; only the selected renders.
- [ ] Naming: A / A⁻¹ everywhere the student sees a transform, radios read
      "Apply A / Undo with A⁻¹", inverse meter renders A⁻¹. (Cryptography's Hill
      key stays M by design.)
- [ ] OVERVIEW ends with the "ONLY SQUARE MATRICES HAVE AN INVERSE..." note.
- [ ] **Robotics (redesigned, destination-driven):** preset sets arm map A;
      destination b is editable; NO slider and NO Apply/Undo radio; the graph shows
      the two actuator-column arrows, the destination b, and (invertible) the solved
      controls drawn tip-to-tail landing on b, NOT the square warp; math is 3 steps
      in order — (1) A/det A then A⁻¹ with det A⁻¹ shown as 1/det A, (2) x = A⁻¹b,
      (3) check A·x = b; the SINGULAR pose draws the reachable line with b marked
      reachable/unreachable and shows the "column 2 = column 1 → det 0 → no inverse"
      explanation instead of the 3 steps. Arm map A and destination b render in
      narrow sub-columns (no screen-wide inputs).
- [ ] **Cryptography:** typing a word shows scrambled ciphertext letters and a
      correctly decoded word with Key 1 and Key 2; the broken key shows the
      "can't be undone" warning and no valid decode.
- [ ] **Medical:** "Full data" reconstructs cleanly; "Too few angles" shows a
      large 1/det / large A⁻¹ entries (instability); "No data" is singular and
      can't reconstruct.
- [ ] **Business:** the five-step algebra renders with live numbers; round trip
      returns the original x; the singular preset shows 1/det = 1/0 undefined with
      the caption; the optional target solver shows the negative-production note
      when applicable.
- [ ] Every screen shows the inverse meter; app runs with `streamlit run app.py`
      and no import errors.
