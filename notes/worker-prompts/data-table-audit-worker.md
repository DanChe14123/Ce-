# Data Table Audit Worker Prompt

你是 `Ce³⁺ 荧光粉激发带位置预测复现` 项目的 data-table audit worker。你的任务是只读审计公开训练表的字段、行数、缺失值、潜在泄漏键和与项目 schema 的差距；不修改仓库、不训练模型。

## Required Context

先读取：

- `AGENTS.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/proposal.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/design.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/tasks.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/session-log.md`
- `notes/source-audit-ce3-excitation-band-baseline.md`

## Inputs To Check

Public repository:

- `https://github.com/BrgochGroup/Ce_5d1_Prediction`

Candidate files:

- `Training_Set_updated_for_5d1_RFE17.xlsx`
- `Training_Set_updated_for_CS.xlsx`
- `Training_Set_updated_for_RP.xlsx`
- `MP_Prediction_List.xlsx`
- `elements_5d1_new.xlsx`
- `elements_rp_new.xlsx`
- `tester.xlsx`

Use temporary storage only if downloading small public files is necessary for inspection. Do not place downloaded files under the project repo.

## Tasks

1. For each workbook, report sheets, shape, column names, obvious target/features, and file role.
2. For `Training_Set_updated_for_5d1_RFE17.xlsx`, inspect:
   - total rows
   - non-null target count
   - unique `Composition` count
   - duplicate full rows
   - duplicate compositions
   - repeated composition with different features/targets
   - target unit and whether target is eV or nm
3. Map public columns to the project schema:
   - present
   - absent
   - derivable from code
   - requires manual source check
4. Identify likely leakage keys:
   - repeated `Composition`
   - same host with multiple cation sites
   - polymorphs
   - rows requiring source DOI/year grouping
   - auxiliary predicted features that may require nested validation
5. Produce a minimal data dictionary for the current public training table and a gap list for the provenance-audited table.

## Prohibitions

- Do not train XGBoost.
- Do not rewrite or normalize the workbook.
- Do not infer missing DOI/year/in-house status.
- Do not edit project files.

## Output

Return your answer using `notes/worker-prompts/worker-feedback-template.md`.

