"""Listing domain model."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Listing:
    """Represents an item listed for sale on the marketplace.

    Attributes:
        listing_id: Unique auto-incremented identifier (starts at 100001).
        title: Short title describing the item.
        description: Detailed description of the item.
        price: Item price as an integer (whole currency units).
        username: The seller's username (original case).
        category: Category grouping for the listing.
        created_at: Timestamp when the listing was created.
    """

    listing_id: int
    title: str
    description: str
    price: int
    username: str
    category: str
    created_at: datetime

    def format_detail(self) -> str:
        """Format listing for GET_LISTING output.

        Returns:
            Pipe-delimited string: title|description|price|created_at|category|username
        """
        return (
            f"{self.title}|{self.description}|{self.price}|"
            f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}|"
            f"{self.category}|{self.username}"
        )

    def format_category(self) -> str:
        """Format listing for GET_CATEGORY output.

        Intentionally delegates to ``format_detail`` today. Kept as a
        separate method so that category-specific formatting (e.g.
        omitting certain fields) can be added later without changing
        callers.

        Returns:
            Pipe-delimited string: title|description|price|created_at|category|username
        """
        return self.format_detail()
