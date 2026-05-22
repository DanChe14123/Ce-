from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


TARGET_COLUMN = "5d1"
GROUP_COLUMN = "Composition"
SHEET_NAME = "RFE44"


def load_original_5d1_table(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=SHEET_NAME)
    required = [GROUP_COLUMN, TARGET_COLUMN, "Predicted CS", "Predicted RP"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def profile_original_5d1_table(df: pd.DataFrame) -> dict[str, Any]:
    duplicate_groups = df.groupby(GROUP_COLUMN).size()
    duplicated = duplicate_groups[duplicate_groups > 1].sort_values(ascending=False)
    empty_rows = int(df.isna().all(axis=1).sum())
    full_duplicate_rows = int(df.duplicated().sum())
    target = df[TARGET_COLUMN]
    return {
        "sheet": SHEET_NAME,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "target_column": TARGET_COLUMN,
        "target_unit": "eV",
        "group_column": GROUP_COLUMN,
        "feature_start_column_index": 2,
        "feature_stop_column_index_exclusive": 46,
        "feature_count": int(df.shape[1] - 2),
        "non_null_target_count": int(target.notna().sum()),
        "unique_composition_count": int(df[GROUP_COLUMN].nunique()),
        "empty_rows": empty_rows,
        "full_duplicate_rows": full_duplicate_rows,
        "duplicated_composition_count": int(duplicated.shape[0]),
        "duplicated_composition_rows": int(duplicated.sum()) if not duplicated.empty else 0,
        "duplicated_compositions": duplicated.astype(int).to_dict(),
        "target_min_eV": float(target.min()),
        "target_mean_eV": float(target.mean()),
        "target_median_eV": float(target.median()),
        "target_max_eV": float(target.max()),
        "columns_list": [str(column) for column in df.columns],
        "missing_provenance_fields": [
            "source_doi",
            "source_year",
            "measurement_source_metadata",
            "is_in_house",
            "explicit_ce_substitution_site",
        ],
    }


def write_json(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
