"""Exception for listing ownership violations."""

from marketplace.exceptions.marketplace_error import MarketplaceError


class ListingOwnerMismatchError(MarketplaceError):
    """Raised when a user tries to delete a listing they do not own.

    Attributes:
        username: The user who attempted the deletion.
        listing_id: The listing that was targeted.
    """

    def __init__(self, username: str, listing_id: int) -> None:
        """Initialise with the mismatched user and listing.

        Args:
            username: The user who tried to delete the listing.
            listing_id: The listing they do not own.
        """
        self.username = username
        self.listing_id = listing_id
        super().__init__(
            f"User '{username}' does not own listing {listing_id}"
        )
