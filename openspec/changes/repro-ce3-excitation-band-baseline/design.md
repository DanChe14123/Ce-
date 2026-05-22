## Context

The target work is a Ce3+ inorganic phosphor excitation-band-position prediction study. The reproduction must distinguish directly supported literature facts from model inferences, experimental hypotheses, and writing guidance. The project currently has no prior active OpenSpec change and no matching project-memory facts.

## Goals / Non-Goals

**Goals:**

- Verify the availability of the paper, MRS 2025 abstract, supplementary information, code, training tables, feature-generation descriptions, and any public data artifacts.
- Classify the reproduction level as `full reproduction` only if complete training data and sufficient feature/label definitions are publicly available; otherwise classify it as `approximate reproduction`.
- Define a traceable Ce3+ dataset schema covering host identity, activator/site information, structural and local-environment descriptors, longest excitation wavelength labels, measurement/source metadata, DOI/year, in-house status, units, and notes.
- Plan an XGBoost or comparable baseline with fixed seeds, group-aware validation, nm-scale metrics, baseline comparisons, and leakage checks.
- Plan literature reconstruction from tables, supplementary files, spectra, figures, and databases without overstating low-confidence extracted values.

**Non-Goals:**

- No wet-lab synthesis, characterization, or experimental validation.
- No large file downloads, code implementation, model training, or benchmark execution during the read-only preparation phase.
- No use of model predictions, conference abstracts, or inaccessible in-house data as verified experimental facts.
- No silent inference of missing fields; use `not reported` when evidence is absent.

## Decisions

- Use `cmd /c openspec ...` for OpenSpec CLI calls on this Windows environment because the PowerShell shim is blocked by script execution policy.
- Use `repro-ce3-excitation-band-baseline` as the active change name.
- Treat public training-data availability as the primary gate between full and approximate reproduction.
- Use the following canonical table fields for the first schema: `material_id`, `host`, `activator`, `co_dopant`, `Ce3+ substitution site`, `crystal structure`, `local coordination`, `composition descriptors`, `longest excitation wavelength_nm`, `measurement/source metadata`, `source_doi`, `source_year`, `is_in_house`, `units`, and `notes`.
- Prefer group-aware splits over random-only splits when host, structural family, literature source, or composition family can create leakage.
- Track every literature-derived label with source provenance and manual-check status.

## Risks / Trade-offs

- If the paper uses inaccessible in-house data, metrics from an approximate reproduction will not be directly comparable to the reported paper metrics.
- Values digitized from plots may carry peak-selection and resolution uncertainty; such labels must be marked lower confidence and excluded from strict benchmark claims unless manually verified.
- Local coordination and substitution-site descriptors may require crystallographic interpretation beyond composition strings; unresolved site assignments must remain `not reported` or `needs manual check`.
- Conference abstracts may reveal scope or claims but usually cannot substitute for raw tables, spectra, code, or supplementary methods.
