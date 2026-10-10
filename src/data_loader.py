"""Source-preserving acquisition and validation for the UCI SECOM files."""

from __future__ import annotations

import hashlib
import shutil
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd


FEATURE_PREFIX = "feature_"


def sha256(path: Path) -> str:
    """Return the SHA-256 checksum of a local file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_secom(archive_url: str, raw_dir: Path) -> dict[str, str]:
    """Download and extract the official UCI archive without modifying its files."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    archive_path = raw_dir / "secom.zip"
    with urllib.request.urlopen(archive_url) as response, archive_path.open("wb") as output:
        shutil.copyfileobj(response, output)
    with zipfile.ZipFile(archive_path) as archive:
        expected = {"secom.data", "secom_labels.data"}
        available = {Path(name).name for name in archive.namelist()}
        missing = expected - available
        if missing:
            raise ValueError(f"Official archive is missing expected files: {sorted(missing)}")
        for member in archive.namelist():
            name = Path(member).name
            if name in expected or name == "secom.names":
                (raw_dir / name).write_bytes(archive.read(member))
    return {
        "archive_sha256": sha256(archive_path),
        "data_sha256": sha256(raw_dir / "secom.data"),
        "labels_sha256": sha256(raw_dir / "secom_labels.data"),
    }


def load_secom(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load raw SECOM observations and labels while preserving source row order."""
    data_path = raw_dir / "secom.data"
    labels_path = raw_dir / "secom_labels.data"
    if not data_path.exists() or not labels_path.exists():
        raise FileNotFoundError("Run scripts/download_data.py before loading SECOM.")

    features = pd.read_csv(data_path, sep=r"\s+", header=None, na_values=["NaN"])
    features.columns = [f"{FEATURE_PREFIX}{index:03d}" for index in range(1, features.shape[1] + 1)]
    # The live source uses a quoted timestamp, so parse it as two fields rather than
    # silently splitting a date/time into a misleading third column.
    labels = pd.read_csv(labels_path, sep=r"\s+", header=None, names=["yield_label", "timestamp_raw"], quotechar='"')
    if len(features) != len(labels):
        raise ValueError(f"Row mismatch: {len(features)} feature rows and {len(labels)} label rows.")
    labels["timestamp"] = pd.to_datetime(labels["timestamp_raw"], errors="coerce", dayfirst=True)
    labels["is_fail"] = labels["yield_label"].eq(1)
    return features, labels


def validate_secom(features: pd.DataFrame, labels: pd.DataFrame) -> dict[str, object]:
    """Return auditable structural checks; do not impose undocumented assumptions."""
    values = set(pd.to_numeric(labels["yield_label"], errors="coerce").dropna().unique())
    return {
        "n_rows": len(features),
        "n_features": features.shape[1],
        "n_labels": len(labels),
        "row_alignment": len(features) == len(labels),
        "observed_labels": [int(value) for value in sorted(values)],
        "timestamp_parse_rate": float(labels["timestamp"].notna().mean()),
        "feature_columns": list(features.columns),
    }


def feature_mapping(features: pd.DataFrame) -> pd.DataFrame:
    """Create an explicit mapping that preserves anonymity rather than inventing names."""
    return pd.DataFrame(
        {
            "source_position": range(1, features.shape[1] + 1),
            "project_feature": features.columns,
            "physical_interpretation": "Not supplied by UCI; intentionally unspecified",
        }
    )
