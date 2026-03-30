"""Tests for marketplace.models."""

import unittest
from datetime import datetime

from marketplace.models import Listing, User


class TestUser(unittest.TestCase):
    """Tests for the User dataclass."""

    def test_creation(self) -> None:
        user = User(username="Alice")
        self.assertEqual(user.username, "Alice")

    def test_normalized_username(self) -> None:
        user = User(username="Alice")
        self.assertEqual(user.normalized_username, "alice")

    def test_frozen_immutability(self) -> None:
        user = User(username="Alice")
        with self.assertRaises(AttributeError):
            user.username = "Bob"  # type: ignore[misc]

    def test_equality(self) -> None:
        self.assertEqual(User(username="Alice"), User(username="Alice"))
        self.assertNotEqual(User(username="Alice"), User(username="alice"))

    def test_hash(self) -> None:
        user_set = {User(username="Alice"), User(username="Alice")}
        self.assertEqual(len(user_set), 1)


class TestListing(unittest.TestCase):
    """Tests for the Listing dataclass."""

    def _make_listing(self, **kwargs) -> Listing:
        defaults = dict(
            listing_id=100001,
            title="Phone",
            description="Brand new",
            price=1000,
            username="user1",
            category="Electronics",
            created_at=datetime(2024, 1, 15, 10, 30, 0),
        )
        defaults.update(kwargs)
        return Listing(**defaults)

    def test_creation(self) -> None:
        listing = self._make_listing()
        self.assertEqual(listing.listing_id, 100001)
        self.assertEqual(listing.title, "Phone")
        self.assertEqual(listing.price, 1000)

    def test_frozen_immutability(self) -> None:
        listing = self._make_listing()
        with self.assertRaises(AttributeError):
            listing.price = 500  # type: ignore[misc]

    def test_format_detail(self) -> None:
        listing = self._make_listing()
        expected = "Phone|Brand new|1000|2024-01-15 10:30:00|Electronics|user1"
        self.assertEqual(listing.format_detail(), expected)

    def test_format_category(self) -> None:
        listing = self._make_listing()
        self.assertEqual(listing.format_category(), listing.format_detail())

    def test_format_detail_with_spaces(self) -> None:
        listing = self._make_listing(
            title="Phone model 8",
            description="Black color, brand new",
        )
        result = listing.format_detail()
        self.assertIn("Phone model 8", result)
        self.assertIn("Black color, brand new", result)

    def test_equality(self) -> None:
        a = self._make_listing()
        b = self._make_listing()
        self.assertEqual(a, b)

    def test_different_listings_not_equal(self) -> None:
        a = self._make_listing(listing_id=100001)
        b = self._make_listing(listing_id=100002)
        self.assertNotEqual(a, b)


if __name__ == "__main__":
    unittest.main()
