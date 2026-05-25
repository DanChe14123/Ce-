## ADDED Requirements

### Requirement: Group-meeting evidence package
The workflow SHALL generate a Chinese group-meeting package for the Ce3+ paper-aligned processed-data reproduction.

#### Scenario: Materials are generated
- **WHEN** the material builder completes
- **THEN** it writes an outline, a speaking script, a key-results table, chart-ready tables, four figure assets, and an editable PPTX deck.

### Requirement: Evidence category separation
The package SHALL preserve evidence boundaries in the outline, script, key-results table, and slides.

#### Scenario: A claim is reported
- **WHEN** a claim appears in generated materials
- **THEN** it is attributable to `Literature Fact`, `Model Inference`, `Experiment Hypothesis`, or `Writing Guidance` where category confusion is possible.

### Requirement: Metric reporting discipline
The package SHALL keep metric aggregation and units explicit.

#### Scenario: A metric is reported
- **WHEN** MAE, RMSE, MSE, or R2 is stated
- **THEN** the material states whether it is fold-mean or global held-out and whether the unit is eV, nm, eV2, or unitless.

### Requirement: Version-boundary discipline
The package SHALL keep the 357-row original release and 358-row later public workbook separate.

#### Scenario: Dataset versions are compared
- **WHEN** the materials discuss the 357-vs-358 discrepancy
- **THEN** they state that metrics from these releases must not be mixed and identify the 358-row workbook as a later public workbook rather than the paper-aligned benchmark.

### Requirement: Reproduction limitation disclosure
The package SHALL disclose the limitations that prevent a provenance-faithful full reproduction.

#### Scenario: Reproduction status is summarized
- **WHEN** the conclusion slide or script summarizes completion status
- **THEN** it says the project completed a paper-aligned 357-row public processed-data baseline reproduction and does not claim complete or provenance-faithful full reproduction.
