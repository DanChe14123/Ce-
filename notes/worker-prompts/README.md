# Worker Prompt Pack

Use these prompts for short, read-only worker threads that support `repro-ce3-excitation-band-baseline`.

Recommended order:

1. `literature-provenance-worker.md`
2. `data-table-audit-worker.md`
3. `modeling-code-audit-worker.md`

All workers must:

- Use Chinese unless writing formal English manuscript text.
- Read `AGENTS.md` first.
- Read `openspec/changes/repro-ce3-excitation-band-baseline/{proposal.md,design.md,tasks.md,session-log.md}`.
- Read `notes/source-audit-ce3-excitation-band-baseline.md`.
- Stay read-only: do not edit project files, do not download large files into the repo, do not train models.
- Separate `Literature Fact`, `Model Inference`, `Experiment Hypothesis`, and `Writing Guidance` when relevant.
- Return results using `worker-feedback-template.md`.

