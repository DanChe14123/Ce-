# Ce3+ Excitation Band Baseline: Source Audit

Date: 2026-05-21
Updated: 2026-05-22 with literature/provenance and data-table worker feedback.

## Literature Fact

- arXiv:2502.18859 is titled "Machine Learning a Phosphor's Excitation Band Position"; it was submitted on 2025-02-26 and lists Nakyung Lee, Malgorzata Sojka, Annie La, Syna Sharma, Sean Kavanagh, Docheon Ahn, David O. Scanlon, and Jakoah Brgoch as authors. Source: https://arxiv.org/abs/2502.18859
- The arXiv abstract states that the model predicts the longest, lowest-energy excitation wavelength for Ce3+ phosphors and was trained on experimental data for 357 Ce3+ cation substitution sites from literature and in-house measurements. Source: https://arxiv.org/abs/2502.18859
- The paper PDF data-availability section states that Ce3+ 5d1 raw training data, feature-generation code, and prediction model are available at `BrgochGroup/Ce_5d1_Prediction`, with Zenodo DOI `10.5281/zenodo.14872504`. Sources: https://arxiv.org/pdf/2502.18859 and https://github.com/BrgochGroup/Ce_5d1_Prediction
- The MRS 2025 Spring Meeting abstract, presentation `MT03.08.09`, is titled "Ensuring Excitation: Machine Learning a Phosphor's Excitation Band Position", scheduled for 2025-04-10, and reports an XGBoost model trained with leave-one-group-out cross-validation on data from 357 cation substitution sites across 337 Ce3+ phosphors from literature and in-house experiments. Source: https://www.mrs.org/meetings-events/annual-meetings/archive/meeting/presentations/view/2025-mrs-spring-meeting/2025-mrs-spring-meeting-4271462
- The GitHub repository `BrgochGroup/Ce_5d1_Prediction` is public and contains a notebook, `Training_Set_updated_for_5d1_RFE17.xlsx`, `Training_Set_updated_for_CS.xlsx`, `Training_Set_updated_for_RP.xlsx`, `MP_Prediction_List.xlsx`, element-property tables, and a tester workbook. Source: https://github.com/BrgochGroup/Ce_5d1_Prediction
- The notebook uses `pymatgen`, `mp_api`, `xgboost`, `scikit-learn`, and Excel workbooks. It can generate descriptors either from Materials Project formula lookup using `MP_API` or from local CIF files in the working directory. Source: https://github.com/BrgochGroup/Ce_5d1_Prediction/blob/main/Ce%205d1%20descriptor%20and%20models.ipynb
- Zenodo DOI `10.5281/zenodo.14872504` resolves through DOI/DataCite metadata to a software record for `NL0119/Ce_5d1_Prediction`, issued on 2025-02-14, version `original`; its DataCite related identifier points to `https://github.com/NL0119/Ce_5d1_Prediction/tree/original`. Sources: https://doi.org/10.5281/zenodo.14872504 and https://api.datacite.org/dois/10.5281/zenodo.14872504
- GitHub reports `NL0119/Ce_5d1_Prediction` tag `original` at commit `49991b75572dd3bf9ac4e5daa6000ac364b39b2d`, committed on 2025-02-12; the tag contains `Training_Set_for_5d1.xlsx` and related model workbooks. Sources: https://api.github.com/repos/NL0119/Ce_5d1_Prediction/commits/original and https://api.github.com/repos/NL0119/Ce_5d1_Prediction/contents?ref=original
- GitHub reports `BrgochGroup/Ce_5d1_Prediction` as a fork of `NL0119/Ce_5d1_Prediction`; the inspected `main` branch commit is `4c7faeb0e92695f08289920ff4882635beff9694`, committed on 2026-03-13. Sources: https://api.github.com/repos/BrgochGroup/Ce_5d1_Prediction and https://api.github.com/repos/BrgochGroup/Ce_5d1_Prediction/commits/main
- The NASSCC 2025 abstract book independently repeats the 357-site / 337-host claim for the same work but does not expose row-level training labels or provenance. Source: https://group.chem.iastate.edu/Kovnir/NASSCC2025/BookofAbstracts.pdf
- A search-indexed NSE Research poster PDF for "Ensuring Excitation: Machine Learning a Phosphor's Excitation Band Position" was found, but it does not provide an inspected row-level source table. Source: https://www.nseresearch.org/2024/posters/Ensuring%20Excitation%20Machine%20Learning%20a%20Phosphor%27s%20Excitation%20Band%20Position.pdf
- No journal DOI was found in inspected publication pages. Confirmed DOI coverage is arXiv DOI `10.48550/arXiv.2502.18859` and Zenodo DOI `10.5281/zenodo.14872504`.

## Source Matrix Summary

| Source | Access | Training labels | Row DOI/year/source metadata | Literature vs in-house flags | Feature/code detail |
| --- | --- | --- | --- | --- | --- |
| arXiv abstract | Accessible | No | Paper-level only | Text says literature + in-house; no row flags | High-level description |
| arXiv PDF + embedded SI | Accessible | No row table found | Paper-level only | Text says literature + in-house; no row flags | Feature classes, methods, SI feature list |
| MRS 2025 MT03.08.09 | Accessible | No | Event/date only | Text says literature + in-house; no row flags | Description only |
| GitHub `NL0119/Ce_5d1_Prediction@original` | Accessible through GitHub API/raw URL; linked from DataCite metadata for Zenodo DOI | Yes, processed `5d1` targets in `Training_Set_for_5d1.xlsx` | No row provenance columns found | No row flags found | Notebook + workbooks |
| GitHub `BrgochGroup/Ce_5d1_Prediction@main` | Accessible | Yes, processed `5d1 Ce` targets in later updated workbook | No row provenance columns found | No row flags found | Notebook + workbooks |
| Zenodo `10.5281/zenodo.14872504` | DOI/DataCite metadata accessible; landing/API/OAI/file routes 403 from this machine | Metadata points to Zenodo-linked GitHub `original` tag; direct Zenodo payload unverified | DOI metadata only; row metadata unverified | Not visible | Related GitHub tag provides code/workbooks; direct Zenodo checksums still blocked |
| NASSCC 2025 abstract book | Accessible | No | Event/book context only | Text says literature + in-house; no row flags | Description only |
| Poster PDF | Search-indexed text found; direct shell HEAD failed TLS | No inspected table | No row metadata | Mentions literature extraction; no row flags | Visual/summary only |
| Institution publication page | Accessible/search-indexed | No | Lists arXiv DOI | No | Description only |

## Model Inference

- Temporary inspection of the Zenodo-linked GitHub tag `NL0119/Ce_5d1_Prediction@original` showed `Training_Set_for_5d1.xlsx` has sheet `RFE44`, shape `(357, 46)`, 357 non-null target values in `5d1`, 330 unique `Composition` values, and no duplicate full rows.
- Temporary inspection of the later public GitHub fork workbook showed `Training_Set_updated_for_5d1_RFE17.xlsx` has shape `(358, 19)`, 358 non-null target values in `5d1 Ce`, 330 unique `Composition` values, and no duplicate full rows.
- Worker cross-check found no duplicated header rows, no all-empty rows, and no overlap between the 3-row `tester.xlsx` example workbook and the public final 5d1 training table.
- The inspected final 5d1 training workbook includes processed target/features but does not include DOI, publication year, source type, raw spectrum provenance, explicit substitution-site labels beyond cation descriptors, or an `is_in_house` flag.
- The 357-vs-358 mismatch is best classified as release/version drift between the Zenodo-linked `original` tag and later `BrgochGroup/main` fork. It is not explained by a blank row, duplicated header row, full duplicate row, or tester-row inclusion artifact.
- Comparing the 357-row `original` table against the 358-row later `main` table found 148 compositions with changed target multisets, 149 exact composition-target pairs only in `original`, and 152 exact composition-target pairs only in the later `main` table. Count changes by composition were `Ca2Si5N8` (+1), `K3Lu(PO4)2` (-2), `KZnSO4Cl` (-1), `KZnSClO4` (+1), `Rb2NaYF6` (+1), and `Sr3(PO4)2` (+1).
- Reproduction level decision: plan `full model reproduction` for the public processed XGBoost baseline, because the final training table, feature-generation notebook, and model workflow are public. Plan `approximate provenance-audit reproduction` for source reconstruction, because the inspected training table does not expose complete source metadata or in-house/literature flags.
- Direct Zenodo record payload and checksums for `10.5281/zenodo.14872504` could not be verified from this machine because Zenodo returned HTTP 403 for landing/API/OAI/export/file routes. DOI/DataCite metadata and the related GitHub `original` tag are accessible non-403 routes.
- `Training_Set_updated_for_5d1_RFE17.xlsx` has 28 duplicated `Composition` values covering 56 rows; all duplicated compositions differ in target and features. Of these, 25/28 differ in coordination number, cation ionic radius, and `chemenv_CN`, and 7/28 also differ in `SGR No.` (`CaCO3`, `CaZrO3`, `Gd(PO3)3`, `K3Lu(PO4)2`, `LiCaBO3`, `LuBO3`, `SrAl2O4`).
- The public prediction list `MP_Prediction_List.xlsx` has 10326 rows and 8101 unique compositions, so candidate row identity must include at least composition plus database/site fields, not composition alone.
- Auxiliary-feature overlap: the 5d1 table shares 118 unique compositions with the centroid-shift table and 55 with the relative-permittivity table.

## Public Workbook Inventory

| file | inspected shape | role |
| --- | --- | --- |
| `Training_Set_for_5d1.xlsx` from `NL0119/Ce_5d1_Prediction@original` | `RFE44`, 357 x 46 | Zenodo-linked original 5d1 training table; target `5d1` in eV; aligns with 357-site paper/abstract count. |
| `Training_Set_updated_for_5d1_RFE17.xlsx` | `Sheet1`, 358 x 19 | Final public processed 5d1 training table; target `5d1 Ce` in eV. |
| `Training_Set_updated_for_CS.xlsx` | `Sheet1`, 158 x 10 | Auxiliary centroid-shift model training table. |
| `Training_Set_updated_for_RP.xlsx` | `reduced`, 1349 x 100; `Sheet1`, 1349 x 8 | Auxiliary relative-permittivity model training table; `Sheet1` appears scratch/auxiliary. |
| `MP_Prediction_List.xlsx` | `Sheet1`, 10326 x 11 | Public candidate prediction table with eV/nm predictions, MP band gap, Debye, and category. |
| `elements_5d1_new.xlsx` | `5d1`, 85 x 7 | Element-property lookup for 5d1 composition descriptors. |
| `elements_rp_new.xlsx` | `rp`, 85 x 18 | Element-property lookup for RP composition descriptors. |
| `tester.xlsx` | `Sheet1`, 3 x 1 | Input template with only `Composition`; no overlap with final training table. |

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
- Baseline model: XGBoost regressor following the public notebook. Keep the Zenodo-linked 357-row `original` release and later 358-row `BrgochGroup/main` release as separate reproduction targets; do not mix metrics across releases.
- Reproducibility controls: record Python/package versions, XGBoost device mode, random seeds, and whether GPU `device='cuda'` is available; if no seed is present in public code, add a documented fixed-seed reproduction branch later rather than altering the source baseline silently.
- Split strategy: reproduce leave-one-group-out using `Composition` as group first; then add stricter group-aware audits by normalized host, structural family, source DOI, and composition family if provenance can be reconstructed.
- Metrics: MAE, RMSE, and R2 for eV-scale training comparison; nm-scale MAE/RMSE around blue LED range because eV-to-nm is nonlinear.
- Baseline comparisons: compare to mean/median target baselines, simple composition-only model, final-feature XGBoost, and if feasible random/group-aware variants.
- Leakage checks: duplicate compositions, multiple substitution sites or polymorphs crossing folds, same source DOI crossing folds, target-derived descriptors, in-house/literature mixing across folds, and predicted-feature reuse from CS/RP auxiliary models.
- Nested-validation risk: `Predicted CS` and `Predicted RP` are auxiliary model outputs used as final 5d1 features. For strict validation, either freeze them as released processed features with clear provenance or regenerate them inside a nested pipeline; do not silently mix the two interpretations.

## Read-Only Code Audit Findings

- The Zenodo-linked `original` notebook uses `LeaveOneGroupOut` with `Composition` as the group for the 5d1 model, so the validation is leave-one-composition-out rather than source-aware or family-aware validation.
- The `original` notebook's saved output for its 5d1 LOGO loop reports eV-scale `avg_mae=0.15338832561753013`, `avg_mse=0.04344782809517265`, `avg_rmse=0.15425705564280934`, and `r2=0.8380042800908163`; these are notebook-saved outputs, not rerun results from this audit.
- The later `BrgochGroup/main` notebook defines a 5d1 `best_model` but its 5d1 LOGO loop calls `CS_model.fit(...)` and `CS_model.predict(...)`. This creates a code-level comparability risk: reproducing the notebook as written and applying the intended `best_model` fix are different tracks.
- Both notebooks hard-code XGBoost `device='cuda'` and do not set an explicit XGBoost estimator seed in the inspected model definitions, so exact reruns must record GPU/CPU mode, package versions, and a seed policy.
- Full details are recorded in `notes/modeling-code-audit-ce3-excitation-band-baseline.md`.

## Literature Reconstruction Plan

- Priority order: public GitHub/Zenodo training workbooks and notebook, paper/SI tables, cited literature tables, original spectra, crystallographic databases, then digitized figures only as low-confidence labels.
- Must manually verify: Ce3+ substitution site, coordination environment, whether the longest excitation/lowest 5d1 peak was selected consistently, measurement type, temperature, source DOI/year, and in-house status.
- Do not treat as strict labels without manual verification: low-resolution or overlapping spectra, unlabeled axes, plots that only show trends, conference abstracts without raw spectra, and spectra where 5d1/5d2 assignment is ambiguous.
- For in-house values already present in the public processed table, keep them usable for model reproduction but mark source provenance as unresolved until the GitHub/Zenodo metadata or paper authors' supporting files identify them.

## Worker Decision

- Literature/provenance and data-table audit workers have reported. Their raw feedback is stored under `notes/worker-feedback/`.
- Do not dispatch writing work yet. Read-only modeling/code audit is complete enough for planning; the next substantive step is to decide whether implementation should first reproduce the paper-aligned 357-row `original` workflow, the later 358-row `main` workflow as written, or the later workflow with an audited `best_model` fix.
- If more workers are used:
  - Literature worker: source matrix and DOI/year/provenance reconstruction; must not treat predictions as experiments.
  - Data worker: schema normalization and missingness/provenance table; must not overwrite raw files.
  - Modeling worker: environment and baseline reproduction; must not train before data provenance and split definitions are frozen.
  - Writing worker: cautious English report sections; must not fabricate citations or source details.
