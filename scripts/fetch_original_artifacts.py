from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ce3_repro.artifacts import fetch_artifacts, write_manifest
from ce3_repro.data import load_original_5d1_table, profile_original_5d1_table, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch and profile NL0119/original Ce3+ 5d1 artifacts.")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("data/raw/ce_5d1_prediction/original"),
        help="Directory for small upstream artifacts and manifest.",
    )
    parser.add_argument(
        "--profile-out",
        type=Path,
        default=Path("reproductions/ce3_original_baseline/dataset_profile.json"),
        help="Dataset profile JSON output path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = fetch_artifacts(args.raw_dir)
    write_manifest(rows, args.raw_dir)

    workbook = args.raw_dir / "Training_Set_for_5d1.xlsx"
    df = load_original_5d1_table(workbook)
    profile = profile_original_5d1_table(df)
    profile["source_workbook"] = str(workbook)
    profile["manifest"] = str(args.raw_dir / "manifest.json")
    write_json(profile, args.profile_out)

    print(f"Fetched {len(rows)} artifacts into {args.raw_dir}")
    print(f"Profiled {profile['rows']} rows x {profile['columns']} columns from {workbook}")
    print(f"Wrote {args.profile_out}")


if __name__ == "__main__":
    main()
