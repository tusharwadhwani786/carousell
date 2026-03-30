"""Command handler for DELETE_LISTING."""

from typing import List

from marketplace.exceptions import ListingNotFoundError, ListingOwnerMismatchError
from marketplace.interfaces import ICommand
from marketplace.services import MarketplaceService


class DeleteListingCommand(ICommand):
    """Handle ``DELETE_LISTING <username> <listing_id>``.

    Deletes a listing only if the requesting user is the owner.
    """

    def __init__(self, service: MarketplaceService) -> None:
        """Initialise with the shared MarketplaceService.

        Args:
            service: The service instance for business logic delegation.
        """
        self._service = service

    def execute(self, args: List[str]) -> str:
        """Delete a listing.

        Args:
            args: ``[username, listing_id]``.
                  ``listing_id`` is parsed as an integer.

        Returns:
            ``"Success"``, ``"Error - listing does not exist"``,
            or ``"Error - listing owner mismatch"``.
        """
        username = args[0]
        listing_id = int(args[1])
        try:
            return self._service.delete_listing(username, listing_id)
        except ListingNotFoundError:
            return "Error - listing does not exist"
        except ListingOwnerMismatchError:
            return "Error - listing owner mismatch"
