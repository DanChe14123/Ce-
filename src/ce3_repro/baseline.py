from __future__ import annotations

import json
import platform
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import LeaveOneGroupOut
from xgboost import XGBRegressor

from .config import ENERGY_TO_NM, NOTEBOOK_SAVED_5D1_LOGO_METRICS, ORIGINAL_5D1_PARAMS
from .data import GROUP_COLUMN, TARGET_COLUMN


def energy_to_nm(values: np.ndarray) -> np.ndarray:
    return ENERGY_TO_NM / values


def _metric_block(y_true: np.ndarray, y_pred: np.ndarray, unit: str) -> dict[str, float | str]:
    mse = mean_squared_error(y_true, y_pred)
    r2: float | None
    if len(y_true) < 2:
        r2 = None
    else:
        r2 = float(r2_score(y_true, y_pred))
    return {
        f"mae_{unit}": float(mean_absolute_error(y_true, y_pred)),
        f"mse_{unit}2": float(mse),
        f"rmse_{unit}": float(np.sqrt(mse)),
        "r2": r2,
    }


def _fold_metric_row(
    model_name: str,
    fold_index: int,
    group_label: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "model": model_name,
        "fold_index": fold_index,
        "group": group_label,
        "test_rows": int(len(y_true)),
    }
    row.update(_metric_block(y_true, y_pred, "eV"))
    row.update(_metric_block(energy_to_nm(y_true), energy_to_nm(y_pred), "nm"))
    return row


def _make_model(seed: int | None, device: str) -> XGBRegressor:
    params = dict(ORIGINAL_5D1_PARAMS)
    params["device"] = device
    if seed is not None:
        params["random_state"] = seed
    return XGBRegressor(**params)


def run_logo_baseline(
    df: pd.DataFrame,
    seed: int | None = 42,
    device: str = "cpu",
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    x = df.iloc[:, 2:46].to_numpy()
    y = df[TARGET_COLUMN].to_numpy(dtype=float)
    groups = df[GROUP_COLUMN].to_numpy()
    logo = LeaveOneGroupOut()

    fold_rows: list[dict[str, Any]] = []
    predictions: list[pd.DataFrame] = []

    for fold_index, (train_index, test_index) in enumerate(logo.split(x, y, groups), start=1):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        group_label = str(groups[test_index][0])

        model = _make_model(seed=seed, device=device)
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)

        train_mean = np.full_like(y_test, fill_value=float(np.mean(y_train)), dtype=float)
        train_median = np.full_like(y_test, fill_value=float(np.median(y_train)), dtype=float)

        fold_rows.append(_fold_metric_row("xgboost_original_params", fold_index, group_label, y_test, y_pred))
        fold_rows.append(_fold_metric_row("train_mean_baseline", fold_index, group_label, y_test, train_mean))
        fold_rows.append(_fold_metric_row("train_median_baseline", fold_index, group_label, y_test, train_median))

        predictions.append(
            pd.DataFrame(
                {
                    "fold_index": fold_index,
                    "Composition": groups[test_index],
                    "row_index": test_index,
                    "y_true_eV": y_test,
                    "y_pred_eV": y_pred,
                    "y_true_nm": energy_to_nm(y_test),
                    "y_pred_nm": energy_to_nm(y_pred),
                }
            )
        )

    fold_metrics = pd.DataFrame(fold_rows)
    prediction_table = pd.concat(predictions, ignore_index=True)
    summary = summarize_run(fold_metrics, prediction_table, seed=seed, device=device)
    return fold_metrics, prediction_table, summary


def summarize_run(
    fold_metrics: pd.DataFrame,
    prediction_table: pd.DataFrame,
    seed: int | None,
    device: str,
) -> dict[str, Any]:
    xgb_folds = fold_metrics[fold_metrics["model"] == "xgboost_original_params"]
    fold_mean_by_model = {
        model_name: {
            "avg_mae_eV": float(model_rows["mae_eV"].mean()),
            "avg_mse_eV2": float(model_rows["mse_eV2"].mean()),
            "avg_rmse_eV": float(model_rows["rmse_eV"].mean()),
            "avg_mae_nm": float(model_rows["mae_nm"].mean()),
            "avg_rmse_nm": float(model_rows["rmse_nm"].mean()),
        }
        for model_name, model_rows in fold_metrics.groupby("model")
    }
    y_true_e = prediction_table["y_true_eV"].to_numpy(dtype=float)
    y_pred_e = prediction_table["y_pred_eV"].to_numpy(dtype=float)
    y_true_nm = prediction_table["y_true_nm"].to_numpy(dtype=float)
    y_pred_nm = prediction_table["y_pred_nm"].to_numpy(dtype=float)

    package_versions = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
    }
    try:
        import sklearn
        import xgboost

        package_versions["scikit_learn"] = sklearn.__version__
        package_versions["xgboost"] = xgboost.__version__
    except Exception as exc:  # pragma: no cover - only used for diagnostics
        package_versions["version_read_error"] = repr(exc)

    return {
        "model": "xgboost_original_params",
        "release": "NL0119/Ce_5d1_Prediction@original",
        "split": "LeaveOneGroupOut grouped by Composition",
        "fold_count": int(xgb_folds.shape[0]),
        "row_count": int(prediction_table.shape[0]),
        "seed_policy": "local deterministic rerun with random_state" if seed is not None else "notebook-like unseeded rerun",
        "seed": seed,
        "device": device,
        "local_model_params": {**ORIGINAL_5D1_PARAMS, "device": device, **({"random_state": seed} if seed is not None else {})},
        "original_notebook_device": "cuda",
        "original_notebook_seed": "not explicitly set in inspected XGBRegressor definition",
        "notebook_saved_metrics": NOTEBOOK_SAVED_5D1_LOGO_METRICS,
        "fold_mean_metrics": fold_mean_by_model["xgboost_original_params"],
        "fold_mean_metrics_by_model": fold_mean_by_model,
        "global_metrics_eV": _metric_block(y_true_e, y_pred_e, "eV"),
        "global_metrics_nm": _metric_block(y_true_nm, y_pred_nm, "nm"),
        "package_versions": package_versions,
        "warnings": [
            "Metrics are from processed workbook features; source DOI/year/in-house groups are absent.",
            "Predicted CS and Predicted RP are used as frozen released features, not regenerated inside nested CV.",
            "CPU deterministic rerun may differ from original notebook CUDA/unseeded behavior.",
        ],
    }


def leakage_audit(df: pd.DataFrame) -> pd.DataFrame:
    group_sizes = df.groupby(GROUP_COLUMN).size().reset_index(name="row_count")
    duplicate_groups = group_sizes[group_sizes["row_count"] > 1].copy()
    rows = [
        {
            "check": "rows",
            "value": int(df.shape[0]),
            "detail": "Total public processed 5d1 rows in original RFE44 sheet.",
        },
        {
            "check": "unique_compositions",
            "value": int(df[GROUP_COLUMN].nunique()),
            "detail": "LeaveOneGroupOut uses this many composition groups.",
        },
        {
            "check": "duplicated_full_rows",
            "value": int(df.duplicated().sum()),
            "detail": "Full duplicate rows in processed table.",
        },
        {
            "check": "duplicated_composition_groups",
            "value": int(duplicate_groups.shape[0]),
            "detail": "Composition groups with more than one row; LOGO keeps each group in one fold.",
        },
        {
            "check": "duplicated_composition_rows",
            "value": int(duplicate_groups["row_count"].sum()) if not duplicate_groups.empty else 0,
            "detail": "Rows covered by duplicated composition groups.",
        },
        {
            "check": "source_aware_split_auditable",
            "value": 0,
            "detail": "Not auditable because DOI/year/source/in-house flags are absent from workbook.",
        },
        {
            "check": "frozen_auxiliary_features",
            "value": int({"Predicted CS", "Predicted RP"}.issubset(df.columns)),
            "detail": "Predicted CS/RP are present as frozen released features.",
        },
    ]
    return pd.DataFrame(rows)


def write_summary(summary: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
