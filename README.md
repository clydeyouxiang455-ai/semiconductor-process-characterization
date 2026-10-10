# Semiconductor Process Characterization & Statistical Analysis

A reproducible portfolio project with two clearly separated modules:

1. **UCI SECOM observational quality analysis.** Data validation, missingness/constant-feature checks, class-imbalance reporting, exploratory Welch tests with Benjamini-Hochberg correction, and a train-only-preprocessed logistic baseline.
2. **Synthetic plasma-etch DOE demonstration.** A fixed-seed 2^3 factorial with center points, response regression/ANOVA, diagnostics inputs, and an illustrative process window. It is not real equipment data.

## Boundaries

SECOM contains anonymized variables. The project never assigns them physical sensor or chamber meanings. Associations are not root-cause proof. The current official raw archive should be treated as the authority for its observed shape: its source matrix has 590 values per row, while the UCI landing page describes 591 features; this discrepancy is reported rather than concealed. The DOE data are generated explicitly for teaching and portfolio demonstration, so no output supports a recipe, capability, yield, or production-performance claim.

## Quick start

Use Python 3.11 or newer (the project is designed to work with Python 3.14 if compatible wheels are available):

```powershell
& "D:\python\python.exe" -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" scripts/download_data.py
& ".\.venv\Scripts\python.exe" scripts/run_analysis.py
& ".\.venv\Scripts\python.exe" scripts/generate_report.py
& ".\.venv\Scripts\python.exe" -m pytest
```

The raw UCI source is intentionally ignored by Git. The download script fetches it from the official UCI archive and writes checksums locally.

## Project flow

```
Official UCI raw files → validation and quality audit → exploratory association tests
                                      └→ train-only preprocessing → held-out baseline

Fixed-seed synthetic DOE → factorial model / ANOVA → illustrative process-window flag
```

## Repository layout

- `configs/`: reproducible thresholds, seed, and explicitly illustrative DOE settings.
- `data/`: source documentation, ignored raw files, processed audit tables, and synthetic DOE output.
- `src/`: reusable loading, preprocessing, statistical, DOE, and plotting modules.
- `scripts/`: download, analysis, and report entry points.
- `reports/`: engineering report, figures, and a real-experiment validation plan.
- `tests/`: unit tests for source handling, preprocessing, statistics, and DOE construction.

## Source

See [data/DATA_SOURCE.md](data/DATA_SOURCE.md). The official UCI SECOM citation is McCann & Johnston (2008), DOI [10.24432/C54305](https://doi.org/10.24432/C54305), CC BY 4.0.
