## Why

The first source-audit phase established that the paper/MRS 357-site count aligns with the Zenodo/DataCite-linked `NL0119/Ce_5d1_Prediction@original` release, while the later `BrgochGroup/main` workbook is a different 358-row release. The next step is to make the paper-aligned 357-row baseline reproducible from public artifacts without relying on notebook state or chat history.

## What Changes

- Create a reproducible pipeline for the `NL0119/Ce_5d1_Prediction@original` 357-row 5d1 table.
- Fetch only small public source artifacts needed for the baseline and record URL, commit/tag, SHA256, row/column counts, target units, and missing provenance fields.
- Implement an auditable XGBoost baseline matching the original notebook's 5d1 settings and leave-one-composition-out split.
- Record metrics in eV and converted nm units, plus mean/median baselines and split/leakage diagnostics.
- Preserve the distinction between processed-model reproduction and provenance-audited literature reconstruction.

## Non-Goals

- Do not train the later 358-row `BrgochGroup/main` workflow in this change.
- Do not treat notebook-saved outputs as rerun metrics.
- Do not infer missing DOI/year/source/in-house fields from composition or target values.
- Do not download large external datasets or query Materials Project unless a later change explicitly requires feature regeneration.

## Impact

- Adds reusable source code under `src/` and entrypoint scripts under `scripts/`.
- Adds paper-aligned reproduction artifacts under `reproductions/ce3_original_baseline/`.
- Adds result tables under `results/tables/`.
- Adds no wet-lab claims and no unverified experimental conclusions.
