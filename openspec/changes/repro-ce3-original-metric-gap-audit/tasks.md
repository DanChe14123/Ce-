## 1. Gate And Plan

- [x] 1.1 Read project `AGENTS.md`.
- [x] 1.2 Check project memory and active OpenSpec state.
- [x] 1.3 Create `repro-ce3-original-metric-gap-audit` OpenSpec change.
- [x] 1.4 Define controlled metric-gap audit plan.

## 2. Implementation

- [x] 2.1 Add metric-gap sweep support without altering the baseline dataset.
- [x] 2.2 Add CUDA availability detection.
- [x] 2.3 Add outputs for seed sweep, device/parallelism comparison, and summary JSON.

## 3. Execution

- [x] 3.1 Run CPU unseeded/default configuration.
- [x] 3.2 Run CPU seeded sweep for seeds `0`, `1`, `22`, `42`, and `100`.
- [x] 3.3 Run CPU `n_jobs=1` comparison for seed `42`.
- [x] 3.4 Run or explicitly skip CUDA comparison based on local availability.

## 4. Analysis And Report

- [x] 4.1 Compare generated fold-mean metrics against notebook-saved metrics.
- [x] 4.2 Separate fold-mean metrics from global held-out metrics.
- [x] 4.3 Write metric-gap audit report with evidence categories separated.
- [x] 4.4 Update prior original-baseline report with a pointer to the metric-gap audit.

## 5. Verification And Publish

- [x] 5.1 Run Python compile/checks.
- [x] 5.2 Validate OpenSpec.
- [x] 5.3 Commit and push the completed metric-gap audit.
