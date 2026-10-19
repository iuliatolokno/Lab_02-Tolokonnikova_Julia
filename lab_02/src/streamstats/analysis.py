from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from .parsers import iter_events
from .models import Report, Event
from .errors import InvalidEventError, StreamStatsError
import logging

logger = logging.getLogger("streamstats.analysis")


def build_report(inputs: List[Path], fmt: str, skip_invalid: bool) -> Report:
    report = Report()
    first_ts = None
    last_ts = None

    level_counter = Counter()
    source_counter = Counter()

    for path in inputs:
        try:
            for line_no, event in iter_events(path, fmt):
                report.total_events += 1
                level_counter[event.level] += 1
                source_counter[event.source] += 1

                if first_ts is None or event.timestamp < first_ts:
                    first_ts = event.timestamp
                if last_ts is None or event.timestamp > last_ts:
                    last_ts = event.timestamp
        except InvalidEventError as e:
            if skip_invalid:
                logger.warning("Пропущена невалидная строка: %s", e)
                report.skipped_lines += 1
            else:
                raise StreamStatsError(f"Ошибка валидации: {e}") from e
        except Exception as e:
          
            if skip_invalid:
                logger.warning("Пропущена строка с ошибкой: %s", e)
                report.skipped_lines += 1
            else:
                raise StreamStatsError(f"Неожиданная ошибка при чтении файла: {e}") from e


    report.by_level = dict(level_counter)
    report.by_source = dict(source_counter)

    if first_ts is not None:
        report.first_timestamp = first_ts.isoformat()
    if last_ts is not None:
        report.last_timestamp = last_ts.isoformat()
    error_levels = {"ERROR", "CRITICAL"}
    error_source_counts = Counter()

   
    sorted_sources = sorted(source_counter.items(), key=lambda x: x[1], reverse=True)
    report.top_5_error_sources = [
        {"source": src, "count": cnt} for src, cnt in sorted_sources[:5]
    ]

    return report
