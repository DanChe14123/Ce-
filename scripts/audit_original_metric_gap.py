from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ce3_repro.baseline import run_logo_baseline
from ce3_repro.config import NOTEBOOK_SAVED_5D1_LOGO_METRICS
from ce3_repro.data import load_original_5d1_table


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Ce3+ original baseline metric gap across seeds/device/n_jobs.")
    parser.add_argument(
        "--workbook",
        type=Path,
        default=Path("data/raw/ce_5d1_prediction/original/Training_Set_for_5d1.xlsx"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("results/tables/ce3_original_metric_gap"),
    )
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 22, 42, 100])
    parser.add_argument("--include-cuda", action="store_true", help="Attempt a CUDA run if nvidia-smi is available.")
    return parser.parse_args()


def cuda_probe() -> dict[str, Any]:
    try:
        proc = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except FileNotFoundError:
        return {"cuda_available": False, "reason": "nvidia-smi not found"}
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {"cuda_available": False, "reason": repr(exc)}
    if proc.returncode != 0:
        return {"cuda_available": False, "reason": proc.stderr.strip() or "nvidia-smi returned non-zero"}
    return {"cuda_available": True, "nvidia_smi": proc.stdout.strip()}


def flatten_summary(run_id: str, summary: dict[str, Any], elapsed_s: float, status: str = "ok") -> dict[str, Any]:
    fold = summary["fold_mean_metrics"]
    global_ev = summary["global_metrics_eV"]
    global_nm = summary["global_metrics_nm"]
    notebook = NOTEBOOK_SAVED_5D1_LOGO_METRICS
    return {
        "run_id": run_id,
        "status": status,
        "device": summary["device"],
        "n_jobs": summary["n_jobs"],
        "seed_policy": summary["seed_policy"],
        "seed": "" if summary["seed"] is None else summary["seed"],
        "elapsed_s": round(elapsed_s, 3),
        "fold_mean_mae_eV": fold["avg_mae_eV"],
        "fold_mean_mse_eV2": fold["avg_mse_eV2"],
        "fold_mean_rmse_eV": fold["avg_rmse_eV"],
        "fold_mean_mae_nm": fold["avg_mae_nm"],
        "fold_mean_rmse_nm": fold["avg_rmse_nm"],
        "global_mae_eV": global_ev["mae_eV"],
        "global_rmse_eV": global_ev["rmse_eV"],
        "global_r2_eV": global_ev["r2"],
        "global_mae_nm": global_nm["mae_nm"],
        "global_rmse_nm": global_nm["rmse_nm"],
        "global_r2_nm": global_nm["r2"],
        "delta_vs_notebook_fold_mae_eV": fold["avg_mae_eV"] - notebook["avg_mae_eV"],
        "delta_vs_notebook_fold_rmse_eV": fold["avg_rmse_eV"] - notebook["avg_rmse_eV"],
        "delta_vs_notebook_r2_global_minus_notebook": global_ev["r2"] - notebook["r2"],
    }


def run_config(df: pd.DataFrame, run_id: str, seed: int | None, device: str, n_jobs: int | None) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()
    _, _, summary = run_logo_baseline(df, seed=seed, device=device, n_jobs=n_jobs)
    elapsed = time.perf_counter() - start
    row = flatten_summary(run_id, summary, elapsed_s=elapsed)
    return row, summary


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    df = load_original_5d1_table(args.workbook)
    cuda = cuda_probe()

    configs: list[dict[str, Any]] = [
        {"run_id": "cpu_unseeded_default", "seed": None, "device": "cpu", "n_jobs": None},
    ]
    configs.extend(
        {"run_id": f"cpu_seed_{seed}_default", "seed": seed, "device": "cpu", "n_jobs": None}
        for seed in args.seeds
    )
    configs.append({"run_id": "cpu_seed_42_n_jobs_1", "seed": 42, "device": "cpu", "n_jobs": 1})
    if args.include_cuda and cuda.get("cuda_available"):
        configs.append({"run_id": "cuda_seed_42_default", "seed": 42, "device": "cuda", "n_jobs": None})

    rows: list[dict[str, Any]] = []
    summaries: dict[str, Any] = {}
    for config in configs:
        print(
            f"Running {config['run_id']} "
            f"(device={config['device']}, seed={config['seed']}, n_jobs={config['n_jobs']})",
            flush=True,
        )
        try:
            row, summary = run_config(df, **config)
        except Exception as exc:
            row = {
                "run_id": config["run_id"],
                "status": "failed",
                "device": config["device"],
                "n_jobs": config["n_jobs"] if config["n_jobs"] is not None else "xgboost_default",
                "seed_policy": "failed",
                "seed": "" if config["seed"] is None else config["seed"],
                "error": repr(exc),
            }
            summary = {"error": repr(exc), "config": config}
        rows.append(row)
        summaries[config["run_id"]] = summary

    if not args.include_cuda or not cuda.get("cuda_available"):
        rows.append(
            {
                "run_id": "cuda_seed_42_default",
                "status": "skipped",
                "device": "cuda",
                "n_jobs": "xgboost_default",
                "seed_policy": "skipped",
                "seed": 42,
                "skip_reason": cuda.get("reason", "CUDA run not requested"),
            }
        )

    runs = pd.DataFrame(rows)
    runs.to_csv(args.out_dir / "metric_gap_runs.csv", index=False)

    seed_sweep = runs[(runs["status"] == "ok") & (runs["device"] == "cpu") & (runs["n_jobs"] == "xgboost_default")].copy()
    seed_sweep.to_csv(args.out_dir / "seed_sweep.csv", index=False)

    device_parallelism = runs[runs["run_id"].isin(["cpu_seed_42_default", "cpu_seed_42_n_jobs_1", "cuda_seed_42_default"])].copy()
    device_parallelism.to_csv(args.out_dir / "device_parallelism.csv", index=False)

    ok = runs[runs["status"] == "ok"].copy()
    best = ok.sort_values("delta_vs_notebook_fold_mae_eV", key=lambda col: col.abs()).head(1).to_dict("records")
    summary = {
        "workbook": str(args.workbook),
        "notebook_saved_metrics": NOTEBOOK_SAVED_5D1_LOGO_METRICS,
        "cuda_probe": cuda,
        "run_count_ok": int(ok.shape[0]),
        "run_count_total_including_skips": int(runs.shape[0]),
        "best_match_by_abs_fold_mae_delta": best[0] if best else None,
        "fold_mae_delta_range_eV": {
            "min": float(ok["delta_vs_notebook_fold_mae_eV"].min()) if not ok.empty else None,
            "max": float(ok["delta_vs_notebook_fold_mae_eV"].max()) if not ok.empty else None,
        },
        "all_run_summaries": summaries,
    }
    (args.out_dir / "metric_gap_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote metric-gap audit outputs to {args.out_dir}", flush=True)


if __name__ == "__main__":
    main()
