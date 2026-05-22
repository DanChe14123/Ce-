## 1. Startup State

- [x] 1.1 Read project `AGENTS.md`.
- [x] 1.2 Confirm project memory status and search for relevant stable facts.
- [x] 1.3 Inspect active OpenSpec changes.
- [x] 1.4 Create `repro-ce3-excitation-band-baseline` change with proposal, design, tasks, specs, and session log.

## 2. Source Audit

- [x] 2.1 Verify arXiv:2502.18859 metadata, abstract, links, and available files.
- [x] 2.2 Verify the corresponding MRS 2025 abstract and record claims separately from experimental facts.
- [x] 2.3 Search for public training tables, supplementary information, code repositories, and feature-generation descriptions.
- [x] 2.4 Classify the reproduction level as full or approximate with evidence-backed rationale.

## 3. Data Reconstruction Plan

- [x] 3.1 Freeze the initial Ce3+ schema and provenance fields.
- [x] 3.2 Define which fields require manual literature or crystallographic verification.
- [x] 3.3 Define which figure-derived values are too uncertain for strict benchmark labels.

## 4. Modeling And Validation Plan

- [x] 4.1 Define XGBoost or comparable baseline inputs, target, seeds, and output artifacts.
- [x] 4.2 Define train/validation/test or group-aware split strategy.
- [x] 4.3 Define metric units, baseline comparisons, and leakage checks.

## 5. Reporting And Handoff

- [x] 5.1 Record first-phase findings in `session-log.md`.
- [x] 5.2 Decide whether worker threads are needed after core source triage.
- [ ] 5.3 Produce the first leader checkpoint with evidence-backed conclusions, blockers, and first next action.
