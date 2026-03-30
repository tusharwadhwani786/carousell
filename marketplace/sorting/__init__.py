"""Sorting strategies for marketplace listings.

Implements the Strategy pattern to decouple sort logic from the
service layer. Each strategy encapsulates one sort dimension
(price or creation time) and supports ascending/descending order.

Adding a new sort dimension requires only a new SortStrategy
subclass -- no changes to existing code (Open/Closed Principle).
"""

from marketplace.sorting.price_sort_strategy import PriceSortStrategy
from marketplace.sorting.sort_strategy import SortStrategy
from marketplace.sorting.time_sort_strategy import TimeSortStrategy

SORT_STRATEGIES = {
    "sort_price": PriceSortStrategy(),
    "sort_time": TimeSortStrategy(),
}
"""Registry mapping sort field names from the CLI protocol to strategy instances."""

__all__ = [
    "SortStrategy",
    "PriceSortStrategy",
    "TimeSortStrategy",
    "SORT_STRATEGIES",
]
