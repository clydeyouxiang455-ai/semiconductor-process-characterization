"""Run both modules end-to-end after `python scripts/download_data.py`."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data_loader import feature_mapping, load_secom, validate_secom
from src.doe import generate_synthetic_doe, process_window
from src.preprocessing import select_model_features
from src.process_model import anova_table, fit_factorial_model
from src.quality_analysis import exploratory_logistic_baseline, quality_summary
from src.statistical_tests import compare_by_yield
from src.visualization import save_doe_scatter, save_missingness_plot


def main() -> None:
    config = yaml.safe_load((ROOT / "configs" / "analysis_config.yaml").read_text(encoding="utf-8"))
    processed, synthetic, figures = ROOT / "data" / "processed", ROOT / "data" / "synthetic", ROOT / "reports" / "figures"
    for folder in (processed, synthetic, figures): folder.mkdir(parents=True, exist_ok=True)

    features, labels = load_secom(ROOT / "data" / "raw")
    validation = validate_secom(features, labels)
    (processed / "secom_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    feature_mapping(features).to_csv(processed / "feature_mapping.csv", index=False)
    feature_summary, dataset_summary = quality_summary(features, labels)
    feature_summary.to_csv(processed / "secom_feature_quality.csv", index=False)
    dataset_summary.to_csv(processed / "secom_dataset_summary.csv", index=False)
    save_missingness_plot(feature_summary, figures / "secom_missingness.png")
    model_features, preprocessing_audit = select_model_features(features, config["secom"]["missingness_threshold"])
    preprocessing_audit.to_csv(processed / "secom_preprocessing_audit.csv", index=False)
    compare_by_yield(model_features, labels["is_fail"]).to_csv(processed / "secom_welch_bh_results.csv", index=False)
    metrics, chosen = exploratory_logistic_baseline(
        model_features, labels["is_fail"], config["secom"]["random_state"], config["secom"]["test_size"], config["secom"]["selected_feature_count"]
    )
    metrics.to_csv(processed / "secom_model_metrics.csv", index=False); chosen.to_csv(processed / "secom_selected_features.csv", index=False)

    doe = generate_synthetic_doe(config["doe"])
    doe = process_window(doe, config["doe"]["illustrative_acceptance_window"])
    doe.to_csv(synthetic / "plasma_etch_doe_synthetic.csv", index=False)
    save_doe_scatter(doe, figures / "synthetic_doe_responses.png")
    for response in ("etch_rate_nm_min", "uniformity_percent"):
        anova_table(fit_factorial_model(doe, response)).to_csv(synthetic / f"anova_{response}.csv", index=False)
    print("Analysis complete. Review reports before interpreting any result as an engineering decision.")


if __name__ == "__main__": main()
