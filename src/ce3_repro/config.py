from __future__ import annotations

from dataclasses import dataclass


ORIGINAL_RELEASE = "NL0119/Ce_5d1_Prediction@original"
ORIGINAL_COMMIT = "49991b75572dd3bf9ac4e5daa6000ac364b39b2d"
RAW_BASE_URL = "https://raw.githubusercontent.com/NL0119/Ce_5d1_Prediction/original"
ENERGY_TO_NM = 1239.84193


@dataclass(frozen=True)
class Artifact:
    name: str
    url: str
    required: bool = True


ORIGINAL_ARTIFACTS = (
    Artifact(
        name="Training_Set_for_5d1.xlsx",
        url=f"{RAW_BASE_URL}/Training_Set_for_5d1.xlsx",
    ),
    Artifact(
        name="5d1Ce Prediction Model.ipynb",
        url=f"{RAW_BASE_URL}/5d1Ce%20Prediction%20Model.ipynb",
    ),
    Artifact(
        name="README.md",
        url=f"{RAW_BASE_URL}/README.md",
    ),
)


ORIGINAL_5D1_PARAMS = {
    "tree_method": "hist",
    "n_estimators": 200,
    "learning_rate": 0.06,
    "max_depth": 9,
    "min_child_weight": 8,
    "subsample": 0.6,
    "base_score": 0.4,
    "colsample_bytree": 1,
    "colsample_bylevel": 1,
    "colsample_bynode": 1,
    "reg_alpha": 0,
    "reg_lambda": 1,
}


NOTEBOOK_SAVED_5D1_LOGO_METRICS = {
    "avg_mae_eV": 0.15338832561753013,
    "avg_mse_eV2": 0.04344782809517265,
    "avg_rmse_eV": 0.15425705564280934,
    "r2": 0.8380042800908163,
}
