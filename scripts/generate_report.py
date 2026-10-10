"""Generate a factual report from persisted analysis tables."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    processed = ROOT / "data" / "processed"; synthetic = ROOT / "data" / "synthetic"; report = ROOT / "reports" / "engineering_report.md"
    summary = pd.read_csv(processed / "secom_dataset_summary.csv").set_index("metric")["value"]
    metrics = pd.read_csv(processed / "secom_model_metrics.csv").set_index("metric")["value"]
    doe = pd.read_csv(synthetic / "plasma_etch_doe_synthetic.csv")
    report.write_text(f"""# Engineering report

## Scope

This reproducible portfolio project separates an observational UCI SECOM yield-analysis module from a synthetic DOE teaching module. It does not contain production equipment data, recipe validation, root-cause proof, or qualified process limits.

## Module A: SECOM quality analysis

The UCI source has {int(summary['rows'])} observations and {int(summary['features'])} anonymized features. The loaded label distribution has {int(summary['fail_count'])} failures and {int(summary['pass_count'])} passes. Missingness, constants, duplicates, source-row alignment, and label/timestamp parsing are persisted under `data/processed/`.

Feature comparisons are exploratory Welch tests with Benjamini-Hochberg adjustment. Associations do not identify a physical mechanism because UCI does not supply feature semantics or experimental interventions.

The leakage-safe logistic baseline evaluates one held-out split: ROC-AUC {metrics['roc_auc']:.3f}, PR-AUC {metrics['pr_auc']:.3f}, and balanced accuracy {metrics['balanced_accuracy_at_0_5']:.3f}. These values are a reproducibility baseline, not a deployment claim. Any real workflow needs time-aware external validation, process context, measurement-system review, and decision-cost calibration.

## Module B: synthetic plasma-etch DOE

The DOE contains {len(doe)} synthetic runs: an illustrative 2^3 factorial plus center-point replicates. {int(doe['within_illustrative_window'].sum())} runs meet the deliberately illustrative response window. Response equations, factor levels, and seed are exposed in `src/doe.py` and `configs/analysis_config.yaml`. This output is solely a demonstration of DOE analysis and must not be interpreted as measured plasma physics or production capability.

## Decision discipline

No Cp/Cpk is calculated because no stable production process and approved specification limits are supplied. No SPC result is described as a production control limit. Before experiment execution, use the validation plan in `reports/experimental_validation_plan.md`.
""", encoding="utf-8")


if __name__ == "__main__": main()
