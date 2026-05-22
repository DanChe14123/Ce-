## 1. Gate And Setup

- [x] 1.1 Read project `AGENTS.md`.
- [x] 1.2 Check project memory and active OpenSpec state.
- [x] 1.3 Create `repro-ce3-original-baseline-rerun` OpenSpec change.
- [x] 1.4 Define paper-aligned implementation plan.

## 2. Data Fetch And Provenance

- [x] 2.1 Add a small, traceable fetch script for `NL0119/Ce_5d1_Prediction@original` artifacts.
- [x] 2.2 Generate raw-artifact manifest with URLs, SHA256, byte sizes, and local paths.
- [x] 2.3 Generate dataset profile for the 357-row `RFE44` 5d1 workbook.

## 3. Baseline Reproduction

- [x] 3.1 Implement reusable loader, profiling, and metric utilities.
- [x] 3.2 Implement paper-aligned leave-one-composition-out XGBoost baseline.
- [x] 3.3 Implement mean/median fold baselines.
- [x] 3.4 Record eV and nm metrics without mixing units.

## 4. Leakage And Reporting

- [x] 4.1 Generate duplicate composition and group-size leakage audit tables.
- [x] 4.2 Record missing provenance blockers for source-aware split.
- [x] 4.3 Write a concise reproduction report with Literature Fact, Model Inference, and Experiment Hypothesis separated.

## 5. Verification And Publish

- [x] 5.1 Run the fetch/profile path.
- [x] 5.2 Run the baseline reproduction path or record dependency blocker.
- [x] 5.3 Validate OpenSpec.
- [x] 5.4 Commit and push the completed second-stage artifacts.
