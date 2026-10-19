from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List

LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

@dataclass
class Event:
    timestamp: datetime
    level: str
    source: str
    message: str

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        required = ["timestamp", "level", "source", "message"]
        if not all(k in data for k in required):
            raise ValueError("Отсутствуют обязательные поля")

        ts_str = data["timestamp"]
        try:
            # Обработка суффикса Z (UTC) для fromisoformat
            timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except ValueError as e:
            raise InvalidTimestampError(f"Неверный формат timestamp: {ts_str}") from e

        level = data["level"].upper()
        if level not in LEVELS:
            raise InvalidEventError(f"Недопустимый уровень: {level}")

        source = data["source"]
        if not source:
            raise InvalidEventError("Поле source не может быть пустым")

        return cls(
            timestamp=timestamp,
            level=level,
            source=source,
            message=data["message"],
        )


@dataclass
class Report:
    total_events: int = 0
    by_level: Dict[str, int] = field(default_factory=dict)
    by_source: Dict[str, int] = field(default_factory=dict)
    top_5_error_sources: List[dict] = field(default_factory=list)
    first_timestamp: Optional[str] = None
    last_timestamp: Optional[str] = None
    skipped_lines: int = 0

    def to_dict(self) -> dict:
        return {
            "total_events": self.total_events,
            "by_level": self.by_level,
            "by_source": self.by_source,
            "top_5_error_sources": self.top_5_error_sources,
            "first_timestamp": self.first_timestamp,
            "last_timestamp": self.last_timestamp,
            "skipped_lines": self.skipped_lines,
        }
