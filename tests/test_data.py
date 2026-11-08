"""Tests for src/data.py: small hand-made examples where we know the right answer."""
import pandas as pd
import pytest

from src.data import add_lifecycle, classify_demand, complete_weeks


def _toy():
    # One SKU at one DC, with week 3 missing (= a week with zero orders)
    return pd.DataFrame({
        "series_id": "SKU-X-1 | ALPHA", "dc": "ALPHA", "offering": "X", "generation": 1,
        "sku": "SKU-X-1", "asp_group": 5,
        "week": [1, 2, 4], "forecast": [100, 110, 120], "orders": [90, 100, 130],
    })


def test_complete_weeks_fills_gap_with_zero_orders():
    out = complete_weeks(_toy())
    assert out["week"].tolist() == [1, 2, 3, 4]
    assert out.loc[out.week == 3, "orders"].item() == 0
    assert not out.loc[out.week == 3, "recorded"].item()
    assert pd.isna(out.loc[out.week == 3, "forecast"].item())  # Intel's forecast is unknown
    assert out["orders"].sum() == 320                         # no orders created or lost


def test_lifecycle_positions():
    out = add_lifecycle(complete_weeks(_toy()))
    assert out["life_position"].tolist() == pytest.approx([0, 1 / 3, 2 / 3, 1])
    assert out["weeks_since_launch"].tolist() == [0, 1, 2, 3]
    assert out["launched_before_data"].all()          # first order in week 1 -> launched before data


@pytest.mark.parametrize("orders, expected", [
    ([100, 102, 98, 101, 99, 100], "smooth"),
    ([10, 300, 20, 250, 5, 400], "erratic"),
    ([0, 0, 50, 0, 0, 52, 0, 48], "intermittent"),
    ([0, 0, 5, 0, 0, 400, 0, 20], "lumpy"),
])
def test_demand_classes(orders, expected):
    assert classify_demand(pd.Series(orders)) == expected
