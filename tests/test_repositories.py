"""Tests for marketplace.repositories."""

import unittest
from datetime import datetime

from marketplace.exceptions import UserAlreadyExistsError
from marketplace.models import Listing, User
from marketplace.repositories import (
    InMemoryListingRepository,
    InMemoryUserRepository,
)


class TestInMemoryUserRepository(unittest.TestCase):
    """Tests for InMemoryUserRepository."""

    def setUp(self) -> None:
        self.repo = InMemoryUserRepository()

    def test_add_and_get(self) -> None:
        user = User(username="Alice")
        self.repo.add(user)
        result = self.repo.get_by_username("Alice")
        self.assertEqual(result, user)

    def test_case_insensitive_lookup(self) -> None:
        self.repo.add(User(username="Alice"))
        self.assertIsNotNone(self.repo.get_by_username("alice"))
        self.assertIsNotNone(self.repo.get_by_username("ALICE"))
        self.assertIsNotNone(self.repo.get_by_username("aLiCe"))

    def test_exists(self) -> None:
        self.assertFalse(self.repo.exists("Alice"))
        self.repo.add(User(username="Alice"))
        self.assertTrue(self.repo.exists("Alice"))
        self.assertTrue(self.repo.exists("alice"))

    def test_get_nonexistent_returns_none(self) -> None:
        self.assertIsNone(self.repo.get_by_username("ghost"))

    def test_duplicate_raises_error(self) -> None:
        self.repo.add(User(username="Alice"))
        with self.assertRaises(UserAlreadyExistsError):
            self.repo.add(User(username="alice"))

    def test_duplicate_exact_case_raises_error(self) -> None:
        self.repo.add(User(username="Alice"))
        with self.assertRaises(UserAlreadyExistsError):
            self.repo.add(User(username="Alice"))

    def test_multiple_users(self) -> None:
        self.repo.add(User(username="Alice"))
        self.repo.add(User(username="Bob"))
        self.assertTrue(self.repo.exists("Alice"))
        self.assertTrue(self.repo.exists("Bob"))
        self.assertFalse(self.repo.exists("Charlie"))


class TestInMemoryListingRepository(unittest.TestCase):
    """Tests for InMemoryListingRepository."""

    def setUp(self) -> None:
        self.repo = InMemoryListingRepository()

    def _make_listing(self, listing_id: int = 100001, **kwargs) -> Listing:
        defaults = dict(
            listing_id=listing_id,
            title="Phone",
            description="Brand new",
            price=1000,
            username="user1",
            category="Electronics",
            created_at=datetime(2024, 1, 15, 10, 30, 0),
        )
        defaults.update(kwargs)
        return Listing(**defaults)

    def test_next_id_starts_at_100001(self) -> None:
        self.assertEqual(self.repo.next_id(), 100001)

    def test_next_id_increments(self) -> None:
        ids = [self.repo.next_id() for _ in range(5)]
        self.assertEqual(ids, [100001, 100002, 100003, 100004, 100005])

    def test_add_and_get(self) -> None:
        listing = self._make_listing()
        self.repo.add(listing)
        result = self.repo.get_by_id(100001)
        self.assertEqual(result, listing)

    def test_get_nonexistent_returns_none(self) -> None:
        self.assertIsNone(self.repo.get_by_id(999999))

    def test_delete_returns_listing(self) -> None:
        listing = self._make_listing()
        self.repo.add(listing)
        deleted = self.repo.delete(100001)
        self.assertEqual(deleted, listing)
        self.assertIsNone(self.repo.get_by_id(100001))

    def test_delete_nonexistent_returns_none(self) -> None:
        self.assertIsNone(self.repo.delete(999999))

    def test_get_by_category(self) -> None:
        self.repo.add(self._make_listing(100001, category="Electronics"))
        self.repo.add(self._make_listing(100002, category="Sports"))
        self.repo.add(self._make_listing(100003, category="Electronics"))

        electronics = self.repo.get_by_category("Electronics")
        self.assertEqual(len(electronics), 2)

        sports = self.repo.get_by_category("Sports")
        self.assertEqual(len(sports), 1)

    def test_get_by_category_empty(self) -> None:
        result = self.repo.get_by_category("Nonexistent")
        self.assertEqual(result, [])

    def test_category_counts_on_add(self) -> None:
        self.repo.add(self._make_listing(100001, category="Electronics"))
        self.repo.add(self._make_listing(100002, category="Electronics"))
        self.repo.add(self._make_listing(100003, category="Sports"))

        counts = self.repo.get_category_counts()
        self.assertEqual(counts["Electronics"], 2)
        self.assertEqual(counts["Sports"], 1)

    def test_category_counts_on_delete(self) -> None:
        self.repo.add(self._make_listing(100001, category="Electronics"))
        self.repo.add(self._make_listing(100002, category="Electronics"))
        self.repo.delete(100001)

        counts = self.repo.get_category_counts()
        self.assertEqual(counts["Electronics"], 1)

    def test_category_removed_when_count_reaches_zero(self) -> None:
        self.repo.add(self._make_listing(100001, category="Electronics"))
        self.repo.delete(100001)

        counts = self.repo.get_category_counts()
        self.assertNotIn("Electronics", counts)

    def test_category_counts_empty(self) -> None:
        self.assertEqual(self.repo.get_category_counts(), {})

    def test_category_counts_returns_copy(self) -> None:
        self.repo.add(self._make_listing(100001, category="Electronics"))
        counts = self.repo.get_category_counts()
        counts["Electronics"] = 999
        self.assertEqual(self.repo.get_category_counts()["Electronics"], 1)


if __name__ == "__main__":
    unittest.main()
