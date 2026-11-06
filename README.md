# Semiconductor Demand Planning: Forecasting & Inventory Optimization

> 🚧 Work in progress. Being built phase by phase; see [docs/PROGRESS_LOG.md](docs/PROGRESS_LOG.md).

A demand-planning project that goes beyond spreadsheet forecasting. It uses **real semiconductor demand data** to:

1. **Score the company's own forecast.** Measure Intel's microprocessor forecast accuracy, bias, and whether that bias is statistically significant.
2. **Build better forecasts.** Compare statistical models (ETS, ARIMA, Croston), machine-learning models (Random Forest, LightGBM, XGBoost) and neural networks (MLP, LSTM, N-HiTS) in a leakage-free rolling backtest, then measure **Forecast Value Add**.
3. **Optimize inventory.** Use ABC-XYZ segmentation, error-based safety stock, reorder points and a simulation that verifies the achieved service level and holding-cost impact.
4. **Communicate like a planner.** Deliver an interactive Streamlit app and an S&OP-style Power BI dashboard.

## Data
- **Intel microprocessor demand:** Manary, M. P. & Willems, S. P. (2022). *Data Set: 187 Weeks of Customer Forecasts and Orders for Microprocessors from Intel Corporation.* Manufacturing & Service Operations Management 24(1):682–689. https://doi.org/10.1287/msom.2020.0933
- **Market signals:** U.S. Census Bureau M3 survey and Federal Reserve industrial production, via [FRED](https://fred.stlouisfed.org/).

## Project structure
```
notebooks/   numbered analysis notebooks (00 bootcamp → 06 inventory)
src/         reusable Python code (metrics, models, inventory math)
app/         Streamlit app
powerbi/     Power BI dashboard + exported tables
docs/        industry primer, concepts primer, learning guide, decisions & progress logs
scripts/     environment check, data download
```

## Run it locally
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/check_env.py
```

*Results, screenshots and the live app link will be added as the phases complete.*
