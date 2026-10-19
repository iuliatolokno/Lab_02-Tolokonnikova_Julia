import argparse
import sys
import logging
from pathlib import Path

from .analysis import build_report
from .report import save_report
from .errors import StreamStatsError

logger = logging.getLogger("streamstats")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s | %(name)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def parse_args():
    parser = argparse.ArgumentParser(description="Анализатор событий (простая версия)")
    parser.add_argument("inputs", nargs="+", help="Файлы для анализа")
    parser.add_argument("--format", choices=["csv", "jsonl"], required=True,
                        help="Формат файлов (csv или jsonl)")

    parser.add_argument("--output", required=True, help="Путь к выходному JSON-файлу")
    parser.add_argument("--skip-invalid", action="store_true",
                        help="Пропускать ошибочные строки вместо остановки")
    
    return parser.parse_args()


def main():
    args = parse_args()
    for p in args.inputs:
        path = Path(p)
        if not path.exists():
            logger.error(f"Файл не найден: {path}")
            sys.exit(1)
    
    try:
        input_paths = [Path(p) for p in args.inputs]
        report = build_report(input_paths, args.format, args.skip_invalid)
        output_path = Path(args.output)
        save_report(report, output_path)
        logger.info("Отчёт успешно сохранён")
        
    except StreamStatsError as e:
        logger.error(f"Ошибка в анализе: {e}")
        sys.exit(2)
    except Exception as e:
        logger.exception("Произошла неожиданная ошибка")
        sys.exit(3)


if __name__ == "__main__":
    main()
