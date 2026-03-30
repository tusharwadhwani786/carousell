"""Marketplace service -- the business logic layer."""

from datetime import datetime

from marketplace.exceptions import (
    CategoryNotFoundError,
    ListingNotFoundError,
    ListingOwnerMismatchError,
    UnknownUserError,
)
from marketplace.interfaces import IListingRepository, IUserRepository
from marketplace.models import Listing, User
from marketplace.sorting import SORT_STRATEGIES, SortStrategy


class MarketplaceService:
    """Core business logic for the marketplace.

    All public methods validate user authentication first, then
    delegate to the appropriate repository. Exceptions are raised
    for error conditions; the command layer translates them to
    user-facing error strings.

    Args:
        user_repo: Repository for user persistence.
        listing_repo: Repository for listing persistence.
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        listing_repo: IListingRepository,
    ) -> None:
        self._user_repo = user_repo
        self._listing_repo = listing_repo

    def _validate_user(self, username: str) -> None:
        """Raise UnknownUserError if the username is not registered.

        Complexity: O(1) via hash lookup.
        """
        if not self._user_repo.exists(username):
            raise UnknownUserError(username)

    def register(self, username: str) -> str:
        """Register a new user.

        Args:
            username: Desired username (case-insensitive uniqueness).

        Returns:
            "Success" on successful registration.

        Raises:
            UserAlreadyExistsError: If the username is already taken.

        Complexity: O(1) amortized.
        """
        user = User(username=username)
        self._user_repo.add(user)
        return "Success"

    def create_listing(
        self,
        username: str,
        title: str,
        description: str,
        price: int,
        category: str,
    ) -> str:
        """Create a new listing for a registered user.

        Args:
            username: The seller's username.
            title: Listing title.
            description: Listing description.
            price: Item price (integer).
            category: Category name.

        Returns:
            The string representation of the new listing ID.

        Raises:
            UnknownUserError: If the username is not registered.

        Complexity: O(1) amortized.
        """
        self._validate_user(username)

        listing_id = self._listing_repo.next_id()
        listing = Listing(
            listing_id=listing_id,
            title=title,
            description=description,
            price=price,
            username=username,
            category=category,
            created_at=datetime.now(),
        )
        self._listing_repo.add(listing)
        return str(listing_id)

    def delete_listing(self, username: str, listing_id: int) -> str:
        """Delete a listing, verifying ownership.

        Args:
            username: The user requesting deletion.
            listing_id: The listing to delete.

        Returns:
            "Success" on successful deletion.

        Raises:
            ListingNotFoundError: If the listing ID does not exist.
            ListingOwnerMismatchError: If the user does not own the listing.

        Complexity: O(1).
        """
        listing = self._listing_repo.get_by_id(listing_id)
        if listing is None:
            raise ListingNotFoundError(listing_id)

        if listing.username.lower() != username.lower():
            raise ListingOwnerMismatchError(username, listing_id)

        self._listing_repo.delete(listing_id)
        return "Success"

    def get_listing(self, username: str, listing_id: int) -> str:
        """Retrieve a listing's details.

        Any registered user may view any listing. The username is
        used solely for authentication.

        Args:
            username: The requesting user (for auth check).
            listing_id: The listing to retrieve.

        Returns:
            Pipe-delimited listing detail string.

        Raises:
            UnknownUserError: If the username is not registered.
            ListingNotFoundError: If the listing ID does not exist.

        Complexity: O(1).
        """
        self._validate_user(username)

        listing = self._listing_repo.get_by_id(listing_id)
        if listing is None:
            raise ListingNotFoundError(listing_id)

        return listing.format_detail()

    def get_category(
        self,
        username: str,
        category: str,
        sort_key: str,
        sort_order: str,
    ) -> str:
        """Retrieve all listings in a category, sorted.

        Args:
            username: The requesting user (for auth check).
            category: Category name to filter by.
            sort_key: One of "sort_price" or "sort_time".
            sort_order: One of "asc" or "dsc".

        Returns:
            Newline-separated pipe-delimited listing strings.

        Raises:
            UnknownUserError: If the username is not registered.
            CategoryNotFoundError: If no listings exist in the category.

        Complexity: O(n log n) where n = listings in the category.
        """
        self._validate_user(username)

        listings = self._listing_repo.get_by_category(category)
        if not listings:
            raise CategoryNotFoundError(category)

        strategy: SortStrategy = SORT_STRATEGIES[sort_key]
        ascending = sort_order == "asc"
        sorted_listings = strategy.sort(listings, ascending)

        return "\n".join(listing.format_category() for listing in sorted_listings)

    def get_top_category(self, username: str) -> str:
        """Return the category with the most active listings.

        Optimized for read-heavy use (e.g. home page): reads from
        a pre-maintained counter rather than scanning all listings.

        Args:
            username: The requesting user (for auth check).

        Returns:
            The name of the top category.

        Raises:
            UnknownUserError: If the username is not registered.

        Complexity: O(k) where k = number of distinct categories.
        """
        self._validate_user(username)

        counts = self._listing_repo.get_category_counts()
        if not counts:
            return ""

        top_category = ""
        top_count = -1
        for category, count in counts.items():
            if count >= top_count:
                top_count = count
                top_category = category
        return top_category
