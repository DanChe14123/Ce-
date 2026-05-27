
# Ce3+ 5d1 激发带位置预测复现组会提纲

## 核心主线

source audit -> version audit -> processed baseline rerun -> metric gap audit -> leakage/provenance limitation

## 一句话结论

完成的是 **paper-aligned 357-row public processed-data baseline reproduction**。目前不能声称完成 provenance-faithful full reproduction，因为公开 workbook 缺少 DOI/year/source/in-house 等行级 provenance 字段，且 `Predicted CS/RP` 未在 nested CV 内重生成。

## Literature Fact

- Zenodo DOI `10.5281/zenodo.14872504` 的 DataCite metadata 指向 `NL0119/Ce_5d1_Prediction/tree/original`。
- `NL0119/Ce_5d1_Prediction@original` 包含 `Training_Set_for_5d1.xlsx` 和原始 notebook。
- `BrgochGroup/Ce_5d1_Prediction@main` 是 later public fork/update，不能和 original 指标混用。

## Model Inference

- `original` workbook: `357 x 46`, sheet `RFE44`, target `5d1` eV, `330` unique compositions。
- later `main` workbook: `358 x 19`，是版本漂移，不是 blank row/header/tester inclusion 可以解释的差异。
- LOGO 实际是 `LeaveOneGroupOut` grouped by `Composition`，应称为 leave-one-composition-out。
- Notebook-saved reference: fold-mean MAE `0.153388` eV, fold-mean RMSE `0.154257` eV, R2 `0.838004`。
- Closest local rerun: CPU unseeded/default fold-mean MAE `0.154993` eV, fold-mean RMSE `0.155834` eV, global R2 `0.835515`。
- Deterministic project baseline: CPU seed=42 fold-mean MAE `0.161535` eV, global MAE `0.160836` eV, global R2 `0.826486`。

## Experiment Hypothesis

- Notebook-saved output 可能来自 unseeded/default 或更接近 seed=0 的 XGBoost 路径。
- 剩余 `+0.001605` eV fold-mean MAE gap 可能来自 XGBoost version、CUDA/CPU behavior 或 platform numerical differences；本机 CUDA 未成功测试，因此不能把 device effect 排除。

## Writing Guidance

- 可以说：完成 paper-aligned 357-row public processed-data baseline reproduction。
- 不要说：完全复现、provenance-faithful full reproduction、source-aware validation。
- 组会结尾建议把下一步限定为三件事：补 row-level provenance、nested-regenerate CS/RP auxiliary features、可选 later-main quick rerun 并严格标注为 later public workbook。

## Slide Plan

1. Thesis: reproduced processed baseline, not full provenance-faithful reproduction.
2. Source audit timeline: arXiv/MRS/DataCite/GitHub/Zenodo linkage.
3. Version audit: 357 original vs 358 main.
4. Pipeline: workbook -> frozen features -> LOGO by composition -> separated metrics.
5. Baseline rerun: seed=42 deterministic metrics and naive baselines.
6. Metric-gap audit: notebook saved vs CPU unseeded/default vs seed sweep.
7. Leakage/provenance limits: missing source fields and non-nested auxiliary features.
8. Takeaways: what is defensible now and what blocks stronger claims.

## Deliverables

- Key results table: `results/tables/ce3_group_meeting_key_results.csv`
- Figure assets: `results/figures/ce3_group_meeting_version_timeline.svg`, `results/figures/ce3_group_meeting_dataset_comparison.svg`, `results/figures/ce3_group_meeting_pipeline.svg`, `results/figures/ce3_group_meeting_metric_gap_seed_sweep.svg`
- Speaking script: `manuscript/ce3_group_meeting_script.md`
