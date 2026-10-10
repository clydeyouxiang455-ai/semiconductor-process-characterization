"""Transparent synthetic 2^3 plasma-etch DOE demonstration."""

from __future__ import annotations

import itertools
import numpy as np
import pandas as pd


def generate_synthetic_doe(config: dict) -> pd.DataFrame:
    """Generate an explicitly illustrative, fixed-seed factorial-plus-center-point table."""
    factors = config["factors"]
    names = list(factors)
    corners = list(itertools.product([-1, 1], repeat=3))
    coded = corners + [(0, 0, 0)] * int(config["center_point_replicates"])
    rng = np.random.default_rng(int(config["random_state"]))
    rows = []
    for run, (pressure_c, power_c, flow_c) in enumerate(coded, start=1):
        codes = [pressure_c, power_c, flow_c]
        physical = {}
        for name, code in zip(names, codes):
            low, high = factors[name]
            physical[name] = (low + high) / 2 + code * (high - low) / 2
        # Deliberately hypothetical response equations. They are not measured physics.
        etch_rate = 103 + 7 * power_c - 4 * pressure_c + 3 * flow_c - 2 * pressure_c * power_c + rng.normal(0, 1.8)
        uniformity = 5.2 + 0.9 * pressure_c - 0.7 * flow_c + 0.5 * power_c * flow_c + rng.normal(0, 0.35)
        rows.append(
            {
                "run_order": run,
                "pressure_coded": pressure_c,
                "rf_power_coded": power_c,
                "gas_flow_coded": flow_c,
                **physical,
                "etch_rate_nm_min": etch_rate,
                "uniformity_percent": uniformity,
                "data_origin": "synthetic_teaching_demonstration",
            }
        )
    return pd.DataFrame(rows)


def process_window(datasets: pd.DataFrame, limits: dict) -> pd.DataFrame:
    """Flag synthetic DOE points meeting illustrative acceptance windows."""
    result = datasets.copy()
    low, high = limits["etch_rate_nm_min"]
    result["within_illustrative_window"] = (
        result["etch_rate_nm_min"].between(low, high) & (result["uniformity_percent"] <= limits["uniformity_percent_max"])
    )
    return result
