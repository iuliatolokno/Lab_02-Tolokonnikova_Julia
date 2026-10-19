import subprocess
from pathlib import Path
import json

def test_cli_generates_report(tmp_path):
    csv_path = tmp_path / "events.csv"
    jsonl_path = tmp_path / "events.jsonl"
    output_path = tmp_path / "report.json"

    csv_path.write_text("timestamp,level,source,message\n2026-10-18T10:00:00,INFO,app,started\n")
    jsonl_path.write_text('{"timestamp": "2026-10-18T11:00:00", "level": "ERROR", "source": "db", "message": "connection"}\n')

    result = subprocess.run(
        [
            "sys.executable", "-m", "streamstats", "analyze",
            str(csv_path), str(jsonl_path),
            "--format", "csv",
            "--output", str(output_path)
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert output_path.exists(), "report.json не создан"

    with output_path.open("r", encoding="utf-8") as f:
        report = json.load(f)

    assert "total_events" in report
    assert "levels" in report
