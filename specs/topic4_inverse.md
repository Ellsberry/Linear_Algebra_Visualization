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

**Narrative / intro (verbatim):**
> **Medical imaging.** A CT scanner can't photograph a slice of you directly. It
> shoots X-rays through the body from many angles and records how much comes out the
> other side. Each reading isn't a picture — it's a blend of everything along that
> X-ray's path.
>
> The shape below is a cross-section of a leg bone: the outer ring is hard bone, the
> inner ring is the soft marrow inside. We pick out specific points on it — call them
> p1, p2 — the true positions of the bone's edge and the marrow's edge.
>
> **Matrix A is built into the scanner.** It's set by the manufacturer and describes
> the physics of how X-rays pass through and get measured — how many angles, where
> the detectors sit. Multiplying a true point by the matrix A gives the scanner's
> measurement of that point — so A turns each real position on the slice into the
> reading the machine records.
>
> **Matrix A⁻¹ runs it backward.** It takes the scanner's measurements and unmixes
> them to recover the true points p1, p2 — turning the raw readings back into a
> picture of the bone and marrow you can actually look at. That recovery *is* the
> reconstructed image on your screen.
>
> The catch: real readings carry a little error, and when det A is close to zero, A⁻¹
> magnifies that error enormously — so the reconstructed bone comes out badly wrong.
> Drag the error slider on each preset to see it.

**The object:** a **leg-bone cross-section** — an outer bone-ring polygon with an
inner marrow-ring polygon. Shown as a faint GHOST (true slice) and a solid
RECONSTRUCTED slice; they overlap when reconstruction is good and separate when it's
unstable.

**Inputs:**
- Preset selectbox `t04e3_preset` — sets the scanner matrix **A**:
  - **"Full data"** -> `[[1.0, 0.5], [0.5, 1.0]]` (det = 0.75; stable).
  - **"Too few angles (unstable)"** -> `[[1.0, 1.0], [1.0, 1.05]]` (det = 0.05;
    invertible but A⁻¹ entries ~21 — the same error is amplified ~19-29x).
  - **"No data in a direction (singular)"** -> `[[1.0, 1.0], [1.0, 1.0]]` (det = 0;
    no inverse — the slice can't be reconstructed).
- Scanner matrix A: `editable_matrix("t04e3_A", 2, compact=True,
  label="Scanner matrix A")`, narrow sub-column.
- **Measurement error slider** `scalar_slider("t04e3_err", "Measurement error", 0.0,
  0.5, 0.0, 0.01)` — adds a small error (in the x direction) to each reading before
  reconstruction. At 0 the reconstruction is perfect.
- No morph slider, no Apply/Undo radio.

**The graph (leg-bone cross-section, ghost vs reconstructed, from primitives):**
Two closed polygons: outer bone ring and inner marrow ring (coordinates supplied in
the build prompt). Two labeled landmark points: p1 = bone edge (top of the outer
ring), p2 = marrow edge. For every polygon point p: reading = A·p; add error
E = (err, 0); reconstructed = A⁻¹·(A·p + E).
- Draw the TRUE bone (both rings) as a faint ghost, labeled "true slice".
- Draw the RECONSTRUCTED bone (both rings) solid, labeled "reconstructed". At error 0
  they coincide; on the unstable preset a small error tears the reconstruction away.
- Mark p1 ("bone edge") and p2 ("marrow edge") on the true bone.
- rng ~10. SINGULAR: no A⁻¹ — draw only the ghost + "no inverse — the slice can't be
  reconstructed."

**Inverse meter** `_inv_meter(A)` under the figure.

**Math (left column) — matrices shown once with plain-word labels, then a live
5-step pipeline in plain English (numbers as illustration, no bare symbols leading).
A⁻¹ does not change when error is added; steps 2-5 do. State this.**

Header (fixed as the slider moves):
- `A = [..]` labeled "**A**: real slice → scanner reading" and `det A = ..`.
- Invertible: `A⁻¹ = [..]` labeled "**A⁻¹**: scanner reading → recovered image",
  `det A⁻¹ = 1/det A = ..`, plus the line "A⁻¹ doesn't change when you add error — the
  error is in the reading, not the matrix." (When det A is near zero, note A⁻¹'s
  entries are huge — that is the instability.)

Then the LIVE pipeline as four lines (both landmarks per line where sensible), plus
one closing sentence. Lines 2 and 4 show the ACTUAL MATRIX ARITHMETIC via st.latex +
w.bmatrix (one equation per landmark), not just result tuples. Lines 2-4 change with
the slider; A and A⁻¹ stay fixed:
1. (plain sentence) "The actual bone edge p1 is at (p1); the actual marrow edge p2 is
   at (p2)."
2. (plain sentence) "The scanner measures each point by multiplying it by A:" THEN
   two st.latex lines:
     A·p1:  A [p1] = [A][p1] = [reading1]   (bmatrix of A, bmatrix of p1, bmatrix of A·p1)
     A·p2:  A [p2] = [A][p2] = [reading2]
3. (plain sentence) "If the machine is off by {err} in the x-direction, the readings
   become (reading1+err) and (reading2+err)." (plain, no matrix math)
4. (plain sentence) "A⁻¹ unmixes the (errored) readings back into positions:" THEN
   two st.latex lines:
     A⁻¹(reading1+err) = [A⁻¹][reading1+err] = [recon1]
     A⁻¹(reading2+err) = [A⁻¹][reading2+err] = [recon2]
   then a plain line: "— instead of the true (p1) and (p2)."
5. (sentence) "On Full data these barely move; on Too few angles the same error
   throws them far off."

**Instability sentence (verbatim, invertible only):**
> A tiny det makes 1/det and the entries of A⁻¹ large — so every small measurement
> error gets amplified by that factor. On "Full data" the reconstruction barely
> moves; on "Too few angles" the same error throws it far off. That is the
> instability.

**Singular message (verbatim, when det = 0):**
> det A = 0 — no inverse. The scan lost information in one direction, so there is no
> way to unmix the readings back into the true slice.

**Notice (always shown):**
> A CT scanner never sees your insides directly — it measures blended data and
> *unmixes* it (applies the inverse) to reconstruct the image. With too little data
> the inverse becomes unstable, so small measurement errors explode — which is why
> scans need enough angles. (Topic 10 shows the real version: MRI reconstruction is
> an inverse Fourier transform.)

---

## Example 4 — Business / economics: the algebra, forward and back. ENDS THE TOPIC.

**The story:** a bakery makes two products — **cakes** and **cookies** — from two
resources — **flour** and **sugar**. The matrix A is the recipe table: each COLUMN is
one product's recipe (how much flour and sugar it needs). Run A forward and it tells
you the total resources a batch uses; run it backward (the inverse) and it answers
"I have this much flour and sugar — how many cakes and cookies can I make?" This is
the screen where the **algebra is the star**, shown openly and explained line by line.

**Intro line (verbatim):**
> **Business.** A bakery makes cakes and cookies out of flour and sugar. The recipe
> matrix A has one column per product: column 1 is a cake's recipe (flour, sugar),
> column 2 is a cookie's recipe. Multiply A by how many of each you bake and it tells
> you the total flour and sugar used. The inverse runs it backward: given the flour
> and sugar you have, it finds how many cakes and cookies that makes.

**Inputs:**
- Preset selectbox `t04e4_preset` — sets the recipe matrix **A**:
  - **"Two different recipes"** -> `[[2.0, 1.0], [1.0, 3.0]]` (det = 5; a cake needs
    2 flour + 1 sugar, a cookie needs 1 flour + 3 sugar — genuinely different, so the
    inverse works).
  - **"Recipes in the same ratio (singular)"** -> `[[2.0, 4.0], [1.0, 2.0]]` (det = 0;
    the cookie uses exactly twice the cake's flour AND twice its sugar — same ratio,
    so from totals alone you can't tell them apart, and the inverse fails).
- Recipe matrix A: `editable_matrix("t04e4_A", 2, compact=True,
  label="Recipe matrix A (col 1 = cake, col 2 = cookie; rows = flour, sugar)")`,
  narrow sub-column.
- Production x: `vector_editor("t04e4_x", 2, (4.0, 2.0),
  label="How many you bake (cakes, cookies)")`, narrow sub-column.

**Compute:** `r = A @ x` (flour and sugar used). If invertible, recover
`x = A⁻¹ @ r` to show the round trip returns the original batch.

**Right panel (secondary, keep light):** `new_figure_2d(rng=14,
x_title="flour used", y_title="sugar used")` showing the resource point r = Ax (an
arrow/point), and on recovery the round-trip point mapped back. The math is the star.

**The algebra block — each step LED BY A PLAIN SENTENCE, formula after. In order:**

1. **"How the resources add up (in general):"**
   `r = A x` written out: `[[a11,a12],[a21,a22]][x1,x2] = [a11 x1 + a12 x2, a21 x1 +
   a22 x2]`. Gloss: "each product uses some flour and some sugar; the total used is
   A times how many you bake."
2. **"With your recipes and batch:"** the same with live numbers — A, x, and the
   resulting r, via w.bmatrix. Gloss naming the result: "so this batch uses {r1}
   flour and {r2} sugar."
3. **"To work backward, we need A⁻¹."** Show the 2x2 inverse formula
   `A⁻¹ = (1/det A) [[a22, -a12], [-a21, a11]]` with det A = a11 a22 − a12 a21.
   Gloss (plain-English explanation of the adjugate, verbatim): "For a 2×2 you build
   the inverse by a fixed recipe: swap the two diagonal numbers, flip the sign of the
   other two, and divide everything by the determinant. The determinant sits in the
   denominator — so if it's zero, you're dividing by zero and there is no inverse."
   Show det A = {value}.
4. **"Your A⁻¹ (with numbers):"** the numeric inverse via w.bmatrix.
5. **"How many of each product the resources make:"**
   `x = A⁻¹ r = [A⁻¹][r] = [x]` live, and the success line "Round trip returns
   {x1} cakes and {x2} cookies ✓".

**Singular preset behavior (det = 0), verbatim caption under step 3 instead of steps
4-5:**
> These two recipes use flour and sugar in the very same ratio — the cookie is just a
> double cake. So from the flour and sugar totals alone you can't tell how many of
> each you made. There's no way to work backward, and the inverse doesn't exist
> (dividing by det A = 0).

**Optional sub-expander "Solve for a resource target":** let the student enter a
flour/sugar amount directly via `vector_editor` (label "Flour and sugar on hand");
compute `x = A⁻¹ r`. If any component is negative, show the honesty note (verbatim):
> The algebra returns a negative number of cakes or cookies — mathematically valid,
> physically impossible. The model is more permissive than a real bakery.

**Inverse meter** `_inv_meter(A)` under the graph.

**Notice (always shown, verbatim):**
> Run the recipe matrix forward and it tells you the resources a batch uses; run it
> backward (the inverse) and it tells you how much to bake to use exactly the flour
> and sugar you have. This "solve A x = r for x" is the exact question of the next
> topic — linear systems.

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
- [ ] **Medical (redesigned, mix/unmix leg bone):** narrative explains CT X-rays in
      plain words (readings are a blend along each path; A is built into the scanner;
      A⁻¹ unmixes readings back to true points p1,p2); object is a LEG-BONE
      cross-section (outer bone ring + marrow ring) shown ghost (true) vs solid
      (reconstructed); preset sets scanner A (Full/unstable/singular) compact in a
      narrow sub-column; measurement-error slider, NO morph/radio; math shows A and
      A⁻¹ once with plain-word labels (real slice->reading / reading->recovered), then
      a LIVE 5-step pipeline for two landmarks (bone edge, marrow edge) each led by a
      plain sentence with numbers after, steps 2-5 moving with the slider while A⁻¹
      stays fixed (stated); singular shows ghost only + "no inverse -- can't unmix";
      naming A/A⁻¹ throughout.
- [ ] **Business (de-crypted, bakery):** concrete story — cakes & cookies from flour
      & sugar; A is the recipe table (col 1 = cake, col 2 = cookie; rows = flour,
      sugar), shown compact in a narrow sub-column; production input labeled "how many
      you bake (cakes, cookies)"; the 5 algebra steps each led by a PLAIN SENTENCE
      with the formula after; step 3 explains the 2×2 adjugate in words (swap the
      diagonal, flip the other two signs, divide by det) and why det=0 kills it;
      round trip returns the original batch; the singular preset ("recipes in the same
      ratio") shows the cookie-is-a-double-cake caption; the optional target solver
      shows the negative-cakes/cookies honesty note; presets renamed to "Two different
      recipes" / "Recipes in the same ratio (singular)".
- [ ] Every screen shows the inverse meter; app runs with `streamlit run app.py`
      and no import errors.
