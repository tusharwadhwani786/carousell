"""Command registry and factory wiring."""

from typing import Dict, List

from marketplace.commands.create_listing_command import CreateListingCommand
from marketplace.commands.delete_listing_command import DeleteListingCommand
from marketplace.commands.get_category_command import GetCategoryCommand
from marketplace.commands.get_listing_command import GetListingCommand
from marketplace.commands.get_top_category_command import GetTopCategoryCommand
from marketplace.commands.register_command import RegisterCommand
from marketplace.interfaces import ICommand
from marketplace.services import MarketplaceService


class CommandRegistry:
    """Maps command names to ICommand instances.

    Usage:
        registry = CommandRegistry()
        registry.register("REGISTER", RegisterCommand(service))
        result = registry.dispatch("REGISTER", ["user1"])
    """

    def __init__(self) -> None:
        """Initialise with an empty command mapping."""
        self._commands: Dict[str, ICommand] = {}

    def register(self, name: str, command: ICommand) -> None:
        """Register a command handler under the given name.

        Args:
            name: The command name as it appears on STDIN (e.g. "REGISTER").
            command: The ICommand instance to handle this command.
        """
        self._commands[name] = command

    def dispatch(self, name: str, args: List[str]) -> str:
        """Look up and execute a command.

        Args:
            name: The command name from parsed input.
            args: The remaining arguments.

        Returns:
            The command's string output for STDOUT.

        Raises:
            KeyError: If the command name is not registered.
        """
        command = self._commands[name]
        return command.execute(args)


def build_registry(service: MarketplaceService) -> CommandRegistry:
    """Wire up all commands and return a ready-to-use registry.

    This factory function is the single place where commands are
    registered. To add a new command, create its class and add
    one line here.

    Args:
        service: The MarketplaceService instance to inject into commands.

    Returns:
        A fully configured CommandRegistry.
    """
    registry = CommandRegistry()
    registry.register("REGISTER", RegisterCommand(service))
    registry.register("CREATE_LISTING", CreateListingCommand(service))
    registry.register("DELETE_LISTING", DeleteListingCommand(service))
    registry.register("GET_LISTING", GetListingCommand(service))
    registry.register("GET_CATEGORY", GetCategoryCommand(service))
    registry.register("GET_TOP_CATEGORY", GetTopCategoryCommand(service))
    return registry
