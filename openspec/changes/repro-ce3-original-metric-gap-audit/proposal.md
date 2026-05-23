## Why

The paper-aligned 357-row baseline rerun produced local deterministic CPU metrics that are close to, but not identical with, the saved output in the original notebook. Before using the rerun as the project reference, the gap must be audited so later claims do not confuse seed, device, version, or metric-aggregation effects with model or data errors.

## What Changes

- Add a controlled metric-gap audit workflow for the `NL0119/Ce_5d1_Prediction@original` 5d1 baseline.
- Run CPU seed sweeps, seeded/unseeded comparisons, and `n_jobs` controls using the same 357-row `RFE44` table.
- Check CUDA availability and run a CUDA comparison only if the local environment actually exposes a usable GPU path.
- Write compact summary tables for fold-mean metrics, global held-out metrics, and deviation from notebook-saved metrics.
- Update the reproduction report with an explicit interpretation of what the gap can and cannot explain.

## Non-Goals

- Do not change the baseline dataset or feature table.
- Do not train the later 358-row `BrgochGroup/main` workflow.
- Do not claim exact author-environment reproduction unless the environment is actually matched.
- Do not use missing source provenance fields to infer split groups.

## Impact

- Adds a metric-gap audit script under `scripts/`.
- Adds result tables under `results/tables/ce3_original_metric_gap/`.
- Adds a report under `reproductions/ce3_original_metric_gap/`.
- Leaves the prior baseline output intact.
