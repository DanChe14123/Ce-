# Zenodo/GitHub Version Audit: Ce3+ 5d1 Training Data

Date: 2026-05-22

## Literature Fact

- Zenodo DOI `10.5281/zenodo.14872504` resolves through DOI/DataCite metadata to a software record titled `NL0119/Ce_5d1_Prediction: Ce3+ Excitation Energy Level Predition Model`, issued on 2025-02-14, version `original`. Sources: https://doi.org/10.5281/zenodo.14872504 and https://api.datacite.org/dois/10.5281/zenodo.14872504
- The DataCite metadata for Zenodo DOI `10.5281/zenodo.14872504` lists a related identifier with relation type `IsSupplementTo`: `https://github.com/NL0119/Ce_5d1_Prediction/tree/original`. Source: https://api.datacite.org/dois/10.5281/zenodo.14872504
- GitHub reports `NL0119/Ce_5d1_Prediction` tag `original` at commit `49991b75572dd3bf9ac4e5daa6000ac364b39b2d`, committed on 2025-02-12. Source: https://api.github.com/repos/NL0119/Ce_5d1_Prediction/commits/original
- The Zenodo-linked `original` tag contains `Training_Set_for_5d1.xlsx`, `Training_Set_for_CS.xlsx`, `Training_Set_for_RP.xlsx`, `Prediction List.xlsx`, `Tester.xlsx`, element tables, README, and `5d1Ce Prediction Model.ipynb`. Source: https://api.github.com/repos/NL0119/Ce_5d1_Prediction/contents?ref=original
- GitHub reports `BrgochGroup/Ce_5d1_Prediction` as a fork of `NL0119/Ce_5d1_Prediction`; its `main` branch commit inspected here is `4c7faeb0e92695f08289920ff4882635beff9694`, committed on 2026-03-13. Source: https://api.github.com/repos/BrgochGroup/Ce_5d1_Prediction and https://api.github.com/repos/BrgochGroup/Ce_5d1_Prediction/commits/main
- Direct Zenodo landing page, API, OAI/export, and guessed file-download routes returned HTTP 403 from this machine during this audit. This blocks direct Zenodo payload checksum verification; it does not contradict the DOI/DataCite related-GitHub evidence.

## Model Inference

- Temporary inspection of Zenodo-linked GitHub tag `NL0119/Ce_5d1_Prediction@original` found `Training_Set_for_5d1.xlsx` with sheet `RFE44`, shape `357 x 46`, 357 non-null `5d1` target values, 330 unique `Composition` values, 0 duplicate full rows, and 0 empty rows.
- Temporary inspection of later fork `BrgochGroup/Ce_5d1_Prediction@main` found `Training_Set_updated_for_5d1_RFE17.xlsx` with shape `358 x 19`, 358 non-null `5d1 Ce` target values, 330 unique `Composition` values, 0 duplicate full rows, and 0 empty rows.
- The 357-vs-358 mismatch is best classified as release/version drift between the Zenodo-linked `original` tag and the later `BrgochGroup/main` fork, not as a blank row, duplicate header row, full duplicate row, or tester-row inclusion artifact.
- The releases differ by more than one appended row. Comparing composition-target multisets found 148 compositions with changed target multisets, 149 exact composition-target pairs only in `original`, and 152 exact composition-target pairs only in the later `main` table.
- Count differences by composition were:

| Composition | original count | later main count | delta |
| --- | ---: | ---: | ---: |
| `Ca2Si5N8` | 1 | 2 | +1 |
| `K3Lu(PO4)2` | 4 | 2 | -2 |
| `KZnSO4Cl` | 1 | 0 | -1 |
| `KZnSClO4` | 0 | 1 | +1 |
| `Rb2NaYF6` | 1 | 2 | +1 |
| `Sr3(PO4)2` | 1 | 2 | +1 |

## Experiment Hypothesis

- The paper/MRS 357-site claim likely aligns with the Zenodo-linked `original` release rather than the later `BrgochGroup/main` workbook. This is strongly supported by row count and DOI/DataCite linkage, but the authors' intent for the later 358-row workbook is not directly reported in the inspected metadata.
- `KZnSO4Cl` versus `KZnSClO4` may reflect formula normalization or naming revision, but this requires source-level or author-level confirmation before being treated as corrected chemistry.

## Reproduction Implication

- Metrics from the 357-row `original` release and 358-row later `main` release must not be mixed.
- The first exact reproduction target should be the Zenodo-linked `original` tag when the goal is paper-count alignment.
- The later 358-row `BrgochGroup/main` release can still support a processed-data rerun, but it should be reported as a newer public workbook version with non-identical features and labels.
- Provenance-audited literature reconstruction remains approximate because neither inspected workbook exposes row-level DOI/year/source/in-house flags.
