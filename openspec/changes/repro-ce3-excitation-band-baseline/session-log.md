# 1. What Was Completed

- [x] Created OpenSpec change `repro-ce3-excitation-band-baseline`.
- [x] Added `proposal.md`, `design.md`, `tasks.md`, and a capability spec for the Ce3+ excitation-band baseline reproduction.
- [x] Verified arXiv:2502.18859 metadata and extracted paper/SI method details from the arXiv PDF.
- [x] Verified the MRS 2025 Spring Meeting abstract page for the corresponding presentation.
- [x] Verified the public GitHub repository `BrgochGroup/Ce_5d1_Prediction` and inspected small training workbooks in a temporary directory.
- [x] Recorded first-phase findings in `notes/source-audit-ce3-excitation-band-baseline.md`.
- [x] Prepared read-only worker prompts under `notes/worker-prompts/` for literature/provenance, data-table audit, and modeling/code audit workers.
- [x] Integrated literature/provenance and data-table worker results into `notes/source-audit-ce3-excitation-band-baseline.md`.
- [x] Stored raw worker feedback under `notes/worker-feedback/`.
- [x] Verified DOI/DataCite metadata for Zenodo DOI `10.5281/zenodo.14872504` and traced it to GitHub repository `NL0119/Ce_5d1_Prediction` tag `original`.
- [x] Compared the Zenodo-linked 357-row `original` 5d1 workbook against the later 358-row `BrgochGroup/main` workbook.
- [x] Added version-audit note `notes/zenodo-github-version-audit.md`.
- [x] Completed read-only modeling/code audit and added `notes/modeling-code-audit-ce3-excitation-band-baseline.md`.

# 2. Evidence-Backed Conclusions

- [x] Project memory is connected under project memory id `ce3-63aa6e88`.
- [x] Active OpenSpec changes were empty before this change was created.
- [x] The paper data-availability section points to public GitHub repository `https://github.com/BrgochGroup/Ce_5d1_Prediction` and Zenodo DOI `10.5281/zenodo.14872504`.
- [x] The public GitHub repository contains a notebook, final 5d1 training workbook, auxiliary CS/RP training workbooks, prediction list, element tables, and tester workbook.
- [x] Temporary inspection found `Training_Set_updated_for_5d1_RFE17.xlsx` has 358 rows, 19 columns, 358 non-null `5d1 Ce` targets, 330 unique compositions, and no full duplicate rows.
- [x] The inspected final 5d1 workbook does not expose DOI/year/source/in-house provenance columns, so provenance-audited reconstruction remains approximate until source metadata are recovered.
- [x] Reproduction level is split: full model reproduction is feasible for the public processed XGBoost baseline; provenance-audited literature reconstruction remains approximate/reconstructed.
- [x] Worker cross-check found no duplicated header rows, no all-empty rows, and no overlap between `tester.xlsx` and the final 5d1 training table.
- [x] The final 5d1 table has 28 duplicated `Composition` values covering 56 rows; all duplicated compositions differ in target and features, supporting site/polymorph-level ambiguity rather than simple duplication.
- [x] `Predicted CS` and `Predicted RP` are auxiliary model outputs used as 5d1 features, creating a nested-validation/provenance risk for strict reruns.
- [x] No journal DOI was found by the literature/provenance worker; confirmed DOI coverage remains arXiv DOI `10.48550/arXiv.2502.18859` and Zenodo DOI `10.5281/zenodo.14872504`.
- [x] DOI/DataCite metadata for Zenodo DOI `10.5281/zenodo.14872504` points to `https://github.com/NL0119/Ce_5d1_Prediction/tree/original`.
- [x] GitHub tag `NL0119/Ce_5d1_Prediction@original` points to commit `49991b75572dd3bf9ac4e5daa6000ac364b39b2d` and contains `Training_Set_for_5d1.xlsx`.
- [x] Temporary inspection of `Training_Set_for_5d1.xlsx` from the `original` tag found sheet `RFE44`, 357 rows, 46 columns, 357 non-null `5d1` targets, and 330 unique compositions.
- [x] The 357-vs-358 mismatch is best classified as release/version drift between the Zenodo-linked `original` tag and the later `BrgochGroup/main` fork, not as a blank row, duplicated header row, full duplicate row, or tester-row inclusion artifact.
- [x] The Zenodo-linked `original` notebook uses `LeaveOneGroupOut` with `Composition` as the group, so the primary public validation is leave-one-composition-out.
- [x] The later `BrgochGroup/main` notebook defines a 5d1 `best_model` but the 5d1 LOGO loop calls `CS_model.fit(...)` and `CS_model.predict(...)`, creating a code-level comparability risk for later-workbook metrics.
- [x] Neither inspected notebook pins dependency versions or sets an explicit XGBoost estimator seed; both hard-code `device='cuda'`.

# 3. Current Blockers

- [ ] Direct Zenodo landing page, API, OAI/export, and guessed file-download routes for DOI `10.5281/zenodo.14872504` still return HTTP 403 from this machine, so direct Zenodo payload checksums remain unverified.
- [ ] The paper/MRS 357-site count aligns with the Zenodo-linked `original` tag, but the authors' intended interpretation of the later 358-row `BrgochGroup/main` update is not directly reported in inspected metadata.
- [ ] Source DOI/year, measurement-source, and in-house/literature flags are not available in the inspected processed 5d1 training workbook.
- [ ] Exact package versions and XGBoost seed/device reproducibility are not yet frozen.
- [ ] Row identity for duplicated compositions cannot be proven from the final 5d1 workbook alone because `Central Cation`, `Database IDs`, DOI/year, and in-house/source flags are absent.
- [ ] Later-workbook benchmark reporting must decide whether to reproduce `BrgochGroup/main` as written or use an audited fix for the 5d1 `CS_model`/`best_model` mismatch.

# 4. First Next Action

- [ ] Decide the first implementation track: paper-aligned `NL0119/original` reproduction, later `BrgochGroup/main` reproduction-as-written, or later `main` with audited `best_model` fix.
