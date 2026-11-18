from dataclasses import dataclass

DAILY_RATES = {
    "economy": 40.0,
    "standard": 60.0,
    "premium": 100.0,
}


@dataclass(frozen=True)
class Quote:
    category: str
    days: int
    daily_rate: float
    total: float
    currency: str = "EUR"


def calculate_quote(category: str, days: int) -> Quote:
    """Calculate a deterministic quote for a vehicle category."""
    normalized_category = category.strip().lower()

    if normalized_category not in DAILY_RATES:
        raise ValueError(f"Unknown vehicle category: {category}")
    if days < 1:
        raise ValueError("The rental duration must be at least one day")

    daily_rate = DAILY_RATES[normalized_category]
    return Quote(
        category=normalized_category,
        days=days,
        daily_rate=daily_rate,
        total=round(daily_rate * days, 2),
    )
