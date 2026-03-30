"""Abstract interface for user persistence operations."""

from abc import ABC, abstractmethod
from typing import Optional

from marketplace.models.user import User


class IUserRepository(ABC):
    """Interface for user persistence operations."""

    @abstractmethod
    def add(self, user: User) -> None:
        """Persist a new user.

        Args:
            user: The User to store.

        Raises:
            UserAlreadyExistsError: If a user with the same
                normalized username already exists.
        """

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by username (case-insensitive).

        Args:
            username: The username to look up.

        Returns:
            The User if found, None otherwise.
        """

    @abstractmethod
    def exists(self, username: str) -> bool:
        """Check whether a username is registered (case-insensitive).

        Args:
            username: The username to check.

        Returns:
            True if the user exists, False otherwise.
        """
