# Ce3+ 5d1 复现组会材料包

Date: 2026-05-27

这个文件夹集中放置组会汇报需要用到的成品材料、图表、表格和核查证据。

## 直接汇报文件

- `ce3_group_meeting_reproduction_deck.pptx`: 8 页组会 PPT。
- `ce3_group_meeting_outline.md`: 汇报提纲。
- `ce3_group_meeting_script.md`: 中文讲稿。

## 图表

位于 `figures/`：

- `ce3_group_meeting_version_timeline.svg`: source/version timeline。
- `ce3_group_meeting_dataset_comparison.svg`: 357 original vs 358 main dataset comparison。
- `ce3_group_meeting_pipeline.svg`: reproduction pipeline diagram。
- `ce3_group_meeting_metric_gap_seed_sweep.svg`: metric gap seed sweep plot。

## 表格

位于 `tables/`：

- `ce3_group_meeting_key_results.csv`: 组会核心结论表，含 evidence category、unit、source artifact 和 caveat。
- `ce3_group_meeting_version_timeline.csv`: timeline 图表数据。
- `ce3_group_meeting_dataset_comparison.csv`: dataset comparison 图表数据。
- `ce3_group_meeting_metric_gap_plot.csv`: metric gap plot 图表数据。

## 核查证据

位于 `evidence/`，用于组会问答或追溯来源：

- `zenodo-github-version-audit.md`
- `modeling-code-audit-ce3-excitation-band-baseline.md`
- `ce3_original_baseline_report.md`
- `ce3_original_metric_gap_report.md`
- `summary.json`
- `metric_gap_runs.csv`

## 汇报边界

可以说：完成 paper-aligned 357-row public processed-data baseline reproduction。

不要说：完成 provenance-faithful full reproduction，或把模型预测、会议摘要、缺证据推断当成实验事实。
