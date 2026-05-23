# Ce3+ 5d1 Original Baseline Rerun Report

Date: 2026-05-22
Release: `NL0119/Ce_5d1_Prediction@original`
Commit: `49991b75572dd3bf9ac4e5daa6000ac364b39b2d`

## Literature Fact

- Zenodo DOI `10.5281/zenodo.14872504` resolves through DOI/DataCite metadata to the `NL0119/Ce_5d1_Prediction` software record, version `original`, issued on 2025-02-14. Sources: https://doi.org/10.5281/zenodo.14872504 and https://api.datacite.org/dois/10.5281/zenodo.14872504
- DataCite metadata lists `https://github.com/NL0119/Ce_5d1_Prediction/tree/original` as a related `IsSupplementTo` identifier. Source: https://api.datacite.org/dois/10.5281/zenodo.14872504
- The original GitHub tag contains `Training_Set_for_5d1.xlsx` and `5d1Ce Prediction Model.ipynb`. Source: https://api.github.com/repos/NL0119/Ce_5d1_Prediction/contents?ref=original

## Model Inference

- Raw artifact manifest: `data/raw/ce_5d1_prediction/original/manifest.csv`.
- Dataset profile: `reproductions/ce3_original_baseline/dataset_profile.json`.
- Baseline outputs: `results/tables/ce3_original_baseline/`.
- The fetched `Training_Set_for_5d1.xlsx` workbook has sheet `RFE44`, 357 rows, 46 columns, 357 non-null `5d1` targets, and 330 unique `Composition` groups.
- Duplicate audit found 0 full duplicate rows and 25 duplicated composition groups covering 52 rows. The LOGO split groups by `Composition`, so rows sharing the same composition stay in the same fold.
- This run used a local deterministic CPU XGBoost rerun with original 5d1 hyperparameters plus `random_state=42`. The inspected notebook used `device='cuda'` and did not set an explicit XGBoost estimator seed.

## Metrics

Primary split: `LeaveOneGroupOut` grouped by `Composition`.

| model | fold-mean MAE eV | fold-mean RMSE eV | fold-mean MAE nm | fold-mean RMSE nm |
| --- | ---: | ---: | ---: | ---: |
| XGBoost original params | 0.161535 | 0.162452 | 16.315181 | 16.390102 |
| Train mean baseline | 0.421168 | 0.422849 | 42.248587 | 42.424544 |
| Train median baseline | 0.420135 | 0.421785 | 42.149800 | 42.324952 |

Global XGBoost metrics over all held-out predictions:

| metric | value |
| --- | ---: |
| MAE eV | 0.160836 |
| RMSE eV | 0.214683 |
| R2 eV | 0.826486 |
| MAE nm | 16.281178 |
| RMSE nm | 22.936547 |
| R2 nm | 0.821455 |

Notebook-saved 5d1 LOGO output from the original notebook reported `avg_mae=0.15338832561753013`, `avg_mse=0.04344782809517265`, `avg_rmse=0.15425705564280934`, and `r2=0.8380042800908163`. These are treated as notebook-saved reference values, not as rerun results.

## Leakage And Provenance

- Source-aware split is not auditable from this workbook because row-level DOI/year/source/in-house fields are absent.
- `Predicted CS` and `Predicted RP` are used as frozen released features. They were not regenerated inside nested cross-validation in this run.
- Fold-level R2 is recorded as blank for one-sample folds because R2 is mathematically undefined with fewer than two test samples.

## Experiment Hypothesis

- The remaining metric gap between notebook-saved values and this deterministic CPU rerun may come from XGBoost version, CPU/GPU behavior, and/or the notebook's missing explicit estimator seed. This has not yet been isolated by ablation.

## Follow-Up Audit

- Metric-gap controls are recorded in `reproductions/ce3_original_metric_gap/report.md`.
- The closest local rerun to the notebook-saved metrics was CPU unseeded/default, not the deterministic `random_state=42` rerun. It produced fold-mean MAE `0.154993` eV versus notebook-saved `0.153388` eV.
