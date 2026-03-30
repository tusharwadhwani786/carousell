"""Exception for missing listing lookups."""

from marketplace.exceptions.marketplace_error import MarketplaceError


class ListingNotFoundError(MarketplaceError):
    """Raised when a listing ID does not exist in the marketplace.

    Attributes:
        listing_id: The ID that was not found.
    """

    def __init__(self, listing_id: int) -> None:
        """Initialise with the missing listing ID.

        Args:
            listing_id: The listing ID that does not exist.
        """
        self.listing_id = listing_id
        super().__init__(f"Listing {listing_id} not found")
