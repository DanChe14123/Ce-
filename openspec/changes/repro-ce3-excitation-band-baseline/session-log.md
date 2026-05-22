# 1. What Was Completed

- [x] Created OpenSpec change `repro-ce3-excitation-band-baseline`.
- [x] Added `proposal.md`, `design.md`, `tasks.md`, and a capability spec for the Ce3+ excitation-band baseline reproduction.
- [x] Verified arXiv:2502.18859 metadata and extracted paper/SI method details from the arXiv PDF.
- [x] Verified the MRS 2025 Spring Meeting abstract page for the corresponding presentation.
- [x] Verified the public GitHub repository `BrgochGroup/Ce_5d1_Prediction` and inspected small training workbooks in a temporary directory.
- [x] Recorded first-phase findings in `notes/source-audit-ce3-excitation-band-baseline.md`.
- [x] Prepared read-only worker prompts under `notes/worker-prompts/` for literature/provenance, data-table audit, and modeling/code audit workers.

# 2. Evidence-Backed Conclusions

- [x] Project memory is connected under project memory id `ce3-63aa6e88`.
- [x] Active OpenSpec changes were empty before this change was created.
- [x] The paper data-availability section points to public GitHub repository `https://github.com/BrgochGroup/Ce_5d1_Prediction` and Zenodo DOI `10.5281/zenodo.14872504`.
- [x] The public GitHub repository contains a notebook, final 5d1 training workbook, auxiliary CS/RP training workbooks, prediction list, element tables, and tester workbook.
- [x] Temporary inspection found `Training_Set_updated_for_5d1_RFE17.xlsx` has 358 rows, 19 columns, 358 non-null `5d1 Ce` targets, 330 unique compositions, and no full duplicate rows.
- [x] The inspected final 5d1 workbook does not expose DOI/year/source/in-house provenance columns, so provenance-audited reconstruction remains approximate until source metadata are recovered.
- [x] Reproduction level is split: full model reproduction is feasible for the public processed XGBoost baseline; provenance-audited literature reconstruction remains approximate/reconstructed.

# 3. Current Blockers

- [ ] Zenodo DOI `10.5281/zenodo.14872504` returned HTTP 403 from this machine and needs verification through another route.
- [ ] The paper/MRS abstracts describe 357 Ce3+ cation substitution sites, while the inspected GitHub final 5d1 workbook has 358 rows; this count mismatch needs resolution.
- [ ] Source DOI/year, measurement-source, and in-house/literature flags are not available in the inspected processed 5d1 training workbook.
- [ ] Exact package versions and XGBoost seed/device reproducibility are not yet frozen.

# 4. First Next Action

- [ ] Create a source matrix for the GitHub workbooks and notebook, then resolve the 357-vs-358 row mismatch before any model training.
