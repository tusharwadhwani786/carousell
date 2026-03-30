"""In-memory user repository implementation."""

from typing import Dict, Optional

from marketplace.exceptions.user_already_exists_error import UserAlreadyExistsError
from marketplace.interfaces.i_user_repository import IUserRepository
from marketplace.models.user import User


class InMemoryUserRepository(IUserRepository):
    """Stores users in a dict keyed by normalized (lowercase) username.

    Complexity:
        add:              O(1) amortized
        get_by_username:  O(1)
        exists:           O(1)
    """

    def __init__(self) -> None:
        """Initialise with an empty user store."""
        self._users: Dict[str, User] = {}

    def add(self, user: User) -> None:
        """Add a user, keyed by normalised (lowercase) username.

        Args:
            user: The User to persist.

        Raises:
            UserAlreadyExistsError: If a user with the same normalised
                username is already stored.
        """
        key = user.normalized_username
        if key in self._users:
            raise UserAlreadyExistsError(user.username)
        self._users[key] = user

    def get_by_username(self, username: str) -> Optional[User]:
        """Look up a user by username (case-insensitive).

        Args:
            username: The username to search for.

        Returns:
            The matching User, or None if not found.
        """
        return self._users.get(username.lower())

    def exists(self, username: str) -> bool:
        """Check if a username is registered (case-insensitive).

        Args:
            username: The username to check.

        Returns:
            True if registered, False otherwise.
        """
        return username.lower() in self._users
