"""Build group-meeting materials for the Ce3+ 5d1 reproduction.

The script is intentionally deterministic and reads only completed local
evidence artifacts. It does not rerun models.
"""

from __future__ import annotations

import csv
import html
import json
import math
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "results" / "tables"
FIGURE_DIR = ROOT / "results" / "figures"
MANUSCRIPT_DIR = ROOT / "manuscript"

SOURCE_AUDIT = ROOT / "notes" / "source-audit-ce3-excitation-band-baseline.md"
VERSION_AUDIT = ROOT / "notes" / "zenodo-github-version-audit.md"
MODELING_AUDIT = ROOT / "notes" / "modeling-code-audit-ce3-excitation-band-baseline.md"
BASELINE_REPORT = ROOT / "reproductions" / "ce3_original_baseline" / "report.md"
METRIC_GAP_REPORT = ROOT / "reproductions" / "ce3_original_metric_gap" / "report.md"
BASELINE_SUMMARY = TABLE_DIR / "ce3_original_baseline" / "summary.json"
DATASET_PROFILE = ROOT / "reproductions" / "ce3_original_baseline" / "dataset_profile.json"
METRIC_GAP_RUNS = TABLE_DIR / "ce3_original_metric_gap" / "metric_gap_runs.csv"

KEY_RESULTS = TABLE_DIR / "ce3_group_meeting_key_results.csv"
VERSION_TIMELINE = TABLE_DIR / "ce3_group_meeting_version_timeline.csv"
DATASET_COMPARISON = TABLE_DIR / "ce3_group_meeting_dataset_comparison.csv"
METRIC_GAP_PLOT = TABLE_DIR / "ce3_group_meeting_metric_gap_plot.csv"

TIMELINE_SVG = FIGURE_DIR / "ce3_group_meeting_version_timeline.svg"
DATASET_SVG = FIGURE_DIR / "ce3_group_meeting_dataset_comparison.svg"
PIPELINE_SVG = FIGURE_DIR / "ce3_group_meeting_pipeline.svg"
METRIC_GAP_SVG = FIGURE_DIR / "ce3_group_meeting_metric_gap_seed_sweep.svg"

OUTLINE_MD = MANUSCRIPT_DIR / "ce3_group_meeting_outline.md"
SCRIPT_MD = MANUSCRIPT_DIR / "ce3_group_meeting_script.md"


REQUIRED_SOURCES = [
    SOURCE_AUDIT,
    VERSION_AUDIT,
    MODELING_AUDIT,
    BASELINE_REPORT,
    METRIC_GAP_REPORT,
    BASELINE_SUMMARY,
    DATASET_PROFILE,
    METRIC_GAP_RUNS,
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def fmt(value: float | int | str | None, digits: int = 6) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return value
    return f"{float(value):.{digits}f}"


def ensure_required_sources() -> None:
    missing = [rel(path) for path in REQUIRED_SOURCES if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def validate_source_artifacts(rows: list[dict], path: Path) -> None:
    missing: list[str] = []
    for row in rows:
        artifact = str(row.get("source_artifact", ""))
        for part in [item.strip() for item in artifact.split(";") if item.strip()]:
            if part.startswith(("http://", "https://")):
                continue
            candidate = ROOT / part
            if not candidate.exists():
                missing.append(f"{path.name}: {part}")
    if missing:
        raise FileNotFoundError("Missing referenced source artifacts: " + ", ".join(missing))


def source(path: Path) -> str:
    return rel(path)


def build_key_results(summary: dict, metric_rows: list[dict]) -> list[dict]:
    notebook = summary["notebook_saved_metrics"]
    fold_mean = summary["fold_mean_metrics"]
    global_ev = summary["global_metrics_eV"]
    baselines = summary["fold_mean_metrics_by_model"]
    best = next(row for row in metric_rows if row["run_id"] == "cpu_unseeded_default")
    seed42 = next(row for row in metric_rows if row["run_id"] == "cpu_seed_42_default")

    rows = [
        {
            "section": "source audit",
            "evidence_category": "Literature Fact",
            "claim": "Zenodo DOI/DataCite metadata points to NL0119/Ce_5d1_Prediction tree/original.",
            "value": "10.5281/zenodo.14872504 -> NL0119/Ce_5d1_Prediction@original",
            "unit": "identifier",
            "source_artifact": source(VERSION_AUDIT),
            "caveat": "Direct Zenodo payload/checksum verification returned HTTP 403 locally.",
        },
        {
            "section": "version audit",
            "evidence_category": "Model Inference",
            "claim": "The paper-aligned reproduction object is the original 357-row workbook, not the later 358-row public workbook.",
            "value": "original 357 x 46; later main 358 x 19",
            "unit": "rows x columns",
            "source_artifact": source(VERSION_AUDIT),
            "caveat": "The authors' intent for the later 358-row update is not directly reported in inspected metadata.",
        },
        {
            "section": "dataset",
            "evidence_category": "Model Inference",
            "claim": "The original workbook contains 330 leave-one-composition-out groups.",
            "value": str(summary["fold_count"]),
            "unit": "composition groups",
            "source_artifact": source(DATASET_PROFILE),
            "caveat": "Composition grouping is not source-aware or provenance-aware.",
        },
        {
            "section": "split",
            "evidence_category": "Model Inference",
            "claim": "The inspected LOGO protocol is leave-one-composition-out.",
            "value": "LeaveOneGroupOut grouped by Composition",
            "unit": "split definition",
            "source_artifact": source(MODELING_AUDIT),
            "caveat": "No DOI/year/source/in-house fields are available to audit source-aware splits.",
        },
        {
            "section": "notebook reference",
            "evidence_category": "Model Inference",
            "claim": "Original notebook-saved output gives the closest author-side reference values.",
            "value": f"MAE {fmt(notebook['avg_mae_eV'])}; RMSE {fmt(notebook['avg_rmse_eV'])}; R2 {fmt(notebook['r2'])}",
            "unit": "fold-mean eV for MAE/RMSE; unitless R2",
            "source_artifact": source(MODELING_AUDIT) + ";" + source(BASELINE_REPORT),
            "caveat": "Notebook-saved values are a saved output artifact, not a local rerun.",
        },
        {
            "section": "closest local rerun",
            "evidence_category": "Model Inference",
            "claim": "CPU unseeded/default is the closest local rerun to notebook-saved fold-mean MAE.",
            "value": f"MAE {fmt(best['fold_mean_mae_eV'])}; RMSE {fmt(best['fold_mean_rmse_eV'])}; global R2 {fmt(best['global_r2_eV'])}",
            "unit": "fold-mean eV for MAE/RMSE; global unitless R2",
            "source_artifact": source(METRIC_GAP_RUNS) + ";" + source(METRIC_GAP_REPORT),
            "caveat": f"Residual MAE gap vs notebook is +{fmt(best['delta_vs_notebook_fold_mae_eV'])} eV.",
        },
        {
            "section": "deterministic baseline",
            "evidence_category": "Model Inference",
            "claim": "CPU seed=42 is the deterministic project baseline, not the closest notebook-state reproduction.",
            "value": f"fold-mean MAE {fmt(fold_mean['avg_mae_eV'])}; global MAE {fmt(global_ev['mae_eV'])}; global R2 {fmt(global_ev['r2'])}",
            "unit": "eV for MAE; unitless R2",
            "source_artifact": source(BASELINE_SUMMARY) + ";" + source(BASELINE_REPORT),
            "caveat": f"Seed=42 fold-mean MAE differs from notebook by +{fmt(seed42['delta_vs_notebook_fold_mae_eV'])} eV.",
        },
        {
            "section": "baseline comparison",
            "evidence_category": "Model Inference",
            "claim": "XGBoost outperforms train mean/median baselines under the same composition-grouped split.",
            "value": f"XGB MAE {fmt(fold_mean['avg_mae_eV'])}; mean baseline {fmt(baselines['train_mean_baseline']['avg_mae_eV'])}; median baseline {fmt(baselines['train_median_baseline']['avg_mae_eV'])}",
            "unit": "fold-mean MAE eV",
            "source_artifact": source(BASELINE_SUMMARY) + ";" + source(BASELINE_REPORT),
            "caveat": "All metrics use processed released features and cannot validate row-level source provenance.",
        },
        {
            "section": "provenance limitation",
            "evidence_category": "Model Inference",
            "claim": "The public processed workbook lacks row-level DOI/year/source/in-house fields.",
            "value": "source_doi; source_year; measurement_source_metadata; is_in_house; explicit_ce_substitution_site missing",
            "unit": "missing fields",
            "source_artifact": source(DATASET_PROFILE) + ";" + source(BASELINE_REPORT),
            "caveat": "This blocks provenance-faithful full reproduction from the public workbook alone.",
        },
        {
            "section": "leakage limitation",
            "evidence_category": "Model Inference",
            "claim": "Predicted CS and Predicted RP are frozen released features in this rerun.",
            "value": "not nested-regenerated",
            "unit": "validation policy",
            "source_artifact": source(MODELING_AUDIT) + ";" + source(BASELINE_REPORT),
            "caveat": "Strict nested validation would require regenerating auxiliary predictions inside each fold.",
        },
        {
            "section": "metric gap",
            "evidence_category": "Experiment Hypothesis",
            "claim": "The remaining notebook-vs-local metric gap may come from XGBoost version, CUDA/CPU behavior, or platform numerical differences.",
            "value": "+0.001605",
            "unit": "fold-mean MAE eV",
            "source_artifact": source(METRIC_GAP_REPORT),
            "caveat": "CUDA was skipped because local nvidia-smi returned non-zero; device effects remain untested.",
        },
        {
            "section": "reporting language",
            "evidence_category": "Writing Guidance",
            "claim": "Use 'paper-aligned 357-row public processed-data baseline reproduction' rather than 'complete reproduction'.",
            "value": "allowed wording",
            "unit": "wording",
            "source_artifact": source(BASELINE_REPORT) + ";" + source(METRIC_GAP_REPORT),
            "caveat": "Do not claim provenance-faithful full reproduction.",
        },
    ]
    return rows


def build_timeline_rows() -> list[dict]:
    return [
        {
            "stage_order": 1,
            "source_node": "arXiv:2502.18859",
            "date_label": "2025-02",
            "evidence_category": "Literature Fact",
            "claim": "Paper/source materials for Ce3+ 5d1 prediction were verified.",
            "source_artifact": source(SOURCE_AUDIT),
            "caveat": "Month follows arXiv identifier; this package does not use a precise posting day.",
        },
        {
            "stage_order": 2,
            "source_node": "MRS 2025 abstract",
            "date_label": "2025",
            "evidence_category": "Literature Fact",
            "claim": "Conference material was checked as source context.",
            "source_artifact": source(SOURCE_AUDIT),
            "caveat": "Conference abstract claims are not treated as verified experimental facts.",
        },
        {
            "stage_order": 3,
            "source_node": "Zenodo/DataCite",
            "date_label": "2025-02-14",
            "evidence_category": "Literature Fact",
            "claim": "DOI metadata issued for version original and points to GitHub tree/original.",
            "source_artifact": source(VERSION_AUDIT),
            "caveat": "Direct Zenodo payload checksums remain unavailable locally due to HTTP 403.",
        },
        {
            "stage_order": 4,
            "source_node": "GitHub original tag",
            "date_label": "2025-02-12",
            "evidence_category": "Literature Fact",
            "claim": "Original tag contains the 357-row `Training_Set_for_5d1.xlsx` workbook.",
            "source_artifact": source(VERSION_AUDIT),
            "caveat": "Paper-aligned processed workbook, not raw literature reconstruction.",
        },
        {
            "stage_order": 5,
            "source_node": "BrgochGroup main fork",
            "date_label": "2026-03-13",
            "evidence_category": "Literature Fact",
            "claim": "Later public fork contains a non-identical 358-row workbook.",
            "source_artifact": source(VERSION_AUDIT) + ";" + source(MODELING_AUDIT),
            "caveat": "Metrics from later main must not be mixed with original-release metrics.",
        },
        {
            "stage_order": 6,
            "source_node": "Local reproduction audits",
            "date_label": "2026-05-22/23",
            "evidence_category": "Model Inference",
            "claim": "Original baseline rerun and metric-gap audit completed locally.",
            "source_artifact": source(BASELINE_REPORT) + ";" + source(METRIC_GAP_REPORT),
            "caveat": "CUDA comparison remains skipped locally.",
        },
    ]


def build_dataset_comparison(profile: dict) -> list[dict]:
    return [
        {
            "release": "NL0119/Ce_5d1_Prediction@original",
            "role": "paper-aligned reproduction object",
            "workbook": "Training_Set_for_5d1.xlsx",
            "sheet": profile["sheet"],
            "rows": profile["rows"],
            "columns": profile["columns"],
            "target": profile["target_column"],
            "feature_count": profile["feature_count"],
            "unique_compositions": profile["unique_composition_count"],
            "metrics_policy": "use for original baseline metrics",
            "source_artifact": source(DATASET_PROFILE) + ";" + source(VERSION_AUDIT),
            "caveat": "Processed workbook lacks row-level DOI/year/source/in-house fields.",
        },
        {
            "release": "BrgochGroup/Ce_5d1_Prediction@main",
            "role": "later public workbook for comparison only",
            "workbook": "Training_Set_updated_for_5d1_RFE17.xlsx",
            "sheet": "single sheet",
            "rows": 358,
            "columns": 19,
            "target": "5d1 Ce",
            "feature_count": 17,
            "unique_compositions": 330,
            "metrics_policy": "do not mix with original metrics",
            "source_artifact": source(VERSION_AUDIT) + ";" + source(MODELING_AUDIT),
            "caveat": "Main notebook has a 5d1 `CS_model`/`best_model` variable mismatch risk.",
        },
    ]


def build_metric_gap_plot_rows(summary: dict, metric_rows: list[dict]) -> list[dict]:
    notebook = summary["notebook_saved_metrics"]
    rows = [
        {
            "run_id": "notebook_saved_output",
            "label": "notebook saved",
            "evidence_category": "Model Inference",
            "device": "cuda saved output",
            "seed": "not explicit",
            "fold_mean_mae_eV": notebook["avg_mae_eV"],
            "fold_mean_rmse_eV": notebook["avg_rmse_eV"],
            "global_r2_eV": notebook["r2"],
            "delta_vs_notebook_fold_mae_eV": 0,
            "source_artifact": source(MODELING_AUDIT) + ";" + source(BASELINE_REPORT),
            "caveat": "Saved output artifact, not a local rerun.",
        }
    ]
    label_map = {
        "cpu_unseeded_default": "CPU unseeded/default",
        "cpu_seed_0_default": "CPU seed 0/default",
        "cpu_seed_100_default": "CPU seed 100/default",
        "cpu_seed_1_default": "CPU seed 1/default",
        "cpu_seed_22_default": "CPU seed 22/default",
        "cpu_seed_42_default": "CPU seed 42/default",
        "cpu_seed_42_n_jobs_1": "CPU seed 42/n_jobs=1",
    }
    selected = [row for row in metric_rows if row["run_id"] in label_map]
    selected.sort(key=lambda row: float(row["fold_mean_mae_eV"]))
    for row in selected:
        rows.append(
            {
                "run_id": row["run_id"],
                "label": label_map[row["run_id"]],
                "evidence_category": "Model Inference",
                "device": row["device"],
                "seed": row["seed"] or "unseeded",
                "fold_mean_mae_eV": row["fold_mean_mae_eV"],
                "fold_mean_rmse_eV": row["fold_mean_rmse_eV"],
                "global_r2_eV": row["global_r2_eV"],
                "delta_vs_notebook_fold_mae_eV": row["delta_vs_notebook_fold_mae_eV"],
                "source_artifact": source(METRIC_GAP_RUNS) + ";" + source(METRIC_GAP_REPORT),
                "caveat": "CPU rerun under local package versions; CUDA not tested locally.",
            }
        )
    return rows


def svg_header(width: int = 1280, height: int = 720) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text{font-family:'Segoe UI','Microsoft YaHei',Arial,sans-serif;fill:#17212b}",
        ".title{font-size:34px;font-weight:700}",
        ".subtitle{font-size:18px;fill:#4b5563}",
        ".small{font-size:15px;fill:#4b5563}",
        ".label{font-size:18px;font-weight:650}",
        ".metric{font-size:26px;font-weight:700}",
        "</style>",
        '<rect x="0" y="0" width="1280" height="720" fill="#fbfaf6"/>',
    ]


def add_text(lines: list[str], x: float, y: float, text: str, cls: str = "small", anchor: str = "start") -> None:
    lines.append(
        f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{html.escape(str(text))}</text>'
    )


def add_wrapped(lines: list[str], x: float, y: float, text: str, width: int, cls: str = "small", line_height: int = 20) -> None:
    wrapped = textwrap.wrap(str(text), width=width, break_long_words=False, replace_whitespace=False)
    for idx, part in enumerate(wrapped):
        add_text(lines, x, y + idx * line_height, part, cls=cls)


def write_svg(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if path.stat().st_size <= 500:
        raise RuntimeError(f"SVG appears too small: {rel(path)}")


def build_timeline_svg(rows: list[dict]) -> None:
    lines = svg_header()
    add_text(lines, 70, 70, "Source and version audit timeline", "title")
    add_text(lines, 70, 102, "DataCite/GitHub evidence separates the 357-row original release from the later 358-row workbook.", "subtitle")
    x0, y = 95, 310
    step = 210
    lines.append(f'<line x1="{x0}" y1="{y}" x2="{x0 + step * (len(rows) - 1)}" y2="{y}" stroke="#8aa0a9" stroke-width="4"/>')
    for idx, row in enumerate(rows):
        x = x0 + idx * step
        color = "#1f7a8c" if idx < 4 else "#d68c2f"
        lines.append(f'<circle cx="{x}" cy="{y}" r="23" fill="{color}"/>')
        add_text(lines, x, y + 7, str(row["stage_order"]), "label", "middle")
        add_text(lines, x, y - 60, row["date_label"], "label", "middle")
        add_wrapped(lines, x - 78, y + 55, row["source_node"], 18, "label", 22)
        add_wrapped(lines, x - 90, y + 118, row["claim"], 28, "small", 19)
    add_text(lines, 70, 650, "Caveat: Zenodo payload checksums remain unverified locally because direct routes returned HTTP 403.", "small")
    write_svg(TIMELINE_SVG, lines)


def build_dataset_svg(rows: list[dict]) -> None:
    lines = svg_header()
    add_text(lines, 70, 70, "Dataset version boundary", "title")
    add_text(lines, 70, 102, "The 357-row original workbook is the paper-aligned target; the 358-row main workbook is a later public update.", "subtitle")
    cards = [(80, 170, "#e8f2f4"), (690, 170, "#fff2df")]
    for row, (x, y, fill) in zip(rows, cards):
        lines.append(f'<rect x="{x}" y="{y}" width="510" height="360" rx="10" fill="{fill}" stroke="#c9d3d8" stroke-width="2"/>')
        add_wrapped(lines, x + 32, y + 54, row["release"], 36, "label", 24)
        add_text(lines, x + 32, y + 125, row["role"], "small")
        add_text(lines, x + 32, y + 190, f'{row["rows"]} rows x {row["columns"]} columns', "metric")
        add_text(lines, x + 32, y + 235, f'features: {row["feature_count"]}; unique compositions: {row["unique_compositions"]}', "label")
        add_wrapped(lines, x + 32, y + 290, row["metrics_policy"], 42, "label", 24)
        add_wrapped(lines, x + 32, y + 335, row["caveat"], 55, "small", 20)
    lines.append('<path d="M590 350 L690 350" stroke="#17212b" stroke-width="3" stroke-dasharray="10 8"/>')
    add_text(lines, 640, 332, "do not mix metrics", "label", "middle")
    add_text(lines, 70, 650, "Source: notes/zenodo-github-version-audit.md; notes/modeling-code-audit-ce3-excitation-band-baseline.md", "small")
    write_svg(DATASET_SVG, lines)


def build_pipeline_svg() -> None:
    lines = svg_header()
    add_text(lines, 70, 70, "Processed-data reproduction pipeline", "title")
    add_text(lines, 70, 102, "The rerun validates the released processed baseline, while preserving provenance and nested-feature caveats.", "subtitle")
    boxes = [
        (80, 220, "DataCite -> original", "Zenodo DOI points to NL0119/original"),
        (340, 220, "357-row RFE44 workbook", "5d1 target; 44 released features"),
        (600, 220, "Frozen auxiliary features", "Predicted CS/RP used as released columns"),
        (860, 220, "LOGO by Composition", "Leave-one-composition-out split"),
        (1120, 220, "Metrics", "fold-mean and global held-out separated"),
    ]
    for idx, (x, y, title, body) in enumerate(boxes):
        lines.append(f'<rect x="{x}" y="{y}" width="200" height="150" rx="8" fill="#eef7f6" stroke="#1f7a8c" stroke-width="2"/>')
        add_wrapped(lines, x + 18, y + 45, title, 20, "label", 22)
        add_wrapped(lines, x + 18, y + 94, body, 24, "small", 19)
        if idx < len(boxes) - 1:
            lines.append(f'<path d="M{x + 200} {y + 75} L{x + 260} {y + 75}" stroke="#17212b" stroke-width="3" marker-end="url(#arrow)"/>')
    lines.insert(
        10,
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#17212b"/></marker></defs>',
    )
    lines.append('<rect x="120" y="470" width="1040" height="90" rx="8" fill="#fff7ed" stroke="#d68c2f" stroke-width="2"/>')
    add_text(lines, 150, 510, "Limitation", "label")
    add_text(lines, 270, 510, "No DOI/year/source/in-house fields; no nested regeneration of auxiliary CS/RP features; CUDA comparison skipped locally.", "small")
    add_text(lines, 70, 650, "Source: reproductions/ce3_original_baseline/report.md; reproductions/ce3_original_metric_gap/report.md", "small")
    write_svg(PIPELINE_SVG, lines)


def build_metric_gap_svg(rows: list[dict]) -> None:
    lines = svg_header()
    add_text(lines, 70, 70, "Metric-gap seed sweep", "title")
    add_text(lines, 70, 102, "Seed policy explains most of the deterministic rerun gap; CUDA/device effects remain untested locally.", "subtitle")
    plot_x, plot_y, plot_w, plot_h = 105, 170, 1060, 380
    values = [float(row["fold_mean_mae_eV"]) for row in rows]
    y_min = math.floor((min(values) - 0.001) * 1000) / 1000
    y_max = math.ceil((max(values) + 0.001) * 1000) / 1000
    lines.append(f'<rect x="{plot_x}" y="{plot_y}" width="{plot_w}" height="{plot_h}" fill="#ffffff" stroke="#d1d5db"/>')
    for tick in range(0, 6):
        value = y_min + (y_max - y_min) * tick / 5
        y = plot_y + plot_h - (value - y_min) / (y_max - y_min) * plot_h
        lines.append(f'<line x1="{plot_x}" y1="{y:.1f}" x2="{plot_x + plot_w}" y2="{y:.1f}" stroke="#e5e7eb"/>')
        add_text(lines, plot_x - 12, y + 5, f"{value:.3f}", "small", "end")
    bar_w = plot_w / len(rows) * 0.58
    for idx, row in enumerate(rows):
        value = float(row["fold_mean_mae_eV"])
        x = plot_x + (idx + 0.5) * plot_w / len(rows) - bar_w / 2
        h = (value - y_min) / (y_max - y_min) * plot_h
        y = plot_y + plot_h - h
        color = "#1f7a8c" if row["run_id"] in {"notebook_saved_output", "cpu_unseeded_default"} else "#d68c2f"
        lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{color}"/>')
        add_text(lines, x + bar_w / 2, y - 8, f"{value:.3f}", "small", "middle")
        label = row["label"].replace("CPU ", "").replace("/default", "")
        wrapped = textwrap.wrap(label, width=13, break_long_words=False)
        for line_idx, part in enumerate(wrapped[:3]):
            add_text(lines, x + bar_w / 2, plot_y + plot_h + 28 + 18 * line_idx, part, "small", "middle")
    add_text(lines, 35, 370, "fold-mean MAE (eV)", "small")
    add_text(lines, 70, 650, "Source: results/tables/ce3_original_metric_gap/metric_gap_runs.csv", "small")
    write_svg(METRIC_GAP_SVG, lines)


def build_outline(summary: dict, key_rows: list[dict]) -> str:
    notebook = summary["notebook_saved_metrics"]
    fold_mean = summary["fold_mean_metrics"]
    global_ev = summary["global_metrics_eV"]
    return f"""
# Ce3+ 5d1 激发带位置预测复现组会提纲

## 核心主线

source audit -> version audit -> processed baseline rerun -> metric gap audit -> leakage/provenance limitation

## 一句话结论

完成的是 **paper-aligned 357-row public processed-data baseline reproduction**。目前不能声称完成 provenance-faithful full reproduction，因为公开 workbook 缺少 DOI/year/source/in-house 等行级 provenance 字段，且 `Predicted CS/RP` 未在 nested CV 内重生成。

## Literature Fact

- Zenodo DOI `10.5281/zenodo.14872504` 的 DataCite metadata 指向 `NL0119/Ce_5d1_Prediction/tree/original`。
- `NL0119/Ce_5d1_Prediction@original` 包含 `Training_Set_for_5d1.xlsx` 和原始 notebook。
- `BrgochGroup/Ce_5d1_Prediction@main` 是 later public fork/update，不能和 original 指标混用。

## Model Inference

- `original` workbook: `357 x 46`, sheet `RFE44`, target `5d1` eV, `330` unique compositions。
- later `main` workbook: `358 x 19`，是版本漂移，不是 blank row/header/tester inclusion 可以解释的差异。
- LOGO 实际是 `LeaveOneGroupOut` grouped by `Composition`，应称为 leave-one-composition-out。
- Notebook-saved reference: fold-mean MAE `{fmt(notebook['avg_mae_eV'])}` eV, fold-mean RMSE `{fmt(notebook['avg_rmse_eV'])}` eV, R2 `{fmt(notebook['r2'])}`。
- Closest local rerun: CPU unseeded/default fold-mean MAE `0.154993` eV, fold-mean RMSE `0.155834` eV, global R2 `0.835515`。
- Deterministic project baseline: CPU seed=42 fold-mean MAE `{fmt(fold_mean['avg_mae_eV'])}` eV, global MAE `{fmt(global_ev['mae_eV'])}` eV, global R2 `{fmt(global_ev['r2'])}`。

## Experiment Hypothesis

- Notebook-saved output 可能来自 unseeded/default 或更接近 seed=0 的 XGBoost 路径。
- 剩余 `+0.001605` eV fold-mean MAE gap 可能来自 XGBoost version、CUDA/CPU behavior 或 platform numerical differences；本机 CUDA 未成功测试，因此不能把 device effect 排除。

## Writing Guidance

- 可以说：完成 paper-aligned 357-row public processed-data baseline reproduction。
- 不要说：完全复现、provenance-faithful full reproduction、source-aware validation。
- 组会结尾建议把下一步限定为三件事：补 row-level provenance、nested-regenerate CS/RP auxiliary features、可选 later-main quick rerun 并严格标注为 later public workbook。

## Slide Plan

1. Thesis: reproduced processed baseline, not full provenance-faithful reproduction.
2. Source audit timeline: arXiv/MRS/DataCite/GitHub/Zenodo linkage.
3. Version audit: 357 original vs 358 main.
4. Pipeline: workbook -> frozen features -> LOGO by composition -> separated metrics.
5. Baseline rerun: seed=42 deterministic metrics and naive baselines.
6. Metric-gap audit: notebook saved vs CPU unseeded/default vs seed sweep.
7. Leakage/provenance limits: missing source fields and non-nested auxiliary features.
8. Takeaways: what is defensible now and what blocks stronger claims.

## Deliverables

- Key results table: `{rel(KEY_RESULTS)}`
- Figure assets: `{rel(TIMELINE_SVG)}`, `{rel(DATASET_SVG)}`, `{rel(PIPELINE_SVG)}`, `{rel(METRIC_GAP_SVG)}`
- Speaking script: `{rel(SCRIPT_MD)}`
"""


def build_script(summary: dict) -> str:
    notebook = summary["notebook_saved_metrics"]
    fold_mean = summary["fold_mean_metrics"]
    global_ev = summary["global_metrics_eV"]
    return f"""
# Ce3+ 5d1 复现组会讲稿

## Slide 1. 本次完成的是 paper-aligned processed-data baseline reproduction

各位老师同学好，这次汇报的主线不是直接宣称“完全复现”，而是先把公开证据链和可复现边界讲清楚。我们目前完成的是基于 Zenodo/DataCite 指向的 `NL0119/Ce_5d1_Prediction@original` 的 357-row public processed-data baseline reproduction。

`Literature Fact`: DOI/DataCite metadata 指向 `tree/original`。  
`Model Inference`: 本地已完成 357-row original baseline rerun 和 metric-gap audit。  
`Writing Guidance`: 这里不使用“完全复现”这个说法，因为公开 processed workbook 缺行级 provenance 字段。

## Slide 2. Source audit 先确定 DOI/GitHub 指向

证据链的关键点是：Zenodo DOI `10.5281/zenodo.14872504` 的 DataCite metadata 指向 `NL0119/Ce_5d1_Prediction/tree/original`，而不是后来的 `BrgochGroup/main` workbook。arXiv 和 MRS 材料提供研究背景和 357-site claim 的上下文，但 conference abstract 不被当成独立实验事实。

`Literature Fact`: DataCite related identifier 指向 original tag。  
`Model Inference`: 这使得 original release 成为 paper-count aligned 的优先复现对象。  
`Caveat`: 本机 Zenodo direct payload/checksum 验证仍被 HTTP 403 阻断。

## Slide 3. 357 vs 358 是 version drift，不能混用指标

版本核查显示，`original` 是 `Training_Set_for_5d1.xlsx`, sheet `RFE44`, `357 x 46`；later `main` 是 `Training_Set_updated_for_5d1_RFE17.xlsx`, `358 x 19`。差异不是空行、重复 header、全重复行或 tester inclusion 可以解释的。

`Model Inference`: 357-row original 对齐 paper/MRS count；358-row main 是 later public workbook。  
`Writing Guidance`: 后续所有指标必须标明 dataset release，不能把 358-row main 的结果拿来解释 original notebook。

## Slide 4. 复现流程是 processed workbook baseline，而不是 raw provenance reconstruction

本地流程读取 released processed workbook，使用 original 5d1 hyperparameters，并以 `Composition` 作为 `LeaveOneGroupOut` group。因此更准确的说法是 leave-one-composition-out。`Predicted CS` 和 `Predicted RP` 在本次作为 frozen released features 使用，没有在每个 fold 内 nested-regenerate。

`Model Inference`: LOGO by Composition 可以避免同 Composition duplicated rows 跨 train/test。  
`Caveat`: 由于没有 DOI/year/source/in-house 字段，它不是 source-aware split。

## Slide 5. Deterministic seed=42 是项目可重复基线

本地 deterministic CPU seed=42 rerun 得到 fold-mean MAE `{fmt(fold_mean['avg_mae_eV'])}` eV，global MAE `{fmt(global_ev['mae_eV'])}` eV，global RMSE `{fmt(global_ev['rmse_eV'])}` eV，global R2 `{fmt(global_ev['r2'])}`。同一 split 下，train mean/median baseline 的 fold-mean MAE 约 `0.421` eV，说明 XGBoost baseline 明显优于 naive baseline。

`Model Inference`: seed=42 是可重复项目基线。  
`Caveat`: 它不是最接近 original notebook saved output 的配置。

## Slide 6. Metric-gap audit 显示 seed policy 解释主要差距

Original notebook saved reference 是 fold-mean MAE `{fmt(notebook['avg_mae_eV'])}` eV，fold-mean RMSE `{fmt(notebook['avg_rmse_eV'])}` eV，R2 `{fmt(notebook['r2'])}`。最接近的本地结果是 CPU unseeded/default：fold-mean MAE `0.154993` eV，fold-mean RMSE `0.155834` eV，global R2 `0.835515`。这比 seed=42 更接近 notebook saved output。

`Model Inference`: seed policy 解释了大部分 deterministic rerun gap。  
`Experiment Hypothesis`: 剩余 `+0.001605` eV MAE gap 可能来自 XGBoost version、CUDA/CPU behavior 或 platform numerical differences。

## Slide 7. 不能声称 full reproduction 的原因

限制主要有四个：第一，public workbook 缺 DOI/year/source/in-house flags；第二，`Predicted CS/RP` 是 frozen auxiliary model output，没有 nested-regenerate；第三，Zenodo direct payload/checksum 本机 403；第四，authors' CUDA/historical environment 没有完全重建。

`Model Inference`: 这些限制直接来自本地 audit artifacts。  
`Writing Guidance`: 因此结论必须限定为 processed-data baseline reproduction。

## Slide 8. 结论和下一步

当前最稳妥的结论是：357-row original release 是 paper-aligned target；我们已完成 public processed-data XGBoost baseline rerun；closest local rerun 与 notebook saved MAE 的差距约 `+0.001605` eV；seed=42 rerun 适合作为项目可重复基线。下一步如果要提高 claim strength，需要补 source metadata、重建 nested auxiliary CS/RP pipeline，并可选地单独 rerun 358-row later main，但必须明确标注为 later public workbook。

`Writing Guidance`: 结尾要强调“不混用版本、不放大结论、不把模型结果当实验事实”。
"""


def main() -> None:
    ensure_required_sources()
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    summary = read_json(BASELINE_SUMMARY)
    profile = read_json(DATASET_PROFILE)
    metric_rows = read_csv(METRIC_GAP_RUNS)
    metric_rows_ok = [row for row in metric_rows if row.get("status") == "ok"]

    key_rows = build_key_results(summary, metric_rows_ok)
    timeline_rows = build_timeline_rows()
    dataset_rows = build_dataset_comparison(profile)
    metric_plot_rows = build_metric_gap_plot_rows(summary, metric_rows_ok)

    write_csv(KEY_RESULTS, ["section", "evidence_category", "claim", "value", "unit", "source_artifact", "caveat"], key_rows)
    write_csv(
        VERSION_TIMELINE,
        ["stage_order", "source_node", "date_label", "evidence_category", "claim", "source_artifact", "caveat"],
        timeline_rows,
    )
    write_csv(
        DATASET_COMPARISON,
        [
            "release",
            "role",
            "workbook",
            "sheet",
            "rows",
            "columns",
            "target",
            "feature_count",
            "unique_compositions",
            "metrics_policy",
            "source_artifact",
            "caveat",
        ],
        dataset_rows,
    )
    write_csv(
        METRIC_GAP_PLOT,
        [
            "run_id",
            "label",
            "evidence_category",
            "device",
            "seed",
            "fold_mean_mae_eV",
            "fold_mean_rmse_eV",
            "global_r2_eV",
            "delta_vs_notebook_fold_mae_eV",
            "source_artifact",
            "caveat",
        ],
        metric_plot_rows,
    )

    for table_path, rows in [
        (KEY_RESULTS, key_rows),
        (VERSION_TIMELINE, timeline_rows),
        (DATASET_COMPARISON, dataset_rows),
        (METRIC_GAP_PLOT, metric_plot_rows),
    ]:
        validate_source_artifacts(rows, table_path)

    build_timeline_svg(timeline_rows)
    build_dataset_svg(dataset_rows)
    build_pipeline_svg()
    build_metric_gap_svg(metric_plot_rows)

    write_text(OUTLINE_MD, build_outline(summary, key_rows))
    write_text(SCRIPT_MD, build_script(summary))

    outputs = [
        KEY_RESULTS,
        VERSION_TIMELINE,
        DATASET_COMPARISON,
        METRIC_GAP_PLOT,
        TIMELINE_SVG,
        DATASET_SVG,
        PIPELINE_SVG,
        METRIC_GAP_SVG,
        OUTLINE_MD,
        SCRIPT_MD,
    ]
    print(json.dumps({"ok": True, "outputs": [rel(path) for path in outputs]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
