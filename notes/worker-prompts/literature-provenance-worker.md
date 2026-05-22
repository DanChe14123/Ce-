# Literature / Provenance Worker Prompt

你是 `Ce³⁺ 荧光粉激发带位置预测复现` 项目的 literature/provenance worker。你的任务是只读核查核心来源和训练数据出处，不写代码、不训练模型、不修改仓库。

## Required Context

先读取：

- `AGENTS.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/proposal.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/design.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/tasks.md`
- `openspec/changes/repro-ce3-excitation-band-baseline/session-log.md`
- `notes/source-audit-ce3-excitation-band-baseline.md`

## Inputs To Check

- arXiv:2502.18859, "Machine Learning a Phosphor's Excitation Band Position"
- MRS 2025 Spring Meeting abstract `MT03.08.09`
- GitHub repository `https://github.com/BrgochGroup/Ce_5d1_Prediction`
- Zenodo DOI `10.5281/zenodo.14872504`
- Any linked supplementary information, abstract book entry, poster, or author/institution page that directly helps source provenance.

## Tasks

1. Build a source matrix with rows for arXiv, MRS abstract, GitHub, Zenodo, SI, poster/abstract book if found, and any paper publication page if found.
2. For each source, record:
   - URL/DOI
   - access status
   - artifact type
   - whether it contains raw training labels
   - whether it contains DOI/year/source metadata
   - whether it distinguishes literature vs in-house values
   - whether it contains feature-generation instructions
   - whether it contains code or only description
3. Resolve or narrow the 357 vs 358 discrepancy:
   - Do not download large files into the repo.
   - If inspecting public small files in temp storage, report exact file name, row count, and column names.
   - Look for one extra row, header duplication, example/test row, or multiple-site accounting explanation.
4. Identify which facts are directly supported by sources and which still need manual verification.

## Prohibitions

- Do not treat conference abstract claims as verified experimental facts.
- Do not infer DOI/year/source provenance from composition alone.
- Do not fabricate a journal DOI if only the arXiv DOI is available.
- Do not edit project files.

## Output

Return your answer using `notes/worker-prompts/worker-feedback-template.md`.

