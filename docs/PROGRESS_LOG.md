# Progress Log

Newest entry at the top. Updated at the end of every working session (via `/checkpoint`).

---

## 2026-11-08 — Day 0: Readiness layer COMPLETE ✅
**Done**
- Owner: Power BI Desktop installed (opens the sample CSV), Streamlit Community Cloud linked to GitHub.
- Owner: bootcamp notebook worked through (all 5 exercises attempted), both primers read.
- `/checkpoint Day 0`: `check_env.py` 34/34 PASS; bootcamp notebook re-executed with 0 errors.

**Key results**
- Concepts quiz: **13.5 / 15** (pass ≥ 12). Bootcamp checkpoint: **3 / 3**.
- Gaps reviewed (see `LEARNING_GUIDE.md`): acting on bias significance (Q7), the AZ-segment implication (Q13), FVA = difference in *accuracy* and overrides can hurt (Q14).

**Next: Day 1, data understanding & EDA**
- Find out what `Forecasted Demand` measures (horizon / lag, single-week vs. cumulative, units) before scoring anything.
- Life-cycle curves by generation, intermittency, DC differences, order-spike patterns.
- Decide how (or whether) to align FRED monthly series with the relative Intel weeks.

---

## 2026-11-06 — Day 0: Readiness layer (Claude's part done; owner tasks pending)
**Done**
- Public repo created: https://github.com/dheerajkusuma17/semiconductor-demand-planning
- Python 3.11 `.venv` with all libraries. Exact versions frozen in `requirements-lock.txt`.
- `scripts/check_env.py`: **34/34 checks pass**. Covers pandas, statsmodels ARIMA/ETS, statsforecast AutoETS/Croston/TSB, bias tests (t-test, Wilcoxon, HAC), Ridge/RF/MLP, LightGBM/XGBoost, PyTorch 2.15 CPU, neuralforecast N-HiTS/LSTM, safety-stock math, Excel export, charts, and the Jupyter kernel.
- Jupyter kernel "Semiconductor DP (.venv)" registered. VS Code extensions installed: Rainbow CSV, GitLens, Data Wrangler (Python, Pylance and Jupyter were already installed).
- Data downloaded and validated with `scripts/download_data.py`:
  - Intel MSOM: 26,114 rows, 86 SKUs, 5 DCs (ALPHA, BETA, DELTA, EPSILON, GAMMA), weeks 1–187, 5 generations, 394 SKU-DC combinations (66 weeks each on average)
  - FRED A34SNO, A34SVS, IPG3344S through Sep 2026
- Docs: `INDUSTRY_PRIMER.md` (fact-checked, 22 sources), `CONCEPTS_PRIMER.md` + quiz, `LEARNING_GUIDE.md`, `DECISIONS_LOG.md`, `READINESS_CHECKLIST.md`, `/checkpoint` skill.
- `notebooks/00_prerequisites_bootcamp.ipynb` executes top to bottom.

**Owner to-do before Day 1**
1. Install Power BI Desktop (Microsoft Store) and open `data/sample/powerbi_test.csv`.
2. Sign in to Streamlit Community Cloud with GitHub (share.streamlit.io).
3. Work through the bootcamp notebook and its 5 exercises.
4. Read `INDUSTRY_PRIMER.md` + `CONCEPTS_PRIMER.md`; take the 15-question quiz (target ≥ 12/15).

**Open questions (for Day 1)**
- A crude first pass gives Intel forecast vs. orders **bias ≈ +217%, WMAPE ≈ 239%**. That's far too large to be a normal weekly forecast error. Before scoring anything on Day 2, find out what `Forecasted Demand` represents: horizon / lag, single week or cumulative, units. Check the dataset paper's description.
- The Intel weeks are relative (1–187), with no calendar dates. Aligning to the monthly FRED series needs the real calendar period. If the paper doesn't give it, FRED is used as market context only, not as model features.
- SKU-A-2 at ALPHA has only 89 of 187 weeks. Life cycles are short, so many series are short. This affects model choice: global ML models and life-cycle features.

---

## 2026-11-05 — Day 0 started
- Plan approved: semiconductor data (Intel MSOM dataset + FRED), Streamlit + Power BI showcase, build + explain style.
