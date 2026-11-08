"""Shared chart style for notebooks, so every chart in the project looks consistent.

Colours come from a colour-blind-checked categorical palette, always assigned in the
same fixed order (slot 1 = first category, etc.). Charts use thin lines, light
gridlines and no top/right borders, so the data stands out.
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Categorical slots, in fixed order (never cycled, never re-ordered per chart)
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
NEUTRAL = "#8a8986"        # for reference lines / "everything else"
TEXT = "#0b0b0b"
TEXT_MUTED = "#52514e"
SURFACE = "#fcfcfb"

# Fixed colour per entity, so a DC or generation keeps its colour in every chart
DC_ORDER = ["ALPHA", "BETA", "DELTA", "EPSILON", "GAMMA"]
DC_COLORS = dict(zip(DC_ORDER, PALETTE))
GEN_COLORS = {g: PALETTE[i] for i, g in enumerate([1, 2, 3, 4, 5])}


def use_project_style() -> None:
    plt.rcParams.update({
        "figure.figsize": (11, 4),
        "figure.dpi": 110,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "axes.edgecolor": "#cfcdc8",
        "axes.labelcolor": TEXT_MUTED,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.axisbelow": True,          # gridlines behind bars, not on top
        "axes.titlecolor": TEXT,
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": "#e6e4df",
        "grid.linewidth": 0.8,
        "xtick.color": TEXT_MUTED,
        "ytick.color": TEXT_MUTED,
        "lines.linewidth": 2.0,
        "legend.frameon": False,
        "legend.labelcolor": TEXT_MUTED,
        "font.size": 10,
    })


def thousands(ax, axis: str = "y") -> None:
    """Format an axis as 12k / 1.2M instead of 12000 / 1200000."""
    def fmt(x, _):
        if abs(x) >= 1e6:
            return f"{x / 1e6:.1f}M"
        if abs(x) >= 1e3:
            return f"{x / 1e3:.0f}k"
        return f"{x:.0f}"
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(FuncFormatter(fmt))


def percent(ax, axis: str = "y", decimals: int = 0) -> None:
    """Format an axis of fractions (0.25) as percentages (25%)."""
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(
        FuncFormatter(lambda x, _: f"{x:.{decimals}%}"))
