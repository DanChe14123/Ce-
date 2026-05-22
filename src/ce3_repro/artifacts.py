from __future__ import annotations

import csv
import hashlib
import json
import urllib.request
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .config import Artifact, ORIGINAL_ARTIFACTS, ORIGINAL_COMMIT, ORIGINAL_RELEASE


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_artifacts(output_dir: Path, artifacts: Iterable[Artifact] = ORIGINAL_ARTIFACTS) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for artifact in artifacts:
        local_path = output_dir / artifact.name
        if not local_path.exists():
            with urllib.request.urlopen(artifact.url, timeout=90) as response:
                local_path.write_bytes(response.read())
        rows.append(
            {
                **asdict(artifact),
                "release": ORIGINAL_RELEASE,
                "commit": ORIGINAL_COMMIT,
                "local_path": str(local_path),
                "byte_size": local_path.stat().st_size,
                "sha256": sha256_file(local_path),
            }
        )
    return rows


def write_manifest(rows: list[dict[str, object]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "manifest.json"
    csv_path = output_dir / "manifest.csv"
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if rows:
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
