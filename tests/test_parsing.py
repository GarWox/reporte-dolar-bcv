import pytest

from dolar_monitor.models import spread_pct
from dolar_monitor.parsing import parse_ves_number


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("36,58720000", 36.5872),
        ("1.234,56", 1234.56),
        ("36.5872", 36.5872),
        (" 42,1056\xa0", 42.1056),
    ],
)
def test_parse_ves_number(raw: str, expected: float) -> None:
    assert parse_ves_number(raw) == expected


@pytest.mark.parametrize("raw", ["", "   ", "abc"])
def test_parse_ves_number_rejects_invalid_values(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_ves_number(raw)


def test_spread_pct() -> None:
    assert spread_pct(40.25, 36.5872) == 10.01
    assert spread_pct(40.9, 36.5872) == 11.79


def test_spread_pct_without_reference() -> None:
    assert spread_pct(40.25, None) is None
    assert spread_pct(None, 36.5) is None
    assert spread_pct(40.25, 0) is None
