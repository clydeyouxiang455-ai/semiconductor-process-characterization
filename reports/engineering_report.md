# Engineering report

Run `python scripts/download_data.py`, `python scripts/run_analysis.py`, and `python scripts/generate_report.py` to replace this placeholder with a report derived from the current official UCI source and the fixed-seed synthetic DOE data.

## Interpretation guardrails

- SECOM feature identifiers are anonymous. Statistical associations are not physical root-cause evidence.
- The raw UCI archive is the authority for its observed shape. The repository records its metadata-versus-file-column discrepancy rather than altering the source.
- Model metrics are exploratory held-out baseline measurements, not a deployment claim.
- The plasma-etch DOE output is deliberately synthetic and cannot validate a process window, recipe, capability, or equipment behavior.
- Do not calculate Cp/Cpk without an appropriate stability assessment and approved specifications.
