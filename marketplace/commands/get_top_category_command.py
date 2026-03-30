"""Command handler for GET_TOP_CATEGORY."""

from typing import List

from marketplace.exceptions import UnknownUserError
from marketplace.interfaces import ICommand
from marketplace.services import MarketplaceService


class GetTopCategoryCommand(ICommand):
    """Handle ``GET_TOP_CATEGORY <username>``.

    Returns the category with the highest number of active listings
    across all users. Optimised for read-heavy use via a pre-maintained
    counter.
    """

    def __init__(self, service: MarketplaceService) -> None:
        """Initialise with the shared MarketplaceService.

        Args:
            service: The service instance for business logic delegation.
        """
        self._service = service

    def execute(self, args: List[str]) -> str:
        """Get the top category by listing count.

        Args:
            args: ``[username]``.

        Returns:
            The category name, or ``"Error - unknown user"``.
        """
        username = args[0]
        try:
            return self._service.get_top_category(username)
        except UnknownUserError:
            return "Error - unknown user"
