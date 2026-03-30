"""Exception for unregistered user references."""

from marketplace.exceptions.marketplace_error import MarketplaceError


class UnknownUserError(MarketplaceError):
    """Raised when a command references a username that is not registered.

    Attributes:
        username: The unrecognised username.
    """

    def __init__(self, username: str) -> None:
        """Initialise with the unknown username.

        Args:
            username: The username that was not found.
        """
        self.username = username
        super().__init__(f"Unknown user '{username}'")
