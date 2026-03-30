"""
End-to-end integration tests for the Carousell Marketplace CLI.

These tests exercise the full stack from command parsing through
service logic to repository storage, matching the exact expected
output from the assignment specification.
"""

import unittest
from io import StringIO
from unittest.mock import patch

from marketplace.commands import build_registry
from marketplace.parser import InputParser
from marketplace.repositories import (
    InMemoryListingRepository,
    InMemoryUserRepository,
)
from marketplace.services import MarketplaceService


class IntegrationTestBase(unittest.TestCase):
    """Base class that wires up the full stack."""

    def setUp(self) -> None:
        self.user_repo = InMemoryUserRepository()
        self.listing_repo = InMemoryListingRepository()
        self.service = MarketplaceService(self.user_repo, self.listing_repo)
        self.registry = build_registry(self.service)
        self.parser = InputParser()

    def run_command(self, line: str) -> str:
        """Parse and execute a single command line, return the output."""
        name, args = self.parser.parse(line)
        return self.registry.dispatch(name, args)


class TestSpecExample(IntegrationTestBase):
    """Replay the exact example from the assignment specification.

    This test executes each command sequentially and verifies the
    output matches the expected STDOUT from the spec. Timestamps
    are tested with 'assertIn' since they depend on wall-clock time.
    """

    def test_full_spec_flow(self) -> None:
        # REGISTER user1 -> Success
        self.assertEqual(self.run_command("REGISTER user1"), "Success")

        # CREATE_LISTING user1 'Phone model 8' 'Black color, brand new' 1000 'Electronics'
        result = self.run_command(
            "CREATE_LISTING user1 'Phone model 8' 'Black color, brand new' 1000 'Electronics'"
        )
        self.assertEqual(result, "100001")

        # GET_LISTING user1 100001
        result = self.run_command("GET_LISTING user1 100001")
        self.assertTrue(result.startswith("Phone model 8|Black color, brand new|1000|"))
        self.assertTrue(result.endswith("|Electronics|user1"))

        # CREATE_LISTING user1 'Black shoes' 'Training shoes' 100 'Sports'
        result = self.run_command(
            "CREATE_LISTING user1 'Black shoes' 'Training shoes' 100 'Sports'"
        )
        self.assertEqual(result, "100002")

        # REGISTER user2 -> Success
        self.assertEqual(self.run_command("REGISTER user2"), "Success")

        # REGISTER user2 -> Error - user already existing
        self.assertEqual(
            self.run_command("REGISTER user2"), "Error - user already existing"
        )

        # CREATE_LISTING user2 'T-shirt' 'White color' 20 'Sports'
        result = self.run_command(
            "CREATE_LISTING user2 'T-shirt' 'White color' 20 'Sports'"
        )
        self.assertEqual(result, "100003")

        # GET_LISTING user1 100003 (user1 viewing user2's listing)
        result = self.run_command("GET_LISTING user1 100003")
        self.assertTrue(result.startswith("T-shirt|White color|20|"))
        self.assertTrue(result.endswith("|Sports|user2"))

        # GET_CATEGORY user1 'Fashion' sort_time asc -> Error - category not found
        self.assertEqual(
            self.run_command("GET_CATEGORY user1 'Fashion' sort_time asc"),
            "Error - category not found",
        )

        # GET_CATEGORY user1 'Sports' sort_time dsc
        result = self.run_command("GET_CATEGORY user1 'Sports' sort_time dsc")
        lines = result.strip().split("\n")
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("T-shirt|"))
        self.assertTrue(lines[1].startswith("Black shoes|"))

        # GET_CATEGORY user1 'Sports' sort_price dsc
        result = self.run_command("GET_CATEGORY user1 'Sports' sort_price dsc")
        lines = result.strip().split("\n")
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("Black shoes|"))
        self.assertTrue(lines[1].startswith("T-shirt|"))

        # GET_TOP_CATEGORY user1 -> Sports (2 listings vs 1 Electronics)
        self.assertEqual(self.run_command("GET_TOP_CATEGORY user1"), "Sports")

        # DELETE_LISTING user1 100003 -> Error - listing owner mismatch
        self.assertEqual(
            self.run_command("DELETE_LISTING user1 100003"),
            "Error - listing owner mismatch",
        )

        # DELETE_LISTING user2 100003 -> Success
        self.assertEqual(
            self.run_command("DELETE_LISTING user2 100003"), "Success"
        )

        # GET_TOP_CATEGORY user2 -> Sports (tie at 1 each; Sports was most
        # recently active so it wins the tie per iteration order)
        self.assertEqual(self.run_command("GET_TOP_CATEGORY user2"), "Sports")

        # DELETE_LISTING user1 100002 -> Success
        self.assertEqual(
            self.run_command("DELETE_LISTING user1 100002"), "Success"
        )

        # GET_TOP_CATEGORY user1 -> Electronics (only category left)
        self.assertEqual(
            self.run_command("GET_TOP_CATEGORY user1"), "Electronics"
        )

        # GET_TOP_CATEGORY user3 -> Error - unknown user
        self.assertEqual(
            self.run_command("GET_TOP_CATEGORY user3"), "Error - unknown user"
        )


class TestEdgeCases(IntegrationTestBase):
    """Additional edge-case integration tests."""

    def test_category_becomes_empty_after_delete(self) -> None:
        self.run_command("REGISTER user1")
        self.run_command("CREATE_LISTING user1 'Item' 'Desc' 50 'Misc'")
        self.run_command("DELETE_LISTING user1 100001")
        self.assertEqual(
            self.run_command("GET_CATEGORY user1 'Misc' sort_time asc"),
            "Error - category not found",
        )

    def test_multiple_categories_top(self) -> None:
        self.run_command("REGISTER user1")
        self.run_command("CREATE_LISTING user1 'A' 'a' 10 'Cat1'")
        self.run_command("CREATE_LISTING user1 'B' 'b' 20 'Cat2'")
        self.run_command("CREATE_LISTING user1 'C' 'c' 30 'Cat2'")
        self.run_command("CREATE_LISTING user1 'D' 'd' 40 'Cat3'")
        self.run_command("CREATE_LISTING user1 'E' 'e' 50 'Cat3'")
        self.run_command("CREATE_LISTING user1 'F' 'f' 60 'Cat3'")
        self.assertEqual(self.run_command("GET_TOP_CATEGORY user1"), "Cat3")

    def test_get_listing_after_delete_fails(self) -> None:
        self.run_command("REGISTER user1")
        self.run_command("CREATE_LISTING user1 'Item' 'Desc' 100 'Cat'")
        self.run_command("DELETE_LISTING user1 100001")
        self.assertEqual(
            self.run_command("GET_LISTING user1 100001"), "Error - not found"
        )

    def test_create_listing_across_users(self) -> None:
        self.run_command("REGISTER user1")
        self.run_command("REGISTER user2")
        self.run_command("CREATE_LISTING user1 'A' 'a' 10 'Cat'")
        self.run_command("CREATE_LISTING user2 'B' 'b' 20 'Cat'")

        result = self.run_command("GET_CATEGORY user1 'Cat' sort_price asc")
        lines = result.strip().split("\n")
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("A|"))
        self.assertTrue(lines[1].startswith("B|"))

    def test_case_insensitive_user_registration(self) -> None:
        self.assertEqual(self.run_command("REGISTER UserOne"), "Success")
        self.assertEqual(
            self.run_command("REGISTER userone"), "Error - user already existing"
        )

    def test_listing_ids_never_reused(self) -> None:
        """IDs should keep incrementing even after deletions."""
        self.run_command("REGISTER user1")
        id1 = self.run_command("CREATE_LISTING user1 'A' 'a' 10 'Cat'")
        self.run_command("DELETE_LISTING user1 " + id1)
        id2 = self.run_command("CREATE_LISTING user1 'B' 'b' 20 'Cat'")
        self.assertNotEqual(id1, id2)
        self.assertEqual(id1, "100001")
        self.assertEqual(id2, "100002")


class TestMainREPL(unittest.TestCase):
    """Test the actual main() REPL function end-to-end."""

    def test_repl_with_piped_input(self) -> None:
        """Simulate piping commands via STDIN through the real main()."""
        from main import main

        commands = (
            "REGISTER user1\n"
            "CREATE_LISTING user1 'Phone' 'New' 1000 'Electronics'\n"
            "GET_TOP_CATEGORY user1\n"
        )
        stdin = StringIO(commands)
        stdout = StringIO()

        with patch("sys.stdin", stdin), patch("sys.stdout", stdout):
            main()

        output = stdout.getvalue()
        self.assertIn("Success", output)
        self.assertIn("100001", output)
        self.assertIn("Electronics", output)
        self.assertNotIn("# ", output)


if __name__ == "__main__":
    unittest.main()
