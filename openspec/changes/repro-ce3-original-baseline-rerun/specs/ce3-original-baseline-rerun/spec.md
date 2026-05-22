## ADDED Requirements

### Requirement: Paper-aligned original release selection
The reproduction workflow SHALL use the Zenodo/DataCite-linked `NL0119/Ce_5d1_Prediction@original` release as the first implementation target.

#### Scenario: Baseline artifacts are fetched
- **WHEN** the workflow downloads public artifacts
- **THEN** it records the `original` release URL, local path, byte size, and SHA256 for each artifact.

### Requirement: 357-row 5d1 workbook profiling
The workflow SHALL profile the `Training_Set_for_5d1.xlsx` workbook before model training.

#### Scenario: Workbook is loaded
- **WHEN** the `RFE44` sheet is parsed
- **THEN** the workflow records row count, column count, target column, target unit, required feature columns, duplicate full rows, empty rows, unique composition count, and duplicated composition groups.

### Requirement: Leave-one-composition-out baseline
The workflow SHALL reproduce the processed 5d1 baseline using `LeaveOneGroupOut` grouped by `Composition`.

#### Scenario: Cross-validation is run
- **WHEN** the model is evaluated
- **THEN** each row's composition group appears in either train or test for a fold, never both.

### Requirement: Metric and unit separation
The workflow SHALL report energy-scale and wavelength-scale metrics separately.

#### Scenario: Metrics are written
- **WHEN** MAE, MSE, RMSE, or R2 is reported
- **THEN** the workflow states whether the metric is in eV, nm, or unitless.

### Requirement: Leakage and provenance limitations
The workflow SHALL document split leakage checks and provenance limitations.

#### Scenario: Source-aware split cannot be run
- **WHEN** DOI/year/source/in-house fields are absent from the public workbook
- **THEN** the workflow records source-aware leakage as not auditable rather than inferring source groups.
