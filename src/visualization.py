"""Matplotlib figures with restrained labels and explicit synthetic-data annotations."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_missingness_plot(summary: pd.DataFrame, path: Path, top_n: int = 25) -> None:
    plot = summary.nlargest(top_n, "missing_rate").sort_values("missing_rate")
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.barh(plot["feature"], plot["missing_rate"], color="#335c81")
    ax.set_xlabel("Missing-value rate")
    ax.set_title("SECOM features with highest missingness")
    fig.tight_layout(); fig.savefig(path, dpi=160); plt.close(fig)


def save_doe_scatter(data: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    scatter = ax.scatter(data["etch_rate_nm_min"], data["uniformity_percent"], c=data["rf_power_coded"], cmap="coolwarm", s=70)
    ax.set_xlabel("Illustrative etch rate (nm/min)")
    ax.set_ylabel("Illustrative uniformity (%)")
    ax.set_title("Synthetic DOE responses; not measured equipment data")
    fig.colorbar(scatter, ax=ax, label="RF power (coded)")
    fig.tight_layout(); fig.savefig(path, dpi=160); plt.close(fig)
