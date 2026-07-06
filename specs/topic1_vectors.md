# Build Spec — Topic 1: Vectors & Combinations

**For the builder (Claude Code):** Topic 1 **already exists** as
`topics/t01_vectors.py`. This spec is **retroactive** — it documents the topic as
built AND specifies two content additions (an Ax = b gesture in the intro, and an
explicit ingredients→A / scoops→x / target→b mapping at the end of Example 3). It
does **not** cover the layout refactor — that's a separate pass after this spec is
reviewed. Follow `CLAUDE.md`.

`TITLE = "1 · Vectors & Combinations"`, `SLUG = "vectors"`. Pattern:
**multi-example** — a top selector chooses Example 1/2/3; only the chosen example's
text, inputs, and visual render.

## The spine (unchanged)

One concrete metaphor runs through all three examples: **each ingredient is a
vector of two numbers — (protein, sugar) per scoop — and a smoothie is a mix.**
Combining vectors (scaling and adding) is the one move almost all of linear algebra
is built on. The three examples build, in order: **scale → add → combine freely**,
landing on the three words **linear combination**, **span**, and **basis**.

Vector naming stays **u, v, v₁, v₂** for ingredients and **c₁, c₂** for scoop
amounts (coefficients). This is fine — these are *ingredients* and *amounts*, a
different role from the "input vector x" of later topics.

## Intro (existing OVERVIEW + a light Ax = b gesture)

Keep the existing OVERVIEW (the "you already know a vector is an arrow… combining
vectors… smoothies" text). **Add one light forward-gesture sentence near the end**
of the intro — plant the Ax = b seed without introducing matrix machinery yet
(the student hasn't seen a matrix; that's Topic 2):

> The question we keep circling — *which combinations of your vectors can reach a
> given target?* — is the central one of the whole course. You'll meet it soon
> written as **Ax = b**. For now, just build the intuition with smoothies.

Keep HOWTO as-is (it'll be folded into the description during the later layout
refactor, not now).

## Example 1 — One ingredient (scaling)

Banana = (1, 4). A slider sets the number of scoops; the arrow grows/shrinks along
its direction. Teaches: **scaling stretches a vector without turning it**, and even
a single vector is a combination of the axis directions (the seed of "basis").

- Presets `_E1_PRESETS`: "More scoops" (×3), "Half a scoop" (×0.5), "Read the
  recipe" (×1 with breakdown on) — each with its notice. Keep.
- "Show the recipe breakdown" checkbox → draws the protein part and sugar part as
  dashed components. Keep.
- Show-the-math: `c · banana = result` (scaling multiplies every component).

## Example 2 — Two ingredients, added (vector addition)

Banana + peanut butter (4, 1). One scoop of each. Teaches: **the sum is where you
land after following one arrow then the other** (tip-to-tail), shown two ways.

- Presets `_E2_PRESETS`: "Tip-to-tail", "Same direction", "Opposite directions" —
  each with notice. Keep.
- View radio: Tip-to-tail / Parallelogram. Keep both renderings.
- Editable vectors u, v. Show-the-math: `u + v = sum` (add component by component).

## Example 3 — The smoothie mixer (combination, span, basis)

The keystone. Two sliders: **c₁ scoops of banana + c₂ scoops of peanut butter** —
the moving point is the **linear combination** c₁v₁ + c₂v₂. Teaches **linear
combination, span, basis** and the independence test.

- Presets `_E3_PRESETS`: "Two good ingredients" (a basis ✓), "Standard axes",
  "Proportional ingredients" (not a basis ✗) — each with notice. Keep.
- The `DEFINITION` block ("What's a basis?") — keep.
- Editable v₁, v₂; "Allow negative scoops" checkbox (extends sliders negative);
  two scoop sliders c₁, c₂; "Show span" checkbox. Keep.
- Visual: the skewed-grid overlay, span shading (whole plane / a line / reachable
  region depending on independence and negatives), the two ingredient vectors, the
  target (10,10) star, and the moving "your smoothie" point. Keep.
- Readouts: recipe line, smoothie/target/distance, basis ✓ / not-a-basis ✗,
  "hit the target" success. Keep.
- Show-the-math: `c₁v₁ + c₂v₂ = result`, plus `det[v₁ v₂]` with the
  independent/dependent interpretation (one / none / infinitely many solutions).
- "Challenge — Make the target smoothie" and "Reality check" (negative scoops) —
  keep.

### NEW — explicit Ax = b mapping (closing payoff of Example 3)

After the student has hit the target and seen span/basis, add an explicit mapping
that ties the metaphor to the algebra — this is the upgrade of the existing
"formalize later when solving Ax = b" gesture into the real correspondence. Place
it at the end of Example 3 (e.g. in the Challenge area or just below the math):

> **A preview of the whole course:** stack your two ingredients as the **columns of
> a matrix A**, call your scoops **x = (c₁, c₂)**, and call the target **b**. Then
> "what scoops reach the target?" is exactly **A x = b** — the equation the rest of
> the course turns on. And a **basis** (two independent ingredients) is precisely
> the case where that equation has **exactly one** answer; proportional ingredients
> (not a basis) give either no answer or infinitely many.

This explains *why* basis/independence matters — it's the one-solution condition —
using the intuition the student just built with the sliders.

## Acceptance checklist (content only; layout refactor is separate)
- [ ] Intro has the light Ax = b gesture sentence (no matrix machinery introduced).
- [ ] All three examples work as before (scaling, addition tip-to-tail/parallelogram,
      the mixer with span/basis/target).
- [ ] Example 3 closes with the explicit ingredients→A / scoops→x / target→b mapping,
      connecting basis to the "exactly one solution" case.
- [ ] Vector naming stays u, v, v₁, v₂, c₁, c₂.
- [ ] All presets, the challenge, and the reality-check are intact.
