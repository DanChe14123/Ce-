# Project Identity

- `project_name`: `Ce³⁺ 荧光粉激发带位置预测复现`
- `project_type`: `research`
- `project_goal`: `复现和审计 Ce3+ 掺杂无机荧光粉最长激发波长/激发带位置预测工作，围绕公开论文、会议摘要、可获得数据和可重建文献数据，建立可追溯的数据表、特征工程、XGBoost 或同类基线模型、交叉验证、泄漏检查和结果解释流程。`
- `primary_scope`: `为 Ce3+ 荧光粉激发带位置预测复现提供长期研究支持，包括核心论文和会议材料核查、Ce3+ 替位点数据重建或获取、字段字典与单位统一、结构/组成/局域环境特征整理、XGBoost 基线复现、leave-one-group-out 或 group-aware split 设计、随机种子和评价指标记录、数据泄漏检查、候选材料预测解释、与 IPOP/稀土发光材料数据驱动综述项目的可比性整理，以及英文复现报告或论文段落写作；不包含湿实验执行，不把模型预测或会议摘要信息当作已验证实验结论，不替代原文献和原始光谱核查。`
- Store project-specific truth here. Keep global working rules in `C:\Users\admin\.codex\AGENTS.md`.

<!-- managed-project:start -->
# Directory Conventions

- `data/raw/`: immutable source data copied from papers, exports, or instruments.
- `data/processed/`: cleaned or transformed datasets ready for analysis.
- `src/`: reusable analysis, training, and evaluation code.
- `scripts/`: one-off project entrypoints and operational helpers.
- `notes/`: literature notes, scratch findings, and analysis notes.
- `reproductions/`: paper-specific reproduction artifacts.
- `experiments/`: experiment plans, ablations, and execution notes.
- `results/figures/`: durable figures for reports and manuscripts.
- `results/tables/`: durable result tables and structured outputs.
- `manuscript/`: outlines, draft sections, and response material.
- `openspec/`: authoritative long-task state.

# Research Defaults

- Prefer these canonical fields when the task supports them:
  - `material_id`
  - `host`
  - `activator`
  - `co_dopant`
  - `structure_family`
  - `synthesis_method`
  - `excitation_nm`
  - `emission_nm`
  - `fwhm_nm`
  - `lifetime_us`
  - `plqy`
  - `temperature_k`
  - `model_target`
  - `source_doi`
  - `source_year`
  - `notes`
- If a field is missing, write `not reported` instead of inferring it silently.

# Type Entry Rules

- Use `research-repro-start` before any paper reproduction, baseline reproduction, model rerun, or result recreation.
- Use `research-task-resume` before continuing a paused long-running task in a new thread.
- Default change names are:
  - `repro-*`
  - `study-*`
  - `write-*`
- Reproduction work is gated:
  - do not start analysis or implementation until a matching `repro-*` change exists
  - if no matching change exists, create one through the `openspec-propose` workflow

# Shared Project Memory Rules

- If `.codex/project-memory.json` exists, use `project-memory-read` before:
  - starting a new long-running task
  - resuming paused work
  - high-risk design, planning, or writing
- Use `project-memory-write` only after a stable fact is evidence-backed and explicitly approved for retention.
- Supported project memory operations are:
  - search project memory
  - list recent facts
  - add stable fact
  - update/delete incorrect fact
- Only write project memory after these four checks all pass:
  - it is a stable fact, not a task-process item
  - it is likely to be reused across future threads
  - it is evidence-backed or explicitly confirmed by the user
  - it can be expressed as one short durable fact rather than a broad summary
- Preferred project memory categories:
  - long-lived project rules
  - validated project decisions
  - evidence-backed stable facts
  - durable rejected constraints
  - confirmed project-relevant user preferences
- Never write current progress, blockers, next actions, temporary TODOs, broad session summaries, speculative hypotheses, or secrets into project memory.

# OpenSpec Workflow

- Each active change must maintain:
  - `proposal.md`
  - `design.md`
  - `tasks.md`
  - `session-log.md`
- If `session-log.md` is missing, create it from `openspec/templates/session-log-template.md`.
- Before starting new long-running work in a thread:
  - read this `AGENTS.md`
  - inspect active `OpenSpec` changes
  - read the active change `session-log.md` if one exists

# Session Log Format

- `1. What Was Completed`
- `2. Evidence-Backed Conclusions`
- `3. Current Blockers`
- `4. First Next Action`

# Reporting Rules

- Separate `Literature Fact`, `Model Inference`, `Experiment Hypothesis`, and `Writing Guidance` whenever confusion is possible.
- Do not write unsupported claims into summaries, manuscripts, or memory candidates.
<!-- managed-project:end -->

