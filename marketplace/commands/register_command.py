"""Command handler for REGISTER."""

from typing import List

from marketplace.exceptions import UserAlreadyExistsError
from marketplace.interfaces import ICommand
from marketplace.services import MarketplaceService


class RegisterCommand(ICommand):
    """Handle ``REGISTER <username>``.

    Registers a new user in the marketplace. Returns "Success" or
    the appropriate error string if the user already exists.
    """

    def __init__(self, service: MarketplaceService) -> None:
        """Initialise with the shared MarketplaceService.

        Args:
            service: The service instance for business logic delegation.
        """
        self._service = service

    def execute(self, args: List[str]) -> str:
        """Register a user.

        Args:
            args: ``[username]``.

        Returns:
            ``"Success"`` or ``"Error - user already existing"``.
        """
        username = args[0]
        try:
            return self._service.register(username)
        except UserAlreadyExistsError:
            return "Error - user already existing"
