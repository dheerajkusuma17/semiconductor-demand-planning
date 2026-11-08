"""Load and prepare the project data.

Everything here is reused by the notebooks and the Streamlit app, so the
cleaning rules are written once and applied the same way everywhere.

Key decisions (see docs/DECISIONS_LOG.md):
- Column names are converted to short snake_case names.
- A "series" is one SKU at one distribution center (SKU-DC), the level a planner
  forecasts and stocks at.
- The raw file only has rows for weeks with orders > 0. Weeks missing *inside* a
  series' life (between its first and last recorded week) are filled with
  orders = 0 and flagged `recorded = False`. Intel's forecast for those weeks is
  unknown, so it stays NaN.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "data" / "raw"
PROCESSED = PROJECT_ROOT / "data" / "processed"

INTEL_COLUMNS = {
    "Distribution Center": "dc",
    "Product Offering": "offering",
    "Generation": "generation",
    "SKU": "sku",
    "ASP Group": "asp_group",
    "Week": "week",
    "Forecasted Demand": "forecast",
    "Customer Orders": "orders",
}

# Syntetos-Boylan-Croston (SBC) demand classification thresholds
ADI_CUTOFF = 1.32   # average demand interval (weeks between non-zero demands)
CV2_CUTOFF = 0.49   # squared coefficient of variation of non-zero demand sizes


def load_intel(path: Path | str | None = None) -> pd.DataFrame:
    """Read the raw Intel CSV and return it with clean column names and a series id."""
    df = pd.read_csv(path or RAW / "intel_msom_2022.csv").rename(columns=INTEL_COLUMNS)
    missing = set(INTEL_COLUMNS.values()) - set(df.columns)
    if missing:
        raise ValueError(f"Intel file is missing columns: {missing}")
    df["series_id"] = df["sku"] + " | " + df["dc"]
    return df.sort_values(["series_id", "week"]).reset_index(drop=True)


def complete_weeks(df: pd.DataFrame) -> pd.DataFrame:
    """Give every series one row per week from its first to its last recorded week.

    Excel analogy: making sure every SKU has every week listed in the sheet,
    typing 0 in the orders column for weeks that were blank.
    """
    static_cols = ["dc", "offering", "generation", "sku", "asp_group"]
    frames = []
    for sid, g in df.groupby("series_id", sort=True):
        weeks = pd.RangeIndex(g["week"].min(), g["week"].max() + 1, name="week")
        full = g.set_index("week").reindex(weeks)
        full["recorded"] = full["orders"].notna()
        full["orders"] = full["orders"].fillna(0).astype(int)
        full[static_cols] = g[static_cols].iloc[0].values
        full["series_id"] = sid
        frames.append(full.reset_index())
    out = pd.concat(frames, ignore_index=True)
    out["generation"] = out["generation"].astype(int)
    out["asp_group"] = out["asp_group"].astype(int)
    return out[["series_id", *static_cols, "week", "forecast", "orders", "recorded"]]


def add_lifecycle(df: pd.DataFrame) -> pd.DataFrame:
    """Add life-cycle position columns.

    - sku_launch_week: first week the SKU had orders at ANY DC (its market launch)
    - launched_before_data: True if the SKU was already selling in week 1
    - weeks_since_launch: week - sku_launch_week
    - series_age: weeks since this SKU-DC's own first week
    - life_position: 0 at a series' first week, 1 at its last week
    """
    out = df.copy()
    out["sku_launch_week"] = out.groupby("sku")["week"].transform("min")
    # SKUs already selling in week 1 launched BEFORE the data starts ("left-censored"):
    # their weeks_since_launch counts from the data start, not the true launch.
    out["launched_before_data"] = out["sku_launch_week"] <= 1
    out["weeks_since_launch"] = out["week"] - out["sku_launch_week"]
    first = out.groupby("series_id")["week"].transform("min")
    last = out.groupby("series_id")["week"].transform("max")
    out["series_age"] = out["week"] - first
    out["life_position"] = ((out["week"] - first) / (last - first).replace(0, np.nan)).fillna(0.0)
    return out


def classify_demand(orders: pd.Series) -> str:
    """Syntetos-Boylan-Croston class for one series of weekly orders.

    - smooth:       regular timing, stable sizes   -> classic methods (ETS, ARIMA) work well
    - erratic:      regular timing, volatile sizes -> harder; ML / buffers
    - intermittent: many zero weeks, stable sizes  -> Croston / TSB
    - lumpy:        many zero weeks, volatile sizes -> hardest of all
    """
    nonzero = orders[orders > 0]
    if len(nonzero) < 2:
        return "insufficient"
    adi = len(orders) / len(nonzero)
    cv2 = (nonzero.std(ddof=0) / nonzero.mean()) ** 2
    if adi < ADI_CUTOFF:
        return "smooth" if cv2 < CV2_CUTOFF else "erratic"
    return "intermittent" if cv2 < CV2_CUTOFF else "lumpy"


def series_summary(df_complete: pd.DataFrame) -> pd.DataFrame:
    """One row per SKU-DC: length, volume, variability and demand class."""
    g = df_complete.groupby("series_id")
    summary = pd.DataFrame({
        "sku": g["sku"].first(),
        "dc": g["dc"].first(),
        "generation": g["generation"].first(),
        "asp_group": g["asp_group"].first(),
        "first_week": g["week"].min(),
        "last_week": g["week"].max(),
        "n_weeks": g.size(),
        "zero_weeks": g["orders"].apply(lambda s: int((s == 0).sum())),
        "total_orders": g["orders"].sum(),
        "mean_orders": g["orders"].mean(),
        "cv": g["orders"].std(ddof=0) / g["orders"].mean(),
    })
    summary["zero_share"] = summary["zero_weeks"] / summary["n_weeks"]
    nonzero = df_complete[df_complete["orders"] > 0].groupby("series_id")["orders"]
    summary["adi"] = summary["n_weeks"] / nonzero.size()
    summary["cv2_nonzero"] = (nonzero.std(ddof=0) / nonzero.mean()) ** 2
    summary["demand_class"] = g["orders"].apply(classify_demand)
    return summary


def load_fred(series_id: str) -> pd.Series:
    """Read a downloaded FRED CSV as a monthly pandas Series indexed by date."""
    df = pd.read_csv(RAW / f"fred_{series_id}.csv")
    date_col = df.columns[0]
    s = pd.to_numeric(df[series_id], errors="coerce")
    s.index = pd.to_datetime(df[date_col])
    s.index.name = "date"
    return s.dropna().rename(series_id)


def build_processed(save: bool = True) -> pd.DataFrame:
    """Raw Intel file -> complete weekly panel with life-cycle columns (Day 1 output)."""
    panel = add_lifecycle(complete_weeks(load_intel()))
    if save:
        PROCESSED.mkdir(parents=True, exist_ok=True)
        panel.to_parquet(PROCESSED / "intel_weekly_panel.parquet", index=False)
    return panel


def load_panel() -> pd.DataFrame:
    """Load the processed weekly panel, building it first if needed."""
    path = PROCESSED / "intel_weekly_panel.parquet"
    return pd.read_parquet(path) if path.exists() else build_processed()
