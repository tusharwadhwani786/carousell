"""Tests for marketplace.commands and marketplace.parser."""

import unittest

from marketplace.commands import (
    CreateListingCommand,
    DeleteListingCommand,
    GetCategoryCommand,
    GetListingCommand,
    GetTopCategoryCommand,
    RegisterCommand,
    build_registry,
)
from marketplace.parser import InputParser
from marketplace.repositories import (
    InMemoryListingRepository,
    InMemoryUserRepository,
)
from marketplace.services import MarketplaceService


class TestInputParser(unittest.TestCase):
    """Tests for InputParser."""

    def setUp(self) -> None:
        self.parser = InputParser()

    def test_simple_command(self) -> None:
        name, args = self.parser.parse("REGISTER user1")
        self.assertEqual(name, "REGISTER")
        self.assertEqual(args, ["user1"])

    def test_quoted_arguments(self) -> None:
        name, args = self.parser.parse(
            "CREATE_LISTING user1 'Phone model 8' 'Black color' 1000 'Electronics'"
        )
        self.assertEqual(name, "CREATE_LISTING")
        self.assertEqual(args[0], "user1")
        self.assertEqual(args[1], "Phone model 8")
        self.assertEqual(args[2], "Black color")
        self.assertEqual(args[3], "1000")
        self.assertEqual(args[4], "Electronics")

    def test_empty_input_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.parser.parse("")

    def test_command_only(self) -> None:
        name, args = self.parser.parse("GET_TOP_CATEGORY")
        self.assertEqual(name, "GET_TOP_CATEGORY")
        self.assertEqual(args, [])


class CommandTestBase(unittest.TestCase):
    """Shared setup for command tests."""

    def setUp(self) -> None:
        self.user_repo = InMemoryUserRepository()
        self.listing_repo = InMemoryListingRepository()
        self.service = MarketplaceService(self.user_repo, self.listing_repo)


class TestRegisterCommand(CommandTestBase):

    def test_success(self) -> None:
        cmd = RegisterCommand(self.service)
        self.assertEqual(cmd.execute(["user1"]), "Success")

    def test_duplicate(self) -> None:
        cmd = RegisterCommand(self.service)
        cmd.execute(["user1"])
        self.assertEqual(cmd.execute(["user1"]), "Error - user already existing")


class TestCreateListingCommand(CommandTestBase):

    def test_success(self) -> None:
        self.service.register("user1")
        cmd = CreateListingCommand(self.service)
        result = cmd.execute(["user1", "Phone", "New", "1000", "Electronics"])
        self.assertEqual(result, "100001")

    def test_unknown_user(self) -> None:
        cmd = CreateListingCommand(self.service)
        result = cmd.execute(["ghost", "Phone", "New", "1000", "Electronics"])
        self.assertEqual(result, "Error - unknown user")


class TestDeleteListingCommand(CommandTestBase):

    def test_success(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "Phone", "New", 1000, "Electronics")
        cmd = DeleteListingCommand(self.service)
        self.assertEqual(cmd.execute(["user1", "100001"]), "Success")

    def test_not_found(self) -> None:
        cmd = DeleteListingCommand(self.service)
        self.assertEqual(
            cmd.execute(["user1", "999999"]), "Error - listing does not exist"
        )

    def test_owner_mismatch(self) -> None:
        self.service.register("user1")
        self.service.register("user2")
        self.service.create_listing("user1", "Phone", "New", 1000, "Electronics")
        cmd = DeleteListingCommand(self.service)
        self.assertEqual(
            cmd.execute(["user2", "100001"]), "Error - listing owner mismatch"
        )


class TestGetListingCommand(CommandTestBase):

    def test_success(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "Phone", "New", 1000, "Electronics")
        cmd = GetListingCommand(self.service)
        result = cmd.execute(["user1", "100001"])
        self.assertIn("Phone|New|1000|", result)

    def test_unknown_user(self) -> None:
        cmd = GetListingCommand(self.service)
        self.assertEqual(cmd.execute(["ghost", "100001"]), "Error - unknown user")

    def test_not_found(self) -> None:
        self.service.register("user1")
        cmd = GetListingCommand(self.service)
        self.assertEqual(cmd.execute(["user1", "999999"]), "Error - not found")


class TestGetCategoryCommand(CommandTestBase):

    def test_success(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "Phone", "New", 1000, "Electronics")
        cmd = GetCategoryCommand(self.service)
        result = cmd.execute(["user1", "Electronics", "sort_price", "asc"])
        self.assertIn("Phone", result)

    def test_not_found(self) -> None:
        self.service.register("user1")
        cmd = GetCategoryCommand(self.service)
        result = cmd.execute(["user1", "Nonexistent", "sort_time", "asc"])
        self.assertEqual(result, "Error - category not found")

    def test_unknown_user(self) -> None:
        cmd = GetCategoryCommand(self.service)
        result = cmd.execute(["ghost", "Electronics", "sort_time", "asc"])
        self.assertEqual(result, "Error - unknown user")


class TestGetTopCategoryCommand(CommandTestBase):

    def test_success(self) -> None:
        self.service.register("user1")
        self.service.create_listing("user1", "A", "a", 10, "Sports")
        cmd = GetTopCategoryCommand(self.service)
        self.assertEqual(cmd.execute(["user1"]), "Sports")

    def test_unknown_user(self) -> None:
        cmd = GetTopCategoryCommand(self.service)
        self.assertEqual(cmd.execute(["ghost"]), "Error - unknown user")


class TestCommandRegistry(CommandTestBase):

    def test_dispatch(self) -> None:
        registry = build_registry(self.service)
        self.service.register("user1")
        result = registry.dispatch("REGISTER", ["user2"])
        self.assertEqual(result, "Success")

    def test_unknown_command_raises(self) -> None:
        registry = build_registry(self.service)
        with self.assertRaises(KeyError):
            registry.dispatch("UNKNOWN_COMMAND", [])

    def test_all_commands_registered(self) -> None:
        self.service.register("user1")
        registry = build_registry(self.service)
        expected = [
            "REGISTER", "CREATE_LISTING", "DELETE_LISTING",
            "GET_LISTING", "GET_CATEGORY", "GET_TOP_CATEGORY",
        ]
        for cmd_name in expected:
            try:
                registry.dispatch(cmd_name, ["user1", "t", "d", "1", "c"])
            except KeyError:
                self.fail(f"Command '{cmd_name}' is not registered")
            except (IndexError, TypeError, ValueError):
                pass


if __name__ == "__main__":
    unittest.main()
