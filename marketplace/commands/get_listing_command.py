"""Command handler for GET_LISTING."""

from typing import List

from marketplace.exceptions import ListingNotFoundError, UnknownUserError
from marketplace.interfaces import ICommand
from marketplace.services import MarketplaceService


class GetListingCommand(ICommand):
    """Handle ``GET_LISTING <username> <listing_id>``.

    Returns full listing details. Any registered user can view any listing;
    the username is only used for authentication.
    """

    def __init__(self, service: MarketplaceService) -> None:
        """Initialise with the shared MarketplaceService.

        Args:
            service: The service instance for business logic delegation.
        """
        self._service = service

    def execute(self, args: List[str]) -> str:
        """Retrieve listing details.

        Args:
            args: ``[username, listing_id]``.
                  ``listing_id`` is parsed as an integer.

        Returns:
            Pipe-delimited listing string, ``"Error - unknown user"``,
            or ``"Error - not found"``.
        """
        username = args[0]
        listing_id = int(args[1])
        try:
            return self._service.get_listing(username, listing_id)
        except UnknownUserError:
            return "Error - unknown user"
        except ListingNotFoundError:
            return "Error - not found"
