# Literature / Provenance Worker Feedback

Date: 2026-05-22

## Worker Role

- Role: Literature / provenance worker
- Files/pages inspected: `AGENTS.md`, active OpenSpec files, `notes/source-audit-ce3-excitation-band-baseline.md`, worker feedback template, arXiv, arXiv PDF/SI pages, MRS abstract, GitHub repo/raw files, Zenodo DOI metadata, NASSCC abstract book, poster search-indexed PDF text, institution publication page.

## Literature Fact

| Source | URL/DOI | Access status | Artifact type | Raw training labels | DOI/year/source metadata | Literature vs in-house | Feature instructions | Code or description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arXiv abstract | https://arxiv.org/abs/2502.18859; DOI https://doi.org/10.48550/arXiv.2502.18859 | Accessible | Preprint record | No | Paper-level yes; row-level no | Says literature + in-house, no row flags | High-level only | Description |
| arXiv PDF + embedded SI pages | https://arxiv.org/pdf/2502.18859 | Accessible | Paper + SI tables | No | Paper-level yes; no row DOI/year | Says both sources, no row flags | Yes, feature classes/list and methods | Description/tables |
| MRS 2025 MT03.08.09 | https://www.mrs.org/meetings-events/annual-meetings/archive/meeting/presentations/view/2025-mrs-spring-meeting/2025-mrs-spring-meeting-4271462 | Accessible | Conference abstract | No | Event/date/institution only | Says literature + in-house, no row flags | No | Description |
| GitHub repo | https://github.com/BrgochGroup/Ce_5d1_Prediction | Accessible via GitHub API/raw | Code/data repo | Yes: `5d1 Ce` target column; no raw spectra | No row DOI/year/source columns found | No flag found | Yes, notebook uses MP API/CIF and element tables | Code + workbooks |
| Zenodo DOI | https://doi.org/10.5281/zenodo.14872504 | Page/API 403 from this machine; DOI CSL JSON accessible | Zenodo software record | Metadata says repository includes raw training data; files not verified | DOI metadata yes; row metadata not verified | Not visible | Metadata mentions descriptor/model; file-level not verified | Unknown due 403 |
| NASSCC 2025 abstract book | https://group.chem.iastate.edu/Kovnir/NASSCC2025/BookofAbstracts.pdf | Accessible | Conference abstract book | No | Event/book context only | Says literature + in-house, no row flags | No | Description |
| Poster PDF | https://www.nseresearch.org/2024/posters/Ensuring%20Excitation%20Machine%20Learning%20a%20Phosphor%27s%20Excitation%20Band%20Position.pdf | Search-indexed text found; direct shell HEAD failed TLS | Poster | No inspected table | No row metadata | Mentions literature extraction, no row flags | Visual/summary only | Description |
| Institution publication page | https://www.ch.cam.ac.uk/person/sk2045?page=1 | Accessible/search-indexed | Publication listing | No | Lists arXiv DOI only | No | No | Description |

- arXiv, MRS, and NASSCC sources all support the public claim of 357 Ce3+ cation substitution sites across 337 host/phosphor entries.
- The arXiv PDF data-availability section points to GitHub and Zenodo for Ce3+ 5d1 training data, feature-generation code, and prediction model.
- No journal DOI was found in inspected publication pages; confirmed DOI coverage is the arXiv DOI plus Zenodo DOI.

## Model Inference

- Temporary inspection of `Training_Set_updated_for_5d1_RFE17.xlsx` found `Sheet1`, shape `358 x 19`, 358 non-null `5d1 Ce` values, 330 unique `Composition` values, 0 full duplicate rows, 0 duplicated header rows, and 0 all-empty rows.
- Temporary inspection of `tester.xlsx` found 3 compositions and 0 overlap with the training workbook, so the example/test workbook is not the extra training row.
- The notebook contains executable feature/model workflow code, including MP API lookup, CIF parsing, XGBoost models, and `LeaveOneGroupOut`; it does not expose row-level source DOI/year or `is_in_house`.

## Experiment Hypothesis

- The 357 vs 358 discrepancy is narrowed but unresolved. Current evidence does not support an extra blank row, duplicated header row, full duplicate row, or obvious tester/example row.
- Plausible explanations are multi-site accounting, version drift between manuscript and released workbook, or a processed-workbook inclusion rule differing from the paper count. These are not verified.

## Missing Evidence

- Zenodo record file list and archived payload contents remain unverified because `zenodo.org/api/records/14872504` and the landing page return HTTP 403 from this machine.
- The public 5d1 workbook lacks `source_doi`, `source_year`, source type, raw spectrum reference, and literature/in-house flags.
- Original literature source table, in-house measurement table, and row-level provenance mapping are not available in the inspected GitHub workbook.
- No project-specific Hugging Face dataset/model/paper artifact was found; the arXiv Hugging Face link appears to be a generic arXivLabs link.

## Risks

- Provenance leakage risk: without DOI/year/source flags, source-aware or literature-aware splits cannot be audited.
- Count mismatch risk: reporting exact reproduction of the paper's 357-site benchmark would be premature while the released workbook has 358 rows.
- Metric comparability risk: public processed workbook can support model rerun, but not a fully provenance-audited literature reconstruction.
- Reporting risk: conference abstracts/poster claims should remain claims, not verified experimental facts.

## Recommended Next Action

- Verify Zenodo from a non-403 route and export the file list/version metadata, then compare the archived Zenodo payload against GitHub `main` to determine whether the 357/358 mismatch is version drift or data-accounting logic.

