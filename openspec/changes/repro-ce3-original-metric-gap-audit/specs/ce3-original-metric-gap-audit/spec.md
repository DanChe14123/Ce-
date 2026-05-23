## ADDED Requirements

### Requirement: Controlled metric-gap audit
The workflow SHALL compare local rerun metrics against original notebook-saved metrics using controlled seed, device, and parallelism settings.

#### Scenario: Metric-gap sweep is executed
- **WHEN** the sweep completes
- **THEN** each run records seed policy, seed value, device, parallelism setting, fold count, row count, fold-mean metrics, global metrics, package versions, and deviation from notebook-saved metrics.

### Requirement: Metric aggregation separation
The workflow SHALL separate fold-mean metrics from global held-out metrics.

#### Scenario: Metrics are summarized
- **WHEN** a report states MAE, RMSE, MSE, or R2
- **THEN** it states whether the metric is fold-mean or global held-out and whether the unit is eV, nm, or unitless.

### Requirement: CUDA availability handling
The workflow SHALL check CUDA availability before attempting GPU comparison.

#### Scenario: CUDA is unavailable
- **WHEN** local CUDA/GPU detection fails
- **THEN** the workflow records the GPU comparison as skipped rather than implying device effects are ruled out.

### Requirement: Evidence-bounded interpretation
The workflow SHALL distinguish isolated causes from unresolved hypotheses.

#### Scenario: Controls do not explain the gap
- **WHEN** seed and parallelism controls do not recover notebook-saved metrics
- **THEN** the workflow labels remaining version/device/environment explanations as hypotheses or unresolved environment drift.
