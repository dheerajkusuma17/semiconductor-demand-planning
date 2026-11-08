# Learning Guide & Interview Prep

This is your personal study document. It grows with every `/checkpoint`: each phase adds its checkpoint questions, your answers, model answers, and interview-style follow-ups.

## How to use it before an interview
1. Read each phase's model answers out loud. Can you explain each one in under a minute, without notes?
2. Practise the "Interview follow-up" questions with a friend, or ask Claude to role-play the interviewer.
3. For each number on your resume, know **where it came from** (which notebook, which metric, which data).

## Excel → Python cheat sheet
| You know this in Excel | In pandas (Python) |
|---|---|
| Open a file | `pd.read_csv("file.csv")` / `pd.read_excel("file.xlsx")` |
| AutoFilter | `df[df["SKU"] == "SKU-A-2"]` |
| Sort | `df.sort_values("Week")` |
| New column with a formula | `df["Error"] = df["Forecast"] - df["Actual"]` |
| PivotTable | `df.pivot_table(index="SKU", columns="DC", values="Orders", aggfunc="sum")` |
| SUMIFS / group subtotal | `df.groupby("SKU")["Orders"].sum()` |
| XLOOKUP / VLOOKUP | `df.merge(lookup_df, on="SKU", how="left")` |
| Moving-average column | `df["Orders"].rolling(4).mean()` |
| Previous row's value | `df["Orders"].shift(1)` |
| `NORM.S.INV(0.95)` | `scipy.stats.norm.ppf(0.95)` |
| `IFERROR` | `df["x"].fillna(0)` |
| Line chart | `df.plot(x="Week", y="Orders")` |

---

<!-- Phase entries are appended below by /checkpoint -->

## Day 0: Concepts quiz (2026-11-08), score 13.5 / 15 ✅

Questions are in `docs/CONCEPTS_PRIMER.md` §7. Only the answers that needed refinement are expanded here. Everything else was fully correct (Q1, 3, 4, 8–11, 15).

**Q2: Why not MAPE for intermittent demand?**
- *Your answer:* MAPE explodes on small and zero periods, inflating the error.
- *Model answer:* With actual = 0, MAPE is **undefined** (division by zero). Tiny actuals make the percentage explode. The error looks inflated, so accuracy looks *worse*. Use WMAPE or MAE.
- *Interview follow-up:* "Which metric would you report to leadership for a portfolio with many slow movers, and why?"

**Q5: Data leakage**
- *Your answer:* Letting the model see the future, e.g. fitting on the full history and reporting that (over-fitted) accuracy.
- *Model answer:* Correct. Other classic examples: a rolling mean that includes the current week, scaling with the full-dataset mean, or a random shuffle split on time-series data.
- *Interview follow-up:* "How did you make sure your backtest had no leakage?"

**Q6: Why a rolling-origin backtest?**
- *Your answer:* It tests on multiple train/test folds, so results are more defensible.
- *Model answer:* Plus: a single split can be lucky or unlucky, and rolling origins **mimic real weekly/monthly re-forecasting**.

**Q7: Bias +3% (p = 0.40) vs. +12% (p = 0.001)**
- *Your answer:* (a) p > 0.05 → reliable; (b) p < 0.05 → reject H0.
- *Model answer:*
  - (a) "Not significant" ≠ "proven unbiased". There is **no evidence of systematic bias**, so treat it as noise and **don't over-correct**.
  - (b) Significant **and** large, so **act**: investigate the cause (e.g. optimistic sales input, a missed end-of-life decline), apply a bias-correction factor, or retrain.
  - Always judge **significance and size together**.
- *Interview follow-up:* "A forecast has +1% bias with p = 0.001 on 5 years of data. Do you act?" (Probably not: significant but tiny. Monitor with the tracking signal.)

**Q12: CSL vs. fill rate**
- *Model answer:*
  - CSL = % of replenishment cycles with **no** stockout. Any stockout fails the whole cycle.
  - Fill rate = % of **units** shipped from stock.
  - For the same policy, **fill rate is usually higher than CSL**.

**Q13: High-value + erratic SKU**
- *Your answer:* AZ.
- *Model answer:* AZ. It is important *and* hard to forecast, so it gets the most planner attention. Options: higher safety stock or a tighter review cycle, customer collaboration on demand signals, or make-to-order where feasible.

**Q14: Forecast Value Add**
- *Your answer:* consensus forecast − statistical forecast (or current − naive). Overrides add context.
- *Model answer:*
  - FVA compares **accuracy**, not forecast values. FVA = accuracy(after step) − accuracy(before step), e.g. accuracy(consensus) − accuracy(stat).
  - Don't assume overrides help. FVA exists because they often **hurt**: research on judgmental adjustments finds that small and upward (optimistic) adjustments frequently reduce accuracy.
  - Measure accuracy with and without overrides, and limit overrides that destroy value.
- *Interview follow-up:* "Sales wants to override your forecast. How do you decide whether to accept it?"

## Day 0: Bootcamp checkpoint (2026-11-08), 3 / 3 ✅

**Q1: pandas equivalents of a PivotTable and XLOOKUP?**
- *Your answer:* `.pivot_table()` and `.merge()`.
- *Model answer:* Correct. Also `groupby()` = SUMIFS / subtotals, which is simpler when you only need one dimension.
- *Interview follow-up:* "How would you combine a forecast table with a product master that has price and lifecycle info?"

**Q2: Why `.shift(1).rolling(4).mean()` and not `.rolling(4).mean()`?**
- *Your answer:* `shift(1)` makes the average use only past weeks; including the current week would be data leakage.
- *Model answer:* Correct. Without the shift, the "forecast" for week t contains week t's actual, which is the answer itself.
- *Interview follow-up:* "Name another way leakage sneaks into feature engineering."

**Q3: `git commit` vs. `git push`?**
- *Your answer:* Commit saves a point with a message; push uploads the saved work to GitHub.
- *Model answer:* Correct. A commit is a local snapshot (save point) that exists only on your laptop. Push copies it to GitHub, which is the backup that protects against losing work.
