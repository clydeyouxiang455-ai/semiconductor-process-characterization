"""Download UCI SECOM source files and record integrity checksums."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data_loader import download_secom


def main() -> None:
    config = yaml.safe_load((ROOT / "configs" / "analysis_config.yaml").read_text(encoding="utf-8"))
    checksums = download_secom(config["secom"]["archive_url"], ROOT / "data" / "raw")
    (ROOT / "data" / "raw" / "checksums.json").write_text(json.dumps(checksums, indent=2), encoding="utf-8")
    print("Downloaded official UCI SECOM source files.")


if __name__ == "__main__":
    main()
