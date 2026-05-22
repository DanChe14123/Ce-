# Data Table Audit Worker Feedback

Date: 2026-05-22

## Worker Role

- Role: Data-table audit worker
- Files/pages inspected: project `AGENTS.md`, active OpenSpec change files, `notes/source-audit-ce3-excitation-band-baseline.md`, `notes/worker-prompts/worker-feedback-template.md`, `BrgochGroup/Ce_5d1_Prediction`, and 7 downloaded `.xlsx` files in `%TEMP%`.
- Project files edited: none. Models trained: none.

## Literature Fact

- The public GitHub repository lists the requested notebook and workbooks: `Ce 5d1 descriptor and models.ipynb`, `Training_Set_updated_for_5d1_RFE17.xlsx`, `Training_Set_updated_for_CS.xlsx`, `Training_Set_updated_for_RP.xlsx`, `MP_Prediction_List.xlsx`, `elements_5d1_new.xlsx`, `elements_rp_new.xlsx`, and `tester.xlsx`.
- The repository README describes the project as an XGBoost model predicting Ce3+ phosphor excitation wavelength. Source: https://github.com/BrgochGroup/Ce_5d1_Prediction
- The notebook derives `Predicted RP` and `Predicted CS` from auxiliary XGBoost models, then uses them as features in the 5d1 model. It converts predicted 5d1 energy to nm with `1239.84193 / energy`.

## Model Inference

| file | sheets / shape | columns / role |
| --- | --- | --- |
| `Training_Set_updated_for_5d1_RFE17.xlsx` | `Sheet1`, 358 x 19 | Final public 5d1 training table. Target: `5d1 Ce`; key features: `Predicted CS`, `Predicted RP`, coordination/site descriptors, `SGR No.`, selected composition descriptors. |
| `Training_Set_updated_for_CS.xlsx` | `Sheet1`, 158 x 10 | Auxiliary centroid-shift training table. Target: `Centroid shift (6.352-G)`; features include `Relative permittivity`, `Coord. no.`, `Rm`, `DeltaR (Rm-RCe)`, bond/electronegativity/polarizability/condensation fields. |
| `Training_Set_updated_for_RP.xlsx` | `reduced`, 1349 x 100; `Sheet1`, 1349 x 8 | Main RP target: `dielectric constant`; 100-column reduced sheet combines formula descriptors plus structural fields. `Sheet1` appears scratch/auxiliary and has many `Unnamed`/missing columns. |
| `MP_Prediction_List.xlsx` | `Sheet1`, 10326 x 11 | Prediction candidates with `Composition`, `Database IDs`, `Central Cation`, coordination descriptors, predicted 5d1 in eV and nm, `MP Eg`, `Debye`, `Category`. |
| `elements_5d1_new.xlsx` | `5d1`, 85 x 7 | Element-property lookup for 5d1 composition descriptors. |
| `elements_rp_new.xlsx` | `rp`, 85 x 18 | Element-property lookup for RP descriptors. |
| `tester.xlsx` | `Sheet1`, 3 x 1 | Input template with only `Composition`. |

`Training_Set_updated_for_5d1_RFE17.xlsx` audit:

| check | result |
| --- | --- |
| total rows / columns | 358 / 19 |
| target column | `5d1 Ce` |
| non-null target count | 358 |
| unique `Composition` count | 330 |
| duplicate full rows | 0 |
| duplicated `Composition` values | 28 values, 56 rows, 28 extra rows |
| repeated composition with different target | all 28 duplicated compositions |
| repeated composition with different features | all 28 duplicated compositions |
| target unit | eV, not nm; range is 2.28-4.98 and notebook separately converts eV to nm |

- Repeated-composition risk details: 25/28 duplicated compositions differ in coordination number, cation ionic radius, and `chemenv_CN`; 7/28 also differ in `SGR No.`: `CaCO3`, `CaZrO3`, `Gd(PO3)3`, `K3Lu(PO4)2`, `LiCaBO3`, `LuBO3`, `SrAl2O4`.
- Auxiliary overlap: 5d1 shares 118 unique compositions with the CS table and 55 with the RP table. `MP_Prediction_List.xlsx` has 10326 rows but only 8101 unique compositions, so prediction-row identity must use at least composition plus database/site fields.
- Minimal 5d1 data dictionary: all 19 columns have 0 missing values. `Composition` is formula string; `5d1 Ce` is eV target; `Predicted CS`/`Predicted RP` are generated auxiliary model features; `coordination_number`, `cation_ionic_radius`, `dopant_ionic_radius`, `chemenv_CN`, `SGR No.` describe local/structural environment; remaining columns are selected averaged/difference/max/min/std composition descriptors.

## Experiment Hypothesis

- The 358-row public table versus 357-site paper/abstract count mismatch may come from an extra duplicated composition, site, polymorph, or table revision, but this is not verified.
- Duplicate `Composition` rows likely represent distinct substitution sites and/or polymorphs, but the final 5d1 workbook lacks `Central Cation`, `Database IDs`, and source provenance needed to prove row identity.

## Missing Evidence

- Absent from final 5d1 table: `material_id`, explicit host/site id, `Central Cation`, `Database IDs`, activator column, co-dopant, synthesis method, DOI, source year, source type, in-house/literature flag, measurement metadata, raw excitation wavelength in nm, emission/FWHM/lifetime/PLQY/temperature, and notes.
- Derivable from code: composition descriptors, MP/CIF structural descriptors, auxiliary `Predicted CS`/`Predicted RP`, and eV-to-nm conversion.
- Requires manual source check: DOI/year grouping, in-house status, exact Ce substitution site, whether repeated formulas are polymorphs or sites, and original spectral peak selection.

## Risks

- Leakage/split risk: `Composition` is necessary but insufficient as the only grouping key for DOI/source, polymorph, and site-level leakage.
- Nested-validation risk: `Predicted CS` and `Predicted RP` are model-generated features and should be frozen with documented provenance or regenerated inside a nested pipeline.
- Reporting risk: current public table supports processed model reproduction better than provenance-audited literature reconstruction.
- Unit risk: model target is eV; any nm metrics require explicit nonlinear conversion.

## Recommended Next Action

- Build a source matrix for the 358 5d1 rows using row identity fields: `Composition`, `SGR No.`, coordination descriptors, target eV, and any recoverable `Central Cation`/`Database IDs`; resolve the 357-vs-358 mismatch before training.

