import csv
import json
from pathlib import Path
from typing import Iterator, Tuple

from .models import Event
from .errors import UnsupportedFormatError, InvalidEventError


def iter_events(path: Path, fmt: str) -> Iterator[Tuple[int, Event]]:
    if fmt == "csv":
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise InvalidEventError("В CSV отсутствует заголовок (первая строка с названиями колонок)")

            for line_no, row in enumerate(reader, start=1):
                event = Event.from_dict(row)
                yield line_no, event

    elif fmt == "jsonl":
        with path.open(encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                event = Event.from_dict(data)
                yield line_no, event
    else:
        raise UnsupportedFormatError(f"Неподдерживаемый формат: {fmt}")
