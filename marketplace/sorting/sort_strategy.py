"""Abstract base for listing sort strategies."""

from abc import ABC, abstractmethod
from typing import List

from marketplace.models.listing import Listing


class SortStrategy(ABC):
    """Abstract base for listing sort strategies."""

    @abstractmethod
    def sort(self, listings: List[Listing], ascending: bool) -> List[Listing]:
        """Sort a list of listings in the specified order.

        Args:
            listings: The listings to sort.
            ascending: True for ascending order, False for descending.

        Returns:
            A new sorted list (original is not mutated).
        """
