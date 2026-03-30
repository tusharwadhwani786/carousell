"""Typed exception hierarchy for the Carousell Marketplace.

Each exception maps to a specific error condition defined in the spec.
Commands catch these and return the exact error strings required by the
protocol, avoiding brittle string matching or generic exception handling.
"""

from marketplace.exceptions.category_not_found_error import CategoryNotFoundError
from marketplace.exceptions.listing_not_found_error import ListingNotFoundError
from marketplace.exceptions.listing_owner_mismatch_error import (
    ListingOwnerMismatchError,
)
from marketplace.exceptions.marketplace_error import MarketplaceError
from marketplace.exceptions.unknown_user_error import UnknownUserError
from marketplace.exceptions.user_already_exists_error import UserAlreadyExistsError

__all__ = [
    "MarketplaceError",
    "UserAlreadyExistsError",
    "UnknownUserError",
    "ListingNotFoundError",
    "ListingOwnerMismatchError",
    "CategoryNotFoundError",
]
