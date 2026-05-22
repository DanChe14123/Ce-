# Modeling/Code Audit: Ce3+ Excitation Band Baseline

Date: 2026-05-22
Scope: read-only notebook and workbook-structure audit. No model training was performed.

## Literature Fact

- The Zenodo-linked GitHub tag `NL0119/Ce_5d1_Prediction@original` contains `5d1Ce Prediction Model.ipynb`, `Training_Set_for_5d1.xlsx`, auxiliary CS/RP training workbooks, prediction list, tester workbook, element tables, and README. Source: https://api.github.com/repos/NL0119/Ce_5d1_Prediction/contents?ref=original
- The later fork `BrgochGroup/Ce_5d1_Prediction@main` contains `Ce 5d1 descriptor and models.ipynb`, `Training_Set_updated_for_5d1_RFE17.xlsx`, updated auxiliary CS/RP workbooks, MP prediction list, tester workbook, updated element tables, and README. Source: https://api.github.com/repos/BrgochGroup/Ce_5d1_Prediction/contents?ref=main
- The README describes the repository as an XGBoost model for predicting Ce3+ phosphor excitation wavelength and instructs users to provide an `.xlsx` file with a first-column header `Composition`. Sources: https://raw.githubusercontent.com/NL0119/Ce_5d1_Prediction/original/README.md and https://raw.githubusercontent.com/BrgochGroup/Ce_5d1_Prediction/main/README.md
- No `requirements.txt`, environment lockfile, or package-version manifest was found in the inspected root file lists for either release.

## Model Inference

- Parsed notebook structure:

| release | notebook | cells | code cells | extracted code lines |
| --- | --- | ---: | ---: | ---: |
| `NL0119/original` | `5d1Ce Prediction Model.ipynb` | 29 | 19 | 601 |
| `BrgochGroup/main` | `Ce 5d1 descriptor and models.ipynb` | 22 | 12 | 580 |

- The `original` notebook reads `Training_Set_for_5d1.xlsx`, sets `X = array[:,2:46]`, `Y = array[:,1]`, and `Compd = array[:,0]`, then uses `LeaveOneGroupOut().split(X, Y, Compd)`. This is leave-one-composition-out because `Compd` is the `Composition` column.
- The `original` 5d1 model is `XGBRegressor(tree_method='hist', device='cuda', n_estimators=200, learning_rate=0.06, max_depth=9, min_child_weight=8, subsample=0.6, base_score=0.4, colsample_bytree=1, colsample_bylevel=1, colsample_bynode=1, reg_alpha=0, reg_lambda=1)`.
- The `original` notebook output cell stores `avg_mae=0.15338832561753013`, `avg_mse=0.04344782809517265`, `avg_rmse=0.15425705564280934`, and `r2=0.8380042800908163` for the 5d1 LOGO loop. These are notebook-saved outputs, not rerun results from this audit.
- The later `main` notebook reads `Training_Set_updated_for_5d1_RFE17.xlsx`, sets `X = array[:,2:]`, `Y = array[:,1]`, and `Compd = array[:,0]`, then uses `LeaveOneGroupOut().split(X, Y, Compd)`. This is also leave-one-composition-out.
- The later `main` notebook defines a 5d1 `best_model` with `n_estimators=500`, `learning_rate=0.03`, `max_depth=8`, `min_child_weight=8`, `subsample=0.6`, `base_score=0.5`, `colsample_bytree=0.9`, and `reg_lambda=0`, but the 5d1 LOGO loop calls `CS_model.fit(X_train, Y_train)` and `CS_model.predict(X_test)` instead of `best_model.fit(...)` and `best_model.predict(...)`.
- Because of that variable mismatch, any `main` notebook 5d1 cross-validation metrics produced by the current code would evaluate the previously defined `CS_model` estimator configuration on the 5d1 table, while the final full-data prediction step fits `best_model` on all rows. This is a code-level comparability risk and must be quantified before reporting later-workbook benchmark metrics.
- Both releases hard-code `device='cuda'` in XGBoost model definitions. Exact reruns need to record GPU availability, XGBoost version, and whether a CPU fallback changes behavior.
- Neither notebook sets an explicit `seed`/`random_state` inside the XGBoost estimators inspected here. Randomness is only visible in KFold definitions for auxiliary RP/CS models in some sections.
- The `original` release evaluates RP and CS auxiliary models with shuffled `KFold` (`random_state=42` for RP, `random_state=22` for CS), while the later `main` release evaluates RP with shuffled `KFold(random_state=42)` and CS with `LeaveOneGroupOut` by composition.
- Both workflows use `Predicted CS` and `Predicted RP` as 5d1 features. For strict validation, they must be treated either as frozen released features or regenerated inside a nested pipeline; mixing these interpretations would create leakage or metric-comparability ambiguity.
- Both workflows convert predicted 5d1 energy to wavelength using `divider = 1.23984193 * 10**3` and `lambda_nm = divider / energy_eV` in the prediction-output section. Cross-validation metrics in the notebooks are eV-scale metrics unless separately converted after prediction.

## Experiment Hypothesis

- The later `main` notebook's `CS_model`/`best_model` mismatch may materially change 5d1 LOGO metrics relative to the intended final model. This is not quantified yet because this audit did not train or rerun models.
- The `original` release is the more defensible paper-aligned benchmark target because its row count matches the 357-site paper/abstract claim and it is the release pointed to by Zenodo/DataCite metadata.

## Reproduction Guidance

- Keep two separate reproduction tracks:
  - `paper-aligned/original`: use `NL0119/Ce_5d1_Prediction@original`, `Training_Set_for_5d1.xlsx`, 357 rows, 44-feature RFE44 table, and the original notebook's LOGO loop.
  - `later-public/main`: use `BrgochGroup/Ce_5d1_Prediction@main`, `Training_Set_updated_for_5d1_RFE17.xlsx`, 358 rows, 17-feature RFE17 table, and explicitly decide whether to reproduce the notebook as written or apply an audited `best_model` fix.
- Report leave-one-composition-out as such. Do not call it source-aware, family-aware, or provenance-aware validation without additional grouping fields.
- Before any training run, freeze package versions, device mode, random seeds, dataset release, target unit, metric definitions, and whether auxiliary predicted features are frozen or nested.
