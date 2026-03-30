"""Exception for empty category queries."""

from marketplace.exceptions.marketplace_error import MarketplaceError


class CategoryNotFoundError(MarketplaceError):
    """Raised when querying a category that has no listings.

    Attributes:
        category: The category name that was not found.
    """

    def __init__(self, category: str) -> None:
        """Initialise with the missing category name.

        Args:
            category: The category that has no active listings.
        """
        self.category = category
        super().__init__(f"Category '{category}' not found")
