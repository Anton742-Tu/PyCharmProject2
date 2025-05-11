import pytest
from src.generators import card_number_generator


def test_card_number_generator() -> None:
    # Тест 1: Генерация одного номера
    gen = card_number_generator(1, 1)
    assert next(gen) == "0000 0000 0000 0001", "Первый номер должен быть 0000 0000 0000 0001"

    # Тест 2: Генерация диапазона
    gen = card_number_generator(1, 3)
    assert list(gen) == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ], "Должны сгенерироваться три последовательных номера"

    # Тест 3: Проверка формата
    gen = card_number_generator(1234567812345678, 1234567812345678)
    number = next(gen)
    assert len(number) == 19, "Длина номера должна быть 19 символов (16 цифр + 3 пробела)"
    assert number.count(" ") == 3, "Должно быть 3 пробела"
    assert number.replace(" ", "").isdigit(), "Должны быть только цифры"

    # Тест 4: Некорректный диапазон (start > end)
    try:
        list(card_number_generator(10, 1))
        assert False, "Должно было возникнуть ValueError"
    except ValueError:
        pass  # Ожидаемое поведение

    # Тест 5: Граничные значения
    gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9999", "Последний номер должен быть 9999 9999 9999 9999"


@pytest.fixture
def card_number_ranges() -> list[tuple[int, int, list[str]]]:
    """Фикстура с примерами диапазонов и ожидаемыми номерами карт."""
    return [
        # start, end, ожидаемые номера
        (
            1,
            3,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
            ],
        ),
        (
            9999,
            10001,
            [
                "0000 0000 0000 9999",
                "0000 0000 0001 0000",
                "0000 0000 0001 0001",
            ],
        ),
        (
            9999999999999998,
            9999999999999999,
            [
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
    ]


@pytest.mark.parametrize(
    "start, end, expected_numbers",
    [
        (
            1,
            3,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
            ],
        ),
        (
            9999,
            10001,
            [
                "0000 0000 0000 9999",
                "0000 0000 0001 0000",
                "0000 0000 0001 0001",
            ],
        ),
    ],
)
def test_card_number_generator_range(
    start: int,
    end: int,
    expected_numbers: list[str],
) -> None:
    """Тест генерации номеров карт в заданном диапазоне."""
    generator = card_number_generator(start, end)
    generated_numbers = list(generator)
    assert generated_numbers == expected_numbers


@pytest.mark.parametrize(
    "start,end,expected_count",
    [
        (1, 1, 1),
        (1, 100, 100),
        (9999999999999990, 9999999999999999, 10),
    ],
)
def test_card_numbers_generator_ranges(start, end, expected_count):
    result = list(card_number_generator(start, end))
    assert len(result) == expected_count


def test_card_number_generator_format() -> None:
    """Тест формата номера карты (16 цифр, разделённых пробелами)."""
    generator = card_number_generator(1234567890123456, 1234567890123456)
    number = next(generator)
    assert len(number) == 19  # 16 цифр + 3 пробела
    assert number.replace(" ", "").isdigit()


def test_card_number_generator_invalid_range() -> None:
    """Тест на некорректный диапазон (start > end)."""
    with pytest.raises(ValueError, match="Start must be less than or equal to end"):
        list(card_number_generator(10, 1))


def test_card_number_generator_edge_cases() -> None:
    """Тест граничных случаев (минимальный и максимальный номера)."""
    # Первый номер
    assert next(card_number_generator(1, 1)) == "0000 0000 0000 0001"
    # Последний номер
    assert next(card_number_generator(9999999999999999, 9999999999999999)) == "9999 9999 9999 9999"


def test_large_range() -> None:
    gen = card_number_generator(1, 100)
    result = list(gen)
    assert len(result) == 100, "Должен генерировать большой диапазон"
    assert result[0] == "0000 0000 0000 0001", "Первый номер должен быть корректным"
    assert result[-1] == "0000 0000 0000 0100", "Последний номер должен быть корректным"


def test_spacing_in_numbers() -> None:
    gen = card_number_generator(1234567812345678, 1234567812345678)
    number = next(gen)
    parts = number.split(" ")
    assert len(parts) == 4, "Должно быть 4 группы цифр"
    assert all(len(part) == 4 for part in parts), "Каждая группа должна содержать 4 цифры"


@pytest.mark.parametrize(
    "start,end,expected_count",
    [
        (1, 1, 1),
        (1, 100, 100),
        (9999999999999990, 9999999999999999, 10),
    ],
)
def test_card_number_generator_ranges(start, end, expected_count):
    result = list(card_number_generator(start, end))
    assert len(result) == expected_count
