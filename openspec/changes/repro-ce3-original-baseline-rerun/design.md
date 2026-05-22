## Context

The target implementation is the paper-aligned `NL0119/Ce_5d1_Prediction@original` release linked by Zenodo/DataCite DOI `10.5281/zenodo.14872504`. The 5d1 workbook has 357 rows and 46 columns in sheet `RFE44`; the model target is `5d1` energy in eV. The original notebook uses `LeaveOneGroupOut` with the `Composition` column as the group.

## Decisions

- Use `NL0119/Ce_5d1_Prediction@original` as the first implementation track.
- Download only the small public workbooks/notebook required to reproduce the processed 5d1 baseline.
- Store downloaded upstream artifacts under `data/raw/ce_5d1_prediction/original/` with a manifest that includes source URL, release label, SHA256, byte size, and local path.
- Use a deterministic CPU-oriented baseline by default for local reproducibility, while recording the original notebook's `device='cuda'` setting as a compatibility difference.
- Match original 5d1 hyperparameters first: `n_estimators=200`, `learning_rate=0.06`, `max_depth=9`, `min_child_weight=8`, `subsample=0.6`, `base_score=0.4`, `colsample_bytree=1`, `colsample_bylevel=1`, `colsample_bynode=1`, `reg_alpha=0`, `reg_lambda=1`.
- Use leave-one-composition-out (`LeaveOneGroupOut` grouped by `Composition`) as the primary split and report it explicitly as composition-grouped validation.
- Add `random_state=42` to the local reproduction estimator only in an explicitly labeled deterministic rerun, because the inspected notebook did not set an XGBoost estimator seed.
- Report notebook-saved metrics and local rerun metrics separately.

## Data Artifacts

- Raw upstream files:
  - `Training_Set_for_5d1.xlsx`
  - `5d1Ce Prediction Model.ipynb`
  - optional README metadata
- Processed local tables:
  - `reproductions/ce3_original_baseline/dataset_profile.json`
  - `results/tables/ce3_original_logo_metrics.csv`
  - `results/tables/ce3_original_leakage_audit.csv`
  - `results/tables/ce3_original_baseline_summary.json`

## Validation

- Verify downloaded file hashes and workbook shape before training.
- Verify required columns: `Composition`, `5d1`, `Predicted CS`, `Predicted RP`, and feature columns 2:46.
- Verify no empty rows, duplicated full rows, and record duplicated composition groups.
- Run leave-one-composition-out XGBoost and aggregate MAE, MSE, RMSE, and R2 in eV.
- Convert predictions and labels to nm with `lambda_nm = 1239.84193 / energy_eV` and report nm MAE/RMSE as secondary nonlinear metrics.
- Compare against mean and median eV baselines using the same folds.

## Risks

- Public processed workbook lacks source DOI/year/source/in-house flags, so source-aware leakage cannot be fully audited.
- CPU reruns may differ from the original GPU notebook if XGBoost version/device behavior differs.
- Adding a deterministic seed improves reproducibility but is not identical to the unseeded notebook unless reported as a local deterministic rerun.
- `Predicted CS` and `Predicted RP` are frozen auxiliary model outputs; this change does not regenerate them inside a nested pipeline.
