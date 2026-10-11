"""Screen 4 -- The rules, and what's next (static reference text)."""
import streamlit as st

_INTRO = """
Here is the whole topic on one screen. `m` is the number of **rows** (equations),
`n` the number of **columns** (unknowns), and `r` the **rank** — the number of
genuinely independent rows, the pivots you find by elimination. Every rule about
inverses, solvability, and the four spaces is really a statement about how `m`,
`n`, and `r` compare.
"""

# Markdown tables (NOT st.table -- it crashes on this repo's pandas/NumPy versions).
_TOOLS_TABLE = """
| Tool | Shape rule | Extra condition | What you get |
|---|---|---|---|
| **A⁻¹** (inverse) | square only — m = n | det ≠ 0 (same as r = n) | undoes A: x = A⁻¹b, exactly one answer |
| **Aᵀ** (transpose) | any shape — m×n becomes n×m | none | always exists; AᵀA is square & symmetric |
| **AᵀA** | always square (n×n) | — | the square system projection will solve |
"""

_COUNTS_TABLE = """
| Rank situation | Shape of A | How many solutions to Ax = b | Why |
|---|---|---|---|
| **r = m = n** | square, full rank | **exactly one**, for every b | invertible, det ≠ 0 |
| **r = n < m** | tall, full column rank | **0 or 1** | null space = {0}; solvable only if b is in the column space |
| **r = m < n** | wide, full row rank | **infinitely many**, for every b | always solvable; free variables = n − r > 0 |
| **r < m and r < n** | rank-deficient | **0 or infinitely many** | 0 if b is unreachable, otherwise free variables remain |
"""

_FOOTER = """
- Free variables = null-space dimension = **n − r**.
- Left-null-space dimension = **m − r**.
- A is invertible **exactly when m = n = r** — square and full rank, which is the
  same as det ≠ 0.
"""

_BRIDGE = """
Look at the rows that say **"0 or 1"** and **"0 or ..."** — the cases where
`Ax = b` can have **no solution at all**. That happens whenever the target `b`
sits outside the column space: no combination of A's columns can reach it, so no
exact answer exists. That's not a dead end — it's the whole next topic. When we
can't hit `b` exactly, we find the point in the column space that comes
**closest**, using a perpendicular shadow. That's projection, and the Aᵀ you just
learned is the tool that builds it.
"""


def render_rules():
    # --- Block 1 -- m, n, r --------------------------------------------------
    st.markdown(_INTRO)

    st.divider()

    # --- Block 2 -- Tool rules table -----------------------------------------
    st.markdown(_TOOLS_TABLE)

    st.divider()

    # --- Block 3 -- Solution-count table + footer facts ----------------------
    st.markdown(_COUNTS_TABLE)
    st.markdown(_FOOTER)

    st.divider()

    # --- Block 4 -- Bridge to projection -------------------------------------
    st.info(_BRIDGE)
