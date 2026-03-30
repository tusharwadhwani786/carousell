"""Exception for duplicate user registration attempts."""

from marketplace.exceptions.marketplace_error import MarketplaceError


class UserAlreadyExistsError(MarketplaceError):
    """Raised when attempting to register a username that already exists.

    Attributes:
        username: The duplicate username that was rejected.
    """

    def __init__(self, username: str) -> None:
        """Initialise with the conflicting username.

        Args:
            username: The username that already exists.
        """
        self.username = username
        super().__init__(f"User '{username}' already exists")
