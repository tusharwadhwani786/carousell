"""Abstract interface for listing persistence operations."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from marketplace.models.listing import Listing


class IListingRepository(ABC):
    """Interface for listing persistence operations."""

    @abstractmethod
    def add(self, listing: Listing) -> None:
        """Persist a new listing.

        Args:
            listing: The Listing to store.
        """

    @abstractmethod
    def get_by_id(self, listing_id: int) -> Optional[Listing]:
        """Retrieve a listing by its unique ID.

        Args:
            listing_id: The listing identifier.

        Returns:
            The Listing if found, None otherwise.
        """

    @abstractmethod
    def delete(self, listing_id: int) -> Optional[Listing]:
        """Remove a listing by ID and return it.

        Args:
            listing_id: The listing identifier.

        Returns:
            The deleted Listing if it existed, None otherwise.
        """

    @abstractmethod
    def get_by_category(self, category: str) -> List[Listing]:
        """Retrieve all listings belonging to a category.

        Args:
            category: The category name (exact match).

        Returns:
            List of Listings in the given category (may be empty).
        """

    @abstractmethod
    def next_id(self) -> int:
        """Generate the next unique listing ID.

        Returns:
            An integer ID, auto-incremented from 100001.
        """

    @abstractmethod
    def get_category_counts(self) -> Dict[str, int]:
        """Return a mapping of category name to active listing count.

        Returns:
            Dict where keys are category names and values are the
            number of active (non-deleted) listings in that category.
        """
