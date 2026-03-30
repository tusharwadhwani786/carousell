"""Tests for marketplace.services."""

import unittest

from marketplace.exceptions import (
    CategoryNotFoundError,
    ListingNotFoundError,
    ListingOwnerMismatchError,
    UnknownUserError,
    UserAlreadyExistsError,
)
from marketplace.repositories import (
    InMemoryListingRepository,
    InMemoryUserRepository,
)
from marketplace.services import MarketplaceService


class TestMarketplaceService(unittest.TestCase):
    """Tests for MarketplaceService business logic."""

    def setUp(self) -> None:
        self.user_repo = InMemoryUserRepository()
        self.listing_repo = InMemoryListingRepository()
        self.service = MarketplaceService(self.user_repo, self.listing_repo)

    # --- REGISTER ---

    def test_register_success(self) -> None:
        result = self.service.register("user1")
        self.assertEqual(result, "Success")

    def test_register_duplicate_raises(self) -> None:
        self.service.register("user1")
        with self.assertRaises(UserAlreadyExistsError):
            self.service.register("user1")

    def test_register_case_insensitive_duplicate(self) -> None:
        self.service.register("User1")
        with self.assertRaises(UserAlreadyExistsError):
            self.service.register("user1")

    # --- CREATE_LISTING ---

    def test_create_listing_returns_id(self) -> None:
        self.service.register("user1")
        result = self.service.create_listing(
            "user1", "Phone", "Brand new", 1000, "Electronics"
        )
        self.assertEqual(result, "100001")

    def test_create_listing_increments_id(self) -> None:
        self.service.register("user1")
        id1 = self.service.create_listing("user1", "A", "a", 10, "Cat1")
        id2 = self.service.create_listing("user1", "B", "b", 20, "Cat2")
        self.assertEqual(id1, "100001")
        self.assertEqual(id2, "100002")

    def test_create_listing_unknown_user(self) -> None:
        with self.assertRaises(UnknownUserError):
            self.service.create_listing(
                "ghost", "Phone", "Brand new", 1000, "Electronics"
            )

    # --- DELETE_LISTING ---

    def test_delete_listing_success(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "Phone", "New", 1000, "Electronics")
        result = self.service.delete_listing("user1", 100001)
        self.assertEqual(result, "Success")

    def test_delete_listing_not_found(self) -> None:
        with self.assertRaises(ListingNotFoundError):
            self.service.delete_listing("user1", 999999)

    def test_delete_listing_owner_mismatch(self) -> None:
        self.service.register("user1")
        self.service.register("user2")
        self.service.create_listing("user1", "Phone", "New", 1000, "Electronics")
        with self.assertRaises(ListingOwnerMismatchError):
            self.service.delete_listing("user2", 100001)

    def test_delete_listing_already_deleted(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "Phone", "New", 1000, "Electronics")
        self.service.delete_listing("user1", 100001)
        with self.assertRaises(ListingNotFoundError):
            self.service.delete_listing("user1", 100001)

    # --- GET_LISTING ---

    def test_get_listing_success(self) -> None:
        self.service.register("user1")
        self.service.create_listing(
            "user1", "Phone model 8", "Black color, brand new", 1000, "Electronics"
        )
        result = self.service.get_listing("user1", 100001)
        self.assertIn("Phone model 8", result)
        self.assertIn("Black color, brand new", result)
        self.assertIn("1000", result)
        self.assertIn("Electronics", result)
        self.assertIn("user1", result)

    def test_get_listing_any_user_can_view(self) -> None:
        self.service.register("user1")
        self.service.register("user2")
        self.service.create_listing("user1", "Phone", "New", 1000, "Electronics")
        result = self.service.get_listing("user2", 100001)
        self.assertIn("Phone", result)

    def test_get_listing_unknown_user(self) -> None:
        with self.assertRaises(UnknownUserError):
            self.service.get_listing("ghost", 100001)

    def test_get_listing_not_found(self) -> None:
        self.service.register("user1")
        with self.assertRaises(ListingNotFoundError):
            self.service.get_listing("user1", 999999)

    # --- GET_CATEGORY ---

    def test_get_category_sort_time_asc(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "A", "desc_a", 100, "Sports")
        self.service.create_listing("user1", "B", "desc_b", 200, "Sports")

        result = self.service.get_category("user1", "Sports", "sort_time", "asc")
        lines = result.strip().split("\n")
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("A|"))
        self.assertTrue(lines[1].startswith("B|"))

    def test_get_category_sort_time_dsc(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "A", "desc_a", 100, "Sports")
        self.service.create_listing("user1", "B", "desc_b", 200, "Sports")

        result = self.service.get_category("user1", "Sports", "sort_time", "dsc")
        lines = result.strip().split("\n")
        self.assertTrue(lines[0].startswith("B|"))
        self.assertTrue(lines[1].startswith("A|"))

    def test_get_category_sort_price_asc(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "Expensive", "e", 500, "Sports")
        self.service.create_listing("user1", "Cheap", "c", 10, "Sports")

        result = self.service.get_category("user1", "Sports", "sort_price", "asc")
        lines = result.strip().split("\n")
        self.assertTrue(lines[0].startswith("Cheap|"))
        self.assertTrue(lines[1].startswith("Expensive|"))

    def test_get_category_sort_price_dsc(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "Expensive", "e", 500, "Sports")
        self.service.create_listing("user1", "Cheap", "c", 10, "Sports")

        result = self.service.get_category("user1", "Sports", "sort_price", "dsc")
        lines = result.strip().split("\n")
        self.assertTrue(lines[0].startswith("Expensive|"))
        self.assertTrue(lines[1].startswith("Cheap|"))

    def test_get_category_not_found(self) -> None:
        self.service.register("user1")
        with self.assertRaises(CategoryNotFoundError):
            self.service.get_category("user1", "Nonexistent", "sort_time", "asc")

    def test_get_category_unknown_user(self) -> None:
        with self.assertRaises(UnknownUserError):
            self.service.get_category("ghost", "Sports", "sort_time", "asc")

    # --- GET_TOP_CATEGORY ---

    def test_get_top_category(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "A", "a", 10, "Electronics")
        self.service.create_listing("user1", "B", "b", 20, "Sports")
        self.service.create_listing("user1", "C", "c", 30, "Sports")

        result = self.service.get_top_category("user1")
        self.assertEqual(result, "Sports")

    def test_get_top_category_after_delete(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "A", "a", 10, "Electronics")
        self.service.create_listing("user1", "B", "b", 20, "Sports")
        self.service.create_listing("user1", "C", "c", 30, "Sports")

        self.service.delete_listing("user1", 100002)
        self.service.delete_listing("user1", 100003)

        result = self.service.get_top_category("user1")
        self.assertEqual(result, "Electronics")

    def test_get_top_category_unknown_user(self) -> None:
        with self.assertRaises(UnknownUserError):
            self.service.get_top_category("ghost")

    def test_get_top_category_empty_marketplace(self) -> None:
        self.service.register("user1")
        result = self.service.get_top_category("user1")
        self.assertEqual(result, "")

    def test_get_top_category_considers_all_users(self) -> None:
        self.service.register("user1")
        self.service.register("user2")
        self.service.create_listing("user1", "A", "a", 10, "Electronics")
        self.service.create_listing("user2", "B", "b", 20, "Sports")
        self.service.create_listing("user2", "C", "c", 30, "Sports")

        result = self.service.get_top_category("user1")
        self.assertEqual(result, "Sports")


if __name__ == "__main__":
    unittest.main()
