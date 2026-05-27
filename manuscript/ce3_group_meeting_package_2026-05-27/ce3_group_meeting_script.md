
# Ce3+ 5d1 复现组会讲稿

## Slide 1. 本次完成的是 paper-aligned processed-data baseline reproduction

各位老师同学好，这次汇报的主线不是直接宣称“完全复现”，而是先把公开证据链和可复现边界讲清楚。我们目前完成的是基于 Zenodo/DataCite 指向的 `NL0119/Ce_5d1_Prediction@original` 的 357-row public processed-data baseline reproduction。

`Literature Fact`: DOI/DataCite metadata 指向 `tree/original`。  
`Model Inference`: 本地已完成 357-row original baseline rerun 和 metric-gap audit。  
`Writing Guidance`: 这里不使用“完全复现”这个说法，因为公开 processed workbook 缺行级 provenance 字段。

## Slide 2. Source audit 先确定 DOI/GitHub 指向

证据链的关键点是：Zenodo DOI `10.5281/zenodo.14872504` 的 DataCite metadata 指向 `NL0119/Ce_5d1_Prediction/tree/original`，而不是后来的 `BrgochGroup/main` workbook。arXiv 和 MRS 材料提供研究背景和 357-site claim 的上下文，但 conference abstract 不被当成独立实验事实。

`Literature Fact`: DataCite related identifier 指向 original tag。  
`Model Inference`: 这使得 original release 成为 paper-count aligned 的优先复现对象。  
`Caveat`: 本机 Zenodo direct payload/checksum 验证仍被 HTTP 403 阻断。

## Slide 3. 357 vs 358 是 version drift，不能混用指标

版本核查显示，`original` 是 `Training_Set_for_5d1.xlsx`, sheet `RFE44`, `357 x 46`；later `main` 是 `Training_Set_updated_for_5d1_RFE17.xlsx`, `358 x 19`。差异不是空行、重复 header、全重复行或 tester inclusion 可以解释的。

`Model Inference`: 357-row original 对齐 paper/MRS count；358-row main 是 later public workbook。  
`Writing Guidance`: 后续所有指标必须标明 dataset release，不能把 358-row main 的结果拿来解释 original notebook。

## Slide 4. 复现流程是 processed workbook baseline，而不是 raw provenance reconstruction

本地流程读取 released processed workbook，使用 original 5d1 hyperparameters，并以 `Composition` 作为 `LeaveOneGroupOut` group。因此更准确的说法是 leave-one-composition-out。`Predicted CS` 和 `Predicted RP` 在本次作为 frozen released features 使用，没有在每个 fold 内 nested-regenerate。

`Model Inference`: LOGO by Composition 可以避免同 Composition duplicated rows 跨 train/test。  
`Caveat`: 由于没有 DOI/year/source/in-house 字段，它不是 source-aware split。

## Slide 5. Deterministic seed=42 是项目可重复基线

本地 deterministic CPU seed=42 rerun 得到 fold-mean MAE `0.161535` eV，global MAE `0.160836` eV，global RMSE `0.214683` eV，global R2 `0.826486`。同一 split 下，train mean/median baseline 的 fold-mean MAE 约 `0.421` eV，说明 XGBoost baseline 明显优于 naive baseline。

`Model Inference`: seed=42 是可重复项目基线。  
`Caveat`: 它不是最接近 original notebook saved output 的配置。

## Slide 6. Metric-gap audit 显示 seed policy 解释主要差距

Original notebook saved reference 是 fold-mean MAE `0.153388` eV，fold-mean RMSE `0.154257` eV，R2 `0.838004`。最接近的本地结果是 CPU unseeded/default：fold-mean MAE `0.154993` eV，fold-mean RMSE `0.155834` eV，global R2 `0.835515`。这比 seed=42 更接近 notebook saved output。

`Model Inference`: seed policy 解释了大部分 deterministic rerun gap。  
`Experiment Hypothesis`: 剩余 `+0.001605` eV MAE gap 可能来自 XGBoost version、CUDA/CPU behavior 或 platform numerical differences。

## Slide 7. 不能声称 full reproduction 的原因

限制主要有四个：第一，public workbook 缺 DOI/year/source/in-house flags；第二，`Predicted CS/RP` 是 frozen auxiliary model output，没有 nested-regenerate；第三，Zenodo direct payload/checksum 本机 403；第四，authors' CUDA/historical environment 没有完全重建。

`Model Inference`: 这些限制直接来自本地 audit artifacts。  
`Writing Guidance`: 因此结论必须限定为 processed-data baseline reproduction。

## Slide 8. 结论和下一步

当前最稳妥的结论是：357-row original release 是 paper-aligned target；我们已完成 public processed-data XGBoost baseline rerun；closest local rerun 与 notebook saved MAE 的差距约 `+0.001605` eV；seed=42 rerun 适合作为项目可重复基线。下一步如果要提高 claim strength，需要补 source metadata、重建 nested auxiliary CS/RP pipeline，并可选地单独 rerun 358-row later main，但必须明确标注为 later public workbook。

`Writing Guidance`: 结尾要强调“不混用版本、不放大结论、不把模型结果当实验事实”。
