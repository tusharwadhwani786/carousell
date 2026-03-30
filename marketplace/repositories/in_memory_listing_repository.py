"""In-memory listing repository implementation."""

import itertools
from typing import Dict, List, Optional

from marketplace.interfaces.i_listing_repository import IListingRepository
from marketplace.models.listing import Listing


class InMemoryListingRepository(IListingRepository):
    """Stores listings in a dict keyed by listing ID.

    Maintains an auxiliary ``_category_counts`` dict that tracks
    the number of active listings per category. This is updated on
    every add/delete so that GET_TOP_CATEGORY can run in O(k) where
    k = number of distinct categories, instead of O(n) across all
    listings.

    Complexity:
        add:                  O(1) amortized
        get_by_id:            O(1)
        delete:               O(1)
        get_by_category:      O(n) where n = listings in that category
        next_id:              O(1)
        get_category_counts:  O(1) -- returns the maintained dict
    """

    _STARTING_ID = 100001

    def __init__(self) -> None:
        """Initialise with empty listing store, category counter, and ID generator."""
        self._listings: Dict[int, Listing] = {}
        self._category_counts: Dict[str, int] = {}
        self._id_generator = itertools.count(self._STARTING_ID)

    def add(self, listing: Listing) -> None:
        """Store a listing and increment its category count.

        Args:
            listing: The Listing to persist.
        """
        self._listings[listing.listing_id] = listing
        self._category_counts[listing.category] = (
            self._category_counts.get(listing.category, 0) + 1
        )

    def get_by_id(self, listing_id: int) -> Optional[Listing]:
        """Retrieve a listing by its unique ID.

        Args:
            listing_id: The listing identifier.

        Returns:
            The Listing if found, None otherwise.
        """
        return self._listings.get(listing_id)

    def delete(self, listing_id: int) -> Optional[Listing]:
        """Remove a listing and decrement its category count.

        If the category count reaches zero, the category is removed
        entirely from the counter to keep GET_TOP_CATEGORY accurate.

        Args:
            listing_id: The listing identifier to remove.

        Returns:
            The deleted Listing if it existed, None otherwise.
        """
        listing = self._listings.pop(listing_id, None)
        if listing is not None:
            count = self._category_counts[listing.category] - 1
            if count <= 0:
                del self._category_counts[listing.category]
            else:
                self._category_counts[listing.category] = count
        return listing

    def get_by_category(self, category: str) -> List[Listing]:
        """Retrieve all active listings in a given category.

        Args:
            category: The category name (exact match).

        Returns:
            List of Listings in the category (empty if none found).
        """
        return [
            listing
            for listing in self._listings.values()
            if listing.category == category
        ]

    def next_id(self) -> int:
        """Generate the next unique listing ID.

        IDs are auto-incremented from 100001 and never reused,
        even after deletions.

        Returns:
            The next integer ID.
        """
        return next(self._id_generator)

    def get_category_counts(self) -> Dict[str, int]:
        """Return a snapshot of category-to-listing-count mapping.

        Returns a copy so callers cannot mutate internal state.

        Returns:
            Dict mapping category names to their active listing count.
        """
        return dict(self._category_counts)
