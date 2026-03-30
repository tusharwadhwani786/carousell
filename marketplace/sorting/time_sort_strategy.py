"""Sort strategy for listing creation time."""

from typing import List

from marketplace.models.listing import Listing
from marketplace.sorting.sort_strategy import SortStrategy


class TimeSortStrategy(SortStrategy):
    """Sorts listings by creation timestamp.

    Used when the CLI receives ``sort_time`` as the sort key.
    """

    def sort(self, listings: List[Listing], ascending: bool) -> List[Listing]:
        """Sort listings by their creation datetime.

        Args:
            listings: The listings to sort.
            ascending: True for oldest-first, False for newest-first.

        Returns:
            A new list sorted by creation time.
        """
        return sorted(
            listings, key=lambda l: l.created_at, reverse=not ascending
        )
