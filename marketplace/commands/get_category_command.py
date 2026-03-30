"""Command handler for GET_CATEGORY."""

from typing import List

from marketplace.exceptions import CategoryNotFoundError, UnknownUserError
from marketplace.interfaces import ICommand
from marketplace.services import MarketplaceService


class GetCategoryCommand(ICommand):
    """Handle ``GET_CATEGORY <username> <category> <sort_key> <sort_order>``.

    Returns all listings in a category, sorted by the specified field
    and direction.
    """

    def __init__(self, service: MarketplaceService) -> None:
        """Initialise with the shared MarketplaceService.

        Args:
            service: The service instance for business logic delegation.
        """
        self._service = service

    def execute(self, args: List[str]) -> str:
        """List all items in a category, sorted.

        Args:
            args: ``[username, category, sort_key, sort_order]``.
                  ``sort_key`` is ``"sort_price"`` or ``"sort_time"``.
                  ``sort_order`` is ``"asc"`` or ``"dsc"``.

        Returns:
            Newline-separated listing strings, ``"Error - unknown user"``,
            or ``"Error - category not found"``.
        """
        username = args[0]
        category = args[1]
        sort_key = args[2]
        sort_order = args[3]
        try:
            return self._service.get_category(
                username, category, sort_key, sort_order
            )
        except UnknownUserError:
            return "Error - unknown user"
        except CategoryNotFoundError:
            return "Error - category not found"
