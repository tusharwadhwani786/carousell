"""Tests for marketplace.sorting."""

import unittest
from datetime import datetime

from marketplace.models import Listing
from marketplace.sorting import (
    SORT_STRATEGIES,
    PriceSortStrategy,
    TimeSortStrategy,
)


class SortingTestBase(unittest.TestCase):
    """Shared fixtures for sorting tests."""

    def setUp(self) -> None:
        self.listings = [
            Listing(100001, "Shoes", "Running shoes", 100, "user1", "Sports",
                    datetime(2024, 1, 15, 10, 0, 0)),
            Listing(100002, "T-shirt", "White", 20, "user2", "Sports",
                    datetime(2024, 1, 15, 11, 0, 0)),
            Listing(100003, "Jacket", "Winter jacket", 200, "user1", "Sports",
                    datetime(2024, 1, 15, 9, 0, 0)),
        ]


class TestPriceSortStrategy(SortingTestBase):
    """Tests for PriceSortStrategy."""

    def setUp(self) -> None:
        super().setUp()
        self.strategy = PriceSortStrategy()

    def test_ascending(self) -> None:
        result = self.strategy.sort(self.listings, ascending=True)
        prices = [l.price for l in result]
        self.assertEqual(prices, [20, 100, 200])

    def test_descending(self) -> None:
        result = self.strategy.sort(self.listings, ascending=False)
        prices = [l.price for l in result]
        self.assertEqual(prices, [200, 100, 20])

    def test_does_not_mutate_original(self) -> None:
        original_ids = [l.listing_id for l in self.listings]
        self.strategy.sort(self.listings, ascending=True)
        current_ids = [l.listing_id for l in self.listings]
        self.assertEqual(original_ids, current_ids)

    def test_empty_list(self) -> None:
        result = self.strategy.sort([], ascending=True)
        self.assertEqual(result, [])

    def test_single_element(self) -> None:
        result = self.strategy.sort([self.listings[0]], ascending=True)
        self.assertEqual(len(result), 1)


class TestTimeSortStrategy(SortingTestBase):
    """Tests for TimeSortStrategy."""

    def setUp(self) -> None:
        super().setUp()
        self.strategy = TimeSortStrategy()

    def test_ascending(self) -> None:
        result = self.strategy.sort(self.listings, ascending=True)
        times = [l.created_at for l in result]
        self.assertEqual(times, sorted(times))

    def test_descending(self) -> None:
        result = self.strategy.sort(self.listings, ascending=False)
        times = [l.created_at for l in result]
        self.assertEqual(times, sorted(times, reverse=True))

    def test_does_not_mutate_original(self) -> None:
        original_ids = [l.listing_id for l in self.listings]
        self.strategy.sort(self.listings, ascending=True)
        current_ids = [l.listing_id for l in self.listings]
        self.assertEqual(original_ids, current_ids)


class TestSortStrategiesRegistry(unittest.TestCase):
    """Tests for the SORT_STRATEGIES mapping."""

    def test_sort_price_registered(self) -> None:
        self.assertIn("sort_price", SORT_STRATEGIES)
        self.assertIsInstance(SORT_STRATEGIES["sort_price"], PriceSortStrategy)

    def test_sort_time_registered(self) -> None:
        self.assertIn("sort_time", SORT_STRATEGIES)
        self.assertIsInstance(SORT_STRATEGIES["sort_time"], TimeSortStrategy)


if __name__ == "__main__":
    unittest.main()
