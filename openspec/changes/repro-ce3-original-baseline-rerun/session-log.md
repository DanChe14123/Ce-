# 1. What Was Completed

- [x] Restored project context from `AGENTS.md`, project memory status, and OpenSpec.
- [x] Confirmed prior change `repro-ce3-excitation-band-baseline` is complete.
- [x] Created OpenSpec change `repro-ce3-original-baseline-rerun`.
- [x] Selected paper-aligned `NL0119/Ce_5d1_Prediction@original` as the first implementation track.
- [x] Added `requirements.txt`, reusable code under `src/ce3_repro/`, and entrypoints under `scripts/`.
- [x] Created local `.venv` and installed dependencies for execution.
- [x] Fetched 3 small upstream artifacts from `NL0119/Ce_5d1_Prediction@original` and wrote manifest files under `data/raw/ce_5d1_prediction/original/`.
- [x] Profiled the 357-row `RFE44` 5d1 workbook and wrote `reproductions/ce3_original_baseline/dataset_profile.json`.
- [x] Ran the leave-one-composition-out XGBoost baseline and wrote result tables under `results/tables/ce3_original_baseline/`.
- [x] Wrote `reproductions/ce3_original_baseline/report.md`.
- [x] Validated `repro-ce3-original-baseline-rerun` with `cmd /c openspec validate repro-ce3-original-baseline-rerun`.

# 2. Evidence-Backed Conclusions

- [x] Project memory is connected under project memory id `ce3-63aa6e88`, with no relevant stable fact returned for this target query.
- [x] The prior source-audit change concluded that Zenodo/DataCite DOI `10.5281/zenodo.14872504` points to `NL0119/Ce_5d1_Prediction@original`.
- [x] The prior audit found the `original` 5d1 workbook has 357 rows, 46 columns, sheet `RFE44`, 357 non-null `5d1` targets, and 330 unique compositions.
- [x] The prior code audit found the `original` notebook uses `LeaveOneGroupOut` grouped by `Composition`.
- [x] The fetched `Training_Set_for_5d1.xlsx` SHA256 is `4a28098c346800b2f0d2ced9618be13086c0287d0aceffc94e4a2d93470435fe`.
- [x] Local deterministic CPU rerun used Python 3.12.13, pandas 3.0.3, scikit-learn 1.8.0, and xgboost 3.2.0.
- [x] XGBoost original-parameter LOGO rerun produced global MAE `0.16083551934720422` eV, RMSE `0.2146831319121065` eV, and R2 `0.8264857369342495`.
- [x] XGBoost fold-mean metrics were MAE `0.1615349876620553` eV and RMSE `0.16245230476530725` eV; train-mean and train-median baselines had fold-mean MAE about `0.421` eV.
- [x] Leakage audit found 0 full duplicate rows and 25 duplicated composition groups covering 52 rows; LOGO keeps duplicated composition rows in the same fold.

# 3. Current Blockers

- [ ] Source DOI/year/source/in-house flags remain unavailable in the public processed workbook.
- [ ] Direct Zenodo payload checksums remain unverified because Zenodo routes returned HTTP 403 in the prior audit.
- [ ] The difference between notebook-saved metrics and local deterministic CPU rerun metrics is not yet isolated; likely factors include XGBoost version, CPU/GPU behavior, and missing explicit notebook seed.

# 4. First Next Action

- [ ] Isolate the metric gap between notebook-saved outputs and the local deterministic CPU rerun by running controlled seed/device/version checks.
