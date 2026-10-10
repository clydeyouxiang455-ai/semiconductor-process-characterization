"""Effect sizes and multiple-testing correction for exploratory feature comparisons."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


def cohens_d(group_a: np.ndarray, group_b: np.ndarray) -> float:
    """Pooled-standard-deviation standardized difference (a minus b)."""
    a, b = np.asarray(group_a, dtype=float), np.asarray(group_b, dtype=float)
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled_variance = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    return np.nan if pooled_variance <= 0 else float((a.mean() - b.mean()) / np.sqrt(pooled_variance))


def compare_by_yield(features: pd.DataFrame, is_fail: pd.Series) -> pd.DataFrame:
    """Run exploratory Welch tests and BH adjustment across anonymous features."""
    rows: list[dict[str, float | str]] = []
    fail_mask = is_fail.astype(bool).to_numpy()
    for name in features.columns:
        fail_values = features.loc[fail_mask, name].dropna().to_numpy()
        pass_values = features.loc[~fail_mask, name].dropna().to_numpy()
        if len(fail_values) < 2 or len(pass_values) < 2:
            continue
        statistic, p_value = stats.ttest_ind(fail_values, pass_values, equal_var=False, nan_policy="omit")
        rows.append(
            {
                "feature": name,
                "n_fail": len(fail_values),
                "n_pass": len(pass_values),
                "mean_fail": float(np.mean(fail_values)),
                "mean_pass": float(np.mean(pass_values)),
                "welch_t": float(statistic),
                "p_value": float(p_value),
                "cohens_d_fail_minus_pass": cohens_d(fail_values, pass_values),
            }
        )
    result = pd.DataFrame(rows)
    if not result.empty:
        result["p_value_bh"] = multipletests(result["p_value"], method="fdr_bh")[1]
        result = result.sort_values(["p_value_bh", "p_value"], kind="stable").reset_index(drop=True)
    return result
