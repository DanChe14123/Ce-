# Ce3+ Original Baseline Metric-Gap Audit

Date: 2026-05-23
Target release: `NL0119/Ce_5d1_Prediction@original`
Workbook: `data/raw/ce_5d1_prediction/original/Training_Set_for_5d1.xlsx`

## Literature Fact

- The metric-gap audit uses the same Zenodo/DataCite-linked `NL0119/Ce_5d1_Prediction@original` release selected in the paper-aligned baseline rerun. Source evidence is recorded in `notes/zenodo-github-version-audit.md` and `reproductions/ce3_original_baseline/report.md`.
- The inspected original notebook did not set an explicit `random_state` or `seed` in the 5d1 `XGBRegressor` definition, and it hard-coded `device='cuda'`. Source: `data/raw/ce_5d1_prediction/original/5d1Ce Prediction Model.ipynb`.

## Model Inference

- Output tables:
  - `results/tables/ce3_original_metric_gap/metric_gap_runs.csv`
  - `results/tables/ce3_original_metric_gap/seed_sweep.csv`
  - `results/tables/ce3_original_metric_gap/device_parallelism.csv`
  - `results/tables/ce3_original_metric_gap/metric_gap_summary.json`
- Seven CPU configurations completed successfully. CUDA comparison was skipped because `nvidia-smi` returned non-zero with a permission error on this machine.
- The previous baseline rerun used `random_state=42`, which produced fold-mean MAE `0.161535` eV. The notebook-like unseeded CPU/default rerun produced fold-mean MAE `0.154993` eV.
- The notebook-saved fold-mean MAE is `0.153388` eV. The notebook-like unseeded CPU/default rerun differs by `+0.001605` eV, whereas the seeded `random_state=42` default-parallelism rerun differs by `+0.008147` eV.
- Unseeded CPU/default and `random_state=0` CPU/default produced identical metrics in this environment.

## Metrics

| run | fold-mean MAE eV | fold-mean RMSE eV | global R2 eV | delta vs notebook MAE eV |
| --- | ---: | ---: | ---: | ---: |
| notebook saved output | 0.153388 | 0.154257 | 0.838004 | 0.000000 |
| CPU unseeded/default | 0.154993 | 0.155834 | 0.835515 | +0.001605 |
| CPU seed 0/default | 0.154993 | 0.155834 | 0.835515 | +0.001605 |
| CPU seed 1/default | 0.158683 | 0.159451 | 0.826913 | +0.005294 |
| CPU seed 22/default | 0.161379 | 0.162125 | 0.829529 | +0.007991 |
| CPU seed 42/default | 0.161535 | 0.162452 | 0.826486 | +0.008147 |
| CPU seed 100/default | 0.156602 | 0.157488 | 0.830062 | +0.003214 |
| CPU seed 42/n_jobs=1 | 0.159381 | 0.160229 | 0.826744 | +0.005992 |

## Interpretation

- Seed policy explains most of the metric gap observed in the prior deterministic `random_state=42` rerun. The notebook-like unseeded run is much closer to the notebook-saved values.
- `n_jobs=1` changes the seed-42 result but does not recover the notebook-saved metric, so parallelism alone does not explain the gap.
- CUDA/device effects remain untested locally because GPU access was unavailable.
- The residual `+0.001605` eV MAE gap between notebook-saved output and unseeded CPU/default is small but not fully isolated. Plausible contributors are XGBoost version, CPU/GPU behavior, and platform-level numerical differences.

## Experiment Hypothesis

- The original notebook-saved output may have been produced by an unseeded or default-seed XGBoost path, likely closer to current `random_state=0` than to the project's deterministic `random_state=42` rerun.
- The remaining gap may shrink or disappear under the original CUDA-enabled environment and historical package versions, but this is not verified here.

## Reporting Guidance

- Use the unseeded/default CPU audit as the closest local approximation to notebook-saved metrics.
- Use the seed-42 CPU result only as a deterministic project rerun, not as the closest reproduction of the notebook state.
- When reporting the paper-aligned baseline, list both:
  - notebook-saved reference: MAE `0.153388` eV, RMSE `0.154257` eV, R2 `0.838004`;
  - closest local rerun: CPU unseeded/default MAE `0.154993` eV, RMSE `0.155834` eV, global R2 `0.835515`.
