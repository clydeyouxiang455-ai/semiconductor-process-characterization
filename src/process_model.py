"""Regression and ANOVA for the synthetic DOE module."""

from __future__ import annotations

import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm


FORMULA = "{response} ~ pressure_coded * rf_power_coded * gas_flow_coded"


def fit_factorial_model(data: pd.DataFrame, response: str):
    """Fit a full two-level factorial model to the synthetic demonstration only."""
    return smf.ols(FORMULA.format(response=response), data=data).fit()


def anova_table(model) -> pd.DataFrame:
    """Return Type-II ANOVA for concise engineering interpretation."""
    return anova_lm(model, typ=2).reset_index(names="term")
