# 1. What Was Completed

- [x] Restored project context from `AGENTS.md`, project memory status, global memory routing, and OpenSpec.
- [x] Confirmed prior changes `repro-ce3-excitation-band-baseline` and `repro-ce3-original-baseline-rerun` are complete.
- [x] Created OpenSpec change `repro-ce3-original-metric-gap-audit`.
- [x] Defined the metric-gap audit plan.
- [x] Added `scripts/audit_original_metric_gap.py`.
- [x] Extended baseline runner to support `n_jobs` controls.
- [x] Ran CPU unseeded/default, CPU seeds `0`, `1`, `22`, `42`, `100`, and CPU seed `42` with `n_jobs=1`.
- [x] Recorded CUDA comparison as skipped because `nvidia-smi` returned non-zero on this machine.
- [x] Wrote metric-gap outputs under `results/tables/ce3_original_metric_gap/`.
- [x] Wrote `reproductions/ce3_original_metric_gap/report.md`.
- [x] Updated `reproductions/ce3_original_baseline/report.md` with a metric-gap pointer.
- [x] Ran `python -m compileall src scripts`.
- [x] Validated `repro-ce3-original-metric-gap-audit` with `cmd /c openspec validate repro-ce3-original-metric-gap-audit`.

# 2. Evidence-Backed Conclusions

- [x] Project memory is connected under project memory id `ce3-63aa6e88`, with no relevant stable fact returned for the metric-gap query.
- [x] Prior local deterministic CPU rerun produced fold-mean MAE `0.1615349876620553` eV and global MAE `0.16083551934720422` eV.
- [x] Original notebook saved output reports fold-mean MAE `0.15338832561753013` eV and R2 `0.8380042800908163`.
- [x] CPU unseeded/default produced fold-mean MAE `0.1549934117114905` eV and global R2 `0.8355147246024563`.
- [x] CPU `random_state=0`/default produced the same metrics as CPU unseeded/default in this environment.
- [x] CPU `random_state=42`/default produced fold-mean MAE `0.1615349876620553` eV, explaining most of the prior gap as seed-policy sensitivity.
- [x] CPU `random_state=42`, `n_jobs=1` produced fold-mean MAE `0.159380745010665` eV; parallelism changes the result but does not recover notebook-saved metrics.

# 3. Current Blockers

- [ ] CUDA/device effects remain untested because local `nvidia-smi` returned non-zero / permission failure.
- [ ] The residual `+0.0016050860939603728` eV fold-mean MAE gap between notebook-saved output and CPU unseeded/default remains unresolved; likely contributors are XGBoost version, CUDA/CPU behavior, or platform numerical differences.

# 4. First Next Action

- [ ] Use `reproductions/ce3_original_metric_gap/report.md` as the reference when reporting original-baseline metric comparability.
