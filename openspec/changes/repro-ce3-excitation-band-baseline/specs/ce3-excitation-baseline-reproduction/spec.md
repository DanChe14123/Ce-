## ADDED Requirements

### Requirement: Source availability audit
The reproduction workflow SHALL verify the availability of the target paper, conference abstract, supplementary information, code, training tables, public datasets, and feature-generation descriptions before model implementation begins.

#### Scenario: Public artifacts are audited
- **WHEN** first-phase source triage is completed
- **THEN** the workflow records which artifacts exist, which are missing, and which claims are directly supported by each source.

### Requirement: Reproduction level classification
The reproduction workflow SHALL classify the effort as `full reproduction` only when complete training labels and sufficient feature-generation details are publicly available; otherwise it SHALL classify the effort as `approximate reproduction`.

#### Scenario: In-house or missing training data is detected
- **WHEN** any required training labels, feature definitions, or source tables are inaccessible
- **THEN** the workflow classifies the effort as `approximate reproduction` and records the expected effect on metric comparability and conclusion strength.

### Requirement: Traceable Ce3+ data schema
The reconstructed dataset SHALL include explicit fields for material identity, host, activator, co-dopants, Ce3+ substitution site, crystal structure, local coordination, composition descriptors, longest excitation wavelength in nm, measurement/source metadata, DOI/year, in-house status, units, and notes.

#### Scenario: A literature field is absent
- **WHEN** a required field is not reported in the source artifact
- **THEN** the dataset records `not reported` rather than inferring the value silently.

### Requirement: Group-aware baseline validation
The modeling plan SHALL define an XGBoost or comparable baseline with fixed seeds, train/validation/test or group-aware split strategy, nm-scale metrics, baseline comparisons, and leakage checks.

#### Scenario: Potential leakage groups exist
- **WHEN** host, structural family, composition family, or literature source can appear across multiple splits
- **THEN** the workflow uses or evaluates a group-aware split and documents remaining leakage risk.

### Requirement: Evidence category separation
The reporting workflow SHALL separate Literature Fact, Model Inference, Experiment Hypothesis, and Writing Guidance whenever those categories could be confused.

#### Scenario: A conference abstract reports candidate predictions
- **WHEN** an abstract, model output, or prediction claim is summarized
- **THEN** the workflow does not present it as verified experimental evidence unless an original experimental source is available.
