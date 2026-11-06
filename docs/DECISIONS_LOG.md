# Decisions Log

Every important choice and assumption, with the reason. Interviewers often ask "why did you choose X?". The answers live here.

| # | Date | Decision | Why | Alternatives considered |
|---|------|----------|-----|------------------------|
| 1 | 2026-11-05 | Use the Intel microprocessor dataset (Manary & Willems 2022) as the SKU-level data | It is real semiconductor demand, and it contains the company's own forecast next to actual orders. That lets us measure forecast accuracy, bias and Forecast Value Add the way a planning team would. | UCI Online Retail (not semiconductor), M5 Walmart (retail), a fully synthetic dataset (not real) |
| 2 | 2026-11-05 | Add FRED / Census M3 market signals | Semiconductor planners watch end-market indicators; these are free and official | WSTS/SIA data (press-release only, harder to automate) |
| 3 | 2026-11-05 | Primary accuracy metric = WMAPE (accuracy = 1 − WMAPE) | It weights errors by volume and does not blow up on low or zero weeks like MAPE does; it is the common industry KPI | MAPE, RMSE, MASE (reported as secondary) |
| 4 | 2026-11-05 | Test bias significance (HAC t-test + Wilcoxon), not just bias size | It separates systematic bias that needs action from random noise that is tolerable | Tracking signal only |
| 5 | 2026-11-05 | Do not reuse the old resume numbers | They came from a different dataset; only measured results get reported | — |
