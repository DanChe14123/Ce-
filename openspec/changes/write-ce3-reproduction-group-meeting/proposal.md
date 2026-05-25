## Why

The Ce3+ excitation-band reproduction now has a completed source/version audit, a paper-aligned 357-row original-baseline rerun, and a metric-gap audit. These results need to be converted into group-meeting-ready materials before 2026-05-27 without weakening the evidence boundary: the package should show what was reproduced, what remains limited by public-data provenance, and which claims are only hypotheses.

## What Changes

- Add a group-meeting writing and visualization workflow for the paper-aligned `NL0119/Ce_5d1_Prediction@original` reproduction.
- Generate a Chinese outline, speaking script, key-results table, chart-ready tables, four SVG figure assets, and an editable PPTX deck.
- Keep all metrics separated by aggregation type and unit, and keep `Literature Fact`, `Model Inference`, `Experiment Hypothesis`, and `Writing Guidance` categories visible where confusion is possible.
- Use the completed local evidence artifacts as sources instead of rerunning models or mixing in the later 358-row public workbook as a benchmark.

## Non-Goals

- Do not rerun the later 358-row `BrgochGroup/main` workflow in this change.
- Do not claim a provenance-faithful full reproduction.
- Do not infer row-level DOI/year/source/in-house provenance from composition or workbook fields that do not contain that information.
- Do not treat CUDA/device effects as ruled out unless a usable CUDA comparison is actually run.

## Impact

- Adds OpenSpec state for group-meeting material production.
- Adds a deterministic builder under `scripts/`.
- Adds durable group-meeting manuscript, table, figure, and deck artifacts under `manuscript/`, `results/tables/`, and `results/figures/`.
