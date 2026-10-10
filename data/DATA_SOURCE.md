# Data sources and scope

## Module A: UCI SECOM

- Official landing page: <https://archive.ics.uci.edu/dataset/179/secom>
- Official archive used by `scripts/download_data.py`: <https://archive.ics.uci.edu/static/public/179/secom.zip>
- Citation: McCann, M. & Johnston, A. (2008). *SECOM* [Dataset]. UCI Machine Learning Repository. <https://doi.org/10.24432/C54305>
- License: CC BY 4.0, as stated on the UCI landing page.

The project downloads the two source text files without changing their contents. UCI's landing-page metadata says 1,567 rows and 591 features. A direct check of the current official `secom.data` archive shows **590 whitespace-separated values per row**; the project records and reports the observed source shape instead of silently padding it to match metadata. `secom_labels.data` contains a yield label and a quoted test timestamp. UCI describes `-1` as pass and `1` as fail. The anonymized feature identifiers do not establish sensor, chamber, recipe, wafer, or physical-process meaning. This project therefore calls them `feature_001` through the observed final column and does not infer physical meaning.

## Module B: illustrative plasma-etching DOE

No openly licensed, complete experimental DOE table with reusable raw response data was selected after source review. The project therefore generates a **synthetic teaching dataset** with a fixed seed. It is designed only to demonstrate factorial design, regression, ANOVA, residual diagnostics, and a hypothetical process-window workflow. It is not semiconductor fab data, does not validate any recipe, and must not be used for production decisions.

The factor names and units are conventional engineering labels only. Their ranges and response equations are transparent in `src/doe.py` and are deliberately not presented as measured equipment behavior.
