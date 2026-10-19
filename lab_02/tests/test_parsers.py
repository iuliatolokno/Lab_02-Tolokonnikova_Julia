import tempfile
import os
from pathlib import Path
import pytest
from streamstats.parsers import iter_csv_lines, iter_jsonl_lines

def test_csv_with_header():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "data.csv"
        path.write_text("timestamp,level,source,message\n2024-01-01T12:00:00,INFO,app,hello", encoding="utf-8")
        lines = list(iter_csv_lines(path))
        assert len(lines) == 1
        _, row = lines[0]
        assert row["level"] == "INFO"

def test_jsonl_unicode():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "data.jsonl"
        path.write_text('{"timestamp":"2024-01-01T12:00:00","level":"INFO","source":"app","message":"привет мир"}\n', encoding="utf-8")
        lines = list(iter_jsonl_lines(path))
        assert len(lines) == 1
