"""User domain model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Represents a registered marketplace user.

    Attributes:
        username: The display username (original case preserved).
    """

    username: str

    @property
    def normalized_username(self) -> str:
        """Return lowercase username for case-insensitive comparisons."""
        return self.username.lower()
