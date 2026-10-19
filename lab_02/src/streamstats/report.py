import json
from pathlib import Path

from .models import Report

def save_report(report: Report, output_path: Path) -> None:
    data = report.to_dict()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
