# Ce3+ Excitation Band Baseline: Source Audit

Date: 2026-05-21

## Literature Fact

- arXiv:2502.18859 is titled "Machine Learning a Phosphor's Excitation Band Position"; it was submitted on 2025-02-26 and lists Nakyung Lee, Malgorzata Sojka, Annie La, Syna Sharma, Sean Kavanagh, Docheon Ahn, David O. Scanlon, and Jakoah Brgoch as authors. Source: https://arxiv.org/abs/2502.18859
- The arXiv abstract states that the model predicts the longest, lowest-energy excitation wavelength for Ce3+ phosphors and was trained on experimental data for 357 Ce3+ cation substitution sites from literature and in-house measurements. Source: https://arxiv.org/abs/2502.18859
- The paper PDF data-availability section states that Ce3+ 5d1 raw training data, feature-generation code, and prediction model are available at `BrgochGroup/Ce_5d1_Prediction`, with Zenodo DOI `10.5281/zenodo.14872504`. Sources: https://arxiv.org/pdf/2502.18859 and https://github.com/BrgochGroup/Ce_5d1_Prediction
- The MRS 2025 Spring Meeting abstract, presentation `MT03.08.09`, is titled "Ensuring Excitation: Machine Learning a Phosphor's Excitation Band Position", scheduled for 2025-04-10, and reports an XGBoost model trained with leave-one-group-out cross-validation on data from 357 cation substitution sites across 337 Ce3+ phosphors from literature and in-house experiments. Source: https://www.mrs.org/meetings-events/annual-meetings/archive/meeting/presentations/view/2025-mrs-spring-meeting/2025-mrs-spring-meeting-4271462
- The GitHub repository is public and contains a notebook, `Training_Set_updated_for_5d1_RFE17.xlsx`, `Training_Set_updated_for_CS.xlsx`, `Training_Set_updated_for_RP.xlsx`, `MP_Prediction_List.xlsx`, element-property tables, and a tester workbook. Source: https://github.com/BrgochGroup/Ce_5d1_Prediction
- The notebook uses `pymatgen`, `mp_api`, `xgboost`, `scikit-learn`, and Excel workbooks. It can generate descriptors either from Materials Project formula lookup using `MP_API` or from local CIF files in the working directory. Source: https://github.com/BrgochGroup/Ce_5d1_Prediction/blob/main/Ce%205d1%20descriptor%20and%20models.ipynb

## Model Inference

- Temporary inspection of the public GitHub training workbook showed `Training_Set_updated_for_5d1_RFE17.xlsx` has shape `(358, 19)`, 358 non-null target values in `5d1 Ce`, 330 unique `Composition` values, and no duplicate full rows.
- The inspected final 5d1 training workbook includes processed target/features but does not include DOI, publication year, source type, raw spectrum provenance, explicit substitution-site labels beyond cation descriptors, or an `is_in_house` flag.
- The inspected final 5d1 workbook has 358 rows, while the arXiv abstract/MRS abstract describe 357 cation substitution sites. This one-row discrepancy must be resolved before claiming exact reproduction of the reported benchmark.
- Reproduction level decision: plan `full model reproduction` for the public processed XGBoost baseline, because the final training table, feature-generation notebook, and model workflow are public. Plan `approximate provenance-audit reproduction` for source reconstruction, because the inspected training table does not expose complete source metadata or in-house/literature flags.
- Zenodo record `10.5281/zenodo.14872504` could not be verified from this machine because Zenodo returned HTTP 403 for API/browser-like requests. This is an access blocker, not evidence that the record is absent.

## Data Table Schema

Required project schema for reconstructed/audited data:

| field | unit/type | required handling |
| --- | --- | --- |
| `material_id` | string | Stable local id; do not reuse across distinct Ce sites. |
| `host` | formula/string | Host formula without silently changing reported stoichiometry. |
| `activator` | string | Usually `Ce3+`; mark mixed activators explicitly. |
| `co_dopant` | string | Use `not reported` if absent. |
| `ce_substitution_site` | string | Cation site, Wyckoff/coordination if known; `not reported` if unresolved. |
| `crystal_structure` | string | Space group, crystal system, database id where available. |
| `local_coordination` | structured string/columns | CN, polyhedron, bond-length fields; manual check required for ambiguous sites. |
| `composition_descriptors` | numeric columns | Elemental stats, predicted CS/RP, local/structure descriptors; record generation script/version. |
| `longest_excitation_wavelength_nm` | nm | Convert from eV using a documented formula; retain original unit/value. |
| `measurement_source_metadata` | string | PLE, diffuse reflectance, digitized figure, table, in-house, etc. |
| `source_doi` | DOI/string | `not reported` if no DOI. |
| `source_year` | integer/string | `not reported` if no year. |
| `is_in_house` | boolean/string | Required for audit; `not reported` if not recoverable. |
| `units` | string | Record original target unit and converted unit. |
| `notes` | string | Peak-selection rules, uncertainty, exclusions, manual-check notes. |

## Modeling And Validation Plan

- Baseline target: 5d1 energy in eV for training, with wavelength in nm reported using `lambda_nm = 1239.84193 / energy_eV`; project reports MAE/RMSE in eV and converted nm-scale errors where useful.
- Baseline model: XGBoost regressor following the public notebook; first reproduce final-feature training table results, then separately evaluate whether code-level issues or missing seeds affect stability.
- Reproducibility controls: record Python/package versions, XGBoost device mode, random seeds, and whether GPU `device='cuda'` is available; if no seed is present in public code, add a documented fixed-seed reproduction branch later rather than altering the source baseline silently.
- Split strategy: reproduce leave-one-group-out using `Composition` as group first; then add stricter group-aware audits by normalized host, structural family, source DOI, and composition family if provenance can be reconstructed.
- Metrics: MAE, RMSE, and R2 for eV-scale training comparison; nm-scale MAE/RMSE around blue LED range because eV-to-nm is nonlinear.
- Baseline comparisons: compare to mean/median target baselines, simple composition-only model, final-feature XGBoost, and if feasible random/group-aware variants.
- Leakage checks: duplicate compositions, multiple substitution sites or polymorphs crossing folds, same source DOI crossing folds, target-derived descriptors, in-house/literature mixing across folds, and predicted-feature reuse from CS/RP auxiliary models.

## Literature Reconstruction Plan

- Priority order: public GitHub/Zenodo training workbooks and notebook, paper/SI tables, cited literature tables, original spectra, crystallographic databases, then digitized figures only as low-confidence labels.
- Must manually verify: Ce3+ substitution site, coordination environment, whether the longest excitation/lowest 5d1 peak was selected consistently, measurement type, temperature, source DOI/year, and in-house status.
- Do not treat as strict labels without manual verification: low-resolution or overlapping spectra, unlabeled axes, plots that only show trends, conference abstracts without raw spectra, and spectra where 5d1/5d2 assignment is ambiguous.
- For in-house values already present in the public processed table, keep them usable for model reproduction but mark source provenance as unresolved until the GitHub/Zenodo metadata or paper authors' supporting files identify them.

## Worker Decision

- Do not split worker threads yet. The leader should first resolve the one-row count mismatch, Zenodo access, and missing provenance fields.
- Split later only after the source matrix is frozen:
  - Literature worker: source matrix and DOI/year/provenance reconstruction; must not treat predictions as experiments.
  - Data worker: schema normalization and missingness/provenance table; must not overwrite raw files.
  - Modeling worker: environment and baseline reproduction; must not train before data provenance and split definitions are frozen.
  - Writing worker: cautious English report sections; must not fabricate citations or source details.
