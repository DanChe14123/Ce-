## Context

The completed evidence base is:

- `notes/zenodo-github-version-audit.md`
- `notes/modeling-code-audit-ce3-excitation-band-baseline.md`
- `reproductions/ce3_original_baseline/report.md`
- `reproductions/ce3_original_metric_gap/report.md`
- `results/tables/ce3_original_baseline/summary.json`
- `results/tables/ce3_original_metric_gap/metric_gap_runs.csv`

The group-meeting story is source audit -> version audit -> processed baseline rerun -> metric-gap audit -> leakage/provenance limitation.

## Decisions

- Treat `NL0119/Ce_5d1_Prediction@original`, 357 rows, sheet `RFE44`, as the paper-aligned reproduction object.
- Treat `BrgochGroup/Ce_5d1_Prediction@main`, 358 rows, as a later public workbook for comparison only, not a benchmark mixed with original metrics.
- Report notebook-saved metrics, closest local CPU unseeded/default rerun metrics, and deterministic CPU seed-42 metrics as separate rows.
- Use eV metrics by default. Mention nm only when explicitly labeled.
- Present LOGO as leave-one-composition-out, not source-aware or provenance-aware validation.
- Use the public processed workbook interpretation: `Predicted CS` and `Predicted RP` are frozen released auxiliary features, not nested-regenerated features.

## Outputs

- `scripts/build_ce3_group_meeting_materials.py`
- `results/tables/ce3_group_meeting_key_results.csv`
- `results/tables/ce3_group_meeting_version_timeline.csv`
- `results/tables/ce3_group_meeting_dataset_comparison.csv`
- `results/tables/ce3_group_meeting_metric_gap_plot.csv`
- `results/figures/ce3_group_meeting_version_timeline.svg`
- `results/figures/ce3_group_meeting_dataset_comparison.svg`
- `results/figures/ce3_group_meeting_pipeline.svg`
- `results/figures/ce3_group_meeting_metric_gap_seed_sweep.svg`
- `manuscript/ce3_group_meeting_outline.md`
- `manuscript/ce3_group_meeting_script.md`
- `manuscript/ce3_group_meeting_reproduction_deck.pptx`

## Deck Design

- Build an 8-slide editable deck in Chinese.
- Use a restrained research presentation system: white/near-white background, dark text, one blue-green accent, and one amber warning/accent color.
- Use editable text, tables, timelines, and diagrams. Do not use official logos, pseudo-logos, or unverified identity assets.
- Each slide title is a claim and each footer/source note points to a local evidence artifact or verified URL.

## Risks

- PPTX rendering can fail if the presentation runtime is unavailable; in that case, the Markdown/script/tables/SVGs remain the minimum usable group-meeting package and the blocker must be recorded.
- Evidence categories may blur in slides if titles are too short; source notes and labels must preserve whether each item is literature fact, model inference, hypothesis, or writing guidance.
