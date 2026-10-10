"""Descriptive quality analysis and a leakage-safe exploratory classifier."""

from __future__ import annotations

import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .preprocessing import make_numeric_pipeline


def quality_summary(features: pd.DataFrame, labels: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build feature-level and data-set-level quality tables."""
    feature_summary = pd.DataFrame(
        {
            "feature": features.columns,
            "missing_count": features.isna().sum().values,
            "missing_rate": features.isna().mean().values,
            "unique_nonmissing": features.nunique(dropna=True).values,
            "is_constant": (features.nunique(dropna=True) <= 1).values,
        }
    )
    dataset_summary = pd.DataFrame(
        [
            ("rows", len(features)),
            ("features", features.shape[1]),
            ("duplicate_feature_rows", int(features.duplicated().sum())),
            ("fail_count", int(labels["is_fail"].sum())),
            ("pass_count", int((~labels["is_fail"]).sum())),
            ("fail_rate", float(labels["is_fail"].mean())),
            ("timestamp_parse_rate", float(labels["timestamp"].notna().mean())),
        ],
        columns=["metric", "value"],
    )
    return feature_summary, dataset_summary


def exploratory_logistic_baseline(
    features: pd.DataFrame, is_fail: pd.Series, random_state: int, test_size: float, selected_feature_count: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fit a train-only imputation/scaling/selection model; report held-out metrics only."""
    x_train, x_test, y_train, y_test = train_test_split(
        features, is_fail.astype(int), test_size=test_size, stratify=is_fail.astype(int), random_state=random_state
    )
    k = min(selected_feature_count, x_train.shape[1])
    model = Pipeline(
        [
            ("numeric", make_numeric_pipeline()),
            ("select", SelectKBest(score_func=f_classif, k=k)),
            ("model", LogisticRegression(class_weight="balanced", max_iter=2000, random_state=random_state)),
        ]
    )
    model.fit(x_train, y_train)
    probability = model.predict_proba(x_test)[:, 1]
    prediction = model.predict(x_test)
    metrics = pd.DataFrame(
        [
            ("held_out_rows", len(y_test)),
            ("positive_rate_test", float(y_test.mean())),
            ("roc_auc", float(roc_auc_score(y_test, probability))),
            ("pr_auc", float(average_precision_score(y_test, probability))),
            ("balanced_accuracy_at_0_5", float(balanced_accuracy_score(y_test, prediction))),
        ],
        columns=["metric", "value"],
    )
    selected = model.named_steps["select"].get_support()
    selected_features = pd.DataFrame({"feature": x_train.columns[selected], "selected_in_training_only": True})
    return metrics, selected_features
