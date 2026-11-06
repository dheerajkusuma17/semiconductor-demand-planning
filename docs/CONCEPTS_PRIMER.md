# Concepts Primer: the theory behind this project

Read this before Day 1. Each idea gets a plain-language explanation, a tiny worked example, and the place it shows up in the project. Take the **quiz at the end**; the target is 12/15.

---

## 1. Time series basics

A **time series** is a list of values recorded in time order, such as weekly orders for one CPU at one warehouse.

| Concept | Plain meaning | Example |
|---|---|---|
| **Level** | The "normal" amount right now | About 500 units/week |
| **Trend** | Steady movement up or down | +10 units/week while a new CPU generation ramps up |
| **Seasonality** | A pattern that repeats on a fixed calendar | Orders spike in the last month of every quarter as customers hit quarter-end targets |
| **Noise** | Random ups and downs no model can predict | One customer pulls an order forward by a week |
| **Autocorrelation** | This week's value is related to last week's | A high week is usually followed by another high-ish week |
| **Stationarity** | Mean and spread stay stable over time (no trend). ARIMA needs this, so it **differences** the data (week-to-week change) to remove trend | Orders 500, 510, 520 → differences 10, 10 = stable |
| **Intermittent demand** | Many weeks with zero demand | A legacy CPU at a small warehouse: 0, 0, 40, 0, 0, 0, 25 … |

**Excel bridge:** a line chart of a column of weekly sales is a time series plot. A "moving average" trendline is a smoothed version of it.

---

## 2. How we judge a forecast fairly

- **Train / test split:** fit the model on older data, then check it on newer data it has never seen. That is like an exam where the questions aren't in the textbook.
- **Data leakage:** accidentally letting the model see the future, for example by using a full-year average that includes the test weeks. It makes results look great on paper and fail in real life. **This is the #1 mistake in forecasting projects.**
- **Rolling-origin backtest:** repeat the train/test split many times, moving the cut-off forward:
  ```
  Cut-off 1: train weeks 1–100  → forecast weeks 101–104
  Cut-off 2: train weeks 1–104  → forecast weeks 105–108
  Cut-off 3: train weeks 1–108  → forecast weeks 109–112   … and so on
  ```
  This mimics how a planner actually re-forecasts every week or month.
- **Horizon:** how far ahead we forecast (e.g. 4 weeks, 13 weeks).
- **Lag:** which forecast version we score. A "lag-4" forecast is the one made 4 weeks before the actual week. Supply decisions are made at the lead time, so **we score the forecast at the lag that matters for supply**.
- **Overfitting:** the model memorises noise in the training data and forecasts badly on new data. It's like a student who memorised last year's answers.

---

## 3. Error metrics: how wrong was the forecast?

Error = Forecast − Actual. Positive means we over-forecast; negative means we under-forecast.

Worked example (3 weeks, one SKU):

| Week | Actual | Forecast | Error (F − A) | Absolute error |
|---|---|---|---|---|
| 1 | 100 | 120 | +20 | 20 |
| 2 | 200 | 180 | −20 | 20 |
| 3 | 10 | 30 | +20 | 20 |
| **Total** | **310** | **330** | **+20** | **60** |

| Metric | Formula | Example result | Notes |
|---|---|---|---|
| **MAE** | average absolute error | 60/3 = **20 units** | Easy to explain, in units |
| **MAPE** | average of (abs error ÷ actual) | (20% + 10% + 200%)/3 = **77%** | Explodes on small actuals (week 3), and is undefined when actual = 0. **Avoid for intermittent demand** |
| **WMAPE** | Σ abs error ÷ Σ actual | 60/310 = **19.4%** | Big-volume weeks count more. **Our main metric** |
| **Forecast accuracy** | 1 − WMAPE | **80.6%** | The number planners report ("71% accuracy" on the old resume was this kind of figure) |
| **Bias %** | Σ error ÷ Σ actual | +20/310 = **+6.5%** | + means over-forecasting, − means under-forecasting |
| **Tracking signal** | cumulative error ÷ MAD | +20/20 = **+1.0** | Outside ±4 means the forecast is drifting and needs attention |

**Excel bridge:** WMAPE = `SUMPRODUCT(ABS(F-A))/SUM(A)`.

---

## 4. Statistics you'll need

- **Mean / standard deviation (σ):** the centre of the data and its typical spread. σ of forecast errors drives safety stock.
- **Normal distribution:** the bell curve. About 68% of values fall within ±1σ, 95% within ±1.96σ, and 99.7% within ±3σ.
- **z-score:** how many σ's away from the mean a value is. In inventory, z sets the service level:

  | Cycle service level | z |
  |---|---|
  | 90% | 1.28 |
  | 95% | 1.645 |
  | 98% | 2.05 |
  | 99% | 2.33 |

  **Excel bridge:** `NORM.S.INV(0.95)` = 1.645.
- **Confidence interval (CI):** a range that likely contains the true value. "Bias = +6% (95% CI: +2% to +10%)" means we're fairly sure the real bias is positive.
- **Hypothesis test and p-value:**
  - **H0 (null hypothesis):** "the forecast is unbiased: average error = 0."
  - **p-value:** if H0 were true, how surprising would our data be? A small p (< 0.05) means it would be very surprising, so we reject H0 and call the bias **statistically significant**.
  - **Significant ≠ large.** With lots of data, a tiny 1% bias can be significant. That's why our decision rule looks at **both** significance and size.
- **t-test vs. Wilcoxon:** the t-test assumes errors are roughly bell-shaped. Wilcoxon only uses ranks, so it is robust to skewed errors and outliers. We run both.
- **HAC (Newey-West) standard errors:** forecast errors in consecutive weeks are related (autocorrelated). A normal t-test then overstates its confidence. HAC corrects for this, so we don't cry "significant!" too easily.

---

## 5. Inventory concepts

- **Lead time (LT):** time from placing a replenishment order to having stock available. In semis it's long, often months.
- **Cycle stock:** inventory that covers *expected* demand between replenishments.
- **Safety stock (SS):** extra inventory that covers *forecast error* during the lead time.
- **Safety stock formula (forecast-error based):**

  `SS = z × σ_error × √LT`

  - `σ_error` is the standard deviation of weekly forecast errors; `LT` is in weeks.
  - Example: z = 1.645 (95%), σ_error = 40 units/week, LT = 4 weeks → SS = 1.645 × 40 × 2 = **132 units**.
  - Why errors and not raw demand? If demand is predictably seasonal, a good forecast already captures that. We only need a buffer for what the forecast *gets wrong*.
- **Reorder point (ROP):** `ROP = expected demand during LT + SS`. With 500/week, ROP = 500 × 4 + 132 = **2,132 units**. When inventory position drops below 2,132, place an order.
- **Cycle service level (CSL) vs. fill rate:**
  - **CSL** = % of replenishment cycles with **no** stockout. 95% CSL means 1 in 20 cycles runs out.
  - **Fill rate** = % of **units** demanded that were shipped from stock. It is usually higher than CSL, because a stockout cycle still fills most units.
  - Always say which one you mean. Interviewers check this.
- **Holding cost:** the cost of carrying inventory, typically 15–30% of item value per year (capital, storage, obsolescence). In semis, obsolescence makes it high.
- **EOQ (Economic Order Quantity):** `√(2 × annual demand × order cost / holding cost per unit)`. It balances ordering often against holding a lot.
- **ABC-XYZ segmentation:**
  - **ABC** by value: A = top ~80% of value, B = next ~15%, C = last ~5%.
  - **XYZ** by variability, measured by the coefficient of variation (CV = σ/mean): X = stable, Y = variable, Z = erratic.
  - Use it to set **different service levels and methods per segment**. For example, AX gets a high service level and is easy to forecast; CZ gets a lower service level and might be made-to-order.

---

## 6. The planning process

- **S&OP / IBP (Sales & Operations Planning / Integrated Business Planning):** a monthly cycle in which demand, supply and finance agree on one plan. The steps run demand review → supply review → pre-S&OP → executive S&OP.
- **Statistical forecast → consensus forecast:** planners start from the model forecast, then sales, marketing and customer input adjust it.
- **Forecast Value Add (FVA):** does each step *improve* accuracy? For example, compare `accuracy(our model) − accuracy(naive)` or `accuracy(consensus) − accuracy(statistical)`. If an override makes the forecast worse, stop doing it. **In this project: FVA of our models vs. Intel's own forecast.**
- **Unconstrained vs. constrained demand:**
  - **Unconstrained:** what customers *want*.
  - **Constrained:** what we *can ship* given supply.
  - In shortages, **allocation** decides who gets what.

---

## 7. Quiz (15 questions)

Answer on paper or in chat first, then open the answers.

1. Weekly orders go 400, 420, 440, 460. Which component dominates: level, trend or seasonality?
2. Why can't MAPE be used for a SKU with many zero-demand weeks?
3. Actual = [50, 150], Forecast = [70, 120]. Compute WMAPE and forecast accuracy.
4. Same data: compute bias %. Is it over- or under-forecasting?
5. What is data leakage? Give one example in a forecasting project.
6. Why do we use a *rolling-origin* backtest instead of a single train/test split?
7. A forecast has bias +3% with p = 0.40. A second has bias +12% with p = 0.001. What would you do with each?
8. Why do we use HAC (Newey-West) errors when testing forecast bias over consecutive weeks?
9. What z-value corresponds to a 95% cycle service level? What's the Excel function?
10. σ_error = 50 units/week, LT = 9 weeks, 95% CSL. Compute safety stock.
11. Average demand 300/week, LT = 9 weeks, SS from Q10. Compute the reorder point.
12. What's the difference between cycle service level and fill rate?
13. A SKU is high-value with erratic demand. Which ABC-XYZ cell is it in, and what does that imply?
14. What is Forecast Value Add, and how would you use it to judge sales overrides?
15. Why should safety stock be based on forecast-error variability rather than raw demand variability?

<details>
<summary><b>Answers (click to open)</b></summary>

1. **Trend** (+20 every week).
2. When actual = 0 you divide by zero, and tiny actuals make the % explode. Use WMAPE or MAE instead.
3. Absolute errors are 20 and 30, so Σ = 50. Σ actual = 200. **WMAPE = 25%, accuracy = 75%.**
4. Errors are +20 and −30, so Σ = −10. Bias = −10/200 = **−5% → under-forecasting.**
5. Using information that wouldn't be known at forecast time. Examples: scaling with the full-dataset mean, a rolling average that includes the current week, or random (non-time-ordered) train/test splits.
6. A single split can be lucky or unlucky. Rolling origins test many periods and mimic real weekly or monthly re-forecasting, so results are more reliable.
7. First: not significant, so treat it as tolerable noise and don't adjust. Second: significant and large, so act. Investigate the cause, apply a bias correction, or retrain.
8. Consecutive errors are correlated, so a plain t-test thinks it has more independent information than it really does and gives p-values that are too small. HAC corrects this.
9. **1.645**, `=NORM.S.INV(0.95)`.
10. 1.645 × 50 × √9 = 1.645 × 50 × 3 = **≈ 247 units.**
11. 300 × 9 + 247 = **2,947 units.**
12. CSL = % of cycles with no stockout. Fill rate = % of units served from stock. The same policy usually has a fill rate higher than its CSL.
13. **AZ**: important and hard to forecast. It needs the most planner attention, possibly higher safety stock or a customer-collaboration / make-to-order approach.
14. FVA = accuracy after a step − accuracy before it. Compare accuracy of the forecast with the overrides vs. without. If overrides lower accuracy (or add bias), limit them.
15. The forecast already explains predictable movement (trend, seasonality). Inventory only needs to buffer what the forecast **gets wrong**. Raw demand σ overstates the risk for predictable items.

</details>
