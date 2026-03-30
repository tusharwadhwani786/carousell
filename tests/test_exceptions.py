"""Tests for marketplace.exceptions."""

import unittest

from marketplace.exceptions import (
    CategoryNotFoundError,
    ListingNotFoundError,
    ListingOwnerMismatchError,
    MarketplaceError,
    UnknownUserError,
    UserAlreadyExistsError,
)


class TestExceptionHierarchy(unittest.TestCase):
    """Verify all exceptions inherit from MarketplaceError."""

    def test_user_already_exists_is_marketplace_error(self) -> None:
        exc = UserAlreadyExistsError("alice")
        self.assertIsInstance(exc, MarketplaceError)
        self.assertEqual(exc.username, "alice")

    def test_unknown_user_is_marketplace_error(self) -> None:
        exc = UnknownUserError("bob")
        self.assertIsInstance(exc, MarketplaceError)
        self.assertEqual(exc.username, "bob")

    def test_listing_not_found_is_marketplace_error(self) -> None:
        exc = ListingNotFoundError(100001)
        self.assertIsInstance(exc, MarketplaceError)
        self.assertEqual(exc.listing_id, 100001)

    def test_listing_owner_mismatch_is_marketplace_error(self) -> None:
        exc = ListingOwnerMismatchError("alice", 100001)
        self.assertIsInstance(exc, MarketplaceError)
        self.assertEqual(exc.username, "alice")
        self.assertEqual(exc.listing_id, 100001)

    def test_category_not_found_is_marketplace_error(self) -> None:
        exc = CategoryNotFoundError("Fashion")
        self.assertIsInstance(exc, MarketplaceError)
        self.assertEqual(exc.category, "Fashion")

    def test_all_have_messages(self) -> None:
        exceptions = [
            UserAlreadyExistsError("alice"),
            UnknownUserError("bob"),
            ListingNotFoundError(100001),
            ListingOwnerMismatchError("alice", 100001),
            CategoryNotFoundError("Fashion"),
        ]
        for exc in exceptions:
            self.assertTrue(str(exc), "Exception should have a message")


if __name__ == "__main__":
    unittest.main()
