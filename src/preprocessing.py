"""Auditable preprocessing utilities with train-only transformations for models."""

from __future__ import annotations

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def select_model_features(features: pd.DataFrame, missingness_threshold: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Drop only threshold-exceeding and constant columns; return an audit table."""
    missing_rate = features.isna().mean()
    unique_count = features.nunique(dropna=True)
    keep = (missing_rate <= missingness_threshold) & (unique_count > 1)
    audit = pd.DataFrame(
        {
            "feature": features.columns,
            "missing_rate": missing_rate.values,
            "unique_nonmissing": unique_count.values,
            "keep_for_model": keep.values,
        }
    )
    return features.loc[:, keep].copy(), audit


def make_numeric_pipeline() -> Pipeline:
    """Median imputation and scaling, fitted only on each training partition."""
    return Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
