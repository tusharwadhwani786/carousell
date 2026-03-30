"""Abstract base classes (interfaces) for the Carousell Marketplace.

These ABCs define the contracts that concrete implementations must
fulfil. The service layer depends only on these abstractions,
enabling dependency injection and easy substitution for testing
or future persistence backends.
"""

from marketplace.interfaces.i_command import ICommand
from marketplace.interfaces.i_listing_repository import IListingRepository
from marketplace.interfaces.i_user_repository import IUserRepository

__all__ = ["IUserRepository", "IListingRepository", "ICommand"]
