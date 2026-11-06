# CLAUDE.md — Semiconductor Demand Planning project

Read this first in every session, then `docs/PROGRESS_LOG.md` for where we left off.

## Goal
Portfolio project for a future **demand planner who works beyond Excel**. Rebuilds a lost resume project
("Demand Forecasting & Inventory Optimization using ML") with **semiconductor** data:
- Intel microprocessor dataset (Manary & Willems 2022, MSOM): 86 SKUs, 5 DCs, 187 weeks, Intel forecast vs. actual orders.
- FRED / US Census M3 market signals (Computers & Electronic Products orders/shipments, semiconductor industrial production).
- Fallback only if the Intel file is unobtainable: clearly labelled synthetic distributor data driven by FRED signals.

Showcase: public GitHub repo `dheerajkusuma17/semiconductor-demand-planning`, Streamlit app, Power BI dashboard.

## Working style (the owner chose "build + explain")
- Claude writes the code quickly; the owner runs it, reads it, answers checkpoint questions.
- Every notebook: opens with **the business question**, explains each step in plain English with **Excel equivalents**
  (groupby = PivotTable, merge = XLOOKUP, rolling = moving-average column), ends with
  **"What a demand planner takes away"** and 3–5 checkpoint questions.
- Explain concepts simply before going deeper. Prefer breadth + rigor: many models (stats, ML, neural), bias *and* bias significance.

## Hard rules
- **Never invent or reuse resume numbers.** The old figures (71% accuracy, $8.9M, 15% holding cost) came from a different
  dataset. Only report numbers the notebooks actually produce.
- **No data leakage:** every forecast is evaluated with a rolling-origin backtest using only data available at the cut-off.
- Every assumption (lead time, holding-cost %, service levels) goes in `docs/DECISIONS_LOG.md` with the reason.
- **Never lose work:** end each phase with `/checkpoint` (run notebooks → quiz → log → commit → push).
- Confirm with the owner before anything public (repo visibility changes, deploys, posts).

## Conventions
- Python 3.11 in `.venv` (activate in PowerShell: `.\.venv\Scripts\Activate.ps1`). Jupyter kernel: "Semiconductor DP (.venv)".
- Reusable logic lives in `src/` (data, features, models, metrics, inventory); notebooks import from it.
- Notebooks are numbered (`00_`…`06_`) and must pass "Restart & Run All".
- Random seeds fixed (42) for reproducibility.
- Primary accuracy metric: WMAPE (accuracy = 1 − WMAPE). Bias: bias %, tracking signal (±4), HAC t-test + Wilcoxon.
- Commit messages: imperative, e.g. "Add bias significance tests".

## Key commands
```powershell
.\.venv\Scripts\Activate.ps1
python scripts/check_env.py            # verify environment
jupyter nbconvert --to notebook --execute --inplace notebooks/<nb>.ipynb
streamlit run app/streamlit_app.py
pytest
```

## Phase status
See `docs/PROGRESS_LOG.md`. Full plan: Day 0 readiness → Day 1 data/EDA → Day 2 Intel forecast accuracy & bias →
Day 3 stats models → Day 4 ML/neural + comparison/FVA → Day 5 inventory optimization → Day 6 Streamlit →
Day 7 Power BI → Day 8 packaging (README, resume bullets, v1.0 tag).
