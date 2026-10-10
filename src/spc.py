"""Exploratory I-MR calculations with explicit baseline and interpretation limits."""

from __future__ import annotations

import numpy as np
import pandas as pd


def imr_limits(series: pd.Series, baseline_fraction: float = 0.60) -> dict[str, float]:
    """Calculate I-chart limits from an assumed baseline; not production control limits."""
    value = series.dropna().astype(float).reset_index(drop=True)
    baseline_n = max(3, int(len(value) * baseline_fraction))
    baseline = value.iloc[:baseline_n]
    moving_range = baseline.diff().abs().dropna()
    mr_bar = float(moving_range.mean())
    center = float(baseline.mean())
    sigma = mr_bar / 1.128 if mr_bar > 0 else np.nan
    return {"baseline_n": baseline_n, "center": center, "mr_bar": mr_bar, "ucl": center + 3 * sigma, "lcl": center - 3 * sigma}
