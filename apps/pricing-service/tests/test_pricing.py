import pytest

from app.pricing import calculate_quote


def test_calculates_a_quote() -> None:
    quote = calculate_quote("standard", 3)

    assert quote.daily_rate == 60.0
    assert quote.total == 181.0
    assert quote.currency == "EUR"


def test_normalizes_the_category() -> None:
    quote = calculate_quote(" Premium ", 2)

    assert quote.category == "premium"
    assert quote.total == 200.0


@pytest.mark.parametrize("days", [0, -1])
def test_rejects_an_invalid_duration(days: int) -> None:
    with pytest.raises(ValueError, match="at least one day"):
        calculate_quote("economy", days)


def test_rejects_an_unknown_category() -> None:
    with pytest.raises(ValueError, match="Unknown vehicle category"):
        calculate_quote("utility", 1)
