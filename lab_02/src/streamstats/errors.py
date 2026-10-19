class StreamStatsError(Exception):
    """Базовый класс ошибок для streamstats."""
    pass

class UnsupportedFormatError(StreamStatsError):
    """Ошибка, если формат файла не поддерживается."""
    pass

class InvalidEventError(StreamStatsError):
    """Ошибка валидации события (не хватает полей, неверный тип и т.д.)."""
    pass

class InvalidTimestampError(StreamStatsError):
    """Ошибка формата временной метки."""
    pass
