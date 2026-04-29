# Managing Carbon Footprints in Inventory Control — Replication

A code replication of:

> Hua, G., Cheng, T.C.E., & Wang, S. (2010). *Managing Carbon Footprints in Inventory Control.* SSRN: <https://ssrn.com/abstract=1628953>

The paper extends the classical EOQ model with a carbon cap-and-trade mechanism, derives the optimal order quantity $Q^*$ in closed form, and proves five theorems on how carbon trade, carbon price, and carbon cap affect order decisions, emissions, and total cost. This repo reproduces every numerical result, figure, and theorem in the paper.

## Project structure

| File | Purpose |
|---|---|
| [`model.py`](model.py) | Pure-function implementation of equations (5)–(7) and the auxiliary quantities $\hat Q$, $\alpha_0$, $X$, $\Delta CO_2$, $\Delta TC$. |
| [`01_table1.ipynb`](01_table1.ipynb) | Reproduces the seven numerical examples in Table 1 (page 16) and verifies every cell against the paper's printed values. |
| [`02_figures.ipynb`](02_figures.ipynb) | Reproduces Figures 2–6 — the carbon-cap sweep (Theorem 4) and the four carbon-price sweeps illustrating Theorem 5(4)'s trichotomy. |
| [`03_theorems.ipynb`](03_theorems.ipynb) | Numerical and symbolic (`sympy`) verification of every clause of Theorems 1–5. |
| [`requirements.txt`](requirements.txt) | Python dependencies. |

## Setup

```bash
pip install -r requirements.txt
```

Dependencies: `numpy`, `pandas`, `matplotlib`, `jupyter` (and `sympy` for the symbolic cross-check, which is bundled with most scientific Python distributions).

## Usage

Open the notebooks in order in VS Code (Jupyter extension) or JupyterLab:

```bash
jupyter notebook
```

Each notebook is self-contained — outputs are pre-executed and embedded, so reviewing the replication doesn't require running anything. To re-execute from scratch:

```bash
jupyter nbconvert --to notebook --execute --inplace 01_table1.ipynb
jupyter nbconvert --to notebook --execute --inplace 02_figures.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_theorems.ipynb
```

## Findings

### 1. Table 1 — exact numerical match

**53 / 56 numeric cells match the paper within ±1** (the paper rounds to integers). The three out-of-tolerance cells are all in Row 1's $Q$ columns and are a typo in the paper, not a model error (see below).

### 2. Figures 2–6 — qualitative shape match

All five figures reproduce the predicted shapes:

| Fig | Sweep | Predicted | Observed |
|---|---|---|---|
| 2 | $\alpha$ | $TC$ linear-decreasing, $CF$ flat | ✓ |
| 3 | $C$, $g/e<h/K$, mid $\alpha$ | $TC$ unimodal, $CF$ ↓ | ✓ peak near $C \approx 0.2$ |
| 4 | $C$, $g/e<h/K$, large $\alpha$ | $TC$ ↓, $CF$ ↓ | ✓ |
| 5 | $C$, $g/e>h/K$, mid $\alpha$ | $TC$ unimodal, $CF$ ↓ | ✓ peak near $C \approx 0.2$ |
| 6 | $C$, $g/e>h/K$, small $\alpha$ | $TC$ ↑, $CF$ ↓ | ✓ |

Y-axis magnitudes differ slightly because the paper does not print the exact $(K,h,e,g,\alpha)$ used for Figs 3–6; this repo picks parameters that satisfy each figure's regime condition (printed in the figure title). The shape — which is what each figure exists to demonstrate — matches.

### 3. Theorems 1–5 — every clause verified

| Theorem | Method | Verdict |
|---|---|---|
| 1 (1)(2)(3) | parameter set per regime, ordering assertion | ✓ |
| 2(1) | 2000 random draws; equality at $g/e=h/K$ | ✓ |
| 2(2) | trichotomy across the three $\alpha$ bands incl. exact zero at $C = C^*$ | ✓ |
| 2(3) corrected | 2000 random draws | ✓ |
| 3 | tested at all 7 Table 1 parameter sets | ✓ |
| 4 | gridded sweep + slope fit (slopes 1 and $-C$ recovered exactly) | ✓ |
| 5 (1)(2)(3) | sign of $dQ^*/dC$, $dCF/dC$, $dX/dC$ by regime | ✓ |
| 5(4) | 400-point grid, sign-change count | ✓ |
| Sympy cross-check | symbolic derivation of $dQ^*/dC$ and $dCF/dC$ | ✓ (with one caveat below) |

### Three paper inaccuracies detected

1. **Table 1 Row 1** prints $\hat Q = Q^* = Q^0 = 8453$, but the formula gives $\sqrt{2 \cdot 180 \cdot 60{,}000 / 0.3} = 8485.28$. The same row's $\alpha_0 = 8485$ matches the formula, and the row's other derived quantities ($X = -485$, $TC = 2643$, $\Delta TC = 97$) are all consistent with $Q = 8485$, not $8453$. **Typo in Table 1.**

2. **Theorem 2(3)** statement reads "*when the transfer quantity $X > 0$, $TC(Q^*) > TC_0$*," but the proof on page 10 derives $TC(Q^*) > KD/Q^* + hQ^*/2$ from $-CX(Q^*) > 0$, which requires $X < 0$. The discussion immediately below the theorem ("when the retailer **buys** carbon credit, his total cost is bound to rise") confirms the intended sign. The notebook tests both the corrected statement ($X < 0 \Rightarrow \Delta TC > 0$, holds with zero violations in 2000 random draws) and the printed version ($X > 0 \Rightarrow \Delta TC > 0$, fails on a substantial fraction of "sell" cases).

3. **Proof of Theorem 5** (page 14) writes
   $$\frac{d\,CF(Q^*)}{dC} = \frac{g(Q^{*2} - \hat Q^2)}{2Q^{*2}}.$$
   The expression on the right is $\frac{\partial CF}{\partial Q}\big|_{Q=Q^*}$, not $\frac{d\,CF(Q^*)}{dC}$ — the chain-rule factor $dQ^*/dC$ is missing. The downstream conclusion (CF decreasing in C when $g/e \ne h/K$) is still correct because the missing factor cancels signs across the two $g/e$ regimes, but the formula as printed is dimensionally inconsistent with $dCF/dC$.

These findings are flagged inline in [`01_table1.ipynb`](01_table1.ipynb) and [`03_theorems.ipynb`](03_theorems.ipynb).

## Reference

Hua, G., Cheng, T.C.E., & Wang, S. (2010). *Managing Carbon Footprints in Inventory Control.* SSRN Electronic Journal. <https://ssrn.com/abstract=1628953>
