# Build Spec — Topic 7: Projection & Least Squares

> **For the builder (Claude Code):** implement as a per-screen package
> `topics/t07_projection/` registered in `app.py` after `t06_spaces`. Follow
> `CLAUDE.md`. Reuse the engine (`engine/widgets.py`, `engine/plotting.py`,
> `engine/parametric.py`) and the Topic 5.5 / Topic 6 patterns. Student-facing text
> below is final copy — implement it, don't reword. Straight ASCII quotes in code.

`TITLE = "7 · Projection & Least Squares"`, `SLUG = "projection"`.

## The through-line

Topic 6 ended with: when the target b is OUTSIDE the column space, there is no exact
solution — so what is the CLOSEST we can get? Projection answers that (the closest
point is b's perpendicular shadow). Least squares is that same idea applied to
fitting data. Every screen answers "no exact answer exists, so what is the best one?"

## Design rules (same as Topic 6)

1. **Viewport blocks.** Each screen is a vertical stack of self-contained blocks;
   each fits ONE screen-height (math LEFT / graph RIGHT via `st.columns([0.5,0.5])`,
   everything for one example visible without scrolling inside the block).
2. **Plain words before symbols**, every time. Define each term in words before any
   notation. No unexplained jargon.
3. **One interaction max per screen** where it teaches; otherwise static.
4. **Tight math:** multi-line equation sets as one aligned LaTeX block.
5. Graphs at the standard ~420 height, engine dark palette, primitives.
6. Perpendicularity of the residual is the recurring VISUAL ANCHOR across the topic.

## Selector

`st.radio` horizontal, key `t07_screen`:
["0 · Perpendicular means dot product zero", "1 · Projecting onto a line",
 "2 · Projecting onto a plane", "3 · Why perpendicular is closest",
 "4 · Line of best fit", "5 · Where this lives in the real world"]

## OVERVIEW (pinned, verbatim)

> Sometimes there is no exact answer — the target sits outside everything a matrix
> can reach, and no input hits it exactly. This topic is about the next best thing:
> the CLOSEST answer. The closest point turns out to be a perpendicular shadow, and
> that one idea powers line-of-best-fit, GPS, and the computer vision in your camera.

---

## Screen 0 — Perpendicular means dot product zero (light interactive)

Keystone primer: the whole topic rests on "perpendicular exactly when the dot
product is zero." He has met the dot product but not this fact.

### Block 1 — the idea (text only, verbatim)

> You already know the **dot product**: multiply two vectors component by component
> and add. For (a1, a2) and (b1, b2) it is a1·b1 + a2·b2 — a single number.
>
> Here is the fact this whole topic is built on: **two vectors are perpendicular
> (at a right angle, 90 degrees) exactly when their dot product is zero.** Not
> close to zero — exactly zero. Turn one vector until it makes a right angle with
> the other, and the dot product lands on 0 at that precise moment.

### Block 2 — interactive: rotate a vector, watch the dot product (math left, graph right)

ONE interaction: a slider for the angle of a movable vector.
  `angle = st.slider("Angle of the blue vector (degrees)", 0, 180, 30, key="t07_angle")`
Fixed reference vector u = (3, 0) (points right). Movable vector v of length ~3 at
the chosen angle: v = (3·cos, 3·sin).

LEFT: st.latex the live dot product with current numbers, one line:
  u · v = 3·(v_x) + 0·(v_y) = <value>
and a plain-language readout beneath (verbatim template):
> Right now the angle is <A> degrees and the dot product is <D>. <VERDICT>
where VERDICT is:
- if |dot| < 0.05 (i.e. at 90 degrees): "That's a right angle — and the dot product
  is zero. Perpendicular."
- else if dot > 0: "The vectors lean the same way (less than 90 degrees apart), so
  the dot product is positive."
- else: "The vectors lean apart (more than 90 degrees), so the dot product is
  negative."

RIGHT: `new_figure_2d` (rng~4); draw u=(3,0) and v at the angle, both from the
origin; when within ~2 degrees of 90, draw a small right-angle square at the origin
and color v to match "perpendicular". Caption: "Slide to 90 degrees and watch the
dot product hit exactly zero."

### Block 3 — three quick checks (math left, no graph)

Verbatim, one aligned block each, showing dot products:
> **Perpendicular pair:** (3, 0) and (0, 2). Dot product 3·0 + 0·2 = 0. Right angle. ✓
> **Another perpendicular pair (tilted):** (2, 1) and (−1, 2). Dot product
> 2·(−1) + 1·2 = 0. Also a right angle. ✓
> **Not perpendicular:** (2, 1) and (1, 1). Dot product 2·1 + 1·1 = 3, not zero — so
> not a right angle.

### Block 4 — closing (verbatim)

> Keep this one fact in your pocket: perpendicular means dot product zero. Every
> screen from here on uses it to find the closest point.

---

## Screen 1 — Projecting onto a line (full scalar derivation)

### Block 1 — the setup (text only, verbatim)

> You have a target point b and a line through the origin (all the multiples of one
> direction vector a). The line is everything you can reach; b is usually NOT on it.
> The question: which point ON the line is CLOSEST to b?
>
> The answer is b's **shadow** on the line — drop straight down from b onto the
> line at a right angle. That closest point is called the **projection** of b onto
> the line. The little arrow from the shadow up to b is the **residual** (the
> leftover), and it is perpendicular to the line.

### Block 2 — interactive: drag the target, see its shadow (math left, graph right)

ONE interaction: move b. Two sliders (b_x, b_y) OR a preset radio of 3 target
points — use two sliders `st.slider` for b_x, b_y (range −6..6, defaults b=(2,5)).
Fixed line direction a = (3, 1).

LEFT: st.latex the projection point p and the residual, live:
  p = <scalar>·a = (<px>, <py>)   (the shadow)
  r = b − p = (<rx>, <ry>)         (the leftover, perpendicular to the line)
and a caption confirming r · a = 0 (compute and show it is ~0).

RIGHT: `new_figure_2d` (rng~7); the line along (3,1) long both ways; b marked; the
projection point p on the line marked "shadow (closest point)"; the perpendicular
dropline from b to p drawn (dashed); a small right-angle mark where it meets the
line. Caption: "The shadow is the closest point; the dashed drop is perpendicular."

### Block 3 — derive the projection formula (math left, no graph)

Full derivation, verbatim, plain words then symbols, as aligned blocks:
> **Step 1 — the shadow is some amount of a.** The closest point sits on the line,
> so it is a scalar multiple of the direction: p = c·a, for some number c we must
> find.
>
> **Step 2 — the leftover is perpendicular to the line.** The residual r = b − p
> must be perpendicular to a. From Screen 0, perpendicular means the dot product is
> zero: a · (b − p) = 0.
>
> **Step 3 — substitute p = c·a and solve for c.** a · (b − c·a) = 0, so
> a·b − c(a·a) = 0, which gives **c = (a·b) / (a·a)**.
>
> **Step 4 — the projection.** p = c·a = ((a·b)/(a·a)) · a.

Then plug in the live a and b to show c and p numerically (one aligned block).

### Block 4 — closing (verbatim)

> That single number c measures how much of b points along the line. The projection
> is the closest reachable point, found purely by the perpendicular rule. Next: the
> same idea when the line becomes a whole plane.

---

## Screen 2 — Projecting onto a plane (column space), 3D

### Block 1 — the idea (text only, verbatim)

> Same story, one dimension up. Now the thing you can reach is a whole PLANE through
> the origin — and from Topic 6 you know a plane like this is a **column space**
> (all the combinations of a matrix's columns). The target b floats in 3D, usually
> off the plane. The closest point is again b's perpendicular shadow, dropped
> straight down onto the plane.
>
> When b is off the plane, there is no exact solution to A·x = b — but the shadow is
> the closest we can get. That shadow is what "best answer" will mean.

### Block 2 — the picture (math left, 3D graph right)

Use the plane spanned by a1 = (1, 0, 1) and a2 = (0, 1, 1) (a column space), and a
target b = (1, 2, 4) off the plane. (VERIFY in build: compute the projection of b
onto the plane and the residual; confirm residual is perpendicular to BOTH a1 and
a2, i.e. residual · a1 = 0 and residual · a2 = 0.)

LEFT: st.markdown the setup; st.latex the two spanning vectors, the target b, the
projection p (the shadow on the plane), and the residual r = b − p, with a caption
confirming r · a1 = 0 and r · a2 = 0 (perpendicular to the whole plane).

RIGHT: `new_figure_3d` (rng~5); the plane (translucent) via `add_plane_3d`; the two
spanning arrows in the plane; b marked above the plane; the projection p on the
plane; the perpendicular dropline b→p (dashed). Caption: "The shadow on the plane is
the closest point; the drop is perpendicular to the whole plane. Rotate to see it."

### Block 3 — closing (verbatim)

> Perpendicular to the whole plane means perpendicular to every direction in it — to
> each column. Turning that sentence into equations is the next screen, and it gives
> the formula that runs everything.

---

## Screen 3 — Why perpendicular = closest: the normal equations (full derivation)

### Block 1 — the goal (text only, verbatim)

> We want the best x — call it x-hat — so that A·x-hat is as close to b as possible.
> "Closest" means the leftover r = b − A·x-hat is perpendicular to everything the
> matrix can reach (the whole column space). We will turn that single sentence into
> an equation you can solve.

### Block 2 — the full derivation (math left, no graph)

Verbatim, plain words before each symbolic line, as aligned blocks. (VERIFY each
algebra step in build.)
> **Step 1 — name the leftover.** After picking x-hat, the leftover is
> r = b − A·x-hat.
>
> **Step 2 — perpendicular to every column.** Closest means r is perpendicular to
> each column of A. Perpendicular means dot product zero (Screen 0), so each column
> of A dotted with r is zero.
>
> **Step 3 — stack those dot products.** Dotting every column of A with r at once is
> exactly A-transpose times r. So all those "= 0" conditions become one equation:
> Aᵀ r = 0.
>
> **Step 4 — substitute the leftover.** Aᵀ(b − A·x-hat) = 0.
>
> **Step 5 — expand.** Aᵀb − AᵀA·x-hat = 0, which rearranges to the **normal
> equations**: AᵀA·x-hat = Aᵀb.
>
> **Step 6 — solve.** When AᵀA can be inverted, x-hat = (AᵀA)⁻¹ Aᵀb. That x-hat is
> the best answer — the one whose leftover is perpendicular to everything reachable.

### Block 3 — why it's called "normal" + when AᵀA is invertible (text only, verbatim)

> "Normal" is the old word for perpendicular — the normal equations are the
> perpendicular equations. AᵀA can be inverted as long as the columns of A are
> independent (no column is a combination of the others) — the same
> independence idea from Topic 6. When that holds, there is exactly one best answer.

### Block 4 — closing (verbatim)

> One formula, AᵀA·x-hat = Aᵀb, finds the closest answer for ANY over-crowded
> system. The next screen turns it loose on real, messy data.

---

## Screen 4 — Line of best fit (least squares), temperature vs. time

### Block 1 — the setup (text only, verbatim)

> Here is real data: a cold drink warming up on the counter, its temperature
> measured every 2 minutes. The points do NOT sit on any straight line — real
> measurements never do. We want the line that misses them by the least total
> amount. That is the **line of best fit**, and it is exactly a projection: no line
> hits every point (the target is outside the column space), so we find the closest
> line instead.

### Block 2 — the data and the fit (math left, graph right)

Data (VERIFIED): times t = [0, 2, 4, 6, 8, 10] minutes; temps = [6, 8, 13, 17, 20,
26] degrees. Best-fit line: **temp = 5 + 2·t** (intercept 5, slope 2, exactly).
Residuals: [+1, −1, 0, 0, −1, +1].

LEFT: st.markdown the setup; a small table or aligned list of the six (time, temp)
points; then st.latex the fitted line "temp = 5 + 2·t" and a caption: "Every 2
minutes the drink warms about 4 degrees (2 degrees per minute); it started near 5."

RIGHT: `new_figure_2d` (rng: x 0..11, y 0..28); the six data points as markers; the
best-fit line temp = 5 + 2t drawn across; each residual as a short vertical dashed
segment from a data point to the line. Caption: "The line of best fit; dashed drops
are the leftovers (residuals) it could not avoid."

### Block 3 — how the fit is computed (math left, no graph)

Verbatim, connect to Screen 3, then the worked normal equations (VERIFY in build):
> This is the normal equations at work. Set up A with two columns — a column of
> 1s (for the starting temperature) and the column of times (for the rate) — and let
> b be the measured temperatures. Then solve AᵀA·x-hat = Aᵀb for x-hat = (start,
> rate).

Show (aligned blocks, real numbers):
  AᵀA = [[6, 30], [30, 220]] ,  Aᵀb = [90, 590]   (wait: VERIFY b column — use the
  VERIFIED temps [6,8,13,17,20,26]; recompute Aᵀb in build and use the true values,
  do NOT copy these placeholders)
  solving gives x-hat = [5, 2]  ->  temp = 5 + 2·t
Caption: "The same AᵀA·x-hat = Aᵀb from the last screen, on real numbers — and the
best fit comes out to clean values."

> NOTE TO BUILDER: compute AᵀA and Aᵀb from the VERIFIED data in code and display the
> true values; the intercept/slope are exactly 5 and 2 (verified), but recompute
> Aᵀb rather than trusting the numbers in this line.

### Block 4 — use it to predict (math left, graph right optional)

Verbatim:
> Once you have the line, you can PREDICT. At t = 12 minutes the line says
> temp = 5 + 2·12 = 29 degrees — a reasonable guess even though we never measured
> there. That is the real power of a best-fit line: filling in what you didn't
> measure.

### Block 5 — closing (verbatim)

> No line hit every point, so we found the closest line — a projection onto what a
> line can reach. Last screen: the places this exact math runs in the real world.

---

## Screen 5 — Where this lives in the real world (text + light visuals)

### Block 1 — GPS (math left / small graph or icon right)

Verbatim:
> **GPS.** Your phone hears from several satellites, each giving a distance. Three
> would be enough for a perfect fix — but your phone usually hears from many more,
> and the numbers never agree exactly (signals bounce, clocks drift). That is an
> over-crowded system with no exact solution — exactly the case this topic solves.
> GPS uses least squares to find the position closest to satisfying ALL the
> measurements at once. The little leftover in each signal is a residual, made as
> small as possible.

### Block 2 — cameras and computer vision (verbatim)

> **Cameras and computer vision.** When your phone stitches a panorama or tracks a
> face, it matches hundreds of points between images. The points are noisy and never
> line up perfectly, so the software fits the best transformation by least squares —
> the same AᵀA·x-hat = Aᵀb — minimizing the total leftover. Best-fit, not exact,
> because exact is impossible with real measurements.

### Block 3 — the big picture (verbatim)

> The pattern is always the same: more measurements than unknowns, no exact answer,
> so find the one that comes closest — the perpendicular shadow, the projection, the
> least-squares fit. From a drink warming on a counter to a phone finding itself on
> Earth, "closest when you can't be exact" is one of the most useful ideas in all of
> mathematics.

### Block 4 — closing bridge (verbatim)

> You have now turned "no solution" into "best solution." Next comes a different
> question about a matrix: are there special directions it only stretches, never
> turns? Those are eigenvectors — the heart of the next topic.

---

## Reuse / new

- REUSE: `new_figure_2d`, `add_vector_2d`, `add_point_2d`, `add_line_2d`,
  `shade_polygon`, `new_figure_3d`, `add_plane_3d`, `_arrow3d` (engine/plotting.py);
  aligned-block LaTeX; read-only compact matrices where a matrix is shown.
- NEW: package `topics/t07_projection/` — `__init__.py` (TITLE, SLUG, OVERVIEW,
  selector, dispatch) + `screen_perp.py`, `screen_line.py`, `screen_plane.py`,
  `screen_normal.py`, `screen_fit.py`, `screen_world.py`.
- NO new engine code expected (dot-product / projection math is inline numpy).

## Acceptance checklist

- [ ] Registered in app.py after Topic 6; selector shows 6 screens (0–5).
- [ ] Screen 0: angle slider; dot product shown live; hits exactly 0 at 90 degrees;
      right-angle mark appears at perpendicular; three static checks correct.
- [ ] Screen 1: target movable; projection point + perpendicular dropline drawn;
      residual·a shown ~0; full 4-step scalar derivation c = (a·b)/(a·a).
- [ ] Screen 2: 3D plane (column space) + target off it + perpendicular shadow;
      residual perpendicular to BOTH spanning vectors (verified in build).
- [ ] Screen 3: full 6-step normal-equations derivation to AᵀA·x-hat = Aᵀb and
      x-hat = (AᵀA)⁻¹Aᵀb; "normal = perpendicular" + independence note.
- [ ] Screen 4: data t=[0,2,4,6,8,10], temp=[6,8,13,17,20,26]; best fit temp = 5+2t
      (VERIFIED); residuals [+1,−1,0,0,−1,+1] drawn as vertical drops; AᵀA and Aᵀb
      recomputed in code from the data; prediction at t=12 gives 29.
- [ ] Screen 5: GPS + cameras + big-picture, all verbatim; Topic 8 eigenvector bridge.
- [ ] Plain words precede every symbol; residual-perpendicularity is the visual
      anchor throughout; all numbers match VERIFIED values.
