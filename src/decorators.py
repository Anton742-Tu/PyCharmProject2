from functools import wraps
import datetime
import traceback
from typing import Callable, TypeVar, Any, Optional
import sys

T = TypeVar("T")  # Generic тип для возвращаемого значения функции


def log(filename: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Декоратор для логирования вызовов функций и ошибок.
    """

    def decorator(_func: Callable[..., T]) -> Callable[..., T]:
        @wraps(_func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Формируем базовую информацию о вызове
            timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            call_info: str = f"\n[{timestamp}] {_func.__name__}\n" f"Arguments: args={args}, kwargs={kwargs}\n"

            try:
                result: T = _func(*args, **kwargs)
                log_entry: str = f"{call_info}Returned: {result}\n{'-' * 40}"
                _write_log(log_entry, filename)
                return result

            except Exception as e:
                error_entry: str = (
                    f"{call_info}"
                    f"ERROR: {type(e).__name__}: {str(e)}\n"
                    f"Traceback:\n{traceback.format_exc()}"
                    f"{'-' * 40}"
                )
                _write_log(error_entry, filename)
                raise  # Повторно поднимаем исключение

        return wrapper

    # Обработка вызова без скобок (@log вместо @log())
    if callable(filename):
        func: Callable[..., T] = filename
        filename = None
        return decorator(func)

    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """Вспомогательная функция для записи лога."""
    print(message)  # Всегда выводим в консоль

    if filename:
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except IOError as e:
            print(f"Ошибка записи в файл {filename}: {e}", file=sys.stderr)
