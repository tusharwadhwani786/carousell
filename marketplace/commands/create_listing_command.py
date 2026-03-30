"""Command handler for CREATE_LISTING."""

from typing import List

from marketplace.exceptions import UnknownUserError
from marketplace.interfaces import ICommand
from marketplace.services import MarketplaceService


class CreateListingCommand(ICommand):
    """Handle ``CREATE_LISTING <username> <title> <description> <price> <category>``.

    Creates a new listing for a registered user and returns the
    auto-generated listing ID.
    """

    def __init__(self, service: MarketplaceService) -> None:
        """Initialise with the shared MarketplaceService.

        Args:
            service: The service instance for business logic delegation.
        """
        self._service = service

    def execute(self, args: List[str]) -> str:
        """Create a listing.

        Args:
            args: ``[username, title, description, price, category]``.
                  ``price`` is parsed as an integer.

        Returns:
            The new listing ID as a string, or ``"Error - unknown user"``.
        """
        username = args[0]
        title = args[1]
        description = args[2]
        price = int(args[3])
        category = args[4]
        try:
            return self._service.create_listing(
                username, title, description, price, category
            )
        except UnknownUserError:
            return "Error - unknown user"
