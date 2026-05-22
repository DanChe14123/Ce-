# Modeling / Code Audit Worker Prompt

你是 `Ce³⁺ 荧光粉激发带位置预测复现` 项目的 modeling/code audit worker。你的任务是只读审计公开 notebook 的建模流程、复现风险和未来执行计划；不要训练模型、不要改代码、不要下载大文件进仓库。

## Required Context

先读取：

- `AGENTS.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/proposal.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/design.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/tasks.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/session-log.md`
- `notes/source-audit-ce3-excitation-band-baseline.md`

## Inputs To Check

- GitHub notebook: `https://github.com/BrgochGroup/Ce_5d1_Prediction/blob/main/Ce%205d1%20descriptor%20and%20models.ipynb`
- GitHub README and file list.
- Public training table names, but only inspect metadata or small temporary copies if needed.

## Tasks

1. Summarize the notebook workflow:
   - imports and dependencies
   - descriptor generation route from Materials Project
   - descriptor generation route from CIF files
   - RP model
   - CS model
   - final 5d1 model
   - output files
2. Extract model settings:
   - XGBoost hyperparameters
   - split/cross-validation strategy
   - group labels
   - metrics
   - target unit conversion
   - GPU/CPU assumptions
   - random seeds, or absence of fixed seeds
3. Identify code-level reproduction risks:
   - variable-name mistakes
   - use of wrong model object in validation
   - missing package versions
   - device-specific behavior
   - Materials Project API requirements
   - non-nested auxiliary predictions
   - possible mismatch between paper description and notebook implementation
4. Define an execution-safe future reproduction checklist:
   - environment lock
   - raw file intake
   - checksum/shape validation
   - no-training smoke test
   - baseline training
   - leakage-aware rerun
   - report artifacts

## Prohibitions

- Do not execute training.
- Do not modify notebook or project code.
- Do not add new dependencies.
- Do not edit project files.

## Output

Return your answer using `notes/worker-prompts/worker-feedback-template.md`.

