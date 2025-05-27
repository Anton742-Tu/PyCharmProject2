from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple
from unittest.mock import MagicMock, patch

import pytest
from src.decorators import log


# Вспомогательные функции с аннотациями типов
def read_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


# 1. Тест форматирования времени
def test_time_formatting(capsys: pytest.CaptureFixture[str]) -> None:
    test_time = datetime(2023, 1, 15, 12, 30, 45)

    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = test_time

        @log()
        def timed_func() -> str:
            return "time check"

        timed_func()

        captured = capsys.readouterr()
        assert "[2023-01-15 12:30:45]" in captured.out


# 2. Тест логирования в консоль
def test_console_logging(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)

    captured = capsys.readouterr()
    assert "add" in captured.out
    assert "args=(2, 3)" in captured.out
    assert "Returned: 5" in captured.out
    assert result == 5


# 3. Тест логирования в файл
def test_file_logging(tmp_path: Path) -> None:
    log_file = tmp_path / "test.log"

    @log(str(log_file))
    def multiply(a: int, b: int) -> int:
        return a * b

    multiply(4, 5)

    assert log_file.exists()
    content = read_file(str(log_file))
    assert "multiply" in content
    assert "args=(4, 5)" in content
    assert "Returned: 20" in content


# 4. Тест логирования ошибок
def test_error_logging(
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path
) -> None:
    log_file = tmp_path / "error.log"

    @log(str(log_file))
    def fail() -> None:
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        fail()

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "ERROR: ValueError" in captured.out
    assert "Test error" in captured.out

    # Проверяем запись в файл
    assert log_file.exists()
    content = read_file(str(log_file))
    assert "ERROR: ValueError" in content


# 6. Тест сохранения метаданных
def test_preserves_metadata() -> None:
    @log()
    def documented_func(a: int) -> int:
        """Тестовая функция"""
        return a

    assert documented_func.__name__ == "documented_func"
    assert documented_func.__doc__ == "Тестовая функция"


# 7. Тест обработки ошибок файловой системы
def test_file_errors_handling(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch
) -> None:
    def mock_open(*args: Any, **kwargs: Any) -> MagicMock:
        raise IOError("Disk error")

    monkeypatch.setattr("builtins.open", mock_open)

    @log("invalid/path.log")
    def safe_func() -> str:
        return "OK"

    result = safe_func()
    captured = capsys.readouterr()

    assert result == "OK"
    assert "Ошибка записи в файл" in captured.err


# 8. Тест с различными типами аргументов
def test_various_argument_types(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def complex_func(
            a: int,
            b: str,
            c: List[int],
            d: Dict[str, str]
    ) -> Tuple[int, str, List[int], Dict[str, str]]:
        return a, b, c, d

    complex_func(1, "test", [1, 2], {"key": "value"})
    captured = capsys.readouterr()

    assert "args=(1, 'test', [1, 2], {'key': 'value'})" in captured.out
