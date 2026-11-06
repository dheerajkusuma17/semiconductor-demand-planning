"""Environment check for the Semiconductor Demand Planning project.

Run:  python scripts/check_env.py

What it does (think of it as a pre-flight checklist):
  1. Confirms we're on Python 3.11 inside the project's .venv
  2. Imports every library and prints its version
  3. Runs a tiny "smoke test" for each forecasting / stats / inventory tool on toy data,
     so we know the library doesn't just import, it actually *works* on this machine
  4. Prints a PASS/FAIL table. Exit code 0 = all good, 1 = something needs fixing.

Re-run it any time something breaks: it is the first troubleshooting step.
"""
from __future__ import annotations

import importlib
import logging
import os
import sys
import tempfile
import time
import traceback
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
logging.disable(logging.WARNING)
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

# Windows consoles sometimes can't print emoji -> fall back to plain text.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    OK, BAD = "✅ PASS", "❌ FAIL"
except Exception:  # pragma: no cover
    OK, BAD = "PASS", "FAIL"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
results: list[tuple[str, bool, str]] = []


def check(name: str):
    """Decorator: run a check, time it, record PASS/FAIL with a short detail."""
    def wrap(fn):
        start = time.perf_counter()
        try:
            detail = fn() or ""
            results.append((name, True, f"{detail} ({time.perf_counter() - start:.1f}s)"))
        except Exception as exc:  # record, don't crash: we want the full checklist
            tb = traceback.format_exc(limit=1).strip().splitlines()[-1]
            results.append((name, False, f"{type(exc).__name__}: {exc} | {tb}"[:300]))
        return fn
    return wrap


# ---------------------------------------------------------------- 1. Python & venv
@check("Python 3.11")
def _():
    v = sys.version_info
    assert (v.major, v.minor) == (3, 11), f"found {v.major}.{v.minor}"
    return sys.version.split()[0]


@check("Running inside project .venv")
def _():
    exe = Path(sys.executable).resolve()
    assert (PROJECT_ROOT / ".venv") in exe.parents, f"python is {exe} - activate .venv first"
    return "yes"


@check("Project path works (spaces and '&')")
def _():
    p = PROJECT_ROOT / "data" / "processed" / "_path_test.txt"
    p.write_text("ok", encoding="utf-8")
    assert p.read_text(encoding="utf-8") == "ok"
    p.unlink()
    return str(PROJECT_ROOT)[-45:]


# ---------------------------------------------------------------- 2. Library imports
LIBS = ["pandas", "numpy", "scipy", "statsmodels", "statsforecast", "sklearn", "lightgbm",
        "xgboost", "torch", "neuralforecast", "matplotlib", "plotly", "openpyxl",
        "streamlit", "requests", "ipykernel", "nbconvert", "pytest"]
for lib in LIBS:
    check(f"import {lib}")(lambda lib=lib: getattr(importlib.import_module(lib), "__version__", "ok"))

# ---------------------------------------------------------------- 3. Smoke tests
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

rng = np.random.default_rng(42)
weeks = pd.date_range("2022-01-02", periods=104, freq="W-SUN")
# Toy weekly demand: level + gentle trend + quarterly wave + noise (like a CPU SKU)
demand = 500 + np.arange(104) * 2 + 60 * np.sin(np.arange(104) * 2 * np.pi / 13) + rng.normal(0, 30, 104)
series = pd.Series(demand.round(), index=weeks, name="orders")


@check("pandas: weekly resample + rolling (= Excel moving average)")
def _():
    ma4 = series.rolling(4).mean()
    monthly = series.resample("ME").sum()
    assert ma4.notna().sum() == 101 and len(monthly) > 20
    return f"{len(monthly)} months"


@check("statsmodels: ARIMA(1,1,1) forecast")
def _():
    from statsmodels.tsa.arima.model import ARIMA
    fc = ARIMA(series, order=(1, 1, 1)).fit().forecast(4)
    assert len(fc) == 4 and np.isfinite(fc).all()
    return f"next week ≈ {fc.iloc[0]:.0f}"


@check("statsmodels: Holt-Winters / ETS")
def _():
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    fc = ExponentialSmoothing(series, trend="add", seasonal="add", seasonal_periods=13).fit().forecast(4)
    assert np.isfinite(fc).all()
    return f"next week ≈ {fc.iloc[0]:.0f}"


@check("statsforecast: AutoETS + Croston + TSB")
def _():
    from statsforecast import StatsForecast
    from statsforecast.models import TSB, AutoETS, CrostonClassic
    intermittent = np.where(rng.random(104) < 0.6, 0, rng.integers(5, 40, 104))  # many zero weeks
    df = pd.concat([
        pd.DataFrame({"unique_id": "smooth_sku", "ds": weeks, "y": series.values}),
        pd.DataFrame({"unique_id": "slow_sku", "ds": weeks, "y": intermittent}),
    ])
    sf = StatsForecast(models=[AutoETS(season_length=13), CrostonClassic(),
                               TSB(alpha_d=0.2, alpha_p=0.2)], freq="W-SUN")
    fc = sf.forecast(df=df, h=4)
    assert len(fc) == 8
    return "2 SKUs x 3 models"


@check("scipy + statsmodels: bias significance (t-test, Wilcoxon, HAC)")
def _():
    from scipy import stats
    import statsmodels.api as sm
    actual = series.values
    biased_fc = actual * 1.10 + rng.normal(0, 20, 104)     # forecast 10% too high
    errors = biased_fc - actual
    p_t = stats.ttest_1samp(errors, 0).pvalue
    p_w = stats.wilcoxon(errors).pvalue
    hac = sm.OLS(errors, np.ones_like(errors)).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    assert p_t < 0.05 and p_w < 0.05 and hac.pvalues[0] < 0.05, "biased forecast not detected"
    return f"biased forecast detected, HAC p={hac.pvalues[0]:.1e}"


def _make_ml_table():
    """Turn the series into an ML 'prediction table': features = past weeks, target = this week."""
    df = pd.DataFrame({"y": series.values})
    for lag in (1, 2, 4, 13):
        df[f"lag_{lag}"] = df["y"].shift(lag)
    df["ma_4"] = df["y"].shift(1).rolling(4).mean()
    df = df.dropna()
    X, y = df.drop(columns="y").values, df["y"].values
    return X[:-8], y[:-8], X[-8:], y[-8:]


def _wmape(actual, fc):
    return np.abs(actual - fc).sum() / np.abs(actual).sum()


@check("scikit-learn: Ridge, Random Forest, MLP")
def _():
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import Ridge
    from sklearn.neural_network import MLPRegressor
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    Xtr, ytr, Xte, yte = _make_ml_table()
    out = []
    for name, m in [("Ridge", Ridge()),
                    ("RF", RandomForestRegressor(n_estimators=100, random_state=42)),
                    ("MLP", make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(32,), max_iter=2000, random_state=42)))]:
        out.append(f"{name} {_wmape(yte, m.fit(Xtr, ytr).predict(Xte)):.0%}")
    return "WMAPE " + ", ".join(out)


@check("LightGBM + XGBoost")
def _():
    import lightgbm as lgb
    import xgboost as xgb
    Xtr, ytr, Xte, yte = _make_ml_table()
    l = lgb.LGBMRegressor(n_estimators=100, min_child_samples=5, verbose=-1, random_state=42).fit(Xtr, ytr)
    x = xgb.XGBRegressor(n_estimators=100, random_state=42).fit(Xtr, ytr)
    return f"WMAPE LGBM {_wmape(yte, l.predict(Xte)):.0%}, XGB {_wmape(yte, x.predict(Xte)):.0%}"


@check("PyTorch (CPU)")
def _():
    import torch
    t = torch.ones(3, 3) @ torch.ones(3, 3)
    assert t.sum().item() == 27
    return f"cuda={torch.cuda.is_available()}"


@check("neuralforecast: N-HiTS + LSTM (tiny training run)")
def _():
    from neuralforecast import NeuralForecast
    from neuralforecast.models import LSTM, NHITS
    df = pd.DataFrame({"unique_id": "sku", "ds": weeks, "y": series.values})
    quiet = dict(max_steps=5, enable_progress_bar=False, logger=False,
                 enable_model_summary=False, accelerator="cpu", random_seed=42)
    nf = NeuralForecast(models=[NHITS(h=4, input_size=12, **quiet),
                                LSTM(h=4, input_size=12, **quiet)], freq="W-SUN")
    nf.fit(df=df)
    fc = nf.predict()
    assert len(fc) == 4
    return "trained 5 steps each"


@check("scipy: safety stock & reorder point math")
def _():
    from scipy.stats import norm
    z = norm.ppf(0.95)                          # 95% cycle service level
    sigma_err, lead_time, avg_demand = 40.0, 4, 500.0
    safety_stock = z * sigma_err * np.sqrt(lead_time)
    rop = avg_demand * lead_time + safety_stock
    assert abs(z - 1.645) < 0.001
    return f"z={z:.3f}, SS={safety_stock:.0f}, ROP={rop:.0f}"


@check("openpyxl: write planner Excel report")
def _():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "reorder_report.xlsx"
        pd.DataFrame({"SKU": ["CPU-A"], "ROP": [2132]}).to_excel(path, index=False)
        assert pd.read_excel(path)["ROP"].iloc[0] == 2132
    return "xlsx round-trip ok"


@check("matplotlib + plotly: render a chart")
def _():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    fig, ax = plt.subplots()
    series.plot(ax=ax)
    plt.close(fig)
    go.Figure(go.Scatter(x=weeks, y=series.values)).to_html(include_plotlyjs=False)
    return "ok"


@check("Jupyter kernel 'semiconductor-dp' registered")
def _():
    from jupyter_client.kernelspec import KernelSpecManager
    specs = KernelSpecManager().find_kernel_specs()
    assert "semiconductor-dp" in specs, "run: python -m ipykernel install --user --name semiconductor-dp"
    return "found"


# ---------------------------------------------------------------- 4. Report
width = max(len(n) for n, _, _ in results)
print("\nSemiconductor Demand Planning - environment check\n" + "=" * (width + 40))
for name, ok, detail in results:
    print(f"{(OK if ok else BAD):8}  {name:<{width}}  {detail}")
failed = [n for n, ok, _ in results if not ok]
print("=" * (width + 40))
print(f"{len(results) - len(failed)}/{len(results)} checks passed.")
if failed:
    print("Needs attention: " + "; ".join(failed))
sys.exit(1 if failed else 0)
