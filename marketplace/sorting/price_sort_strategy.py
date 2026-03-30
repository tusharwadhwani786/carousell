"""Sort strategy for listing price."""

from typing import List

from marketplace.models.listing import Listing
from marketplace.sorting.sort_strategy import SortStrategy


class PriceSortStrategy(SortStrategy):
    """Sorts listings by price.

    Used when the CLI receives ``sort_price`` as the sort key.
    """

    def sort(self, listings: List[Listing], ascending: bool) -> List[Listing]:
        """Sort listings by their integer price.

        Args:
            listings: The listings to sort.
            ascending: True for cheapest-first, False for most-expensive-first.

        Returns:
            A new list sorted by price.
        """
        return sorted(listings, key=lambda l: l.price, reverse=not ascending)
