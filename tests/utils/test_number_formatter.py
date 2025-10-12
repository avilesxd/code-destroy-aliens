import pytest

from src.utils.number_formatter import NumberFormatter


@pytest.fixture
def formatter() -> NumberFormatter:
    return NumberFormatter(decimals=1)


def test_less_than_1000(formatter: NumberFormatter) -> None:
    assert formatter.format(999) == "999"
    assert formatter.format(1) == "1"
    assert formatter.format(0) == "0"


def test_thousands(formatter: NumberFormatter) -> None:
    assert formatter.format(1000) == "1K"
    assert formatter.format(1500) == "1.5K"
    assert formatter.format(19999) == "20K"


def test_millions(formatter: NumberFormatter) -> None:
    assert formatter.format(1_000_000) == "1M"
    assert formatter.format(2_500_000) == "2.5M"


def test_billions(formatter: NumberFormatter) -> None:
    assert formatter.format(1_000_000_000) == "1B"
    assert formatter.format(3_400_000_000) == "3.4B"


def test_trillions(formatter: NumberFormatter) -> None:
    assert formatter.format(1_000_000_000_000) == "1T"
    assert formatter.format(5_600_000_000_000) == "5.6T"


def test_quadrillions(formatter: NumberFormatter) -> None:
    assert formatter.format(1_000_000_000_000_000) == "1Qa"
    assert formatter.format(7_800_000_000_000_000) == "7.8Qa"


def test_no_decimals() -> None:
    formatter = NumberFormatter(decimals=1)
    assert formatter.format(1250) == "1.2K"
    assert formatter.format(2_500_000) == "2.5M"


def test_high_precision() -> None:
    formatter = NumberFormatter(decimals=3)
    assert formatter.format(1234) == "1.234K"
    assert formatter.format(5_678_900) == "5.679M"


def test_negative_number() -> None:
    formatter = NumberFormatter()
    with pytest.raises(ValueError, match="non-negative"):
        formatter.format(-1000)


def test_invalid_type_string() -> None:
    formatter = NumberFormatter()
    with pytest.raises(TypeError, match="int or float"):
        formatter.format("1000")  # type: ignore[arg-type]


def test_invalid_type_none() -> None:
    formatter = NumberFormatter()
    with pytest.raises(TypeError, match="int or float"):
        formatter.format(None)  # type: ignore[arg-type]


def test_invalid_type_list() -> None:
    formatter = NumberFormatter()
    with pytest.raises(TypeError, match="int or float"):
        formatter.format([1000])  # type: ignore[arg-type]
