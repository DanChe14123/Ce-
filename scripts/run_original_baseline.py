from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ce3_repro.baseline import leakage_audit, run_logo_baseline, write_summary
from ce3_repro.data import load_original_5d1_table


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run paper-aligned NL0119/original Ce3+ 5d1 baseline.")
    parser.add_argument(
        "--workbook",
        type=Path,
        default=Path("data/raw/ce_5d1_prediction/original/Training_Set_for_5d1.xlsx"),
        help="Path to Training_Set_for_5d1.xlsx from NL0119/original.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Local deterministic XGBoost random_state.")
    parser.add_argument("--device", default="cpu", help="XGBoost device for local rerun; default is cpu.")
    parser.add_argument(
        "--tables-dir",
        type=Path,
        default=Path("results/tables/ce3_original_baseline"),
        help="Directory for CSV/JSON metric outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = load_original_5d1_table(args.workbook)
    fold_metrics, predictions, summary = run_logo_baseline(df, seed=args.seed, device=args.device)
    audit = leakage_audit(df)

    args.tables_dir.mkdir(parents=True, exist_ok=True)
    fold_metrics.to_csv(args.tables_dir / "fold_metrics.csv", index=False)
    predictions.to_csv(args.tables_dir / "predictions.csv", index=False)
    audit.to_csv(args.tables_dir / "leakage_audit.csv", index=False)
    write_summary(summary, args.tables_dir / "summary.json")

    metrics = summary["global_metrics_eV"]
    print(
        "XGBoost LOGO global metrics: "
        f"MAE={metrics['mae_eV']:.6f} eV, "
        f"RMSE={metrics['rmse_eV']:.6f} eV, "
        f"R2={metrics['r2']:.6f}"
    )
    print(f"Wrote metric tables to {args.tables_dir}")


if __name__ == "__main__":
    main()
