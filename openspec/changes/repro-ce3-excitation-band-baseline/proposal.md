## Why

This project needs a controlled reproduction state before auditing the Ce3+ phosphor excitation-band-position baseline. The first phase must determine whether the published work exposes enough data, code, supplementary material, or feature-generation detail for full reproduction, or whether only an approximate reproduction is defensible.

## What Changes

- Establish a `repro-*` OpenSpec change for arXiv:2502.18859, "Machine Learning a Phosphor's Excitation Band Position", and the corresponding MRS 2025 abstract.
- Define a traceable source-audit workflow for paper, conference abstract, supplementary information, code, public datasets, and feature descriptions.
- Define the minimum data schema for Ce3+ host, substitution-site, structural, local-environment, target-label, and source-provenance fields.
- Define baseline modeling requirements for XGBoost or comparable tree-based regressors, group-aware validation, fixed seeds, nm-scale metrics, leakage checks, and baseline comparison.
- Preserve the project boundary: no wet-lab execution, no unsupported conversion of model predictions or conference claims into verified experimental conclusions, and no replacement for original spectra or literature checks.

## Capabilities

### New Capabilities

- `ce3-excitation-baseline-reproduction`: Source audit, data reconstruction, modeling, validation, leakage review, and reporting requirements for the Ce3+ excitation-band-position reproduction.

### Modified Capabilities

- None.

## Impact

- Affects project planning and research artifacts under `openspec/`, `notes/`, `data/`, `reproductions/`, `experiments/`, `results/`, and `manuscript/`.
- Does not introduce code, dependencies, downloaded datasets, or model training in the first read-only preparation phase.
