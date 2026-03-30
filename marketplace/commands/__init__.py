"""Command implementations and registry for the marketplace CLI.

Each command class implements ``ICommand``, keeping argument parsing
thin and delegating business logic to ``MarketplaceService``. The
``CommandRegistry`` maps command names to handler instances, making
it trivial to add new commands without modifying existing code
(Open/Closed Principle).
"""

from marketplace.commands.command_registry import CommandRegistry, build_registry
from marketplace.commands.create_listing_command import CreateListingCommand
from marketplace.commands.delete_listing_command import DeleteListingCommand
from marketplace.commands.get_category_command import GetCategoryCommand
from marketplace.commands.get_listing_command import GetListingCommand
from marketplace.commands.get_top_category_command import GetTopCategoryCommand
from marketplace.commands.register_command import RegisterCommand

__all__ = [
    "RegisterCommand",
    "CreateListingCommand",
    "DeleteListingCommand",
    "GetListingCommand",
    "GetCategoryCommand",
    "GetTopCategoryCommand",
    "CommandRegistry",
    "build_registry",
]
