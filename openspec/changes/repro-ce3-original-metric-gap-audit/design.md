## Context

The previous rerun used `NL0119/Ce_5d1_Prediction@original`, sheet `RFE44`, `LeaveOneGroupOut` grouped by `Composition`, original 5d1 hyperparameters, CPU device, and `random_state=42`. It produced fold-mean MAE `0.1615349876620553` eV. The original notebook saved output reported fold-mean MAE `0.15338832561753013` eV and R2 `0.8380042800908163`.

## Decisions

- Treat notebook-saved metrics as a reference artifact, not as rerun ground truth.
- Compare against notebook-saved values using the same fold-mean metric definitions first.
- Also report global held-out metrics, but keep them separate from fold-mean values.
- Run a focused CPU sweep:
  - unseeded CPU/default parallelism
  - seeded CPU/default parallelism for seeds `0`, `1`, `22`, `42`, and `100`
  - seeded CPU/`n_jobs=1` for seed `42`
- Check CUDA availability with `nvidia-smi`; if unavailable, record `cuda_available=false` and skip GPU training.
- Keep the default local rerun device as CPU because it is reproducible on this machine.

## Outputs

- `results/tables/ce3_original_metric_gap/metric_gap_runs.csv`
- `results/tables/ce3_original_metric_gap/seed_sweep.csv`
- `results/tables/ce3_original_metric_gap/device_parallelism.csv`
- `results/tables/ce3_original_metric_gap/metric_gap_summary.json`
- `reproductions/ce3_original_metric_gap/report.md`

## Interpretation Rules

- `Model Inference` must be based on generated result tables or code outputs.
- `Experiment Hypothesis` must be used for any explanation not isolated by the completed controls.
- If all CPU controls remain separated from notebook-saved metrics, the report must classify the remaining gap as unresolved environment drift, with likely contributors listed but not asserted.

## Risks

- Full seed sweeps are computationally repetitive because each configuration runs 330 LOGO folds.
- XGBoost default behavior can change across versions, so current-version CPU controls may not reproduce historical notebook output.
- CUDA may not be available locally; absence of a GPU comparison cannot be treated as evidence that device has no effect.
